-- This is the full test sql.  See comment below for use in IVR Simulator

select meter 
from meterbase
where feeder in ('13-1', '13-2', '13-4')
order by random()*22464 --22464 is the total number of meters in the table
limit 200


-- ***copy and paste the following directly into the where box of the IVR simulator
-- meterbase.feeder in ('13-1', '13-2', '13-4') order by random()*22464  limit 200

-- ***used in coweta-fayette's strom/stress testing effort
-- meterbase.feeder in ('24-32', '24-22', '24-52', '25-42', '25-52', '27-22') order by random()  limit 200

-- Non Reapting Random calls with a limit
-- meterbase.meter like '%' and meterbase.meter not in (select meter from calls where deleted = False and callstatus ilike 'active') order by random() limit 200
meterbase.feeder like '__-2' and meterbase.meter not in (select meter from calls where deleted = False and callstatus ilike 'active') order by random() limit 1000