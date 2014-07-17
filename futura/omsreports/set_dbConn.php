<?php
//Constants
$_host = 'localhost';
$_port = '5432';
$_dbnm = 'coweta-fayette';
$_user = 'postgres';
$_pswd = 'usouth';
$_conn = '';
?>
<!DOCTYPE html>
<html>
<head>
<title>Dynamic Database Connection Setting</title>
</head>
<body>
<h1>Dynamic Database Connection Setting</h1>
<form>
<table>
<tr><td>Host:</td><td><input type="text" name="_host" value="<?php echo $_host;?>"></td></tr>
<tr><td>Port:</td><td><input type="text" name="_port" value="<?php echo $_port;?>"></td></tr>
<tr><td>Database:</td><td><input type="text" name="_dbnm" value="<?php echo $_dbnm;?>"></td></tr>
<tr><td>User:</td><td><input type="text" name="_user" value="<?php echo $_user;?>"></td></tr>
<tr><td>Password:</td><td><input type="text" name="_pswd" value="<?php echo $_pswd;?>"></td></tr>
<tr><td>&nbsp;</td><td><input type="button" name="Update" value="update"></td></tr>
</table>
</form>
<br>
<?php 
//Default Connection
$_conn .= '<?php';
$format = '$dbconn = pg_connect("host=\'%s\' port=\'%s\' dbname=\'%s\' user=\'%s\' password=\'%s\'")';
$_conn .= sprintf($format,$_host,$_port,$_dbnm,$_user,$_pswd);
$_conn .= 'if (!$dbconn) {';
$_conn .= ' 	echo "A db connection error occurred!<br>\n";';
$_conn .= ' 	echo "Suggestion: Make sure PostgreSQL is running.<br>\n";';
$_conn .= ' 	echo "<a href="http://modelserver/omsreports">Click to go back to Modelserver</a>";';
$_conn .= ' 	exit;';
$_conn .= '};';
$_conn .= '?>';

//$fo = file
//highlight_string($_conn);
?>
</body>
</html>