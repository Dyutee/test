#!/usr/bin/python
import cgitb, os, cgi,sys, datetime
cgitb.enable()
sys.path.append('/var/nasexe/python/');
import tools

form = cgi.FieldStorage()

if(form.getvalue("disk_name")):
	get_disk = form.getvalue("disk_name")

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

			var chart = new CanvasJS.Chart("chartContainer",{
				title :{
					text: 'Disk usage of """+get_disk+"""'
				}, 
				axisX: {                                                
					title: "Time",
					valueFormatString: "hh:mm:ss"
				},           
				axisY: {
					title: "Size(GB)",
				},          
				data: [{
					type: "line",
					showInLegend: true,
					lineThickness: 2,
					name: "used",
					markerType: "square",
					color: "#F08080",
					dataPoints: dps 
				},
				{
					type: "line",
					showInLegend: true,
					lineThickness: 2,
					name: "free",
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
				ajax.open("GET", 'canvas-graph/disk_usage_"""+get_disk+"""', false);
				ajax.send(null);

				for (var j = 0; j < count; j++) {       

					yVal = ajax.responseText;
					var res = yVal.split(":"); 
					yVal = parseFloat(res[0]);
					yVal2 = parseFloat(res[1])
		
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

			<div id="chartContainer" style="height: 300px; width:100%;"></div>

	</body>
	</html>
	"""

else:
	print """

                        <div style="text-align:center; margin:20px;"> Error! Could not display disk data.</div>



        </body>
        </html>
        """

	

