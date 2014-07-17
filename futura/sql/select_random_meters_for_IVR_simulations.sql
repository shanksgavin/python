select meter 
from meterbase
order by random()*(select count(meter) from meterbase) --total number of meters in table, ex: 22464
limit 200
