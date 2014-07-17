<!DOCTYPE HTML>
<html>
<!--#include virtual="omsreports/dbConn.asp"-->
<head>
<title>Futura OMS - Top 10 Closed Case Counts By Cause Per Year</title>
<link rel="stylesheet" type="text/css" href="OMSStyleSheet.css"/>
<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>
<script src="../Highcharts-3.0.0/js/highcharts.js" type="text/javascript"></script>
<script src="../Highcharts-3.0.0/js/modules/exporting.js" type="text/javascript"></script>
<script type='text/javascript'>
$(document).ready(function() {
var charts = [];
<%
dbConn.Open
' Create sql script to run prior to execution of this report
' to analyze db and populate historydata, yearlydata tables

'Company Name for Report
sqlCompanyName = "SELECT setting_value AS setup_company_name FROM settings WHERE setting_name = 'company_name'"
set rsCompanyName = Server.CreateObject("ADODB.recordset")
rsCompanyName.Open sqlCompanyName, dbConn

' Determine the available years to report
sqlYears = "SELECT distinct(to_char(datestrt, 'YYYY')) as case_year FROM cases WHERE to_char(datestrt, 'YYYY') NOT IN ('0011','0010') GROUP BY case_year ORDER BY case_year asc"
'sqlYears = "SELECT distinct(to_char(datestrt, 'YYYY')) as case_year FROM cases WHERE to_char(datestrt, 'YYYY') IN ('2010') GROUP BY case_year ORDER BY case_year asc"
set rsYears = Server.CreateObject("ADODB.recordset")
rsYears.Open sqlYears, dbConn

' Cycle through each Year of statistics
dim rowYearCnt, tableHTML, tableYear, chartData, chartYear, causeData, causeTable, showChart
rowYearCnt = 0
dim yearDict, tableDict
Set yearDict = Server.CreateObject("Scripting.Dictionary")
Set tableDict = Server.CreateObject("Scripting.Dictionary")
do until rsYears.EOF
    rowYearCnt = rowYearCnt + 1
    'Determine Annual Case Causes and Totals
    'Start inner loop construct for Annual Cause Totals
    sqlAnnualCauses = "select distinct(cause) as cause, count(cause) as cause_counts, coalesce(sum(custhours),0) AS custhours from cases where datestrt between '" & rsYears.Fields.Item("case_year") & "-01-01' and '" & rsYears.Fields.Item("case_year") & "-12-31' and casestatus in ('Closed', 'CLOSED') and deleted = 'f' group by cause order by custhours desc limit 10"
    set rsAnnualCauses = Server.CreateObject("ADODB.recordset")
    rsAnnualCauses.Open sqlAnnualCauses, dbConn
    dim rowCnt
    do until rsAnnualCauses.EOF
        rowCnt = rowCnt + 1
        rsAnnualCauses.MoveNext
     loop
    'Build Date Table
    'if at least one case then print out data table
    if rowCnt > 0 then
        rsAnnualCauses.MoveFirst
        do until rsAnnualCauses.EOF
            if rsAnnualCauses.Fields.Item("cause") = "" then 
                causeData = "['Undefined Cause (Blank)', " & rsAnnualCauses.Fields.Item("custhours") & "],"
                causeTable = "        <tr><td>Undefined Cause (Blank)</td><td  style='text-align: right;'>" & FormatNumber(rsAnnualCauses.Fields.Item("custhours"),3) & "</td></tr>" & vbCrLF
            else
                causeData = "['" & rsAnnualCauses.Fields.Item("cause") & "', " & rsAnnualCauses.Fields.Item("custhours") & "],"
                causeTable = "        <tr><td>" & rsAnnualCauses.Fields.Item("cause") & "</td><td style='text-align: right;'>" & FormatNumber(rsAnnualCauses.Fields.Item("custhours"),3) & "</td></tr>" & vbCrLF
            end if
            if rsAnnualCauses.Fields.Item("custhours") > 0 then
                showChart = true
            else
                showChart = false
            end if
            chartData = chartData + causeData
            tableHTML = tableHTML + causeTable
            rsAnnualCauses.MoveNext
        loop
        chartData = Left(chartData,Len(chartData)-1)
        
    else
        chartData = "['No Data', 1]"
        tableHTML = "    <tr><td colspan=2 style='text-align: center; color: crimson;'>No Data Available for " & rsYears.Fields.Item("case_year") & "</td></tr>" & vbCrLF
    end if
    'Add dataDict containing HighChart data and tableHTML to yearDict
    
    if showChart then
        'Insert New Chart into charts array
        Response.Write("charts.push(new Highcharts.Chart({" & vbCrLF)
        Response.Write("    chart: {" & vbCrLF)
        Response.Write("        renderTo: 'chart_"& rsYears.Fields.Item("case_year") & "'," & vbCrLF)
        Response.Write("        type: 'pie'" & vbCrLF)
        Response.Write("    }," & vbCrLF)
        Response.Write("    title: { text: 'Causes with Customer Outage Hours, " & rsYears.Fields.Item("case_year") & "'}," & vbCrLF)
        Response.Write("    series: [{" & vbCrLF)
        Response.Write("        data: [" & chartData & "]" & vbCrLF)
        Response.Write("    }]" & vbCrLF)
        Response.Write("}) ) ;" & vbCrLF)
        Response.Write(vbCrLF)
    else
        'Insert Empty Chart into charts array when data values are 0
        Response.Write("charts.push(new Highcharts.Chart({" & vbCrLF)
        Response.Write("    chart: {" & vbCrLF)
        Response.Write("        renderTo: 'chart_"& rsYears.Fields.Item("case_year") & "'," & vbCrLF)
        Response.Write("        type: 'pie'" & vbCrLF)
        Response.Write("    }," & vbCrLF)
        Response.Write("    title: { text: 'No Data Available, " & rsYears.Fields.Item("case_year") & "'}," & vbCrLF)
        Response.Write("    series: [{" & vbCrLF)
        Response.Write("        data: [['No Data Available', 1]]" & vbCrLF)
        Response.Write("    }]" & vbCrLF)
        Response.Write("}) ) ;" & vbCrLF)
        Response.Write(vbCrLF)
    end if

    'Close before moving to the next Year
    rsAnnualCauses.Close
    
    'yearDict.Add rowYearCnt, rsYears.Fields.Item("case_year")
    'Response.Write("//" & rsYears.Fields.Item("case_year") & vbCrLF)
    tableDict.Add rowYearCnt, tableHTML
    'set dataDict = Nothing
    tableHTML = ""
    chartData = ""
    rsYears.MoveNext
loop

%>
});
</script>
</head>
<body bgcolor="White">
<div class="header">
    <table class="reportHeader">
        <tr class="rowHeader">
