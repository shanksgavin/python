<!DOCTYPE HTML>
<html>
<!--#include virtual="omsreports/dbConn.asp"-->
<%
dbConn.Open
' Create sql script to run prior to execution of this report
' to analyze db and populate historydata, yearlydata tables

'Company Name for Report
sqlCompanyName = "SELECT setup.company_name AS setup_company_name FROM public.setup setup"
set rsCompanyName = Server.CreateObject("ADODB.recordset")
rsCompanyName.Open sqlCompanyName, dbConn

' Determine the available years to report
sqlYears = "SELECT DISTINCT(year_rpt) as year FROM historydata ORDER BY year ASC"
set rsYears = Server.CreateObject("ADODB.recordset")
rsYears.Open sqlYears, dbConn

' Use these Queries within the Yearly looping construct
' Determine SAIFI values per year
sqlSAIFI = "" 'To be filled in later; Just a placeholder
'set rsSAIFI = Server.CreateObject("ADODB.recordset")
'rsSAIFI.Open sqlSAIFI, dbConn
' Determine SAIDI values per year

sqlSAIDI = "" 'To be filled in later; Just a placeholder
'set rsSAIFI = Server.CreateObject("ADODB.recordset")
'rsSAIFI.Open sqlSAIFI, dbConn
%>
<head>
<title>Futura OMS Report 7a</title>
<link rel="stylesheet" type="text/css" href="OMSStyleSheet.css">
</head>
<body bgcolor="White">
<div class="header">
    <table class="reportHeader">
        <tr class="rowHeader">
<%
'Fill in table header for 7A report
Response.Write("        <td align='left' colspan=3 style='font-size:18px;'>" & rsCompanyName.Fields.Item("setup_company_name") & " (DB: " & dbConn.DefaultDatabase & ")</td>" & vbCrLf)
Response.Write("        <td align='right' colspan=2 style='font-size:28px; font-weight:bold;'>Form 7A</td>" & vbCrLf)
rsCompanyName.Close
%>
        </tr>
    </table>
</div>
<div>
<table class="report">
    <tr>
        <th style="width: 10%; text-align:center; vertical-align:text-top;" nowrap>
            Cause Type
        </th>
        <th style="width: 10%; text-align:center; vertical-align:text-top;">
            Number of Outages
        </th>
        <th style="width: 10%; text-align:center; vertical-align:text-top;">
            Number of Consumers Affected
        </th>
        <th style="width: 10%; text-align:center; vertical-align:text-top;">
            Consumer Minutes
        </th>
        <th style="width: 10%; text-align:center; vertical-align:text-top;">
            Average Number of Consumers
        </th>
        <th style="width: 10%; text-align:center; vertical-align:text-top;">
            SAIFI
        </th>
        <th style="width: 10%; text-align:center; vertical-align:text-top;">
            SAIDI
        </th>
        <th style="width: 10%; text-align:center; vertical-align:text-top;">
            CAIDI
        </th>
        <th style="width: 10%; text-align:center; vertical-align:text-top;">
            ASAI
        </th>
    </tr>
