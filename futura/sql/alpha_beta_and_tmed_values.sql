-- This script utilizes the saidi_daily_values(text, text) function currently, only in the wiregrass_2_2_0_84 db on fta_williamg
/*
 * Uncomment line below to recalculate the daily SAIDI values for a given time period
 * Understand that executing the function will drop the existing table and recreate
 
   select saidi_daily_values('2011-01-01','2014-01-31'); --Starting Year, Ending Year

 */
select sum(daily_case_total) as total_cases,
	sum(daily_saidi) as total_daily_saidi,
	avg(nat_log_saidi) as saidi_alpha, 
	stddev(nat_log_saidi) as saidi_beta, 
	exp(avg(nat_log_saidi)+(2.5*stddev(nat_log_saidi))) as tmed -- tmed is currently inaccurate as the epsilon value needs to be identified and added at beginning of this line
from saidi_daily_values
where datestrt between '2014-01-01' and '2014-01-22';

-- select *
-- from saidi_daily_values
-- where datestrt between '2014-01-01' and '2014-01-22';