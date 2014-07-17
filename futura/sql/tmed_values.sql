select datestrt,
	sum((enddate::float/60000)-(startdate::float/60000)) as duration_mins, -- Calculating Case Duration converted to Minutes
	sum(((enddate::float/60000)-(startdate::float/60000)*custout)/22459) as saidi, -- Calculating SAIDI
	ln(sum(((enddate::float/60000)-(startdate::float/60000)*custout)/22459)) as natural_log
	-- still need to find alpha and beta of the dataset
from cases
where datestrt between '2013-01-01' and '2013-12-31'
and casestatus = 'Closed'
and enddate-startdate > 300000
group by datestrt
having sum(((enddate::float/60000)-(startdate::float/60000)*custout)/22459) > 0
order by datestrt asc