PG-COMPARE
==========

.. image:: https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg
    :target: https://saythanks.io/to/WTFox

---------------


A cli tool to compare two postgres databases. Given two databases, one
it considers truth and one to test against, pg-compare will compare the
following items and verify they’re identical on both databases. -
database catalogs - tables - columns in each table - indexes - primary
keys - row counts

Installing
~~~~~~~~~~

1. Clone this repo
2. ``pip install .``

To run it
~~~~~~~~~

::

    pg-compare --help
    Usage: pg-compare [OPTIONS]

    Options:
      -a, --all                       Run all comparisons.
      -s, --select [catalogs|columns|indexes|pks|rowcounts|tables]
                                      Select specific comparisons to run.
      -o, --outfile TEXT              Specify a csv file to be created for failed
                                      comparisons.
      --help                          Show this message and exit.


::

    pg-compare --all
    ********************************************************************************
                            === PG-COMPARE ===

    This is used to compare two databases. Takes two connection strings. One it
    considers truth and another to test against it. Used to determine the difference
    in two databases.

    ********************************************************************************
    Truth connection string: host='scranton1' dbname='manager_db' user='mscott' password='improv1!'
    Test connection string: host='scranton2' dbname='manage_db' user='dshrute' password='beetsBSG'
    Retrieving details for all tables. This could take awhile... OK
    Comparing catalogs... OK
    Comparing columns... OK
    Comparing indexes... OK
    Comparing pks... FAIL
    Comparing rowcounts... OK
    Comparing tables... OK

::

    pg-compare -s catalogs -s columns
    ********************************************************************************
                            === PG-COMPARE ===

    This is used to compare two databases. Takes two connection strings. One it
    considers truth and another to test against it. Used to determine the difference
    in two databases.

    ********************************************************************************
    Truth connection string: host='scranton1' dbname='manager_db' user='mscott' password='improv1!'
    Test connection string: host='scranton2' dbname='manage_db' user='dshrute' password='beetsBSG'
    Retrieving details for all tables. This could take awhile... OK
    Comparing catalogs... OK
    Comparing columns... OK

::

    pg-compare -s catalogs -s columns -o "path/to/file.csv"
    ********************************************************************************
                            === PG-COMPARE ===

    This is used to compare two databases. Takes two connection strings. One it
    considers truth and another to test against it. Used to determine the difference
    in two databases.

    ********************************************************************************
    Truth connection string: host='scranton1' dbname='manager_db' user='mscott' password='improv1!'
    Test connection string: host='scranton2' dbname='manage_db' user='dshrute' password='beetsBSG'
    Retrieving details for all tables. This could take awhile... OK
    Comparing catalogs... OK
    Comparing columns... FAIL
    Building report... OK

Built With
~~~~~~~~~~

-  `click`_ - The cli framework used
-  `psycopg2`_ - For postgres

Authors
~~~~~~~

-  **Anthony Fox** - *Initial work* - `wtfox`_

.. _click: http://www.dropwizard.io/1.0.2/docs/
.. _psycopg2: https://maven.apache.org/
.. _wtfox: https://github.com/wtfox