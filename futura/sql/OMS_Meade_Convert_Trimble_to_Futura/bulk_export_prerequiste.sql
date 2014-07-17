-- Enable XP_CMDSHELL
--Use Master
--GO

--EXEC master.dbo.sp_configure 'show advanced options', 1
--RECONFIGURE WITH OVERRIDE
--GO

--EXEC master.dbo.sp_configure 'xp_cmdshell', 1
--RECONFIGURE WITH OVERRIDE
--GO

-- Disable XP_CMDSHELL
Use Master
GO

EXEC master.dbo.sp_configure 'xp_cmdshell', 0
RECONFIGURE WITH OVERRIDE
GO

EXEC master.dbo.sp_configure 'show advanced options', 0
RECONFIGURE WITH OVERRIDE
GO
