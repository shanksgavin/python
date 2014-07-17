select *
from oms_logfiles.omslogs
where date_ between '2013-08-20' and '2013-08-26'
-- and time_ between '10:15:45.000' and '10:16:00.000'
and message ilike '%error%'
and message not ilike '%without error%'
-- and category = 'issue'
order by date_ asc, time_ asc, log_id asc
