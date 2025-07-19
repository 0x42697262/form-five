from src.lib import database
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

    result = database.create(db_path)
    result = database.update(db_path, "osu", 3)
    result = database.update(db_path, "osu", 4.5)

    assert result == sqlite3.SQLITE_OK
