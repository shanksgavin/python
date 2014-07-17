-- select *
-- from vw_console_logs
-- where date_ between '2013-06-17' and '2013-06-17'
-- and time_ between '14:44:00' and '14:45:00'
-- or message like '%130617-O0062'
-- order by date_ desc, time_ desc, log_id asc
-- limit 2000

select *
from vw_console_logs
where date_ = '2013-06-20'
and time_ between '11:19' and '11:21'
and category != '[0]'
order by date_ asc, time_ asc, log_id asc