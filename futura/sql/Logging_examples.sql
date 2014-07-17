-- select *
-- from omsclient
-- where message ilike 'Automation%'
-- order by date_ desc, time_ desc;
-- 

-- select *
-- from omsclient
-- where date_ = '2013-05-08'
-- and time_ = '14:36:59.74';

select *
from obj_model
where category = 'issue'
and date_ = '2013-05-08'
order by date_ desc, time_ desc, log_id asc;