-- Uncomment where statement when looking for a specific date
select calldate, calltime, count(ticketnum)
from calls
--where calldate = '2014-04-24'
group by calldate, calltime
order by calldate, calltime asc