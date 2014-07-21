-- Select all audit tables with data only
-- Empty tables indicate no data has changed
SELECT relname as table_name
FROM pg_stat_user_tables 
WHERE schemaname = 'oms_audits'
GROUP BY relname, n_live_tup
HAVING n_live_tup > 0
ORDER BY n_live_tup DESC;