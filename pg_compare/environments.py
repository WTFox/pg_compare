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
import os


# Disable spinner
PGCOMPARE_NO_SPIN = os.environ.get('PGCOMPARE_NO_SPIN')

# Disable concurrency
PGCOMPARE_NO_ASYNC = os.environ.get('PGCOMPARE_NO_ASYNC')

# Disable fun stuff on windows.
if os.name == 'nt':
    PGCOMPARE_NO_SPIN = True
