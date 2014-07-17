select *
from cases
where datestrt
between to_date('2013/03/07', 'yyyy/mm/dd')
and to_date('2013/03/10', 'yyyy/mm/dd')
and casestatus <> 'Closed'