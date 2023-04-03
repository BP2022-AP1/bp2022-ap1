import argparse
import os
import subprocess

from peewee_migrate import Router

from src.base_model import db
from src.constants import tables

MIGRATION_DIRECTORY: str = "db/local/migrations"


def run(args: argparse.Namespace):
    """Run the database

    :param args: parsed arguments containing the string `database_name`
    :type args: argparse.Namespace
    """
    name = args.database_name
    print("Running database...")
    print(os.getcwd())
    subprocess.run(
        [
            "docker",
            "compose",
            "-f",
            "db/local/docker-compose.yml",
            "up",
            "-d",
            "-".join(["postgres", name]),
        ],
        check=True,
    )


def stop(args: argparse.Namespace):
    """Stop the database

    :param args: parsed arguments containing the string `database_name`
    :type args: argparse.Namespace
    """
    name = args.database_name
    print("Stopping database...")
    subprocess.run(
        [
            "docker",
            "compose",
            "-f",
            "db/local/docker-compose.yml",
            "stop",
            "-".join(["postgres", name]),
        ],
        check=True,
    )


def create(_: argparse.Namespace):
    """Create database tables"""
    db.create_tables(tables)
    print("Created tables")


def drop(_: argparse.Namespace):
    """Drop database tables"""
    db.drop_tables(tables)
    print("Dropped tables")


def recreate(args: argparse.Namespace):
    """Drop and create database tables

    :param args: parsed arguments (no arguments are used)
    :type args: argparse.Namespace
    """
    drop(args)
    create(args)


def construct_migration_router() -> Router:
    """Construct a migration router

    :return: A migration router
    :rtype: Router
    """
    if not os.path.exists(MIGRATION_DIRECTORY):
        os.mkdir(MIGRATION_DIRECTORY)
    return Router(db, migrate_dir=MIGRATION_DIRECTORY)


def migration(args: argparse.Namespace):
    """Create, run or rollback (a) migration(s)

    :param args: parsed arguments containing the string `migration_action` and the string `migration_name`
    """
    action = args.migration_action
    name = args.migration_name
    router = construct_migration_router()

    if action == "create":
        router.create(name)
        print(f"Created migration: {name}")
    elif action == "run":
        if name == "ALL":
            router.run()
            print("Ran all unapplied migrations")
        else:
            router.run(name)
            print(f"Ran migration: {name}")


def rollback(_: argparse.Namespace):
    """Rollback latest migration"""
    router = construct_migration_router()
    router.rollback()
    print("Rolled back latest migration")


def execute_on_args():
    """Parse command line arguments and execute the corresponding function"""
    parser = argparse.ArgumentParser(description="Manage database")
    subparsers = parser.add_subparsers(dest="action", help="Action to perform")

    run_parser = subparsers.add_parser("run", help="Run the database")
    run_parser.add_argument(
        "database_name", type=str, help="Name of the database", choices=["dev", "test"]
    )
    run_parser.set_defaults(func=run)

    stop_parser = subparsers.add_parser("stop", help="Stop the database")
    stop_parser.add_argument(
        "database_name", type=str, help="Name of the database", choices=["dev", "test"]
    )
    stop_parser.set_defaults(func=stop)

    create_parser = subparsers.add_parser("create", help="Create database tables")
    create_parser.set_defaults(func=create)

    drop_parser = subparsers.add_parser("drop", help="Drop database tables")
    drop_parser.set_defaults(func=drop)

    recreate_parser = subparsers.add_parser(
        "recreate", help="Drop and create database tables"
    )
    recreate_parser.set_defaults(func=recreate)

    migration_parser = subparsers.add_parser("migration", help="Manage migration")
    migration_parser.add_argument(
        "migration_action",
        type=str,
        help="Action to perform",
        choices=["create", "run"],
    )
    migration_parser.add_argument(
        "migration_name", type=str, help="Name of the migration"
    )
    migration_parser.set_defaults(func=migration)

    rollback_parser = subparsers.add_parser(
        "rollback", help="Rollback latest migration"
    )
    rollback_parser.set_defaults(func=rollback)

    args = parser.parse_args()
    args.func(args)


def main():
    """Main entry point for the script"""
    execute_on_args()


if __name__ == "__main__":
    main()
