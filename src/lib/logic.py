from datetime import date, datetime
from pathlib import Path
import sqlite3

from src.lib import database

# hard coded lol
ALLOWED_CATEGORIES = {
    "software_development":         "software_development",
    "programming":                  "software_development",
    "coding":                       "software_development",
    "network_labs":                 "network_labs",
    "networking":                   "network_labs",
    "system_pwn":                   "system_pwn",
    "hackthebox":                   "system_pwn",
    "tryhackme":                    "system_pwn",
    "vulnhub":                      "system_pwn",
    "malware_research":             "malware_research",
    "malware_development":          "malware_research",
    "maldev":                       "malware_research",
    "capture_the_flag":             "capture_the_flag",
    "ctf":                          "capture_the_flag",
    "reverse_engineering":          "reverse_engineering",
    "bug_bounty":                   "bug_bounty",
    "stock_trading":                "stock_trading",
    "statistical_learning":         "statistical_learning",
    "cryptography":                 "cryptography",
    "osu":                          "osu",
    "gaming":                       "gaming",
    "doomscroll":                   "doomscroll",
    "doomscrolling":                "doomscroll",
    "exercise":                     "exercise",
}


def update_category(category: str, hours: int | float, db_path: Path) -> type:
    category = category.lower()
    today = date.today().strftime("%Y-%m-%d")

    assert isinstance(hours, (int, float)), "hours is not a number"
    assert isinstance(db_path, Path), "Not a Path"
    assert db_path.parent.exists(), f"{
        db_path.parent} parent directory does not exists"
    assert category in ALLOWED_CATEGORIES, f"{
        category} category does not exist"

    resp = database.create(db_path)

    if resp == sqlite3.OperationalError:
        print(f"[!] Database already exists: {db_path}")
        print("[!] Proceed to update hours")

    resp = database.update(db_path=db_path, date=today,
                           category=category, hours=hours)

    return resp


def read_data(date_str: str, category: str, db_path: Path) -> list:
    category = category.lower()

    assert isinstance(db_path, Path), "Not a Path"
    assert db_path.parent.exists(), f"{
        db_path.parent} parent directory does not exists"
    if category not in ALLOWED_CATEGORIES:
        category = ''

    result = database.read(
        db_path=db_path, selected_date=date_str, category=category)

    return result


def read_hours(date_str: str, category: str, db_path: Path) -> int | float:
    category = category.lower()

    assert isinstance(db_path, Path), "Not a Path"
    assert db_path.parent.exists(), f"{
        db_path.parent} parent directory does not exists"
    assert category in ALLOWED_CATEGORIES, f"{
        category} category does not exist"

    result = database.read_hours(
        db_path=db_path, selected_date=date_str, category=category)

    return result


def arg_update(category: str, hours: str, db_path: Path):
    assert hours.isdigit() is True, "hours is not a number"
    category = ALLOWED_CATEGORIES.get(category.lower())
    assert category is not None, 'Not a valid category'

    hours = float(hours)
    today = date.today().strftime("%Y-%m-%d")

    current_hours = read_hours(
        date_str=today, category=category, db_path=db_path)[0]
    print(current_hours)
    total_hours = current_hours + hours

    resp = update_category(category, total_hours, db_path)


def arg_set(category: str, hours: str, db_path: Path):
    category = ALLOWED_CATEGORIES.get(category.lower())
    assert category is not None, 'Not a valid category'
    try:
        hours = float(hours)
    except ValueError:
        raise "hours is not a number"

    hours = float(hours)
    resp = update_category(category, hours, db_path)


def arg_view(db_path: Path) -> list:
    assert isinstance(db_path, Path), "Not a Path"
    assert db_path.parent.exists(), f"{
        db_path.parent} parent directory does not exists"
    database.create(db_path=db_path)
    result = read_data(date_str='', category='', db_path=db_path)

    return result


def calculate_points(db_path: Path) -> float:
    assert isinstance(db_path, Path), "Not a Path"
    assert db_path.parent.exists(), f"{
        db_path.parent} parent directory does not exists"

    today = date.today().strftime("%Y-%m-%d")
    points_today: float = database.read_day_hours_total(
        db_path=db_path, selected_date=today)[0]
    doomscroll = database.read_hours(
        db_path=db_path, selected_date=today, category='doomscroll')[0]
    osu = database.read_hours(
        db_path=db_path, selected_date=today, category='osu')[0]
    gaming = database.read_hours(
        db_path=db_path, selected_date=today, category='gaming')[0]
    points_today -= doomscroll * 2
    points_today -= osu
    points_today -= gaming

    return points_today


def is_valid_date(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False
