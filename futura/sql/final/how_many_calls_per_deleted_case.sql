select distinct(customer), count(customer)
from casescustomers
where deleted = 't'
group by customer
order by count desc