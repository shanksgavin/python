-- Creates a function to show case summary info between dates WITHOUT major event days
create or replace function case_summary_from_to_dates(_start text, _end text, _tmed double precision) 
returns table (total_cases bigint, total_custouts double precision, total_cust_hours float, total_saidi float) as
$$
BEGIN
	-- TODO: Check for parameter values before executing
	-- TODO: If NOT EXIST then set default values
	
	-- Case Summary Totals Excluding Major Event Days
	if exists(select * from information_schema.tables
		where table_catalog = CURRENT_CATALOG
		and table_schema = CURRENT_SCHEMA
		and table_name = 'saidi_daily_values')
	then
		return query
		select count(casenum),
			sum(custout),
			sum((enddate::float/3600000)-(startdate::float/3600000)), -- Calculating Case Duration converted to Hours
			sum((((enddate::float/60000)-(startdate::float/60000))*custout)/22459) -- Calculating SAIDI
		from cases
		where datestrt between to_date(_start::text,'YYYY-MM-DD') and to_date(_end::text,'YYYY-MM-DD')
		and casestatus = 'Closed'
		and enddate-startdate > 300000
		having sum((((enddate::float/60000)-(startdate::float/60000))*custout)/22459) > 0 
		and sum((((enddate::float/60000)-(startdate::float/60000))*custout)/22459) < _tmed;
	else
		raise notice 'TABLE DOES NOT EXIST: saidi_daily_values';
	end if;
	
END;
$$
language 'plpgsql';
