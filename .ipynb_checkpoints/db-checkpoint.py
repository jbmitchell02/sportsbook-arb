import sqlite3

def setup_h2h():
    conn = sqlite3.connect('h2h_opps.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS h2h_opps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sport TEXT,
            team1 TEXT,
            team2 TEXT,
            book1 TEXT,
            book2 TEXT,
            odds1 REAL,
            odds2 REAL,
            arb_returns REAL,
            bet_prop REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def setup_spreads():
    conn = sqlite3.connect('spreads_opps.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS spreads_opps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sport TEXT,
            team1 TEXT,
            team2 TEXT,
            book1 TEXT,
            book2 TEXT,
            spread REAL,
            odds1 REAL,
            odds2 REAL,
            arb_returns REAL,
            bet_prop REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def add_h2h_opp(sport, team1, team2, book1, book2, odds1, odds2, arb_returns, bet_prop):
    conn = sqlite3.connect('h2h_opps.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO h2h_opps (sport, team1, team2, book1, book2, odds1, odds2, arb_returns, bet_prop)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (sport, team1, team2, book1, book2, odds1, odds2, arb_returns, bet_prop))
    conn.commit()
    conn.close()

def add_spreads_opp(sport, team1, team2, book1, book2, spread, odds1, odds2, arb_returns, bet_prop):
    conn = sqlite3.connect('spreads_opps.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO spreads_opps (sport, team1, team2, book1, book2, spread, odds1, odds2, arb_returns, bet_prop)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (sport, team1, team2, book1, book2, spread, odds1, odds2, arb_returns, bet_prop))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    setup_h2h()
    setup_spreads()