select casenum,
	to_char(to_timestamp(startdate/1000), 'YYYY-MM-DD HH24:MI') as "Start",
	-- datestrt || ' ' || to_char(timestrt, 'HH24:MI') as "Report Start",
	to_char(to_timestamp(enddate/1000), 'YYYY-MM-DD HH24:MI') as "End",
	-- dateend,
	elementname as "Element Name",
	assignedto as "Crew",
	round(((enddate::float/3600000)-(startdate::float/3600000))::numeric, 2) as "Outage Time", -- Calculating Case Duration converted to Hours
	custout as "Cust Out",
	round((((enddate::float/3600000)-(startdate::float/3600000))*custout)::numeric, 2) as "Cust Hours",
	round(((((enddate::float/60000)-(startdate::float/60000))*custout)/22426)::numeric, 2) as saidi -- Calculating SAIDI
from cases
where datestrt between '2014-01-20' and '2014-01-22'
-- or dateend between '2014-01-20' and '2014-01-22'
and casestatus = 'Closed'
-- and enddate-startdate > 300000
-- group by datestrt
-- having sum((((enddate::float/60000)-(startdate::float/60000))*custout)/22459) > 0
order by startdate asc;