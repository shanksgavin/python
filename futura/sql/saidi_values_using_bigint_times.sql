select casenum, 	-- OMS Case Number
	cause, 		-- OMS Cause
	datestrt, 		-- Human Readable Case Start Date
	timestrt, 		-- Human Readable Case Start Time
	dateend, 		-- Human Readable Case End Date
	timeend, 		-- Human Readable Case End Time
	custhours, 	-- OMS Calculated Customer Outage Hours
	totalcustdownstream, -- All Customers Downstream from Device; Inclusive of All Phases
	oldcustout, 	-- Affected Customers Downstream from Device; Only Power Out Phases
	custout, 		-- Adjusted Affected Customers Downstream from Device; Considers Additional Downstream Cases
	to_timestamp(startdate/1000) as startdate, -- BigInt Start Date Converted to Timestamp
	to_timestamp(enddate/1000) as enddate, -- BigInt End Date Converted to Timestamp
	((enddate::decimal/60000)-(startdate::decimal/60000)*custout)/60.0 as new_custhours, -- Subtracting Start from End (bigint) dates converted to minutes; believed to be proper though it produces many negative values
	((startdate::decimal/60000)-(enddate::decimal/60000)*custout)/60.0 as new_custhours2, -- Subtracting End from Start (bigint) dates converted to minutes; not corrected but done to compare results
	enddate-startdate as duration_ms, -- Calculating Case Duration in Milliseconds
	(enddate::decimal/60000)-(startdate::decimal/60000) as duration_mins, -- Calculating Case Duration converted to Minutes
	(((enddate::decimal/60000)-(startdate::decimal/60000)*custout)/22459) as saidi -- Calculating SAIDI
	--
	-- SAIDI needs to be the sum of the Duration divided by Total Customers
	--
from cases
where datestrt between '2013-01-01' and '2013-12-31'
and casestatus = 'Closed'
and enddate-startdate > 300000
-- and (((enddate::decimal/60000)-(startdate::decimal/60000)*custout)/22459) >= 0
order by datestrt asc, timestrt asc