"""Reads your last golf round in Garmin Connect and writes golf.json for the Golf S72 Data+ watch face.

Only hole counts are published (eagles, birdies, pars, bogeys, double bogeys or worse): no course, no date
of play, no location. Uses the unofficial python-garminconnect library (Garmin has no public golf API).

Login: GARMIN_EMAIL + GARMIN_PASSWORD secrets. If Garmin sends a code by email or SMS, the run stops and
waits; run the workflow by hand with that code. The renewed login is kept, encrypted with your secrets,
in the Actions cache (.tokens), never committed.
"""
import base64
import hashlib
import json
import os
import sys
from datetime import date
from pathlib import Path

from cryptography.fernet import Fernet, InvalidToken
from garminconnect import Garmin

DIR = Path(".tokens")
TOKENS = DIR / "tokens.bin"
PENDING = DIR / "pending.bin"
OUT = Path("golf.json")

EMAIL = os.environ.get("GARMIN_EMAIL", "").strip()
PASSWORD = os.environ.get("GARMIN_PASSWORD", "")
TOKEN_SECRET = os.environ.get("GARMIN_TOKENS", "").strip()
CODE = os.environ.get("MFA_CODE", "").strip()
MANUAL = os.environ.get("GITHUB_EVENT_NAME") == "workflow_dispatch"

KEY = base64.urlsafe_b64encode(hashlib.sha256((EMAIL + PASSWORD + TOKEN_SECRET).encode()).digest())


def save(path, text):
    DIR.mkdir(exist_ok=True)
    path.write_bytes(Fernet(KEY).encrypt(text.encode()))


def load(path):
    try:
        return Fernet(KEY).decrypt(path.read_bytes()).decode() if path.exists() else ""
    except InvalidToken:
        return ""


def mark(state):
    """Writes the login state in golf.json, readable by anyone: "ok", or "code" while waiting for the Garmin code."""
    data = json.loads(OUT.read_text()) if OUT.exists() else {}
    data["etat"] = state
    OUT.write_text(json.dumps(data) + "
")


def login():
    store = load(TOKENS) or TOKEN_SECRET
    if store:
        g = Garmin()
        g.login(store)
        return g
    if not (EMAIL and PASSWORD):
        sys.exit("Add the GARMIN_EMAIL and GARMIN_PASSWORD secrets: see README, step 3.")
    g = Garmin(EMAIL, PASSWORD, return_on_mfa=True)
    state = load(PENDING)
    if state and CODE:
        g.resume_login(json.loads(state), CODE)
        PENDING.unlink()
        return g
    if state and not MANUAL:
        print("Waiting for the Garmin code: Actions > Update golf ring > Run workflow, type the code.")
        mark("code")
        sys.exit(0)
    status, state = g.login()
    if status == "needs_mfa":
        save(PENDING, json.dumps(state))
        print("Garmin sent you a code by email or SMS. Now: Actions > Update golf ring > Run workflow, "
              "type the code in the box, Run workflow.")
        mark("code")
        sys.exit(0)
    return g


def main():
    g = login()
    summary = g.get_golf_summary(limit=1)
    cards = summary.get("scorecardSummaries") if isinstance(summary, dict) else summary
    old = json.loads(OUT.read_text()) if OUT.exists() else {}
    result = {k: old.get(k, 0) for k in ("trous", "eagle", "birdie", "par", "bogey", "plus")}
    if cards:
        card_id = cards[0].get("id") or cards[0].get("scorecardId")
        detail = g.get_golf_scorecard(card_id)
        stats = {}
        if isinstance(detail, dict) and detail.get("scorecardDetails"):
            stats = (detail["scorecardDetails"][0].get("scorecardStats") or {}).get("round") or {}
        result = {
            "trous": stats.get("holesPlayed", 0),
            "eagle": stats.get("holesEagle", 0) + stats.get("holesDoubleEagleOrUnder", 0),
            "birdie": stats.get("holesBirdie", 0),
            "par": stats.get("holesPar", 0),
            "bogey": stats.get("holesBogey", 0),
            "plus": stats.get("holesOverBogey", 0),
        }
    # one change a day at least, so GitHub keeps the schedule running (it pauses after 60 days without commits)
    result["maj"] = date.today().isoformat()
    result["etat"] = "ok"
    OUT.write_text(json.dumps(result) + "\n")
    print("golf.json:", result)
    save(TOKENS, g.client.dumps())


if __name__ == "__main__":
    main()
