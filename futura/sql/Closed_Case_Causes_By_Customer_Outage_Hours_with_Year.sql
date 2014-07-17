SELECT DISTINCT(cause) AS cause, count(cause) AS cause_count, sum(custhours) AS custhours, to_char(datestrt, 'YYYY') AS cause_year
FROM cases
WHERE casestatus = 'Closed'
--AND datestrt >= '$P!{Start Date:}'::date
--AND dateend <= '$P!{End Date:}'::date
AND deleted = 'false'
AND repowereddate != startdate
GROUP BY cause, cause_year
ORDER BY cause_year DESC, custhours DESC
--LIMIT 10