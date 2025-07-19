from pathlib import Path
import argparse

from src.lib import logic


def main():
    default_db_path: Path = Path("./chicken-habits.db").absolute()

    parser = argparse.ArgumentParser(description="Track your habit hours")
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        '-u',
        '--update',
        nargs=2,
        metavar=('CATEGORY', 'HOURS'),
        help="Increment hours for a category",
    )
    group.add_argument(
        '-s',
        '--set',
        nargs=2,
        metavar=('CATEGORY', 'HOURS'),
        help="Set hours for a category (overwrite)",
    )
    parser.add_argument(
        '--database',
        default=default_db_path,
        help=f"Path to SQLite database file (default: {default_db_path})"
    )

    args = parser.parse_args()

    if args.update:
        category = args.update[0]
        hours = args.update[1]
        logic.arg_update(category=category, hours=hours, db_path=args.database)

    if args.set:
        category = args.set[0]
        hours = args.set[1]
        logic.arg_set(category=category, hours=hours, db_path=args.database)

    result = logic.arg_view(db_path=args.database)
    current_date = ''
    for log in result:
        if current_date != log[0]:
            current_date = log[0]
            print(f"{current_date}:")
        print(f"You logged `{log[1]}` for {log[2]} hours.")
    print()
    print(f"Your total points today: {logic.calculate_points(args.database)}")
    print("Minimum points required per day: 2.0")


if __name__ == "__main__":
    main()
