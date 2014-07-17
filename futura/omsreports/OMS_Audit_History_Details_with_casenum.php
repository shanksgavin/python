<!DOCTYPE HTML>
<?php
 
// set maximum number of records to be returned for performance
$maxRows = 100;

// get form variables
// audit table 
if ($_GET['t'] == ""){
	$atbl = "audit_customers";
} else {
	$atbl = $_GET['t'];
}
// casenum
if ($_GET['casenum'] == ""){
	$casenum = "";
} else {
	$casenum = $_GET['casenum'];
}

// require database connection file
//require('dbConn.php');
/*
$dbconn = pg_connect("host='localhost' port='5432' dbname='cwf' user='postgres' password='usouth'");
if (!$dbconn) {
	echo "A  db connection error occurred!\n";
	exit;
}
*/
require('dbConn.php');

?>
<head>
<title>OMS Audit Trail of <?php echo strtoupper($atbl); ?></title>
<meta http-equiv="Content-Type" content="text/html;charset=UTF-8" />
<link rel="stylesheet" type="text/css" href="OMSStyleSheet.css" />
</head>
<body>
<h1>OMS Audit Trail of <?php echo strtoupper($atbl); ?></h1>
<form action="OMS_Audit_History_Details.php" method="get" name="details_form">
<h3>CASENUM: <span style="color:Red;">
	<input type="hidden" name="t" value="<?php echo $atbl; ?>" />
	<input type="text" size="12" name="casenum" <?php if ($casenum != "") {echo "value=\"".$casenum."\"";} ?>" onchange="this.form.submit()" />
	<input type="submit" value="Submit" />
	</span>
</h3>
</form>
<?php 
// define sql to return all records from audit table
if ($casenum != ""){
	$where = " WHERE casenum = '".$casenum."' ";
} else {
	$where = "";
}

$stmtCount = "SELECT count(*) FROM ".$atbl.$where;

// execute query to return audit trail
$queryCount = pg_query($dbconn, $stmtCount);

if (!$queryCount) {
	echo "A sql execution error occurred while counting audit table ".$atbl.".<br>\n";
	echo $stmtCount;
	exit;
}

// get total row count from sql
$rs_total_row_count = pg_fetch_all($queryCount);
$total_row_count = $rs_total_row_count[0]['count'];

if ($total_row_count > $maxRows) {
	$stmt = "SELECT * FROM ".$atbl.$where." ORDER BY stamp desc limit ". $maxRows;
	// re-execute query to return audit trail
	$query = pg_query($dbconn, $stmt);
	if (!$query) {
		echo "A sql execution error occurred while retrieving TOP ".$maxRows." rows of audit table ".$atbl.".\n";
		exit;
	}
} else {
	$stmt = "SELECT * FROM ".$atbl." ORDER BY stamp desc";
	//echo $dbconn."<br>\n";
	echo $stmt."<br>\n";
	// re-execute query to return audit trail
	$query = pg_query($dbconn, $stmt);
	if (!$query) {
		echo "A sql execution error occurred while retrieving data from audit table ".$atbl.".<br>\n";
		exit;
	}
}
// fetch all rows and content from executed sql
$rs_field_count = pg_num_fields($query);
$rs_row_count = pg_num_rows($query);

// fetch all rows after double check of row count less than 25
// ivrcalls is currently > 200k and growing
// Sean suggsts that someone's integration is connected to my machine
// and I am not able to close the calls so they keep coming...
$rs = pg_fetch_all($query);

echo "<table border=1>\n";
echo "    <tr>\n";
if ($rs_row_count < 1) {
    echo "        <th nowrap align='left'><h3>".strtoupper($atbl)."</h3></th>\n";
    echo "    </tr><tr>\n";
    echo "        <td align='left'>No Data Available In This Table</td>\n";
    echo "    </tr>\n";
} else {
    echo "        <th nowrap align='left' colspan='".$rs_field_count."'><h3>".strtoupper($atbl)." (Top ".$rs_row_count." of ".$total_row_count." rows)</h3></th>\n";
    echo "    </tr><tr>\n";
    for ($f=0; $f < $rs_field_count; $f++) {
    	$fieldname = pg_field_name($query, $f);
        echo "        <th nowrap>".$fieldname."</th>\n";
    }
    echo "    </tr>\n";
    foreach ($rs as $row) {
        echo "    <tr>\n";
        foreach ($row as $data) {
            If (is_null($data) || $data == "") {
				echo "        <td>&nbsp;</td>\n";
            } else {
                echo "        <td nowrap>".$data."</td>\n";
            }
        }
    echo "    </tr>\n";
	}
}
echo "</table><br>\n";
pg_close($dbconn);
?>
<a href="//modelserver/omsreports">Home</a> | <a href="//modelserver/omsreports/OMS_Audit_History.php">OMS Audit History</a>
</body>
</html>