"""

| '_ \ / _` |_____ / __/ _ \| '_ ` _ \| '_ \ / _` | '__/ _ \
| |_) | (_| |_____| (_| (_) | | | | | | |_) | (_| | | |  __/
| .__/ \__, |      \___\___/|_| |_| |_| .__/ \__,_|_|  \___|
|_|    |___/                          |_|

This is used to compare two databases. Takes two connection strings. One it
considers truth and another to test against it. Used to determine the difference
in two databases.
"""
import contextlib
import sys
import threading

import click
from psycopg2 import ProgrammingError, OperationalError
from psycopg2.extensions import parse_dsn

from . import config
from .environments import PG_NO_SPIN, PG_NO_ASYNC
from .models import PGDetails
from .vendor.blindspin import spinner


TITLE_TEXT = """\
This is used to compare two databases. Takes two connection strings. One it
considers truth and another to test against it. Used to determine the difference
in two databases.
"""


if PG_NO_SPIN:
    @contextlib.contextmanager
    def spinner():
        yield


def initialize():
    """ Initial processing before the comparisons begin. """
    print_welcome_text()

    config.truth_db = PGDetails(**config.truth_db_config)
    config.test_db = PGDetails(**config.test_db_config)

    message = "Retrieving details for all tables. This could take awhile... "
    click.secho(message, fg="yellow", nl="")
    with spinner():
        load_table_details_for_both_dbs(config.truth_db, config.test_db)

    click.secho("OK", fg="green")
    return


def transform_conn_string(conn_string):
    """ Transforms any valid connection string passed in to a dict and
    returns the dict. If the conn_string is invalid or not supported it
    echos that to stdout and exits the cli.

    Ex:
        'dbname=test user=postgres password=secret' ->
            {'password': 'secret', 'user': 'postgres', 'dbname': 'test'}

        "postgresql://someone@example.com/somedb?connect_timeout=10" ->
            {'host': 'example.com', 'user': 'someone', 'dbname': 'somedb', 'connect_timeout': '10'}
    """
    try:
        conn_dict = parse_dsn(conn_string)
    except ProgrammingError:
        message = "Invalid connection string: {}. Exiting.".format(conn_string)
        click.secho(message, fg="red")
        sys.exit(1)

    return conn_dict


def prompt_for_conn_strings():
    """ Prompts user to put in connection strings. """
    click.echo("Please input the needed connection strings.")
    config.truth_db_conn_string = click.prompt("Database to consider TRUTH: ")
    config.test_db_conn_string = click.prompt("Database to consider TEST: ")
    return


def print_welcome_text():
    """ Outputs welcome text """
    output = click.style('*' * 80, fg="cyan")
    output += '\n\t\t\t'
    output += click.style("=== PG-COMPARE ===\n\n", fg="yellow", bold=True)
    output += click.style(TITLE_TEXT, fg="cyan")
    output += '\n'
    output += click.style('*' * 80, fg="cyan")
    click.echo(output)
    return


def load_table_details_for_both_dbs(*databases):
    """ Load all needed data from both databases into memory. """

    if PG_NO_ASYNC:
        for db in databases:
            db.get_details_for_tables()
    else:
        threads = []
        for db in databases:
            process = threading.Thread(target=db.get_details_for_tables)
            process.start()
            threads.append(process)

        for process in threads:
            process.join()

    return
