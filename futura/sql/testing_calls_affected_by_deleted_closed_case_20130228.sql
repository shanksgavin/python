-- show specific cases
-- this closed case was deleted from OMC Client
-- for test case #808
-- http://gisprod/devconsole/ViewTestCaseDetails.aspx?pid=28&tid=808
select *
from cases
where casenum = '130225-O0034';

-- show specific casescustomers
-- this closed case was deleted from OMC Client
-- for test case #808
-- http://gisprod/devconsole/ViewTestCaseDetails.aspx?pid=28&tid=808
select *
from casescustomers
where casenum = '130225-O0057';

-- show all customers involved in a specific case from casescustomers
select *
from customers
where elementid in (select customer
from casescustomers
where casenum = '130225-O0057');

-- show all calls with a potential selection criteria
select *
from calls
where ticketnum = '130225-O0057';

-- show all ticketnums on 25FEB2013 from calls
select *
from calls
where ticketnum like '130225-%'
order by ticketnum asc;

-- show distinct case event characters of the ticketnum from calls
select distinct(substring(ticketnum from 8 for 1)), count(substring(ticketnum from 8 for 1))
from calls
group by ticketnum;

-- show only the case event character of the ticketnum from calls
select substring(ticketnum from 8 for 1)
from calls;

-- show all active callbundles
select *
from callbundles;

-- show all events for the calls
select *
from calls_events;

-- shows distinct ticket/case numbers from calls_events with counts
select distinct(ticketnum), count(ticketnum)
from calls_events
group by ticketnum
order by ticketnum desc;

-- show all events for the cases
select *
from cases_events;

-- Shows distinct combination of casenums and events with counts
select distinct(casenum,event) as case_event, count(event)
from cases_events
group by (case_event)
order by case_event desc;