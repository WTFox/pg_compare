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
import click

import compare_functions
from . import config
from .utils import initialize, prompt_for_conn_strings, transform_conn_string


config.available_tests = compare_functions.available_tests()


@click.command()
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
def cli(truthdb, testdb, everything, select, outfile):
    """ This is used to compare two databases. Takes two connection strings. One it
    considers truth and another to test against it. Used to determine the difference
    in two databases.
    """
    config.outfile = outfile
    if not all([truthdb, testdb]):
        prompt_for_conn_strings()

    config.truth_db_config = transform_conn_string(truthdb)
    config.test_db_config = transform_conn_string(testdb)

    initialize()
    if select:
        compare_functions.run(select)
    else:
        compare_functions.run(config.available_tests)

    click.secho("\nfin ⭐️\n", color="cyan")

    return


if __name__ == '__main__':
    cli()
