-- select *
-- from save_data
-- where date_ between '2013-05-09' and '2013-05-09'
-- and time_ between '17:30:00.000' and '17:59:00.000'
-- and message ilike '%java%'
-- order by date_ asc, time_ asc, log_id asc
-- 

select *
from oms_logfiles.omslogs
where date_ between '2014-01-03' and '2014-01-03'
and time_ between '08:00:00.000' and '13:00:00.000'
and message ilike '%servicelink%'
-- and category = 'unknown'
order by date_ asc, time_ asc, log_id asc
