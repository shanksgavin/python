-- Can only be used with oms_logfiles schema
-- and insert_oms_logs.py

select date_, message
from oms_logfiles.omslogs
where message like '%Setting Key does not exist:%'
group by date_, message
order by date_, message asc