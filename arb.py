import pandas as pd
from odds import MLBDataHandler
import odds
import db

def calc_returns(v1, v2):
    top = v1 * v2
    bottom = v1 + v2
    return (top/bottom) - 1

class MLBArbitrage:
    '''
    idk what im doing with this yet
    '''

    def __init__(self, apiKey, markets=['h2h', 'spreads', 'totals'], bookmakers='all', regions='us'):
        self.apiKey = apiKey
        self.markets = markets
        self.bookmakers = bookmakers
        self.regions = regions
        self.datahandler = MLBDataHandler(apiKey, markets, bookmakers, regions)
        self.opportunities = self._update_opportunities()

    def _update_opportunities(self):
        pass


def arbitrage_calc(apiKey, markets=['all'], bookmakers='all'):
    if 'all' in markets:
        h2h = odds.get_mlb_h2h_odds(apiKey, bookmakers)
        spreads = odds.get_mlb_spreads_odds(apiKey, bookmakers)
        totals = odds.get_mlb_totals_odds(apiKey, bookmakers)
        h2h_arb(h2h)
        spreads_arb(spreads)
        totals_arb(totals)
        return
    if 'h2h' in markets:
        h2h = odds.get_mlb_h2h_odds(apiKey, bookmakers)
        h2h_arb(h2h)
    if 'spreads' in markets:
        spreads = odds.get_mlb_spreads_odds(apiKey, bookmakers)
        spreads_arb(spreads)
    if 'totals' in markets:
        totals = odds.get_mlb_totals_odds(apiKey, bookmakers)
        totals_arb(totals)

def h2h_arb(games):
    for game, odds in games.items():
        v1_idx = odds.iloc[:, 1].idxmax()
        v2_idx = odds.iloc[:, 2].idxmax()
        v1 = odds.iloc[v1_idx, 1]
        v2 = odds.iloc[v2_idx, 2]
        R = calc_returns(v1, v2)
        if R > -0.05:
            home_team = game[0]
            away_team = game[1]
            book1 = odds.iloc[v1_idx, 0]
            book2 = odds.iloc[v2_idx, 0]
            print_h2h_arb(home_team, away_team, book1, book2, v1, v2, R)

def print_h2h_arb(home_team, away_team, book1, book2, v1, v2, R):
    print(f'H2H ({home_team}, {away_team}): {round(R*100, 3)}%')
    print(f'    {book1}: {v1}, {home_team}, {round(v2/v1, 3)}*b_2')
    print(f'    {book2}: {v2}, {away_team}, {round(v1/v2, 3)}*b_1')
    print()

def spreads_arb(games):
    for game, odds in games.items():
        v1_idx = odds.iloc[:, 1].idxmax()
        v2_idx = odds.iloc[:, 2].idxmax()
        v1 = odds.iloc[v1_idx, 1]
        v2 = odds.iloc[v2_idx, 2]
        R = calc_returns(v1, v2)
        if R > -0.05:
            home_team = game[0]
            away_team = game[1]
            spread = game[2]
            book1 = odds.iloc[v1_idx, 0]
            book2 = odds.iloc[v2_idx, 0]
            print_spread_arb(home_team, away_team, spread, book1, book2, v1, v2, R)

def print_spread_arb(home_team, away_team, spread, book1, book2, v1, v2, R):
    print(f'Spread {spread} ({home_team}, {away_team}): {round(R*100, 3)}%')
    print(f'    {book1}: {v1}, {home_team}, {round(v2/v1, 3)}*b_2')
    print(f'    {book2}: {v2}, {away_team}, {round(v1/v2, 3)}*b_1')
    print()


def totals_arb(games):
    for game, odds in games.items():
        grouped_odds = odds.groupby('total')
        for total, group in grouped_odds:
            v1 = group.iloc[:, 1].max()
            v1_index = group.iloc[:, 1].idxmax()
            v2 = group.iloc[:, 2].max()
            v2_index = group.iloc[:, 2].idxmax()
            R = calc_returns(v1, v2)
            if R > -0.05:
                team1 = game[0]
                team2 = game[1]
                book1 = group.iloc[v1_index, 0]
                book2 = group.iloc[v2_index, 0]
                bet_prop = v1/v2
                #db.add_totals_opp('baseball_mlb', team1, team2, book1, book2, total, v1, v2, R, bet_prop)
                print(f'Total {total} ({team1}, {team2}): {round(R*100, 3)}%')
                print(f'    {book1}: {v1}, {team1}, {round(1/bet_prop, 3)}*b_2')
                print(f'    {book2}: {v2}, {team2}, {round(bet_prop, 3)}*b_1')
                print()
