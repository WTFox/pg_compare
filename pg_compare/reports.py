# -*- coding: utf-8 -*-
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
    """ Object to keep track of errors occurred during the comparisons
    and build the end report, if needed.
    """
    def __init__(self):
        self.errors = []
        return

    def clear(self):
        """ Clean out all errors. """
        self.errors = []
        return

    def log(self, category, message):
        """ Log a new error. """
        self.errors.append(ErrorRecord(category, message))
        return

    def build_report(self):
        """ Triggers the report to be compiled and create the file
        if needed.
        """
        if len(self.errors) and config.outfile:
            config.log.info("Building report...")
            self._create_file(config.outfile)
            self._compile_report()

        return

    def _compile_report(self):
        """ Builds the report csv. """
        with click.open_file(config.outfile, "w") as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(['index', 'type', 'message'])
            for idx, error in enumerate(self.errors):
                csv_writer.writerow([idx, error.type, error.message])

        return

    @staticmethod
    def _create_file(filename):
        """ Creates the file if it doesn't exist already.
        Ignores stdout if a - is passed in.
        """
        if filename and filename != '-':
            if not os.path.exists(os.path.dirname(filename)):
                os.makedirs(os.path.dirname(filename))

        return

