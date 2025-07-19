from src.lib import database
from datetime import date
from pathlib import Path
import sqlite3
import tempfile


def test_create():
    with tempfile.NamedTemporaryFile(prefix='chicken', suffix='.db', delete=True) as tmp:
        db_path = Path(tmp.name)
    print(db_path)

    result = database.create(db_path)

    assert result == sqlite3.SQLITE_OK

    result = database.create(db_path)
    assert result == sqlite3.OperationalError


def test_update():
    with tempfile.NamedTemporaryFile(prefix='chicken', suffix='.db', delete=True) as tmp:
        db_path = Path(tmp.name)
    print(db_path)

    database.create(db_path)
    database.update(db_path, "osu", 3)
    database.update(db_path, "osu", 4.5)

    con = sqlite3.connect(db_path)
    cur = con.cursor()

    today = date.today().strftime("%Y-%m-%d")
    cur.execute(
        "SELECT * FROM habit_log WHERE date=? AND category=?;", (today, "osu"))

    result = cur.fetchall()

    assert len(result) == 1
    assert result == [(today, 'osu', 4.5)]


def test_read():
    with tempfile.NamedTemporaryFile(prefix='chicken', suffix='.db', delete=True) as tmp:
        db_path = Path(tmp.name)
    print(db_path)

    database.create(db_path)
    database.update(db_path, "software_development", 2)
    database.update(db_path, "osu", 3)
    database.update(db_path, "doomscroll", 2.5)
    database.update(db_path, "osu", 4.5)

    today = date.today().strftime("%Y-%m-%d")

    result = database.read(db_path, today, 'osu')
    assert len(result) == 1
    assert result == [(today, 'osu', 4.5)]

    result = database.read(db_path, today, '')
    assert len(result) == 3
    assert result == [
        (today, 'software_development', 2),
        (today, 'osu', 4.5),
        (today, 'doomscroll', 2.5),
    ]
