SELECT elementid, element, casenum, casestatus, datestrt, dateend, status, assigned, visible, confirmed, deleted
FROM cases
WHERE casenum like '______-P%'
ORDER BY status, casenum