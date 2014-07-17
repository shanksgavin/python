SELECT n.nspname as "Schema",  c.relname AS datname,  
CASE c.relkind 
    WHEN 'r' THEN 'table' 
    WHEN 'v' THEN 'view' 
    WHEN 'i' THEN 'index' 
    WHEN 'S' THEN 'sequence' 
    WHEN 's' THEN 'special' 
END as "Type",  u.usename as "Owner", 
(SELECT obj_description(c.oid, 'pg_class')) AS comment  
FROM pg_catalog.pg_class c 
LEFT JOIN pg_catalog.pg_user u ON u.usesysid = c.relowner 
LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace 
WHERE n.nspname='public' AND c.relkind IN ('r','') 
AND n.nspname NOT IN ('pg_catalog', 'pg_toast', 'information_schema')
ORDER BY datname ASC 