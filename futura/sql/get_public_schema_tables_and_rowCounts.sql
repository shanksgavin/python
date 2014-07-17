SELECT c.relname as tblname, c.reltuples as tblRowCount
FROM pg_catalog.pg_class c
LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
WHERE n.nspname='public' AND c.relkind IN ('r','')
AND n.nspname NOT IN ('pg_catalog', 'pg_toast', 'information_schema')
ORDER BY c.reltuples DESC, c.relname ASC