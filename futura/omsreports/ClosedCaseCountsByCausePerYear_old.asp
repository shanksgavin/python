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
sqlYears = "SELECT distinct(to_char(datestrt, 'YYYY')) as case_year FROM cases WHERE to_char(datestrt, 'YYYY') NOT IN ('0011','0010') GROUP BY case_year ORDER BY case_year asc"
'sqlYears = "SELECT distinct(to_char(datestrt, 'YYYY')) as case_year FROM cases WHERE to_char(datestrt, 'YYYY') IN ('2010') GROUP BY case_year ORDER BY case_year asc"
set rsYears = Server.CreateObject("ADODB.recordset")
rsYears.Open sqlYears, dbConn

%>
<head>
<title>Futura OMS - Closed Case Counts By Cause Per Year</title>
<link rel="stylesheet" type="text/css" href="OMSStyleSheet.css"/>
<script src="http://code.highcharts.com/highcharts.js" type="text/javascript"></script>
<script src="http://code.highcharts.com/modules/exporting.js" type="text/javascript"></script>
</head>
<body bgcolor="White">
<div class="header">
    <table class="reportHeader">
        <tr class="rowHeader">
<%
'Fill in table header for 7A report
Response.Write("        <td align='left' style='font-size:18px;'>" & rsCompanyName.Fields.Item("setup_company_name") & " (DB: " & dbConn.DefaultDatabase & ")</td>" & vbCrLf)
Response.Write("        <td align='right' style='font-size:28px; font-weight:bold;'>Closesd Cases By Cause</td>" & vbCrLf)
rsCompanyName.Close
%>
        </tr>
    </table>
</div>
<%
' Cycle through each Year of statistics
dim rowYearCnt, tableHTML, tableYear, chartData, chartYear
rowYearCnt = 0
dim yearDict, dataDict, k, i
Set yearDict = Server.CreateObject("Scripting.Dictionary")
Set dataDict = Server.CreateObject("Scripting.Dictionary")
do until rsYears.EOF
    rowYearCnt = rowYearCnt + 1
    Response.Write(rsYears.Fields.Item("case_year") & "<br>" & vbCrLF)
    
    'Determine Annual Case Causes and Totals
    'Start inner loop construct for Annual Cause Totals
    sqlAnnualCauses = "select distinct(cause) as cause, count(cause) as cause_counts from cases where datestrt between '" & rsYears.Fields.Item("case_year") & "-01-01' and '" & rsYears.Fields.Item("case_year") & "-12-31' and casestatus in ('Closed', 'CLOSED') and deleted = 'f' group by cause order by cause asc"
    set rsAnnualCauses = Server.CreateObject("ADODB.recordset")
    rsAnnualCauses.Open sqlAnnualCauses, dbConn
    dim rowCnt
    do until rsAnnualCauses.EOF
        'Response.Write("Entered into loop for rsAnnualCauses<br>" & vbCrLF)
        'Response.Write("Key will be: " & rsAnnualCauses.Fields.Item("cause") & "<br>" & vbCrLF)
        rowCnt = rowCnt + 1
        'Build Chart Data
        if rsAnnualCauses.Fields.Item("cause") = "" then 
            'Response.Write("Key: " & "BLANK" & " Value: " & rsAnnualCauses.Fields.Item("cause_counts") & "<br>" & vbCrLF)
            dataDict.Add rowCnt, "['BLANK'," & rsAnnualCauses.Fields.Item("cause_counts") & "]"
            'Response.Write("Array Value: " & dataDict.Item(rowCnt) & "<br>" & vbCrLF)
        else
            'Response.Write("Key: " & rowCnt & " Value: " & rsAnnualCauses.Fields.Item("cause_counts") & "<br>" & vbCrLF)
            dataDict.Add rowCnt, "['" & rsAnnualCauses.Fields.Item("cause") & "', " & rsAnnualCauses.Fields.Item("cause_counts") & "]"
            'Response.Write("Array Value: " & dataDict.Item(rowCnt) & "<br>" & vbCrLF)
        end if
        'Response.Write("Row Count: " & rowCnt & "<br>" & vbCrLF)
        'k = dataDict.Keys
        'for i=0 to dataDict.Count-1
        '    Response.Write(k(i)&"<br>")
        'next
        rsAnnualCauses.MoveNext
        'Response.Write("Moved to next row.<br>" & vbCrLF)
    loop
    'Build Date Table
    'if at least one case then print out data table
    'Response.Write("Building tableHTML.<br>" & vbCrLF)
    if rowCnt > 0 then
        rsAnnualCauses.MoveFirst
        do until rsAnnualCauses.EOF
            chartData = chartData + "['" & rsAnnualCauses.Fields.Item("cause") & "', " & rsAnnualCauses.Fields.Item("cause_counts") & "']"
            tableHTML = tableHTML + "    <tr>" & vbCrLF
            tableHTML = tableHTML + "        <td>" & rsAnnualCauses.Fields.Item("cause") & "</td><td>" & rsAnnualCauses.Fields.Item("cause_counts") & "</td>" & vbCrLF
            tableHTML = tableHTML + "    </tr>" & vbCrLF
            rsAnnualCauses.MoveNext
        loop
        'Response.Write(tableHTML)
        tableYear = "table_" & rsYears.Fields.Item("case_year")
        chartYear = "table_" & rsYears.Fields.Item("case_year")
        'Response.Write("What: " & tableYear & "<br>")
        dataDict.Add tableYear, tableHTML
    'Close before moving to the next Year
    rsAnnualCauses.Close
    else
        chartData = "['No Data', 1]"
        tableHTML = "    <tr><td colspan=2 style='text-align: center; color: crimson;'>No Data Available for " & rsYears.Fields.Item("case_year") & "</td></tr>" & vbCrLF
        tableYear = "table_" & rsYears.Fields.Item("case_year")
        chartYear = "table_" & rsYears.Fields.Item("case_year")
        'Response.Write("What: " & tableYear)
        dataDict.Add tableYear, tableHTML
    end if
    'tableYear = "table_" & rsYears.Fields.Item("case_year")
    'Response.Write("TableYear: " & dataDict.Item(tableYear))
    'Add dataDict containing HighChart data and tableHTML to yearDict
    yearDict.Add rsYears.Fields.Item("case_year"), dataDict
    for each x in yearDict
        Response.Write(vbCrLF & "<br>Year in yearDict: " & x & "<br>")
        for each data in yearDict.Item(x)
            Response.Write("Key: " & data & " has Data: " & yearDict.Item(x).Item(data) & "<br>")
        next
    next
    dataDict.RemoveAll
    yearDict.RemoveAll
    'set dataDict = Nothing
    rsYears.MoveNext
