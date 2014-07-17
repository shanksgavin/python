select distinct(casenum) as casenum, count(customer) as customer
from casescustomers
where deleted = 'f' 
and casenum like '______-O____'
group by casenum
order by customer DESC, casenum DESC