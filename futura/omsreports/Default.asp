<!DOCTYPE html>
<html>
<head>
<title>OMS ASP Display Available Reports</title>
<meta http-equiv="Content-Type" content="text/html;charset=UTF-8" />
<link rel="stylesheet" type="text/css" href="OMSStyleSheet.css" />
</head>
<body>
<div class="left">
<table>
<tr><td><img src="Logo.jpg" alt="Futura Systems, Inc. Logo"/></td><td colspan="2"><h1>Report Listing</h1></td></tr>
<tr align="left"><th colspan="2" width="50%">Report Name</th><th width="50%">Last Modified</th></tr>
<%
dim thefolder, strfile, dateToday, dateOfFile
dim dateWebColor

'Set Today's Date
dateToday = Now

'Set OMSReports webserver path
thefolder=server.mappath("\omsreports")

'Create ServerObject for accessing files on webserver
set fs = server.createobject("Scripting.FileSystemObject")
set f = fs.getfolder(thefolder)
set fl = f.files    ' list of files

'Looping through all files in omsreport folder
'1. Filter out all files except the reports
'2. Build a link to the report

'Enhancements:
'1. Define and List all possible reports 
'2. Determine if report is available
'3. Build link if present
'4. Display only report name if not present

for each strfile in fl
    dateOfFile = strfile.DateLastModified
    if (DateDiff("d", dateOfFile, dateToday) > 5) then
        dateWebColor = "<td style='color: red;'>" & strfile.DateLastModified & " (" & DateDiff("d", dateOfFile,  dateToday) & " days old!)</td>"
    else
        dateWebColor = "<td>" & strfile.DateLastModified & " (" & DateDiff("d", dateOfFile,  dateToday) & " days old!)</td>"
    end if

	ext = fs.GetExtensionName(strfile)
	If ext = "html" Then
		response.write("<tr><td colspan=2><a href='" & strfile.name & "'>" & strfile.name & "</a></td>" & dateWebColor & "</tr>")
	ElseIf ext = "pdf" Then
		response.write("<tr><td colspan=2><a href='" & strfile.name & "'>" & strfile.name & "</a></td>" & dateWebColor & "</tr>")
	End If
next
%>
</table>
</div>
<%
set fs = nothing
set f = nothing
set fl = nothing
%>
<div class='right'>
<table>
    <tr align="center"><td colspan="2"><h1>OMS Live Reports</h1></td></tr>
    <tr align="left"><th width="40%">Report Name</th><th width="60%">Description</th></tr>
    <tr valign="top"><td><a href="report7a.asp">Report 7a</a></td><td>Displays the 7a report.</td></tr>
    <tr valign="top"><td><a href="PastOutageCountsByCounty.asp">Past Outages By County</a></td><td>Display past outage counts grouped by county. Defaults to current month. Allows user to set a date range.</td></tr>
    <tr valign="top"><td><a href="ActiveOutageCountsByCounty.asp">Active Outages By County</a></td><td>Display active outage counts grouped by county.</td></tr>
    <tr valign="top"><td><a href="UniqueStatus.asp">Unique Status Values</a></td><td>Displays distinct status values for cases that are not deleted.</td></tr>
    <tr valign="top"><td><a href="UniqueCaseStatus.asp">Unique Case Status</a></td><td>Displays the unique status type for cases that are NOT deleted within db and totals each type</td></tr>
    <tr valign="top"><td><a href="AllUniqueCaseStatus.asp">All Unique Case Status</a></td><td>Displays the unique status type for ALL cases within db and totals each type</td></tr>
    <tr valign="top"><td><a href="CurrentPredictedCallBundles.asp">Currently Predicted Call Bundles</a></td><td>Displays active Call Bundles in the system. Refreshes every 15 seconds.</td></tr>
    <tr valign="top"><td><a href="CaseHistoryWithCallCounts.asp">Case History with Call Count</a></td><td>Displays history of cases with total number of calls associated with the case. Default sorted by largest calls per case.</td></tr>
    <tr valign="top"><td><a href="OMSTablesWithRowCounts.asp">Tables with Row Count</a></td><td>Displays all available tables in OMS with row counts since last VACUUM. Default sorted by largest row count then table name alphabetically.</td></tr>
    <tr valign="top"><td><a href="OMSTestCaseCustomersUpdateOnPhaseChange.asp?casenum=0&autoRefresh=f">Testing Casescustomers Table Update</a></td><td>Testing Casescustomers table is updated when a Predicted/Confirmed Case has its phase changed.</td></tr>
    <tr valign="top"><td colspan="2"><hr /></td></tr>
    <tr valign="top"><td><a href="FuturaActiveCalls.asp">Futura Active Calls</a></td><td>Displays all active calls in OMS. This attempts to replace the Jasper Report of the same name.</td></tr>
    <tr valign="top"><td><a href="FuturaActiveCallsAutoRefresh.asp">Futura Active Calls Auto Refresh</a></td><td>Displays all active calls in OMS. This attempts to replace the Jasper Report of the same name. This report refreshes every 2 seconds.</td></tr>
    <tr valign="top"><td><a href="FuturaActiveCases.asp">Futura Active Cases</a></td><td>Displays all active cases in OMS ('Call Bundles', 'CauseFound', 'CauseUnknown', 'Predicted'). This report pulls cases from callbundles and cases tables</td></tr>
    <tr valign="top"><td><a href="OMSTablesWithCasenumField.asp">Tracking Active Rogue Case</a></td><td>Displays an active case in Report, but is not active in OMS Client.</td></tr>
    <tr valign="top"><td colspan="2"><hr /></td></tr>
    <tr valign="top"><td><a href="ChartingTest.asp">Chart Testing</a></td><td>Testing out Highcharts with IIS7 and ASP classic code.</td></tr>
    <tr valign="top"><td><a href="ClosedCaseCountsByCausePerYear.asp">Annual Outage Causes with Custhours</a></td><td>Displays Closed Case Causes with Total Outage Hours for every Year</td></tr>
</table>
</div>
</body>
</html>