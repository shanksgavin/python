<?php
//$q = intval($_GET['q']);

// make db connection
$dbconn = pg_connect("host='localhost' port='5432' dbname='cwf' user='postgres' password='usouth'");
if (!$dbconn) {
	echo "A  db connection error occurred!<br>\n";
	echo "<a href=\"http://modelserver/omsreports\">Click to go back to Modelserver</a>";
	exit;
} 

// obtain list of all audit tables
$sql_calls = "SELECT calls.customer, calls.street AS Address, to_char(min(date '1970-01-01' +  (calls.datecall/1000.||' seconds')::INTERVAL), 'MM/DD/YY HH:MIPM') as First_Called, count(calls.record_id) as Times_Called FROM calls WHERE ltrim(rtrim(upper(callstatus))) IN ('ACTIVE') AND calls.deleted=false GROUP BY calls.customer, calls.street, calls.account ORDER BY First_Called desc, customer asc";
$calls = pg_query($dbconn, $sql_calls);

if (!$calls) {
	echo "A sql execution error occurred while obtaing list of calls table.\n";
	exit;
}

// fetch all rows and content from executed sql
$calls_rs_field_count = pg_num_fields($calls);
$calls_rs_row_count = pg_num_rows($calls);
$calls_rs = pg_fetch_all($calls);

echo "<table border=1>\n";
echo "    <tr>\n";
if ($calls_rs_row_count < 1) {
    echo "        <th nowrap align='left'><h3>Active Calls</h3></th>\n";
    echo "    </tr><tr>\n";
    echo "        <td align='left'>No Active Calls in OMS at this time.</td>\n";
    echo "    </tr>\n";
} else {
    echo "        <th nowrap align='left' colspan='".$calls_rs_field_count."'><h3>Active Calls</h3></th>\n";
    echo "    </tr><tr>\n";
    for ($f=0; $f < $calls_rs_field_count; $f++) {
    	$fieldname_ = pg_field_name($calls, $f);
        echo "        <th nowrap>".$fieldname_."</th>\n";
    }
    echo "    </tr>\n";
    foreach ($calls_rs as $row) {
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
