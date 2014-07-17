<!DOCTYPE HTML>
<html>
<head>
<title>Test Postgres Connection</title>
</head>
<body>
<%
set dbConn=Server.CreateObject("ADODB.Connection")
dbConn.ConnectionString = "Driver={PostgreSQL Unicode};Server=10.40.0.170;Port=5432;Database=omsprod;Uid=postgres;Pwd=usouth;"
dbConn.Open 
Response.Write("Attributes: " & dbConn.Attributes & "<br>")
Response.Write("CommandTimeout: " & dbConn.CommandTimeout & "<br>")
Response.Write("ConnectionString: " & dbConn.ConnectionString & "<br>")
Response.Write("ConnectionTimeout: " & dbConn.ConnectionTimeout & "<br>")
Response.Write("CursorLocation: " & dbConn.CursorLocation & "<br>")
Response.Write("DefaultDatabase: " & dbConn.DefaultDatabase & "<br>")
Response.Write("IsolationLevel: " & dbConn.IsolationLevel & "<br>")
Response.Write("Mode: " & dbConn.Mode & "<br>")
Response.Write("Provider: " & dbConn.Provider & "<br>")
Response.Write("State: " & dbConn.State & "<br>")
Response.Write("Version: " & dbConn.Version & "<br>")
Response.Write("<br>")

set rs = Server.CreateObject("ADODB.recordset")
sql = "SELECT * FROM trucks"
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