SELECT DISTINCT(county) as county, COUNT(county) as outages from (
select cc.customer, m.elementid, m.county from casescustomers cc, meterbase m, cases c
where cc.customer = m.elementid 
AND cc.casenum = c.casenum
AND c.casestatus in ('CauseFound', 'CauseUnknown', 'Predicted')
AND cc.deleted = FALSE
--AND (c.datestrt>='2013-01-24' and c.dateend<='2013-03-04')
) AS customers
GROUP BY customers.county
ORDER BY customers.county ASC
