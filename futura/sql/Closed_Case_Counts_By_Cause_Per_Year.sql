-- select distinct(cause) as cause, casestatus, count(cause) as cause_counts
-- from cases
-- where datestrt
-- between '2011-01-01' and '2011-12-31'
-- and cause in (select distinct(cause) as cause from cases)
-- and deleted = 'f'
-- group by cause, casestatus
-- order by casestatus, cause asc;

select distinct(cause) as cause, count(cause) as cause_counts
from cases
where datestrt
between '2011-01-01' and '2011-12-31'
and casestatus in ('Closed', 'CLOSED')
and deleted = 'f'
and repowereddate <> startdate
group by cause
order by cause asc;