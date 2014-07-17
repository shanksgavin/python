select distinct(customer), count(customer)
from casescustomers
where deleted = 'f'
group by customer
order by count desc