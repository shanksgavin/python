select datestrt,
	--to_timestamp(startdate/1000) as startdate,
	--to_timestamp(enddate/1000) as enddate,
	(startdate::float/60000) as startdate_int,
	(enddate::float/60000) as enddate_int,
	-- enddate-startdate as duration_ms, -- Calculating Case Duration in Milliseconds
	((enddate::float/60000)-(startdate::float/60000)) as duration_mins, -- Calculating Case Duration converted to Minutes
	custout,
	((enddate::float/60000)-(startdate::float/60000)*custout) as nextstep,
	(((enddate::decimal/60000)-(startdate::decimal/60000)*custout)/22459) as saidi -- Calculating SAIDI
	--
	-- SAIDI needs to be the sum of the Duration divided by Total Customers
	--
from cases
where datestrt between '2013-01-01' and '2013-12-31'
and casestatus = 'Closed'
and enddate-startdate > 300000
-- and ((enddate::decimal/60000)-(startdate::decimal/60000)*custout) >= 0
-- group by datestrt
-- having sum(((enddate::decimal/60000)-(startdate::decimal/60000)*custout)/22459) >= 0
order by datestrt asc