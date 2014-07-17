<!DOCTYPE HTML>
<html>
<head>
<title>Reporting OMS Active Calls</title>
<link rel="stylesheet" type="text/css" href="OMSStyleSheet.css" />
</head>
<body>
<!--#include virtual="omsreports/dbConn.asp"-->
<%
'Open db connections to execute queries
dbConn.Open
sqlFields = "SELECT customer, phone AS Phone, street AS Address, datecall AS First_Called, record_id AS Times_Called FROM calls WHERE ltrim(rtrim(upper(callstatus))) IN ('ACTIVE') AND deleted=false LIMIT 1"
set rsFields = Server.CreateObject("ADODB.recordset")
rsFields.Open sqlFields, dbConn

'Query Company Name for Report
sqlCompanyName = "SELECT setup.company_name AS setup_company_name FROM public.setup setup"
set rsCompanyName = Server.CreateObject("ADODB.recordset")
rsCompanyName.Open sqlCompanyName, dbConn

'Begin to build table for presenting report
Response.Write("<table border=0>" & vbCrLf)
Response.Write("    <tr id='header' class='rowHeader'>" & vbCrLf)
Response.Write("        <td align='left' colspan=3 style='font-size:18px;'>" & rsCompanyName.Fields.Item("setup_company_name") & "</td>" & vbCrLf)
Response.Write("        <td align='right' colspan=3 style='font-size:28px; font-weight:bold;'>Active Calls</td>" & vbCrLf)
Response.Write("    </tr>" & vbCrLf)
rsCompanyName.Close

Response.Write("    <tr class='subheader'><td colspan=6>As of " & now & "</td></tr>" & vbCrLf)
'Test if query returned data.
'If False: Display a message indicating no data available
'If True: Execute detailed query and build table to display content
If rsFields.EOF Then
    'Display a message to user that no data was returned
    Response.Write("    <tr>" & vbCrLf)
    Response.Write("        <td>No Data Available In This Table</td>" & vbCrLf)
    Response.Write("    </tr>" & vbCrLf)
Else
    'Query data and build table to display
    sqlData = "SELECT calls.customer, case when length(ltrim(rtrim(calls.phone)))='10' then '(' ||SUBSTR(calls.phone,1,3)||')'||' '||SUBSTR(calls.phone,4,3)||'-'||SUBSTR(calls.phone,7,4) else calls.phone end AS Phone, calls.street AS Address, to_char(min(date '1970-01-01' +  (calls.datecall/1000.||' seconds')::INTERVAL), 'MM/DD/YY HH:MIPM') as First_Called, count(calls.record_id) as Times_Called FROM calls WHERE ltrim(rtrim(upper(callstatus))) IN ('ACTIVE') AND calls.deleted=false GROUP BY calls.customer, calls.street, Phone, calls.account ORDER BY calls.customer"
    set rsData = Server.CreateObject("ADODB.recordset")
    rsData.Open sqlData, dbConn

    Response.Write("    <tr align='left' style='text-transform:capitalize; background-color:#F0EFEF;' nowrap>" & vbCrLf)
    'Loop through recordset to obtain and print table headers
    do until rsFields.EOF
      Response.Write("        <th>&nbsp;</th>" & vbCrLf)
      for each x in rsFields.Fields
        Response.Write("        <th>" & replace(x.name, "_", " ") & "</th>" & vbCrLf)
      next
      rsFields.MoveNext
    loop
    Response.Write("    </tr>" & vbCrLf)
    'Create a counter to determine alternate table rows
    dim rowCounter
    rowCounter = 1
    do until rsData.EOF
      'Alternate table row background color
      If (rowCounter mod 2) = 0 Then
        Response.Write("    <tr class='alt'><td>" & rowCounter & "</td>" & vbCrLf)
      Else
        Response.Write("    <tr><td>" & rowCounter & "</td>" & vbCrLf)
      End If
      'Loop through recordset to print out all data
      'Test if data value returned is NULL replace with a placeholder
      'Also check for field "times_called" and center it within <td>
      for each y in rsData.Fields
        If (IsNull(y.value) OR y.value = "") Then
          Response.Write("        <td>&nbsp;</td>" & vbCrLf)
        ElseIf y.name = "times_called" Then
          Response.Write("        <td align='center'>" & y.value & "</td>" & vbCrLf)
        Else
          Response.Write("        <td nowrap>" & y.value & "</td>" & vbCrLf)
        End If
      next
      Response.Write("    </tr>" & vbCrLf)
      rowCounter = rowCounter + 1
      rsData.MoveNext
    loop
    rsData.close
End If
Response.Write("</table>")
rsFields.close
dbConn.close
%>
</body>
</html>