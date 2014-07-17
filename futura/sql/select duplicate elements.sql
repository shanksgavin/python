select *
-- into switch_no_alt_values_20131120
from switch
where elementid in 
	(
	select elementid
	from switch 
	group by elementid
	having count(elementid) > 1
	)
and altupstreamela = ''
and altupstreamelb = ''
and altupstreamelc = ''
order by elementid asc