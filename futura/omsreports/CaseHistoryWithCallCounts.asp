<!DOCTYPE HTML>
<html>
<head>
<title>Reporting Case History with Call Count</title>
<!--#include virtual="omsreports/dbConn.asp"-->
<link rel="stylesheet" type="text/css" href="omsreports/StyleSheet.css">
</head>
<%
dbConn.Open
sql = "select distinct(casenum) as casenum, count(casenum) as call_cnt from casescustomers group by casenum order by call_cnt desc"
'sql = "select distinct(casestatus), count(casestatus) from cases group by casestatus order by casestatus"
set rs = Server.CreateObject("ADODB.recordset")
rs.Open sql, dbConn
%>
<body>
<h1>OMS Case History with Call Count</h1>
<h3>Reporting database: <span style="color:Red;"><% Response.Write(dbConn.DefaultDatabase) %></span></h3>
    <table style="width: 500px;">
        <tr>
            <th width=100>&nbsp;</th>
            <th style="width: 200px;" align="left">
                Case Number
            </th>
            <th style="width: 200px;" align='left'>
                Number of Calls
            </th>
        </tr>

<%
'Response.Write("<h3>" & sql & "</h3>")
dim rowCnt
rowCnt = 1
do until rs.EOF
  Response.Write("        <tr>")
  Response.Write("          <td width=100>"&rowCnt&"</td>")
  Response.Write("          <td style='width: 200px;'>" & rs.Fields.Item("casenum") & "</td>")
  Response.Write("          <td style='width: 200px;'>" & rs.Fields.Item("call_cnt") & "</td>")
  Response.Write("        </tr>")
  rowCnt = rowCnt + 1
  rs.MoveNext
loop

rs.close
dbConn.close
%>
    </table>
</body>
<html>