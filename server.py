#!/usr/bin/env python3
"""Local server behind the proposal UI.

Serves ui/index.html, discovers the guides in guides/ and the person profiles in
this folder, and assembles the prompt for a job description. If ANTHROPIC_API_KEY
is set it will also generate the proposal directly; without a key it runs in
manual mode, where you copy the prompt into Claude Code and paste the reply back.

    ./run-ui.sh            # then open http://localhost:8765
"""

import json
import os
import re
import sys
import threading
import time
import uuid
import datetime
import html
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
GUIDES = ROOT / "guides"
UI = ROOT / "ui"
PORT = int(os.environ.get("PROPOSAL_UI_PORT", "8765"))
MODEL = os.environ.get("PROPOSAL_UI_MODEL", "claude-opus-5")

# A person profile is a root .md file with a single-word name: Mario.md, Zachary.md.
# Everything else at the root (CLAUDE.md, proposal-*.md, working notes) is skipped.
NOT_A_PERSON = {"CLAUDE.md", "README.md", "MEMORY.md"}

# Job queue. Without an API key the UI hands the job to the Claude Code session
# that is watching this queue, and polls until the proposal comes back.
JOBS = {}
JOBS_LOCK = threading.Lock()
MSG_SEQ = [0]  # monotonic id so the watcher can poll for anything new
JOBS_DIR = ROOT / ".jobs"
PROPOSALS = ROOT / "proposals"   # readable local archive, one markdown file per proposal
QUEUE_DIR = ROOT / ".queue"      # jobs pulled off the relay, waiting to be written

# History retention. Jobs are kept in .jobs/*.json on this machine, never in the
# browser, and older ones are purged on a daily boundary anchored to Japan time.
JST = datetime.timezone(datetime.timedelta(hours=9))
PURGE_AT_JST = (20, 30)      # 8:30pm JST
RETENTION_DAYS = 3           # anything older than this at the boundary goes


def next_purge_epoch(now=None):
    """Epoch seconds of the next 20:30 JST boundary."""
    now = now or datetime.datetime.now(tz=JST)
    target = now.replace(hour=PURGE_AT_JST[0], minute=PURGE_AT_JST[1],
                         second=0, microsecond=0)
    if target <= now:
        target += datetime.timedelta(days=1)
    return target.timestamp()


def purge_old_jobs():
    """Drop jobs older than RETENTION_DAYS. A pending boost is never purged."""
    cutoff = time.time() - RETENTION_DAYS * 86400
    removed = []
    with JOBS_LOCK:
        for job_id, job in list(JOBS.items()):
            if job.get("created", 0) >= cutoff:
                continue
            # Still waiting on a boost the user has not ticked off: keep it.
            if job.get("boost") == "yes" and not job.get("done"):
                continue
            JOBS.pop(job_id, None)
            f = JOBS_DIR / f"{job_id}.json"
            if f.is_file():
                f.unlink()
            # The markdown in proposals/ is deliberately left alone. Retention
            # trims the working list, it does not throw away finished work.
            removed.append(job_id)
    if removed:
        print(f"  purged {len(removed)} job(s) older than {RETENTION_DAYS} days", flush=True)
    return removed


def purge_loop():
    while True:
        wait = max(30, next_purge_epoch() - time.time())
        time.sleep(wait)
        try:
            purge_old_jobs()
        except Exception as exc:
            print(f"  purge failed: {exc}", flush=True)


SKIP_LINES = ("summary", "overview", "about the job", "job description")


def derive_title(jd: str, limit: int = 46) -> str:
    """Best-effort label from the job description, used until a better one is posted."""
    for raw in jd.strip().splitlines():
        line = raw.strip(" \t-•*#").strip()
        low = line.lower()
        if not line or low in SKIP_LINES:
            continue
        if low.startswith("needs to hire"):
            continue
        if len(line) <= limit:
            return line
        cut = line[:limit].rsplit(" ", 1)[0]
        return (cut or line[:limit]) + "..."
    return "Untitled job"


def new_job(guide_id, person_id, jd, client="", screening="", url="", title=""):
    job = {
        "id": uuid.uuid4().hex[:8],
        "guide": guide_id,
        "person": person_id,
        "client": client.strip(),
        "jd": jd.strip(),
        # A job off the relay knows its real Upwork title. Only guess when
        # there is nothing to go on, which is a hand-pasted description.
        "title": (title or "").strip() or derive_title(jd),
        "title_from_post": bool((title or "").strip()),
        "screening": screening.strip(),
        "screening_answers": [],
        "images": None,          # None = unknown, [] = none built, [names] = built
        "url": url.strip(),      # Upwork job URL, from the input box or edited in the history
        "boost": "",             # "yes" | "no" | "" (not decided)
        "when": "",              # boost time, wall clock in JST, "YYYY-MM-DDTHH:MM"
        "done": False,           # ticked off in the history list
        "messages": [],
        "questions": [],
        "status": "queued",
        "note": "waiting for Claude Code to pick it up",
        "proposal": "",
        "created": time.time(),
    }
    with JOBS_LOCK:
        for m in job.get("messages", []):
            MSG_SEQ[0] = max(MSG_SEQ[0], m.get("seq", 0))
        JOBS[job["id"]] = job
    JOBS_DIR.mkdir(exist_ok=True)
    (JOBS_DIR / f"{job['id']}.json").write_text(json.dumps(job, indent=2), encoding="utf-8")
    return job


