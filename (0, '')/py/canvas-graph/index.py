#!/usr/bin/python
import cgitb, sys, time
cgitb.enable()

#sys.path.append('/var/www/fs4/py/')
#import common_methods

#get_temp = common_methods.getsystemperature()
#print get_temp

print 'Content-type: text/html'
print

print """

<!DOCTYPE HTML>
<html>

<title>Fs4 Graphs</title>

<head>
        <script type="text/javascript">
        window.onload = function () {
		
		var cur_date = new Date();
		var get_min = cur_date.getMinutes();
		var get_sec = cur_date.getSeconds();
		var join_time  = cur_date.getMinutes()+':'+cur_date.getSeconds()


                var dps = []; // dataPoints
		//var dps = [{x: '11-20', y: 10}, {x: '11-30', y: 10}, {x: '11-40', y: 10}, {x: '11-50', y: 10}, {x: '11-60', y: 10}];   //dataPoints. 

                var chart = new CanvasJS.Chart("chartContainer",{
                        title :{
                                text: "Temperature data"
                        }, 
			axisX: {						
				title: "Time",
				valueFormatString: "hh:mm:ss"
			},           
			axisY: {
				title: "Temperature(celcius)",
			},          
                        data: [{
                                type: "line",
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
			ajax.onreadystatechange = function() {
			if (ajax.readyState == 4) {
			 //alert(ajax.responseText);
			}
			};
			ajax.open("GET", "ajax_val_temp", false);
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
        <script type="text/javascript" src="canvasjs.min.js"></script>
</head>
<body>
        <div id="chartContainer" style="height: 300px; width:100%;">
        </div>
</body>
</html>
"""

