Select repowereddate, startdate, enddate, datestrt, timestrt, dateend, timeend, * 
from cases
where casestatus = 'Closed'
and datestrt >= '3/1/2013'::date
and dateend <= '4/5/2013'::date
and deleted = 'false'
and repowereddate != startdate
order by feeder asc, cause asc, dateend asc