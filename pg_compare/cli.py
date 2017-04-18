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
import logging
import sys

import click
import click_log

import compare_functions
from . import config
from .utils import initialize, prompt_for_conn_strings, transform_conn_string, calculate_elapsed_time


config.available_tests = compare_functions.available_tests()


@click.command()
@click_log.init('pg-compare')
@click.option('-a', '--truthdb',
              help='Connection string for database to consider truth.')
@click.option('-b', '--testdb',
              help='Connection string for database to test.')
@click.option('-e', '--everything', is_flag=True,
              help='Run all comparisons.')
@click.option('-s', '--select', type=click.Choice(config.available_tests), multiple=True,
              help="Select specific comparisons to run.")
@click.option('-o', '--outfile', type=click.Path(writable=True, dir_okay=False),
              help="Specify a csv file to be created for failed comparisons.")
@click.option('-v', '--verbosity', count=True,
              help="Specify verbosity level")
def cli(truthdb, testdb, everything, select, outfile, verbosity):
    """ This is used to compare two databases. Takes two connection strings. One it
    considers truth and another to test against it. Used to determine the difference
    in two databases.
    """
    verbosity_mapping = {
        1: "ERROR",
        2: "WARNING",
        3: "INFO"
    }
    config.log = logging.getLogger('pg-compare')
    config.log.setLevel(verbosity_mapping.get(verbosity, "ERROR"))
    config.outfile = outfile
    if not all([truthdb, testdb]):
        prompt_for_conn_strings()

    config.truth_db_config = transform_conn_string(truthdb)
    config.test_db_config = transform_conn_string(testdb)

    initialize()
    if select:
        result = compare_functions.run(select)
    else:
        result = compare_functions.run(config.available_tests)

    message = "\nfin ⭐️\n"
    config.log.info(message)

    sys.stdout.write("{} - ".format(calculate_elapsed_time()))

    if result:
        sys.stdout.write("OK\n")
        sys.exit(0)
    else:
        sys.stdout.write("FAIL\n")
        sys.exit(1)


if __name__ == '__main__':
    cli()
