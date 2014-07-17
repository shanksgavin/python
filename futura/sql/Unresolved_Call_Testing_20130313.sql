select *
from calls
where 
--casenotes = 'Unresolved Call created during IVR Load'
--deleted = 'f'
typedata in (348160, 117788672, 117526528, 872448)
--takenby ilike 'williamg%'
--callstatus not in ('CLOSED', 'closed')
--unres_orig in ('t')
and unres_call in ('t', 'f')
--and ticketnum like '%-C0015'
--and calldate > '2013-03-10'
order by ticketnum asc