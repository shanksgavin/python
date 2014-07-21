-- Randomly select account, cis_location, and customer name (with phase)
-- for testing UPN Account/CISLocation Mismatch among other tests
select c.account, m.cis_location, m.cis_location, c.customer, m.phase
from customers as c
Join meterbase as m
ON c.account = m.account
order by random()
limit 5