select distinct(upn_outage_id), count(upn_outage_id)
from calls
group by upn_outage_id
having count(upn_outage_id) > 1
order by count desc