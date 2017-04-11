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
import sys

from .config import config

# Inject vendored directory into system path.
v_path = os.path.sep.join([os.path.dirname(os.path.realpath(__file__)), 'vendor'])
sys.path.append(v_path)

from .cli import cli


if __name__ == '__main__':
    cli()
