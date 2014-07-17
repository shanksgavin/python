select c.record_id, c.elementid, c.deviceout, c.ticketnum, c.code, cb.elementid, cb.casenum, cb.casestatus, cb.calls
from calls as c
left outer join callbundles as cb
on c.deviceout = cb.elementid
where c.callstatus ilike 'ACTIVE'
and cb.elementid is not null

UNION

select c.record_id, c.elementid, c.deviceout, c.ticketnum, c.code, cb.elementid, cb.casenum, cb.casestatus, cb.calls
from calls as c
left outer join callbundles as cb
on c.deviceout = cb.elementname
where c.callstatus ilike 'ACTIVE'
and cb.elementname is not null;

-- select *
-- from calls as c
-- left outer join callbundles as cb
-- on c.deviceout = cb.elementid
-- where c.callstatus ilike 'ACTIVE';