<!DOCTYPE html>
<html>
<head>
<title>OMS Pie Charting of 2011 Closed Cases</title>
<meta http-equiv="Content-Type" content="text/html;charset=UTF-8" />
<link rel="stylesheet" type="text/css" href="OMSStyleSheet.css" />
<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>
<script type="text/javascript">
    $(function () {
        $('#closed_cases').highcharts({
            chart: {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false
            },
            title: {
                text: 'Closed Case Causes, 2011'
            },
            tooltip: {
                valueDecimals: 1,
                valueSuffix: '%',
                pointFormat: '{series.name}: <b>{point.percentage}</b>'
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: true,
                        color: '#000000',
                        connectorColor: '#000000',
                        formatter: function () {
                            return '<b>' + this.point.name + '</b>: ' + this.y;
                        }
                    }
                }
            },
            series: [{
                type: 'pie',
                name: 'Cause',
                size: '60%',
                data: [
                    ['BLANK', 98],
                    ['Accident 2010', 21],
                    ['Check Voltage  2800', 1],
                    ['Customers Equipment  2046', 26],
                    ['House Fire  2050', 6],
                    ['Kudzu/Vines 2122', 5],
                    ['Lightning 2110', 217],
                    ['No Outage  2000', 71],
                    ['none provided!', 30],
                    ['Powersouth 2115', 12],
                    ['Reconnect Meter  2150', 3],
                    ['Requested by Crew  2070', 25],
                    ['Storm  2100', 23],
                    ['Tree-Off R/W  2120', 118],
                    ['Tree-On R/W 2121', 186],
                    ['Unknown  2052', 331],
                    ['Vandalism/Stolen  2051', 2],
                    ['WEC Equipment Failure  2045', 59],
                    ['Wildlife  2015', 165]
                ]
            }]
        });
    });
</script>

</head>
<body>
<script src="../Highcharts-3.0.0/js/highcharts.js"></script>
<script src="../Highcharts-3.0.0/js/modules/exporting.js"></script>
<div id="closed_cases" style="min-width: 400px; width: 800px; min-height: 400px; height: 600px; margin: 0 auto"></div>
</body>
</html>