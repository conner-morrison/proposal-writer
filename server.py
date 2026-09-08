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


def new_job(guide_id, person_id, jd, client="", screening=""):
    job = {
        "id": uuid.uuid4().hex[:8],
        "guide": guide_id,
        "person": person_id,
        "client": client.strip(),
        "jd": jd.strip(),
        "screening": screening.strip(),
        "screening_answers": [],
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


def save_job(job):
    JOBS_DIR.mkdir(exist_ok=True)
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
        if path == "/api/config":
            return self._send(
                200,
                {
                    "guides": list_guides(),
                    "people": list_people(),
                    "mode": "api" if os.environ.get("ANTHROPIC_API_KEY") else "bridge",
                    "model": MODEL,
                },
            )
        if path == "/api/jobs":
            with JOBS_LOCK:
                rows = sorted(JOBS.values(), key=lambda j: j["created"], reverse=True)
            return self._send(200, {"jobs": [
                {k: j[k] for k in ("id", "guide", "person", "status", "note", "created")}
                for j in rows[:20]
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
                    job["proposal"] = data.get("proposal") or ""
                    job["status"] = "done"
                    job["note"] = "written by Claude Code"
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
                              data.get("screening") or "")
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
    if not (UI / "index.html").is_file():
        sys.exit("ui/index.html is missing")
    mode = "API mode" if os.environ.get("ANTHROPIC_API_KEY") else "bridge mode (jobs go to Claude Code)"
    print(f"Proposal UI on http://localhost:{PORT}  [{mode}]")
    print(f"  guides: {', '.join(g['id'] for g in list_guides()) or 'none'}")
    print(f"  people: {', '.join(p['id'] for p in list_people()) or 'none'}")
    print(f"  jobs restored: {len(JOBS)}")
    print("  Ctrl+C to stop")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nstopped")
