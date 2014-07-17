select *
from calls
where customer = 'NALL DAVID MARK'
or unres_call = 't'
order by customer asc