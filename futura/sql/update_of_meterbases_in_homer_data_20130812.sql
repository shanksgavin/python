select *
from oms_logfiles.omslogs
where date_ = '2013-08-12'
and time_ between '11:23:50.0' and '11:24:05.0'
order by date_ asc, time_ asc, log_id desc