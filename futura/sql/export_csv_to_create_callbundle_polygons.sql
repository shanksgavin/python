-- create export file to use in pytohn script to build polygons of callbundle life cycle
select audit_id, boundary
from audit_callbundles
where stamp between '2013-06-09 07:00:00' and '2013-06-10 15:00:00'
order by stamp asc