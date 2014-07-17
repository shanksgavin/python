-- select elementid, element, phase, casenum, custout, datestrt, casestatus, assigned, calls, totalcustdownstream, feeder, createdby, custhours 
select *
from cases 
where deleted = '0' 
and casestatus IN ('CauseFound', 'CauseUnknown', 'Predicted') 
order by casenum desc