import requests
import pandas as pd

def get_odds(apiKey, sport, market, bookmakers='all', regions='us', oddsFormat='decimal'):
    '''
    Parameters
        apiKey: Your personal The Odds API key
        sport: 'baseball_mlb', ...
        market: 'h2h', 'spreads', 'totals'
        bookmakers: Comma separated string of bookmakers to include
        regions: Comma separated string of regions to include
        oddsFormat: 'decimal', 'american'

    Returns the request to The Odds API as a dictionary
    '''
    if bookmakers == 'all':
        return requests.get(
            f'https://api.the-odds-api.com/v4/sports/{sport}/odds',
            params={
                'apiKey': apiKey,
                'regions': regions,
                'markets': market,
                'oddsFormat': oddsFormat
                }).json()
    else:
        return requests.get(
            f'https://api.the-odds-api.com/v4/sports/{sport}/odds',
            params={
                'apiKey': apiKey,
                'regions': regions,
                'markets': market,
                'oddsFormat': oddsFormat,
                'bookmakers': bookmakers
                }).json()

class MLBDataHandler:
    '''
    Class to handle MLB data from The Odds API. Access the data through the odds variable and update it with update_odds().

    self.odds
        Keys
            h2h: ('h2h', home_team, away_team)
            spreads: ('spreads', home_team, away_team, spread)
            totals: ('totals', home_team, away_team, total)
        Values
            h2h & spreads: DataFrame with columns ['bookmakers', home_team, away_team]
            totals: DataFrame with columns ['bookmakers', 'Over', 'Under']
    '''

    def __init__(self, apiKey, markets=['h2h', 'spreads', 'totals'], bookmakers='all', regions='us'):
        '''
        Parameters
            apiKey: Your personal The Odds API key
            markets: List of markets to include
            bookmakers: Comma separated string of bookmakers to include
            regions: Comma separated string of regions to include
        '''
        self.apiKey = apiKey
        self.markets = markets
        self.bookmakers = bookmakers
        self.regions = regions
        self.odds = {}
    
    def _get_h2h_odds(self):
        response = get_odds(self.apiKey, 'baseball_mlb', 'h2h', self.bookmakers, self.regions)
        h2h_odds = {}

        for game in response:
            home_team = game['home_team']
            away_team = game['away_team']
            odds = {'bookmakers': [], home_team: [], away_team: []}

            for book in game['bookmakers']:
                bookmaker = book['key']
                team1 = book['markets'][0]['outcomes'][0]['name']
                team2 = book['markets'][0]['outcomes'][1]['name']
                odds1 = book['markets'][0]['outcomes'][0]['price']
                odds2 = book['markets'][0]['outcomes'][1]['price']

                odds['bookmakers'].append(bookmaker)
                odds[team1].append(odds1)
                odds[team2].append(odds2)
            
            h2h_odds[('h2h', home_team, away_team)] = pd.DataFrame(odds)

        return h2h_odds
    
    def _get_spreads_odds(self):
        response = get_odds(self.apiKey, 'baseball_mlb', 'spreads', self.bookmakers, self.regions)
        spreads_odds = {}

        for game in response:
            home_team = game['home_team']
            away_team = game['away_team']
            odds = {}

            for book in game['bookmakers']:
                bookmaker = book['key']
                team1 = book['markets'][0]['outcomes'][0]['name']
                team2 = book['markets'][0]['outcomes'][1]['name']
                odds1 = book['markets'][0]['outcomes'][0]['price']
                odds2 = book['markets'][0]['outcomes'][1]['price']
                spread = book['markets'][0]['outcomes'][0]['point']
                if team1 != home_team:
                    spread = -spread

                if spread not in odds.keys():
                    odds[spread] = {'bookmakers': [], home_team: [], away_team: []}

                odds[spread]['bookmakers'].append(bookmaker)
                odds[spread][team1].append(odds1)
                odds[spread][team2].append(odds2)

            for spread, odds in odds.items():
                spreads_odds[('spreads', home_team, away_team, spread)] = pd.DataFrame(odds)

        return spreads_odds
    
    def _get_totals_odds(self):
        response = get_odds(self.apiKey, 'baseball_mlb', 'totals', self.bookmakers, self.regions)
        totals_odds = {}

        for game in response:
            home_team = game['home_team']
            away_team = game['away_team']
            odds = {}

            for book in game['bookmakers']:
                bookmaker = book['key']
                over_or_under1 = book['markets'][0]['outcomes'][0]['name']
                over_or_under2 = book['markets'][0]['outcomes'][1]['name']
                odds1 = book['markets'][0]['outcomes'][0]['price']
                odds2 = book['markets'][0]['outcomes'][1]['price']
                total = book['markets'][0]['outcomes'][0]['point']

                if total not in odds.keys():
                    odds[total] = {'bookmakers': [], 'Over': [], 'Under': []}

                odds[total]['bookmakers'].append(bookmaker)
                odds[total][over_or_under1].append(odds1)
                odds[total][over_or_under2].append(odds2)

            for total, odds in odds.items():
                totals_odds[('totals', home_team, away_team, total)] = pd.DataFrame(odds)

        return totals_odds
    
    def update_odds(self):
        new_odds = {}
        if 'h2h' in self.markets:
            new_odds.update(self._get_h2h_odds())
        if 'spreads' in self.markets:
            new_odds.update(self._get_spreads_odds())
        if 'totals' in self.markets:
            new_odds.update(self._get_totals_odds())
        self.odds = new_odds
