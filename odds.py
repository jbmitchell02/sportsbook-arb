
import requests
import pandas as pd

    
class DataHandler:

    def __init__(self, apiKey, sports, bookmakers, markets=['h2h', 'spreads', 'totals']):
        self.apiKey = apiKey
        self.sports = sports
        self.markets = ','.join(markets)
        self.bookmakers = ','.join(bookmakers)
        self.odds = {}

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
    
    def _process_h2h(self, sport, market, bookmaker, home_team, away_team):
        details = (sport, 'h2h', home_team, away_team)
        if details not in self.odds.keys():
            self.odds[details] = {'bookmakers': [], home_team: [], away_team: []}
        team1 = market['outcomes'][0]['name']
        odds1 = market['outcomes'][0]['price']
        team2 = market['outcomes'][1]['name']
        odds2 = market['outcomes'][1]['price']
        self.odds[details]['bookmakers'].append(bookmaker)
        self.odds[details][team1].append(odds1)
        self.odds[details][team2].append(odds2)

    def _process_spreads(self, sport, market, bookmaker, home_team, away_team):
        details = (sport, 'spreads', home_team, away_team, market['outcomes'][0]['point'])
        if details not in self.odds.keys():
            self.odds[details] = {'bookmakers': [], home_team: [], away_team: []}
        team1 = market['outcomes'][0]['name']
        odds1 = market['outcomes'][0]['price']
        team2 = market['outcomes'][1]['name']
        odds2 = market['outcomes'][1]['price']
        self.odds[details]['bookmakers'].append(bookmaker)
        self.odds[details][team1].append(odds1)
        self.odds[details][team2].append(odds2)

    def _process_totals(self, sport, market, bookmaker, home_team, away_team):
        details = (sport, 'totals', home_team, away_team, market['outcomes'][0]['point'])
        if details not in self.odds.keys():
            self.odds[details] = {'bookmakers': [], 'Over': [], 'Under': []}
        over_under1 = market['outcomes'][0]['name']
        odds1 = market['outcomes'][0]['price']
        over_under2 = market['outcomes'][1]['name']
        odds2 = market['outcomes'][1]['price']
        self.odds[details]['bookmakers'].append(bookmaker)
        self.odds[details][over_under1].append(odds1)
        self.odds[details][over_under2].append(odds2)

    def update_odds(self):
        self.odds = {}
        for sport in self.sports:
            req = self._req_api(sport)
            for game in req:
                home_team = game['home_team']
                away_team = game['away_team']
                for book in game['bookmakers']:
                    bookmaker = book['key']
                    for market in book['markets']:
                        bet_type = market['key']
                        if bet_type == 'h2h':
                            self._process_h2h(sport, market, bookmaker, home_team, away_team)
                        elif bet_type == 'spreads':
                            self._process_spreads(sport, market, bookmaker, home_team, away_team)
                        elif bet_type == 'totals':
                            self._process_totals(sport, market, bookmaker, home_team, away_team)
        for key in self.odds.keys():
            self.odds[key] = pd.DataFrame(self.odds[key])
