select distinct(message) as failed_cases, count(message)
from vw_console_logs
where message like 'SetCase failed%'
group by message
order by message desc