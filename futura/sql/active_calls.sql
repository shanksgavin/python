select ticketnum, *
from calls
where deleted = '0'
and callstatus not in ('CLOSED', 'closed', 'Closed')
order by ticketnum asc