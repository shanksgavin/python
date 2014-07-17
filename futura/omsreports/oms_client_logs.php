<?php 
//get form variables
if ($_POST['db_name'] == ""){
	$db_name = "wiregrass_2_2_0_84";
	$db_name_old = "";
} else if ($_POST['db_name'] != $_POST['db_name_old']){
	$db_name = $_POST['db_name'];
	$selected_report_day = "default";
	$selected_start_time = "default";
	$selected_end_time = "default";
} else {
	$db_name = $_POST['db_name'];
}
//$selected_report_day
if ($_POST['selected_report_day'] == ""){
	$selected_report_day = "default";
} else {
	$selected_report_day = $_POST['selected_report_day'];
}
//$selected_start_time
if ($_POST['selected_start_time'] == ""){
	$selected_start_time = "default";
} else {
	$selected_start_time = $_POST['selected_start_time'];
}
//$selected_end_time
if ($_POST['selected_end_time'] == ""){
	$selected_end_time = "default";
} else {
	$selected_end_time = $_POST['selected_end_time'];
}


// Make connection to localhost database
$dbconn_init = pg_connect("host='localhost' port='5432' dbname='".$db_name."' user='postgres' password='usouth'");
if (!$dbconn_init) {
	echo "A db connection error occurred!\n";
	exit;
}

// Query all available databases on localhost
$sql_avail_dbs = pg_query($dbconn_init, "select datname from pg_database where datistemplate = false order by datname asc");
if (!$sql_avail_dbs) {
	echo "A sql execution error occurred (Getting Available Databases.\n";
	exit;
}
// Fetch all database names to build select list
$rs_avail_dbs = pg_fetch_all($sql_avail_dbs);

// Query all available days to generate a report
$sql_avail_days = pg_query($dbconn_init, "select available_report_dates from oms_logfiles.available_report_dates order by available_report_dates desc");
if (!$sql_avail_days) {
	echo "A sql execution error occurred (Getting Available Reporting Days).\n";
	exit;
}
// Fetch all Report Days to build select list
$rs_avail_days = pg_fetch_all($sql_avail_days);

if ($selected_report_day != "default"){
	// Query all available minutes in the selected day to generate a report
	$sql_avail_minutes = pg_query($dbconn_init, "select available_report_minutes from oms_logfiles.available_report_minutes where available_report_dates = '".$selected_report_day."' order by available_report_minutes asc");
	if (!$sql_avail_minutes) {
		echo "A sql execution error occurred (Getting Available Reporting Minutes For Selected Day).\n";
		exit;
	}
	// Fetch all Report Days to build select list
	$rs_avail_minutes = pg_fetch_all($sql_avail_minutes);
}

