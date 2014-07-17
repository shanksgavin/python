create or replace function oms_logfiles.update_log_stats() returns void as
$$
BEGIN
	-- Drop metadata tables to recalculate values
	drop table if exists oms_logfiles.available_report_dates;
	raise notice 'DROPPED: oms_logfiles.available_report_dates';
	drop table if exists oms_logfiles.available_report_minutes;
	raise notice 'DROPPED: oms_logfiles.available_report_minutes';
	drop table if exists oms_logfiles.objectmodel_transactions_per_minute;
	raise notice 'DROPPED: oms_logfiles.objectmodel_transactions_per_minute';
	drop table if exists oms_logfiles.savedata_transactions_per_minute;
	raise notice 'DROPPED: oms_logfiles.savedata_transactions_per_minute';
	drop table if exists oms_logfiles.client_transactions_per_minute;
	raise notice 'DROPPED: oms_logfiles.client_transactions_per_minute';

	-- start the process to recalculate the dates from logfile data
	BEGIN
		create table oms_logfiles.available_report_dates as
		select date_ as available_report_dates
		from oms_logfiles.omslogs
		group by date_
		order by date_ desc;
	EXCEPTION
		WHEN disk_full THEN
			raise notice 'DISK FULL: Cannot create oms_logfiles.available_report_dates';
		WHEN duplicate_table THEN
			raise notice 'DUPLICATE TABLE: Cannot create oms_logfiles.available_report_dates';
	END;
	raise notice 'COMPLETED: available_report_dates processed.';

	-- start the process to recalculate the minutes from logfile data
	BEGIN
		create table oms_logfiles.available_report_minutes as
		select date_ as available_report_dates, date_trunc('minute', time_) as available_report_minutes
		from oms_logfiles.omslogs
		group by date_, date_trunc('minute', time_)
		order by date_ desc, date_trunc('minute', time_) asc;
	EXCEPTION
		WHEN disk_full THEN
			raise notice 'DISK FULL: Cannot create oms_logfiles.available_report_minutes';
		WHEN duplicate_table THEN
			raise notice 'DUPLICATE TABLE: Cannot create oms_logfiles.available_report_minutes';
	END;
	raise notice 'COMPLETED: available_report_minutes processed.';

	-- start the process to recalculate the ObjectModel transactions per minute
	BEGIN
		create table oms_logfiles.objectmodel_transactions_per_minute as
		select date_, date_trunc('minute', time_) as minute_, count(time_) as tpm --tpm = transactions per minute 
		from oms_logfiles.omslogs 
		where logfile ilike '%ObjectModel%' 
		group by date_, date_trunc('minute', time_) 
		order by date_, date_trunc('minute', time_) asc;
	EXCEPTION
		WHEN disk_full THEN
			raise notice 'DISK FULL: Cannot create oms_logfiles.objectmodel_transactions_per_minute';
		WHEN duplicate_table THEN
			raise notice 'DUPLICATE TABLE: Cannot create oms_logfiles.objectmodel_transactions_per_minute';
	END;
	raise notice 'COMPLETED: objectmodel_transactions_per_minute processed.';

	-- start the process to recalculate the SaveData transactions per minute
	BEGIN
		create table oms_logfiles.savedata_transactions_per_minute as
		select date_, date_trunc('minute', time_) as minute_, count(time_) as tpm --tpm = transactions per minute 
		from oms_logfiles.omslogs 
		where logfile ilike '%SaveData%' 
		group by date_, date_trunc('minute', time_) 
		order by date_, date_trunc('minute', time_) asc;
	EXCEPTION
		WHEN disk_full THEN
			raise notice 'DISK FULL: Cannot create oms_logfiles.savedata_transactions_per_minute';
		WHEN duplicate_table THEN
			raise notice 'DUPLICATE TABLE: Cannot create oms_logfiles.savedata_transactions_per_minute';
	END;
	raise notice 'COMPLETED: savedata_transactions_per_minute processed.';
	
	-- start the process to recalculate the Client transactions per minute
	BEGIN
		create table oms_logfiles.client_transactions_per_minute as
		select date_, date_trunc('minute', time_) as minute_, count(time_) as tpm --tpm = transactions per minute 
		from oms_logfiles.omslogs 
		where logfile ilike '%Client%' 
		group by date_, date_trunc('minute', time_) 
		order by date_, date_trunc('minute', time_) asc;
	EXCEPTION
		WHEN disk_full THEN
			raise notice 'DISK FULL: Cannot create oms_logfiles.client_transactions_per_minute';
		WHEN duplicate_table THEN
			raise notice 'DUPLICATE TABLE: Cannot create oms_logfiles.client_transactions_per_minute';
	END;
	raise notice 'COMPLETED: client_transactions_per_minute processed.';
	
END;
$$
language 'plpgsql';