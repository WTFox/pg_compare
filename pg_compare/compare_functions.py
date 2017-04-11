"""
| '_ \ / _` |_____ / __/ _ \| '_ ` _ \| '_ \ / _` | '__/ _ \
| |_) | (_| |_____| (_| (_) | | | | | | |_) | (_| | | |  __/
| .__/ \__, |      \___\___/|_| |_| |_| .__/ \__,_|_|  \___|
|_|    |___/                          |_|

This is used to compare two databases. Takes two connection strings. One it
considers truth and another to test against it. Used to determine that both
databases are the same.

"""
import inspect
import sys

import click

from .config import config
from .reports import ErrorReport
from .sqls import INDEXNAME_SELECT, MAX_PK_SELECT


error_report = ErrorReport()


def available_tests():
    test_funcs = []
    funcs = inspect.getmembers(sys.modules[__name__], inspect.isfunction)
    for f_name, f_pointer in funcs:
        if f_name.startswith('pgcompare_'):
            test_funcs.append(f_name.split('pgcompare_')[1])

    return test_funcs


def run(test_names):
    funcs = dict(inspect.getmembers(sys.modules[__name__], inspect.isfunction))
    for test_name in test_names:
        click.echo("Comparing {}... ".format(test_name), nl="")

        func_name = "pgcompare_{}".format(test_name)

        if funcs.get(func_name)():
            click.secho("OK", fg="green")
        else:
            click.secho("FAIL", fg="red")

    error_report.build_report()
    return


def pgcompare_catalogs():
    """ Do the catalogs of each database match?
    """
    success = True
    if config.truth_db.catalog != config.test_db.catalog:
        error_report.log('Catalog', 'Catalogs do not match')
        success = False

    return success


def pgcompare_tables():
    """ Do all the tables in truth exist in test (hint: look at pg_catalog.pg_tables)?
    """
    success = True
    for table in config.truth_db.tables:
        if table not in config.test_db.tables:
            success = False
            error_report.log('Table', 'Table: {} is not in test db.'.format(table.name))

    return success


def pgcompare_rowcounts():
    """ For every table in truth, does it have the same count in test?
    """
    success = True
    for table in config.truth_db.tables:
        truth_rowcount = getattr(table, 'rowcount', None)
        test_table = config.test_db.get_table_by_name(table.name)
        test_rowcount = getattr(test_table, 'rowcount', None)

        if truth_rowcount == 0 and test_rowcount == 0:
            continue

        if truth_rowcount != test_rowcount or not all([truth_rowcount, test_rowcount]):
            message = 'Rowcount {} for {} differs in test db ({})'
            error_report.log('RowCount', message.format(table.rowcount, table.name, test_rowcount))
            success = False

        return success


def pgcompare_columns():
    """ For every table in truth, does it have the same columns in test?
    """
    success = True
    for table in config.truth_db.tables:
        truth_columns = set(sorted(table.columns))
        test_table = config.test_db.get_table_by_name(table.name)
        if not test_table:
            continue

        test_columns = set(sorted(test_table.columns))
        if truth_columns != test_columns:
            success = False
            for missing_col in truth_columns ^ test_columns:
                message = 'Col {} does not exist in test db.'
                error_report.log('Column', message.format(missing_col))

    return success


def pgcompare_indexes():
    """ For every index in truth, does the index exist in test (pg_catalog.pg_indexes)
    """
    success = True
    with config.truth_db.executor(INDEXNAME_SELECT) as truth_result:
        indexes_in_truth = set([x[0] for x in truth_result.fetchall()])

    with config.test_db.executor(INDEXNAME_SELECT) as test_result:
        indexes_in_test = set([x[0] for x in test_result.fetchall()])

    if indexes_in_truth != indexes_in_test:
        success = False
        for missing_idx in indexes_in_truth ^ indexes_in_test:
            message = 'Index {} does not exist in test db.'
            error_report.log('Index', message.format(missing_idx))

    return success


def pgcompare_pks():
    """ For the primary key column in each table, if it's an int does the max of it on truth = max on test?
    """
    success = True
    for table in config.truth_db.tables:
        test_table = config.test_db.get_table_by_name(table.name)

        if not hasattr(table, 'name') or not hasattr(table, 'primary_key'):
            continue

        if not hasattr(test_table, 'name') or not hasattr(test_table, 'primary_key'):
            continue

        if not table.primary_key and not test_table.primary_key:
            continue

        if table.primary_key != test_table.primary_key:
            success = False
            message = 'PK {} in {} does not match pk in test db, {}'
            error_report.log('PK', message.format(table.primary_key, table.name, test_table.primary_key))

        if table.primary_key_type != test_table.primary_key_type:
            success = False
            message = 'PK type {} in {} does not match pk type in test db, {}'
            error_report.log('PK', message.format(table.primary_key, table.name, test_table.primary_key))

        with config.truth_db.executor(MAX_PK_SELECT % (table.primary_key, table.name)) as truth_result:
            max_pk = truth_result.fetchone()

        with config.test_db.executor(MAX_PK_SELECT % (test_table.primary_key, test_table.name)) as test_result:
            max_test_pk = test_result.fetchone()

        if not all([max_pk, max_test_pk]) or max_pk != max_test_pk:
            success = False
            message = 'Max PK {} in {} does not match max pk type in test db, {}'
            error_report.log('PK', message.format(max_pk, table.name, max_test_pk))

    return success


if __name__ == '__main__':
    pass