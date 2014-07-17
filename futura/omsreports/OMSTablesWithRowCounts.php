<!DOCTYPE HTML>
<head>
<title>Reporting OMS Tables with Row Counts since last DB VACUUM</title>
<meta http-equiv="Content-Type" content="text/html;charset=UTF-8" />
<link rel="stylesheet" type="text/css" href="OMSStyleSheet.css" />
</head>
<?php
//get form variables
if ($_POST['db_name'] == ""){
	$db_name = "omsprod";
} else {
	$db_name = $_POST['db_name'];
}

$dbconn_init = pg_connect("host='localhost' port='5432' dbname='postgres' user='postgres' password='usouth'");
if (!$dbconn_init) {
	echo "A  db connection error occurred!\n";
	exit;
}

$sql_avial_dbs = pg_query($dbconn_init, "select datname from pg_database where datistemplate = false order by datname asc");
if (!$sql_avial_dbs) {
	echo "A sql execution error occurred.\n";
	exit;
}

$rs_avail_dbs = pg_fetch_all($sql_avial_dbs);
//print_r($rs_avail_dbs);
?>
<body>
<h1>OMS Tables with Row Counts since last DB VACUUM</h1>
<form action="OMSTablesWithRowCounts.php" method="post" name="db_form">
<h3>Reporting database: <span style="color:Red;">
	<select name="db_name" onchange="this.form.submit()">
<?php foreach ($rs_avail_dbs as $db) {
	if ($db_name == $db['datname']) {
		print "        <option value=\"".$db['datname']."\" selected=\"selected\">".$db['datname']."</option>\n";
	} else {
		print "        <option value=\"".$db['datname']."\">".$db['datname']."</option>\n";
	}
}?>
	</select>
	</span>
</h3>
</form>
<?php 
// make db connection
$dbconn = pg_connect("host='localhost' port='5432' dbname='$db_name' user='postgres' password='usouth'");
if (!$dbconn) {
	echo "A  db connection error occurred!\n";
	exit;
}

// execute sql against db connection
$stmt = "SELECT c.relname as tblname, c.reltuples as tblRowCount FROM pg_catalog.pg_class c LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace WHERE n.nspname='public' AND c.relkind IN ('r','') AND n.nspname NOT IN ('pg_catalog', 'pg_toast', 'information_schema') ORDER BY c.reltuples DESC, c.relname ASC";
$sql = pg_query($dbconn, $stmt);
if (!$sql) {
	echo "A sql execution error occurred.\n";
	exit;
}

// fetch all rows and content from executed sql 
$rs = pg_fetch_all($sql);

?>
<table style="width: 500px;">
    <tr>
        <th width="100">
            &nbsp;
        </th>
        <th style="width: 200px;" align="left">
            Table Name
        </th>
        <th style="width: 200px;" align='left'>
            Number of Rows
        </th>
    </tr>

<?php 
echo "<h3>".$stmt."</h3>";
$rowCnt = 1;
foreach ($rs as $row) {
	echo "    <tr>\n";
    echo "        <td width=100>".$rowCnt."</td>\n";
    echo "        <td style='width: 200px;'><a href='OMSTableDataView10.php?tblName=".$row['tblname']."&db_name=".$db_name."'>".$row['tblname']."</a></td>\n";
    echo "        <td style='width: 200px;'>".$row['tblrowcount']."</td>\n";
    echo "    </tr>\n";
    $rowCnt = $rowCnt + 1;
}

// close db connections
pg_close($dbconn_init);
pg_close($dbconn);
?>
</table>
</body>
</html>