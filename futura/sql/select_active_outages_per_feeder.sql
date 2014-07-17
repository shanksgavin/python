-- produces unique feeders with predicted or confirmed case counts
select feeder, casestatus, phase, count(case_num) as case_total, sum(custout_sum) as custout_total
from active_outages_by_feeder_with_counts
group by feeder, phase, casestatus
order by feeder asc, casestatus asc, phase asc

-- QUERY BELOW IS USED TO BUILD THE VIEW USED IN ABOVE QUERY                     --
-- full code is commented in case it is needed to recreate view for above query  --

-- View: active_outages_by_feeder_with_counts

-- DROP VIEW active_outages_by_feeder_with_counts

-- CREATE OR REPLACE VIEW active_outages_by_feeder_with_counts AS
-- 	select feeder, phase, casestatus, casenum as case_num, custout as custout_sum
-- 	from cases as c
-- 	where deleted = 'f'
-- 	and casestatus not ilike '%closed%'
-- 
-- 	UNION
-- 
-- 	select feeder, phase, casestatus, casenum as case_num, 
-- 		case totalcustdownstream  when 0  then 1 else totalcustdownstream end as custout_sum
-- 	from callbundles;
-- 
-- ALTER TABLE active_outages_by_feeder_with_counts OWNER TO postgres;
-- GRANT ALL ON TABLE active_outages_by_feeder_with_counts TO postgres;
-- COMMENT ON VIEW active_outages_by_feeder_with_counts IS 'Report: Active Outages By Feeder With Counts';