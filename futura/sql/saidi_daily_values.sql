﻿-- Creates a function to be used in separate sql which supplies the years to have the Alpha, Beta, & Tmed Calculated
create or replace function saidi_daily_values(_start text, _end text) returns void as
$$
BEGIN
	-- TODO: Check for parameter values before executing
	-- TODO: If NOT EXIST then set default values
	if not exists(select * from information_schema.tables
		where table_catalog = CURRENT_CATALOG
		and table_schema = CURRENT_SCHEMA
		and table_name = 'saidi_daily_values')
	then
		create table saidi_daily_values as
		select datestrt,
			count(casenum) as daily_case_total,
			sum(custout) as total_custouts,
			sum((enddate::float/60000)-(startdate::float/60000)) as duration_mins, -- Calculating Case Duration converted to Minutes
			sum((((enddate::float/60000)-(startdate::float/60000))*custout)/22459) as daily_saidi, -- Calculating SAIDI
			ln(sum((((enddate::float/60000)-(startdate::float/60000))*custout)/22459)) as nat_log_saidi
		from cases
		where datestrt between to_date(_start,'YYYY-MM-DD') and to_date(_end,'YYYY-MM-DD')
		and casestatus = 'Closed'
		and enddate-startdate > 300000
		group by datestrt
		having sum((((enddate::float/60000)-(startdate::float/60000))*custout)/22459) > 0
		order by datestrt asc;
		raise notice 'CREATED: saidi_daily_values';
	else
		-- Drop table in case of schema change
		drop table saidi_daily_values;
		raise notice 'DROPPED: saidi_daily_values';

		-- Recreate Table
		create table saidi_daily_values as
		select datestrt,
			count(casenum) as daily_case_total,
			sum(custout) as total_custouts,
			sum((enddate::float/60000)-(startdate::float/60000)) as duration_mins, -- Calculating Case Duration converted to Minutes
			sum((((enddate::float/60000)-(startdate::float/60000))*custout)/22459) as daily_saidi, -- Calculating SAIDI
			ln(sum((((enddate::float/60000)-(startdate::float/60000))*custout)/22459)) as nat_log_saidi
		from cases
		where datestrt between to_date(_start::text,'YYYY-MM-DD') and to_date(_end::text,'YYYY-MM-DD')
		and casestatus = 'Closed'
		and enddate-startdate > 300000
		group by datestrt
		having sum((((enddate::float/60000)-(startdate::float/60000))*custout)/22459) > 0
		order by datestrt asc;
		raise notice 'CREATED: saidi_daily_values';
		
	end if;
	
END;
$$
language 'plpgsql';

-- select saidi_daily_values();
-- drop function saidi_daily_values();