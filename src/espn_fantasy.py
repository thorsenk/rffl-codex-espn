import requests
import json
import os
import re
from urllib.parse import urlencode
from datetime import datetime

# League and season configuration
LEAGUE_ID = 323196
SEASON_YEAR = 2024

# ESPN API endpoints
BASE_URL = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons"
LEAGUE_ENDPOINT = f"{BASE_URL}/{SEASON_YEAR}/segments/0/leagues/{LEAGUE_ID}"

# Authentication credentials
SWID = os.getenv("SWID", "{C3FCDEE0-434E-498F-9793-E68E81750B9B}")
ESPN_S2 = os.getenv("ESPN_S2", "AEBebWLZzXW%2F%2BPh%2F3tuRf2MJgDaxB%2FH9RfEPqR4sa%2FHjRk6trjdKXhhU0s27pbycQjkBrIb5riFGaiiK9kiKIbtfy04IG4TXVXqElWkvYa8FbgOwSD7dSzOLg8cZKnk7quC6EYfXFZ9L8FQMjZd6Iu2mTwgbf1fWWXxcnVF2U0T5ubojV05mauwFYvKcqeeosDSscg4JGyVA6sgXbCCVOTH5z31321jOYt3KG52i5fYMGI6kGtcyFaA8pjgpfp71N8LfxLW87Y2RmLRAyNv9iUnGYPnsX%2BwRFH%2F4jJ0kKTg%2BLg%3D%3D")

# Position mapping
POSITION_MAP = {
    1: "QB",
    2: "RB",
    3: "WR",
    4: "TE",
    5: "K",
    16: "D/ST"
}

