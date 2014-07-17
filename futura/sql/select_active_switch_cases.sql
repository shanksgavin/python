-- Selecting Active Switch Cases
select casenum, casestatus, repowereddate, startdate, enddate, datestrt, timestrt, dateend, timeend
from cases
where enddate != repowereddate
and casestatus not in ('Closed', 'Predicted Closed', 'Predicted')
-- or enddate is NULL
order by casenum asc