<!DOCTYPE HTML>
<html>
<head>
<title>Reporting OMS Tables with Row Counts since last DB VACUUM</title>
<!--#include virtual="omsreports/dbConn.asp"-->
<link rel="stylesheet" type="text/css" href="OMSStyleSheet.css">
</head>
<%
dbConn.Open
sql = "SELECT c.relname as tblname, c.reltuples as tblRowCount FROM pg_catalog.pg_class c LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace WHERE n.nspname='public' AND c.relkind IN ('r','') AND n.nspname NOT IN ('pg_catalog', 'pg_toast', 'information_schema') ORDER BY c.reltuples DESC, c.relname ASC"
set rs = Server.CreateObject("ADODB.recordset")
rs.Open sql, dbConn
%>
<body>
<h1>OMS Tables with Row Counts since last DB VACUUM</h1>
<h3>Reporting database: <span style="color:Red;"><% Response.Write(dbConn.DefaultDatabase) %></span></h3>
<table style="width: 500px;">
    <tr>
        <th width="100">
            &nbsp;
        </th>
        <th style="width: 200px;" align="left">
            Table Name
        </th>
        <th style="width: 200px;" align='left'>
            Number of Rows
        </th>
    </tr>

<%
'Response.Write("<h3>" & sql & "</h3>")
dim rowCnt
rowCnt = 1
do until rs.EOF
  Response.Write("    <tr>")
  Response.Write("        <td width=100>"&rowCnt&"</td>")
  Response.Write("        <td style='width: 200px;'><a href='OMSTableDataView10.asp?tblName=" & rs.Fields.Item("tblname") & "'>" & rs.Fields.Item("tblname") & "</a></td>")
  Response.Write("        <td style='width: 200px;'>" & rs.Fields.Item("tblRowCount") & "</td>")
  Response.Write("    </tr>")
  rowCnt = rowCnt + 1
  rs.MoveNext
loop

rs.close
dbConn.close
%>
</table>
</body>
<html>