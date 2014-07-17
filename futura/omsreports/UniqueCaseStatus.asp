<!DOCTYPE HTML>
<html>
<head>
<title>Reporting Unique Case Status Types and Counts</title>
<!--#include virtual="omsreports/dbConn.asp"-->
<link rel="stylesheet" type="text/css" href="omsreports/StyleSheet.css">
</head>
<%
dbConn.Open
sql = "select distinct(casestatus), count(casestatus) from cases where deleted = '0' group by casestatus order by casestatus"
'sql = "select distinct(casestatus), count(casestatus) from cases group by casestatus order by casestatus"
set rs = Server.CreateObject("ADODB.recordset")
rs.Open sql, dbConn
%>
<body>
<h1>OMS Unique Case Status Types and Counts</h1>
<h3>Reporting database: <span style="color:Red;"><% Response.Write(dbConn.DefaultDatabase) %></span></h3>
    <table style="width: 400px;">
        <tr>
            <th style="width: 200px;" align="left">
                Case Status
            </th>
            <th style="width: 200px;" align='left'>
                Number of Cases
            </th>
        </tr>

<%
'Response.Write("<h3>" & sql & "</h3>")
do until rs.EOF
  Response.Write("        <tr>")
  Response.Write("          <td style='width: 200px;'>" & rs.Fields.Item("casestatus") & "</td>")
  Response.Write("          <td style='width: 200px;'>" & rs.Fields.Item("count") & "</td>")
  Response.Write("        </tr>")
  rs.MoveNext
loop

rs.close
dbConn.close
%>
    </table>
</body>
<html>