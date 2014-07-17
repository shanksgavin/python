<%@ Language="VBscript" %>
<!DOCTYPE HTML>
<html>
<head>
<title>Reporting Past Outages By County</title>
<!--#include virtual="omsreports/dbConn.asp"-->
<link rel="stylesheet" type="text/css" href="OMSStyleSheet.css"/>
<script language="javascript" type="text/javascript">
    function addLeadingZero(val) {
        var addLeadingZero = val;
        if (val < 10) {
            addLeadingZero = "0" + val;
        }
        return addLeadingZero;
    }

function validateForm() {
    var fObj = document.forms["outageCounts"];
    var startDate = Number(document.forms["outageCounts"]["startDate"].value);
    //var xStartDate = document.getElementById("startDate");
    var endDate = Number(document.forms["outageCounts"]["endDate"].value);
    //alert("Start Date Type: " + typeof (startDate) + "\n Start Date Value: " + startDate);

    if (isNaN(startDate)) {
        //var sd = startDate;
        var sd1 = new Date();
        startDate1 = sd1.getFullYear() + addLeadingZero(sd1.getMonth()+1) + addLeadingZero(sd1.getDate());
        fObj.elements["startDate"].value = startDate1;
        alert("Start Date was not correct and reformatted: " + startDate1);
        //return startDate
    }
    if (isNaN(endDate)) {
        endDate = Date(year, month, day);
        alert("End Date was not correct and reformatted: " + endDate);
    }
    if (startDate > endDate) {
        alert("Start is greater than End!");
        //confirm("Start Date must occur before End Date.\n Please click Cancel and correct Start Date.");
    }
}
</script>
</head>
<%
'Declare form variables
Dim startDate, endDate
Dim today, currentDay
today = Now
currentDay = Day(Now)-1

'Response.Write(today)

'Assign variables with form data
'Use Request.Form("name") with form method="POST"
'Use Request.QueryString("name") with form methos="GET"
startDate = Request.Form("startDate")
endDate = Request.Form("endDate")

'Response.Write("Start Date: " & startDate & "<br>" & vbCrLF)
'Response.Write("End Date: " & endDate & "<br>" & vbCrLF)

'Copied function from http://stackoverflow.com/questions/10580185/asp-formatting-date
function addLeadingZero(value)
    addLeadingZero = value
    if value < 10 then
        addLeadingZero = "0" & value
    end if
end function

'Check for dates. If no dates, set default dates
if startDate = "" then
    startDate = DateAdd("d", -currentDay, today)
    startDate = Year(startDate) & addLeadingZero(Month(startDate)) & addLeadingZero(Day(startDate))
end if

if endDate = "" then
    'endDate = today
    endDate = Year(today) & addLeadingZero(Month(today)) & addLeadingZero(Day(today))
end if

'Response.Write("Start Date After Checks: " & startDate & "<br>" & vbCrLF)
'Response.Write("End Date After Checks: " & endDate & "<br>" & vbCrLF)

dbConn.Open
sql = "SELECT DISTINCT(county) as county, COUNT(county) as outages from (select cc.customer, m.elementid, m.county from casescustomers cc, meterbase m, cases c where cc.customer = m.elementid AND cc.casenum = c.casenum AND c.casestatus ilike '%CLOSED%' AND cc.deleted = FALSE AND (c.datestrt>='" & startDate & "' and c.dateend<= '" & endDate & "')) AS customers GROUP BY customers.county ORDER BY customers.county ASC"
set rs = Server.CreateObject("ADODB.recordset")
rs.Open sql, dbConn
%>
<body>
<h1>OMS Past Outages By County</h1>
<h3>Reporting database: <span style="color:Red;"><% Response.Write(dbConn.DefaultDatabase) %></span></h3>
    <form action="OutageCountsByCounty.asp" method="post" id="outageCounts" name="outageCounts" onsubmit="validateForm()">
    <table style="width: 600px;">
        <tr>
            <th>Start Date: <input id="startDate" name="startDate" type="text" value="<% Response.Write(startDate) %>"/></th>
            <th>End Date: <input id="endDate" name="endDate" type="text" value="<% Response.Write(endDate) %>" /></th>
            <th><input id="submit" name="submit" type="submit" title="Get Outages" value="Get Outages" /></th>
        </tr>
        <tr>
            <td colspan="3" align="center">Date Format: yyyymmdd</td>
        </tr>

    </table>
    </form>
    <table style="width: 400px;">
        <tr>
            <th style="width: 200px;" align="left">
                County
            </th>
            <th style="width: 200px;" align='left'>
                Outages
            </th>
        </tr>
<%
dim county
do until rs.EOF
    if rs.Fields.Item("county") = "" then
        county = "<span style='color: red;'>No County Assigned</span>"
    else
        county = rs.Fields.Item("county")
    end if
    Response.Write("        <tr>" & vbCrLf)
    Response.Write("          <td style='width: 200px;'>" & county & "</td>" & vbCrLf)
    Response.Write("          <td style='width: 200px;'>" & rs.Fields.Item("outages") & "</td>" & vbCrLf)
    Response.Write("        </tr>" & vbCrLf)
    rs.MoveNext
loop

rs.close
dbConn.close
%>
    </table>
</body>
<html>