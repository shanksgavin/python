<!DOCTYPE HTML>
<html>
<head>
<title>Meade's Data Conversion</title>
<meta http-equiv="Content-Type" content="text/html;charset=UTF-8" />
<link rel="stylesheet" type="text/css" href="OMSStyleSheet.css" />
</head>
<body>
<H1>Meade's OMS Conversion from Trimble Data</H1>
<?php
// require database connection file
require('dbConnMeade.php');

$stmtOutageIDs = "select distinct(prikey) as outageid, troublecallcount from historic_data.historicaloutages group by prikey, troublecallcount order by troublecallcount desc";

// execute query to return audit trail
$queryOutageIDs = pg_query($dbconn, $stmtOutageIDs);

if (!$queryOutageIDs) {
	echo "A sql execution error occurred while getting OutageIDs <br>\n";
	echo $stmtOutageIDs;
	exit;
}

$rs_avail_outages = pg_fetch_all($queryOutageIDs);

// casenum
if ($_GET['outageid'] == ""){
	$outageid = "";
} else {
	$outageid = $_GET['outageid'];
}

?>
<form action="Meade_OMS_Conversion.php" method="get" name="details_form">
<h3>Reporting on OutageID: <span style="color:Red;">
	<select name="outageid" onchange="this.form.submit()">
<?php foreach ($rs_avail_outages as $outages) {
	if ($outageid == $outages['outageid']) {
		print "        <option value=\"".$outages['outageid']."\" selected=\"selected\">".$outages['outageid']." (".$outages['troublecallcount'].")</option>\n";
	} else {
		print "        <option value=\"".$outages['outageid']."\">".$outages['outageid']." (".$outages['troublecallcount'].")</option>\n";
	}
}?>
	</select>
	</span>
</h3>
</form>

