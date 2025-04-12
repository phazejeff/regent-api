import requests
class Faceit:
    def __init__(self, api_key):
        self.api_key = api_key
        # faceit please fix your dogshit api endpoints thanks
        self.api_root = "https://open.faceit.com/data/v4"
        self.api_v1_root = "https://www.faceit.com/api/stats/v1"
        self.api_v1_championships_root = "https://www.faceit.com/api/championships/v1"
        self.game_id = "cs2"

    def _get_header(self):
        return {
            "Authorization": "Bearer " + self.api_key,
            "Accept": "application/json"
        }
    
    def get_player_by_nickname(self, nickname: str):
        r: dict = requests.get(
            f"{self.api_root}/players",
            params={
                "nickname" : nickname,
                "game" : self.game_id
            },
            headers=self._get_header()
        ).json()
        return r
    
    def get_player_stats(self, player_id):
        r: dict = requests.get(
            f"{self.api_root}/players/{player_id}/stats/{self.game_id}",
            params={"limit" : 20},
            headers=self._get_header()
        ).json()
        return r

    def get_championship_matches(self, championship_id, type="past", amount=20, offset=0):
        r: dict = requests.get(
            f"{self.api_root}/championships/{championship_id}/matches?type={type}&limit={amount}&offset={offset}", 
            headers=self._get_header()
        ).json()
        items = r.get('items')
        matches = []
        for match in items:
            if match.get("status") == "CANCELLED":
                continue
            matches.append(match)
        return matches
    
    def get_match_ids_from_championship_group(self, championship_id, group, offset, limit):
        r: dict = requests.get(f"https://www.faceit.com/api/match/v3/match?entityId={championship_id}&entityType=championship&group={group}&offset={offset}&limit={limit}").json()
        match_ids = []
        for i in r.get('payload'):
            i: dict
            match_ids.append(i.get('id'))

        return match_ids
    
    def get_match_stats(self, match_id):
        return requests.get(
            f"{self.api_root}/matches/{match_id}/stats", 
            headers=self._get_header()
        ).json()
    
    def get_all_groups(self, championship_id):
        r: dict = requests.get(
            f"{self.api_root}/leaderboards/championships/{championship_id}",
            headers=self._get_header()
        ).json()

        groups = []
        for item in r.get("items"):
            item: dict
            groups.append(item.get("group"))
        return groups
    
    def get_rankings(self, championship_id, group=None):
        url = f"{self.api_root}/leaderboards/championships/{championship_id}"
        if group:
            url = url + f"/groups/{group}"
        r: dict = requests.get(
            url,
            headers=self._get_header()    
        ).json()
        items: list[dict] = r.get('items')
        return items
    
    def get_playoff_rankings(self, championship_id):
        r: dict = requests.get(
            f"{self.api_root}/championships/{championship_id}/results",
            headers=self._get_header()    
        ).json()
        return r
    
    def get_team_games(self, team_id, tournament_id):
        r: dict = requests.get(
            f"{self.api_v1_root}/stats/time/teams/{team_id}/games/{self.game_id}" 
        ).json()
        games = {
            "won" : [],
            "loss" : []
        }

        done = []
        for game in r:
            game: dict
            match_id: str = game.get("matchId")
            if tournament_id != game.get("competitionId"):
                continue
            if match_id in done:
                continue
            match = self.get_match(match_id)
            if match.result.team1.id == team_id:
                maps_won = match.result.bo3_score_1
                maps_lost = match.result.bo3_score_2
            else:
                maps_won = match.result.bo3_score_2
                maps_lost = match.result.bo3_score_1
            for i in range(maps_won):
                games["won"].append(match)
            for i in range(maps_lost):
                games["loss"].append(match)
            done.append(match.id)

        return games

    def get_championship_details(self, championship_id) -> dict:
        r: dict = requests.get(
            f"{self.api_v1_championships_root}/championship/{championship_id}"
        ).json()
        return r.get('payload')
    