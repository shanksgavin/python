select casenum, casestatus, cause, datestrt, timestrt, dateend, timeend, custhours, totalcustdownstream, oldcustout, custout,
CASE WHEN totalcustdownstream = 0 
	THEN Null 
	ELSE EXTRACT(EPOCH FROM ((to_timestamp(dateend||' '||timeend,'YYYY-MM-DD HH24:MI:SS')-to_timestamp(datestrt||' '||timestrt,'YYYY-MM-DD HH24:MI:SS'))*totalcustdownstream))/60.0 END as calccusthours1, 
CASE WHEN custout = 0 
	THEN Null 
	ELSE EXTRACT(EPOCH FROM ((to_timestamp(dateend||' '||timeend,'YYYY-MM-DD HH24:MI:SS')-to_timestamp(datestrt||' '||timestrt,'YYYY-MM-DD HH24:MI:SS'))*custout))/60.0 END as calccusthoursCustout, 
EXTRACT(EPOCH FROM ((to_timestamp(dateend||' '||timeend,'YYYY-MM-DD HH24:MI:SS')-to_timestamp(datestrt||' '||timestrt,'YYYY-MM-DD HH24:MI:SS'))*custout)/22459)/60.0 as saidi
from cases
where datestrt between '2013-01-01' and '2013-12-31'
and casestatus = 'Closed'
order by datestrt asc, timestrt asc