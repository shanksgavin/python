select distinct(casestatus), count(casestatus)
from cases
group by (casestatus)
order by casestatus asc