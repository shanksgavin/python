select distinct(casestatus), count(casestatus)
from cases
where deleted = '0'
group by (casestatus)
order by casestatus asc