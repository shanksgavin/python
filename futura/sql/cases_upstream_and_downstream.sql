select casenum, pwroutupstreamcases, pwroutdownstreamcases
from cases
where casenum in (
	select casenum
	from cases
	where pwroutdownstreamcases is not NULL
	and pwroutdownstreamcases <> ''
	and casestatus = 'Closed'
	and deleted = 'False'
	order by casenum desc
	)
order by casenum desc