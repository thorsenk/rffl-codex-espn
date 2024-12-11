"""
Utility functions for interacting with the ESPN Fantasy Football API.
Specifically designed for the RFFL (Redneck Fantasy Football League) Codex project.
"""

import requests
from typing import Dict, Any, Optional
from ..config.settings import SWID, ESPN_S2, DEFAULT_HEADERS

def get_cookies() -> Dict[str, str]:
    """Get authentication cookies for ESPN API."""
    return {
        'SWID': SWID,
        'espn_s2': ESPN_S2
    }

def make_api_request(url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Make a request to the ESPN API.
    
    Args:
        url: The API endpoint URL
        params: Optional query parameters
    
    Returns:
        Dict containing the API response
    
    Raises:
        requests.exceptions.RequestException: If the API request fails
    """
    try:
        response = requests.get(
            url,
            params=params,
            cookies=get_cookies(),
            headers=DEFAULT_HEADERS
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        raise

def get_league_data(league_id: int, season: int) -> Dict[str, Any]:
    """
    Get league data for a specific season.
    
    Args:
        league_id: ESPN league ID (RFFL ID: 323196)
        season: Year of the season
    
    Returns:
        Dict containing league data
    """
    url = f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{season}/segments/0/leagues/{league_id}"
    params = {
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
    return make_api_request(url, params)

def get_team_name_map(league_data: Dict[str, Any]) -> Dict[int, Dict[str, str]]:
    """
    Create a mapping of team IDs to team names and owners.
    
    Args:
        league_data: League data from the ESPN API
    
    Returns:
        Dict mapping team IDs to team information
    """
    team_map = {}
    if 'teams' in league_data:
        for team in league_data['teams']:
            team_id = team.get('id')
            
            # Get team name components
            team_name = team.get('name', '').strip()
            if not team_name:
                location = team.get('location', '').strip()
                nickname = team.get('nickname', '').strip()
                team_name = f"{location} {nickname}".strip()
                if not team_name:
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
                'name': team_name or f"Team {team_id}",
                'owner': owner_name,
                'owner_id': owner_id,
                'abbrev': team.get('abbrev', ''),
                'location': team.get('location', ''),
                'nickname': team.get('nickname', '')
            }
    return team_map 