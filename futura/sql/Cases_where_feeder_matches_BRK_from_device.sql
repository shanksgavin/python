-- select elementname, *
-- from device
-- where element = 'BKR'
-- order by elementname asc;

-- feeders that DO NOT MATCH elementname from devices
select *
from cases
where feeder not in (select elementname
		from device
		where element = 'BKR')
and deleted = 'f'
order by feeder asc;

-- feeders that DO MATCH elementname from devices
select *
from cases
where feeder in (select elementname
		from device
		where element = 'BKR')
and deleted = 'f'
order by feeder asc;

-- All Cases that are NOT deleted
select *
from cases
where deleted = 'f'
order by feeder asc;

-- Unique casestatus with counts where feeder is a BRK
-- select distinct(casestatus), count(casestatus)
-- from cases
-- where feeder in (select elementname
-- 		from device
-- 		where element = 'BKR')
-- and deleted = 'f'
-- group by casestatus;