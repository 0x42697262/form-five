import sqlite3
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


def update(db_path: Path, date: str, category: str, hours: int) -> type:
    if not isinstance(hours, (float, int)):
        return sqlite3.DataError
    if not isinstance(db_path, Path):
        return sqlite3.DataError
    if not db_path.exists():
        return sqlite3.DatabaseError

    con = sqlite3.connect(db_path)
    cur = con.cursor()

    cur.execute("""INSERT INTO habit_log (date, category, hours)
                VALUES (?, ?, ?)
                ON CONFLICT (date, category) DO UPDATE SET
                    hours = excluded.hours;
                """, (date, category, hours)
                )

    con.commit()

    return sqlite3.SQLITE_OK


def read(db_path: Path, selected_date: str, category: str):
    if not isinstance(db_path, Path):
        return sqlite3.DataError
    if not db_path.exists():
        return sqlite3.DatabaseError

    category = category.lower()

    con = sqlite3.connect(db_path)
    cur = con.cursor()

    if category:
        cur.execute("""SELECT * FROM habit_log
                        WHERE date=? AND category=?;
                    """, (selected_date, category)
                    )
    if not category or not selected_date:
        cur.execute("SELECT * FROM habit_log;")
    result = cur.fetchall()

    return result


def read_day(db_path: Path, selected_date: str):
    if not isinstance(db_path, Path):
        return sqlite3.DataError
    if not db_path.exists():
        return sqlite3.DatabaseError

    con = sqlite3.connect(db_path)
    cur = con.cursor()

    cur.execute("""SELECT * FROM habit_log
                    WHERE date=?;
                """, selected_date
                )
    result = cur.fetchall()

    return result


def read_day_hours_total(db_path: Path, selected_date: str) -> float:
    if not isinstance(db_path, Path):
        return sqlite3.DataError
    if not db_path.exists():
        return sqlite3.DatabaseError

    con = sqlite3.connect(db_path)
    cur = con.cursor()

    cur.execute("SELECT SUM(hours) FROM habit_log WHERE date=?;",
                (selected_date,))
    result = cur.fetchone()

    return result


def read_hours(db_path: Path, selected_date: str, category: str):
    if not isinstance(db_path, Path):
        return sqlite3.DataError
    if not db_path.exists():
        return sqlite3.DatabaseError

    category = category.lower()

    con = sqlite3.connect(db_path)
    cur = con.cursor()

    if category:
        cur.execute("""SELECT hours FROM habit_log
                        WHERE date=? AND category=?;
                    """, (selected_date, category)
                    )
    result = cur.fetchone()

    if not result:
        result = (0,)

    return result
