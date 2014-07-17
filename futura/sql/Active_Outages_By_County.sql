select c.elementid, c.element, c.casenum, c.custout, c.casestatus, c.status, c.elementname, c.feeder, c.deleted
from cases as c
where c.casestatus in ('CauseFound', 'CauseUnknown', 'Predicted')
and c.deleted = FALSE
UNION
select cb.elementid, cb.element, cb.casenum, cb.custout, cb.casestatus, cb.status, cb.elementname, cb.feeder, cb.deleted
from callbundles as cb