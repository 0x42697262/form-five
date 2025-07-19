from pathlib import Path
import argparse

from src.lib import logic

MINIMUM_WEEKLY_POINTS = 21


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

    points = logic.calculate_points_weekly(db_path=args.database)
    total_points = 0
    print(f"Start date of the week: {points.get('__monday')}")
    print(f"End date of the week: {points.get('__sunday')}")
    for day, log in points.items():
        if not isinstance(log, dict):
            continue
        print(f"{day}:")
        for category, hours in log.items():
            if category != '__points':
                print(f"You logged `{category}` for {hours} hours.")
        total_points += log['__points']
        print(f"Total points: {log['__points']}")
        print()
    print('-'*4)
    print(f"Total points this week: {total_points}")
    print(f"Minimum weekly points required: {MINIMUM_WEEKLY_POINTS}")
    if total_points < MINIMUM_WEEKLY_POINTS:
        print("You did not reach the minimum weekly points. Please put more effort.")
    print('-'*4)


if __name__ == "__main__":
    main()
