<?php
// make db connection
/*
$dbconn = pg_connect("host='localhost' port='5432' dbname='cwf' user='postgres' password='usouth'");
if (!$dbconn) {
	echo "A  db connection error occurred!<br>\n";
	echo "<a href=\"http://modelserver/omsreports\">Click to go back to Modelserver</a>";
	exit;
}
*/
require("dbConn.php");

// obtain list of all audit tables
$sql_cases = "select record_id,
	casenum,
	casestatus
from staging_cases
union
select record_id,
	casenum,
	case when (repoweredby != '') then 'Switch' else casestatus end as casestatus
from cases
where casestatus not ilike '%Closed'
and deleted = False
order by casenum, record_id asc";
$cases = pg_query($dbconn, $sql_cases);

if (!$cases) {
	echo "A sql execution error occurred while obtaing list of calls table.\n";
	exit;
}

// fetch all rows and content from executed sql
$cases_rs_field_count = pg_num_fields($cases);
$cases_rs_row_count = pg_num_rows($cases);
$cases_rs = pg_fetch_all($cases);

echo "<table border=1>\n";
echo "    <tr>\n";
if ($cases_rs_row_count < 1) {
    echo "        <th nowrap align='left'><h3>Active Cases</h3></th>\n";
    echo "    </tr><tr>\n";
    echo "        <td align='left'>No Active Cases in OMS at this time.</td>\n";
    echo "    </tr>\n";
} else {
    echo "        <th nowrap align='left' colspan='".$cases_rs_field_count."'><h3>Active Cases  (".$cases_rs_row_count.")</h3></th>\n";
    echo "    </tr><tr>\n";
    for ($f=0; $f < $cases_rs_field_count; $f++) {
    	$fieldname_ = pg_field_name($cases, $f);
        echo "        <th nowrap>".$fieldname_."</th>\n";
    }
    echo "    </tr>\n";
    foreach ($cases_rs as $row) {
        $record_id = $row[record_id];
        $org_record_id = $row[org_record_id];
        $casestatus = $row[casestatus];
        if ($casestatus == 'callbundle') {
        	echo "    <tr class=\"callbundle\">\n";
        } elseif ($casestatus == 'Predicted') {
        	echo "    <tr class=\"predicted\">\n";
        } elseif ($casestatus == 'CauseFound') {
        	echo "    <tr class=\"causefound\">\n";
        } elseif ($casestatus == 'CauseUnknown') {
        	echo "    <tr class=\"causeunknown\">\n";
        } elseif ($casestatus == 'Switch') {
        	echo "    <tr class=\"switch\">\n";
        } else {
        	echo "    <tr class=\"other\">\n";
        }
        foreach ($row as $data) {
            If (is_null($data) || $data == "") {
				echo "        <td width=115>&nbsp;</td>\n";
            } else {
	            echo "        <td width=115 nowrap>".$data."</td>\n";
            }
        }
    echo "    </tr>\n";
	}
}
echo "</table><br>\n";

pg_close($dbconn);
?> 
