"""
| '_ \ / _` |_____ / __/ _ \| '_ ` _ \| '_ \ / _` | '__/ _ \
| |_) | (_| |_____| (_| (_) | | | | | | |_) | (_| | | |  __/
| .__/ \__, |      \___\___/|_| |_| |_| .__/ \__,_|_|  \___|
|_|    |___/                          |_|

This is used to compare two databases. Takes two connection strings. One it
considers truth and another to test against it. Used to determine that both
databases are the same.

"""

SELECT_CATALOG = """\
    SELECT n.nspname as "Schema",
      c.relname as "Name",
      CASE c.relkind WHEN 'r' THEN 'table' WHEN 'v' THEN 'view' WHEN 'm' THEN 'materialized view' WHEN 'i' THEN 'index' WHEN 'S' THEN 'sequence' WHEN 's' THEN 'special' WHEN 'f' THEN 'foreign table' END as "Type",
      pg_catalog.pg_get_userbyid(c.relowner) as "Owner"
    FROM pg_catalog.pg_class c
         LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
    WHERE c.relkind IN ('r','v','m','S','f','')
          AND n.nspname <> 'pg_catalog'
          AND n.nspname <> 'information_schema'
          AND n.nspname !~ '^pg_toast'
      AND pg_catalog.pg_table_is_visible(c.oid)
    ORDER BY 1,2;
""".strip()

FIND_PK_COLUMN_SELECT = """\
    SELECT a.attname,
      format_type(a.atttypid, a.atttypmod) AS data_type
    FROM pg_index i
    JOIN pg_attribute a ON a.attrelid = i.indrelid
      AND a.attnum = ANY (i.indkey)
    WHERE i.indrelid = '%s' :: REGCLASS AND i.indisprimary;
""".strip()

COLUMN_SELECT = """\
    SELECT column_name
    FROM information_schema.columns
    WHERE table_name='%s';
""".strip()

ROWCOUNT_SELECT = "SELECT count(*) FROM %s;"

INDEXNAME_SELECT = "SELECT indexname FROM pg_catalog.pg_indexes;"

MAX_PK_SELECT = "SELECT %s FROM %s ORDER BY 1 DESC LIMIT 1;"


if __name__ == '__main__':
    pass
