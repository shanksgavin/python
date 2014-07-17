select cases.casenum, cases.datestrt, cases.timestrt, cases.timeend, cases.dateend, cases.casestatus, calls.callstatus, calls.elementid, calls.ticketnum
from cases
join casescustomers as cc on cases.casenum = cc.casenum
join calls on cc.customer = calls.elementid
where calls.callstatus ilike 'active'
--and cases.casestatus not ilike 'active'
order by casenum asc