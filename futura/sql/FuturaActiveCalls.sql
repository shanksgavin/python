SELECT calls.customer, 
       case 
       when length(ltrim(rtrim(calls.phone)))='10' 
       then '(' ||SUBSTR(calls.phone,1,3)||')'||' '||SUBSTR(calls.phone,4,3)||'-'||SUBSTR(calls.phone,7,4) 
       else calls.phone end AS Phone, 
       calls.street AS Address, 
       to_char(min(date '1970-01-01' +  (calls.datecall/1000.||' seconds')::INTERVAL), 'MM/DD/YY HH:MIPM') as First_Called,
       count(calls.record_id) as Times_Called 
 FROM calls 
 WHERE ltrim(rtrim(upper(callstatus))) IN ('ACTIVE') 
 AND calls.deleted=false 
 GROUP BY calls.customer, calls.street, Phone, calls.account 
 ORDER BY First_Called