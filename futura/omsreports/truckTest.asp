<!DOCTYPE HTML>
<html>
<head>
<title>Reporting OMS Truck Information</title>
</head>
<body>
<h1>OMS Truck Information</h1>
<!--#include virtual="omsreports/dbConn.asp"-->
<%
dbConn.Open
sql = "SELECT * FROM trucks"
'sql = "select distinct(casestatus), count(casestatus) from cases group by casestatus"
set rs = Server.CreateObject("ADODB.recordset")
rs.Open sql, dbConn

Response.Write("<h3>" & sql & "</h3>")
do until rs.EOF
  for each x in rs.Fields
    Response.Write(x.name)
    Response.Write(" = ")
    Response.Write(x.value & "<br>")
  next
  Response.Write("<br>")
  rs.MoveNext
loop

rs.close
dbConn.close
%>
</body>
<html>