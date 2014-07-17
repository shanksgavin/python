-- select *
-- from calls
-- where deleted = 'f'
-- and calldate between '2013-04-16' and '2013-05-10'

-- delete from calls 
-- where deleted = 'f'
-- and calldate between '2013-04-16' and '2013-05-10'

select casescustomers.*, cases.casenum
from casescustomers
join cases
on casescustomers.casenum = cases.casenum
where cases.deleted = 'f'
and cases.datestrt between '2013-04-16' and '2013-05-10'
and cases.dateend between '2013-04-16' and '2013-05-10'

-- delete from casescustomers
-- where casenum in (select casenum from cases where deleted = 'f' and cases.datestrt between '2013-04-16' and '2013-05-10' and cases.dateend between '2013-04-16' and '2013-05-10')

-- delete from cases
-- where deleted = 'f' and cases.datestrt between '2013-04-16' and '2013-05-10' and cases.dateend between '2013-04-16' and '2013-05-10'