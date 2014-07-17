INSERT INTO [MCEC_Trimble_OMS].[dbo].[HistoricalTroubleCalls]
           ([Prikey]
           ,[CISKEY]
           ,[OutageID]
           ,[District]
           ,[Source]
           ,[Source_Branch]
           ,[UplineDevice]
           ,[LastOutageTime]
           ,[TraceAttribute]
           ,[CallBackNumber]
           ,[CallBackRequested]
           ,[OverideDefaultPriority]
           ,[lutPriorityCode]
           ,[lutTroubleCode]
           ,[lutTroubleCallTypeCode]
           ,[CreationDate]
           ,[LastModified]
           ,[LastModifiedBy]
           ,[Comments]
           ,[Processed]
           ,[CallCount]
           ,[Message]
           ,[s_Left]
           ,[s_Top]
           ,[ArcID]
           ,[CreatedBy]
           ,[ATTACHEDDEVICEID]
           ,[AMRRestoreTime]
           ,[AMRRestored])
     VALUES
           (<Prikey, int,>
           ,<CISKEY, varchar(50),>
           ,<OutageID, int,>
           ,<District, varchar(50),>
           ,<Source, varchar(50),>
           ,<Source_Branch, varchar(50),>
           ,<UplineDevice, varchar(30),>
           ,<LastOutageTime, datetime,>
           ,<TraceAttribute, varchar(3),>
           ,<CallBackNumber, varchar(15),>
           ,<CallBackRequested, bit,>
           ,<OverideDefaultPriority, bit,>
           ,<lutPriorityCode, int,>
           ,<lutTroubleCode, int,>
           ,<lutTroubleCallTypeCode, int,>
           ,<CreationDate, datetime,>
           ,<LastModified, datetime,>
           ,<LastModifiedBy, varchar(50),>
           ,<Comments, varchar(255),>
           ,<Processed, bit,>
           ,<CallCount, int,>
           ,<Message, image,>
           ,<s_Left, float,>
           ,<s_Top, float,>
           ,<ArcID, int,>
           ,<CreatedBy, varchar(50),>
           ,<ATTACHEDDEVICEID, int,>
           ,<AMRRestoreTime, datetime,>
           ,<AMRRestored, bit,>)
GO

