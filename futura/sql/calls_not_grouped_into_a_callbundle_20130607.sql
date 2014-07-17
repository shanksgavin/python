select audit_id, operation, stamp, elementid, element, phase, casenum, casestatus, calls, totalcustdownstream, deleted, org_record_id
from audit_callbundles
where calls like '%130607-C0012%'
--or casenum = '130607-X0343'
order by stamp asc