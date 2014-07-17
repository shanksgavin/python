<!DOCTYPE HTML>
<html>
<head>
<title>Reporting Currently Predicted Call Bundles</title>
<!--#include virtual="omsreports/dbConn.asp"-->
<meta http-equiv="refresh" content="15">
<link rel="stylesheet" type="text/css" href="OMSStyleSheet.css">
</head>
<%
dbConn.Open
'sql = "select distinct(casestatus), count(casestatus) from cases where deleted = '0' group by casestatus order by casestatus"
sql = "SELECT element, phase, casenum, custout, datestrt, pwrout, casestatus, assigned, crews, visible, calls, totalcustdownstream, downstreamcases, pwroutdownstreamcases, uptrace, feeder FROM callbundles ORDER BY casenum ASC"
sqlCount = "SELECT count(*) as rowcount FROM callbundles"
set rs = Server.CreateObject("ADODB.recordset")
set rsCount = Server.CreateObject("ADODB.recordset")
rs.Open sql, dbConn
rsCount.Open sqlCount, dbConn
%>
<body>
<h1>OMS Currently Predicted Call Bundles with details</h1>
<h3>Reporting database: <span style class='red'><% Response.Write(dbConn.DefaultDatabase) %></span></h3>
<%
dim rowNum
rowNum = 1
Response.Write("<h3>Total Predicted Call Bundles: " & rsCount.Fields.Item("rowcount") & "</h3>" & vbCrLf)
'Response.Write("<h3>" & sql & "</h3>")
do until rs.EOF
  Response.Write("<div class='hidden'>" & vbCrLf)
  Response.Write("    <table id='"& rs.Fields.Item("casenum") & "' border=1>" & vbCrLf)
  Response.Write("        <tr style='background-color:gray;'>" & vbCrLf)
  Response.Write("          <td width=400>(" & rowNum & ") Case Number: " & rs.Fields.Item("casenum") & "</td><td width=200>Power Out? " & rs.Fields.Item("pwrout") & "</td><td width=200>Start of Outage: " & rs.Fields.Item("datestrt") & "</td>" & vbCrLf)
  Response.Write("        </tr>" & vbCrLf)
  Response.Write("    </table>" & vbCrLf)
  Response.Write("</div>" & vbCrLf)
  Response.Write("<div class='hidden'>" & vbCrLf)
  Response.Write("    <table id='"& rs.Fields.Item("casenum") & "_data'border=1>" & vbCrLf)
  Response.Write("        <tr>" & vbCrLf)
  Response.Write("          <td width=400>Element ID: " & rs.Fields.Item("element") & "</td><td width=200>Phase: " & rs.Fields.Item("phase") & "</td><td width=200>Feeder: " & rs.Fields.Item("feeder") & "</td>" & vbCrLf)
  Response.Write("        </tr>" & vbCrLf)
  Response.Write("        <tr>" & vbCrLf)
  Response.Write("          <td>Case Status: " & rs.Fields.Item("casestatus") & "</td><td>Customers without power:</td><td>" & rs.Fields.Item("custout") & "</td>" & vbCrLf)
  Response.Write("        </tr>" & vbCrLf)
  Response.Write("        <tr>" & vbCrLf)
  Response.Write("          <td>Is Case Assigned? " & rs.Fields.Item("assigned") & "</td><td colspan=2>Total Affected, Downstream Customers: " & rs.Fields.Item("totalcustdownstream") & "</td>" & vbCrLf)
  Response.Write("        </tr>" & vbCrLf)
  Response.Write("        <tr>" & vbCrLf)
  Response.Write("          <td>If so, by: " & rs.Fields.Item("crews") & "</td><td colspan=2>&nbsp;</td>" & vbCrLf)
  Response.Write("        </tr>" & vbCrLf)
  Response.Write("        <tr>" & vbCrLf)
  Response.Write("          <td>Calls in bundle:</td><td colspan=2>" & rs.Fields.Item("calls") & "</td>" & vbCrLf)
  Response.Write("        </tr>" & vbCrLf)
  Response.Write("        <tr>" & vbCrLf)
  Response.Write("          <td>Downstream Cases:</td><td colspan=2>" & rs.Fields.Item("downstreamcases") & "</td>" & vbCrLf)
  Response.Write("        </tr>" & vbCrLf)
  Response.Write("        <tr>" & vbCrLf)
  Response.Write("          <td>Downstrean Cases without Power:</td><td colspan=2>" & rs.Fields.Item("pwroutdownstreamcases") & "</td>" & vbCrLf)
  Response.Write("        </tr>" & vbCrLf)
  Response.Write("        <tr valign='top'>" & vbCrLf)
  Response.Write("          <td>Uptrace:</td><td colspan=2>" & rs.Fields.Item("uptrace") & "</td>" & vbCrLf)
  Response.Write("        </tr>" & vbCrLf)
  Response.Write("    </table>" & vbCrLf)
  Response.Write("</div>" & vbCrLf)
  rowNum = rowNum + 1
  rs.MoveNext
loop

rs.close
dbConn.close
%>
</body>
<html>