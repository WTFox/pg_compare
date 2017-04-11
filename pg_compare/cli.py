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
from .utils import initialize


config.available_tests = compare_functions.available_tests()


@click.group()
def cli():
    return


@cli.command()
@click.option('-t', '--total', help='Examine all items.', is_flag=True)
@click.option('-s', '--select', type=click.Choice(config.available_tests), multiple=True)
@click.option('-o', '--outfile', help="File to use as csv report")
def diff(total, select, outfile):
    initialize()
    if outfile:
        config.outfile = outfile

    if total:
        compare_functions.run(config.available_tests)
        return

    if select:
        compare_functions.run(select)
        return

    return


if __name__ == '__main__':
    cli()
