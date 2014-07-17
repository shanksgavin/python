select customer, elementid, count(elementid)
from calls
group by customer, elementid
order by count desc, customer, elementid asc