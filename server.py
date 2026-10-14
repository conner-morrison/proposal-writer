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
PROFILES = ROOT / "profiles"
UI = ROOT / "ui"
PORT = int(os.environ.get("PROPOSAL_UI_PORT", "8765"))
MODEL = os.environ.get("PROPOSAL_UI_MODEL", "claude-opus-5")

# A person profile is a single-word .md file in profiles/: Mario.md, Zachary.md.
# Everything personal lives in that folder and the folder is gitignored, so this
# repo deploys with somebody else's people in it. A hyphenated name there is
# supporting material rather than a person (connor-github.md), and these names
# are skipped outright in case one is ever dropped in beside the profiles.
NOT_A_PERSON = {"CLAUDE.md", "README.md", "MEMORY.md"}

# Job queue. Without an API key the UI hands the job to the Claude Code session
# that is watching this queue, and polls until the proposal comes back.
JOBS = {}
JOBS_LOCK = threading.Lock()
MSG_SEQ = [0]  # monotonic id so the watcher can poll for anything new
JOBS_DIR = ROOT / ".jobs"
PROPOSALS = ROOT / "proposals"   # readable local archive, one markdown file per proposal
QUEUE_DIR = ROOT / ".queue"      # jobs pulled off the relay, waiting to be written
THREADS_DIR = ROOT / ".threads"  # the Report page: talking to the server, not about jobs
IDENTITY_FILE = ROOT / ".identity.json"  # who this project is to the server, once registered
STATE_DIR = ROOT / ".state"              # runtime state for the three workers
WORKERS_FILE = STATE_DIR / "workers.json"

# The three roles, separated so they can run at once without tripping over each
# other. None of this is new behaviour: the project already brought jobs in,
# analysed them and wrote proposals. What is new is that each role has its own
# lifecycle, so one can be paused without the others stopping.
#
#   bringer   the server's own relay poll. The only one that runs *inside* this
#             process, so start/stop genuinely starts and stops the thread.
#   analyzer  a Claude Code session on haiku, working the queue in order.
#   writer    a Claude Code session writing proposals.
#
# The analyzer and the writer are sessions rather than threads, so the server
# cannot start them. What it holds is the *intent*: a session reads its own
# state before each step and obeys it. "running" means carry on, "paused" means
# finish nothing new and wait, "stopped" means do not pick anything up.
WORKER_ROLES = ("bringer", "analyzer", "writer")
WORKERS = {}
WORKERS_LOCK = threading.Lock()

# A worker's stored intent. "off" is never stored: it is derived from nobody
# being attached, because a role with no session behind it is not in any state
# a person chose for it.
WORKER_STATES = ("idle", "running", "paused", "error")

# How long after its last heartbeat a session still counts as attached. A
# session that checks in every 30 seconds stays attached comfortably; one that
# has gone away shows as off within two missed beats.
WORKER_ATTACH_SECONDS = 90

# Report threads. One per instruction the server sent us, or per request we
# sent it. Deliberately separate from JOBS: nothing about a proposal belongs
# here, only the conversation around it.
THREADS = {}
THREADS_LOCK = threading.Lock()

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



# Country of the client, read off the "Location:" line Upwork posts carry, and
# the language a proposal to that client would be written in. English-speaking
# markets map to English, which is how the UI knows there is nothing to
# translate. Only the markets that actually show up in this queue are listed;
# an unlisted country simply leaves the button inactive.
COUNTRY_LANGUAGE = {
    "united states": ("United States", None), "usa": ("United States", None),
    "united kingdom": ("United Kingdom", None), "uk": ("United Kingdom", None),
    "canada": ("Canada", None), "australia": ("Australia", None),
    "new zealand": ("New Zealand", None), "ireland": ("Ireland", None),
    "singapore": ("Singapore", None), "india": ("India", None),
    "germany": ("Germany", "German"), "austria": ("Austria", "German"),
    "switzerland": ("Switzerland", "German"),
    "france": ("France", "French"), "belgium": ("Belgium", "Dutch"),
    "spain": ("Spain", "Spanish"), "mexico": ("Mexico", "Spanish"),
    "argentina": ("Argentina", "Spanish"), "colombia": ("Colombia", "Spanish"),
    "chile": ("Chile", "Spanish"), "peru": ("Peru", "Spanish"),
    "portugal": ("Portugal", "Portuguese"), "brazil": ("Brazil", "Portuguese"),
    "italy": ("Italy", "Italian"), "netherlands": ("Netherlands", "Dutch"),
    "sweden": ("Sweden", "Swedish"), "norway": ("Norway", "Norwegian"),
    "denmark": ("Denmark", "Danish"), "finland": ("Finland", "Finnish"),
    "poland": ("Poland", "Polish"), "czechia": ("Czechia", "Czech"),
    "czech republic": ("Czech Republic", "Czech"),
    "ukraine": ("Ukraine", "Ukrainian"), "russia": ("Russia", "Russian"),
    "turkey": ("Turkey", "Turkish"), "greece": ("Greece", "Greek"),
    "romania": ("Romania", "Romanian"), "hungary": ("Hungary", "Hungarian"),
    "israel": ("Israel", "Hebrew"),
    "united arab emirates": ("United Arab Emirates", "Arabic"),
    "uae": ("United Arab Emirates", "Arabic"),
    "saudi arabia": ("Saudi Arabia", "Arabic"), "egypt": ("Egypt", "Arabic"),
    "japan": ("Japan", "Japanese"), "south korea": ("South Korea", "Korean"),
    "korea": ("South Korea", "Korean"), "china": ("China", "Chinese"),
    "taiwan": ("Taiwan", "Chinese"), "hong kong": ("Hong Kong", "Chinese"),
    "vietnam": ("Vietnam", "Vietnamese"), "thailand": ("Thailand", "Thai"),
    "indonesia": ("Indonesia", "Indonesian"),
    "philippines": ("Philippines", "Filipino"),
}


def _country_from_name(name):
    """Resolve a country typed into the UI. Unknown names are kept as the
    country so the job still records where the client is, with no language,
    which leaves the translate button inactive rather than guessing."""
    raw = str(name or "").strip()
    if not raw:
        return None, None
    hit = COUNTRY_LANGUAGE.get(raw.lower())
    return hit if hit else (raw, None)


def detect_country(jd: str):
    """(country, language) from the post's Location line, or (None, None).

    language is None for an English-speaking market: the country is known, but
    there is nothing to translate into.
    """
    # Upwork writes this as a bullet inside the Client block, so allow the
    # list marker: "- Location: <flag> United States".
    m = re.search(r"^[\s\-*\u2022]*(?:Location|Country)\s*:\s*(.+)$",
                  jd or "", re.M | re.I)
    if not m:
        return None, None
    # Strip the flag emoji Upwork prefixes and any trailing city detail.
    raw = re.sub(r"[\U0001F1E6-\U0001F1FF]", "", m.group(1)).strip(" ,.\t")
    raw = raw.split(",")[-1].strip() if "," in raw else raw
    return COUNTRY_LANGUAGE.get(raw.lower(), (None, None))



def save_thread(t):
    THREADS_DIR.mkdir(exist_ok=True)
    (THREADS_DIR / f"{t['id']}.json").write_text(json.dumps(t, indent=2), encoding="utf-8")


def load_threads():
    if not THREADS_DIR.is_dir():
        return
    for f in THREADS_DIR.glob("*.json"):
        try:
            t = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        THREADS[t["id"]] = t


def new_thread(kind, title, channel="", sender="", text="", role="server"):
    """kind is 'instruction' (the server telling us something) or 'request'
    (us asking the server for something)."""
    t = {
        "id": uuid.uuid4().hex[:8],
        "kind": kind if kind in ("request", "registration") else "instruction",
        "title": (title or "").strip()[:120] or "Untitled",
        "channel": channel,
        "sender": sender,
        "created": time.time(),
        "updated": time.time(),
        "completed": False,
        "completed_at": None,
        # registration threads only: waiting until the server hands back an id
        "status": "waiting" if kind == "registration" else "",
        "url": "",
        "assigned_id": None,
        "messages": [],
    }
    with THREADS_LOCK:
        THREADS[t["id"]] = t
    if text.strip():
        thread_say(t, role, text)
    else:
        save_thread(t)
    return t


def thread_say(t, role, text):
    role = role if role in ("server", "claude", "user") else "server"
    with THREADS_LOCK:
        msg = {"seq": len(t["messages"]) + 1, "role": role,
               "text": str(text), "ts": time.time()}
        t["messages"].append(msg)
        t["updated"] = msg["ts"]
        save_thread(t)
    return msg


def thread_row(t):
    """What the sidebar needs, and nothing more."""
    last = t["messages"][-1] if t["messages"] else None
    return {"id": t["id"], "kind": t["kind"], "title": t["title"],
            "status": t.get("status", ""), "assigned_id": t.get("assigned_id"),
            "channel": t.get("channel", ""), "completed": bool(t["completed"]),
            "created": t["created"], "updated": t["updated"],
            "count": len(t["messages"]),
            "preview": (last["text"][:90] if last else ""),
            "last_role": (last["role"] if last else "")}



# ---- identity -----------------------------------------------------------
# Registration is a handshake: we send the server this project's name, the
# server approves and hands back an id. After that the id is what we send, and
# the server maps it back to the name on its side.

def project_name():
    return read_env().get("PROJECT_NAME") or "Proposal Writer"


def _worker_blank(role):
    # Idle, not running: a fresh worker has been allocated nothing and started
    # by nobody. Claiming "running" at boot was the bug this replaced.
    return {"role": role, "state": "idle", "note": "", "current": "",
            "error": "", "last_seen": None, "changed": time.time(),
            # Commands are counted, not just stored as a level. Pressing Stop
            # and then Start before the session's next heartbeat used to be
            # invisible to it: the level was back to running, so nothing had
            # apparently happened. The counter means a session can tell that a
            # command was issued even when the state it ends on is unchanged,
            # and the panel can say whether it was heard.
            "command_seq": 0, "last_command": "", "command_at": None,
            "acked_seq": 0, "acked_at": None,
            # Set when a person presses Write proposal, Submit and rewrite, or
            # Answer screening while the writer is mid-draft. The writer yields,
            # the person's job goes first, and this clears when it lands.
            "yielded_to": ""}


