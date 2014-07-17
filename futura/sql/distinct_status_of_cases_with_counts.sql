select distinct(status), count(status)
from cases
--where deleted = '0'
group by (status)
order by status