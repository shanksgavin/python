select distinct(c.casenum, m.county) as county, 
	count(cc.customer), 
	cc.deleted as cc_deleted,
	c.deleted as c_deleted
	--m.elementid, 
	--m.county 
from casescustomers cc, meterbase m, cases c
where cc.customer = m.elementid 
AND cc.casenum = c.casenum
AND c.casestatus in ('CauseFound', 'CauseUnknown', 'Predicted')
AND cc.deleted = FALSE
AND c.deleted = FALSE
--AND (c.datestrt>='2013-01-24' and c.dateend<='2013-03-04')
GROUP BY c.casenum, m.county, cc_deleted, c_deleted
--GROUP BY customers.county
ORDER BY county ASC