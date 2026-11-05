"""Reads your last golf round in Garmin Connect and writes golf.json for the Golf S72 Data+ watch face.

Only hole counts are published (eagles, birdies, pars, bogeys, double bogeys or worse): no course, no date
of play, no location. Uses the unofficial python-garminconnect library (Garmin has no public golf API).
"""
import json
import os
from datetime import date
from pathlib import Path

from garminconnect import Garmin

TOKENS = Path(".tokens/tokens.json")   # renewed tokens, kept in the private Actions cache, never committed
OUT = Path("golf.json")


def main():
    store = TOKENS.read_text() if TOKENS.exists() else os.environ.get("GARMIN_TOKENS", "").strip()
    if not store:
        raise SystemExit("GARMIN_TOKENS secret is missing: see README, step 3.")
    g = Garmin()
    g.login(store)
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
    OUT.write_text(json.dumps(result) + "\n")
    print("golf.json:", {k: v for k, v in result.items()})
    TOKENS.parent.mkdir(exist_ok=True)
    TOKENS.write_text(g.client.dumps())


if __name__ == "__main__":
    main()
