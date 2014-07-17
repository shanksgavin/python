<!DOCTYPE html>
<html>
<head>
<title>OMS Webmap Affected Customers (fta_williamg::coweta-fayette)</title>
<meta http-equiv="refresh" content="30">
<link rel="stylesheet" type="text/css" href="OMSStyleSheet.css" />
</head>
<body>
<h1>Displaying Affected Customers from Views (Staging Data)</h1>
<?php
$dbconn = pg_connect("host='fta_williamg' port='5432' dbname='coweta-fayette' user='postgres' password='usouth'");
if (!$dbconn) {
	echo "A db connection error occurred!<br>\n";
	echo "Suggestion: Make sure PostgreSQL is running.<br>\n";
	echo "<a href=\"http://modelserver/omsreports\">Click to go back to Modelserver</a>";
	exit;
}
/*********************************************************************/
// Obtain Custout Count
$sql_cc = "SELECT COUNT(*) FROM public.staging_casescustomers";
$cc = pg_query($dbconn, $sql_cc);
if (!$cc) {
	echo "A sql execution error occurred while obtaing custout count.\n";
	exit;
}
// fetch custout count
$cc_rs = pg_fetch_all($cc);
$custouts = $cc_rs[0]["count"];
/*********************************************************************/
// Obtain webmap_update_interval
$sql_webmap_update_interval = "SELECT setting_value FROM public.settings WHERE setting_name = 'webmap_update_interval'";
$wui = pg_query($dbconn, $sql_webmap_update_interval);
if (!$wui) {
	echo "A sql execution error occurred while obtaing webmap_update_interval.\n";
	exit;
}
// fetch webmap_update_interval
$wui_rs = pg_fetch_all($wui);
$webmap_update_interval = $wui_rs[0]["setting_value"];
/*********************************************************************/
// Obtain webmap_update_interval_busy
$sql_webmap_update_interval_busy = "SELECT setting_value FROM public.settings WHERE setting_name = 'webmap_update_interval_busy'";
$wuib = pg_query($dbconn, $sql_webmap_update_interval_busy);
if (!$wuib) {
	echo "A sql execution error occurred while obtaing webmap_update_interval_busy.\n";
	exit;
}
// fetch webmap_update_interval_busy
$wuib_rs = pg_fetch_all($wuib);
$webmap_update_interval_busy = $wuib_rs[0]["setting_value"];
/*********************************************************************/
// Display Staging_Info data
$sql_si = "SELECT * FROM public.staging_info";
$si = pg_query($dbconn, $sql_si);
if (!$si) {
	echo "A sql execution error occurred while obtaing staging_info data.\n";
	exit;
}
// fetch data from $si
$si_row_count = pg_num_rows($si);
$si_rs = pg_fetch_all($si);
/*********************************************************************/
$busy_threshold = $si_rs[0]["busy_threshold"];
$last_update_str = $si_rs[0]["last_update_time_ts"];
$next_update_str = $si_rs[0]["next_update_time_ts"];
$last_update = strtotime($last_update_str);
$next_update = strtotime($next_update_str);

$time_interval_mins = ($next_update - $last_update)/60;

echo "<h2>Last Update was ".$last_update_str."; Next Updated at ".$next_update_str."; Diff: ".$time_interval_mins." mins</h2>\n";
// Test if OMS is busy based on custout value
if ($custouts >= $busy_threshold) {
	// Test if busy interval matches staging_info timestamps between last and next updates
	if ($webmap_update_interval_busy == $time_interval_mins) {
		echo "<span class=\"green\"><h2>Busy -- Next Update in ".$webmap_update_interval_busy." minute(s)</h2></span><br>\n";
	} else {
		echo "<span class=\"red\"><h2>Busy -- Next Update in ".$webmap_update_interval_busy." minute(s)</h2></span><br>\n";
	}
} else {
	if ($webmap_update_interval == $time_interval_mins) {
		echo "<span class=\"green\"><h2>Next Update in ".$webmap_update_interval." minute(s)</h2></span><br>\n";
	} else {
		echo "<span class=\"red\"><h2>Next Update in ".$webmap_update_interval." minute(s)</h2></span><br>\n";
	}
}


// obtain list of all cases
$sql_outagecases = "SELECT * FROM public.outagecases ORDER BY timestrt"; //Selecting from VIEW
$outagecases = pg_query($dbconn, $sql_outagecases);
$sql_affected_customers = "SELECT SUM(custcount) FROM public.outagecases"; //Selecting from VIEW
$affected_customers = pg_query($dbconn, $sql_affected_customers);

if (!$outagecases) {
	echo "A sql execution error occurred while obtaing outagecases data.\n";
	exit;
}
if (!$affected_customers) {
	echo "A sql execution error occurred while obtaing affected_customers data.\n";
	exit;
}

// fetch all rows and content for Active Outage Cases
$outagecases_rs_field_count = pg_num_fields($outagecases);
$outagecases_rs_row_count = pg_num_rows($outagecases);
$outagecases_rs = pg_fetch_all($outagecases);
$colspan = $outagecases_rs_field_count + 1;
$lineNumber = 0;

// fetch total Affected Customers
$affected_customers_rs = pg_fetch_result($affected_customers, 0, 0);

echo "<table border=1>\n";
echo "    <tr>\n";
if ($outagecases_rs_row_count < 1) {
	echo "        <th nowrap align='left'><h3>Active Outages</h3></th>\n";
	echo "    </tr><tr>\n";
	echo "        <td align='left'>No Data Available At This Time --Check System--</td>\n";
	echo "    </tr>\n";
} else {
	echo "        <th nowrap align='center' colspan='".$colspan."'><h2>Active Outages (".$outagecases_rs_row_count.") affecting ". $affected_customers_rs ." customers</h2></th>\n";
	echo "    </tr><tr><td>&nbsp;</td>\n";
	for ($f=0; $f < $outagecases_rs_field_count; $f++) {
		$fieldname_ = pg_field_name($outagecases, $f);
		echo "        <th nowrap>".strtoupper($fieldname_)."</th>\n";
	}
	echo "    </tr>\n";
	foreach ($outagecases_rs as $row) {
		echo "    <tr>\n";
		echo "        <td>".++$lineNumber."</td>\n";
		$fieldndx = 0;
		foreach ($row as $data) {
			if ($fieldndx == 0) {
				$fieldwidth = 300;
			} else {
				$fieldwidth = 115;
			}
			If (is_null($data) || $data == "") {
				echo "        <td width=".$fieldwidth.">&nbsp;</td>\n";
			} else {
				echo "        <td width=".$fieldwidth." nowrap>".$data."</td>\n";
			}
			$fieldndx++;
		}
		echo "    </tr>\n";
	}
}
echo "</table><br>\n";

pg_close($dbconn);
?>
</body>
</html>