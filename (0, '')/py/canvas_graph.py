#!/usr/bin/python
import cgitb, os, cgi,sys, datetime
cgitb.enable()
sys.path.append('/var/nasexe/python/');
import tools

print 'Content-type: text/html'
print

print"""
<script type="text/javascript">
        window.onload = function () {
                
                var cur_date = new Date();
                var get_min = cur_date.getMinutes();
                var get_sec = cur_date.getSeconds();
                var join_time  = cur_date.getMinutes()+':'+cur_date.getSeconds()


                var dps = []; // dataPoints

                var chart = new CanvasJS.Chart("chartContainer",{
                        title :{
                                text: "Temperature data"
                        }, 
                        axisX: {                                                
                                title: "Time",
                                valueFormatString: "hh:mm:ss"
                        },           
                        axisY: {
                                title: "Temp(celcius)",
                        },          
                        data: [{
                                type: "line",
				showInLegend: true,
                                lineThickness: 2,
                                name: "temperature",
                                markerType: "square",
                                color: "#20B2AA",
                                dataPoints: dps 
                        }]
                });

                var xVal = new Date();
                var yVal = 100; 
                var updateInterval = 2000;
                var dataLength = 100000; // number of dataPoints visible at any point
                var updateChart = function (count) {
                        count = count || 1;
                        // count is number of times loop runs to generate random dataPoints.
                        

                        var ajax = new XMLHttpRequest();
                        ajax.open("GET", "canvas-graph/ajax_val_temperature", false);
                        ajax.send(null);

                        for (var j = 0; j < count; j++) {       

                                yVal = parseInt(ajax.responseText);
                                dps.push({
                                        x: xVal,
                                        y: yVal
                                });
                                
                                xVal = new Date();
                                
                        };

                        if (dps.length > dataLength)
                        {
                                dps.shift();                            
                        }
                        
                        chart.render();         

                };
                // generates first set of dataPoints
                updateChart(dataLength); 

                // update chart after specified time. 
                setInterval(function(){updateChart()}, updateInterval); 

        }
        </script>
        <script type="text/javascript" src="canvas-graph/canvasjs.min.js"></script>
</head>
<body>

        	<div id="chartContainer" style="height: 300px; width:100%;"></div>


</body>
</html>
"""

