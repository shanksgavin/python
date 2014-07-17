DROP TABLE historic_data.historicaltroublecalls;

CREATE TABLE historic_data.historicaltroublecalls (
	prikey int NULL,
	ciskey varchar(50) NULL,
	outageid int NULL,
	district varchar(50) NULL,
	source varchar(50) NULL,
	source_branch varchar(50) NULL,
	uplinedevice varchar(30) NULL,
	lastoutagetime timestamp NULL DEFAULT '1977-01-01 00:00:00-05', -- Converted datatype datetime to timestamp
	traceattribute varchar(3) NULL,
	callbacknumber varchar(15) NULL,
	callbackrequested boolean NULL, -- Converted datatype bit to boolean
	overidedefaultpriority boolean NULL, -- Converted datatype bit to boolean
	lutprioritycode int NULL,
	luttroublecode int NULL,
	luttroublecalltypecode int NULL,
	creationdate timestamp NULL, -- Converted datatype datetime to timestamp
	lastmodified timestamp NULL, -- Converted datatype datetime to timestamp
	lastmodifiedby varchar(50) NULL,
	comment_ varchar(255) NULL,
	processed boolean NULL, -- Converted datatype bit to boolean
	callcount int NULL,
	message text NULL, -- Converted datatype image to text
	s_left float NULL,
	s_top float NULL,
	arcid int NULL,
	createdby varchar(50) NULL,
	attacheddeviceid int NULL,
	amrrestoretime timestamp NULL, -- Converted datatype datetime to timestamp
	amrrestored boolean NULL -- Converted datatype bit to boolean
)