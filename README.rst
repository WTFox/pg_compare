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

``pg-compare --help``

Built With
----------

-  `click`_ - The web framework used
-  `psycopg2`_ - Dependency Management

Authors
-------

-  **Anthony Fox** - *Initial work* - `wtfox`_

Todos
-----

-  [ ] Add tests!!! :(

.. _click: http://www.dropwizard.io/1.0.2/docs/
.. _psycopg2: https://maven.apache.org/
.. _wtfox: https://github.com/wtfox