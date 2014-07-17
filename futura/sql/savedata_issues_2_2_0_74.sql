-- use omsprod_bad_data db
select distinct(ticketnum)
from audit_calls
where ticketnum like '130820-C%'
and audit_stamp > '2013-08-08'
and customer != 'unresolved call'
and ivr_object_id = ''
group by ticketnum
order by ticketnum asc