-- View: vw_console_logs

-- DROP VIEW vw_console_logs

CREATE OR REPLACE VIEW vw_console_logs AS
	select date_, time_, category, message, logfile, log_id
	from obj_model
	union
	select date_, time_, category, message, logfile, log_id
	from omsclient
	union
	select date_, time_, category, message, logfile, log_id
	from save_data
	-- order by date_ desc, time_ desc, log_id asc
	;

ALTER TABLE vw_console_logs OWNER TO postgres;
GRANT ALL ON TABLE vw_console_logs TO postgres;
COMMENT ON VIEW vw_console_logs IS 'Compiled 3 Logs in to one - ObjModel, Client, and SaveData';