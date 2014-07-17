--Working on fta_williamg
--With db named omsprod using HOMER data
--not to be confused with omsprod using WIREGRASS data

-- select record_id, customer, feeder, ticketnum, takenby, casenum, casenotes, remarks, caselist, shapefield, unres_orig, *
-- from calls
-- where deleted = 'False'
-- and callstatus = 'ACTIVE'
-- --and unres_orig = 'True'
-- order by record_id desc;

-- select *
-- from cases
-- where casenum like '130429-_0004%';

-- select *
-- from calls
-- where ticketnum = '130422-C0001';

select *
from calls
where caselist like '130429-_0004%';

-- update calls
-- set callstatus = 'CLOSED'
-- where record_id = 56616;

-- update calls
-- set caselist = '130429-O0004.'
-- where record_id = 56616;