def load_workers():
    """Worker state survives a restart, so a paused writer stays paused."""
    with WORKERS_LOCK:
        for role in WORKER_ROLES:
            WORKERS[role] = _worker_blank(role)
        if WORKERS_FILE.is_file():
            try:
                saved = json.loads(WORKERS_FILE.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                saved = {}
            for role in WORKER_ROLES:
                row = saved.get(role)
                if isinstance(row, dict):
                    WORKERS[role].update({k: v for k, v in row.items()
                                          if k in WORKERS[role]})
                    WORKERS[role]["role"] = role
                    if WORKERS[role]["state"] not in WORKER_STATES:
                        WORKERS[role]["state"] = "idle"
        # Nothing is mid-step across a restart, so no role comes back claiming
        # to be busy and none comes back owing a person a turn. The command
        # counter is reset together with its ack, so a restart does not look
        # like an unheard command.
        for role in WORKER_ROLES:
            WORKERS[role]["current"] = ""
            WORKERS[role]["last_seen"] = None
            WORKERS[role]["yielded_to"] = ""
            WORKERS[role]["command_seq"] = 0
            WORKERS[role]["acked_seq"] = 0
            WORKERS[role]["acked_at"] = None
    save_workers()


def save_workers():
    STATE_DIR.mkdir(exist_ok=True)
    with WORKERS_LOCK:
        WORKERS_FILE.write_text(json.dumps(WORKERS, indent=2), encoding="utf-8")


def worker_set(role, **fields):
    if role not in WORKER_ROLES:
        return None
    with WORKERS_LOCK:
        w = WORKERS.setdefault(role, _worker_blank(role))
        if "state" in fields and fields["state"] != w.get("state"):
            w["changed"] = time.time()
        w.update(fields)
        out = dict(w)
    save_workers()
    return out


def worker_get(role):
    with WORKERS_LOCK:
        return dict(WORKERS.get(role) or _worker_blank(role))


def worker_attached(role, w=None):
    """Is there actually something behind this role right now?

    The bringer is a thread in this process, so it is attached whenever the
    server is up. The analyzer and the writer are Claude Code sessions, so they
    are attached only while one is heartbeating. Without this the panel showed
    a role as "running" when no session had ever existed, which is the bug this
    answers: a stored intent is not a worker.
    """
    if role == "bringer":
        return True
    w = w or worker_get(role)
    seen = w.get("last_seen")
    return bool(seen) and (time.time() - seen) <= WORKER_ATTACH_SECONDS


# What "running" is called, per role. A person reading the panel wants the verb
# for the job, not the state of the process: a writer that is running is either
# writing or waiting for something to write, and those are different facts.
WORKER_VERBS = {"bringer": "bringing", "analyzer": "analyzing", "writer": "writing"}


def worker_activity(role, w=None):
    """The word to show beside the name.

    Off, idle, paused and error are shown as they are. A **running** worker is
    shown as its own verb while it genuinely holds work and as `waiting`
    otherwise, so "running" never has to stand for both.

    **Decided from what the server knows, not from what the session says.**
    The first version read the heartbeat's `current` and called any non-empty
    value work — so a session reporting "idle, watching the queue", which is
    the honest thing for it to report, was labelled analyzing. A stale `current`
    had the same effect and would never clear.

    The server already owns the truth: a claimed queue row is an analysis in
    progress, and a job being written is a proposal in progress. Those cannot
    be stale and a session cannot misreport them.
    """
    w = w or worker_get(role)
    st = worker_status(role, w)
    if st != "running":
        return st
    if role == "bringer":
        # Set by the poll loop itself, so it is server truth too. Holding the
        # long poll is waiting; only rows in hand are bringing.
        cur = str(w.get("current") or "").strip()
        return "bringing" if cur.startswith("bringing") else "waiting"
    if role == "analyzer":
        return "analyzing" if work_in_flight("analysis") else "waiting"
    # The writer is writing only when the job in flight is *its* job. A
    # proposal the person is writing in their own session is not this role's
    # work, and must not light this row up.
    # Every job in flight, not just the first one found. Two can be written at
    # once — the person's in their session and the queue's in the writer's — so
    # asking only about the first made this row depend on dict order.
    with JOBS_LOCK:
        for job in JOBS.values():
            if job.get("status") not in ("working", "revising"):
                continue
            if (job.get("writing_by") or job.get("initiator")) == "writer":
                return "writing"
    return "waiting"


def worker_status(role, w=None):
    """What to show. "off" outranks everything, because an unattached role is
    not paused or idle, it is absent."""
    w = w or worker_get(role)
    if w.get("state") == "error":
        return "error"
    if not worker_attached(role, w):
        return "off"
    return w.get("state") or "idle"


def worker_may_run(role):
    """What a session is allowed to do right now.

    `run` false means do not start the next piece of work. The reason is
    separated so a session can say why it is holding rather than looking stuck.
    """
    w = worker_get(role)
    if w["state"] == "error":
        return {"run": False, "reason": "error, needs a person", **w}
    if w["state"] == "idle":
        return {"run": False, "reason": "not started", **w}
    if w["state"] == "paused":
        return {"run": False, "reason": "paused", **w}
    # No yield check: a person's job no longer stops the writer. The two run
    # in their own sessions, on their own jobs, side by side.
    return {"run": True, "reason": "", **w}


def worker_raise_error(role, detail, current=""):
    """Something unexpected that a person has to look at.

    Sets the role to error, which stops it, and rings Night Fury once. An alarm
    about our own machinery is not job info, so it never goes to Hungry.
    """
    if role not in WORKER_ROLES:
        return None
    before = worker_get(role)
    out = worker_set(role, state="error", error=str(detail)[:400],
                     note="stopped on an error, needs a person",
                     current=str(current or before.get("current") or "")[:160])
    if before.get("state") != "error":
        lines = [f"<b>Error in the {role}</b>",
                 html.escape(str(detail)[:600])]
        if out.get("current"):
            lines.append("Was on: " + html.escape(out["current"]))
        telegram_send("\n".join(lines), f"worker {role} error")
    print(f"  worker {role} ERROR: {str(detail)[:160]}", flush=True)
    return out


def writer_yield_to_user(what, job_id=""):
    """Record that the person started something. **It no longer stops anybody.**

    The writer used to stand down here so the person's job went first. That was
    right while one session did both; it is wrong now that the person's job is
    written in their own session and the writer has its own. On the user's
    instruction of 2026-10-14 the two run side by side and a button press
    interrupts nothing.

    Kept as a note rather than deleted, because "what is the writer doing and
    why" is worth answering on the Profile tab, and because the three call
    sites are the honest record of when a person took a turn.
    """
    if not job_id:
        return None
    label = f"{what} {job_id}".strip()
    worker_set("writer", note=f"the person started a {what} of their own; "
                              f"carrying on regardless")
    print(f"  person started {label}; writer not interrupted", flush=True)
    return label


def writer_resume_after_user(job_id=""):
    """The person's job finished. Clears a stale yield and nothing else.

    Yielding is gone, so there is normally nothing to clear. This stays so that
    a writer left yielded by the old behaviour — a state file written before
    2026-10-14 — frees itself the first time a person's job lands rather than
    waiting for somebody to notice.
    """
    w = worker_get("writer")
    if not w.get("yielded_to"):
        return None
    worker_set("writer", yielded_to="", note="cleared a yield left by the old behaviour")
    print(f"  cleared stale yield {w['yielded_to']!r}", flush=True)
    return w["yielded_to"]


def load_identity():
    base = {"name": project_name(), "id": None, "url": None,
            "registered_at": None, "thread": None}
    if IDENTITY_FILE.is_file():
        try:
            base.update(json.loads(IDENTITY_FILE.read_text(encoding="utf-8")))
        except Exception:
            pass
    base["name"] = base.get("name") or project_name()
    return base


def save_identity(ident):
    IDENTITY_FILE.write_text(json.dumps(ident, indent=2), encoding="utf-8")
    return ident


def send_registration(url, thread):
    """POST this project's name to the server the user named. A synchronous id
    in the reply is accepted immediately; otherwise the thread waits for the
    server to approve out of band."""
    body = json.dumps({
        "type": "registration_request",
        "name": project_name(),
        "thread": thread["id"],
        "callback": f"http://localhost:{PORT}/api/registration/callback",
    }).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST",
                                 headers={"content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as r:
        raw = r.read().decode("utf-8", "replace")
    try:
        return json.loads(raw)
    except Exception:
        return {"raw": raw[:500]}


def approve_registration(thread, assigned_id, note=""):
    ident = load_identity()
    ident["id"] = str(assigned_id)
    ident["registered_at"] = time.time()
    ident["thread"] = thread["id"] if thread else ident.get("thread")
    save_identity(ident)
    if thread:
        with THREADS_LOCK:
            thread["status"] = "approved"
            thread["assigned_id"] = str(assigned_id)
            thread["updated"] = time.time()
            save_thread(thread)
        thread_say(thread, "server",
                   f"Approved. Your id is {assigned_id}."
                   + (f"\n{note}" if note else ""))
    print(f"  registered as id {assigned_id}", flush=True)
    return ident


def who_wrote(label):
    """Normalise any "by" label to the only two answers that matter.

    The claim takes a free-text session name and /api/generate takes an
    `initiator`, but a person reading the queue card wants one of two words:
    was this the **writer** working the queue, or the **user** pressing a
    button. Anything that is not plainly the worker reads as the user, because
    the UI sends nothing and a person is the default actor.
    """
    v = str(label or "").strip().lower()
    if not v:
        return ""
    return "writer" if ("worker" in v or "writer" in v) else "user"


def new_job(guide_id, person_id, jd, client="", screening="", url="", title="",
            notes="", guide_mode="auto", country="", person_mode="auto",
            initiator="user"):
    job = {
        "id": uuid.uuid4().hex[:8],
        "guide": guide_id,
        # "auto" lets the writer overrule the guide per decision-maker.md;
        # "manual" means the person chose and the writer must not change it.
        "guide_mode": "manual" if guide_mode == "manual" else "auto",
        "person": person_id,
        # Who asked for this job, and who is writing or wrote it. The card in
        # the queue reads these back as "writing by writer" / "written by user".
        "initiator": who_wrote(initiator) or "user",
        "writing_by": "",
        "written_by": "",
        # The same two readings for the person, and the same enforcement. What
        # arrives here is the dropdown either way, so the job is always
        # writable; in auto that value is a default the writer may replace.
        # Unlike the guide, this one has to be settled *first*: whose pool the
        # repository search runs against depends on it.
        "person_mode": "manual" if person_mode == "manual" else "auto",
        "client": client.strip(),
        "jd": jd.strip(),
        # A job off the relay knows its real Upwork title. Only guess when
        # there is nothing to go on, which is a hand-pasted description.
        "title": (title or "").strip() or derive_title(jd),
        "title_from_post": bool((title or "").strip()),
        "screening": screening.strip(),
        "screening_answers": [],
        # One box, two readings, decided by the tick beside it. Ticked, the text
        # is the client's own screening questions. Unticked, it is the user
        # talking to the writer about this proposal. They are stored apart so
        # neither can ever be answered as though it were the other.
        "notes": notes.strip(),
        "notes_reply": "",
        # Client's country, for the translate button under the proposal.
        # A pasted post carries no Location line, so the UI can supply the
        # country by hand. What is typed wins over what is parsed.
        "country": (_country_from_name(country)[0] or detect_country(jd)[0]),
        "language": (_country_from_name(country)[1] if _country_from_name(country)[0]
                     else detect_country(jd)[1]),
        "translation": "",
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
        job.setdefault("guide_mode", "auto")
        job.setdefault("person_mode", "auto")
        job.setdefault("initiator", "user")
        job.setdefault("writing_by", "")
        job.setdefault("written_by", "")
        if not job.get("country"):
            job["country"], job["language"] = detect_country(job.get("jd", ""))
            job.setdefault("translation", "")
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


def _telegram_post(token, chat, text, tag="", bot=""):
    """One message to one bot. Returns True if Telegram accepted it, and logs
    either way, so "did the server send that?" has an answer."""
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
        print(f"  telegram[{bot}] {'sent' if ok else 'refused'} {tag}".rstrip(), flush=True)
        return ok
    except Exception as exc:
        print(f"  telegram[{bot}] send failed {tag}: {exc}", flush=True)
        return False


def telegram_send(text, tag=""):
    """Night Fury: proposal done, boost due, and a write that stalled or failed.

    Never job info. The bot a message arrives from is what says whether it is a
    job worth reading or a proposal worth sending, before either is opened.
    """
    env = read_env()
    return _telegram_post(env.get("TELEGRAM_BOT_TOKEN", ""),
                          env.get("TELEGRAM_CHAT_ID", ""), text, tag, bot="night-fury")


def telegram_jobs_send(text, tag=""):
    """Hungry: job info from the analyzer, and nothing else.

    Its own token and chat id, which is the whole point of the split. Until
    2026-10-13 nothing read these two variables at all: `telegram_new_job` was
    written for Night Fury's token and then disabled, so the jobs bot was
    configured in .env and never once used.
    """
    env = read_env()
    return _telegram_post(env.get("TELEGRAM_JOBS_BOT_TOKEN", ""),
                          env.get("TELEGRAM_JOBS_CHAT_ID", ""), text, tag, bot="hungry")


def work_in_flight(kind=None):
    """What is being worked on right now, or None.

    **Two floors, not one**, since 2026-10-14. They used to be the same lock,
    so a proposal being written stopped the analyzer taking a row — which made
    every button press quietly stall triage as well. They are independent now:

      * `analysis` — a queue row claimed (`analysing_since` set, no analysis yet)
      * `proposal` — a job being written (status "working" or "revising")

    `kind` asks about one of them; omitted, it reports either, which is what
    the old single-floor callers expect.

    **Writing is no longer exclusive.** Two sessions write side by side — the
    person's own job in their session, the queue's in the writer's — so this
    reports what is happening rather than refusing a second writer. The thing
    that keeps them apart is the addressed claim, not this.

    A queued job is not in flight: it has been created but nothing has picked
    it up, so it blocks nothing.
    """
    if kind in (None, "analysis") and QUEUE_DIR.is_dir():
        for f in sorted(QUEUE_DIR.glob("*.json")):
            try:
                item = json.loads(f.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            if item.get("analysing_since") and not item.get("analysis"):
                return {"kind": "analysis", "seq": item["seq"],
                        "since": item["analysing_since"],
                        "title": (item.get("body") or {}).get("title") or ""}
    if kind in (None, "proposal"):
        with JOBS_LOCK:
            for job in JOBS.values():
                if job.get("status") in ("working", "revising"):
                    return {"kind": "proposal", "job": job["id"],
                            "since": job.get("created"),
                            "title": job.get("title") or "",
                            "claimed_by": job.get("claimed_by", "")}
    return None


def _without_work_history(text):
    """The posting, with the client's past contracts cut off the end."""
    text = str(text or "")
    m = WH_HEADER.search(text)
    return (text[:m.start()] if m else text).strip()


def telegram_job_analysed(item):
    """Hungry hears about an analysed job from the general vollna search.

    **Sent after the analysis and never before it**, on the user's instruction
    of 2026-10-13, because the analysis is what produces the three things worth
    knowing: whether the job is dropped, whose job it is, and the client's
    name. A message sent on arrival could carry none of them, and a separate
    alarm for a row merely *waiting* to be analysed was removed the same day —
    it said nothing a person could act on.

    So the three post-analysis facts lead the message:

      * **dropped or not** — expressed by the message existing at all, since a
        dropped row rings neither bell
      * **the person**, which the stack marks decide outright
      * **the client's name**, when the reviews named one

    **One message per job.** The verdict leads, so the notification preview
    still names the job, its marks and its person, and the posting follows in
    the same message. It was two until 2026-10-13, which meant one job buzzed
    the phone twice.
    """
    b = item.get("body", {})
    seq = item.get("seq")
    client = b.get("client") if isinstance(b.get("client"), dict) else {}

    head = ["<b>" + html.escape(b.get("title") or "Untitled job") + "</b>"]
    stack = [x for x in (item.get("stack") or []) if x]
    # The verdict, in one line: the marks and who they chose. Falls back to
    # deriving the person so the message is right even for a row analysed
    # before the person was recorded on it.
    person = item.get("person") or person_for_stack(stack)
    verdict = []
    if stack:
        verdict.append("Stack: " + ", ".join(stack))
    if person:
        verdict.append("Person: " + person)
    if verdict:
        head.append(html.escape(" \u00b7 ".join(verdict)))
    head.append("Budget: " + html.escape(str(b.get("budget") or "not specified")))
    bits = []
    for label, key in (("Rank", "rank"), ("Location", "location")):
        value = client.get(key) or b.get("client" + key[0].upper() + key[1:])
        if value:
            bits.append(f"{label}: {value}")
    if client.get("paymentVerified") or b.get("clientPaymentVerified"):
        bits.append("Payment verified")
    if bits:
        head.append(html.escape(" \u00b7 ".join(str(x) for x in bits)))
    if item.get("client_name"):
        head.append("Client: " + html.escape(item["client_name"]))
    url = b.get("upworkUrl") or b.get("url")
    if url:
        head.append(html.escape(url))

    # One message per job, not two. It used to send the headline and the
    # description separately so each read cleanly on its own; that is two
    # notifications for one job, which the user asked to merge on 2026-10-13.
    # The verdict still comes first, so the notification preview is unchanged.
    headline = "\n".join(head)
    # The work history is cut off before the posting is sent. The feed appends
    # the client's past contracts to the end of the description, so sending it
    # raw sends fifty contracts with it and buries the job in them. The count is
    # already on the queue card and the detail sits behind its button there,
    # which is where it can be read deliberately. analyzer-rule.md step 4 asked
    # for this; the code was still sending the lot until 2026-10-14.
    desc = _without_work_history(b.get("description") or "")
    if desc:
        # Telegram caps a message at 4096 characters and HTML-escaping only ever
        # makes text longer, so the budget is measured on the escaped result
        # rather than on the raw description.
        room = 3900 - len(headline)
        body = html.escape(desc)
        if len(body) > room:
            cut = html.escape(desc[:max(room, 200)]).rstrip()
            body = cut + "\n\n[...truncated, full text is in the queue]"
        text = headline + "\n\n" + body
    else:
        text = headline + "\n\n<i>This post arrived with no description.</i>"
    return telegram_jobs_send(text, f"seq {seq}")


def queue_should_tell_hungry(item):
    """True when this analysed row is one Hungry should hear about.

    Two tests and no others, per the instruction of 2026-10-13: the job came
    from the general vollna search, and it was not dropped. Announced once, so
    a second POST of the same analysis does not ring the phone again; a
    deliberate re-analysis clears the flag and may announce afresh.
    """
    if str((item.get("body") or {}).get("source") or "") != "search":
        return False
    if item.get("dropped"):
        return False
    return not item.get("notified_jobs")


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
        try:
            _write_check_once()
        except Exception as exc:
            print(f"  write check failed: {exc}", flush=True)
        time.sleep(30)


def _boost_check_once():
    now = time.time()
    with JOBS_LOCK:
        due = []
        for job in JOBS.values():
            # A time on the row IS the intent to boost. Requiring the dropdown
            # to be flipped to "yes" as well meant a row with a deadline set sat
            # there silently. Only an explicit "no" suppresses the alarm now.
            if (job.get("when")
                    and str(job.get("boost") or "").lower() != "no"
                    and not job.get("done")
                    and not job.get("boost_notified")):
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


# How long a write may take before the phone is told it is dragging. Measured
# from the moment writing was triggered, which is when the job was created:
# pressing "Write proposal" on a queue row creates it, and so does acting on a
# `bid` decision from the general vollna search. Those are the only two ways a
# write ever starts, so job["created"] is the start of the clock in both.
WRITE_SLOW_AFTER = 8 * 60


def telegram_write_slow(job):
    """Taking longer than usual. Not a failure: the write may still land."""
    mins = int((time.time() - job.get("created", time.time())) // 60)
    lines = ["<b>Still writing</b>",
             html.escape(job.get("title") or job["id"]),
             f"{mins} minutes since writing started, longer than usual.",
             f"Status: {html.escape(str(job.get('status') or 'unknown'))}"]
    if job.get("awaiting_github"):
        lines.append("Held at the github gate, waiting for a reply.")
    if job.get("url"):
        lines.append(html.escape(job["url"]))
    return telegram_send("\n".join(lines), f"job {job['id']} slow")


def telegram_write_failed(job, reason=""):
    """Something came back for this job but there was no proposal in it."""
    lines = ["<b>Failed to write proposal</b>",
             html.escape(job.get("title") or job["id"])]
    if reason:
        lines.append(html.escape(reason))
    lines.append(f"Status: {html.escape(str(job.get('status') or 'unknown'))}")
    if job.get("url"):
        lines.append(html.escape(job["url"]))
    return telegram_send("\n".join(lines), f"job {job['id']} failed")


def _write_check_once():
    """Two things the phone should hear about an unfinished write.

    A write is triggered one of two ways and nothing else: a person presses
    "Write proposal" on a queue row, or a `bid` decision on an undropped job
    from the general vollna search is acted on. Both create the job, so the
    clock starts at job["created"].

    Before this, a job could be created and simply sit: the two that stalled on
    2026-10-13 were queued for over an hour and the phone said nothing either
    way, because the only proposal alarm fired on a *finished* draft. Silence
    read exactly like success.
    """
    now = time.time()
    slow, failed = [], []
    with JOBS_LOCK:
        for job in JOBS.values():
            # A refusal is not a failed write, and a dropped row rings neither
            # bell by design. Cancelled is a person's own decision.
            if job.get("dropped") or job.get("status") == "cancelled":
                continue
            has_text = bool(str(job.get("proposal") or "").strip())
            # A /result that carried no proposal text marked the job on its
            # way out. That is the writer reporting back empty, which is the
            # clearest failure there is, so it rings ahead of the slow alarm.
            if job.get("write_error") and not job.get("notified_failed"):
                failed.append((job, str(job["write_error"])))
                continue
            # Something reached the panel for this job but carried no proposal.
            # /result refuses an empty one outright, so a done job with nothing
            # in it means the state was reached some other way: a crash between
            # the status flip and the save, or a hand-edited record.
            if job.get("status") == "done" and not has_text:
                if not job.get("notified_failed"):
                    failed.append((job, "the job finished with an empty proposal"))
                continue
            if has_text:
                continue
            if (now - job.get("created", now) > WRITE_SLOW_AFTER
                    and not job.get("notified_slow")):
                slow.append(job)
    # Flags set before sending, so a slow Telegram cannot double-fire when the
    # next tick overlaps this one. Same reason as the boost alarm.
    for job, reason in failed:
        with JOBS_LOCK:
            job["notified_failed"] = True
            save_job(job)
        if job_was_dropped(job["id"]):
            print(f"  telegram skipped: job {job['id']} was dropped", flush=True)
            continue
        telegram_write_failed(job, reason)
        print(f"  write-failed telegram sent for job {job['id']}", flush=True)
    for job in slow:
        with JOBS_LOCK:
            job["notified_slow"] = True
            save_job(job)
        if job_was_dropped(job["id"]):
            print(f"  telegram skipped: job {job['id']} was dropped", flush=True)
            continue
        telegram_write_slow(job)
        print(f"  write-slow telegram sent for job {job['id']} "
              f"({int((now - job.get('created', now)) // 60)} min)", flush=True)


def telegram_proposal_done(job):
    """One short message when a proposal is finished and ready to copy."""
    label = "Proposal rewritten" if job.get("status_was_revising") else "Proposal done"
    lines = [f"<b>{label}</b>", html.escape(job.get("title") or job["id"])]
    if job.get("url"):
        lines.append(html.escape(job["url"]))
    return telegram_send("\n".join(lines), f"job {job['id']} done")


def github_gate_open(job):
    """True when this job is waiting on a reply from the github channel."""
    return bool(job.get("awaiting_github")) and not job.get("github_replied")


def clear_github_gate(job, reason, reply=None):
    job["awaiting_github"] = False
    job["github_replied"] = True
    job["github_reply"] = reply or {}
    # Did we get back what we asked about? We know how many repositories were
    # published, so a short reply or a non-zero `failed` is detectable rather
    # than reaching the writer as a complete answer. Recorded on the job so the
    # writer can say so in the note instead of quietly writing from a partial.
    asked = len(job.get("github_refs") or [])
    got = len((reply or {}).get("repos") or [])
    failed = (reply or {}).get("failed")
    short = asked and got < asked
    job["github_partial"] = bool(short or (failed not in (None, 0, "0")))
    job["github_counts"] = {"published": asked, "returned": got, "failed": failed}
    job["note"] = f"github gate cleared ({reason}), writing continues"
    if job["github_partial"]:
        job["note"] += f" — PARTIAL: published {asked}, returned {got}, failed {failed}"
        print(f"  WARNING: github reply for {job['id']} is partial: published {asked}, "
              f"returned {got}, failed={failed}", flush=True)
    save_job(job)
    print(f"  github gate cleared for job {job['id']}: {reason}", flush=True)


def apply_github_reply(body):
    """A message on the github channel can release a job that is waiting.

    Matched on an explicit job id when the reply carries one. A bare ack with
    no id releases the job that has been waiting longest — see the comment
    below for why guessing beat refusing.

    **With two jobs at the gate this can cross wires**, and that is the cost of
    the guess: the counterpart sends acks without a job id, so a reply that
    answered the newer search will release the older job, which then writes
    from repositories that answered a different question. It only bites when
    two sessions hold gates at once. The fix is upstream — replies carrying the
    job id — not here.
    """
    job_id = str(body.get("job") or body.get("job_id") or "").strip()
    with JOBS_LOCK:
        waiting = [j for j in JOBS.values() if github_gate_open(j)]
        if job_id:
            target = JOBS.get(job_id)
            if target is not None and github_gate_open(target):
                target["github_match"] = "by job id"
                clear_github_gate(target, f"reply for {job_id}", body)
                return True
            print(f"  github reply names job {job_id!r}, which is not waiting", flush=True)
            return False
        if not waiting:
            print("  github ack arrived with nothing waiting", flush=True)
            return False
        # A bare ack releases the job that has been waiting longest. Refusing to
        # guess sounded safer and was worse: an ack with no job id would be
        # discarded and the job would wait forever. Oldest-first matches the
        # order the searches were published in.
        #
        # **Since 2026-10-14 the counterpart sends the job id on every reply**,
        # so reaching this branch at all is a regression on their side rather
        # than business as usual. With one gate open the guess is still right.
        # With several it is a coin toss, so the job carries a mark saying the
        # match was guessed and the writer is told to say so in the note.
        waiting.sort(key=lambda j: j.get("created", 0))
        target = waiting[0]
        extra = f", {len(waiting) - 1} still waiting" if len(waiting) > 1 else ""
        if len(waiting) > 1:
            target["github_match"] = "guessed"
            print(f"  WARNING: github reply carried no job id and {len(waiting)} gates "
                  f"were open; released {target['id']} by age, which may be the wrong "
                  f"one. The counterpart agreed to send the job id.", flush=True)
        else:
            target["github_match"] = "guessed-unambiguous"
        clear_github_gate(target, f"bare ack, oldest of {len(waiting)} waiting{extra}", body)
        return True


def relay_publish(channel, body):
    """Post a message to one of the workspace's channels as this worker."""
    out = relay_call("POST", "/publish", {"channel": channel, "body": body})
    print(f"  relay published to {channel}: seq {out.get('seq')}", flush=True)
    return out


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

# A second producer posts jobs under capitalised, spaced keys and calls them
# "job-decision": the same job, plus a bid/skip verdict and the reasoning for
# it. Mapped onto the ordinary shape so those rows look and behave like every
# other one in the queue.
DECISION_KEYS = {
    "Job title": "title",
    "Job link": "upworkUrl",
    "Job description": "description",
    "projectId": "vollnaProjectId",
    "decision": "aiQualification",
    "reason": "aiReason",
}


def _as_text(v):
    """Queue bodies come from more than one producer and the same field is not
    always the same type. One bad row used to take the whole queue down."""
    if v is None:
        return ""
    if isinstance(v, str):
        return v
    if isinstance(v, (list, tuple)):
        return "\n\n".join(str(x) for x in v)
    return str(v)


def _client_name(v):
    """The search feed sends the client as {"name": "Michelle", "mentions": 1}
    on some jobs, a bare string on others, and nothing at all on the rest."""
    if isinstance(v, dict):
        return str(v.get("name") or "").strip()
    return str(v or "").strip()


# The saved Vollna search that produces these calls itself
# "general-vollna-search". In the queue it is just "search".
SEARCH_SOURCES = {"job-decision", "general-vollna-search", "vollna-search"}


# The client's own screening questions, which the general vollna search sends
# alongside the posting. **Optional**: a post that asks nothing carries none of
# these keys at all, so every reader of them has to cope with the field being
# absent rather than empty. The producer's exact spelling is not fixed, so all
# the plausible ones are accepted and normalised onto `screeningQuestions`.
SCREENING_KEYS = ("screeningQuestions", "screening_questions", "screening",
                  "screeningQuestion", "questions")

# "1. ", "2) ", "- ", "Q1: " — list furniture a producer may leave on a question.
SCREENING_BULLET = re.compile(r"^(?:[-*•–]\s*|\(?\d{1,2}[.)]\s*|Q\s*\d{1,2}\s*[.):]\s*)")


def screening_text(value):
    """The client's screening questions as plain text, one question per line.

    The rest of the server already has a shape for these: `job["screening"]` is
    text and `/screening_request` splits it on newlines, so this collapses
    whatever the feed sent into exactly that. Three shapes have to survive,
    because a producer sending fields is free to choose any of them: a list of
    strings, a list of objects where the question is under `question`, `text`,
    `q` or `title`, and one block of text with a question per line.

    List furniture is stripped, since "1. Have you done this?" is the question
    numbered by the producer rather than part of what the client asked. Blank
    entries and duplicates are dropped, so a trailing empty element in the
    array cannot become an empty question for somebody to answer.
    """
    if value is None:
        return ""
    items = []
    if isinstance(value, str):
        items = value.splitlines()
    elif isinstance(value, dict):
        # {"questions": [...]} or {"1": "...", "2": "..."}
        inner = value.get("questions")
        if inner is not None:
            return screening_text(inner)
        items = [value[k] for k in sorted(value)]
    elif isinstance(value, (list, tuple)):
        for v in value:
            if isinstance(v, dict):
                v = (v.get("question") or v.get("text") or v.get("q")
                     or v.get("title") or "")
            items.append(v)
    else:
        items = [value]
    out = []
    for raw in items:
        # One question is one line, whatever whitespace the producer used.
        q = " ".join(_as_text(raw).split())
        q = SCREENING_BULLET.sub("", q).strip()
        if q and q not in out:
            out.append(q)
    return "\n".join(out)


def body_screening(body):
    """The screening questions on a job body, or "" when the post asked none."""
    if not isinstance(body, dict):
        return ""
    for key in SCREENING_KEYS:
        if body.get(key):
            text = screening_text(body[key])
            if text:
                return text
    return ""


def _normalise_job_body(body):
    if not isinstance(body, dict):
        return body
    src = str(body.get("source", "")).lower()
    if str(body.get("type", "")).lower() != "job-decision" and src not in SEARCH_SOURCES:
        # Not a search row, so nothing else here applies — but if some other
        # producer ever sends screening questions they are still the client's
        # questions, and they cost nothing to carry.
        scr = body_screening(body)
        return {**body, "screeningQuestions": scr} if scr else body
    out = dict(body)
    for src, dst in DECISION_KEYS.items():
        if src in out and not out.get(dst):
            v = out[src]
            # that producer sends the description as a list of paragraphs on
            # some jobs and a plain string on others
            if isinstance(v, (list, tuple)):
                v = "\n\n".join(str(x) for x in v)
            out[dst] = v
    out["type"] = "job"
    out["source"] = "search"
    # The client's screening questions, when the post had any. Normalised onto
    # one key in one shape here so that nothing downstream has to know which
    # spelling the producer used or whether it sent a list or a block of text.
    scr = body_screening(out)
    if scr:
        out["screeningQuestions"] = scr
    else:
        out.pop("screeningQuestions", None)      # an empty field is no field
    name = _client_name(out.get("clientName"))
    if name:
        out["clientName"] = name
        client = out.get("client")
        out["client"] = {**client, "name": name} if isinstance(client, dict) else {"name": name}
    return out


# The marks the analyzer may put on a job, per analyzer-rule.md step 1.
STACK_MARKS = ("Data", "AI", "ML", "Full", "Crypto")


# A stack that is only `Full` is dropped. On the user's instruction of
# 2026-10-14: plain web and application work with no data, AI, ML or crypto
# angle to it is commodity work, and nothing here differentiates a bid on it.
# An empty stack was already a drop, so there are now two ways to get one.
FULL_ONLY = frozenset({"Full"})


def stack_is_dropped(stack):
    """True when these marks mean the row goes.

    Two cases: no mark at all, which means no engineer here can do the work;
    and `Full` on its own, which means they could but it is not worth a
    Connect. Both delete the row, so be sure before posting either.
    """
    marks = frozenset(m for m in (stack or []) if m in STACK_MARKS)
    return (not marks) or marks == FULL_ONLY


def person_for_stack(stack):
    """The person these marks choose, or "" when there are no marks.

    Two rules, both from the user on 2026-10-13, and `Crypto` is checked first:

      1. **`Crypto` present is Zachary**, unconditionally. Cryptocurrency and
         blockchain work is his whatever else the job also wants.
      2. Otherwise **`Data` present and `AI` absent is Zachary**; everything
         else is Connor. Data-led work is his, and the moment a job wants AI it
         is Connor's — so `Data` + `AI` is Connor, and the `AI` mark decides it.

    Rule 1 takes precedence, so `Crypto` + `AI` is Zachary even though `AI`
    would otherwise send it to Connor. That is the one place the two rules
    disagree, and it is resolved this way because the crypto instruction was
    given as a flat assignment with no exception attached to it.

    Rule 2 was first written as the mark sets enumerated, from the three the
    instruction named; `Data`+`ML`+`Full` was missing and went to Connor, which
    the user corrected the same day. It is a predicate now, because that is the
    actual rule and a predicate cannot drop a case.

    No marks means the row was dropped, and a dropped row is never written, so
    it has no person. Anything else resolves, so the analyzer never has to
    guess and the choice cannot drift between one job and the next.
    """
    marks = {m for m in (stack or []) if m in STACK_MARKS}
    # A dropped row has no person, and `Full` on its own is now a drop, so it
    # resolves to nobody rather than to Connor as it used to.
    if stack_is_dropped(marks):
        return ""
    if "Crypto" in marks:
        return "Zachary"
    return "Zachary" if ("Data" in marks and "AI" not in marks) else "Connor"


WH_HEADER = re.compile(r"^Work history \((\d+) past contracts?\):\s*$", re.M)
WH_ENTRY = re.compile(r"^(in progress|#(\d+))\s+(.*)$")
WH_FEEDBACK = re.compile(r"^to (freelancer|client)\s+([\d.]+):\s*(.*)$")


def parse_work_history(description):
    """The client's past contracts, which arrive inside the description text.

    The search feed appends them under "Work history (N past contracts):"
    rather than sending them as fields, which is why nothing read them before.
    Each entry is a status line, then one line of terms, then up to two lines
    of feedback:

        #14 Consulting Support
        Feb 2026 - Aug 2026 | 5hrs | $23.63/hr | billed $118.13
        to freelancer 5: (no text)
        to client 5: One of the best employers to work for!

    "in progress" marks a live contract, "#N" a finished one. Any of the terms
    can be "?" where Upwork does not show it and feedback text can be
    "(no text)", so every field here is allowed to come back empty.

    Returns None when there is no work-history section at all, which is a
    different thing from a client whose section says zero contracts.
    """
    text = _as_text(description)
    m = WH_HEADER.search(text)
    if not m:
        return None
    entries, cur = [], None

    for raw in text[m.end():].splitlines():
        line = raw.strip()
        if not line:
            continue
        hit = WH_ENTRY.match(line)
        if hit:
            if cur:
                entries.append(cur)
            cur = {"status": "in progress" if hit.group(1) == "in progress" else "finished",
                   "index": int(hit.group(2)) if hit.group(2) else None,
                   "name": hit.group(3).strip(),
                   "period": "", "hours": "", "rate": "", "billed": "",
                   "to_freelancer": None, "to_client": None}
            continue
        if cur is None:
            break                   # past the section: another block has begun
        fb = WH_FEEDBACK.match(line)
        if fb:
            body = fb.group(3).strip()
            side = "to_freelancer" if fb.group(1) == "freelancer" else "to_client"
            cur[side] = {"score": fb.group(2),
                         "text": "" if body == "(no text)" else body}
            continue
        if "|" in line:
            # Read by position, because a "?" gives nothing to recognise it by.
            parts = [p.strip() for p in line.split("|")] + ["", "", "", ""]
            cur["period"], cur["hours"], cur["rate"] = parts[0], parts[1], parts[2]
            billed = parts[3]
            cur["billed"] = billed[6:].strip() if billed.lower().startswith("billed") else billed
            continue
        cur["name"] = f"{cur['name']} {line}".strip()   # a name that wrapped
    if cur:
        entries.append(cur)
    return {"count": int(m.group(1)), "entries": entries}


def parse_labelled_body(text):
    """general-vollna-search posts a job as labelled text, not as fields.

    relay_pull used to replace any non-dict body with {}, so such a job failed
    _looks_like_a_job and was filed as an empty "Instruction" thread and acked:
    it never arrived as a job. This turns the labels back into the producer's
    own key names, so _normalise_job_body maps them like any other row of its.

    The verdict is preserved here, because the queue row has columns for it.
    queue_jd then leaves it out again when it builds the job description, so
    the decision reaches the queue but never the proposal.
    """
    labels = {
        "job title": "Job title", "title": "Job title",
        "job link": "Job link", "link": "Job link", "url": "Job link",
        "job description": "Job description", "description": "Job description",
        "projectid": "projectId", "project id": "projectId",
        "decision": "decision", "qualification": "decision",
        "reason": "reason",
        "budget": "budget", "published": "published", "posted": "posted",
        "location": "clientLocation", "rank": "clientRank",
        "rating": "clientRating", "reviews": "clientReviews",
        "payment verified": "clientPaymentVerified", "spent": "clientSpent",
        "registered": "clientRegistered",
        # Optional, and the labelled shape is where the continuation rule earns
        # its keep: the questions arrive as the lines under the label, one per
        # line, and land in this one field for screening_text to split.
        "screening questions": "screeningQuestions",
        "screening question": "screeningQuestions",
        "screening": "screeningQuestions",
        "questions": "screeningQuestions",
    }
    out, current = {}, None
    for raw in text.splitlines():
        line = raw.strip()
        head, sep, rest = line.partition(":")
        key = labels.get(head.strip().lower()) if sep else None
        if key:
            current = key
            out[key] = rest.strip()
            continue
        if current and line:
            out[current] = f"{out[current]}\n{line}".strip()
    out = {k: v for k, v in out.items() if v}
    if out and "Job title" not in out:
        for raw in text.splitlines():
            line = raw.strip()
            head, sep, _ = line.partition(":")
            if sep and labels.get(head.strip().lower()):
                break
            if line:
                out["Job title"] = line
                break
    out = _unswallow_title(out)
    if out:
        out.setdefault("source", "general-vollna-search")
    return out


# A title is one line. Anything longer means the continuation rule above ran
# away with the posting.
TITLE_SANE_CHARS = 200


def _unswallow_title(out):
    """Put the posting back where it belongs when the title ate it.

    The continuation rule is what lets a description run over many lines: a
    line that is not itself a known label extends the field above it. When the
    producer sends the body straight after `Job title:` with no
    `Job description:` in front of it, every one of those lines lands in the
    title instead, and the description is left empty or a stub.

    Seen on 2026-10-14, queue row 692: a 5038-character title across 74 lines
    carrying the whole posting, the project info and the work history, beside a
    13-character description reading "Role Overview". The row could not be
    analysed at all.

    The fix keeps the first line as the title and hands the rest to the
    description. Nothing is discarded: a stub description is kept and appended,
    because a fragment the producer sent is still the producer's text.
    """
    title = str(out.get("Job title") or "")
    if len(title) <= TITLE_SANE_CHARS or "\n" not in title:
        return out
    first, _, rest = title.partition("\n")
    rest = rest.strip()
    if not rest:
        return out
    stub = str(out.get("Job description") or "").strip()
    body = rest
    if stub and stub not in rest:
        body = f"{rest}\n\n{stub}"
    out["Job title"] = first.strip()[:200]
    out["Job description"] = body
    print(f"  malformed row repaired: title held {len(title)} chars, "
          f"moved {len(rest)} of them into the description", flush=True)
    return out


def _looks_like_a_job(body):
    if not isinstance(body, dict):
        return False
    if str(body.get("type", "")).lower() in NOISE_TYPES:
        return False
    return bool(
        body.get("title") or body.get("url") or body.get("upworkUrl")
        or body.get("description") or body.get("jobDescription")
    )


# What the relay says this project is, re-learned on every poll. Deliberately
# in memory and not on disk: /messages reports the worker id and the channel of
# every message it hands over, so a restart knows all of this again inside one
# poll, and there is no state file to go stale or to leak into a public repo.
RELAY_STATE = {
    "worker_id": "",        # the identity the relay allocated, from /messages
    "channels": {},         # channel -> {"seen": n, "last": epoch}
    "last_poll": None,      # a successful /messages, whether or not it carried anything
    "last_error": "",
    "notices": 0,           # how many the relay has sent this project
}
RELAY_STATE_LOCK = threading.Lock()


def relay_seed_channels():
    """Seed the channel map from stored history, at boot.

    The relay exposes no way to list the channels a worker is allocated — a
    channel is only ever learned from a message arriving on it. Without this,
    /api/relay/status reads an empty list after every restart until the next
    job lands, which looks like "allocated nothing" rather than "nothing has
    arrived yet". The queue rows and the report threads both record the channel
    they came in on, so the answer is already on disk.
    """
    seen = {}
    for folder, pattern in ((QUEUE_DIR, "*.json"), (THREADS_DIR, "*.json")):
        if not folder.is_dir():
            continue
        for f in folder.glob(pattern):
            try:
                row = json.loads(f.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            ch = str(row.get("channel") or "")
            if not ch or ch == "pasted":      # a paste never came off the relay
                continue
            got = seen.setdefault(ch, {"seen": 0, "last": None})
            got["seen"] += 1
            ts = row.get("ts") or row.get("created")
            if isinstance(ts, (int, float)):
                got["last"] = max(got["last"] or 0, ts)
    if seen:
        with RELAY_STATE_LOCK:
            for ch, row in seen.items():
                RELAY_STATE["channels"].setdefault(ch, row)
        print(f"  relay channels seen before: {', '.join(sorted(seen))}", flush=True)


def relay_note_poll(payload):
    """Record what a successful poll told us about ourselves.

    The relay answers /messages with the worker id it knows us by and, when it
    has something to say to this project rather than work to give it, a
    `notices` array. Both used to be dropped on the floor: relay_pull read
    `messages` and nothing else, so the project could not say which channel it
    was allocated and never heard a word the relay addressed to it.
    """
    with RELAY_STATE_LOCK:
        if payload.get("worker_id"):
            RELAY_STATE["worker_id"] = str(payload["worker_id"])
        RELAY_STATE["last_poll"] = time.time()
        RELAY_STATE["last_error"] = ""
        for msg in payload.get("messages", []):
            ch = str(msg.get("channel") or "")
            if not ch:
                continue
            row = RELAY_STATE["channels"].setdefault(ch, {"seen": 0, "last": None})
            row["seen"] += 1
            row["last"] = time.time()


def relay_take_notices(payload):
    """A notice is the relay talking to this project. File each one as a thread.

    That is what the Report page already is, so a notice arrives the same way
    an instruction message does and is read in the same place. Kept defensive
    about the shape: the array has only ever come back empty here, so a notice
    may be a string or an object and either must survive.
    """
    for notice in payload.get("notices", []) or []:
        if isinstance(notice, dict):
            title = (notice.get("title") or notice.get("subject")
                     or notice.get("type") or "Notice from the relay")
            text = (notice.get("text") or notice.get("message")
                    or notice.get("body") or json.dumps(notice, indent=2))
            channel = str(notice.get("channel") or "")
            sender = str(notice.get("sender") or "relay")
        else:
            title, text, channel, sender = "Notice from the relay", str(notice), "", "relay"
        t = new_thread("instruction", str(title), channel=channel,
                       sender=sender, text=str(text), role="server")
        with RELAY_STATE_LOCK:
            RELAY_STATE["notices"] += 1
        print(f"  relay notice -> thread {t['id']}: {t['title'][:46]!r}", flush=True)


def relay_enrol(label=""):
    """Enrol this machine with the relay as a worker.

    A one-time handshake whose result lives on the relay, keyed to the worker
    id and token in .env. It used to be the only thing proposal_bridge.py did
    that was worth keeping, and when the bridge was deleted on 2026-10-13 the
    project was left with no way to enrol at all: fine while this machine
    stayed enrolled, useless the moment the token rotated, the worker was
    removed in the console, or the repo was cloned somewhere new.

    This enrols and nothing else. It cannot create a job, which is the whole
    reason the bridge went.
    """
    env = read_env()
    worker = env.get("RELAY_WORKER", "").strip()
    token = env.get("RELAY_TOKEN", "").strip()
    if not worker or not token:
        raise RuntimeError("no RELAY_WORKER or RELAY_TOKEN in .env")
    # The relay's /enrol takes `name` and requires it. proposal_bridge.py sent
    # {worker_id, token, label} and would now be rejected 422 — its enrol code
    # had gone stale against the live API some time before it was deleted, so
    # this is the current shape rather than the one it used. The worker id and
    # token still travel: the relay ignores extras it does not know, and if it
    # ever honours them again this asks for the identity .env already holds.
    body = {"name": worker, "worker_id": worker, "token": token,
            "label": label or f"{project_name()} (local)"}
    try:
        out = relay_call("POST", "/enrol", body)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:300]
        if exc.code == 409:
            # Already enrolled is the normal answer on a machine that works.
            return {"status": "already", "worker_id": worker, "detail": detail}
        raise RuntimeError(f"relay refused the enrolment: {exc.code} {detail}") from exc
    out = out if isinstance(out, dict) else {}
    return {"status": out.get("status") or "sent", "worker_id": worker,
            "message": out.get("message") or "", "detail": ""}


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
    # Who the relay says we are, which channels it is handing us, and anything
    # it has to say to this project. Done before the messages are walked so a
    # failure further down still leaves the identity recorded.
    relay_note_poll(payload)
    relay_take_notices(payload)
    kept = []
    for msg in payload.get("messages", []):
        raw_body = msg.get("body")
        if isinstance(raw_body, dict):
            body = raw_body
        elif isinstance(raw_body, str) and raw_body.strip():
            body = parse_labelled_body(raw_body)      # labelled text, not fields
        else:
            body = {}
        body = _normalise_job_body(body)
        if msg.get("channel") == "github":
            # Replies land here from whichever worker answers the search.
            # Our own github_refs posts come back too; those are not replies.
            if body.get("type") != "github_refs":
                apply_github_reply(body)
            relay_call("POST", "/ack", {"channel": msg["channel"], "seq": msg["seq"]})
            continue
        if _looks_like_a_job(body):
            existing = QUEUE_DIR / f"{msg['seq']:06d}.json"
            if not existing.is_file():        # never clobber a typed-in client name
                item = {"seq": msg["seq"], "channel": msg["channel"],
                        "sender": msg.get("sender", ""), "ts": msg.get("ts", time.time()),
                        "body": body,
                        "client_name": _client_name(body.get("clientName")),
                        # The client's screening questions, when the feed sent
                        # them. Kept on the row as well as in the body so the
                        # card can say there are some and /api/generate can
                        # hand them to the job without re-deriving them.
                        "screening": body_screening(body),
                        "used": False,
                        # The analyzer fires on arrival for the search feed only,
                        # per analyzer-rule.md. Other alerts are not analysed.
                        "analysis_wanted": body.get("source") == "search",
                        "analysis": ""}
                queue_save(item)
                kept.append(item)
                title = body.get("title") or body.get("jobTitle") or ""
                print(f"  relay job seq {msg['seq']} arrived from {msg.get('sender','?')}: "
                      f"type={body.get('type','?')} title={title[:46]!r}", flush=True)
        else:
            # Not a job, not a github reply: the server is talking to us rather
            # than sending work. That is what the Report page is for, so keep
            # it as a thread instead of dropping it on the floor.
            title = (body.get("title") or body.get("subject")
                     or body.get("instruction") or body.get("type") or "Instruction")
            text = (body.get("text") or body.get("message") or body.get("body")
                    or body.get("instruction") or json.dumps(body, indent=2))
            t = new_thread("instruction", str(title), channel=msg.get("channel", ""),
                           sender=msg.get("sender", ""), text=str(text), role="server")
            print(f"  relay instruction seq {msg['seq']} -> thread {t['id']}: "
                  f"{t['title'][:46]!r}", flush=True)
        relay_call("POST", "/ack", {"channel": msg["channel"], "seq": msg["seq"]})
    # Arrival is still not announced: the queue in the UI already shows a new
    # row, and the phone message was noise. Disabled on the user's instruction
    # of 2026-09-24, and telegram_new_job() was deleted on 2026-10-13 — it had
    # been dead for three weeks and, because it called telegram_send, anyone
    # putting it back would have pushed job info down Night Fury. What Hungry
    # gets instead is the *analysed* job, from telegram_job_analysed, which
    # fires once the verdict exists rather than the moment a row lands.
    return len(kept)


def _row_write_state(item):
    """Writing or written, and by whom, for one queue row."""
    job = JOBS.get(item.get("job_id", "")) or {}
    if not job:
        return {"write_state": "", "write_by": ""}
    if str(job.get("proposal") or "").strip():
        return {"write_state": "written",
                "write_by": job.get("written_by") or job.get("initiator") or ""}
    if job.get("status") in ("working", "revising"):
        return {"write_state": "writing",
                "write_by": job.get("writing_by") or job.get("initiator") or ""}
    return {"write_state": "", "write_by": ""}


def queue_items():
    """Newest first. Each row is what the UI needs and nothing more.

    **A dropped row is not here to be filtered out.** It is deleted the moment
    the analysis drops it, on the user's instruction of 2026-10-13: hiding it
    was the first attempt and left the directory growing with rows nobody would
    ever look at again.
    """
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
            "reason": b.get("aiReason", ""),
            # which alert this row came in on, so the queue says where its
            # jobs are coming from rather than presenting one undifferentiated list
            "source": b.get("source", "") or b.get("filter", ""),
            "sender": item.get("sender", ""),
            "analysis": item.get("analysis", ""),
            "analysis_wanted": bool(item.get("analysis_wanted")),
            # Set while a session actually holds this row, so the card can say
            # "analysing…" only when that is true and "awaiting analysis"
            # otherwise. Without it the two states looked identical.
            "analysing_since": item.get("analysing_since"),
            "has_jd": bool(_as_text(b.get("description")).strip()),
            # The client's screening questions, if the post asked any. The text
            # travels with the row because it is short and a person looking at
            # the card wants to know the questions exist before pressing Write.
            "screening": item.get("screening") or body_screening(b),
            # Just the count, so the row stays small. The entries themselves are
            # fetched per item when the button is pressed.
            "work_history": (parse_work_history(b.get("description")) or {}).get("count"),
            "stack": item.get("stack") or [],
            "dropped": bool(item.get("dropped")),
            "client_name": _client_name(item.get("client_name")) or _client_name(client.get("name")),
            "used": bool(item.get("used")),
            "written_at": item.get("written_at"),
            "job_id": item.get("job_id", ""),
            "job_status": (JOBS.get(item.get("job_id", ""), {}) or {}).get("status", ""),
            "has_proposal": bool((JOBS.get(item.get("job_id", ""), {}) or {}).get("proposal")),
            # What the card shows, and who did it. "writing" while somebody
            # holds the job, "written" once a proposal exists, "" before
            # anything started. The second half is the point: a person looking
            # at the queue wants to know whether the writer or they themselves
            # are on it, so two sessions never duplicate a letter.
            **_row_write_state(item),
        })
    out.sort(key=lambda r: r["seq"])      # newest at the bottom
    return out


def queue_mark_written(job_id):
    """Mark the queue row as written, and keep it.

    It used to be deleted the moment a proposal landed, on the grounds that a
    finished row has no work left in it. That also threw away the only copy of
    the original relay post, so the job could never be run again from the
    queue. The row now stays and carries the job id, which is what lets the UI
    offer it a second time.
    """
    if not job_id or not QUEUE_DIR.is_dir():
        return None
    for f in sorted(QUEUE_DIR.glob("*.json")):
        try:
            item = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if item.get("job_id") == job_id:
            item["used"] = True
            item["written_at"] = time.time()
            queue_save(item)
            return item.get("seq")
    return None


def job_was_dropped(job_id):
    """True when this job's queue row was marked dropped by the analyser.

    A dropped row is one no engineer here can write: the analysis found no
    Data, AI, ML, Full or Crypto work in it. The writer still posts a /result saying
    so, because the UI needs something in the box, but that is a refusal and
    not a finished proposal, so no alarm goes out for it.
    """
    if not job_id or not QUEUE_DIR.is_dir():
        return False
    for f in sorted(QUEUE_DIR.glob("*.json")):
        try:
            item = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if item.get("job_id") == job_id:
            return bool(item.get("dropped"))
    return False


# A pasted row needs a seq of its own, and it must never collide with a relay
# message's. Relay seqs count up from 1 and are in the hundreds; pasted rows
# count up from here, so the two ranges cannot meet.
PASTED_SEQ_BASE = 900000


def next_pasted_seq():
    highest = PASTED_SEQ_BASE
    if QUEUE_DIR.is_dir():
        for f in QUEUE_DIR.glob("*.json"):
            try:
                seq = int(f.stem)
            except ValueError:
                continue
            if seq >= PASTED_SEQ_BASE:
                highest = max(highest, seq + 1)
    return highest


def queue_delete(seq):
    """Remove one row from the queue. True if it was there."""
    f = QUEUE_DIR / f"{int(seq):06d}.json"
    if not f.is_file():
        return False
    try:
        f.unlink()
        return True
    except OSError:
        return False


def queue_get(seq):
    f = QUEUE_DIR / f"{int(seq):06d}.json"
    if not f.is_file():
        return None
    return json.loads(f.read_text(encoding="utf-8"))


# Field order for the job description built out of a relay row. The title goes
# first because queue_jd's first line becomes the job's title; then the posting
# itself, then the terms, then who is offering them.
JD_KEYS = ("description", "jobDescription", "jd", "snippet", "summary", "details", "text")
JD_FACTS = [("Budget", "budget"), ("Published", "published"), ("Posted", "posted")]
JD_CLIENT_FIELDS = [
    ("Rank", "rank"), ("Rating", "rating"), ("Payment verified", "paymentVerified"),
    ("Location", "location"), ("Reviews", "reviews"), ("Jobs posted", "jobsPosted"),
    ("Hire rate", "hireRate"), ("Spent", "spent"), ("Registered", "registered"),
]


def queue_jd(item):
    """The job description the writer works from, built out of a queue row.

    Lived in proposal_bridge.py until the bridge was removed on 2026-10-13. It
    is kept here because the queue is now the only way a job is created, so
    this is the only formatter: every job description the writer ever sees is
    built by this function.

    The body is already a dict by the time a row is saved — relay_pull runs
    parse_labelled_body and _normalise_job_body on the way in — so the dict
    path below is the real one. The verdict is deliberately not printed: the
    producer's own bid decision belongs to the queue row, and inside the job
    description it would read as the client's words.
    """
    body = item.get("body", {})
    if isinstance(body, str):
        return body.strip()
    # A pasted row is handed back exactly as it was typed. Clients plant
    # application instructions in the posting ("start your proposal with the
    # word banana"), so prepending a derived title or appending a Link line
    # would move the first line and lose the job. The link is a field on the
    # row, and reaches the job through data["url"] instead.
    if isinstance(body, dict) and body.get("pasted"):
        return str(body.get("description") or "").strip()
    if not isinstance(body, dict):
        return json.dumps(body, indent=2, ensure_ascii=False)

    lines = [str(body.get("title") or "Untitled job").strip()]
    for key in JD_KEYS:
        value = body.get(key)
        if isinstance(value, list):      # that producer sends it as paragraphs
            value = "\n\n".join(str(v).strip() for v in value if str(v).strip())
        if isinstance(value, str) and value.strip():
            lines += ["", value.strip()]
            break

    terms = [f"{label}: {body[key]}" for label, key in JD_FACTS if body.get(key)]
    link = body.get("upworkUrl") or body.get("url") or body.get("link")
    if link:
        terms.append(f"Link: {link}")
    if terms:
        lines += ["", *terms]

    client = body.get("client") if isinstance(body.get("client"), dict) else {}
    facts = []
    for label, key in JD_CLIENT_FIELDS:
        flat = body.get("client" + key[0].upper() + key[1:])
        value = client.get(key, flat)
        if value not in (None, ""):
            facts.append(f"{label}: {value}")
    if facts:
        lines += ["", "Client:", *[f"- {f}" for f in facts]]
    return "\n".join(lines)


def pull_loop():
    """Hold a request open on the relay, so a new job arrives here at once.

    This is the **bringer**, and it is the one role that really runs in this
    process. Paused or stopped, it does not poll at all: no new rows arrive
    until it is started again, which is the point of having the button.
    """
    while True:
        allowed = worker_may_run("bringer")
        if not allowed["run"]:
            worker_set("bringer", current="",
                       note=f"not polling ({allowed['reason']})",
                       last_seen=time.time())
            time.sleep(5)
            continue
        try:
            worker_set("bringer", current="holding the relay poll",
                       last_seen=time.time(), note="")
            kept = relay_pull(wait=25)
            if kept:
                # Held just long enough for the panel to show it: the next loop
                # puts it back to holding the poll.
                worker_set("bringer",
                           current=f"bringing {kept} job{'' if kept == 1 else 's'}",
                           last_seen=time.time())
        except Exception as exc:
            with RELAY_STATE_LOCK:
                RELAY_STATE["last_error"] = str(exc)[:300]
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
    # A retitled job would otherwise leave its old file behind. This glob stays
    # narrow on purpose: it runs on every save, and widening it to *_<id>*.md
    # would delete a translation every time the proposal was re-exported.
    for stale in PROPOSALS.glob(f"*_{job['id']}.md"):
        if stale.name != name:
            stale.unlink()

    imgs = job.get("images")
    body = job.get("proposal", "").strip()
    lines = [
        f"# {job.get('title') or job['id']}",
        "",
        f"- **Person:** {job.get('person','')}"
        f"{' (chosen by hand)' if job.get('person_mode') == 'manual' else ' (decided per job)'}",
        f"- **Guide:** {job.get('guide','')}"
        f"{' (chosen by hand)' if job.get('guide_mode') == 'manual' else ' (decided per job)'}",
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

    if job.get("notes"):
        lines += ["---", "", "## What the user asked for", "", job["notes"].strip(), ""]
        if job.get("notes_reply"):
            lines += ["**Reply:**", "", job["notes_reply"].strip(), ""]

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
    """Only for an explicit delete. The timed purge deliberately leaves these.

    The glob is deliberately wider than the one export_proposal writes: a job
    can have more files than its own export, such as a translation saved as
    ..._<id>_ES.md. Matching on the id alone takes those with it, so a deleted
    row cannot leave a copy of its proposal behind in the archive.
    """
    for f in PROPOSALS.glob(f"*_{job['id']}*.md"):
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
    for p in sorted(PROFILES.glob("*.md")):
        if p.name in NOT_A_PERSON or "-" in p.stem:
            continue
        out.append({"id": p.stem, "name": title_of(p, p.stem), "file": f"profiles/{p.name}"})
    return out


def read_guide(guide_id: str) -> str:
    p = GUIDES / f"{guide_id}.md"
    if not p.is_file():
        raise FileNotFoundError(f"no guide named {guide_id}")
    return p.read_text(encoding="utf-8")


def read_person(person_id: str) -> str:
    # The id arrives from the browser, so it must not be able to climb out of
    # profiles/ and read the server's own files.
    # A hyphen means supporting material rather than a person, which is the
    # same rule list_people() applies: connor-github.md is read by hand when a
    # Connor proposal needs it, never built into a prompt as though it were him.
    if "/" in person_id or "\\" in person_id or person_id.startswith(".") or "-" in person_id:
        raise FileNotFoundError(f"no person profile named {person_id}")
    p = PROFILES / f"{person_id}.md"
    if not p.is_file() or p.name in NOT_A_PERSON:
        raise FileNotFoundError(f"no person profile named {person_id}")
    return p.read_text(encoding="utf-8")


def build_prompt(guide_id: str, person_id: str, jd: str, client: str = "",
                 screening: str = "", notes: str = ""):
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
    told = ""
    if notes.strip():
        told = (
            "\n\n=== WHAT THE USER TOLD YOU ABOUT THIS PROPOSAL ===\n"
            f"{notes.strip()}\n\n"
            "This is the user talking to you, exactly as if they had typed it into a chat. It is "
            "NOT the client and NOT a screening question, so never answer it inside the "
            "proposal. Follow it while writing. If any of it asks you something, or is a call "
            "you had to make and they should see, reply to it separately after the proposal.\n"
        )
    user = f"=== JOB DESCRIPTION ===\n{jd.strip()}\n{who}{ask}{told}\nWrite the proposal."
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
        if path == "/api/stats":
            # The three counts the Profile tab shows above the workers. Computed
            # here rather than in the page so the definitions live in one place:
            # what counts as a source, as analysed, as written.
            rows = queue_items()
            analysed = [r for r in rows if r.get("analysis")]

            def _src(r):
                return str(r.get("source") or "").lower() or "(none)"

            def _dec(r):
                return str(r.get("qualification") or "").lower()

            src = {}
            for r in rows:
                src[_src(r)] = src.get(_src(r), 0) + 1
            dec = {}
            for r in analysed:
                dec[_dec(r)] = dec.get(_dec(r), 0) + 1
            with JOBS_LOCK:
                written = [j for j in JOBS.values() if str(j.get("proposal") or "").strip()]
                boosted = [j for j in written if str(j.get("when") or "").strip()]
                n_written, n_boost = len(written), len(boosted)
            known = ("search", "vollna", "upwork")
            return self._send(200, {
                "queue": {
                    "total": len(rows),
                    "search": src.get("search", 0),
                    "vollna": src.get("vollna", 0),
                    "upwork": src.get("upwork", 0),
                    "other": sum(v for k, v in src.items() if k not in known),
                },
                "analysed": {
                    "total": len(analysed),
                    "bid": dec.get("bid", 0),
                    "manual_check": dec.get("manual check", 0),
                    "skip": dec.get("skip", 0),
                    "pending": len(rows) - len(analysed),
                },
                "written": {
                    "total": n_written,
                    "boosted": n_boost,
                    "unboosted": n_written - n_boost,
                },
            })

        if path == "/api/workers":
            rows = []
            for role in WORKER_ROLES:
                w = worker_get(role)
                w["may_run"] = worker_may_run(role)["run"]
                w["attached"] = worker_attached(role, w)
                # What the panel shows. "off" when nothing is behind the role,
                # whatever intent is stored against it.
                w["status"] = worker_status(role, w)
                # What the panel prints beside the name: the role's own verb
                # while it is working, "waiting" while it is running but idle.
                w["activity"] = worker_activity(role, w)
                # Outstanding until the session echoes the seq back. This is
                # what answers "did it hear me?" without guessing.
                w["command_pending"] = bool(
                    int(w.get("command_seq") or 0) > int(w.get("acked_seq") or 0))
                w["kind"] = "thread" if role == "bringer" else "session"
                rows.append(w)
            return self._send(200, {"workers": rows})

        if path == "/api/relay/status":
            # What the relay allocated this project, read off the live poll
            # rather than a stored file. "channels" is what it has actually
            # handed us, so an empty list means nothing has arrived yet, not
            # that nothing is allocated.
            with RELAY_STATE_LOCK:
                st = {
                    "worker_id": RELAY_STATE["worker_id"],
                    "channels": [
                        {"channel": ch, "seen": v["seen"], "last": v["last"]}
                        for ch, v in sorted(RELAY_STATE["channels"].items())
                    ],
                    "last_poll": RELAY_STATE["last_poll"],
                    "last_error": RELAY_STATE["last_error"],
                    "notices": RELAY_STATE["notices"],
                }
            env = read_env()
            st["configured_worker"] = env.get("RELAY_WORKER", "")
            st["relay"] = env.get("RELAY_URL", "")
            st["connected"] = bool(st["worker_id"]) and not st["last_error"]
            return self._send(200, st)

        if path == "/api/identity":
            return self._send(200, load_identity())

        if path == "/api/threads":
            with THREADS_LOCK:
                rows = sorted(THREADS.values(),
                              key=lambda t: (t["completed"], -t["updated"]))
            return self._send(200, {"threads": [thread_row(t) for t in rows]})

        m = re.fullmatch(r"/api/thread/([0-9a-f]{8})", path)
        if m:
            with THREADS_LOCK:
                t = THREADS.get(m.group(1))
            if not t:
                return self._send(404, {"error": "no such thread"})
            return self._send(200, t)

        # The client's past contracts, on demand. Kept out of /api/queue because
        # one row can carry fifty of them and the queue is polled constantly.
        m = re.fullmatch(r"/api/queue/(\d+)/history", path)
        if m:
            seq = int(m.group(1))
            f = QUEUE_DIR / f"{seq:06d}.json"
            if not f.is_file():
                return self._send(404, {"error": "no such queue row"})
            try:
                body = json.loads(f.read_text(encoding="utf-8")).get("body") or {}
            except (OSError, ValueError) as exc:
                return self._send(500, {"error": f"could not read row: {exc}"})
            wh = parse_work_history(body.get("description"))
            if wh is None:
                return self._send(200, {"seq": seq, "count": None, "entries": [],
                                        "note": "this job carries no work-history section"})
            return self._send(200, {"seq": seq, **wh})

        if path == "/api/work/inflight":
            # One thing at a time. A session asks this before starting
            # anything; `busy` true means finish that first.
            busy = work_in_flight()
            return self._send(200, {"busy": bool(busy), "work": busy,
                                    "analysis": work_in_flight("analysis"),
                                    "proposal": work_in_flight("proposal")})

        m = re.fullmatch(r"/api/queue/(\d+)/writable", path)
        if m:
            # Asked before a write starts, so the button can warn instead of
            # quietly creating a second job for a post somebody is already on.
            item = queue_get(m.group(1))
            if not item:
                return self._send(404, {"error": "no such queue item"})
            st = _row_write_state(item)
            out = {"seq": item["seq"], **st, "job_id": item.get("job_id", "")}
            if st["write_state"] == "writing":
                out.update(ok=False, reason="in progress",
                           message=f"This job is being written by the "
                                   f"{st['write_by'] or 'another session'} right now.")
            elif st["write_state"] == "written":
                out.update(ok=True, confirm=True,
                           message=f"This job was already written by the "
                                   f"{st['write_by'] or 'another session'}. Write it again?")
            else:
                out.update(ok=True, confirm=False, message="")
            return self._send(200, out)

        if path == "/api/queue/analyzing":
            return self._send(200, {"seqs": [
                r["seq"] for r in queue_items()
                if r["analysis_wanted"] and not r["analysis"]]})

        if path == "/api/queue":
            return self._send(200, {"queue": queue_items()})

        if path == "/api/jobs":
            with JOBS_LOCK:
                rows = sorted(JOBS.values(), key=lambda j: j["created"], reverse=True)
            return self._send(200, {"jobs": [
                {k: j.get(k) for k in
                 ("id", "guide", "person", "status", "note", "created", "title", "images",
                  "url", "boost", "when", "done", "awaiting_github", "source", "dropped",
                  "guide_mode", "person_mode")}
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
        if path == "/api/jobs/screening":
            with JOBS_LOCK:
                ids = [j["id"] for j in JOBS.values() if j.get("screening_pending")]
            return self._send(200, {"ids": ids})

        if path == "/api/jobs/answered":
            with JOBS_LOCK:
                ids = [j["id"] for j in JOBS.values() if j["status"] == "revising"]
            return self._send(200, {"ids": ids})
        if path == "/api/jobs/github_released":
            # Jobs whose github gate has cleared and which still need a draft.
            # The writer's monitor polls this: without it a cleared gate was
            # silent and nothing resumed.
            with JOBS_LOCK:
                ids = [j["id"] for j in JOBS.values()
                       if j.get("github_replied")
                       and not j.get("awaiting_github")
                       and not j.get("github_resumed")
                       and j.get("status") in ("queued", "working")]
            return self._send(200, {"ids": ids})

        if path == "/api/jobs/translating":
            with JOBS_LOCK:
                ids = [j["id"] for j in JOBS.values()
                       if j.get("translate_wanted") and not j.get("translation")]
            return self._send(200, {"ids": ids})
        if path == "/api/jobs/queued":
            with JOBS_LOCK:
                ids = [j["id"] for j in JOBS.values() if j["status"] == "queued"]
            return self._send(200, {"ids": ids})
        if path == "/api/jobs/next":
            # Whoever asks gets the oldest queued job. Fine when one session
            # writes; a race once two do, because neither can say which job it
            # means and each can take the other's. Prefer the addressed claim
            # below, POST /api/job/<id>/claim, whenever the id is known.
            with JOBS_LOCK:
                pending = sorted(
                    (j for j in JOBS.values() if j["status"] == "queued"),
                    key=lambda j: j["created"],
                )
                if not pending:
                    return self._send(200, {"job": None})
                job = pending[0]
                job["status"] = "working"
                job["claimed_by"] = str(data.get("by") or "").strip()[:40] if isinstance(data, dict) else ""
                job["writing_by"] = who_wrote(job["claimed_by"]) or job.get("initiator") or "user"
                job["note"] = f"writing by {job['writing_by']}"
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
                        #
                        # It is also the clearest sign a write went wrong: the
                        # writer came back for this job and had nothing. Marked
                        # here rather than sent here, because a Telegram round
                        # trip must never happen while JOBS_LOCK is held; the
                        # watcher reads the mark on its next tick and sends it
                        # from outside the lock, within 30 seconds.
                        job["write_error"] = "the writer returned no proposal text"
                        save_job(job)
                        return self._send(400, {
                            "error": "no proposal in the result: send the text in "
                                     "'proposal', or POST /note and /questions instead",
                            "status": job["status"]})
                    job["proposal"] = text
                    job["status"] = "done"
                    # On progress -> written, and by whom. Falls back through
                    # the claim and then the initiator, so a result posted
                    # without a claim still attributes correctly.
                    job["written_by"] = (who_wrote(data.get("by"))
                                         or job.get("writing_by")
                                         or job.get("initiator") or "user")
                    job["writing_by"] = ""
                    # A retry that works clears the failure, so a job that came
                    # back empty once and was then written does not keep a mark
                    # saying it failed.
                    job.pop("write_error", None)
                    # The writer can say outright that this was a refusal rather
                    # than a proposal. Cheaper and surer than inferring it from
                    # the queue row, which only carries a job id once the row has
                    # been pressed into a job.
                    if data.get("dropped"):
                        job["dropped"] = True
                    written = queue_mark_written(job["id"])
                    if written is not None:
                        print(f"  queue seq {written} written, row kept for a rerun",
                              flush=True)
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
            # The person's turn is over, so the writer may pick up again. Keyed
            # on the job id, so an unrelated job finishing does not free it.
            writer_resume_after_user(m.group(1))
            if finished is not None:
                if finished.get("dropped") or job_was_dropped(finished["id"]):
                    print(f"  telegram skipped: job {finished['id']} was dropped, "
                          "not a finished proposal", flush=True)
                else:
                    telegram_proposal_done(finished)
            return self._send(200, {"ok": True})

        m = re.fullmatch(r"/api/job/([0-9a-f]{8})/await_github", path)
        if m:
            with JOBS_LOCK:
                job = JOBS.get(m.group(1))
                if not job:
                    return self._send(404, {"error": "no such job"})
                job["awaiting_github"] = True
                job["github_replied"] = False
                job["github_resumed"] = False
                # The links travel with the arming so the UI can show what is
                # being waited on, rather than an unexplained pause.
                repos = data.get("repos")
                if isinstance(repos, list):
                    job["github_refs"] = [
                        {"url": str(r.get("url") or "")[:400],
                         "why": str(r.get("why") or "")[:600]}
                        for r in repos if isinstance(r, dict) and r.get("url")
                    ]
                job["note"] = "waiting for a reply on the github channel"
                save_job(job)
            print(f"  job {job['id']} is waiting on the github channel", flush=True)
            return self._send(200, {"ok": True, "awaiting_github": True})

        m = re.fullmatch(r"/api/job/([0-9a-f]{8})/github_ack", path)
        if m:
            with JOBS_LOCK:
                job = JOBS.get(m.group(1))
                if not job:
                    return self._send(404, {"error": "no such job"})
                job["github_resumed"] = True
                save_job(job)
            return self._send(200, {"ok": True})

        m = re.fullmatch(r"/api/job/([0-9a-f]{8})/resume_github", path)
        if m:
            with JOBS_LOCK:
                job = JOBS.get(m.group(1))
                if not job:
                    return self._send(404, {"error": "no such job"})
                if not github_gate_open(job):
                    return self._send(200, {"ok": True, "note": "was not waiting"})
                clear_github_gate(job, "released by hand")
            return self._send(200, {"ok": True, "released": True})

        if path == "/api/register":
            url = str(data.get("url") or "").strip()
            if not url.lower().startswith(("http://", "https://")):
                return self._send(400, {"error": "a http or https URL is required"})
            t = new_thread("registration", f"Register with {url}",
                           channel="registration", sender="", text="")
            with THREADS_LOCK:
                t["url"] = url
                save_thread(t)
            ident = load_identity()
            ident["url"] = url
            save_identity(ident)
            thread_say(t, "claude",
                       f"Registration request sent to {url}\nname: {project_name()}")
            try:
                reply = send_registration(url, t)
            except Exception as exc:
                thread_say(t, "server", f"Could not reach the server: {exc}")
                return self._send(200, {"ok": True, "id": t["id"], "status": "waiting",
                                        "error": str(exc)})
            got = reply.get("id") or reply.get("assigned_id")
            if got:
                approve_registration(t, got, str(reply.get("note") or ""))
            else:
                thread_say(t, "server",
                           "Received, waiting for approval.\n" + json.dumps(reply)[:400])
            return self._send(200, {"ok": True, "id": t["id"],
                                    "status": t.get("status"), "reply": reply})

        m = re.fullmatch(r"/api/thread/([0-9a-f]{8})/retry", path)
        if m:
            with THREADS_LOCK:
                t = THREADS.get(m.group(1))
            if not t:
                return self._send(404, {"error": "no such thread"})
            if t["kind"] != "registration":
                return self._send(400, {"error": "only a registration can be retried"})
            url = t.get("url") or load_identity().get("url") or ""
            if not url:
                return self._send(400, {"error": "this registration has no URL"})
            thread_say(t, "claude", f"Asking again: {url}")
            try:
                reply = send_registration(url, t)
            except Exception as exc:
                thread_say(t, "server", f"Could not reach the server: {exc}")
                return self._send(200, {"ok": True, "status": "waiting", "error": str(exc)})
            got = reply.get("id") or reply.get("assigned_id")
            if got:
                approve_registration(t, got, str(reply.get("note") or ""))
            else:
                thread_say(t, "server",
                           "Still waiting for approval.\n" + json.dumps(reply)[:400])
            return self._send(200, {"ok": True, "status": t.get("status"), "reply": reply})

        if path == "/api/registration/callback":
            # The server calls this when it approves, out of band.
            got = data.get("id") or data.get("assigned_id")
            if not got:
                return self._send(400, {"error": "id is required"})
            tid = str(data.get("thread") or "")
            with THREADS_LOCK:
                t = THREADS.get(tid) or next(
                    (x for x in THREADS.values()
                     if x["kind"] == "registration" and x.get("status") == "waiting"), None)
            approve_registration(t, got, str(data.get("note") or ""))
            return self._send(200, {"ok": True, "id": str(got)})

        if path == "/api/thread":
            title = str(data.get("title") or "").strip()
            if not title:
                return self._send(400, {"error": "title is required"})
            t = new_thread(str(data.get("kind") or "request"), title,
                           channel=str(data.get("channel") or ""),
                           sender=str(data.get("sender") or ""),
                           text=str(data.get("text") or ""),
                           role=str(data.get("role") or "claude"))
            return self._send(200, {"ok": True, "id": t["id"], "thread": t})

        m = re.fullmatch(r"/api/thread/([0-9a-f]{8})/message", path)
        if m:
            with THREADS_LOCK:
                t = THREADS.get(m.group(1))
            if not t:
                return self._send(404, {"error": "no such thread"})
            if t["completed"]:
                return self._send(409, {"error": "this thread is completed"})
            text = str(data.get("text") or "").strip()
            if not text:
                return self._send(400, {"error": "empty message"})
            msg = thread_say(t, str(data.get("role") or "user"), text)
            return self._send(200, {"ok": True, "message": msg})

        m = re.fullmatch(r"/api/thread/([0-9a-f]{8})/complete", path)
        if m:
            with THREADS_LOCK:
                t = THREADS.get(m.group(1))
                if not t:
                    return self._send(404, {"error": "no such thread"})
                done = data.get("completed")
                t["completed"] = True if done is None else bool(done)
                t["completed_at"] = time.time() if t["completed"] else None
                t["updated"] = time.time()
                save_thread(t)
            return self._send(200, {"ok": True, "completed": t["completed"]})

        m = re.fullmatch(r"/api/thread/([0-9a-f]{8})/delete", path)
        if m:
            with THREADS_LOCK:
                t = THREADS.pop(m.group(1), None)
            f = THREADS_DIR / f"{m.group(1)}.json"
            if f.is_file():
                f.unlink()
            return self._send(200, {"ok": True, "deleted": bool(t)})

        if path == "/api/relay/publish":
            channel = str(data.get("channel") or "").strip()
            if not channel:
                return self._send(400, {"error": "channel is required"})
            if "body" not in data:
                return self._send(400, {"error": "body is required"})
            try:
                out = relay_publish(channel, data["body"])
            except Exception as exc:
                return self._send(502, {"error": str(exc)})
            return self._send(200, {"ok": True, **out})

        m = re.fullmatch(r"/api/worker/(bringer|analyzer|writer)/"
                         r"(start|pause|resume|stop|heartbeat|error)", path)
        if m:
            role, action = m.group(1), m.group(2)
            if action == "heartbeat":
                # A session saying it is alive and what it is on. Returns what
                # it is allowed to do, so one call both reports and asks.
                #
                # `ack` is the session saying which command it has seen. Send
                # back the `command_seq` from the previous reply and the panel
                # can say the order was heard; omit it and the panel says it is
                # still outstanding, which is the honest reading.
                fields = {"last_seen": time.time(),
                          "current": str(data.get("current") or "")[:160]}
                if "note" in data:
                    fields["note"] = str(data.get("note"))[:200]
                if data.get("ack") is not None:
                    try:
                        fields["acked_seq"] = int(data["ack"])
                        fields["acked_at"] = time.time()
                    except (TypeError, ValueError):
                        pass
                worker_set(role, **fields)
                w = worker_get(role)
                return self._send(200, {
                    "ok": True, "status": worker_status(role),
                    # Echo these back so a session can tell a command was
                    # issued even when the state it landed on is unchanged.
                    "command_seq": w.get("command_seq", 0),
                    "last_command": w.get("last_command", ""),
                    **worker_may_run(role)})
            if action == "error":
                out = worker_raise_error(role, data.get("error") or "unspecified",
                                         data.get("current") or "")
                return self._send(200, {"ok": True, "worker": out,
                                        "status": worker_status(role)})
            state = {"start": "running", "resume": "running",
                     "pause": "paused", "stop": "idle"}[action]
            before = worker_get(role)
            fields = {"state": state, "note": f"{action} pressed",
                      "command_seq": int(before.get("command_seq") or 0) + 1,
                      "last_command": action, "command_at": time.time()}
            if state != "running":
                fields["current"] = ""
            if action in ("start", "resume"):
                # Starting clears a yield and clears an error: the person is
                # explicitly asking for it back, having presumably looked. It
                # also clears `current`, since a worker being started is not
                # part-way through whatever it was last doing.
                fields["yielded_to"] = ""
                fields["error"] = ""
                fields["current"] = ""
            out = worker_set(role, **fields)
            print(f"  worker {role}: {action} -> {state}", flush=True)
            return self._send(200, {"ok": True, "worker": out,
                                    "status": worker_status(role),
                                    "may_run": worker_may_run(role)["run"]})

        if path == "/api/relay/enrol":
            # Restores what went with proposal_bridge.py. Enrolment only: it
            # reads the worker id and token out of .env, hands them to the
            # relay, and can do nothing else. Safe to call when already
            # enrolled, which answers "already".
            try:
                out = relay_enrol(str(data.get("label") or ""))
            except RuntimeError as exc:
                return self._send(502, {"error": str(exc)})
            except Exception as exc:
                return self._send(502, {"error": f"could not reach the relay: {exc}"})
            print(f"  relay enrol: {out['status']} as {out['worker_id']}", flush=True)
            return self._send(200, {"ok": True, **out})

        if path == "/api/queue/paste":
            # The only other way a job description gets in. /api/generate takes
            # a queue seq and nothing else, so a hand-pasted post is made into
            # a row here first and then generated from it like a relay job.
            # One door for every job: the row is what carries the link, the
            # title and the client through to the proposal and the archive.
            text = str(data.get("jd") or "").strip()
            if not text:
                return self._send(400, {"error": "paste a job description first"})
            seq = next_pasted_seq()
            item = {
                "seq": seq,
                "channel": "pasted",
                "sender": "pasted by hand",
                "ts": time.time(),
                "body": {
                    # Marked so queue_jd hands the text back untouched.
                    "pasted": True,
                    "title": str(data.get("title") or "").strip() or derive_title(text),
                    "description": text,
                    "upworkUrl": str(data.get("url") or "").strip(),
                    "source": "pasted",
                },
                "client_name": _client_name(data.get("client")),
                # Recorded on the job too. Only "search" is ever written
                # automatically, so this is inert as a trigger and useful as a
                # label: the archive says the post was pasted, not fed in.
                "source": "pasted",
                "used": False,
                # Only the general vollna search is analysed, per
                # analyzer-rule.md. A person pasting a post has already judged it.
                "analysis_wanted": False,
                "analysis": "",
            }
            queue_save(item)
            print(f"  pasted job queued as seq {seq}: "
                  f"{item['body']['title'][:46]!r}", flush=True)
            return self._send(200, {"ok": True, "seq": seq})

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

        m = re.fullmatch(r"/api/queue/(\d+)/analysis", path)
        if m:
            item = queue_get(m.group(1))
            if not item:
                return self._send(404, {"error": "no such queue item"})
            item["analysis"] = str(data.get("analysis") or "").strip()
            item["analysis_wanted"] = False
            item["analysed_at"] = time.time()
            # The client's name can ride along, so the analyser does not need a
            # second round trip to /meta for it. Speed is the point: triage runs
            # on the fastest model and every avoidable HTTP hop is latency on a
            # step that happens forty times a day. Absent means unchanged, so
            # posting an analysis never wipes a name typed in by hand.
            if "client_name" in data:
                item["client_name"] = _client_name(data.get("client_name"))[:80]
            # Work finished: the floor is free for the next row.
            item.pop("analysing_since", None)
            # The marks from step 1 of analyzer-rule.md. An empty list means no
            # engineer here can do the work, which is what dropped means: the
            # row is then deleted outright, since nothing here can do the work
            # and it is not waiting on anybody. That makes the drop final: no
            # redo can reverse it and the analysis text goes with the file, and
            # nothing is sent to Telegram for it.
            if "stack" in data:
                item["stack"] = [s for s in (str(x).strip() for x in (data.get("stack") or []))
                                 if s in STACK_MARKS]
                item["dropped"] = stack_is_dropped(item["stack"])
                # The marks decide the person, so it is settled here rather
                # than being judged again when the job is created. A dropped
                # row resolves to "" because it is never written.
                item["person"] = person_for_stack(item["stack"])
            # Hungry hears about it here, and this is the only place that
            # sends job info. No lock is held in this handler — the queue is
            # files, not JOBS — so the send is made directly rather than
            # deferred, and telegram never raises.
            tell = queue_should_tell_hungry(item)
            if tell:
                item["notified_jobs"] = True
            if item.get("dropped"):
                # Gone, not hidden. Nothing here can do the work, so the row has
                # no further use and does not stay on disk. The trade is that
                # the drop cannot be reversed with a redo and the reasoning goes
                # with it: a wrong call means the post has to arrive again.
                queue_delete(item["seq"])
                print(f"  seq {item['seq']} dropped and removed from the queue", flush=True)
                return self._send(200, {"ok": True, "stack": [], "dropped": True,
                                        "removed": True, "announced": False})
            queue_save(item)
            if tell:
                telegram_job_analysed(item)
                print(f"  hungry told about seq {item['seq']}: "
                      f"stack={item.get('stack')}", flush=True)
            return self._send(200, {"ok": True, "stack": item.get("stack"),
                                    "dropped": bool(item.get("dropped")),
                                    "announced": bool(tell)})

        m = re.fullmatch(r"/api/queue/(\d+)/claim", path)
        if m:
            item = queue_get(m.group(1))
            if not item:
                return self._send(404, {"error": "no such queue item"})
            if item.get("analysis"):
                return self._send(409, {"error": "already analysed",
                                        "analysis": item["analysis"]})
            # Only another *analysis* blocks this. A proposal being written
            # no longer does: the analyzer and a writer are different jobs in
            # different sessions and have no reason to wait for each other.
            busy = work_in_flight("analysis")
            if busy and busy.get("seq") != item["seq"]:
                # The whole point of the claim: the next piece of work does not
                # start until this one is done.
                return self._send(409, {"error": "something else is in flight; "
                                                 "finish it before starting this",
                                        "work": busy})
            item["analysing_since"] = time.time()
            queue_save(item)
            print(f"  seq {item['seq']} claimed for analysis", flush=True)
            return self._send(200, {"ok": True, "seq": item["seq"],
                                    "analysing_since": item["analysing_since"]})

        m = re.fullmatch(r"/api/queue/(\d+)/release", path)
        if m:
            # Let go without having analysed it, so an abandoned claim does not
            # block every later piece of work.
            item = queue_get(m.group(1))
            if not item:
                return self._send(404, {"error": "no such queue item"})
            item.pop("analysing_since", None)
            queue_save(item)
            print(f"  seq {item['seq']} released", flush=True)
            return self._send(200, {"ok": True, "seq": item["seq"]})

        m = re.fullmatch(r"/api/queue/(\d+)/analyze", path)
        if m:
            item = queue_get(m.group(1))
            if not item:
                return self._send(404, {"error": "no such queue item"})
            item["analysis_wanted"] = True
            if data.get("redo"):
                item["analysis"] = ""
                # Asking for it again means the verdict may change, and a row
                # that was dropped and is now workable is worth hearing about.
                item.pop("notified_jobs", None)
            item.pop("analysing_since", None)
            queue_save(item)
            return self._send(200, {"ok": True, "seq": item["seq"]})

        m = re.fullmatch(r"/api/queue/(\d+)/delete", path)
        if m:
            f = QUEUE_DIR / f"{int(m.group(1)):06d}.json"
            existed = f.is_file()
            if existed:
                f.unlink()
            return self._send(200, {"ok": True, "deleted": existed})

        if path == "/api/queue/clear":
            # Empty the queue in one call. Refresh only ever *pulls* from the
            # relay, so before this the only way to clear a backlog was to
            # delete rows one at a time: 51 of them went that way by hand on
            # 2026-10-13, which is what prompted the button.
            #
            # Dropped rows are taken too. They are hidden from the list rather
            # than deleted on arrival, so a clear is the thing that actually
            # reclaims them.
            removed = 0
            if QUEUE_DIR.is_dir():
                for f in sorted(QUEUE_DIR.glob("*.json")):
                    try:
                        f.unlink()
                        removed += 1
                    except OSError:
                        pass
            print(f"  queue cleared: {removed} row(s) removed", flush=True)
            return self._send(200, {"ok": True, "removed": removed,
                                    "queue": queue_items()})

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

        # Screening questions remembered too late. The client's questions are
        # read before the cover letter, so a job written without them is only
        # half delivered, and the old fix was rerunning the whole post. This
        # asks for the answers alone: the proposal, the guide and the open
        # questions are left exactly as they were.
        m = re.fullmatch(r"/api/job/([0-9a-f]{8})/screening_request", path)
        if m:
            with JOBS_LOCK:
                job = JOBS.get(m.group(1))
                if not job:
                    return self._send(404, {"error": "no such job"})
                text = str(data.get("screening") or "").strip()
                if not text:
                    return self._send(400, {"error": "no screening questions given"})
                asked = [l for l in text.splitlines() if l.strip()]
                job["screening"] = text
                job["screening_pending"] = True
                job["note"] = (f"answering {len(asked)} screening question"
                               f"{'' if len(asked) == 1 else 's'}, proposal untouched")
                save_job(job)
                print(f"  job {job['id']} wants {len(asked)} screening answers "
                      f"(proposal stays as written)", flush=True)
            writer_yield_to_user("screening answers", m.group(1))
            return self._send(200, {"ok": True, "questions": len(asked)})

        m = re.fullmatch(r"/api/job/([0-9a-f]{8})/screening_answers", path)
        if m:
            writer_resume_after_user(m.group(1))
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
                job["screening_pending"] = False
                save_job(job)
            return self._send(200, {"ok": True, "count": len(job["screening_answers"])})

        m = re.fullmatch(r"/api/job/([0-9a-f]{8})/translate", path)
        if m:
            with JOBS_LOCK:
                job = JOBS.get(m.group(1))
                if not job:
                    return self._send(404, {"error": "no such job"})
                lang = job.get("language")
                # The page sends what is on screen, so edits made since the
                # draft landed are what gets translated. Falling back to the
                # stored proposal keeps the endpoint usable from curl.
                body = str(data.get("english") or "").strip() or job.get("proposal", "")
                if not lang:
                    return self._send(400, {"error": "no translatable country on this job"})
                if not body.strip():
                    return self._send(400, {"error": "no proposal to translate yet"})
                # A stored translation is only valid for the English that made
                # it. Once that changes the cache is stale and must be redone.
                if job.get("translation") and job.get("translation_source", "") != body:
                    job["translation"] = ""
                if body != job.get("proposal", ""):
                    job["proposal"] = body        # keep the edited version as the letter
                job["translation_source"] = body
                if job.get("translation"):
                    return self._send(200, {"ok": True, "ready": True,
                                            "translation": job["translation"],
                                            "language": lang})
                job["translate_wanted"] = True
                job["note"] = f"translating into {lang}"
                save_job(job)
            if os.environ.get("ANTHROPIC_API_KEY"):
                try:
                    out = call_anthropic(
                        f"Translate the Upwork proposal below into {lang}, as a native "
                        f"speaker would write it to a client in {job.get('country')}. Keep "
                        "every markdown bold marker, every line break, every URL and the "
                        "sign-off name exactly as they are. Translate nothing inside a URL. "
                        "Return only the translation.",
                        body)
                except Exception as exc:
                    return self._send(502, {"error": str(exc)})
                with JOBS_LOCK:
                    job["translation"] = out.strip()
                    job["translation_source"] = body
                    job["translate_wanted"] = False
                    job["note"] = f"translated into {lang}"
                    save_job(job)
                return self._send(200, {"ok": True, "ready": True,
                                        "translation": job["translation"], "language": lang})
            # Bridge mode: the Claude Code session writes it, same as the proposal.
            return self._send(202, {"ok": True, "ready": False, "language": lang})

        m = re.fullmatch(r"/api/job/([0-9a-f]{8})/translation", path)
        if m:
            with JOBS_LOCK:
                job = JOBS.get(m.group(1))
                if not job:
                    return self._send(404, {"error": "no such job"})
                job["translation"] = str(data.get("translation") or "").strip()
                job["translation_source"] = job.get("proposal", "")
                job["translate_wanted"] = False
                job["note"] = f"translated into {job.get('language') or 'the local language'}"
                save_job(job)
            return self._send(200, {"ok": True})

        m = re.fullmatch(r"/api/job/([0-9a-f]{8})/guide", path)
        if m:
            # The writer decides the guide from the job description, per
            # decision-maker.md, so the dropdown is only ever a default. Stored
            # back here so the UI and the archived copy name the guide that
            # actually wrote the letter.
            want = str(data.get("guide") or "").strip()
            if want not in {g["id"] for g in list_guides()}:
                return self._send(400, {"error": f"no guide named {want!r}"})
            with JOBS_LOCK:
                job = JOBS.get(m.group(1))
                if not job:
                    return self._send(404, {"error": "no such job"})
                if job.get("guide_mode") == "manual":
                    return self._send(409, {
                        "error": "this job's guide was chosen by hand; auto mode off",
                        "guide": job.get("guide")})
                was = job.get("guide")
                job["guide"] = want
                save_job(job)
            return self._send(200, {"ok": True, "guide": want, "was": was})

        m = re.fullmatch(r"/api/job/([0-9a-f]{8})/person", path)
        if m:
            # Same contract as the guide above: in auto the dropdown is only a
            # default and the writer records whoever the post actually suits.
            # This one must be posted *before* the repository search, since
            # Connor's own pool is searched first and Zachary's is not, so the
            # person decides what the search even is.
            want = str(data.get("person") or "").strip()
            if want not in {p["id"] for p in list_people()}:
                return self._send(400, {"error": f"no person named {want!r}"})
            with JOBS_LOCK:
                job = JOBS.get(m.group(1))
                if not job:
                    return self._send(404, {"error": "no such job"})
                if job.get("person_mode") == "manual":
                    return self._send(409, {
                        "error": "this job's person was chosen by hand; auto mode off",
                        "person": job.get("person")})
                was = job.get("person")
                job["person"] = want
                save_job(job)
            return self._send(200, {"ok": True, "person": want, "was": was})

        m = re.fullmatch(r"/api/job/([0-9a-f]{8})/notes_reply", path)
        if m:
            with JOBS_LOCK:
                job = JOBS.get(m.group(1))
                if not job:
                    return self._send(404, {"error": "no such job"})
                job["notes_reply"] = str(data.get("reply") or "")
                save_job(job)
            return self._send(200, {"ok": True})

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

                # The panel is not the only thing that can change before a
                # rewrite. Screening questions pasted in at the last moment, or
                # an edited job description, used to be dropped on the floor
                # because this endpoint only ever read the answers.
                changed = []
                if "screening" in data:
                    new_scr = str(data.get("screening") or "").strip()
                    if new_scr != (job.get("screening") or ""):
                        job["screening"] = new_scr
                        changed.append("screening questions")
                if "notes" in data:
                    new_notes = str(data.get("notes") or "").strip()
                    if new_notes != (job.get("notes") or ""):
                        job["notes"] = new_notes
                        changed.append("notes from the user")
                for field in ("jd", "url"):
                    if field in data:
                        val = str(data.get(field) or "").strip()
                        if val and val != (job.get(field) or ""):
                            job[field] = val
                            changed.append("job description" if field == "jd" else "url")

                job["status"] = "revising"
                job["status_was_revising"] = True
                job["note"] = "answers submitted, writing the final version"
                if changed:
                    job["note"] += " (also updated: " + ", ".join(changed) + ")"
                    print(f"  job {job['id']} rewrite carries new {', '.join(changed)}",
                          flush=True)
                # A rewrite is a new version, so it gets its own alarm. The
                # per-version reset keeps two sessions posting the SAME version
                # from double-firing, which is what the flag was added for.
                job["notified_done"] = False
                save_job(job)
            # Outside the lock, like every other side effect here.
            writer_yield_to_user("rewrite", m.group(1))
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

        m = re.fullmatch(r"/api/job/([0-9a-f]{8})/claim", path)
        if m:
            # Take one named job. Two sessions writing at once need this: the
            # oldest-queued claim cannot express "the job I was asked for", so
            # each could take the other's work. Refused if somebody already
            # holds it, which is what makes the two safe to run side by side.
            with JOBS_LOCK:
                job = JOBS.get(m.group(1))
                if not job:
                    return self._send(404, {"error": "no such job"})
                if job["status"] in ("working", "revising"):
                    return self._send(409, {
                        "error": "already claimed",
                        "status": job["status"],
                        "claimed_by": job.get("claimed_by", "")})
                if job["status"] == "done":
                    return self._send(409, {"error": "already written",
                                            "status": "done"})
                job["status"] = "working"
                job["claimed_by"] = str(data.get("by") or "").strip()[:40]
                # Fall back to who asked for the job when the claim did not say.
                job["writing_by"] = who_wrote(data.get("by")) or job.get("initiator") or "user"
                job["note"] = f"writing by {job['writing_by']}"
                save_job(job)
            print(f"  job {job['id']} claimed by {job.get('claimed_by') or 'an unnamed session'}",
                  flush=True)
            return self._send(200, {"ok": True, "job": job})

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
        # Who pressed it. The UI sends nothing and so counts as the person; the
        # writer session sends initiator "worker" for jobs it creates itself,
        # which must not make it stand down for its own work.
        by_user = str(data.get("initiator") or "user").lower() != "worker"

        # Every job comes off a queue row, and there is no other way in. A row
        # carries the posting, the Upwork link, the real title and the client
        # name as fields, so the job gets all four; the raw-jd shape this used
        # to accept carried only prose, which is how a job with no URL was
        # created for every message that crossed the relay. A pasted
        # description is queued first, by /api/queue/paste, and arrives here as
        # a seq like any other. Removed 2026-10-13 with proposal_bridge.py.
        queued = None
        if data.get("queue_seq") in (None, ""):
            return self._send(400, {
                "error": "a job is created from a queue row: send queue_seq. "
                         "Paste one in with POST /api/queue/paste, which returns its seq",
                "hint": "raw 'jd' is no longer accepted"})
        queued = queue_get(data["queue_seq"])
        if not queued:
            return self._send(404, {"error": f"queue item {data['queue_seq']} is gone"})
        jd = queue_jd(queued)
        data = dict(data)
        # An analysed row already decided the person from its stack marks, per
        # analyzer-rule.md. In auto that decision wins over the dropdown, which
        # is only ever a default; in manual the user's pick stands untouched.
        if (data.get("person_mode") or "auto") != "manual" and queued.get("person"):
            person_id = queued["person"]
        data["url"] = (queued.get("body", {}).get("upworkUrl")
                       or queued.get("body", {}).get("url") or "")
        data["client"] = queued.get("client_name", "")
        data["title"] = (queued.get("body", {}).get("title") or "").strip()
        # The client's own screening questions, when the feed sent them with
        # the post. They reach the job exactly as typed-in ones do, so the
        # writer answers them and they are archived with the letter. A person
        # ticking the box and typing their own still wins: this only fills the
        # field when the request left it empty.
        if not str(data.get("screening") or "").strip():
            row_scr = (queued.get("screening")
                       or body_screening(queued.get("body") or {}))
            if row_scr:
                data["screening"] = row_scr
                print(f"  seq {queued['seq']} carries "
                      f"{len(row_scr.splitlines())} screening question(s) from the feed",
                      flush=True)

        if path in ("/api/prompt", "/api/generate"):
            if not jd.strip():
                return self._send(400, {"error": "that queue row has no job description in it"})
            try:
                system, user = build_prompt(guide_id, person_id, jd, data.get("client") or "",
                                            data.get("screening") or "",
                                            data.get("notes") or "")
            except FileNotFoundError as exc:
                return self._send(400, {"error": str(exc)})

            if path == "/api/prompt":
                return self._send(200, {"prompt": f"{system}\n\n{user}"})

            if not os.environ.get("ANTHROPIC_API_KEY"):
                job = new_job(guide_id, person_id, jd, data.get("client") or "",
                              data.get("screening") or "", data.get("url") or "",
                              data.get("title") or "", data.get("notes") or "",
                              data.get("guide_mode") or "auto",
                              data.get("country") or "",
                              data.get("person_mode") or "auto",
                              data.get("initiator") or "user")
                if by_user:
                    writer_yield_to_user("proposal", job["id"])
                if queued:
                    queued["used"] = True
                    queued["job_id"] = job["id"]
                    queue_save(queued)
                    # Carry the feed forward onto the job. Only a row from the
                    # general vollna search is analysed, and only such a job may
                    # be dropped rather than written: an alert or a hand-typed
                    # job is the person asking for a proposal, so it gets one.
                    # Without this the job has no memory of which feed it came
                    # from and that distinction cannot be made after the fact.
                    job["source"] = queued.get("source") or ""
                    job["queue_seq"] = queued.get("seq")
                    job["sender"] = queued.get("sender") or ""
                    save_job(job)
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
    load_threads()
    purge_old_jobs()          # catch up if the server was down at the boundary
    threading.Thread(target=purge_loop, daemon=True).start()
    load_workers()
    print("  workers: " + ", ".join(f"{r}={worker_get(r)['state']}"
                                    for r in WORKER_ROLES), flush=True)
    relay_seed_channels()
    threading.Thread(target=pull_loop, daemon=True).start()
    threading.Thread(target=boost_check_loop, daemon=True).start()
    if not (UI / "index.html").is_file():
        sys.exit("ui/index.html is missing")
    # profiles/ is gitignored, so a fresh clone of this repo arrives without it
    # and without anybody in it. Make the folder rather than listing no people
    # and leaving the reason to be guessed at.
    PROFILES.mkdir(exist_ok=True)
    mode = "API mode" if os.environ.get("ANTHROPIC_API_KEY") else "bridge mode (jobs go to Claude Code)"
    print(f"Proposal UI on http://localhost:{PORT}  [{mode}]")
    print(f"  guides: {', '.join(g['id'] for g in list_guides()) or 'none'}", flush=True)
    people = list_people()
    print(f"  people: {', '.join(p['id'] for p in people) or 'none'}", flush=True)
    if not people:
        print("    no profiles yet: put one .md file per person in profiles/, "
              "single-word name, e.g. profiles/Alex.md", flush=True)
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