<%
' Cycle through each Year of statistics
dim rowCnt
rowCnt = 1
do until rsYears.EOF
    Response.Write("    <tr>" & vbCrLF)
    Response.Write("        <td colspan=9 style='background-color: #70A9C6; color: white; font-family: Arial; font-size:12;'>" & rsYears.Fields.Item("year") & "</td>" & vbCrLF)
    Response.Write("    </tr>" & vbCrLF)
    ' Start inner loop construct for Yearly Details
    ' Power Supply Stats
    sqlAnnualDataPowerSupply = "SELECT * FROM historydata WHERE year_rpt = " & rsYears.Fields.Item("year") & " AND causetype = 'p'"
    set rsAnnualDataPowerSupply = Server.CreateObject("ADODB.recordset")
    rsAnnualDataPowerSupply.Open sqlAnnualDataPowerSupply, dbConn
    dim counter
    counter = 0
    do until rsAnnualDataPowerSupply.EOF
        counter = counter + 1
        rsAnnualDataPowerSupply.MoveNext
    loop
    'response.write("The number of records is: " & counter & vbCrLF)
    if counter > 0 then
        rsAnnualDataPowerSupply.MoveFirst
        Response.Write("    <tr>" & vbCrLF)
        Response.Write("        <td nowrap>Power Supply</td>" & vbCrLF)
        Response.Write("        <td>" & formatNumber(rsAnnualDataPowerSupply.Fields.Item("outagecount"), 0, 0, 0, -1) & "</td>" & vbCrLF)
        Response.Write("        <td>" & formatNumber(rsAnnualDataPowerSupply.Fields.Item("custaffected"), 0, 0, 0, -1) & "</td>" & vbCrLF)
        Response.Write("        <td>" & formatNumber(rsAnnualDataPowerSupply.Fields.Item("totalcusthours")*60, 0, 0, 0, -1) & "</td>" & vbCrLF)
        Response.Write("        <td>" & formatNumber(rsAnnualDataPowerSupply.Fields.Item("avgcustserved"), 0, 0, 0, -1) & "</td>" & vbCrLF)
        Response.Write("        <td>" & formatNumber(rsAnnualDataPowerSupply.Fields.Item("custaffected")/rsAnnualDataPowerSupply.Fields.Item("avgcustserved"), 3) & "</td>" & vbCrLF)
        Response.Write("        <td>" & formatNumber(((rsAnnualDataPowerSupply.Fields.Item("totalcusthours")*60)*rsAnnualDataPowerSupply.Fields.Item("custaffected"))/rsAnnualDataPowerSupply.Fields.Item("avgcustserved"), 0, 0, 0, -1) & "</td>" & vbCrLF)
        Response.Write("        <td>CAIDI Value</td>" & vbCrLF)
        Response.Write("        <td>ASAI Value</td>" & vbCrLF)
        Response.Write("    </tr>" & vbCrLF)
        rsAnnualDataPowerSupply.Close
    else
        Response.Write("    <tr><td nowrap>Power Supply</td><td colspan=8 style='text-align: center; color: crimson;'>No Data Available for this Year's Event</td></tr>" & vbCrLF)
    end if
    set counter = Nothing
    ' Major Event Stats
    sqlAnnualDataMajorEvent = "SELECT * FROM historydata WHERE year_rpt = " & rsYears.Fields.Item("year") & " AND causetype = 'm'"
    set rsAnnualDataMajorEvent = Server.CreateObject("ADODB.recordset")
    rsAnnualDataMajorEvent.Open sqlAnnualDataMajorEvent, dbConn
    'dim counter
    counter = 0
    do until rsAnnualDataMajorEvent.EOF
        counter = counter + 1
        rsAnnualDataMajorEvent.MoveNext
    loop
    'response.write("The number of records is: " & counter & vbCrLF)
    if counter > 0 then
        rsAnnualDataMajorEvent.MoveFirst
        Response.Write("    <tr class='alt'>" & vbCrLF)
        Response.Write("        <td nowrap>Major Event</td>" & vbCrLF)
        Response.Write("        <td>" & formatNumber(rsAnnualDataMajorEvent.Fields.Item("outagecount"), 0, 0, 0, -1) & "</td>" & vbCrLF)
        Response.Write("        <td>" & formatNumber(rsAnnualDataMajorEvent.Fields.Item("custaffected"), 0, 0, 0, -1) & "</td>" & vbCrLF)
        Response.Write("        <td>" & formatNumber(rsAnnualDataMajorEvent.Fields.Item("totalcusthours")*60, 0, 0, 0, -1) & "</td>" & vbCrLF)
        Response.Write("        <td>" & formatNumber(rsAnnualDataMajorEvent.Fields.Item("avgcustserved"), 0, 0, 0, -1) & "</td>" & vbCrLF)
        Response.Write("        <td>" & formatNumber(rsAnnualDataMajorEvent.Fields.Item("custaffected")/rsAnnualDataMajorEvent.Fields.Item("avgcustserved"), 3) & "</td>" & vbCrLF)
        Response.Write("        <td>" & formatNumber(((rsAnnualDataMajorEvent.Fields.Item("totalcusthours")*60)*rsAnnualDataMajorEvent.Fields.Item("custaffected"))/rsAnnualDataMajorEvent.Fields.Item("avgcustserved"), 0, 0, 0, -1) & "</td>" & vbCrLF)
        Response.Write("        <td>CAIDI Value</td>" & vbCrLF)
        Response.Write("        <td>ASAI Value</td>" & vbCrLF)
        Response.Write("    </tr>" & vbCrLF)
        rsAnnualDataMajorEvent.Close
    else
        Response.Write("    <tr class='alt'><td nowrap>Major Event</td><td colspan=8 style='text-align: center; color: crimson;'>No Data Available for this Year's Event</td></tr>" & vbCrLF)
    end if
    set counter = Nothing

    ' Planned Event Stats
    sqlAnnualDataPlanned = "SELECT * FROM historydata WHERE year_rpt = " & rsYears.Fields.Item("year") & " AND causetype = 's'"
    set rsAnnualDataPlanned = Server.CreateObject("ADODB.recordset")
    rsAnnualDataPlanned.Open sqlAnnualDataPlanned, dbConn
    'dim counter
    counter = 0
    do until rsAnnualDataPlanned.EOF
        counter = counter + 1
        rsAnnualDataPlanned.MoveNext
    loop
    'response.write("The number of records is: " & counter)
    if counter > 0 then
        rsAnnualDataPlanned.MoveFirst    
        Response.Write("    <tr>" & vbCrLF)
        Response.Write("        <td nowrap>Planned</td>" & vbCrLF)
        Response.Write("        <td>" & formatNumber(rsAnnualDataPlanned.Fields.Item("outagecount"), 0, 0, 0, -1) & "</td>" & vbCrLF)
        Response.Write("        <td>" & formatNumber(rsAnnualDataPlanned.Fields.Item("custaffected"), 0, 0, 0, -1) & "</td>" & vbCrLF)
        Response.Write("        <td>" & formatNumber(rsAnnualDataPlanned.Fields.Item("totalcusthours")*60, 0, 0, 0, -1) & "</td>" & vbCrLF)
        Response.Write("        <td>" & formatNumber(rsAnnualDataPlanned.Fields.Item("avgcustserved"), 0, 0, 0, -1) & "</td>" & vbCrLF)
        Response.Write("        <td>" & formatNumber(rsAnnualDataPlanned.Fields.Item("custaffected")/rsAnnualDataPlanned.Fields.Item("avgcustserved"), 3) & "</td>" & vbCrLF)
        Response.Write("        <td>" & formatNumber(((rsAnnualDataPlanned.Fields.Item("totalcusthours")*60)*rsAnnualDataPlanned.Fields.Item("custaffected"))/rsAnnualDataPlanned.Fields.Item("avgcustserved"), 0, 0, 0, -1) & "</td>" & vbCrLF)
        Response.Write("        <td>CAIDI Value</td>" & vbCrLF)
        Response.Write("        <td>ASAI Value</td>" & vbCrLF)
        Response.Write("    </tr>" & vbCrLF)
        rsAnnualDataPlanned.Close
    else
        Response.Write("    <tr><td nowrap>Planned</td><td colspan=8 style='text-align: center; color: crimson;'>No Data Available for this Year's Event</td></tr>" & vbCrLF)
    end if
    set counter = Nothing

    ' All Other Stats
    sqlAnnualDataOther = "SELECT * FROM historydata WHERE year_rpt = " & rsYears.Fields.Item("year") & " AND causetype = 'o'"
    set rsAnnualDataOther = Server.CreateObject("ADODB.recordset")
    rsAnnualDataOther.Open sqlAnnualDataOther, dbConn
    'dim counter
    counter = 0
    do until rsAnnualDataOther.EOF
        counter = counter + 1
        rsAnnualDataOther.MoveNext
    loop
    'response.write("The number of records is: " & counter)
    if counter > 0 then
        rsAnnualDataOther.MoveFirst    
        Response.Write("    <tr class='alt'>" & vbCrLF)
        Response.Write("        <td nowrap>All Other</td>" & vbCrLF)
        Response.Write("        <td>" & formatNumber(rsAnnualDataOther.Fields.Item("outagecount"), 0, 0, 0, -1) & "</td>" & vbCrLF)
        Response.Write("        <td>" & formatNumber(rsAnnualDataOther.Fields.Item("custaffected"), 0, 0, 0, -1) & "</td>" & vbCrLF)
        Response.Write("        <td>" & formatNumber(rsAnnualDataOther.Fields.Item("totalcusthours")*60, 0, 0, 0, -1) & "</td>" & vbCrLF)
        Response.Write("        <td>" & formatNumber(rsAnnualDataOther.Fields.Item("avgcustserved"), 0, 0, 0, -1) & "</td>" & vbCrLF)
        Response.Write("        <td>" & formatNumber(rsAnnualDataOther.Fields.Item("custaffected")/rsAnnualDataOther.Fields.Item("avgcustserved"), 3) & "</td>" & vbCrLF)
        Response.Write("        <td>" & formatNumber(((rsAnnualDataOther.Fields.Item("totalcusthours")*60)*rsAnnualDataOther.Fields.Item("custaffected"))/rsAnnualDataOther.Fields.Item("avgcustserved"), 0, 0, 0, -1) & "</td>" & vbCrLF)
        Response.Write("        <td>CAIDI Value</td>" & vbCrLF)
        Response.Write("        <td>ASAI Value</td>" & vbCrLF)
        Response.Write("    </tr>" & vbCrLF)
        rsAnnualDataOther.Close
    else
        Response.Write("    <tr class='alt'><td nowrap>All Other</td><td colspan=8 style='text-align: center; color: crimson;'>No Data Available for this Year's Event</td></tr>" & vbCrLF)
    end if
    set counter = Nothing
    
    rowCnt = rowCnt + 1
    rsYears.MoveNext
loop

rsYears.close
dbConn.close
%>
</table>
</div>
</body>
<html>