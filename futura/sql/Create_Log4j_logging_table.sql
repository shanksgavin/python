-- Table: oms_logfiles.omslogs_log4j

-- DROP TABLE oms_logfiles.omslogs_log4j;

-- DROP TABLE oms_logfiles.omslogs_log4j;

CREATE TABLE oms_logfiles.omslogs_log4j
(
  date_ date NOT NULL,
  time_ time with time zone NOT NULL,
  category character varying(100) NOT NULL,
  message text,
  logfile character varying(15) NOT NULL,
  log_id bigserial NOT NULL
)
WITH (
  OIDS=FALSE
);
ALTER TABLE oms_logfiles.omslogs_log4j
  OWNER TO postgres;
