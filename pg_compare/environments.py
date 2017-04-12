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
PG_NO_SPIN = os.environ.get('PG_NO_SPIN')

# Disable concurrency
PG_NO_ASYNC = os.environ.get('PG_NO_ASYNC')

# Disable stuff on windows.
if os.name == 'nt':
    PG_NO_SPIN = True
