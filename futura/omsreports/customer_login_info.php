<?php
$dbconn = pg_connect("host='fta_omsimpl' port='5432' dbname='implserver' user='postgres' password='gis123!@#'");
if (!$dbconn) {
	echo "A db connection error occurred!<br>\n";
	echo "Suggestion: Make sure PostgreSQL is running.<br>\n";
	echo "<a href=\"http://modelserver/omsreports\">Click to go back to Modelserver</a>";
	exit;
}

// obtain list of all audit tables
$sql_customer_login_info = "SELECT * FROM customer_login_info"; //Selecting from VIEW
$customer_login_info = pg_query($dbconn, $sql_customer_login_info);

if (!$customer_login_info) {
	echo "A sql execution error occurred while obtaing list of calls table.\n";
	exit;
}

// fetch all rows and content from executed sql
$customer_login_info_rs_field_count = pg_num_fields($customer_login_info);
$customer_login_info_rs_row_count = pg_num_rows($customer_login_info);
$customer_login_info_rs = pg_fetch_all($customer_login_info);
$colspan = $customer_login_info_rs_field_count + 1;
$lineNumber = 0;

echo "<table border=1>\n";
echo "    <tr>\n";
if ($customer_login_info_rs_row_count < 1) {
	echo "        <th nowrap align='left'><h3>Client Login Information</h3></th>\n";
	echo "    </tr><tr>\n";
	echo "        <td align='left'>No Data Available At This Time --Check System--</td>\n";
	echo "    </tr>\n";
} else {
	echo "        <th nowrap align='left' colspan='".$colspan."'><h3>Login Information for ".$customer_login_info_rs_row_count." Clients</h3></th>\n";
	echo "    </tr>\n";
	for ($f=0; $f < $customer_login_info_rs_field_count; $f++) {
		$fieldname_ = pg_field_name($customer_login_info, $f);
		echo "        <th nowrap>".strtoupper($fieldname_)."</th>\n";
	}
	echo "    </tr>\n";
	foreach ($customer_login_info_rs as $row) {
		echo "    <tr>\n";
		
		$fieldndx = 0;
		foreach ($row as $data) {
			if ($fieldndx == 1) {
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