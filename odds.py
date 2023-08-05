import requests
import pandas as pd

def get_mlb_odds(apiKey, regions, markets, oddsFormat):
    response = requests.get(
        'https://api.the-odds-api.com/v4/sports/baseball_mlb/odds',
        params={
            'apiKey': apiKey,
            'regions': regions, # us | us2 | uk | au | eu
            'markets': markets, # h2h | spreads | totals | outrights
            'oddsFormat': oddsFormat, # decimal | american
            'bookmakers': 'barstool,betmgm,betrivers,draftkings,fanduel,pointsbetus,unibet_us,williamhill_us,wynnbet'
            }).json()
    return response

def get_mlb_h2h_odds(apiKey):
    response = get_mlb_odds(apiKey, 'us', 'h2h', 'decimal')
    games = []
    for game in response:
        odds = {'bookmakers': [], game['home_team']: [], game['away_team']: []}
        for book in game['bookmakers']:
            odds['bookmakers'].append(book['key'])
            odds[book['markets'][0]['outcomes'][0]['name']].append(book['markets'][0]['outcomes'][0]['price'])
            odds[book['markets'][0]['outcomes'][1]['name']].append(book['markets'][0]['outcomes'][1]['price'])
        df = pd.DataFrame(odds)
        games.append(df)
    return games

def get_mlb_spreads_odds(apiKey):
    response = get_mlb_odds(apiKey, 'us', 'spreads', 'decimal')
    games = []
    for game in response:
        odds = {'bookmakers': [], game['home_team']: [], game['away_team']: [], 'spread': []}
        for book in game['bookmakers']:
            odds['bookmakers'].append(book['key'])
            odds[book['markets'][0]['outcomes'][0]['name']].append(book['markets'][0]['outcomes'][0]['price'])
            odds[book['markets'][0]['outcomes'][1]['name']].append(book['markets'][0]['outcomes'][1]['price'])
            odds['spread'].append(abs(book['markets'][0]['outcomes'][0]['point']))
        df = pd.DataFrame(odds)
        games.append(df)
    return games
