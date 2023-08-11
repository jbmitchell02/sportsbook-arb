
import sqlite3


def setup_opps():
    conn = sqlite3.connect('opps.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS opps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sport TEXT,
            bet_type TEXT,
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


if __name__ == '__main__':
    setup_opps()
