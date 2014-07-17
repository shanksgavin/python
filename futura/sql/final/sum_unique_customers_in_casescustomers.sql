-- select distinct(customer), count(customer)
-- from casescustomers
-- group by customer
-- order by count desc

select *
from calls
limit 10

-- select distinct(elementid), count(elementid)
-- from calls
-- where elementid != ''
-- group by elementid
-- order by count desc
-- limit 10

-- select *
-- from customers
-- where elementid = 'MB-326201024414'

-- select *
-- from customers
-- where elementid in (
-- select distinct(elementid)
-- from calls
-- where elementid != ''
-- group by elementid
-- limit 10
-- )