def load_jobs():
    """Jobs survive a server restart: the .jobs mirror is the source of truth."""
    if not JOBS_DIR.is_dir():
        return
    for f in JOBS_DIR.glob("*.json"):
        try:
            job = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        for field, default in (("url", ""), ("boost", ""), ("when", ""), ("done", False)):
            job.setdefault(field, default)
        if not job.get("title"):
            job["title"] = derive_title(job.get("jd", ""))
        if job.get("status") == "working":
            # nobody is holding it any more, put it back in the queue
            job["status"] = "queued"
            job["note"] = "requeued after a server restart"
        for m in job.get("messages", []):
            MSG_SEQ[0] = max(MSG_SEQ[0], m.get("seq", 0))
        JOBS[job["id"]] = job


def add_message(job, role, text):
    with JOBS_LOCK:
        MSG_SEQ[0] += 1
        msg = {"seq": MSG_SEQ[0], "role": role, "text": text, "ts": time.time()}
        job.setdefault("messages", []).append(msg)
        save_job(job)
    return msg


def read_env():
    """Relay credentials from .env. Absent is fine: the queue is then empty."""
    out = {}
    f = ROOT / ".env"
    if not f.is_file():
        return out
    for line in f.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            out[k.strip()] = v.strip()
    return out


def relay_call(method, path, body=None, timeout=30):
    env = read_env()
    base, token = env.get("RELAY_URL", ""), env.get("RELAY_TOKEN", "")
    if not base or not token:
        raise RuntimeError("no RELAY_URL or RELAY_TOKEN in .env")
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        base.rstrip("/") + path, data=data, method=method,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=timeout) as res:
        return json.loads(res.read() or b"null")


def telegram_send(text, tag=""):
    """One message. Returns True if Telegram accepted it, and logs either way,
    so "did the server send that?" has an answer."""
    env = read_env()
    token, chat = env.get("TELEGRAM_BOT_TOKEN", ""), env.get("TELEGRAM_CHAT_ID", "")
    if not token or not chat:
        return False
    try:
        data = json.dumps({"chat_id": chat, "text": text, "parse_mode": "HTML",
                           "disable_web_page_preview": True}).encode()
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data=data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=15) as res:
            ok = bool(json.loads(res.read() or b"null").get("ok"))
        print(f"  telegram {'sent' if ok else 'refused'} {tag}".rstrip(), flush=True)
        return ok
    except Exception as exc:
        print(f"  telegram send failed {tag}: {exc}", flush=True)
        return False


def telegram_new_job(item):
    """Two messages per job, in this order and no other:

      1. the title, the budget and the link
      2. the job description on its own

    The headline leads so the notification preview names the job. The
    description follows as its own message, which reads and forwards cleanly
    with nothing wrapped round it.

    Skipped for an item already claimed for writing: a job being worked on is
    not news. Never raises, since the job is saved before this runs.
    """
    if item.get("used"):
        print(f"  telegram skipped seq {item.get('seq')}: already claimed", flush=True)
        return False

    b = item.get("body", {})
    seq = item.get("seq")

    # 1. title, what it pays, where to open it
    head = ["<b>" + html.escape(b.get("title") or "Untitled job") + "</b>",
            "Budget: " + html.escape(str(b.get("budget") or "not specified"))]
    url = b.get("upworkUrl") or b.get("url")
    if url:
        head.append(html.escape(url))
    ok = telegram_send("\n".join(head), f"seq {seq} (1/2 headline)")

    # 2. the posting itself, nothing around it
    desc = (b.get("description") or "").strip()
    if desc:
        if len(desc) > 3900:            # Telegram caps a message at 4096
            desc = desc[:3900].rstrip() + "\n\n[...truncated, full text is in the queue]"
        second = html.escape(desc)
    else:
        second = "<i>This post arrived with no description.</i>"
    ok = telegram_send(second, f"seq {seq} (2/2 description)") and ok
    return ok


