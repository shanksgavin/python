<!DOCTYPE html>
<html>
<head>
<title>OMS Pie Charting of 2010 Closed Cases</title>
<meta http-equiv="Content-Type" content="text/html;charset=UTF-8" />
<link rel="stylesheet" type="text/css" href="OMSStyleSheet.css" />
<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>
<script type="text/javascript">
$(function () {
    var colors = Highcharts.getOptions().colors,
        categories = ['Predicted Closed', 'Closed'],
        name = 'Closed Case Status',
        data = [{
            y: 4,
            color: colors[0],
            drilldown: {
                name: 'Predicted Closed - Causes',
                categories: ['No Value','Unknown 2052'],
                data: [3,1],
                color: colors[0]
                }
            }, {
            y: 101,
            color: colors[2],
            drilldown: {
                name: 'Closed - Causes',
                categories: ["Accident 2010","Kudzu/Vines 2122","Lightning 2110","No Outage  2000","Tree-On R/W 2121","Unknown  2052","WEC Equipment Failure  2045","Wildlife  2015"],
                data: [3,1,2,13,16,49,5,12],
                color: colors[2]
                }
            }];

        // Build the data arrays
        var browserData = [];
        var versionsData = [];
        for (var i = 0; i < data.length; i++) {
    
            // add browser data
            browserData.push({
                name: categories[i],
                y: data[i].y,
                color: data[i].color
            });
    
            // add version data
            for (var j = 0; j < data[i].drilldown.data.length; j++) {
                var brightness = 0.2 - (j / data[i].drilldown.data.length) / 5 ;
                versionsData.push({
                    name: data[i].drilldown.categories[j],
                    y: data[i].drilldown.data[j],
                    color: Highcharts.Color(data[i].color).brighten(brightness).get()
                });
            }
        }
    
        // Create the chart
        $('#closed_cases').highcharts({
            chart: {
                type: 'pie',
            },
            title: {
                text: 'Wiregrass 2010 Closed Case Counts by Cause'
            },
            yAxis: {
                title: {
                    text: 'Total percent of Closed Cases'
                }
            },
            plotOptions: {
                pie: {
                    startAngle: 270,
                    shadow: false,
                    center: ['54%', '50%']
                }
            },
            legend: {
                floating: true
            },
            tooltip: {
                enabled: true
            },
            series: [{
                name: 'Total ',
                data: browserData,
                size: '48%',
                tooltip: {
                    valueSuffix: ' Cases'
                },
                dataLabels: {
                    formatter: function() {
                        return this.y > 0 ? this.point.name : null;
                    },
                    color: 'white',
                    distance: -46,
                    inside: false,
                    rotation: 0
                }
            }, {
                name: 'Total Causes',
                data: versionsData,
                size: '60%',
                innerSize: '48%',
                dataLabels: {
                    formatter: function() {
                        // display only if larger than 4
                        return this.y > 0 ? '<b>'+ this.point.name +':</b> '+ this.y : null;
                    }
                }
            }]
        });
    });
</script>

</head>
<body>
<script src="../Highcharts-3.0.0/js/highcharts.js"></script>
<script src="../Highcharts-3.0.0/js/modules/exporting.js"></script>
<div id="closed_cases" style="min-width: 400px; width: 600px; min-height: 400px; height: 600px; margin: 0 auto"></div>
</body>
</html>