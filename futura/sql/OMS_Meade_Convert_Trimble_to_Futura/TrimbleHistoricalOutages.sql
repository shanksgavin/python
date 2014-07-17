DROP TABLE historic_data.historicaloutages;

CREATE TABLE historic_data.historicaloutages(
	prikey numeric NULL,
	cangrow boolean NULL, -- Converted datatype bit to boolean
	predicteddevice varchar(255) NULL,
	troublecallcount int NULL,
	customercount int NULL,
	district varchar(50) NULL,
	source varchar(50) NULL,
	source_branch varchar(50) NULL,
	createdby varchar(50) NULL,
	lastmodified timestamp NULL, -- Converted datatype datetime to timestamp
	lastmodifiedby varchar(50) NULL,
	acknowledgedtime timestamp NULL, -- Converted datatype datetime to timestamp
	creationdate timestamp NULL, -- Converted datatype datetime to timestamp
	crewassignedtime timestamp NULL, -- Converted datatype datetime to timestamp
	crewdispatchedtime timestamp NULL, -- Converted datatype datetime to timestamp
	crewenroutetime timestamp NULL, -- Converted datatype datetime to timestamp
	crewatsitetime timestamp NULL, -- Converted datatype datetime to timestamp
	restorationtime timestamp NULL, -- Converted datatype datetime to timestamp
	estrestorationtime timestamp NULL, -- Converted datatype datetime to timestamp
	closedtime timestamp NULL, -- Converted datatype datetime to timestamp
	luttypecode int NULL,
	lutstatuscode int NULL,
	lutcausecode int NULL,
	lutweathercode int NULL,
	luttroublecode int NULL,
	lutprioritycode int NULL,
	lutactiontakencode int NULL,
	comment_ varchar(255) NULL,
	isplanned boolean NULL, -- Converted datatype bit to boolean
	automaticchange boolean NULL, -- Converted datatype bit to boolean
	callbacklistgenerated boolean NULL, -- Converted datatype bit to boolean
	callcommentcount int NULL,
	defaultmessage text NULL, -- converted datatype image to text
	overstatusmsg boolean NULL, -- Converted datatype bit to boolean
	s_top float NULL,
	s_left float NULL,
	s_bottom float NULL,
	s_right float NULL,
	arcid varchar(50) NULL,
	shapename varchar(50) NULL,
	faultarc bigint NULL,
	faultlocation varchar(50) NULL,
	faultextent varchar(50) NULL,
	crewincharge varchar(50) NULL,
	tracetheme varchar(50) NULL,
	tracetype int NULL,
	partiallyrestored boolean NULL, -- Converted datatype bit to boolean
	parentoutage bigint NULL,
	traceattribute varchar(3) NULL,
	outagename varchar(50) NULL,
	revised_date varchar(50) NULL,
	branch_custcount int NULL,
	revised_source varchar(50) NULL,
	revised_source_branch varchar(50) NULL,
	revised_branch_custcount int NULL,
	predicteddeviceid int NULL,
	outageid int NULL,
	acknowledgedby varchar(50) NULL,
	crewassignedby varchar(50) NULL,
	crewdispatchedby varchar(50) NULL,
	crewenrouteby varchar(50) NULL,
	crewatsiteby varchar(50) NULL,
	restoredby varchar(50) NULL,
	closedby varchar(50) NULL,
	comments_edited varchar(250) NULL,
	date_edited timestamp NULL, -- Converted datatype datetime to timestamp
	over12hr varchar(1) NULL
);