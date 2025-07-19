import math
import sqlite3
from datetime import date
from pathlib import Path


def create(db_path: Path) -> type:
    if not isinstance(db_path, Path):
        return sqlite3.DataError

    con = sqlite3.connect(db_path)
    cur = con.cursor()

    cur.execute("""
                SELECT name
                FROM sqlite_master
                WHERE type='table' AND name='habit_log';
                """)
    result = cur.fetchone()

    if result:
        return sqlite3.OperationalError

    cur.execute("""CREATE TABLE habit_log(
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                hours REAL NOT NULL CHECK (hours >= 0),
                PRIMARY KEY (date, category)
                );""")
    con.commit()

    return sqlite3.SQLITE_OK


def update(db_path: Path, category: str, hours: int) -> type:
    if not isinstance(hours, (float, int)):
        return sqlite3.DataError
    if not isinstance(db_path, Path):
        return sqlite3.DataError

    today = date.today().strftime("%Y-%m-%d")
    hours = math.floor(hours)

    con = sqlite3.connect(db_path)
    cur = con.cursor()

    cur.execute("""INSERT INTO habit_log (date, category, hours)
                VALUES (?, ?, ?)
                ON CONFLICT (date, category) DO UPDATE SET
                    hours = excluded.hours;
                """, (today, category, hours)
                )

    con.commit()

    return sqlite3.SQLITE_OK
