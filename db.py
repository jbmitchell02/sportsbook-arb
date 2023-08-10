
import sqlite3


def setup_mlb_opps():
    conn = sqlite3.connect('mlb_opps.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mlb_opps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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


def add_mlb_opp(mlb_opp):
    if mlb_opp.returns > 0:
        conn = sqlite3.connect('mlb_opps.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO mlb_opps (market, home_team, away_team, point, book1, book2, odds1, odds2, returns)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (mlb_opp.market, mlb_opp.home_team, mlb_opp.away_team, mlb_opp.point, mlb_opp.book1, mlb_opp.book2, mlb_opp.odds1, mlb_opp.odds2, mlb_opp.returns))
        conn.commit()
        conn.close()


if __name__ == '__main__':
    setup_mlb_opps()
