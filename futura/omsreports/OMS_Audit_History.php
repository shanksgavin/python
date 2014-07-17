<!DOCTYPE HTML>
<?php 
// make db connection
/*
$dbconn = pg_connect("host='localhost' port='5432' dbname='cwf' user='postgres' password='usouth'");
if (!$dbconn) {
	echo "A  db connection error occurred!\n";
	exit;
}
*/
require('dbConn.php');


// obtain list of all audit tables
$audit_sql = "SELECT c.relname 
		FROM pg_catalog.pg_class c 
		LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace 
		WHERE n.nspname='oms_audits' 
		AND c.relkind IN ('r','') 
		AND n.nspname NOT IN ('pg_catalog', 'pg_toast', 'information_schema')
		AND c.relname ilike 'audit%'
		ORDER BY c.relname ASC";
$audit = pg_query($dbconn, $audit_sql);

if (!$audit) {
	echo "A sql execution error occurred while obtaing list of audit tables.\n";
	exit;
}

// fetch all rows and content from executed sql 
$audit_rs_field_count = pg_num_fields($audit);
$audit_rs_row_count = pg_num_rows($audit);
$audit_rs = pg_fetch_all($audit);
//print_r($audit_rs);
?>
<head>
<title>OMS Audit Trail of <?php echo $audit_rs_row_count; ?> Tables</title>
<meta http-equiv="Content-Type" content="text/html;charset=UTF-8" />
<link rel="stylesheet" type="text/css" href="OMSStyleSheet.css" />
</head>
<body>
<h1>OMS Audit Trail of <?php echo $audit_rs_row_count; ?> Tables</h1>
<table width=500>
<?php 
// loop thru each found audit table
$tableCounter = 0;
foreach ( $audit_rs as $atbl) {
	// define sql to return all records from audit table
	$stmt = "SELECT count(*) FROM oms_audits.".$atbl['relname'];
	// execute query to return audit trail
	$query = pg_query($dbconn, $stmt);
	
	if (!$query) {
		echo "A sql execution error occurred while retrieving audit table '".$atbl['relname']."'.<br>\n";
		//print_r($atbl);
		exit;
	}
	
	// fetch all rows and content from executed sql
	$rs_field_count = pg_num_fields($query);
	$rs_row_count = pg_num_rows($query);
	$rs = pg_fetch_all($query);
	//print_r($rs);
	foreach ($rs as $row) {
		$tableCounter++;
		echo "    <tr>\n";
        foreach ($row as $data) {
            If (is_null($data) || $data == "") {
				echo "        <td colspan=3>No Data Was Found</td>\n";
            } else {
                echo "        <td>".$tableCounter."</td><td><a href='OMS_Audit_History_Details.php?t=".$atbl['relname']."'>".$atbl['relname']."</a></td><td>(".$data." rows)</td>\n";
            }
        }
        echo "</tr>\n";
    }
}
pg_close($dbconn);
?>
</table>
<a href="//modelserver/omsreports">Home</a>
</body>
</html>