def _jst_wall_to_epoch(wall):
    """Wall clock "YYYY-MM-DDTHH:MM" in JST -> Unix epoch seconds. None on bad input."""
    if not wall:
        return None
    try:
        parts = wall.replace("T", "-").replace(":", "-").split("-")
        y, mo, d, h, mi = (int(x) for x in parts[:5])
    except (ValueError, IndexError):
        return None
    import calendar
    return calendar.timegm((y, mo, d, h, mi, 0, 0, 0, 0)) - 9 * 3600


def telegram_boost_due(job):
    """Alarm when a boosted job's scheduled time arrives."""
    lines = ["<b>Boost now</b>",
             html.escape(job.get("title") or job["id"])]
    if job.get("when"):
        lines.append("Scheduled for " + html.escape(job["when"]) + " JST")
    if job.get("url"):
        lines.append(html.escape(job["url"]))
    return telegram_send("\n".join(lines), f"job {job['id']} boost due")


def boost_check_loop():
    """Every 30 seconds, look for a boosted job whose deadline has arrived and
    is not yet done. Fire the Telegram once per job by flagging boost_notified."""
    while True:
        try:
            _boost_check_once()
        except Exception as exc:
            print(f"  boost check failed: {exc}", flush=True)
        time.sleep(30)


def _boost_check_once():
    now = time.time()
    with JOBS_LOCK:
        due = []
        for job in JOBS.values():
            if (job.get("boost") == "yes"
                    and not job.get("done")
                    and not job.get("boost_notified")
                    and job.get("when")):
                when_epoch = _jst_wall_to_epoch(job["when"])
                if when_epoch is not None and when_epoch <= now:
                    due.append(job)
    for job in due:
        # Set the flag before sending so a slow Telegram doesn't cause a
        # double-fire if the loop tick overlaps.
        with JOBS_LOCK:
            job["boost_notified"] = True
            save_job(job)
        telegram_boost_due(job)
        print(f"  boost telegram sent for job {job['id']}", flush=True)


def telegram_proposal_done(job):
    """One short message when a proposal is finished and ready to copy."""
    lines = ["<b>Proposal done</b>", html.escape(job.get("title") or job["id"])]
    if job.get("url"):
        lines.append(html.escape(job["url"]))
    return telegram_send("\n".join(lines), f"job {job['id']} done")


def queue_save(item):
    QUEUE_DIR.mkdir(exist_ok=True)
    (QUEUE_DIR / f"{item['seq']:06d}.json").write_text(
        json.dumps(item, indent=2, ensure_ascii=False), encoding="utf-8")


# Upstream posts to the `jobs` channel come from three producers: Vollna's
# email scraper (type "job"), Upwork's own new-job notification worker, and
# Upwork's invitations worker. Earlier the filter accepted only type "job",
# which meant the other two were acked and silently dropped for weeks. It now
# keeps anything with a URL or a title. Explicit noise-shapes (the Apps Script
# test pings) are still dropped, but named in the log.
NOISE_TYPES = {"test", "ping", "heartbeat"}


def _looks_like_a_job(body):
    if not isinstance(body, dict):
        return False
    if str(body.get("type", "")).lower() in NOISE_TYPES:
        return False
    return bool(
        body.get("title") or body.get("url") or body.get("upworkUrl")
        or body.get("description") or body.get("jobDescription")
    )


def relay_pull(wait=0.0):
    """Take what the relay is holding, keep everything that looks like a job,
    acknowledge the lot.

    With `wait`, the relay holds the request open until something arrives, so
    a posted job reaches this machine in about as long as the network takes.

    Stored locally *before* acking, so a crash in between re-delivers rather
    than loses. Every dropped message is logged with its type and sender, so
    a new upstream producer sending an unfamiliar shape shows up loudly next
    time instead of vanishing.
    """
    payload = relay_call("GET", f"/messages?wait={wait}", timeout=wait + 20)
    kept = []
    for msg in payload.get("messages", []):
        body = msg.get("body") if isinstance(msg.get("body"), dict) else {}
        if _looks_like_a_job(body):
            existing = QUEUE_DIR / f"{msg['seq']:06d}.json"
            if not existing.is_file():        # never clobber a typed-in client name
                item = {"seq": msg["seq"], "channel": msg["channel"],
                        "sender": msg.get("sender", ""), "ts": msg.get("ts", time.time()),
                        "body": body, "client_name": "", "used": False}
                queue_save(item)
                kept.append(item)
                title = body.get("title") or body.get("jobTitle") or ""
                print(f"  relay job seq {msg['seq']} arrived from {msg.get('sender','?')}: "
                      f"type={body.get('type','?')} title={title[:46]!r}", flush=True)
        else:
            print(f"  relay skipped seq {msg['seq']} from {msg.get('sender','?')}: "
                  f"type={body.get('type','?')} keys={list(body)[:6]}", flush=True)
        relay_call("POST", "/ack", {"channel": msg["channel"], "seq": msg["seq"]})
    for item in kept:
        telegram_new_job(item)
    return len(kept)


