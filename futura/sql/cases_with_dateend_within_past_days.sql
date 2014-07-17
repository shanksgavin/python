select casenum, casestatus, datestrt, dateend, status
from cases
where dateend > NOW() - INTERVAL '35 DAY'
order by dateend, casenum desc