select distinct(m.county), count(county)
from meterbase as m
join (select c.elementid
from calls as c
left outer join callbundles as cb
on c.deviceout = cb.elementid
where c.callstatus ilike 'ACTIVE'
and cb.elementid is not null

UNION

select c.elementid
from calls as c
left outer join callbundles as cb
on c.deviceout = cb.elementname
where c.callstatus ilike 'ACTIVE'
and cb.elementname is not null)

as active_calls
on m.elementid = active_calls.elementid
group by county

-- select *
-- from calls as c
-- left outer join callbundles as cb
-- on c.deviceout = cb.elementid
-- where c.callstatus ilike 'ACTIVE';