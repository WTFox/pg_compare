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
import time

from models import AttributeContainer


config = AttributeContainer()
config.truth_db_conn_string = None
config.test_db_conn_string = None
config.truth_db = None
config.test_db = None
config.outfile = None
config.available_tests = []
config.start_time = time.time()


if __name__ == '__main__':
    pass
