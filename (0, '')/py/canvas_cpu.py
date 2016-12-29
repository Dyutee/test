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
                var dpx = []; // dataPoints
                //var dps = [{x: '11-20', y: 10}, {x: '11-30', y: 10}, {x: '11-40', y: 10}, {x: '11-50', y: 10}, {x: '11-60', y: 10}];   //dataPoints. 

                var chart = new CanvasJS.Chart("chartContainer",{
                        title :{
                                text: "CPU Temperature data"
                        }, 
                        axisX: {                                                
                                title: "Time",
                                valueFormatString:" "
                        },           
                        axisY: {
                                title: "Temp (celsius)",
                                valueFormatString:" "
                        },          
                        data: [{
                                type: "line",
				showInLegend: true,
				lineThickness: 2,
				name: "CPU 1",
				markerType: "square",
				color: "#F08080",
                                dataPoints: dps 
                        },
			{
                                type: "line",
				showInLegend: true,
				lineThickness: 2,
				name: "CPU 2",
				markerType: "square",
				color: "#20B2AA",
                                dataPoints: dpx 

				
			}]
                });

                var xVal = new Date();
                var yVal = 100;
                var yVal2 = 100;

 
                var updateInterval = 2000;
                var dataLength = 100000; // number of dataPoints visible at any point
                var updateChart = function (count) {
                        count = count || 1;
                        // count is number of times loop runs to generate random dataPoints.
                        

                        var ajax = new XMLHttpRequest();
                        ajax.open("POST", "canvas-graph/cpu1", false);
                        ajax.send(null);

                        var ajax2 = new XMLHttpRequest();
                        ajax2.open("POST", "canvas-graph/cpu2", false);
                        ajax2.send(null);

                        for (var j = 0; j < count; j++) {       

                                yVal = parseInt(ajax.responseText);
                                yVal2 = parseInt(ajax2.responseText);
                                dps.push({
                                        x: xVal,
                                        y: yVal
                                });
                                
                                dpx.push({
                                        x: xVal,
                                        y: yVal2
                                });
                                
                                xVal = new Date();
                                
                        };

                        if (dps.length > dataLength)
                        {
                                dps.shift();                            
                        }
                        
                        if (dpx.length > dataLength)
                        {
                                dpx.shift();                            
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

        	<div id="chartContainer" style="height: 300px; "></div>


</body>
</html>
"""

