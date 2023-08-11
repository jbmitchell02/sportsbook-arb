
import requests
import pandas as pd
from datetime import datetime, timezone


class GameDetails:

    def __init__(self, id, sport_key, sport_title, commence_time, home_team, away_team):
        self.id = id
        self.sport_key = sport_key
        self.sport_title = sport_title
        self.home_team = home_team
        self.away_team = away_team
        utc_time = datetime.strptime(commence_time, '%Y-%m-%dT%H:%M:%SZ')
        self.commence_time = utc_time.replace(tzinfo=timezone.utc).astimezone(tz=None)

    def __str__(self):
        time = self.commence_time.strftime('%m/%d %I:%M %p')
        return f'{self.sport_title}: {self.home_team} vs {self.away_team} @ {time}'
    
    def __repr__(self):
        return str(self)
    
    def __eq__(self, other):
        if isinstance(other, GameDetails):
            return self.id == other.id
        
    def __hash__(self):
        return hash(self.id)


class OddsHandler:

    def __init__(self, apiKey, sports, bookmakers, markets=['h2h', 'spreads', 'totals']):
        self.apiKey = apiKey
        self.sports = sports
        self.markets = ','.join(markets)
        self.bookmakers = ','.join(bookmakers)
        self.odds = {}

    def update_odds(self):
        self.odds.clear()
        for sport in self.sports:
            request = self._req_api(sport)
            for game in request:
                self._process_game(game)
        self._convert_to_dfs()

    def _req_api(self, sport):
        return requests.get(
            f'https://api.the-odds-api.com/v4/sports/{sport}/odds',
            params={
                'apiKey': self.apiKey,
                'regions': 'us',
                'markets': self.markets,
                'oddsFormat': 'decimal',
                'bookmakers': self.bookmakers
                }).json()

    def _process_game(self, game):
        id = game['id']
        sport_key = game['sport_key']
        sport_title = game['sport_title']
        commence_time = game['commence_time']
        home_team = game['home_team']
        away_team = game['away_team']
        details = GameDetails(id, sport_key, sport_title, commence_time, home_team, away_team)
        for book in game['bookmakers']:
            bookmaker = book['key']
            for market in book['markets']:
                bet_type = market['key']
                point = 0
                if bet_type == 'spreads' or bet_type == 'totals':
                    point = market['outcomes'][0]['point']
                team1 = market['outcomes'][0]['name']
                odds1 = market['outcomes'][0]['price']
                team2 = market['outcomes'][1]['name']
                odds2 = market['outcomes'][1]['price']
                if bet_type == 'spreads' and team1 != home_team:
                    point = -point
                key = (details, bet_type, point)
                if key not in self.odds.keys():
                    self._new_key(key)
                self.odds[key]['bookmakers'].append(bookmaker)
                self.odds[key][team1].append(odds1)
                self.odds[key][team2].append(odds2)

    def _new_key(self, key):
        details = key[0]
        bet_type = key[1]
        if bet_type == 'totals':
            self.odds[key] = {'bookmakers': [], 'Over': [], 'Under': []}
        else:
            self.odds[key] = {'bookmakers': [], details.home_team: [], details.away_team: []}

    def _convert_to_dfs(self):
        for details, odds in self.odds.items():
            self.odds[details] = pd.DataFrame(odds)
