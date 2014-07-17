<%@ Language="VBscript" %>
<!DOCTYPE HTML>
<html>
<head>
<title>Reporting OMS Table Data Top 25 Rows</title>
</head>
<body>
<h1>OMS Table Data Top 25 Rows</h1>
<!--#include virtual="omsreports/dbConn.asp"-->
<%
'Declare form variables
Dim tblName

'Assign variables with form data
'Use Request.Form("name") with form method="POST"
'Use Request.QueryString("name") with form methos="GET"
tblName = Request.QueryString("tblName")

'let's now print out the received values in the browser
Response.Write("Table Name: " & tblName & "<br>")

dbConn.Open
sqlFields = "SELECT * FROM " & tblName & " LIMIT 1"
sqlData = "SELECT * FROM " & tblName & " ORDER BY OID DESC LIMIT 25"
set rsFields = Server.CreateObject("ADODB.recordset")
set rsData = Server.CreateObject("ADODB.recordset")
rsFields.Open sqlFields, dbConn
rsData.Open sqlData, dbConn

Response.Write("<h3>" & sqlData & "</h3>")
Response.Write("<table border=1>")
Response.Write("    <tr>")
do until rsFields.EOF
  for each x in rsFields.Fields
    Response.Write("        <td>" & x.name & "</td>")
  next
  rsFields.MoveNext
loop
Response.Write("    </tr>")
do until rsData.EOF
  Response.Write("    <tr>")
  for each y in rsData.Fields
    If IsNull(y.value) Then
      Response.Write("        <td>&nbsp;</td>")
    Else
      Response.Write("        <td>" & y.value & "</td>")
    End If
  next
  Response.Write("    </tr>")
  rsData.MoveNext
loop
Response.Write("</table>")
rsFields.close
rsData.close
dbConn.close
%>
</body>
<html>