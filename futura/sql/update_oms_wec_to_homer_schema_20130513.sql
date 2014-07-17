
--
-- FOREIGN KEYS [DROP]
-- 

--ALTER TABLE security_actions DROP CONSTRAINT security_actions_fk;
--ALTER TABLE security_userroles DROP CONSTRAINT security_users_fk2;
--ALTER TABLE security_userroles DROP CONSTRAINT security_roles_fk;

--
-- avl_vehicles
-- 

ALTER TABLE avl_vehicles
ADD vendor VARCHAR(50) DEFAULT ''::text;

--
-- avl_vendors
-- 

ALTER TABLE avl_vendors
ADD mspk_version TEXT DEFAULT 4.0;

--
-- calls
-- 

ALTER TABLE calls ALTER COLUMN customer TYPE TEXT;
ALTER TABLE calls ALTER COLUMN street TYPE TEXT;
ALTER TABLE calls ALTER COLUMN servadr2 TYPE TEXT;
ALTER TABLE calls ALTER COLUMN servadr3 TYPE TEXT;
ALTER TABLE calls ALTER COLUMN account TYPE TEXT;
ALTER TABLE calls ALTER COLUMN phone TYPE TEXT;
ALTER TABLE calls ALTER COLUMN phonenew TYPE TEXT;
ALTER TABLE calls ALTER COLUMN meter TYPE TEXT;
ALTER TABLE calls ALTER COLUMN pole_num TYPE TEXT;
ALTER TABLE calls ALTER COLUMN feeder TYPE TEXT;
ALTER TABLE calls ALTER COLUMN elementid TYPE TEXT;
ALTER TABLE calls ALTER COLUMN phase TYPE TEXT;
ALTER TABLE calls ALTER COLUMN deviceout TYPE TEXT;
ALTER TABLE calls ALTER COLUMN devicelist TYPE TEXT;
ALTER TABLE calls ALTER COLUMN ticketnum TYPE TEXT;
ALTER TABLE calls ALTER COLUMN takenby TYPE TEXT;
ALTER TABLE calls ALTER COLUMN time TYPE TEXT;
ALTER TABLE calls ALTER COLUMN trans_num TYPE TEXT;
ALTER TABLE calls ALTER COLUMN code TYPE TEXT;
ALTER TABLE calls ALTER COLUMN priority TYPE TEXT;
--ALTER TABLE calls ALTER COLUMN casenotes DROP DEFAULT;
ALTER TABLE calls ALTER COLUMN casenum TYPE TEXT;
--ALTER TABLE calls ALTER COLUMN caseprev DROP DEFAULT;
ALTER TABLE calls ALTER COLUMN oldcase TYPE TEXT;
ALTER TABLE calls ALTER COLUMN callstatus TYPE TEXT;
--ALTER TABLE calls ALTER COLUMN remarks DROP DEFAULT;
ALTER TABLE calls ALTER COLUMN caselist TYPE TEXT;
ALTER TABLE calls ALTER COLUMN called_back_by TYPE TEXT;

--
-- callsfromcis
-- 

ALTER TABLE callsfromcis ALTER COLUMN sequenceid TYPE INTEGER;
ALTER TABLE callsfromcis
ADD ivr_object_id TEXT DEFAULT ''::text;
--ALTER TABLE callsfromcis ADD CONSTRAINT callsfromcis_pkey PRIMARY KEY (sequenceid);

--
-- callstocis
-- 

ALTER TABLE callstocis
ADD cis_location TEXT DEFAULT ''::text;
ALTER TABLE callstocis
ADD upn_outage_id INT8 DEFAULT 0;

--
-- call_audio
-- 

ALTER TABLE call_audio
ADD audiourl TEXT DEFAULT ''::text;

--
-- capacitor
-- 

ALTER TABLE capacitor ALTER COLUMN guid SET DEFAULT ''::TEXT;
ALTER TABLE capacitor ALTER COLUMN layer_name SET DEFAULT ''::TEXT;
--ALTER TABLE capacitor DROP CONSTRAINT capacitor_pkey;

--
-- cases
-- 

--ALTER TABLE cases ALTER COLUMN remarks TYPE VARCHAR(150);
ALTER TABLE cases ALTER COLUMN memo TYPE VARCHAR(1000);
ALTER TABLE cases ALTER COLUMN upstreamcases TYPE VARCHAR(150);
ALTER TABLE cases ALTER COLUMN downstreamcases TYPE VARCHAR(150);
ALTER TABLE cases ALTER COLUMN pwroutupstreamcases TYPE VARCHAR(150);
ALTER TABLE cases ALTER COLUMN pwroutdownstreamcases TYPE VARCHAR(150);
ALTER TABLE cases ALTER COLUMN createdby TYPE TEXT;
--ALTER TABLE cases ALTER COLUMN missing_device_info DROP DEFAULT;
--ALTER TABLE cases ALTER COLUMN sl_complete DROP DEFAULT;
ALTER TABLE cases ALTER COLUMN ivrpredefinedmessageid TYPE VARCHAR(50);
ALTER TABLE cases ALTER COLUMN substation TYPE TEXT;

--
-- case_base_crew
-- 

-- ERROR: No command to synchronize table differences, you need to re-create the table.

--
-- case_causes
-- 

ALTER TABLE case_causes ALTER COLUMN cause_type SET DEFAULT 'O'::TEXT;

