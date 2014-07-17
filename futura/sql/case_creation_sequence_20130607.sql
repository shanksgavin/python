-- select *
-- from audit_cases
-- where casenum = '130606-O0116'
-- order by stamp asc

select *
from audit_cases
where calls like '%130607-C0012%'
order by stamp asc