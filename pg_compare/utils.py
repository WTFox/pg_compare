"""

| '_ \ / _` |_____ / __/ _ \| '_ ` _ \| '_ \ / _` | '__/ _ \
| |_) | (_| |_____| (_| (_) | | | | | | |_) | (_| | | |  __/
| .__/ \__, |      \___\___/|_| |_| |_| .__/ \__,_|_|  \___|
|_|    |___/                          |_|

This is used to compare two databases. Takes two connection strings. One it
considers truth and another to test against it. Used to determine the difference
in two databases.
"""

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

    click.secho("Retrieving details for all tables. This could take awhile... ", fg="yellow", nl="")
    with blindspin.spinner():
        load_table_details_for_both_dbs(config.truth_db, config.test_db)

    click.secho("OK", fg="green")
    return


def print_welcome_text():
    output = click.style('*' * 80, fg="cyan")
    output += '\n\t\t\t'
    output += click.style("=== PG-COMPARE ===\n\n", fg="yellow", bold=True)
    output += click.style(TITLE_TEXT, fg="cyan")
    output += '\n'
    output += click.style('*' * 80, fg="cyan")
    click.echo(output)


def prompt_for_conn_strings():
    config.truth_db_conn_string = click.prompt("Truth connection string")
    config.test_db_conn_string = click.prompt("Test connection string")
    return


def load_table_details_for_both_dbs(*databases):
    for db in databases:
        db.get_details_for_tables()
    return


