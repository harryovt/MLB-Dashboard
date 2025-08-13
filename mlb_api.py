import requests

def get_player_info(name):
    url = f"https://statsapi.mlb.com/api/v1/people/search?names={name}"
    res = requests.get(url).json()
    if not res.get('people'):
        return None
    player = res['people'][0]
    return {
        'id': player['id'],
        'name': player['fullName'],
        'team': player.get('currentTeam', {}).get('name', 'Unknown'),
        'position': player.get('primaryPosition', {}).get('name', 'Unknown')
    }

def get_player_stats(player_id, season='2023'):
    url = f"https://statsapi.mlb.com/api/v1/people/{player_id}/stats?stats=season&season={season}"
    res = requests.get(url).json()
    try:
        return res['stats'][0]['splits'][0]['stat']
    except (IndexError, KeyError):
        return {}
    
import pandas as pd

def clean_stats(stats_dict):
    cleaned = {}
    for k, v in stats_dict.items():
        try:
            if '.' in v:
                cleaned[k] = float(v)
            else:
                cleaned[k] = int(v)
        except (ValueError, TypeError):
            cleaned[k] = v
    return pd.DataFrame(cleaned.items(), columns=["Stat", "Value"])

# Example usage
def main():
    player = get_player_info("Aaron Judge")
    if player:
        stats = get_player_stats(player['id'])
        print(f"{player['name']} ({player['team']} - {player['position']})")
        print(stats)
    else:
        print("Player not found.")

if __name__ == "__main__":
    main()