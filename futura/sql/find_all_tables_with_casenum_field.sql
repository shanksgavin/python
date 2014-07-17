select cls.relname,typ.typname,att.attname
from pg_attribute att
left join pg_class cls on cls.oid = att.attrelid
left join pg_type typ on typ.oid = att.atttypid
where att.attname = 'cis_location'  -- use cls.relname = '%' to find a table
order by cls.relname asc