<%@ Language="VBscript" %>
<!DOCTYPE HTML>
<html>
<head>
<title>Reporting OMS Table Data Top 10 Rows</title>
<%
'Declare form variables
Dim tblName

'Assign variables with form data
'Use Request.Form("name") with form method="POST"
'Use Request.QueryString("name") with form methos="GET"
tblName = Request.QueryString("tblName")
autoRefresh = Request.QueryString("autoRefresh")
refreshRate = Request.QueryString("refreshRate")
if autoRefresh = "true" then
    Response.Write("<meta http-equiv='refresh' content='" & refreshRate & "'>" & vbCrLF)
end if
%>
</head>
<body>
<h1>OMS Table Data Top 10 Rows</h1>
<!--#include virtual="omsreports/dbConn.asp"-->
<%
'let's now print out the received values in the browser
Response.Write("Table Name: " & tblName & "<br>" & vbCrLf)

dbConn.Open
sqlFields = "SELECT * FROM " & tblName & " LIMIT 1"
set rsFields = Server.CreateObject("ADODB.recordset")
rsFields.Open sqlFields, dbConn

Response.Write("<table border=1>" & vbCrLf)
Response.Write("    <tr>" & vbCrLf)
If rsFields.EOF Then
    Response.Write("        <th nowrap><h3>" & sqlFields & "</h3></th>" & vbCrLf)
    Response.Write("    </tr><tr>" & vbCrLf)
    Response.Write("        <td>No Data Available In This Table</td>" & vbCrLf)
    Response.Write("    </tr>" & vbCrLf)
Else
    sqlData = "SELECT * FROM " & tblName & " LIMIT 10"
    set rsData = Server.CreateObject("ADODB.recordset")
    rsData.Open sqlData, dbConn

    Response.Write("        <th nowrap align='left' colspan=30><h3>" & sqlData & "</h3></th>" & vbCrLf)
    Response.Write("    </tr><tr>" & vbCrLf)
    do until rsFields.EOF
      for each x in rsFields.Fields
        Response.Write("        <th nowrap>" & x.name & "</th>" & vbCrLf)
      next
      rsFields.MoveNext
    loop
    Response.Write("    </tr>" & vbCrLf)
    do until rsData.EOF
      Response.Write("    <tr>" & vbCrLf)
      for each y in rsData.Fields
        If (IsNull(y.value) OR y.value = "") Then
          Response.Write("        <td>&nbsp;</td>" & vbCrLf)
        Else
          Response.Write("        <td nowrap>" & y.value & "</td>" & vbCrLf)
        End If
      next
      Response.Write("    </tr>" & vbCrLf)
      rsData.MoveNext
    loop
    rsData.close
End If
Response.Write("</table>" & vbCrLf)
rsFields.close
dbConn.close
%>
</body>
<html>