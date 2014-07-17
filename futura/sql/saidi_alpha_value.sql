-- This script utilizes the saidi_daily_values(text, text) function currently, only in the wiregrass_2_2_0_84 db on fta_williamg
-- select saidi_daily_values_updated('2010-01-01','2014-12-31'); --Starting Year, Ending Year
select avg(nat_log_saidi) as saidi_alpha, 
	stddev(nat_log_saidi) as saidi_beta, 
	exp(avg(nat_log_saidi)+(2.5*stddev(nat_log_saidi))) as tmed -- tmed is currently inaccurate as the epsilon value needs to be identified and added at beginning of this line
from saidi_daily_values
where datestrt between '2013-01-01' and '2013-12-31';