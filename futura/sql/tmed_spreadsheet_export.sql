select datestrt,
	CASE WHEN cause = '190 - Other planned' THEN 'PLANNED'
		WHEN cause = '000 - Power supply' THEN 'POWER SUPPLY'
		WHEN cause = '' THEN 'UNKNOWN'
		ELSE 'OTHER'
	END as cause,
	timestrt,
	((enddate::float/60000)-(startdate::float/60000)) as duration_mins, -- Calculating Case Duration converted to Minutes
	custout,
	((enddate::float/60000)-(startdate::float/60000))*custout as cust_mins
from cases
where datestrt between '2013-01-01' and '2013-12-31'
and casestatus = 'Closed'
and enddate-startdate > 300000
-- group by datestrt
order by datestrt asc, timestrt asc