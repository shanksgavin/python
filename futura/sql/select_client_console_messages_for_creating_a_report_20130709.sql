-- select *
-- from omsclient_20130709_140031839000
-- where date_ = '2013-06-07'
-- and time_ between '16:00' and '16:00:49.450'
-- order by date_ asc, time_ asc, log_id asc

select *
from vw_console_logs
where 
--message ilike '%130709-C0237%' and 
date_ = '2013-07-10' and 
time_ between '10:28' and '10:29' -- 10:31:30
order by date_ asc, time_ asc, log_id asc