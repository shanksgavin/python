<%@ Language="VBscript" %>
<!--#include virtual="omsreports/dbConn.asp"-->
<!DOCTYPE HTML>
<html>
<head>
<title>Testing Casescustomers Table Updates</title>
<script type="text/javascript">
    function formSubmit() {
        document.getElementById("testDeletedClosedCases").submit();
    }
</script>
<%
'Open database connection
dbConn.Open

'Query Active Casenums
sqlCases = "select casenum from cases where deleted = '0' and casestatus IN ('CauseFound', 'CauseUnknown', 'Predicted') order by casenum asc"
set rsCases = Server.CreateObject("ADODB.recordset")
rsCases.Open sqlCases, dbConn

'Declare form variables
Dim tblName, auotRefresh, refreshRate, casenum, casestatus, getForm

'Determine if page has been viewed before
tblName = "casescustomers"
autoRefresh = ""
refreshRate = 0
casenum = ""

'Assign variables with form data
'Use Request.QueryString("name") with form methos="GET"
if isempty(autoRefresh) then
    autoRefresh = "f"
else
    autoRefresh = Request.QueryString("autoRefresh")
end if
    refreshRate = 10
if isempty(casenum) then
    casenum = "0"
else
    casenum = Request.QueryString("casenum")
end if
    getForm = "f"
else
    'Use Request.Form("name") with form method="POST"
    getForm = "f"
    'tblName = Request.Form("tblName")
    autoRefreshNDX = Request.Form("autoRefresh")
    response.write(TypeName(autoRefreshNDX) & " - " & Len(autoRefreshNDX))
    autoRefresh = Right(Request.Form("autoRefresh"),1)
    response.write(TypeName(autoRefresh) & " - " & autoRefresh & "<br />")
    refreshNDX = Request.Form("refreshRate").Count
    response.write(TypeName(refreshNDX) & " - " & refreshNDX)
    refreshRate = Request.Form("refreshRate")(refreshNDX)
    response.write(TypeName(refreshRate) & " - " & refreshRate & "<br />")
    casenum = Request.Form("casenum")
end if

if autoRefresh = "t" then
    Response.Write("<meta http-equiv='refresh' content='" & refreshRate & "'>" & vbCrLF)
end if
%>
</head>
<body>
<h1>OMS Testing Casescustomers Table Updates When Phase Changes On Case</h1>
<br />
<%
Response.Write("<form method='post' action='OMSTestCaseCustomersUpdateOnPhaseChange.asp' id='testDeletedClosedCases' name='testDeletedClosedCases'>" & vbCrLF)
Response.Write("<input type='hidden' name='getForm' value='" & getForm & "' />" & vbCrLF)
Response.Write("<input type='hidden' name='tblName' value='" & tblName & "' />" & vbCrLF)
Response.Write("<input type='hidden' name='autoRefresh' value='" & autoRefresh & "' />" & vbCrLF)
Response.Write("<input type='hidden' name='refreshRate' value='" & refreshRate & "' />" & vbCrLF)
Response.Write("<table><tr>" & vbCrLF)
Response.Write("    <td><select name='casenum'>" & vbCrLF)
do until rsCases.EOF
    if casenum = rsCases.Fields.Item("casenum") then
        Response.Write("        <option value='" & rsCases.Fields.Item("casenum") & "' selected='selected'>" & rsCases.Fields.Item("casenum") & "</option>" & vbCrLF)
    else
        Response.Write("        <option value='" & rsCases.Fields.Item("casenum") & "'>" & rsCases.Fields.Item("casenum") & "</option>" & vbCrLF)
    end if
    rsCases.MoveNext
loop
Response.Write("    </select></td>" & vbCrLF)
Response.Write("    <td><select name='autoRefresh'>" & vbCrLF)
if autoRefresh = "t" then
    Response.Write("        <option value='f'>FALSE</option><option value='t' selected='selected'>TRUE</option>" & vbCrLF)
else
    Response.Write("        <option value='f' selected='selected'>FALSE</option><option value='t'>TRUE</option>" & vbCrLF)
end if
Response.Write("    </select></td>" & vbCrLF)
Response.Write("    <td><select name='refreshRate'>" & vbCrLF)
'Define refreshRate increments
times=Array("5","10","15","30","60")
for each t in times
    if t = CStr(refreshRate) then
        Response.Write("        <option value=" & t & " selected='selected'> " & t & " Seconds</option>" & vbCrlF)
    else
        Response.Write("        <option value=" & t & "> " & t & " Seconds</option>" & vbCrlF)
    end if
next
Response.Write("    </select></td>" & vbCrLF)
Response.Write("    <td><input type='submit' value='Update' name='Update' onClick='formSubmit()' /></td>" & vbCrLF)
Response.Write("</tr></table>" & vbCrLF)
Response.Write("</form>" & vbCrLF)
%>
This page shows the data in casescustomers table for a specific casenum.<br />
If no data is showing, add "&casenum={paste a casenum}" onto the end of the URL<br />
<%
'let's now print out the received values in the browser
Response.Write("<b>Table Name: " & tblName & "</b><br>" & vbCrLf)

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
    sqlData = "SELECT * FROM " & tblName & " WHERE casenum like '" & casenum & "' ORDER BY casenum DESC"
    Response.Write("        <th nowrap align='left' colspan=30><h3>" & sqlData & "</h3></th>" & vbCrLf)
    set rsData = Server.CreateObject("ADODB.recordset")
    rsData.Open sqlData, dbConn

    Response.Write("    </tr><tr>" & vbCrLf)
    
    sqlDataCount = "SELECT count(*) FROM " & tblName & " WHERE casenum like '" & casenum & "'"
    set rsDataCount = Server.CreateObject("ADODB.recordset")
    rsDataCount.Open sqlDataCount, dbConn

    Response.Write("        <th nowrap align='center' colspan=30 ><h3 style='color: red;'>" & rsDataCount.Fields.Item(0) & " Total Calls involved in case</h3></th>" & vbCrLf)
    
    Response.Write("    </tr><tr>" & vbCrLf)
    Response.Write("        <th nowrap>&nbsp;</th>" & vbCrLf)
    do until rsFields.EOF
      for each x in rsFields.Fields
        Response.Write("        <th nowrap>" & x.name & "</th>" & vbCrLf)
      next
      rsFields.MoveNext
    loop
    Response.Write("    </tr>" & vbCrLf)
    dim rownum
    rownum = 0
    do until rsData.EOF
      rownum = rownum + 1
      Response.Write("    <tr><td>" & rownum & "</td>" & vbCrLf)
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
</html>