loop
Response.Write("Data Construction Complete.")
if rowYearCnt > 0 then
    rsYears.MoveFirst
    do until rsYears.EOF
        Response.Write("<div id='year_" & rsYears.Fields.Item("case_year") & "' style='width: 8.5in; margin-left: .17in;'>" & vbCrLF)
        Response.Write("<div id='chart_" & rsYears.Fields.Item("case_year") & "' style='min-width: 400px; width: 400px; min-height: 400px; position: relative; float: left;'></div>" & vbCrLF)
        Response.Write("<div id='table_" & rsYears.Fields.Item("case_year") & "' style='min-width: 400px; width: 400px; min-height: 400px;  margin-right: .17in; position: relative;'>" & vbCrLF)
        Response.Write("<table>" & vbCrLF)
        Response.Write("    <tr>" & vbCrLF)
        Response.Write("        <td colspan=2 style='background-color: #70A9C6; color: white; font-family: Arial; font-size:12;'>" & rsYears.Fields.Item("case_year") & "</td>" & vbCrLF)
        Response.Write("    </tr>" & vbCrLF)
        'Create Table Data Headers
        Response.Write("    <tr>" & vbCrLF)
        Response.Write("        <th>Cause</th><th>Total</th>" & vbCrLF)
        Response.Write("    </tr>" & vbCrLF)
        'Print tableHTML from dataDict inside of yearDict
        Response.Write(yearDict("table_" & rsYears.Fields.Item("case_year")))
        'Close the Table and two open DIV tags
        Response.Write("    </table>" & vbCrLF)
        Response.Write("</div>" & vbCrLF)
        Response.Write("</div>" & vbCrLF)
        rsYears.MoveNext
    loop
    rsYears.close
else
    Response.Write("No Data Available for Any Years!" & vbCrLF)
end if


dbConn.close
%>
</body>
</html>