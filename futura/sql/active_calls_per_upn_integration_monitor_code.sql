select record_id, customer, '' address, street, phase, pole_num, caselist, casenotes, 
	callstatus, account, phone, meter, feeder, calldate || ' ' || calltime calldatetime, pwrout, ticketnum,
	region, oldcase, servadr2 || ' ' || servadr3 servaddr, typedata, prevcalls, phonenew, phonechange,
	callbackrequired, elementid, takenby, datecall, code, xtraservice, remarks, call_back_date || ' ' ||
	call_back_time call_back_date_time, called_back, called_back_by, pinged, power_ok 
from calls
where callstatus not ilike '%closed%'
-- and deleted = 'False'