/*
 * Case Summary Details for the Last Month
 * This query provides the details only for the Case Details Section
 * at the very bottom of the Case Summary - Last Month Report
 * Created on January 22, 2014
 * Created by William Gavin
 */
select elementid as "Element Name",
	casenum as "Case Number",
	to_char(to_timestamp(startdate/1000), 'YYYY-MM-DD HH:MI') as "Start Date",
	-- datestrt || ' ' || to_char(timestrt, 'HH24:MI') as "Report Start Date",
	to_char(to_timestamp(enddate/1000), 'YYYY-MM-DD HH:MI') as "End Date",
	-- dateend || ' ' || to_char(timeend, 'HH24:MI') as "Report End Date",
	round((((enddate::float/3600000)-(startdate::float/3600000))*custout)::numeric, 2) as "Cust Hours"
from cases
where datestrt between '2013-12-01' and '2013-12-31'
-- or dateend between '2014-01-20' and '2014-01-22'
and casestatus = 'Closed'
order by startdate desc;