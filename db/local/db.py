import argparse
import os
import sys
import subprocess
from typing import Type

from peewee_migrate import Router

from src.base_model import BaseModel, db

MIGRATION_DIRECTORY: str = "db/local/migrations"

models: list[Type[BaseModel]] = BaseModel.__subclasses__()


def run(args: argparse.Namespace):
    """Run the database

    :param args: parsed arguments
    :type args: argparse.Namespace
    """
    name = args.database_name
    print('Running database...')
    print(os.getcwd())
    subprocess.run([
        "docker-compose", "-f", "db/local/docker-compose.yml", "up",
        "-d", "-".join(["postgres", name])
    ])


def stop(args: argparse.Namespace):
    """Stop the database

    :param args: parsed arguments
    :type args: argparse.Namespace
    """
    name = args.database_name
    print('Stopping database...')
    subprocess.run([
        "docker-compose", "-f", "db/local/docker-compose.yml", "stop",
        "-".join(["postgres", name])
    ])


def create(_: argparse.Namespace):
    """Create database tables
    """
    db.create_tables(models)
    print('Created tables')


def drop(_: argparse.Namespace):
    """Drop database tables
    """
    db.drop_tables(models)
    print('Dropped tables')


def recreate(args: argparse.Namespace):
    """Drop and create database tables

    :param args: parsed arguments
    :type args: argparse.Namespace
    """
    drop(args)
    create(args)


def fail_on_name(name: str | None):
    """Fail if no name is provided

    :param name: migration name to test
    :type name: str | None
    """
    if not name:
        print('Please provide a name for the migration', file=sys.stderr)
        sys.exit(1)


def migration(args: argparse.Namespace):
    """Create, run or rollback (a) migration(s)

    :param args: parsed arguments
    """
    action = args.migration_action
    name = args.migration_name

    if not os.path.exists(MIGRATION_DIRECTORY):
        os.mkdir(MIGRATION_DIRECTORY)
    router = Router(db, migrate_dir=MIGRATION_DIRECTORY)

    if action == 'create':
        fail_on_name(name)
        router.create(name)
        print(f'Created migration: {name}')
    elif action == 'run':
        if not name:
            router.run()
            print('Ran all unapplied migrations')
        else:
            router.run(name)
            print(f'Ran migration: {name}')
    elif action == 'rollback':
        fail_on_name(name)
        router.rollback(name)
        print(f'Rolled back migration: {name}')


def execute_on_args():
    """Parse command line arguments and execute the corresponding function
    """
    parser = argparse.ArgumentParser(description='Manage database')
    subparsers = parser.add_subparsers(
        dest='action', help='Action to perform'
    )

    run_parser = subparsers.add_parser('run', help='Run the database')
    run_parser.add_argument(
        "database_name", type=str, help="Name of the database",
        choices=['dev', 'test']
    )
    run_parser.set_defaults(func=run)

    stop_parser = subparsers.add_parser('stop', help='Stop the database')
    stop_parser.add_argument(
        "database_name", type=str, help="Name of the database",
        choices=['dev', 'test']
    )
    stop_parser.set_defaults(func=stop)

    create_parser = subparsers.add_parser(
        'create', help='Create database tables'
    )
    create_parser.set_defaults(func=create)

    drop_parser = subparsers.add_parser('drop', help='Drop database tables')
    drop_parser.set_defaults(func=drop)

    recreate_parser = subparsers.add_parser(
        'recreate', help='Drop and create database tables'
    )
    recreate_parser.set_defaults(func=recreate)

    migration_parser = subparsers.add_parser(
        'migration', help='Manage migration'
    )
    migration_parser.add_argument(
        "migration_action", type=str, help="Action to perform",
        choices=['create', 'run', 'rollback']
    )
    migration_parser.add_argument(
        "migration_name", type=str, help="Name of the migration"
    )
    migration_parser.set_defaults(func=migration)

    args = parser.parse_args()
    args.func(args)


def main():
    """Main entry point for the script
    """
    execute_on_args()


if __name__ == "__main__":
    main()