--
-- case_failures
-- 

--ALTER TABLE case_failures ALTER COLUMN code DROP DEFAULT;

--
-- case_other
-- 

--ALTER TABLE case_other ALTER COLUMN code DROP DEFAULT;

--
-- case_truck_member_history
-- 

--ALTER TABLE case_truck_member_history ALTER COLUMN crew_truck_history_id DROP NOT NULL;
--ALTER TABLE case_truck_member_history DROP CONSTRAINT pk_case_truck_member_history;

--
-- case_weather
-- 

--ALTER TABLE case_weather ALTER COLUMN code DROP DEFAULT;

--
-- connection
-- 

ALTER TABLE connection ALTER COLUMN guid SET DEFAULT ''::TEXT;
ALTER TABLE connection ALTER COLUMN layer_name SET DEFAULT ''::TEXT;

--
-- crews
-- 

ALTER TABLE crews
ADD sl_crew_id TEXT;

--
-- customers
-- 

ALTER TABLE customers
ADD guid TEXT DEFAULT ''::text;
ALTER TABLE customers
ADD layer_name TEXT DEFAULT ''::text;
ALTER TABLE customers
ADD map_oid INT4;

--
-- device
-- 

ALTER TABLE device ALTER COLUMN guid SET DEFAULT ''::TEXT;
ALTER TABLE device ALTER COLUMN layer_name SET DEFAULT ''::TEXT;

--
-- downline_devices
-- 

-- ERROR: No command to synchronize table differences, you need to re-create the table.

--
-- ivrcallerrors
-- 

-- ERROR: No command to synchronize table differences, you need to re-create the table.

--
-- light
-- 

ALTER TABLE light ALTER COLUMN guid SET DEFAULT ''::TEXT;
ALTER TABLE light ALTER COLUMN layer_name SET DEFAULT ''::TEXT;

--
-- meterbase
-- 

ALTER TABLE meterbase ALTER COLUMN guid SET DEFAULT ''::TEXT;
ALTER TABLE meterbase ALTER COLUMN layer_name SET DEFAULT ''::TEXT;

--
-- new_meterbase
-- 

-- ERROR: No command to synchronize table differences, you need to re-create the table.

--
-- new_regions
-- 

ALTER TABLE new_regions ALTER COLUMN consumerscount TYPE TEXT;
--ALTER TABLE new_regions DROP COLUMN centroid;

--
-- omstocislog
-- 

--ALTER TABLE omstocislog ALTER COLUMN recordcreationtime DROP NOT NULL;
--ALTER TABLE omstocislog ALTER COLUMN active DROP NOT NULL;
--ALTER TABLE omstocislog ALTER COLUMN verb DROP NOT NULL;
--ALTER TABLE omstocislog ALTER COLUMN mbrsep DROP NOT NULL;
--ALTER TABLE omstocislog DROP CONSTRAINT omstocislog_pkey;

--
-- pole
-- 

ALTER TABLE pole ALTER COLUMN guid SET DEFAULT ''::TEXT;
ALTER TABLE pole ALTER COLUMN layer_name SET DEFAULT ''::TEXT;

--
-- regulator
-- 

ALTER TABLE regulator ALTER COLUMN guid SET DEFAULT ''::TEXT;
ALTER TABLE regulator ALTER COLUMN layer_name SET DEFAULT ''::TEXT;

--
-- sections
-- 

ALTER TABLE sections ALTER COLUMN guid SET DEFAULT ''::TEXT;
ALTER TABLE sections ALTER COLUMN layer_name SET DEFAULT ''::TEXT;

--
-- security_actions
-- 


--
-- security_userroles
-- 


--
-- setup
-- 

--ALTER TABLE setup ALTER COLUMN cispollinterval SET DEFAULT 30;
--ALTER TABLE setup ALTER COLUMN ping_good_time SET DEFAULT 900000;
--ALTER TABLE setup ALTER COLUMN fm_system_version SET DEFAULT 9.3;
--ALTER TABLE setup
--ADD saidi_exempt_causes TEXT DEFAULT ''::text;
ALTER TABLE setup ALTER COLUMN validation_file_path SET DEFAULT 'C:/MAP_FILES/VALIDATION.TXT'::TEXT;
--ALTER TABLE setup DROP COLUMN crc_move_pred_case_to_prediction;
--ALTER TABLE setup DROP COLUMN crc_delete_downstream_pred_cases;
--ALTER TABLE setup DROP COLUMN crc_combine_cases_time_diff;

--
-- substation
-- 

ALTER TABLE substation ALTER COLUMN guid SET DEFAULT ''::TEXT;
ALTER TABLE substation ALTER COLUMN layer_name SET DEFAULT ''::TEXT;

--
-- switch
-- 

ALTER TABLE switch ALTER COLUMN guid SET DEFAULT ''::TEXT;
ALTER TABLE switch ALTER COLUMN layer_name SET DEFAULT ''::TEXT;

--
-- transformer
-- 

ALTER TABLE transformer ALTER COLUMN guid SET DEFAULT ''::TEXT;
ALTER TABLE transformer ALTER COLUMN layer_name SET DEFAULT ''::TEXT;

--
-- trucks
-- 

--ALTER TABLE trucks ALTER COLUMN truckmemo TYPE VARCHAR(1000);
