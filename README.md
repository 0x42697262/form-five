# 🐔 Chicken Habits — Weekly Habit Tracker

Track your habit hours and earn points each week.

## 📦 Features

* Add or set hours to any defined category
* Points system with weekly summaries
* Uses SQLite with a simple schema
* CLI interface using `argparse`

## 📋 Requirements

* Python 3.13+
* [`uv`](https://github.com/astral-sh/uv) for dependency management

> Note: No third-party packages are currently required — pure standard library.

---

## 🚀 Usage

### Create or update hours for a category:

```bash
uv run python main.py --update programming 2.5
uv run python main.py --set osu 1
```

### Optional: Specify custom database location

```bash
uv run python main.py --set ctf 3 --database ./mytracker.db
```

### Weekly Summary Output

After each command, you'll see:

* Dates tracked this week
* Logged hours by category
* Points earned per day
* Weekly total & whether minimum target was met

---

## 📁 Default Database

If not specified, the database is stored as:

```
./chicken-habits.db
```

---

## 🧠 Categories Supported

Short forms like `ctf`, `osu`, `maldev`, etc. are automatically mapped to their canonical names.

---

## 🛠 Development

Use [`uv`](https://github.com/astral-sh/uv) to manage and run:

```bash
uv venv
source .venv/bin/activate
uv pip install -e .
```

---

## 🧪 Testing

You can pass a temporary SQLite path when writing unit tests. Example with `tempfile`:

```python
import tempfile
from pathlib import Path

with tempfile.NamedTemporaryFile(suffix=".db") as tmp:
    db_path = Path(tmp.name)
    # use `db_path` in test
```
