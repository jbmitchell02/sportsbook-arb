import pandas as pd
import odds
import db

def arbitrage_calc(apiKey, markets='all'):
    if markets == 'all':
        h2h_games = odds.get_mlb_h2h_odds(apiKey)
        spreads_games = odds.get_mlb_spreads_odds(apiKey)
        h2h_arb(h2h_games)
        spreads_arb(spreads_games)
    elif markets == 'h2h':
        h2h_games = odds.get_mlb_h2h_odds(apiKey)
        h2h_arb(h2h_games)
    elif markets == 'spreads':
        spreads_games = odds.get_mlb_spreads_odds(apiKey)
        spreads_arb(spreads_games)
    else:
        print('Invalid market. Please choose from: all, h2h, spreads')


def h2h_arb(games):
    for df in games:
        v1 = df.iloc[:, 1].max()
        v1_index = df.iloc[:, 1].idxmax()
        v2 = df.iloc[:, 2].max()
        v2_index = df.iloc[:, 2].idxmax()
        top = v1 * v2 - v1 - v2
        bottom = v1 + v2
        if top > bottom:
            R = (top/bottom)-1
            team1 = df.columns[1]
            team2 = df.columns[2]
            book1 = df.iloc[v1_index, 0]
            book2 = df.iloc[v2_index, 0]
            bet_prop = v1/v2
            #db.add_h2h_opp('baseball_mlb', team1, team2, book1, book2, v1, v2, R, bet_prop)
            print(f'H2H ({team1}, {team2}): {round(R*100, 3)}%')
            print(f'    {book1}: {v1} - {team1}')
            print(f'    {book2}: {v2} - {team2}')

def spreads_arb(games):
    for df in games:
        grouped_df = df.groupby('spread')
        for spread, group in grouped_df:
            v1 = group.iloc[:, 1].max()
            v1_index = group.iloc[:, 1].idxmax()
            v2 = group.iloc[:, 2].max()
            v2_index = group.iloc[:, 2].idxmax()
            top = v1 * v2 - v1 - v2
            bottom = v1 + v2
            if top > bottom:
                R = (top/bottom)-1
                team1 = group.columns[1]
                team2 = group.columns[2]
                book1 = group.iloc[v1_index, 0]
                book2 = group.iloc[v2_index, 0]
                bet_prop = v1/v2
                #db.add_spreads_opp('baseball_mlb', team1, team2, book1, book2, spread, v1, v2, R, bet_prop)
                print(f'Spread {spread} ({team1}, {team2}): {round(R*100, 3)}%')
                print(f'    {book1}: {v1} - {team1}')
                print(f'    {book2}: {v2} - {team2}')