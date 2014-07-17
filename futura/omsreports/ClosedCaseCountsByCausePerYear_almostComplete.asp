<!DOCTYPE HTML>
<html>
<!--#include virtual="omsreports/dbConn.asp"-->
<head>
<title>Futura OMS - Closed Case Counts By Cause Per Year</title>
<link rel="stylesheet" type="text/css" href="OMSStyleSheet.css"/>
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

%>
<script src="http://code.highcharts.com/highcharts.js" type="text/javascript"></script>
<script src="http://code.highcharts.com/modules/exporting.js" type="text/javascript"></script>
</head>
<body bgcolor="White">
<script src="../Highcharts-3.0.0/js/highcharts.js"></script>
<script src="../Highcharts-3.0.0/js/modules/exporting.js"></script>
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
    'Response.Write(rsYears.Fields.Item("case_year") & "<br>" & vbCrLF)
    
    'Determine Annual Case Causes and Totals
    'Start inner loop construct for Annual Cause Totals
    sqlAnnualCauses = "select distinct(cause) as cause, count(cause) as cause_counts from cases where datestrt between '" & rsYears.Fields.Item("case_year") & "-01-01' and '" & rsYears.Fields.Item("case_year") & "-12-31' and casestatus in ('Closed', 'CLOSED') and deleted = 'f' group by cause order by cause asc"
    set rsAnnualCauses = Server.CreateObject("ADODB.recordset")
    rsAnnualCauses.Open sqlAnnualCauses, dbConn
    dim rowCnt
    do until rsAnnualCauses.EOF
        rowCnt = rowCnt + 1
        'Build Chart Data
        'if rsAnnualCauses.Fields.Item("cause") = "" then 
        '    chartData = chartData + "['BLANK'," & rsAnnualCauses.Fields.Item("cause_counts") & "],"
        'else
        '    chartData = chartData + "['" & rsAnnualCauses.Fields.Item("cause") & "', " & rsAnnualCauses.Fields.Item("cause_counts") & "],"
        'end if
        rsAnnualCauses.MoveNext
     loop
    'Build Date Table
    'if at least one case then print out data table
    if rowCnt > 0 then
        rsAnnualCauses.MoveFirst
        do until rsAnnualCauses.EOF
            chartData = chartData + "['" & rsAnnualCauses.Fields.Item("cause") & "', " & rsAnnualCauses.Fields.Item("cause_counts") & "],"
            tableHTML = tableHTML + "        <tr><td>" & rsAnnualCauses.Fields.Item("cause") & "</td><td>" & rsAnnualCauses.Fields.Item("cause_counts") & "</td></tr>" & vbCrLF
            rsAnnualCauses.MoveNext
        loop
        chartData = Left(chartData,Len(chartData)-1)
        'tableYear = "table_" & rsYears.Fields.Item("case_year")
        'chartYear = "chart_" & rsYears.Fields.Item("case_year")
        'dataDict.Add chartYear, chartData
    'Close before moving to the next Year
    rsAnnualCauses.Close
    else
        chartData = "['No Data', 1]"
        tableHTML = "    <tr><td colspan=2 style='text-align: center; color: crimson;'>No Data Available for " & rsYears.Fields.Item("case_year") & "</td></tr>" & vbCrLF
        'tableYear = "table_" & rsYears.Fields.Item("case_year")
        'chartYear = "chart_" & rsYears.Fields.Item("case_year")
        'dataDict.Add tableYear, tableHTML
    end if
    'Add dataDict containing HighChart data and tableHTML to yearDict
    yearDict.Add rsYears.Fields.Item("case_year"), dataDict
    for each x in yearDict
        'Response.Write(vbCrLF & "<br>Year in yearDict: " & x & "<br>")
        Response.Write("<div id='year_" & rsYears.Fields.Item("case_year") & "' style='width: 8.5in; margin-left: .17in;'>" & vbCrLF)
        Response.Write("<script type='text/javascript'>" & vbCrLF)
        Response.Write("    $(function () {" & vbCrLF)
        Response.Write("        $('#chart_" & rsYears.Fields.Item("case_year") & "').highcharts({" & vbCrLF)
        Response.Write("            chart: {" & vbCrLF)
        Response.Write("                plotBackgroundColor: null," & vbCrLF)
        Response.Write("                plotBorderWidth: null," & vbCrLF)
        Response.Write("                plotShadow: false" & vbCrLF)
        Response.Write("            }," & vbCrLF)
        Response.Write("            title: {" & vbCrLF)
        Response.Write("                text: 'Closed Case Causes, " & rsYears.Fields.Item("case_year")& "'" & vbCrLF)
        Response.Write("            }," & vbCrLF)
        Response.Write("            tooltip: {" & vbCrLF)
        Response.Write("                valueDecimals: 1," & vbCrLF)
        Response.Write("                valueSuffix: '%'," & vbCrLF)
        Response.Write("                pointFormat: '{series.name}: <b>{point.percentage}</b>'" & vbCrLF)
        Response.Write("            }," & vbCrLF)
        Response.Write("            plotOptions: {" & vbCrLF)
        Response.Write("                pie: {" & vbCrLF)
        Response.Write("                    allowPointSelect: true," & vbCrLF)
        Response.Write("                    cursor: 'pointer'," & vbCrLF)
        Response.Write("                    dataLabels: {" & vbCrLF)
        Response.Write("                        enabled: true," & vbCrLF)
        Response.Write("                        color: '#000000'," & vbCrLF)
        Response.Write("                        connectorColor: '#000000'," & vbCrLF)
        Response.Write("                        formatter: function () {" & vbCrLF)
        Response.Write("                            return '<b>' + this.point.name + '</b>: ' + this.y;" & vbCrLF)
        Response.Write("                        }" & vbCrLF)
        Response.Write("                    }" & vbCrLF)
        Response.Write("                }" & vbCrLF)
        Response.Write("            }," & vbCrLF)
        Response.Write("            series: [{" & vbCrLF)
        Response.Write("                type: 'pie'," & vbCrLF)
        Response.Write("                name: 'Cause'," & vbCrLF)
        Response.Write("                size: '60%'," & vbCrLF)
        Response.Write("                data: [" & vbCrLF)
        Response.Write(chartData)
        Response.Write("                ]" & vbCrLF)
        Response.Write("            }]" & vbCrLF)
        Response.Write("        });" & vbCrLF)
        Response.Write("    });" & vbCrLF)
        Response.Write("</script>" & vbCrLF)
        
        Response.Write("<div id='chart_" & rsYears.Fields.Item("case_year") & "' style='min-width: 400px; width: 400px; min-height: 400px; position: relative; float: left;'></div>" & vbCrLF)
        Response.Write("<div id='table_" & rsYears.Fields.Item("case_year") & "' style='min-width: 400px; width: 400px; min-height: 400px; position: relative; float: left;'>" & vbCrLF)
        'Response.Write("Key: " & data & " has Data: " & yearDict.Item(x).Item(data) & "<br>")
        Response.Write("<table>" & vbCrLF)
        Response.Write("        <tr><td colspan=2 style='background-color: #70A9C6; color: white; font-family: Arial; font-size:12;'>" & rsYears.Fields.Item("case_year") & "</td></tr>" & vbCrLF)
        'Create Table Data Headers
        Response.Write("        <tr><th>Cause</th><th>Total</th></tr>" & vbCrLF)
        'Print the preformed table from lines 71 to 77
        Response.Write(tableHTML)
        Response.Write("</table>" & vbCrLF)
        Response.Write("</div>" & vbCrLF)
        Response.Write("</div>" & vbCrLF)
    next
    dataDict.RemoveAll
    yearDict.RemoveAll
    'set dataDict = Nothing
    tableHTML = ""
    rsYears.MoveNext
loop

dbConn.close
%>
</body>
</html>