<?php 
if ($outageid != "") {
	//$stmtOutCalls = "select * from historicaloutages as out join historicaltroublecalls as tc on out.prikey = tc.outageid where out.prikey = " . $outageid;
	$stmtOutage = "select * from historic_data.historicaloutages where prikey = ".$outageid;
	$stmtOutCalls = "select * from historic_data.historicaltroublecalls as tc where tc.outageid = " . $outageid . " order by creationdate asc";
	$stmtCustOuts = "select * from historic_data.historicalcustout as co where co.outageid = " . $outageid . " order by starttime asc";
	
	// execute query to return audit trail
	$queryOutage = pg_query($dbconn, $stmtOutage);
	$queryOutCalls = pg_query($dbconn, $stmtOutCalls);
	$queryCustOuts = pg_query($dbconn, $stmtCustOuts);
	
	// fetch all rows and content from executed sql
	$rs_field_count = pg_num_fields($queryOutCalls);
	$rs_row_count = pg_num_rows($queryOutCalls);
	$rs_custout_field_count = pg_num_fields($queryCustOuts);
	$rs_custout_row_count = pg_num_rows($queryCustOuts);
	
	if (!$queryOutCalls) {
		echo "A sql execution error occurred while getting Outage Calls <br>\n";
		echo $stmtOutCalls;
		exit;
	}
	
	if (!$queryCustOuts) {
		echo "A sql execution error occurred while getting CustOuts <br>\n";
		echo $stmtCustOuts;
		exit;
	}
	
	$rs_outage = pg_fetch_all($queryOutage);
	$rs_outage_calls = pg_fetch_all($queryOutCalls);
	$rs_custouts = pg_fetch_all($queryCustOuts);
	
	echo "<table border=1>\n";
	//Build Table to display Outage Information before listing associated calls
	echo "    <tr><th>PriKey (OutageID)</th><td>".$rs_outage[0]['prikey']."</td><th>Predicted Device</th><td>".$rs_outage[0]['predicteddevice']."</td><th>Last Modified</th><td>".$rs_outage[0]['lastmodified']."</td></tr>\n";
	echo "    <tr><th>Can Grow</th><td>".$rs_outage[0]['cangrow']."</td><th>Trouble Call Counts</th><td>".$rs_outage[0]['troublecallcount']."</td><th>Acknowledged Time</th><td>".$rs_outage[0]['acknowledgedtime']."</td></tr>\n";
	echo "    <tr><th>District</th><td>".$rs_outage[0]['district']."</td><th>Customers (Out) Counts</th><td>".$rs_outage[0]['customercount']."</td><th>Creation Date</th><td>".$rs_outage[0]['creationdate']."</td></tr>\n";
	echo "    <tr><th>Source</th><td>".$rs_outage[0]['source']."</td><th>Branch Cust Count</th><td>".$rs_outage[0]['branch_custcount']."</td><th>Crew Assigned Time</th><td>";
		if (is_null($rs_outage[0]['crewassignedtime'])) {
			echo "NULL";
		} else {
			echo $rs_outage[0]['crewassignedtime'];
		}
	echo "</td></tr>\n";
	echo "</table>\n";
	echo "<hr>\n";
	/********
	 * Start new dynamic html table for all calls in a case
	 */
	echo "<h3>Trouble Calls</h3>\n";
	if ($rs_row_count < 1) {
		//echo "        <th nowrap align='left'><h3>".strtoupper($atbl)."</h3></th>\n";
		//echo "    </tr><tr>\n";
		echo "<table border=1>\n";
		echo "    <tr>\n";
		echo "        <td align='left'>No Trouble Calls Involved in this Outage</td>\n";
		echo "    </tr>\n";
		echo "</table>\n";
	} else {
		echo "<table border=1>\n";
		//Build Table to list out all associated calls
		$rowcounter = 1;
		echo "    <tr>\n";
		echo "        <td>&nbsp;</td>\n";
		for ($f=0; $f < $rs_field_count; $f++) {
			$fieldname = pg_field_name($queryOutCalls, $f);
			echo "        <th nowrap>".$fieldname."</th>\n";
		}
		echo "    </tr>\n";
		
		foreach ($rs_outage_calls as $row) {
			echo "    <tr>\n";
			echo "        <td>".$rowcounter++."</td>\n";
			foreach ($row as $data) {
				If (is_null($data) || $data == "") {
					echo "        <td><NULL></NULL></td>\n";
				} else {
					echo "        <td nowrap>".$data."</td>\n";
				}
			}
			echo "    </tr>\n";
		}
		echo "</table><br>\n";
	}
	/********
	 * Start new dynamic html table for all custouts in a case
	*/
	echo "<hr />\n";
	echo "<h3>CustOuts</h3>\n";
	if ($rs_custout_row_count < 1) {
		//echo "        <th nowrap align='left'><h3>".strtoupper($atbl)."</h3></th>\n";
		//echo "    </tr><tr>\n";
		echo "<table border=1>\n";
		echo "    <tr>\n";
		echo "        <td align='left'>No Data Available In This Table</td>\n";
		echo "    </tr>\n";
		echo "</table>\n";
	} else {
		/********
		 * Start new dynamic html table for all custouts in a case
		*/
		echo "<table border=1 width=50%>\n";
		//Build Table to list out all associated calls
		$custout_rowcounter = 1;
		echo "    <tr>\n";
		echo "        <td>&nbsp;</td>\n";
		for ($y=0; $y < $rs_custout_field_count; $y++) {
			$fieldnameCustouts = pg_field_name($queryCustOuts, $y);
			echo "        <th nowrap>".$fieldnameCustouts."</th>\n";
		}
		echo "    </tr>\n";
		
		foreach ($rs_custouts as $row_custouts) {
			echo "    <tr>\n";
			echo "        <td>".$custout_rowcounter++."</td>\n";
			foreach ($row_custouts as $data) {
				If (is_null($data) || $data == "") {
					echo "        <td><NULL></NULL></td>\n";
				} else {
					echo "        <td>".$data."</td>\n";
				}
			}
			echo "    </tr>\n";
		}
		echo "</table><br>\n";
	}
	
	pg_close($dbconn);
} else {
	print "<h3>Nothing selected!</h3>";
}
	
?>
</body>
</html>