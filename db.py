
import sqlite3


def setup_opps():
    conn = sqlite3.connect('opps.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS opps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sport TEXT,
            market TEXT,
            home_team TEXT,
            away_team TEXT,
            point REAL,
            book1 TEXT,
            book2 TEXT,
            odds1 REAL,
            odds2 REAL,
            returns REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


def add_opp(opp):
    if opp.returns > 0:
        conn = sqlite3.connect('opps.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO mlb_opps (sport, market, home_team, away_team, point, book1, book2, odds1, odds2, returns)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (opp.sport, opp.market, opp.home_team, opp.away_team, opp.point, opp.book1, opp.book2, opp.odds1, opp.odds2, opp.returns))
        conn.commit()
        conn.close()


if __name__ == '__main__':
    setup_opps()
