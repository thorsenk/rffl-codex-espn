"""
Configuration settings for the RFFL Codex ESPN Data Extractor.
"""

import os
from typing import Dict, Any

# League Configuration
LEAGUE_ID = 323196  # RFFL League ID
SEASON_YEAR = 2024  # Current season

# API Configuration
BASE_URL = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons"
LEAGUE_ENDPOINT = f"{BASE_URL}/{SEASON_YEAR}/segments/0/leagues/{LEAGUE_ID}"

# Authentication
SWID = os.getenv("SWID", "{C3FCDEE0-434E-498F-9793-E68E81750B9B}")
ESPN_S2 = os.getenv("ESPN_S2", "AEBebWLZzXW%2F%2BPh%2F3tuRf2MJgDaxB%2FH9RfEPqR4sa%2FHjRk6trjdKXhhU0s27pbycQjkBrIb5riFGaiiK9kiKIbtfy04IG4TXVXqElWkvYa8FbgOwSD7dSzOLg8cZKnk7quC6EYfXFZ9L8FQMjZd6Iu2mTwgbf1fWWXxcnVF2U0T5ubojV05mauwFYvKcqeeosDSscg4JGyVA6sgXbCCVOTH5z31321jOYt3KG52i5fYMGI6kGtcyFaA8pjgpfp71N8LfxLW87Y2RmLRAyNv9iUnGYPnsX%2BwRFH%2F4jJ0kKTg%2BLg%3D%3D")

# Position Mapping
POSITION_MAP: Dict[int, str] = {
    1: "QB",
    2: "RB",
    3: "WR",
    4: "TE",
    5: "K",
    16: "D/ST"
}

# League Settings
ROSTER_SETTINGS: Dict[str, Any] = {
    "starters": [
        {"position": "QB", "count": 1},
        {"position": "RB", "count": 2},
        {"position": "WR", "count": 2},
        {"position": "TE", "count": 1},
        {"position": "FLEX", "count": 1},  # RB/WR/TE
        {"position": "D/ST", "count": 1},
        {"position": "K", "count": 1}
    ],
    "bench_spots": 7,
    "total_roster_size": 16  # 9 starters + 7 bench
}

# API Request Headers
DEFAULT_HEADERS = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
} 