select count(phase) :: int
from casescustomers
where casenum in (select casenum from cases where deleted = '0' and casestatus IN ('CauseFound', 'CauseUnknown', 'Predicted') order by casenum desc)
