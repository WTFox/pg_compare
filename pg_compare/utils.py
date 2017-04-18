# -*- coding: utf-8 -*-
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
import time

import click
from psycopg2 import ProgrammingError
from psycopg2.extensions import parse_dsn

from . import config
from .environments import PGCOMPARE_NO_SPIN, PGCOMPARE_NO_ASYNC
from .models import PGDetails
from .vendor.blindspin import spinner


TITLE_TEXT = """\
This is used to compare two databases. Takes two connection strings. One it
considers truth and another to test against it. Used to determine the difference
in two databases.
"""


if PGCOMPARE_NO_SPIN or PGCOMPARE_NO_ASYNC:
    @contextlib.contextmanager
    def spinner():
        yield


def initialize():
    """ Initial processing before the comparisons begin. """
    print_welcome_text()

    config.truth_db = PGDetails(**config.truth_db_config)
    config.test_db = PGDetails(**config.test_db_config)

    message = click.style("Retrieving details for all tables. This could take awhile... ", fg="yellow")
    config.log.info(message)
    with spinner():
        load_table_details_for_both_dbs(config.truth_db, config.test_db)

    # Clearing that status
    sys.stdout.write("\b")
    sys.stdout.flush()

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
        config.log.error(message)
        sys.exit(1)

    return conn_dict


def prompt_for_conn_strings():
    """ Prompts user to put in connection strings. """
    config.truth_db_conn_string = click.prompt("Database to consider TRUTH: ")
    config.test_db_conn_string = click.prompt("Database to consider TEST: ")
    return


def print_welcome_text():
    """ Outputs welcome text """
    output = '\n\t\t\t'
    output += click.style("=== PG-COMPARE ===\n\n", fg="yellow", bold=True)
    output += click.style(TITLE_TEXT)
    output += '\n'
    config.log.info(output)

    print_info_about_databases()
    return


def print_info_about_databases():
    """ Show the connection details of truth and test database """
    from tabulate import tabulate

    output = []
    displayed_keys = []
    for k, v in config.truth_db_config.items():
        output.append((k, v, config.test_db_config.get(k, '')))
        displayed_keys.append(k)

    for k, v in config.test_db_config.items():
        if k not in displayed_keys:
            output.append((k, config.truth_db_config.get(k, ''), v))
            displayed_keys.append(k)

    config.log.info(tabulate(output, headers=['', 'Truth Database', 'Test Database'], tablefmt="simple"))
    config.log.info('\n')
    return


def load_table_details_for_both_dbs(*databases):
    """ Load all needed data from both databases into memory. """

    if PGCOMPARE_NO_ASYNC:
        for db in databases:
            db.get_details_for_tables()

        return

    threads = []
    stop_event = threading.Event()
    initial_active_threads = threading.active_count()
    for db in databases:
        process = threading.Thread(target=db.get_details_for_tables)
        process.start()
        threads.append(process)

    while threading.active_count() > initial_active_threads:
        try:
            time.sleep(0.1)
        except (KeyboardInterrupt, SystemExit):
            stop_event.set()

        if stop_event.is_set():
            for db in databases:
                db._close_all()

            sys.exit(1)

    return


def calculate_elapsed_time():
    """ Calculates time the script took to execute. """
    end_time = time.time()
    seconds = end_time - config.start_time
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%d:%02d:%02d" % (h, m, s)
