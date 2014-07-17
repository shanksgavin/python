select casenum, casestatus, to_char(to_timestamp(startdate/1000),'YYYY-MM-DD HH24:MI:SS.MS') as case_start, datestrt, timestrt,
to_char(to_timestamp(enddate/1000),'YYYY-MM-DD HH24:MI:SS.MS') as case_end, dateend, timeend,
(enddate::decimal/60000)-(startdate::decimal/60000) as duration_minutes
from cases
where datestrt between '2013-01-01' and '2013-12-31'
and casestatus ilike 'closed'
and deleted = False
and enddate-startdate > 300000
order by datestrt asc, timestrt asc