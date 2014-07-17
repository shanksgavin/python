<?php
$dbconn = pg_connect("host='localhost' port='5432' dbname='coweta-fayette' user='postgres' password='usouth'");
if (!$dbconn) {
	echo "A db connection error occurred!<br>\n";
	echo "Suggestion: Make sure PostgreSQL is running.<br>\n";
	echo "<a href=\"http://modelserver/omsreports\">Click to go back to Modelserver</a>";
	exit;
}
?>