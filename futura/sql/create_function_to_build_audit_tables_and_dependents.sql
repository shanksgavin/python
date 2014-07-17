-- DROP FUNCTION build_audit_tables();

CREATE OR REPLACE FUNCTION build_audit_tables() RETURNS integer AS $$
DECLARE
	tbl text;
	atbl text;
	atbls integer;
	col text;
	cnt integer;
	curdate date := current_date;
	SQL text;
BEGIN
	-- Perform Existence test then backup table if rowcount greater than zero
	EXECUTE 'SELECT COUNT(*) 
	FROM pg_catalog.pg_class c 
	LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace 
	WHERE n.nspname=''public'' 
	AND c.relname like ''audit_%''
	AND c.relkind IN (''r'','''') 
	AND n.nspname NOT IN (''pg_catalog'', ''pg_toast'', ''information_schema'')'
	INTO atbls;

	IF atbls > 0 THEN
		FOR atbl IN 
			SELECT c.relname 
			FROM pg_catalog.pg_class c 
			LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace 
			WHERE n.nspname='public' 
			AND c.relname like 'audit_%' 
			AND c.relkind IN ('r','') 
			AND n.nspname NOT IN ('pg_catalog', 'pg_toast', 'information_schema') 
			ORDER BY c.relname ASC 
		LOOP
		SQL := 'SELECT INTO cnt COUNT(*) FROM ' || atbl;
		EXECUTE SQL;
		IF cnt > 0 THEN
			RAISE NOTICE '***Backing up table %', atbl;
			-- RAISE NOTICE '   ' || to_char(curdate);
			SQL := 'SELECT * INTO ' || atbl || '_' || curdate || ' FROM ' || atbl;
			EXECUTE SQL;
		END IF;

		END LOOP;
	END IF;
	
	RAISE NOTICE 'Selecting OMS Tables to conduct audits';
	-- Start the process to build the audit tables in any database
	-- Developed for PostgreSQL 8.4
	FOR tbl IN 
		SELECT c.relname 
		FROM pg_catalog.pg_class c 
		LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace 
		WHERE n.nspname='public' 
		AND c.relkind IN ('r','') 
		AND n.nspname NOT IN ('pg_catalog', 'pg_toast', 'information_schema') 
		ORDER BY c.relname ASC
	LOOP

	-- Create a copy of each table then add Audit Columns
	RAISE NOTICE '***Building Audit Table on %', tbl;
	
	-- Then DROP table before recreating
	BEGIN
		SQL := 'DROP TABLE IF EXISTS audit_' || tbl;
		EXECUTE SQL;
	EXCEPTION WHEN plpgsql_error THEN
		-- Do nothing; Just skip
	END;
	-- Copy table into audit table then add audit columns
		BEGIN
			SQL := 'CREATE TABLE audit_' || tbl || ' AS SELECT * FROM ' || tbl;
			-- RAISE NOTICE 'SQL := %', SQL;
			EXECUTE SQL;
			SQL := 'TRUNCATE audit_' || tbl;
			EXECUTE SQL;
			SQL := 'ALTER TABLE audit_' || tbl || ' ADD COLUMN audit_id serial NOT NULL';
			EXECUTE SQL;
			SQL := 'ALTER TABLE audit_' || tbl || ' ADD COLUMN audit_sql_action character(1) NOT NULL';
			EXECUTE SQL;
			SQL := 'ALTER TABLE audit_' || tbl || ' ADD COLUMN audit_stamp timestamp without time zone NOT NULL';
			EXECUTE SQL;
			SQL := 'ALTER TABLE audit_' || tbl || ' ADD COLUMN audit_user_id text NOT NULL';
			EXECUTE SQL;
		EXCEPTION WHEN no_data_found THEN
			RAISE NOTICE 'No Data in table';
		END;
	END LOOP;

	RAISE NOTICE '***Building Audit Tables Completed.';
	RETURN 1;

END;
$$ LANGUAGE plpgsql;