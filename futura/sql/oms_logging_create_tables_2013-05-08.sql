-- Table: obj_model

-- DROP TABLE obj_model;

CREATE TABLE obj_model
(
  date_ date,
  time_ time without time zone,
  category character varying(100),
  message text,
  log_id bigint,
  logfile character varying
)
WITH (
  OIDS=FALSE
);
ALTER TABLE obj_model OWNER TO postgres;
COMMENT ON TABLE omsclient IS E'Contains the contents of C:\\omsprint\\Logs\\ObjectModel\\objectmodel.log through omsclient.log.10';

-- Table: omsclient

-- DROP TABLE omsclient;

CREATE TABLE omsclient
(
  date_ date,
  time_ time without time zone,
  category character varying(100),
  message text,
  log_id bigserial NOT NULL,
  logfile character varying,
  CONSTRAINT omsclient_pk PRIMARY KEY (log_id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE omsclient OWNER TO postgres;
COMMENT ON TABLE omsclient IS E'Contains the contents of C:\\omsprint\\Logs\\omsclient\\omsclinet.log through omsclient.log.10';
