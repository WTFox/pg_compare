"""

| '_ \ / _` |_____ / __/ _ \| '_ ` _ \| '_ \ / _` | '__/ _ \
| |_) | (_| |_____| (_| (_) | | | | | | |_) | (_| | | |  __/
| .__/ \__, |      \___\___/|_| |_| |_| .__/ \__,_|_|  \___|
|_|    |___/                          |_|

This is used to compare two databases. Takes two connection strings. One it
considers truth and another to test against it. Used to determine the difference
in two databases.
"""
import threading

import click

from . import config
from .models import PGDetails
from .vendor import blindspin


TITLE_TEXT = """\
This is used to compare two databases. Takes two connection strings. One it
considers truth and another to test against it. Used to determine the difference
in two databases.
"""


def initialize():
    """ Initial processing before the comparisons begin. """
    print_welcome_text()
    check_for_connection_strings()

    config.truth_db = PGDetails(config.truth_db_conn_string)
    config.test_db = PGDetails(config.test_db_conn_string)

    message = "Retrieving details for all tables. This could take awhile... "
    click.secho(message, fg="yellow", nl="")
    with blindspin.spinner():
        load_table_details_for_both_dbs(config.truth_db, config.test_db)

    click.secho("OK", fg="green")
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


def check_for_connection_strings():
    """ Checks to see if the user passed in connection strings.
    Prompts for connection strings if they do not exist.
    """
    truth_conn_str = config.truth_db_conn_string
    test_conn_str = config.test_db_conn_string
    if not all([truth_conn_str, test_conn_str]):
        prompt_for_conn_strings()

    return


def prompt_for_conn_strings():
    """ Prompts user to put in connection strings. """
    click.echo("Please input the needed connection strings. Without surrounding quotes.")
    config.truth_db_conn_string = click.prompt("Database to consider TRUTH: ")
    config.test_db_conn_string = click.prompt("Database to consider TEST: ")
    return


def load_table_details_for_both_dbs(*databases):
    """ Load all needed data from both databases into memory. """
    threads = []
    for db in databases:
        process = threading.Thread(target=db.get_details_for_tables)
        process.start()
        threads.append(process)

    # We now pause execution on the main thread by 'joining' all of our started threads.
    # This ensures that each has finished processing the urls.
    for process in threads:
        process.join()

    return
