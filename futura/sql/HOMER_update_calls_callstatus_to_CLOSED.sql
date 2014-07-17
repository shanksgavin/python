-- select distinct(callstatus), count(callstatus)
-- from calls
-- group by callstatus;

select *
from calls
where callstatus in ('closed', 'Closed');

-- update calls
-- set callstatus = 'CLOSED'
-- where callstatus in ('closed', 'Closed');