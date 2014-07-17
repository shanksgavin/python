<!DOCTYPE HTML>
<html>
<head>
<title>Reporting OMS Tables with "CASENUM" = '130114-O0054'</title>
<!--#include virtual="omsreports/dbConn.asp"-->
<link rel="stylesheet" type="text/css" href="OMSStyleSheet.css">
</head>
<%
dbConn.Open
'sql = "SELECT c.relname as tblname, c.reltuples as tblRowCount FROM pg_catalog.pg_class c LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace WHERE n.nspname='public' AND c.relkind IN ('r','') AND n.nspname NOT IN ('pg_catalog', 'pg_toast', 'information_schema') ORDER BY c.reltuples DESC, c.relname ASC"
sql = "select cls.relname as tblname from pg_attribute att left join pg_class cls on cls.oid = att.attrelid left join pg_type typ on typ.oid = att.atttypid where att.attname = 'casenum' and cls.relname in (SELECT c.relname FROM pg_catalog.pg_class c LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace WHERE n.nspname='public' AND c.relkind IN ('r','') AND n.nspname NOT IN ('pg_catalog', 'pg_toast', 'information_schema') ORDER BY c.relname ASC)"
set rs = Server.CreateObject("ADODB.recordset")
rs.Open sql, dbConn
%>
<body>
<h1>OMS Tables with "CASENUM" Field &<br /> "CASENUM" = '130114-O0054'</h1>
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
            Row Count
        </th>
    </tr>

<%
Response.Write("<h3>" & sql & "</h3>")
dim rowCnt
rowCnt = 1
do until rs.EOF
    sqlTbl = "SELECT * FROM " & rs.Fields.Item("tblname") & " WHERE casenum = '130114-O0054' LIMIT 1"
    sqlTblCnt = "SELECT count(*) FROM " & rs.Fields.Item("tblname") & " WHERE casenum = '130114-O0054'"
    'Response.Write("<tr><td width=500 colspan=3 align='center'>" & sqlTbl & "</td></tr>" & vbCrLf)
    set rsTbl = Server.CreateObject("ADODB.recordset")
    set rsTblCnt = Server.CreateObject("ADODB.recordset")
    rsTbl.Open sqlTbl, dbConn
    rsTblCnt.Open sqlTblCnt, dbConn
    'dim tblFields
    'fieldIndex = 0
    'Response.Write(rsTblCnt.Fields.Item("count"))
    If rsTblCnt.Fields.Item(0) Then
        do until rsTbl.EOF
            Response.Write("    <tr>" & vbCrLf)
            Response.Write("        <td width=100>"&rowCnt&"</td>" & vbCrLf)
            Response.Write("        <td style='width: 200px;'>" & rs.Fields.Item("tblname") & "</a></td>" & vbCrLf)
            Response.Write("        <td style='width: 200px;'>" & rsTblCnt.Fields.Item(0) & "</td>" & vbCrLf)
            Response.Write("    </tr>" & vbCrLf)
            rsTbl.MoveNext
            'rsTblCnt.MoveNext
        loop
    Else
        Response.Write("    <tr>" & vbCrLf)
        Response.Write("        <td width=100>"&rowCnt&"</td>" & vbCrLf)
        Response.Write("        <td style='width: 200px;'>" & rs.Fields.Item("tblname") & "</a></td>" & vbCrLf)
        Response.Write("        <td style='width: 200px;'>Case NOT found.</td>" & vbCrLf)
        Response.Write("    </tr>" & vbCrLf)
    End If
    rsTbl.close
    rsTblCnt.close
    rowCnt = rowCnt + 1
    'tblFields = 0
    'casenumFound = FALSE
    rs.MoveNext
loop

rs.close
dbConn.close
%>
</table>
</body>
<html>