if ($selected_report_day != "default" && $selected_start_time != "default" && $selected_end_time != "default"){
	// Query all available minutes in the selected day to generate a report data
	$sql_log_minutes = pg_query($dbconn_init, "select available_report_minutes from oms_logfiles.available_report_minutes where available_report_dates = '".$selected_report_day."' and available_report_minutes between '".$selected_start_time."' and '".$selected_end_time."' order by available_report_minutes asc");
	if (!$sql_log_minutes) {
		echo "A sql execution error occurred (Available Minutes on Selected Day).\n";
		exit;
	}
	// Fetch all Report Days to build select list
	$rs_log_minutes = pg_fetch_all($sql_log_minutes);
	
	// Query only ObjectModel Logs in the selected day to generate a report data
	$sql_ObjectModel_minutes = pg_query($dbconn_init, "select minute_, tpm from oms_logfiles.objectmodel_transactions_per_minute where date_ = '".$selected_report_day."' and minute_ between '".$selected_start_time."' and '".$selected_end_time."' order by minute_ asc");
	if (!$sql_ObjectModel_minutes) {
		echo "A sql execution error occurred (ObjectModel Minutes on Selected Day).\n";
		echo "Start: ".$selected_start_time."\n";
		echo "End: ".$selected_end_time."\n";
		exit;
	}
	// Fetch all ObjectModel Log Entries to build chart data
	$rs_ObjectModel_minutes = pg_fetch_all($sql_ObjectModel_minutes);
	
	// Query only SaveData Logs in the selected day to generate a report data
	$sql_SaveData_minutes = pg_query($dbconn_init, "select minute_, tpm from oms_logfiles.savedata_transactions_per_minute where date_ = '".$selected_report_day."' and minute_ between '".$selected_start_time."' and '".$selected_end_time."' order by minute_ asc");
	if (!$sql_SaveData_minutes) {
		echo "A sql execution error occurred (SaveData Minutes on Selected Day).\n";
		exit;
	}
	// Fetch all SaveData Log Entries to build chart data
	$rs_SaveData_minutes = pg_fetch_all($sql_SaveData_minutes);
	
	// Query only Client Logs in the selected day to generate a report data
	$sql_Client_minutes = pg_query($dbconn_init, "select minute_, tpm from oms_logfiles.client_transactions_per_minute where date_ = '".$selected_report_day."' and minute_ between '".$selected_start_time."' and '".$selected_end_time."' order by minute_ asc");
	if (!$sql_Client_minutes) {
		echo "A sql execution error occurred (Client Minutes on Selected Day).\n";
		exit;
	}
	// Fetch all Client Log Entries to build chart data
	$rs_Client_minutes = pg_fetch_all($sql_Client_minutes);
}
?>
<!DOCTYPE html>
<head>
<title>OMS Client Logs on Display</title>
<meta http-equiv="Content-Type" content="text/html;charset=UTF-8" />
<link rel="stylesheet" type="text/css" href="OMSStyleSheet.css" />
<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>
<script src="../Highcharts-3.0.0/js/highcharts.js" type="text/javascript"></script>
<script src="../Highcharts-3.0.0/js/modules/exporting.js" type="text/javascript"></script>
</head>
<body>
<h1>OMS Log File Stats from Client's Server</h1>
<form action="oms_client_logs.php" method="post" name="db_form">
<?php echo "<input type=\"hidden\" name=\"db_name_old\" value=\"".$db_name."\">"; ?>
<table width=800>
	<tr>
		<td width=250><h3>Reporting Database:</h3></td>
		<td width=200><select name="db_name" onchange="this.form.submit()">
		<?php foreach ($rs_avail_dbs as $db) {
			if ($db_name == $db['datname']) {
				print "        <option value=\"".$db['datname']."\" selected=\"selected\">".$db['datname']."</option>\n";
			} else {
				print "        <option value=\"".$db['datname']."\">".$db['datname']."</option>\n";
			}
		}?>
		</select></td>
		<td width=150><h3>Start Time:</h3></td>
		<td width=200><select name="selected_start_time" onchange="this.form.submit()">
			<option value="default">Choose Start Time</option>
		<?php foreach ($rs_avail_minutes as $start_time) {
			if ($selected_start_time == $start_time['available_report_minutes']) {
				print "        <option value=\"".$start_time['available_report_minutes']."\" selected=\"selected\">".$start_time['available_report_minutes']."</option>\n";
			} else {
				print "        <option value=\"".$start_time['available_report_minutes']."\">".$start_time['available_report_minutes']."</option>\n";
			}
		}?>
		</select></td>
	</tr>
	<tr>
		<td width=250><h3>Available Days to Report:</h3>
		<td width=200><select name="selected_report_day" onchange="this.form.submit()">
			<option value="default">Choose Report Date</option>
		<?php foreach ($rs_avail_days as $report_day) {
			if ($selected_report_day == $report_day['available_report_dates']) {
				print "        <option value=\"".$report_day['available_report_dates']."\" selected=\"selected\">".$report_day['available_report_dates']."</option>\n";
			} else {
				print "        <option value=\"".$report_day['available_report_dates']."\">".$report_day['available_report_dates']."</option>\n";
			}
		}?>
		</select></td>
		<td width=150><h3>End Time:</h3>
		<td width=200><select name="selected_end_time" onchange="this.form.submit()">
			<option value="default">Choose End Time</option>
		<?php foreach ($rs_avail_minutes as $end_time) {
			if ($selected_end_time == $end_time['available_report_minutes']) {
				print "        <option value=\"".$end_time['available_report_minutes']."\" selected=\"selected\">".$end_time['available_report_minutes']."</option>\n";
			} else {
				print "        <option value=\"".$end_time['available_report_minutes']."\">".$end_time['available_report_minutes']."</option>\n";
			}
		}?>
		</select></td>
	</tr>
