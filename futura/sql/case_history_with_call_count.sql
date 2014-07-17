select distinct(casenum), count(casenum) call_cnt
from casescustomers
group by casenum
order by call_cnt desc