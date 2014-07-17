-- Export script from Trimble for OMS to import into PostgreSQL
-- Existing Meade Trimble SQL Server data is on GISTEST in the MCEC_Trimble_OMS database
-- Author: William Gavin
-- Created On: December 12, 2013

-- Current settings use a Tab delimiter and all values are treated as text regardless of SQL Server data type

EXEC xp_cmdshell 'bcp "select * from [MCEC20_OMS].[dbo].[HistoricalTroubleCalls]" queryout "D:\OMS_Trimble_Data_Conversion\historicaltroublecalls_data.sql" -T -c -t \t';
EXEC xp_cmdshell 'bcp "select * from [MCEC20_OMS].[dbo].[HistoricalOutages]" queryout "D:\OMS_Trimble_Data_Conversion\historicaloutages_data.sql" -T -c -t \t';
EXEC xp_cmdshell 'bcp "select * from [MCEC20_OMS].[dbo].[HistoricalCustOut]" queryout "D:\OMS_Trimble_Data_Conversion\historicalcustout_data.sql" -T -c -t \t';