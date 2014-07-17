-- select *
-- from save_data
-- where date_ between '2013-05-09' and '2013-05-09'
-- and time_ between '17:30:00.000' and '17:59:00.000'
-- and message ilike '%java%'
-- order by date_ asc, time_ asc, log_id asc
-- 

select *
from obj_model
where date_ between '2013-06-06' and '2013-06-06'
and time_ between '16:00:00.000' and '17:00:00.000'
and message like 'java.lang.NullPointerException%'
and category = 'issue'
order by date_ asc, time_ asc, log_id asc
