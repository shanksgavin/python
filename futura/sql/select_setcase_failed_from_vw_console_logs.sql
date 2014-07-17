select *
from vw_console_logs
where message like 'SetCase failed%'
order by date_ desc, time_ desc, log_id asc