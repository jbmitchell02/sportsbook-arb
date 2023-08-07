import pandas as pd
import odds
import db

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
    
def calc_returns(v1, v2):
    top = v1 * v2 - v1 - v2
    bottom = v1 + v2
    return top/bottom

def h2h_arb(games):
    for game, odds in games.items():
        v1 = odds.iloc[:, 1].max()
        v1_index = odds.iloc[:, 1].idxmax()
        v2 = odds.iloc[:, 2].max()
        v2_index = odds.iloc[:, 2].idxmax()
        R = calc_returns(v1, v2)
        if R > -0.01:
            team1 = game[0]
            team2 = game[1]
            book1 = odds.iloc[v1_index, 0]
            book2 = odds.iloc[v2_index, 0]
            bet_prop = v1/v2
            #db.add_h2h_opp('baseball_mlb', team1, team2, book1, book2, v1, v2, R, bet_prop)
            print(f'H2H ({team1}, {team2}): {round(R*100, 3)}%')
            print(f'    {book1}: {v1}, {team1}, {round(1/bet_prop, 3)}*b_2')
            print(f'    {book2}: {v2}, {team2}, {round(bet_prop, 3)}*b_1')
            print()

def spreads_arb(games):
    for game, odds in games.items():
        grouped_odds = odds.groupby('spread')
        for spread, group in grouped_odds:
            v1 = group.iloc[:, 1].max()
            v1_index = group.iloc[:, 1].idxmax()
            v2 = group.iloc[:, 2].max()
            v2_index = group.iloc[:, 2].idxmax()
            R = calc_returns(v1, v2)
            if R > -0.01:
                team1 = game[0]
                team2 = game[1]
                book1 = group.iloc[v1_index, 0]
                book2 = group.iloc[v2_index, 0]
                bet_prop = v1/v2
                #db.add_spreads_opp('baseball_mlb', team1, team2, book1, book2, spread, v1, v2, R, bet_prop)
                print(f'Spread {spread} ({team1}, {team2}): {round(R*100, 3)}%')
                print(f'    {book1}: {v1}, {team1}, {round(1/bet_prop, 3)}*b_2')
                print(f'    {book2}: {v2}, {team2}, {round(bet_prop, 3)}*b_1')
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
            if R > -0.01:
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
