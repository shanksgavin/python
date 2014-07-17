SELECT distinct(substring(casenum from 1 for 2)) as yy, count(substring(casenum from 1 for 2)) as yy_count
FROM casescustomers
WHERE deleted = '0'
GROUP BY yy
ORDER BY yy ASC;

select distinct(to_char(datestrt, 'YYYY')) as case_year
from cases
where to_char(datestrt, 'YYYY') not in ('0011','0010')
group by case_year
order by case_year desc;

select *
from cases
where to_char(datestrt, 'YYYY') in ('0011','0010')