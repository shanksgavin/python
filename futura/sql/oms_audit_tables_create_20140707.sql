-- Function: oms_audit_schema_create()

-- DROP FUNCTION oms_audit_schema_create();

CREATE OR REPLACE FUNCTION oms_audit_schema_create()
  RETURNS void AS
$BODY$
DECLARE v_table record;
begin
        -- Create Initial OMS Audit Schema
        -- Fail cleanly if already exists
        begin
                execute 'CREATE SCHEMA oms_audits';
                raise notice 'Created Schema: oms_audits';
        exception
                when duplicate_schema then
                        raise notice 'ERROR: OMS Audit Schema Already Exists';
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
                        raise notice 'WARN: OMS Audit Tables, Triggers, & Functions have been dropped';
        end;

        for v_table in select t.table_name as tbl
                from information_schema.tables t
                where t.table_schema = current_schema
                and t.table_type = 'BASE TABLE'
                and t.table_name not like 'new%'
                and t.table_name not like 'audit%'
                order by t.table_name asc
        LOOP
                --raise notice 'Create Audit Table from Existing Table';
                Execute 'create table oms_audits.audit_' || v_table.tbl || ' (LIKE public.' || v_table.tbl || ')';
                execute 'ALTER TABLE oms_audits.audit_' || v_table.tbl || ' ADD COLUMN audit_id serial NOT NULL';
                execute 'ALTER TABLE oms_audits.audit_' || v_table.tbl || ' ADD COLUMN audit_sql_action character(1) NOT NULL';
                execute 'ALTER TABLE oms_audits.audit_' || v_table.tbl || ' ADD COLUMN audit_stamp timestamp without time zone NOT NULL';
                execute 'ALTER TABLE oms_audits.audit_' || v_table.tbl || ' ADD COLUMN audit_user_id text NOT NULL';
                raise notice 'CREATED: Audit Table for %', v_table.tbl;
                --raise notice 'Create Function';
                execute 'CREATE OR REPLACE FUNCTION public.audit_' || v_table.tbl || '() RETURNS TRIGGER AS $usr_audit$
                                        BEGIN
                                            IF (TG_OP = ''DELETE'') THEN
                                                INSERT INTO oms_audits.audit_' || v_table.tbl || ' VALUES (OLD.*, DEFAULT, ''D'', now(), user);
                                                RETURN OLD;
                                            ELSIF (TG_OP = ''UPDATE'') THEN
                                                INSERT INTO oms_audits.audit_' || v_table.tbl || ' VALUES (NEW.*, DEFAULT, ''U'', now(), user);
                                                RETURN NEW;
                                            ELSIF (TG_OP = ''INSERT'') THEN
                                                INSERT INTO oms_audits.audit_' || v_table.tbl || ' VALUES (NEW.*, DEFAULT, ''I'', now(), user);
                                                RETURN NEW;
                                            END IF;
                                            RETURN NULL; -- result is ignored since this is an AFTER trigger
                                        END;
                                    $usr_audit$ LANGUAGE plpgsql';
                raise notice 'CREATED: Function for %', v_table.tbl;
                --raise notice 'Create Trigger';
                execute 'CREATE TRIGGER audit_' || v_table.tbl || '_trg AFTER INSERT OR UPDATE OR DELETE ON public.' || v_table.tbl || ' FOR EACH ROW EXECUTE PROCEDURE audit_' || v_table.tbl || '()';
                raise notice 'CREATED: Trigger for %', v_table.tbl;
                --raise notice 'Audit Table Created for: %', v_table.tbl;
        end loop;
        raise notice 'COMPLETED: OMS Audit Schema & Tables';
end;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION oms_audit_schema_create()
  OWNER TO postgres;
