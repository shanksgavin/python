<html>
<head>
<title>OMS ASP Display Available Reports</title>
<meta http-equiv="Content-Type" content="text/html;charset=UTF-8" />
<link rel="stylesheet" type="text/css" href="OMSStyleSheet.css" />
</head>
<body>
<div class="left">
<table border="0">
	<tr><td><img src="Logo.jpg" alt="Futura Systems, Inc. Logo"/></td><td colspan="2"><h1>Report Listing</h1></td></tr>
	<tr align="left">
		<th colspan="2" width="50%">Report Name</th>
		<th width="50%">Last Modified</th>
	</tr>
<?php
$dir = './';
$files = scandir($dir);
unset($files[0]);
unset($files[1]);
foreach($files as $file){
	$path_parts = pathinfo($dir.$file);
	if ($path_parts['extension'] == 'pdf' || $path_parts['extension'] == 'html'){
		print("    <tr>\n");
		print("        <td colspan='2'><a href='$file'>".$file."</a></td>\n");
		if (time() - filemtime($file) > 432000){ 
		// 5 days converted to seconds (60*60*24*5)
			print("        <td class=\"filestamp\">".date("F d Y H:i:s", filemtime($file))."</td>\n");
		} else {
			print("        <td>".date("F d Y H:i:s", filemtime($file))."</td>\n");
		}
		print("    </tr>\n");
	}
}
?>
</table>
</div>
<div class='right'>
<table>
    <tr align="center"><td colspan="2"><h1>OMS Live Reports</h1></td></tr>
    <tr align="left"><th width="40%">Report Name</th><th width="60%">Description</th></tr>
    <tr valign="top"><td><a href="report7a.asp">Report 7a</a></td><td>Displays the 7a report.</td></tr>
    <tr valign="top"><td><a href="PastOutageCountsByCounty.asp">Past Outages By County</a></td><td>Display past outage counts grouped by county. Defaults to current month. Allows user to set a date range.</td></tr>
    <tr valign="top"><td><a href="ActiveOutageCountsByCounty.asp">Active Outages By County</a></td><td>Display active outage counts grouped by county.</td></tr>
    <tr valign="top"><td><a href="UniqueStatus.asp">Unique Status Values</a></td><td>Displays distinct status values for cases that are not deleted.</td></tr>
    <tr valign="top"><td><a href="UniqueCaseStatus.asp">Unique Case Status</a></td><td>Displays the unique status type for cases that are NOT deleted within db and totals each type</td></tr>
    <tr valign="top"><td><a href="AllUniqueCaseStatus.asp">All Unique Case Status</a></td><td>Displays the unique status type for ALL cases within db and totals each type</td></tr>
    <tr valign="top"><td><a href="CurrentPredictedCallBundles.asp">Currently Predicted Call Bundles</a></td><td>Displays active Call Bundles in the system. Refreshes every 15 seconds.</td></tr>
    <tr valign="top"><td><a href="CaseHistoryWithCallCounts.asp">Case History with Call Count</a></td><td>Displays history of cases with total number of calls associated with the case. Default sorted by largest calls per case.</td></tr>
    <tr valign="top"><td><a href="OMSTablesWithRowCounts.php">Tables with Row Count</a></td><td>Displays all available tables in OMS with row counts since last VACUUM. Default sorted by largest row count then table name alphabetically.</td></tr>
    <tr valign="top"><td><a href="OMSTestCaseCustomersUpdateOnPhaseChange.asp?casenum=0&autoRefresh=f">Testing Casescustomers Table Update</a></td><td>Testing Casescustomers table is updated when a Predicted/Confirmed Case has its phase changed.</td></tr>
    <tr valign="top"><td colspan="2"><hr /></td></tr>
    <tr valign="top"><td><a href="FuturaActiveCalls.asp">Futura Active Calls</a></td><td>Displays all active calls in OMS. This attempts to replace the Jasper Report of the same name.</td></tr>
    <tr valign="top"><td><a href="FuturaActiveCallsAutoRefresh.asp">Futura Active Calls Auto Refresh</a></td><td>Displays all active calls in OMS. This attempts to replace the Jasper Report of the same name. This report refreshes every 2 seconds.</td></tr>
    <tr valign="top"><td><a href="FuturaActiveCases.asp">Futura Active Cases</a></td><td>Displays all active cases in OMS ('Call Bundles', 'CauseFound', 'CauseUnknown', 'Predicted'). This report pulls cases from callbundles and cases tables</td></tr>
    <tr valign="top"><td><a href="OMSTablesWithCasenumField.asp">Tracking Active Rogue Case</a></td><td>Displays an active case in Report, but is not active in OMS Client.</td></tr>
    <tr valign="top"><td colspan="2"><hr /></td></tr>
    <tr valign="top"><td><a href="ChartingTest.asp">Chart Testing</a></td><td>Testing out Highcharts with IIS7 and ASP classic code.</td></tr>
    <tr valign="top"><td><a href="ClosedCaseCountsByCausePerYear.asp">Annual Outage Causes with Custhours</a></td><td>Displays Closed Case Causes with Total Outage Hours for every Year</td></tr>
    <tr valign="top"><td><a href="OMS_Audit_History.php">OMS Audit Trail - BETA</a></td><td>Displays results of selected OMS tables for auditing purposes.  Will be extra useful to hunt down when OMS writes to Customers table.</td></tr>
    <tr valign="top"><td><a href="Meade_OMS_Conversion.php">Meade's Data Conversion</a></td><td>Show Meade's Outages with all related Calls.</td></tr>
    <tr valign="top"><td><a href="oms_client_logs.php">Client's OMS Log Files</a></td><td>Display Client Log Files in a more friendly fashion.</td></tr>
    <tr valign="top"><td><a href="oms_dashboard.php">Interactive OMS Active Calls and Cases</a></td><td>Display Active OMS Calls and Cases interactively using AJAX</td></tr>
    <tr valign="top"><td><a href="customer_login_info.php">Client Info (FTA_OMSIMPL)</a></td><td>Display Client Information from OMSIMPL</td></tr>
    <tr valign="top"><td><a href="omswebmap_counts.php">OMS Webmap Data and Counts</a></td><td>Display OMSWebMap Active Outages and Affected Customers</td></tr>
</table>
</div>
</body>
</html>
