delete from switch
where elementid in 
	(
	select elementid
	from switch 
	group by elementid
	having count(elementid) = 2
	)
and altupstreamela = ''
and altupstreamelb = ''
and altupstreamelc = ''