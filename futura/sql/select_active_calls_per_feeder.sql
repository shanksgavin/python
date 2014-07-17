-- produces unique feeders with active call counts
select distinct(feeder), phase, count(feeder) as calls
from meterbase
where meter in (select meter from calls where callstatus = 'ACTIVE')
group by feeder, phase
order by feeder asc