<%
'Fill in table header for report
Response.Write("        <td align='left' style='font-size:18px;'>" & rsCompanyName.Fields.Item("setup_company_name") & " (DB: " & dbConn.DefaultDatabase & ")</td>" & vbCrLf)
Response.Write("        <td align='right' style='font-size:28px; font-weight:bold;'>Top 10 Causes Per Year</td>" & vbCrLf)
rsCompanyName.Close
%>
        </tr>
    </table>
</div>
<%
'Build main content of charts and reports
dim rowData
rowData = 0
if rowYearCnt > 0 then
    rsYears.MoveFirst
    do until rsYears.EOF
        rowData = rowData + 1
        'Response.Write("Loop: " & rowYearCnt & vbCrLF)
        Response.Write("<div id='year_" & rsYears.Fields.Item("case_year") & "' style='width: 11in; margin-left: .17in;'>" & vbCrLF)
        Response.Write("<div id='chart_" & rsYears.Fields.Item("case_year") & "' style='min-width: 400px; width: 6in; min-height: 400px; position: relative; float: left;'></div>" & vbCrLF)
        Response.Write("<div id='table_" & rsYears.Fields.Item("case_year") & "' style='min-width: 400px; width: 4in; min-height: 400px; position: relative; float: left;'>" & vbCrLF)
        'Response.Write("Key: " & data & " has Data: " & yearDict.Item(x).Item(data) & "<br>")
        Response.Write("<table>" & vbCrLF)
        Response.Write("        <tr><td colspan=2 style='background-color: #70A9C6; color: white; font-family: Arial; font-size:20px; text-align: center;'>" & rsYears.Fields.Item("case_year") & "</td></tr>" & vbCrLF)
        'Create Table Data Headers
        Response.Write("        <tr><th>Cause</th><th>Outage Hours</th></tr>" & vbCrLF)
        'Print the preformed table from lines 71 to 77
        Response.Write(tableDict.Item(rowData))
        Response.Write("</table>" & vbCrLF)
        Response.Write("</div>" & vbCrLF)
        Response.Write("</div>" & vbCrLF)
        rsYears.MoveNext
    Loop
else
    Response.Write("No Body Text to loop through<br>" & vbCrLF)
end if
rsYears.Close
dbConn.Close
%>
</body>
</html>