def queue_items():
    """Newest first. Each row is what the UI needs and nothing more."""
    out = []
    if not QUEUE_DIR.is_dir():
        return out
    for f in sorted(QUEUE_DIR.glob("*.json")):
        try:
            item = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        b = item.get("body", {})
        client = b.get("client") if isinstance(b.get("client"), dict) else {}
        out.append({
            "seq": item["seq"],
            "title": b.get("title") or "Untitled job",
            "url": b.get("upworkUrl") or b.get("url") or "",
            "budget": b.get("budget") or "",
            "published": b.get("published") or "",
            "location": client.get("location", ""),
            "verified": client.get("paymentVerified"),
            "qualification": b.get("aiQualification", ""),
            "has_jd": bool((b.get("description") or "").strip()),
            "client_name": item.get("client_name", ""),
            "used": bool(item.get("used")),
            "job_id": item.get("job_id", ""),
            "job_status": (JOBS.get(item.get("job_id", ""), {}) or {}).get("status", ""),
            "has_proposal": bool((JOBS.get(item.get("job_id", ""), {}) or {}).get("proposal")),
        })
    out.sort(key=lambda r: r["seq"])      # newest at the bottom
    return out


def queue_drop_for_job(job_id):
    """Take a finished job's row out of the queue.

    The row exists to say "this still needs writing". Once a proposal is
    stored the row has no work left in it, and leaving it there means the
    list stops being a list of what to do.
    """
    if not job_id or not QUEUE_DIR.is_dir():
        return None
    for f in sorted(QUEUE_DIR.glob("*.json")):
        try:
            item = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if item.get("job_id") == job_id:
            f.unlink()
            return item.get("seq")
    return None


def queue_get(seq):
    f = QUEUE_DIR / f"{int(seq):06d}.json"
    if not f.is_file():
        return None
    return json.loads(f.read_text(encoding="utf-8"))


def queue_jd(item):
    """The job description the writer works from, built by the bridge's own
    formatter so the relay path and the manual path agree."""
    from proposal_bridge import as_jd
    return as_jd(item.get("body", {}))


def pull_loop():
    """Hold a request open on the relay, so a new job arrives here at once."""
    while True:
        try:
            relay_pull(wait=25)
        except Exception as exc:
            print(f"  relay pull failed: {exc}", flush=True)
            time.sleep(15)          # only back off when something is wrong


def slugify(text, limit=48):
    out = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    return (out[:limit].rstrip("-") or "untitled")


def export_proposal(job):
    """Write the proposal to proposals/ as readable markdown.

    This is the durable local copy. The .jobs record is the queue's working
    state; this is the thing you would actually open in a month.
    """
    if not job.get("proposal"):
        return
    PROPOSALS.mkdir(exist_ok=True)
    when = datetime.datetime.fromtimestamp(job.get("created", time.time()), tz=JST)
    name = f"{when:%Y-%m-%d}_{slugify(job.get('title') or job['id'])}_{job.get('person','')}" \
           f"_{job['id']}.md"
    # A retitled job would otherwise leave its old file behind.
    for stale in PROPOSALS.glob(f"*_{job['id']}.md"):
        if stale.name != name:
            stale.unlink()

    imgs = job.get("images")
    body = job.get("proposal", "").strip()
    lines = [
        f"# {job.get('title') or job['id']}",
        "",
        f"- **Person:** {job.get('person','')}",
        f"- **Guide:** {job.get('guide','')}",
        f"- **Client:** {job.get('client') or '(not given)'}",
        f"- **Job URL:** {job.get('url') or '(not saved)'}",
        f"- **Written:** {when:%Y-%m-%d %H:%M} JST",
        f"- **Length:** {len(body.replace('**', '')):,} characters",
        f"- **Images:** {', '.join(imgs) if imgs else 'none'}",
        f"- **Job id:** {job['id']}",
        "",
        "---",
        "",
        "## Proposal",
        "",
        body,
        "",
    ]

    if job.get("screening_answers"):
        lines += ["---", "", "## Screening answers", ""]
        for a in job["screening_answers"]:
            lines += [f"**Q. {a.get('question','').strip()}**", "",
                      a.get("answer", "").strip(), ""]

    if job.get("questions"):
        lines += ["---", "", "## Questions raised while writing", ""]
        for q in job["questions"]:
            lines.append(f"- **{q.get('text','').strip()}**")
            if q.get("assumption"):
                lines.append(f"  - Assumed: {q['assumption'].strip()}")
            if q.get("answer"):
                lines.append(f"  - Answered: {q['answer'].strip()}")
            if q.get("ignored"):
                lines.append("  - Ignored")
        lines.append("")

    if job.get("jd"):
        lines += ["---", "", "## Job description", "", job["jd"].strip(), ""]

    (PROPOSALS / name).write_text("\n".join(lines), encoding="utf-8")
    job["export"] = name
    return name


