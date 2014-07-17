<?php
$dbconn = pg_connect("host='localhost' port='5432' dbname='oms_meade' user='postgres' password='usouth'");
if (!$dbconn) {
	echo "A db connection error occurred!<br>\n";
	echo "Suggestion: Make sure PostgreSQL is running.<br>\n";
	exit;
}
?>