SELECT DISTINCT(county) as county, COUNT(county) as outages from (
select cc.customer, m.elementid, m.county, cc.deleted,cc.casenum from casescustomers cc, meterbase m, cases c
where cc.customer = m.elementid 
AND cc.casenum = c.casenum
AND c.casestatus in ('CauseFound', 'CauseUnknown', 'Predicted')
--Need to include Call Bundles also to get all active outages/cases
AND cc.deleted = 'f'
AND (c.datestrt>='2013-02-21' and c.dateend<='2013-03-04')
) AS customers
GROUP BY customers.county
ORDER BY customers.county ASC