﻿-- select feeder
-- from callbundles
-- where feeder = 'PT''s';

select record_id, feeder
from calls
where feeder = 'PT''s';
-- record_id's found to have PT's as a Feeder are (23462, 23256)

--correcting the values now
-- update calls
-- set feeder = 'PT''s'
-- where record_id in (23462, 23256)

-- select feeder
-- from callsfromcis
-- where feeder = 'PT''s';
-- 
-- select feeder
-- from connection
-- where feeder = 'PT''s';
-- 
-- select feeder
-- from capacitor
-- where feeder = 'PT''s';
-- 
-- select feeder
-- from cases
-- where feeder = 'PT''s';
-- 
-- select feeder
-- from device
-- where feeder = 'PT''s';
-- 
-- select feeder
-- from ivrcalls
-- where feeder = 'PT''s';
-- 
-- select feeder
-- from light
-- where feeder = 'PT''s';
-- 
-- select feeder
-- from meterbase
-- where feeder = 'PT''s';
-- 
-- select feeder
-- from new_capacitor
-- where feeder = 'PT''s';
-- 
-- select feeder
-- from new_device
-- where feeder = 'PT''s';
-- 
-- select feeder
-- from new_light
-- where feeder = 'PT''s';
-- 
-- select feeder
-- from new_meterbase
-- where feeder = 'PT''s';
-- 
-- select feeder
-- from new_regulator
-- where feeder = 'PT''s';
-- 
-- select feeder
-- from new_sections
-- where feeder = 'PT''s';
-- 
-- select feeder
-- from new_substation
-- where feeder = 'PT''s';
-- 
-- select feeder
-- from new_switch
-- where feeder = 'PT''s';
-- 
-- select feeder
-- from new_transformer
-- where feeder = 'PT''s';
-- 
-- select feeder
-- from ptfile
-- where feeder = 'PT''s';
-- 
-- select feeder
-- from regulator
-- where feeder = 'PT''s';
-- 
-- select feeder
-- from sections
-- where feeder = 'PT''s';
-- 
-- select feeder
-- from substation
-- where feeder = 'PT''s';
-- 
-- select feeder
-- from switch
-- where feeder = 'PT''s';
-- 
-- select feeder
-- from tempckts
-- where feeder = 'PT''s';
-- 
-- select feeder
-- from transformer
-- where feeder = 'PT''s';
-- 
-- select feeder
-- from upncalls
-- where feeder = 'PT''s';