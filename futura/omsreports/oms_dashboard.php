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
?>
<html>
<head>
<link rel="stylesheet" type="text/css" href="OMSStyleSheet.css" />
<title>OMS Dashboard using <?php echo pg_dbname($dbconn);?></title>
<script>
// Get Active Calls
window.setInterval(function()
{
if (window.XMLHttpRequest)
  {// code for IE7+, Firefox, Chrome, Opera, Safari
  xmlhttpCalls=new XMLHttpRequest();
  xmlhttpCases=new XMLHttpRequest();
  }
else
  {// code for IE6, IE5
  xmlhttpCalls=new ActiveXObject("Microsoft.XMLHTTP");
  xmlhttpCases=new ActiveXObject("Microsoft.XMLHTTP");
  }

// Get Active Calls onReadyStateChange
xmlhttpCalls.onreadystatechange=function()
  {
  if (xmlhttpCalls.readyState==4 && xmlhttpCalls.status==200)
    {
    document.getElementById("activeCalls").innerHTML=xmlhttpCalls.responseText;
    }
  };

// Get Active Cases onReadyStateChange
xmlhttpCases.onreadystatechange=function()
  {
  if (xmlhttpCases.readyState==4 && xmlhttpCases.status==200)
    {
    document.getElementById("activeCases").innerHTML=xmlhttpCases.responseText;
    }
  };
  
xmlhttpCalls.open("GET","getActiveCalls.php",true);
xmlhttpCalls.send();
xmlhttpCases.open("GET","getActiveCases.php",true);
xmlhttpCases.send();

var d=new Date();
var t=d.toLocaleTimeString();
document.getElementById("pulse").innerHTML=t;

},1000);

</script>
</head>
<body>
<div id="header" class="header"><p class="header">Futura Systems OMS Dashboard<img class="header" alt="Futura Systems Logo" src="./images/logo.gif"></p><div id="pulse" class="pulse"></div></p></div>
<div id="activeInfo" class="activeInfo">
	<div id="activeCalls" class="activeCalls"><b>Active Calls will be listed here.</b></div>
	<div id="activeCases" class="activeCases"><b>Active Cases will be listed here.</b></div>
</div>
</body>
</html> 