-- Creates a function to be used in separate sql which supplies the years to have the Alpha, Beta, & Tmed Calculated
create or replace function case_summary_from_to_dates(_start text, _end text, _tmed double precision) returns void as
$$
BEGIN
	-- TODO: Check for parameter values before executing
	-- TODO: If NOT EXIST then set default values

	-- Case Summary Totals Including Major Event Days
	if exists(select * from information_schema.tables
		where table_catalog = CURRENT_CATALOG
		and table_schema = CURRENT_SCHEMA
		and table_name = 'saidi_daily_values')
	then
		select datestrt,
			sum(custout) as total_custouts,
			sum((enddate::float/60000)-(startdate::float/60000)) as duration_mins, -- Calculating Case Duration converted to Minutes
			sum((((enddate::float/60000)-(startdate::float/60000))*custout)/22459) as daily_saidi, -- Calculating SAIDI
			ln(sum((((enddate::float/60000)-(startdate::float/60000))*custout)/22459)) as nat_log_saidi
		from cases
		where datestrt between to_date(_start,'YYYY-MM-DD') and to_date(_end,'YYYY-MM-DD')
		and casestatus = 'Closed'
		and enddate-startdate > 300000
		-- group by datestrt
		having sum((((enddate::float/60000)-(startdate::float/60000))*custout)/22459) > 0
		order by datestrt asc;
		-- raise notice 'CREATED: saidi_daily_values';
	else
		raise notice 'TABLE DOES NOT EXIST: saidi_daily_values';
	end if;
	
END;
$$
language 'plpgsql';
