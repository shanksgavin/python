select distinct(county), count(county)
from meterbase
--where county = ''
group by county
order by county asc