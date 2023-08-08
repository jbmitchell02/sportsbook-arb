import requests
import pandas as pd

def get_odds(sport, apiKey, regions, markets, oddsFormat='decimal', bookmakers='all'):
    response = requests.get(
        f'https://api.the-odds-api.com/v4/sports/{sport}/odds',
        params={
            'apiKey': apiKey,
            'regions': regions, # us | us2 | uk | au | eu
            'markets': markets, # h2h | spreads | totals | outrights
            'oddsFormat': oddsFormat, # decimal | american
            'bookmakers': bookmakers
            }).json()
    return response

def get_mlb_h2h_odds(apiKey, bookmakers='all'):
    response = get_odds('baseball_mlb', apiKey, 'us', 'h2h', 'decimal', bookmakers)
    games = {}
    for game in response:
        home_team = game['home_team']
        away_team = game['away_team']
        odds = {'bookmakers': [], home_team: [], away_team: []}
        for book in game['bookmakers']:
            odds['bookmakers'].append(book['key'])
            odds[book['markets'][0]['outcomes'][0]['name']].append(book['markets'][0]['outcomes'][0]['price'])
            odds[book['markets'][0]['outcomes'][1]['name']].append(book['markets'][0]['outcomes'][1]['price'])
        df = pd.DataFrame(odds)
        games[(home_team, away_team)] = df
    return games

def get_mlb_spreads_odds(apiKey, bookmakers='all'):
    response = get_odds('baseball_mlb', apiKey, 'us', 'spreads', 'decimal', bookmakers)
    games = {}

    for game in response:
        spreads = {}
        home_team = game['home_team']
        away_team = game['away_team']

        for book in game['bookmakers']:
            bookmaker = book['key']
            team1 = book['markets'][0]['outcomes'][0]['name']
            team2 = book['markets'][0]['outcomes'][1]['name']
            odds1 = book['markets'][0]['outcomes'][0]['price']
            odds2 = book['markets'][0]['outcomes'][1]['price']
            spread = book['markets'][0]['outcomes'][0]['point']
            spread_team = book['markets'][0]['outcomes'][0]['name']
            if spread_team != home_team:
                spread = -spread
            if spread not in spreads.keys():
                spreads[spread] = {'bookmakers': [], home_team: [], away_team: []}
            spreads[spread]['bookmakers'].append(bookmaker)
            spreads[spread][team1].append(odds1)
            spreads[spread][team2].append(odds2)

        for spread, odds in spreads.items():
            games[(home_team, away_team, spread)] = pd.DataFrame(odds)

    return games

def get_mlb_totals_odds(apiKey, bookmakers='all'):
    response = get_odds('baseball_mlb', apiKey, 'us', 'totals', 'decimal', bookmakers)
    games = {}
    for game in response:
        home_team = game['home_team']
        away_team = game['away_team']
        odds = {'bookmakers': [], 'Over': [], 'Under': [], 'total': []}
        for book in game['bookmakers']:
            odds['bookmakers'].append(book['key'])
            odds[book['markets'][0]['outcomes'][0]['name']].append(book['markets'][0]['outcomes'][0]['price'])
            odds[book['markets'][0]['outcomes'][1]['name']].append(book['markets'][0]['outcomes'][1]['price'])
            odds['total'].append(book['markets'][0]['outcomes'][0]['point'])
        df = pd.DataFrame(odds)
        games[(home_team, away_team)] = df
    return games
