<!DOCTYPE HTML>
<html>
<head>
<title>Listing all OMS Test Cases</title>
<!--#include virtual="omsreports/dbConn.asp"-->
<link rel="stylesheet" type="text/css" href="OMSStyleSheet.css">
</head>
<%
dbDevConsole.Open
sqlTestCases = "SELECT TESTCASEID, DESCRIPTION, SPECIALINSTRUCTIONS, TESTCASEDOC, EXPECTEDRESULT, TESTCASENAME, AUTHOR, MODIFIEDBY, DATECREATED, DATEMODIFIED, PRIORITY, CATEGORYID FROM TESTCASE WHERE (CATEGORYID IN (40, 49, 50, 51, 66))"
set rsTestCases = Server.CreateObject("ADODB.recordset")
rsTestCases.Open sqlTestCases, dbDevConsole
%>
<body>
<h1>Listing all OMS Test Cases</h1>
<h3>Reporting database: <span style="color:Red;"><% Response.Write(dbDevConsole.DefaultDatabase) %></span></h3>
    <table style="width: 600px;">
        <tr>
            <th style="width: 30px;" align="left">
                Test Case ID
            </th>
            <th style="width: 300px;" align="left">
                Test Case Name
            </th>
            <th style="width: 300px;" align='left'>
                Priority
            </th>
            <th style="width: 300px;" align='left'>
                Description
            </th>
            <th style="width: 300px;" align='left'>
                Special Instructions
            </th>
            <th style="width: 300px;" align='left'>
                Expected Results
            </th>
        </tr>
<%
dim lineCount
lineCount = 1
do until rsTestCases.EOF
  Response.Write("        <tr>" & vbCrLf)
  Response.Write("          <td style='width: 30px;'>" & lineCount & "</td>" & vbCrLf)
  Response.Write("          <td style='width: 300px;'>" & rsTestCases.Fields.Item("TESTCASEID") & "</td>" & vbCrLf)
  Response.Write("          <td style='width: 300px;'>" & rsTestCases.Fields.Item("TESTCASENAME") & "</td>" & vbCrLf)
  Response.Write("          <td style='width: 300px;'>" & rsTestCases.Fields.Item("PRIORITY") & "</td>" & vbCrLf)
  Response.Write("          <td style='width: 300px;'>" & rsTestCases.Fields.Item("DESCRIPTION") & "</td>" & vbCrLf)
  Response.Write("          <td style='width: 300px;'>" & rsTestCases.Fields.Item("SPECIALINSTRUCTIONS") & "</td>" & vbCrLf)
  Response.Write("          <td style='width: 300px;'>" & rsTestCases.Fields.Item("EXPECTEDRESULT") & "</td>" & vbCrLf)
  Response.Write("        </tr>" & vbCrLf)
  lineCount = lineCount + 1
  rsTestCases.MoveNext
loop

rsTestCases.close
dbDevConsole.close
%>
    </table>
</body>
<html>