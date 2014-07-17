select casenum, count(*)+1 as total_cases_downstream, pwroutdownstreamcases
from (
	select casenum, regexp_matches(pwroutdownstreamcases, ',', 'g'), pwroutdownstreamcases
	from cases
	where pwroutdownstreamcases is not NULL
	-- and split_part(pwroutdownstreamcases, ',', 2) <> ''
	and casestatus = 'Closed'
	and deleted = 'False'
	) 
	as alias
group by casenum, pwroutdownstreamcases
order by casenum desc

/*
 * I borrowed the idea to count downstream cases from the following website
 * http://stormbyte.blogspot.com/2012/05/count-regexp-matches-on-table-sorting.html
 */