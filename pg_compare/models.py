"""
| '_ \ / _` |_____ / __/ _ \| '_ ` _ \| '_ \ / _` | '__/ _ \
| |_) | (_| |_____| (_| (_) | | | | | | |_) | (_| | | |  __/
| .__/ \__, |      \___\___/|_| |_| |_| .__/ \__,_|_|  \___|
|_|    |___/                          |_|

This is used to compare two databases. Takes two connection strings. One it
considers truth and another to test against it. Used to determine that both
databases are the same.

"""
from collections import namedtuple
from contextlib import contextmanager

import psycopg2

from .sqls import SELECT_CATALOG, ROWCOUNT_SELECT, COLUMN_SELECT, FIND_PK_COLUMN_SELECT


Table = namedtuple("Table", "name rowcount columns primary_key primary_key_type")


class PGDetails(object):
    def __init__(self, conn_string):
        self.conn_string = conn_string
        self.conn = None
        self.cur = None
        self._table_details = None
        self._catalog = self._build_catalog()
        self._table_names = [row[1] for row in self._catalog if row[2] == 'table']

    @property
    def catalog(self):
        return self._catalog

    @property
    def tables(self):
        return self._table_details if self._table_details else self._table_names

    @contextmanager
    def executor(self, statement):
        _cur = self._get_cursor()
        _cur.execute(statement)
        results = _cur
        yield results
        self._close_all()

    def get_table_by_name(self, name):
        """ Given a table name found in truth, attempt to
        return that same table in test. If no table is
        found by that name, return None.
        """
        table_name = None
        if self._table_details:
            try:
                table_name = [x for x in self._table_details if x.name == name][0]
            except IndexError:
                pass

        return table_name

    def get_details_for_tables(self):
        """ Load all needed data into memory for comparisons.

        Retrieves:
            - Rowcounts
            - Columns per table
            - PK and PK type per table (if exists)
        """
        _tables = []
        cursor = self._get_cursor()
        for table_name in self._table_names:
            cursor.execute(ROWCOUNT_SELECT % table_name)
            _rowcount = cursor.fetchone()[0]

            cursor.execute(COLUMN_SELECT % table_name)
            _cols = [el[0] for el in cursor.fetchall()]

            cursor.execute(FIND_PK_COLUMN_SELECT % table_name)
            _pk_result = cursor.fetchone()
            _pk, _pk_type = _pk_result if _pk_result else (None, None)
            _table = Table(name=table_name, rowcount=_rowcount, columns=_cols, primary_key=_pk, primary_key_type=_pk_type)
            _tables.append(_table)

        self._close_all()
        self._table_details = _tables

    def _build_catalog(self):
        resultset = []
        with self.executor(SELECT_CATALOG) as result:
            resultset = result.fetchall()
        return resultset

    def _get_conn(self):
        return psycopg2.connect(self.conn_string)

    def _get_cursor(self):
        if not self.conn:
            self.conn = self._get_conn()
        return self.conn.cursor()

    def _close_all(self):
        if self.cur:
            self.cur.close()
            self.cur = None
        if self.conn:
            self.conn.close()
            self.conn = None


if __name__ == '__main__':
    pass