</table>
</form>
<?php
if ($selected_report_day != "default" && $selected_start_time != "default" && $selected_end_time != "default"){
	print("<script type='text/javascript'>\n");
	print("$(document).ready(function() {\n");
	print("    $('#container').highcharts({\n");
	print("        chart: {\n");
	print("            type: 'column'\n");
	print("        },\n");
	print("        title: {\n");
	print("            text: 'OMS Server Activity on ".$selected_report_day." from Log Files'\n");
	print("        },\n");
	print("        xAxis: {\n");
	print("            categories: ["); // loop thru all log minutes returned from sql
	$category_data = "";
	foreach ($rs_log_minutes as $log_minute) {
		$category_data = $category_data."'".$log_minute['available_report_minutes']."',";
		}
	$category_data = substr($category_data, 0, -1);
	print($category_data."],\n");
	print("            labels: {\n");
	print("                rotation: -80,\n");
	print("                align: 'right'\n");
	print("            }\n");
	print("        },\n");
	print("        yAxis: {\n");
	print("            min: 0,\n");
	print("            title: {\n");
	print("                text: 'Transactions per Minute'\n");
	print("            },\n");
	print("            stackLabels: {\n");
	print("                enabled: true,\n");
	print("                style: {\n");
	print("	                   fontWeight: 'bold',\n");
	print("	                   color: (Highcharts.theme && Highcharts.theme.textColor) || 'gray'\n");
	print("                }\n");
	print("            }\n");
	print("        },\n");
	print("        legend: {\n");
	print("	           align: 'right',\n");
	print("	           x: -70,\n");
	print("	           verticalAlign: 'top',\n");
	print("	           y: 20,\n");
	print("	           floating: true,\n");
	print("	           backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColorSolid) || 'white',\n");
	print("	           borderColor: '#CCC',\n");
	print("	           borderWidth: 1,\n");
	print("	           shadow: false\n");
	print("        },\n");
	print("        tooltip: {\n");
	print("	           formatter: function() {\n");
	print("		           return '<b>'+ this.x +'</b><br/>'+\n");
	print("		               this.series.name +': '+ this.y +'<br/>'+\n");
	print("		               'Total: '+ this.point.stackTotal;\n");
	print("	           }\n");
	print("        },\n");
	print("        plotOptions: {\n");
	print("	           column: {\n");
	print("		           stacking: 'normal',\n");
	print("		           dataLabels: {\n");
	print("			           enabled: true,\n");
	print("			           color: (Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white',\n");
	print("			           style: {\n");
	print("				           textShadow: '0 0 3px black, 0 0 3px black'\n");
	print("			           }\n");
	print("		           }\n");
	print("	           }\n");
	print("        },\n");
	print("        series: [{\n");
	print("	           name: 'ObjectModel',\n");
	print("	           data: [");
	$objectmodel_counter = 0;
	$objectmodel_data = "";
	foreach ($rs_log_minutes as $log_minute) {
		if ($log_minute['available_report_minutes'] == $rs_ObjectModel_minutes[$objectmodel_counter]['minute_']) {
			$objectmodel_data = $objectmodel_data.$rs_ObjectModel_minutes[$objectmodel_counter]['tpm'].",";
			$objectmodel_counter++;
			} else {
			$objectmodel_data = $objectmodel_data."0,";
			}
		}
	$objectmodel_data = substr($objectmodel_data, 0, -1);
	print($objectmodel_data."]\n");
	print("        }, {\n");
	print("	           name: 'SaveData',\n");
	print("	           data: [");
	$savedata_counter = 0;
	$savedata_data = "";
	foreach ($rs_log_minutes as $log_minute) {
		if ($log_minute['available_report_minutes'] == $rs_SaveData_minutes[$savedata_counter]['minute_']) {
			$savedata_data = $savedata_data.$rs_SaveData_minutes[$savedata_counter]['tpm'].",";
			$savedata_counter++;
		} else {
			$savedata_data = $savedata_data."0,";
		}
	}
	$savedata_data = substr($savedata_data, 0, -1);
	print($savedata_data."]\n");
	print("        }, {\n");
	print("	           name: 'Client',\n");
	print("	           data: [");
	$client_counter = 0;
	$client_data = "";
	foreach ($rs_log_minutes as $log_minute) {
		if ($log_minute['available_report_minutes'] == $rs_Client_minutes[$client_counter]['minute_']) {
			$client_data = $client_data.$rs_Client_minutes[$client_counter]['tpm'].",";
			$client_counter++;
		} else {
			$client_data = $client_data."0,";
		}
	}
	$client_data = substr($client_data, 0, -1);
	print($client_data."]\n");
	print("        }]\n");
	print("    });\n");
	print("});\n");
	print("</script>\n");
	//print($selected_report_day);
} else {
	print("Please select a report date.");
}
?>
<div id="container">
</div>
</body>
<?php 
pg_close($dbconn_init)
?>
</html>