select distinct(casenum) as casenum, count(casenum)
from cases
where deleted = 'f'
and casenum like '______-O____'
group by casenum
order by count desc