def remove_export(job):
    """Only for an explicit delete. The timed purge deliberately leaves these."""
    for f in PROPOSALS.glob(f"*_{job['id']}.md"):
        f.unlink()


def save_job(job):
    JOBS_DIR.mkdir(exist_ok=True)
    try:
        export_proposal(job)
    except Exception as exc:                 # never lose the job over the archive
        print(f"  could not export {job['id']}: {exc}", flush=True)
    (JOBS_DIR / f"{job['id']}.json").write_text(json.dumps(job, indent=2), encoding="utf-8")


def title_of(path: Path, fallback: str) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def list_guides():
    out = []
    for p in sorted(GUIDES.glob("*.md")):
        out.append({"id": p.stem, "name": title_of(p, p.stem), "file": f"guides/{p.name}"})
    return out


def list_people():
    out = []
    for p in sorted(ROOT.glob("*.md")):
        if p.name in NOT_A_PERSON or "-" in p.stem:
            continue
        out.append({"id": p.stem, "name": title_of(p, p.stem), "file": p.name})
    return out


def read_guide(guide_id: str) -> str:
    p = GUIDES / f"{guide_id}.md"
    if not p.is_file():
        raise FileNotFoundError(f"no guide named {guide_id}")
    return p.read_text(encoding="utf-8")


def read_person(person_id: str) -> str:
    p = ROOT / f"{person_id}.md"
    if not p.is_file() or p.name in NOT_A_PERSON:
        raise FileNotFoundError(f"no person profile named {person_id}")
    return p.read_text(encoding="utf-8")


def build_prompt(guide_id: str, person_id: str, jd: str, client: str = "",
                 screening: str = ""):
    guide = read_guide(guide_id)
    person = read_person(person_id)
    system = (
        "You are writing an Upwork proposal.\n\n"
        "Follow the guide below exactly. Every fact, link, number, and the sign-off name come "
        "from the person profile below and nowhere else. Never invent a URL, a client name, or a "
        "metric.\n\n"
        "Return ONLY the proposal in markdown, using **bold** for sub-headlines. No preamble, no "
        "commentary, no code fences.\n\n"
        f"=== PROPOSAL GUIDE ===\n{guide}\n\n"
        f"=== PERSON PROFILE ===\n{person}\n"
    )
    who = f"\n\nThe client's name is {client.strip()}. Address them by it.\n" if client.strip() else ""
    ask = ""
    if screening.strip():
        ask = (
            "\n\n=== THE CLIENT'S OWN SCREENING QUESTIONS ===\n"
            f"{screening.strip()}\n\n"
            "Answer each of these separately, in the same copy-ready form as the proposal, so "
            "each answer can be pasted into its own field. Keep each one short and specific.\n"
        )
    user = f"=== JOB DESCRIPTION ===\n{jd.strip()}\n{who}{ask}\nWrite the proposal."
    return system, user


