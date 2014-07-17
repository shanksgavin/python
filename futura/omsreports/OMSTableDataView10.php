<!DOCTYPE HTML>
<head>
<title>Reporting OMS Table Data Top 10 Rows</title>
<meta http-equiv="Content-Type" content="text/html;charset=UTF-8" />
<link rel="stylesheet" type="text/css" href="OMSStyleSheet.css" />
</head>
<body>
<h1>OMS Table Data Top 10 Rows</h1>
<?php 
//Assign variables with form data
$tblName = strtolower($_GET['tblName']);
$db_name = strtolower($_GET['db_name']);

//let's now print out the received values in the browser
echo "Table Name: ".$tblName."<br>\n";
echo "DB Name   : ".$db_name."<br>\n";

// make db connection
$dbconn = pg_connect("host='localhost' port='5432' dbname='$db_name' user='postgres' password='usouth'");
if (!$dbconn) {
	echo "A  db connection error occurred!\n";
	exit;
}

// execute sql against db connection
$stmt = "SELECT * FROM ".$tblName." LIMIT 10";
$sql = pg_query($dbconn, $stmt);
if (!$sql) {
	echo "A sql execution error occurred.\n";
	exit;
}

// fetch all rows and content from executed sql 
$rs_field_count = pg_num_fields($sql);
$rs_row_count = pg_num_rows($sql);
$rs = pg_fetch_all($sql);

echo "<table border=1>\n";
echo "    <tr>\n";
if ($rs_row_count < 1) {
    echo "        <th nowrap><h3>".$stmt."</h3></th>\n";
    echo "    </tr><tr>\n";
    echo "        <td>No Data Available In This Table</td>\n";
    echo "    </tr>\n";
} else {
    echo "        <th nowrap align='left' colspan='".$rs_field_count."'><h3>".$stmt."</h3></th>\n";
    echo "    </tr><tr>\n";
    for ($f=0; $f < $rs_field_count; $f++) {
    	$fieldname = pg_field_name($sql, $f);
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
echo "</table>\n";
pg_close($dbconn);
?>
<a href="//modelserver/omsreports">Home</a>
</body>
</html>