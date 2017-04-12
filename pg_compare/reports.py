"""
| '_ \ / _` |_____ / __/ _ \| '_ ` _ \| '_ \ / _` | '__/ _ \
| |_) | (_| |_____| (_| (_) | | | | | | |_) | (_| | | |  __/
| .__/ \__, |      \___\___/|_| |_| |_| .__/ \__,_|_|  \___|
|_|    |___/                          |_|

This is used to compare two databases. Takes two connection strings. One it
considers truth and another to test against it. Used to determine that both
databases are the same.

"""
import csv
import os
from collections import namedtuple

import click

from . import config

ErrorRecord = namedtuple('Error', 'type message')


class ErrorReport(object):
    def __init__(self):
        self.errors = []

    def clear(self):
        self.errors = []

    def log(self, type, message):
        self.errors.append(ErrorRecord(type, message))

    def build_report(self):
        if len(self.errors) and config.outfile:
            click.echo("Building report...", nl="")
            self._create_file(config.outfile)
            self._compile_report()
            click.secho("OK", fg="green")

    def _compile_report(self):
        with click.open_file(config.outfile, "w") as f:
            csvwriter = csv.writer(f)
            csvwriter.writerow(['index', 'type', 'message'])
            for idx, error in enumerate(self.errors):
                csvwriter.writerow([idx, error.type, error.message])

    @staticmethod
    def _create_file(filename):
        """ Creates the file if it doesn't exist already.
        Ignores stdout if a - is passed in.
        """
        if filename and filename != '-':
            if not os.path.exists(os.path.dirname(filename)):
                os.makedirs(os.path.dirname(filename))

        return