# League roster settings
ROSTER_SETTINGS = {
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

def get_cookies():
    return {
        'SWID': SWID,
        'espn_s2': ESPN_S2
    }

def get_headers():
    return {
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Origin': 'https://fantasy.espn.com',
        'Referer': f'https://fantasy.espn.com/football/league?leagueId={LEAGUE_ID}'
    }

def get_league_info():
    """Get basic league information"""
    print(f"\nFetching league information for League ID: {LEAGUE_ID}, Season: {SEASON_YEAR}")
    
    view_params = {
        'view': [
            'mTeam',
            'mRoster',
            'mMatchup',
            'mSettings',
            'mStandings',
            'mStatus',
            'mScoreboard',
            'mSchedule'
        ]
    }
    
    params = urlencode(view_params, doseq=True)
    url = f"{LEAGUE_ENDPOINT}?{params}"
    
    try:
        response = requests.get(
            url,
            cookies=get_cookies(),
            headers=get_headers()
        )
        
        if response.status_code == 401:
            print("Authentication failed. Please check your SWID and ESPN_S2 tokens.")
            return None
        elif response.status_code == 404:
            print("League not found. Please verify the League ID and Season.")
            return None
        
        response.raise_for_status()
        
        try:
            data = response.json()
            if not data:
                print("Received empty response from ESPN")
                return None
            return data
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching league data: {e}")
        return None

def get_team_name_map(league_data):
    """Create a mapping of team IDs to team names and owners"""
    team_map = {}
    if 'teams' in league_data:
        for team in league_data['teams']:
            team_id = team.get('id')
            
            # Get team name components
            team_name = team.get('name', '').strip()  # Try to get full name first
            if not team_name:  # If no full name, try location + nickname
                location = team.get('location', '').strip()
                nickname = team.get('nickname', '').strip()
                team_name = f"{location} {nickname}".strip()
                if not team_name:  # If still no name, use team abbreviation
                    team_name = team.get('abbrev', 'Team').strip()
            
            # Get owner information
            owner_id = team.get('owners', ['Unknown'])[0]
            owner_name = 'Unknown Owner'
            if 'members' in league_data:
                for member in league_data['members']:
                    if member.get('id') == owner_id:
                        first_name = member.get('firstName', '').strip()
                        last_name = member.get('lastName', '').strip()
                        owner_name = f"{first_name} {last_name}".strip()
                        break
            
            team_map[team_id] = {
                'name': team_name or f"Team {team_id}",  # Fallback if no name found
                'owner': owner_name,
                'owner_id': owner_id,
                'abbrev': team.get('abbrev', ''),
                'location': team.get('location', ''),
                'nickname': team.get('nickname', '')
            }
    return team_map

def get_team_info(league_data):
    """Extract and display team information"""
    if not league_data or 'teams' not in league_data:
        print("No team data available")
        return
    
    team_map = get_team_name_map(league_data)
    
    print("\nTeams in the League:")
    for team_id, team_info in team_map.items():
        record = next((team['record'] for team in league_data['teams'] if team['id'] == team_id), {})
        wins = record.get('overall', {}).get('wins', 0)
        losses = record.get('overall', {}).get('losses', 0)
        ties = record.get('overall', {}).get('ties', 0)
        points_for = record.get('overall', {}).get('pointsFor', 0)
        
        print(f"- {team_info['name']}")
        print(f"  Owner: {team_info['owner']}")
        print(f"  Record: {wins}-{losses}-{ties}")
        print(f"  Points For: {points_for:.2f}")

def get_roster_info(league_data):
    """Extract and display roster information"""
    if not league_data or 'teams' not in league_data:
        print("No roster data available")
        return
    
    team_map = get_team_name_map(league_data)
    print("\nRoster Information:")
    
    for team in league_data['teams']:
        team_info = team_map.get(team.get('id'), {'name': 'Unknown Team', 'owner': 'Unknown Owner'})
        print(f"\n{team_info['name']} ({team_info['owner']}):")
        
        if 'roster' in team:
            entries = team['roster'].get('entries', [])
            organized_roster = organize_roster_by_position(entries)
            starters, bench = suggest_starters(organized_roster)
            
            print("\n  Starting Lineup:")
            for pos, player in starters:
                print(f"    {pos:<5} - {player}")
            
            print("\n  Bench:")
            for pos, player in bench:
                print(f"    {pos:<5} - {player}")
            
            print("\nTotal roster size:", len(entries))

def organize_roster_by_position(players):
    """Organize players by their positions"""
    organized = {
        "QB": [],
        "RB": [],
        "WR": [],
        "TE": [],
        "D/ST": [],
        "K": []
    }
    
    for player in players:
        pos_id = player.get('playerPoolEntry', {}).get('player', {}).get('defaultPositionId')
        if pos_id:
            pos = POSITION_MAP.get(pos_id, "Unknown")
            player_name = player.get('playerPoolEntry', {}).get('player', {}).get('fullName', 'Unknown Player')
            organized[pos].append(player_name)
    
    return organized

def suggest_starters(organized_roster):
    """Suggest starting lineup based on league settings"""
    starters = []
    bench = []
    
    # Copy the organized roster to work with
    available = {pos: list(players) for pos, players in organized_roster.items()}
    
    # Fill required positions first
    for pos_setting in ROSTER_SETTINGS["starters"]:
        pos = pos_setting["position"]
        count = pos_setting["count"]
        
        if pos == "FLEX":
            # Handle FLEX position (RB/WR/TE)
            flex_options = []
            for flex_pos in ["RB", "WR", "TE"]:
                flex_options.extend([(p, flex_pos) for p in available[flex_pos]])
            
            if flex_options:
                player, pos_type = flex_options[0]  # Take first available flex player
                starters.append(("FLEX", player))
                available[pos_type].remove(player)
        else:
            # Handle regular positions
            for _ in range(count):
                if available[pos]:
                    starters.append((pos, available[pos].pop(0)))
    
    # Remaining players go to bench
    for pos, players in available.items():
        for player in players:
            bench.append((pos, player))
    
    return starters, bench

def get_matchup_info(league_data):
    """Get and display matchup information"""
    if 'schedule' not in league_data:
        print("No matchup data available")
        return
    
    team_map = get_team_name_map(league_data)
    current_week = league_data.get('status', {}).get('currentMatchupPeriod', 0)
    print(f"\nMatchup Information (Current Week: {current_week})")
    
    # Group matchups by week
    matchups_by_week = {}
    for game in league_data['schedule']:
        week = game.get('matchupPeriodId', 0)
        if week not in matchups_by_week:
            matchups_by_week[week] = []
        matchups_by_week[week].append(game)
    
    # Display matchups for each week
    for week in sorted(matchups_by_week.keys()):
        print(f"\nWeek {week}:")
        for game in matchups_by_week[week]:
            home_team_id = game.get('home', {}).get('teamId')
            away_team_id = game.get('away', {}).get('teamId')
            
            if home_team_id in team_map and away_team_id in team_map:
                home_team = team_map[home_team_id]
                away_team = team_map[away_team_id]
                
                home_score = game.get('home', {}).get('totalPoints', 0)
                away_score = game.get('away', {}).get('totalPoints', 0)
                
                print(f"  {away_team['name']} ({away_team['owner']}) vs. {home_team['name']} ({home_team['owner']})")
                if week <= current_week:
                    print(f"  Score: {away_score:.2f} - {home_score:.2f}")
                print()

def main():
    print("Using credentials:")
    print(f"SWID: {SWID}")
    print(f"ESPN_S2: {ESPN_S2[:30]}...")  # Only show first 30 chars for security
    
    # Get league data
    league_data = get_league_info()
    
    if league_data:
        # Display team information with records
        get_team_info(league_data)
        
        # Display matchup information
        get_matchup_info(league_data)
        
        # Display roster information
        get_roster_info(league_data)
    else:
        print("Failed to retrieve league data")

if __name__ == "__main__":
    main() 