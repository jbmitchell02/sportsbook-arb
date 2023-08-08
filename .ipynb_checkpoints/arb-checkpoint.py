import pandas as pd
import odds
import db

def calc_returns(v1, v2):
    top = v1 * v2 - v1 - v2
    bottom = v1 + v2
    return top/bottom

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

def h2h_arb(games, return_threshold):
    for game, odds in games.items():
        v1_idx = odds.iloc[:, 1].idxmax()
        v2_idx = odds.iloc[:, 2].idxmax()
        v1 = odds.iloc[v1_idx, 1]
        v2 = odds.iloc[v2_idx, 2]
        R = calc_returns(v1, v2)
        if R > return_threshold:
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

def spreads_arb(games, return_threshold):
    for game, odds in games.items():
        v1_idx = odds.iloc[:, 1].idxmax()
        v2_idx = odds.iloc[:, 2].idxmax()
        v1 = odds.iloc[v1_idx, 1]
        v2 = odds.iloc[v2_idx, 2]
        R = calc_returns(v1, v2)
        if R > return_threshold:
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

#basically changed it so we loop over every set of unique totals for every game, then print them more structured, idrk if this is better or worse though. 
def totals_arb(games, return_threshold):
    print(f"Return Threshold is: {return_threshold}")
    for game, odds in games.items():
        print(f"Books for ({game[0]}, {game[1]}):\n")
        unique_totals = odds['total'].unique() #grab list of unique totals to loop over through the odds df
        for total in unique_totals:
            print(f'\tTotal: {total}:')
            for index, row in odds[odds['total']==total].iterrows():
                v1 = row['Over']
                v2 = row['Under']
                R = calc_returns(v1,v2)
                if R > return_threshold:
                    team1 = game[0]
                    team2 = game[1]
                    book = row['bookmakers']
                    bet_prop = v1/v2
                    print(f'\t\t    {book}: {v1}, {team1}, {round(1/bet_prop, 3)}*b_2')
                    print(f'\t\t    {book}: {v2}, {team2}, {round(bet_prop, 3)}*b_1')
                    print(f'\t\t    Return: {round(R*100, 3)}%')
                    print()