def call_anthropic(system: str, user: str) -> str:
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set")
    body = json.dumps(
        {
            "model": MODEL,
            "max_tokens": 4000,
            "system": system,
            "messages": [{"role": "user", "content": user}],
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=body,
        headers={
            "content-type": "application/json",
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
        },
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        payload = json.load(resp)
    return "".join(b.get("text", "") for b in payload.get("content", []))


class Server(ThreadingHTTPServer):
    # Default backlog is 5. Two pollers plus a browser can burst past that and
    # get connection-refused even while the server is perfectly healthy.
    request_queue_size = 128
    daemon_threads = True
    allow_reuse_address = True


class Handler(BaseHTTPRequestHandler):
    server_version = "ProposalUI/1.0"

    def log_message(self, fmt, *args):
        sys.stderr.write("  %s\n" % (fmt % args))

    def _send(self, code, body, ctype="application/json; charset=utf-8"):
        if isinstance(body, (dict, list)):
            body = json.dumps(body)
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self):
        n = int(self.headers.get("Content-Length") or 0)
        if not n:
            return {}
        return json.loads(self.rfile.read(n).decode("utf-8"))

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path in ("/", "/index.html"):
            f = UI / "index.html"
            if not f.is_file():
                return self._send(500, "ui/index.html is missing", "text/plain; charset=utf-8")
            return self._send(200, f.read_text(encoding="utf-8"), "text/html; charset=utf-8")
        if path == "/favicon.png":
            f = UI / "favicon.png"
            if not f.is_file():
                return self._send(404, {"error": "no favicon"})
            return self._send(200, f.read_bytes(), "image/png")
        if path == "/api/config":
            return self._send(
                200,
                {
                    "guides": list_guides(),
                    "people": list_people(),
                    "mode": "api" if os.environ.get("ANTHROPIC_API_KEY") else "bridge",
                    "retention_days": RETENTION_DAYS,
                    "purge_at_jst": "%02d:%02d" % PURGE_AT_JST,
                    "model": MODEL,
                },
            )
        if path == "/api/queue":
            return self._send(200, {"queue": queue_items()})

        if path == "/api/jobs":
            with JOBS_LOCK:
                rows = sorted(JOBS.values(), key=lambda j: j["created"], reverse=True)
            return self._send(200, {"jobs": [
                {k: j.get(k) for k in
                 ("id", "guide", "person", "status", "note", "created", "title", "images",
                  "url", "boost", "when", "done")}
                for j in rows[:200]
            ]})
        if path.startswith("/api/messages/since"):
            try:
                after = int(self.path.split("seq=")[1].split("&")[0])
            except Exception:
                after = 0
            with JOBS_LOCK:
                out = []
                for job in JOBS.values():
                    for msg in job.get("messages", []):
                        if msg["seq"] > after:
                            out.append({"job": job["id"], **msg})
                out.sort(key=lambda m: m["seq"])
                return self._send(200, {"messages": out, "max_seq": MSG_SEQ[0]})
        if path == "/api/jobs/answered":
            with JOBS_LOCK:
                ids = [j["id"] for j in JOBS.values() if j["status"] == "revising"]
            return self._send(200, {"ids": ids})
        if path == "/api/jobs/queued":
            with JOBS_LOCK:
                ids = [j["id"] for j in JOBS.values() if j["status"] == "queued"]
            return self._send(200, {"ids": ids})
        if path == "/api/jobs/next":
            with JOBS_LOCK:
                pending = sorted(
                    (j for j in JOBS.values() if j["status"] == "queued"),
                    key=lambda j: j["created"],
                )
                if not pending:
                    return self._send(200, {"job": None})
                job = pending[0]
                job["status"] = "working"
                job["note"] = "Claude Code is writing it"
                save_job(job)
            return self._send(200, {"job": job})
        m = re.fullmatch(r"/api/job/([0-9a-f]{8})", path)
        if m:
            with JOBS_LOCK:
                job = JOBS.get(m.group(1))
            if not job:
                return self._send(404, {"error": "no such job"})
            return self._send(200, job)
        return self._send(404, {"error": "not found"})

    def do_POST(self):
        path = self.path.split("?", 1)[0]
        try:
            data = self._read_json()
        except Exception as exc:
            return self._send(400, {"error": f"bad JSON: {exc}"})

        m = re.fullmatch(r"/api/job/([0-9a-f]{8})/result", path)
        if m:
            finished = None
            with JOBS_LOCK:
                job = JOBS.get(m.group(1))
                if not job:
                    return self._send(404, {"error": "no such job"})
                if job["status"] == "cancelled" and not data.get("proposal"):
                    return self._send(409, {"error": "job was cancelled", "status": "cancelled"})
                if data.get("error"):
                    job["status"] = "error"
                    job["note"] = str(data["error"])
                else:
                    text = (data.get("proposal") or "").strip()
                    if not text:
                        # A result with no proposal used to mark the job done and
                        # empty, which reads as "written" in the UI and hands the
                        # user nothing. Refuse it and leave the job claimable.
                        return self._send(400, {
                            "error": "no proposal in the result: send the text in "
                                     "'proposal', or POST /note and /questions instead",
                            "status": job["status"]})
                    job["proposal"] = text
                    job["status"] = "done"
                    dropped = queue_drop_for_job(job["id"])
                    if dropped is not None:
                        print(f"  queue seq {dropped} written, row removed", flush=True)
                    # One Telegram alarm per job, no matter how many /result calls
                    # arrive (from a peer session, from a rewrite after answers).
                    if not job.get("notified_done"):
                        job["notified_done"] = True
                        finished = job
                    else:
                        print(f"  telegram skipped: job {job['id']} already notified", flush=True)
                    job["note"] = ("final version, no further questions"
                                   if job.get("status_was_revising")
                                   else "written by Claude Code")
                    # The real Upwork title wins. A writer's own summary of the
                    # job is not the job's name, and renaming it makes the row
                    # impossible to match against the post.
                    if data.get("title") and not job.get("title_from_post"):
                        job["title"] = str(data["title"]).strip()[:60]
                    if "images" in data:
                        imgs = data.get("images")
                        job["images"] = list(imgs) if isinstance(imgs, list) else []
                save_job(job)
            # Sent outside the lock: a Telegram round trip must not hold up
            # every other request, and the job is already stored by now.
            if finished is not None:
                telegram_proposal_done(finished)
            return self._send(200, {"ok": True})

        if path == "/api/queue/refresh":
            try:
                added = relay_pull()
            except Exception as exc:
                return self._send(502, {"error": str(exc)})
            return self._send(200, {"ok": True, "added": added, "queue": queue_items()})

        m = re.fullmatch(r"/api/queue/(\d+)/meta", path)
        if m:
            item = queue_get(m.group(1))
            if not item:
                return self._send(404, {"error": "no such queue item"})
            if "client_name" in data:
                item["client_name"] = str(data["client_name"]).strip()[:80]
            if "used" in data:
                item["used"] = bool(data["used"])
            queue_save(item)
            return self._send(200, {"ok": True})

        m = re.fullmatch(r"/api/queue/(\d+)/delete", path)
        if m:
            f = QUEUE_DIR / f"{int(m.group(1)):06d}.json"
            existed = f.is_file()
            if existed:
                f.unlink()
            return self._send(200, {"ok": True, "deleted": existed})

        if path == "/api/jobs/clear":
            with JOBS_LOCK:
                removed = len(JOBS)
                for job_id, job in list(JOBS.items()):
                    f = JOBS_DIR / f"{job_id}.json"
                    if f.is_file():
                        f.unlink()
                    remove_export(job)      # an explicit clear takes the archive too
                JOBS.clear()
            return self._send(200, {"ok": True, "removed": removed})

        m = re.fullmatch(r"/api/job/([0-9a-f]{8})/delete", path)
        if m:
            job_id = m.group(1)
            with JOBS_LOCK:
                gone = JOBS.pop(job_id, None)
                existed = gone is not None
                f = JOBS_DIR / f"{job_id}.json"
                if f.is_file():
                    f.unlink()
                if gone:
                    remove_export(gone)     # an explicit delete takes the archive too
            return self._send(200, {"ok": True, "deleted": existed})

        m = re.fullmatch(r"/api/job/([0-9a-f]{8})/meta", path)
        if m:
            with JOBS_LOCK:
                job = JOBS.get(m.group(1))
                if not job:
                    return self._send(404, {"error": "no such job"})
                # If either boost or the deadline shifts, the alarm should be
                # able to fire again for the new schedule.
                if ("boost" in data and data.get("boost") != job.get("boost")) or (
                        "when" in data and data.get("when") != job.get("when")):
                    job["boost_notified"] = False
                for field in ("url", "boost", "when"):
                    if field in data:
                        job[field] = str(data.get(field) or "").strip()[:400]
                if "done" in data:
                    job["done"] = bool(data.get("done"))
                save_job(job)
            return self._send(200, {"ok": True})

        m = re.fullmatch(r"/api/job/([0-9a-f]{8})/screening_answers", path)
        if m:
            with JOBS_LOCK:
                job = JOBS.get(m.group(1))
                if not job:
                    return self._send(404, {"error": "no such job"})
                job["screening_answers"] = [
                    {
                        "question": str(a.get("question") or "").strip(),
                        "answer": str(a.get("answer") or "").strip(),
                    }
                    for a in data.get("answers") or []
                    if str(a.get("answer") or "").strip()
                ]
                save_job(job)
            return self._send(200, {"ok": True, "count": len(job["screening_answers"])})

        m = re.fullmatch(r"/api/job/([0-9a-f]{8})/questions", path)
        if m:
            with JOBS_LOCK:
                job = JOBS.get(m.group(1))
                if not job:
                    return self._send(404, {"error": "no such job"})
                # This endpoint replaces the whole list. Two writers on one
                # queue made that a silent clobber: one session's questions
                # vanished under another's, and the panel then disagreed with
                # the stored draft. Refuse unless the caller means it.
                if job.get("questions") and not data.get("replace"):
                    return self._send(409, {
                        "error": "this job already has questions; pass replace:true "
                                 "to overwrite them",
                        "existing": len(job["questions"])})
                job["questions"] = [
                    {
                        "id": i,
                        "text": str(q.get("text") or "").strip(),
                        "assumption": str(q.get("assumption") or "").strip(),
                        "answer": "",
                        "ignored": False,
                    }
                    for i, q in enumerate(data.get("questions") or [])
                    if str(q.get("text") or "").strip()
                ]
                save_job(job)
            return self._send(200, {"ok": True, "count": len(job["questions"])})

        m = re.fullmatch(r"/api/job/([0-9a-f]{8})/answers", path)
        if m:
            with JOBS_LOCK:
                job = JOBS.get(m.group(1))
                if not job:
                    return self._send(404, {"error": "no such job"})
                by_id = {q["id"]: q for q in job.get("questions", [])}
                for a in data.get("answers") or []:
                    q = by_id.get(a.get("id"))
                    if q is not None:
                        q["answer"] = str(a.get("answer") or "").strip()
                        q["ignored"] = bool(a.get("ignored"))
                job["status"] = "revising"
                job["status_was_revising"] = True
                job["note"] = "answers submitted, writing the final version"
                save_job(job)
            return self._send(200, {"ok": True})

        m = re.fullmatch(r"/api/job/([0-9a-f]{8})/message", path)
        if m:
            with JOBS_LOCK:
                job = JOBS.get(m.group(1))
            if not job:
                return self._send(404, {"error": "no such job"})
            role = data.get("role") or "user"
            text = (data.get("text") or "").strip()
            if role not in ("user", "claude"):
                return self._send(400, {"error": "role must be user or claude"})
            if not text:
                return self._send(400, {"error": "empty message"})
            msg = add_message(job, role, text)
            return self._send(200, {"ok": True, "seq": msg["seq"]})

        m = re.fullmatch(r"/api/job/([0-9a-f]{8})/cancel", path)
        if m:
            with JOBS_LOCK:
                job = JOBS.get(m.group(1))
                if not job:
                    return self._send(404, {"error": "no such job"})
                if job["status"] in ("queued", "working"):
                    job["status"] = "cancelled"
                    job["note"] = "stopped from the UI"
                    save_job(job)
            return self._send(200, {"ok": True, "status": job["status"]})

        m = re.fullmatch(r"/api/job/([0-9a-f]{8})/note", path)
        if m:
            with JOBS_LOCK:
                job = JOBS.get(m.group(1))
                if not job:
                    return self._send(404, {"error": "no such job"})
                job["note"] = str(data.get("note") or "")
                save_job(job)
            return self._send(200, {"ok": True})

        guide_id = (data.get("guide") or "").strip()
        person_id = (data.get("person") or "").strip()
        jd = data.get("jd") or ""

        # A job picked off the relay queue carries its own description, link
        # and client name. The request only has to name the seq.
        queued = None
        if data.get("queue_seq") not in (None, ""):
            queued = queue_get(data["queue_seq"])
            if not queued:
                return self._send(404, {"error": f"queue item {data['queue_seq']} is gone"})
            jd = queue_jd(queued)
            data = dict(data)
            data["url"] = (queued.get("body", {}).get("upworkUrl")
                           or queued.get("body", {}).get("url") or "")
            data["client"] = queued.get("client_name", "")
            data["title"] = (queued.get("body", {}).get("title") or "").strip()

        if path in ("/api/prompt", "/api/generate"):
            if not jd.strip():
                return self._send(400, {"error": "paste a job description first"})
            try:
                system, user = build_prompt(guide_id, person_id, jd, data.get("client") or "",
                                            data.get("screening") or "")
            except FileNotFoundError as exc:
                return self._send(400, {"error": str(exc)})

            if path == "/api/prompt":
                return self._send(200, {"prompt": f"{system}\n\n{user}"})

            if not os.environ.get("ANTHROPIC_API_KEY"):
                job = new_job(guide_id, person_id, jd, data.get("client") or "",
                              data.get("screening") or "", data.get("url") or "",
                              data.get("title") or "")
                if queued:
                    queued["used"] = True
                    queued["job_id"] = job["id"]
                    queue_save(queued)
                return self._send(200, {"job": job["id"], "mode": "bridge"})

            try:
                text = call_anthropic(system, user)
            except RuntimeError as exc:
                return self._send(503, {"error": str(exc), "mode": "manual"})
            except urllib.error.HTTPError as exc:
                detail = exc.read().decode("utf-8", "replace")[:400]
                return self._send(502, {"error": f"API {exc.code}: {detail}"})
            except Exception as exc:
                return self._send(502, {"error": f"request failed: {exc}"})
            return self._send(200, {"proposal": text})

        return self._send(404, {"error": "not found"})


def main():
    load_jobs()
    purge_old_jobs()          # catch up if the server was down at the boundary
    threading.Thread(target=purge_loop, daemon=True).start()
    threading.Thread(target=pull_loop, daemon=True).start()
    threading.Thread(target=boost_check_loop, daemon=True).start()
    if not (UI / "index.html").is_file():
        sys.exit("ui/index.html is missing")
    mode = "API mode" if os.environ.get("ANTHROPIC_API_KEY") else "bridge mode (jobs go to Claude Code)"
    print(f"Proposal UI on http://localhost:{PORT}  [{mode}]")
    print(f"  guides: {', '.join(g['id'] for g in list_guides()) or 'none'}", flush=True)
    print(f"  people: {', '.join(p['id'] for p in list_people()) or 'none'}", flush=True)
    print(f"  jobs restored: {len(JOBS)}", flush=True)
    nxt = datetime.datetime.fromtimestamp(next_purge_epoch(), tz=JST)
    print(f"  history kept {RETENTION_DAYS} days, next purge {nxt:%Y-%m-%d %H:%M} JST", flush=True)
    print("  Ctrl+C to stop")
    Server(("127.0.0.1", PORT), Handler).serve_forever()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nstopped")
