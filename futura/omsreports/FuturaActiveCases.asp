<!DOCTYPE HTML>
<html>
<head>
<title>Reporting All Active Cases and Call Bundles</title>
<!--#include virtual="omsreports/dbConn.asp"-->
<meta http-equiv="refresh" content="30">
<link rel="stylesheet" type="text/css" href="OMSStyleSheet.css">
</head>
<%
dbConn.Open
sqlCases = "select elementid, element, phase, casenum, custout, datestrt, casestatus, assigned, calls, totalcustdownstream, feeder, createdby, custhours, downstreamcases, pwroutdownstreamcases from cases where deleted = '0' and casestatus IN ('CauseFound', 'CauseUnknown', 'Predicted') order by casenum desc"
sqlCallBundles = "select elementid, element, phase, casenum, custout, datestrt, casestatus, assigned, calls, totalcustdownstream, feeder, createdby, custhours from callbundles order by casenum asc"
set rsCases = Server.CreateObject("ADODB.recordset")
set rsCallBundles = Server.CreateObject("ADODB.recordset")
rsCases.Open sqlCases, dbConn
rsCallBundles.Open sqlCallBundles, dbConn
%>
<body>
<h1>OMS All Active Cases and Call Bundles</h1>
<h3>Reporting database: <span style="color:Red;"><% Response.Write(dbConn.DefaultDatabase) %></span></h3>
    <table style="width: 600px;">
        <tr>
            <th style="width: 30px;" align="left">
                &nbsp;
            </th>
            <th style="width: 300px;" align="left">
                Case Number
            </th>
            <th style="width: 300px;" align='left'>
                Case Status
            </th>
        </tr>
<%
dim lineCount
lineCount = 1
do until rsCases.EOF
  Response.Write("        <tr>" & vbCrLf)
  Response.Write("          <td style='width: 30px;'>" & lineCount & "</td>" & vbCrLf)
  Response.Write("          <td style='width: 300px;'>" & rsCases.Fields.Item("casenum") & "</td>" & vbCrLf)
  Response.Write("          <td style='width: 300px;'>" & rsCases.Fields.Item("casestatus") & "</td>" & vbCrLf)
  Response.Write("        </tr>" & vbCrLf)
  lineCount = lineCount + 1
  rsCases.MoveNext
loop
Response.Write("        <tr><td colspan=3>***Call Bundles Waiting to be Predicted or Confirmed Below***</td></tr>" & vbCrLf)
do until rsCallBundles.EOF
  Response.Write("        <tr>" & vbCrLf)
  Response.Write("          <td style='width: 30px;'>" & lineCount & "</td>" & vbCrLf)
  Response.Write("          <td style='width: 300px;'>" & rsCallBundles.Fields.Item("casenum") & "</td>" & vbCrLf)
  Response.Write("          <td style='width: 300px;'>" & rsCallBundles.Fields.Item("casestatus") & "</td>" & vbCrLf)
  Response.Write("        </tr>" & vbCrLf)
  lineCount = lineCount + 1
  rsCallBundles.MoveNext
loop

rsCases.close
rsCallBundles.close
dbConn.close
%>
    </table>
</body>
<html>