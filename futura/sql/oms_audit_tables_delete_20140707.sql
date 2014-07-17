-- Function: oms_audit_schema_delete()

-- DROP FUNCTION oms_audit_schema_delete();

CREATE OR REPLACE FUNCTION oms_audit_schema_delete()
  RETURNS void AS
$BODY$
DECLARE v_table record;
begin
        for v_table in select t.table_name as tbl
                from information_schema.tables t
                where t.table_schema = 'oms_audits'
                and t.table_type = 'BASE TABLE'
                and t.table_name not like 'new%'
                and t.table_name like 'audit_%'
                order by t.table_name asc
        LOOP
                execute 'DROP TABLE IF EXISTS oms_audits.' || v_table.tbl || ' CASCADE';
                execute 'DROP TRIGGER IF EXISTS ' || v_table.tbl || '_trg ON ' || substring(v_table.tbl from 7 for length(v_table.tbl)) || ' CASCADE';
                execute 'DROP FUNCTION IF EXISTS ' || v_table.tbl || '() CASCADE';
        -- return;
        -- exit;
        end loop;
        raise notice 'NOTICE: OMS Audit Tables, Triggers, & Functions have been dropped';
        -- Remove the OMS Audit Schema
        execute 'DROP SCHEMA IF EXISTS oms_audits CASCADE';
        raise notice 'NOTICE: OMS Audit Schema has been dropped.';
end;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION oms_audit_schema_delete()
  OWNER TO postgres;
