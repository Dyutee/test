#!/usr/bin/python
import cgitb, os, cgi,sys, datetime, header
cgitb.enable()
sys.path.append('/var/nasexe/python/');
import tools

if(header.form.getvalue("ethernet")):
	get_ethernet = header.form.getvalue("ethernet")

	#print 'Content-type: text/html'
	#print
	import left_nav

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
					text: '"""+get_ethernet+""" Traffic data'
				}, 
				axisX: {                                                
					title: "Time",
					valueFormatString: "hh:mm:ss"
				},           
				axisY: {
					title: "traffic(bytes)",
				},          
				data: [{
					type: "line",
					showInLegend: true,
					lineThickness: 2,
					name: "incoming",
					markerType: "square",
					color: "#F08080",
					dataPoints: dps 
				},
				{
					type: "line",
					showInLegend: true,
					lineThickness: 2,
					name: "outgoing",
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
				ajax.open("GET", 'canvas-graph/traffic_"""+get_ethernet+"""', false);
				ajax.send(null);

				for (var j = 0; j < count; j++) {       

					yVal = ajax.responseText;
					var res = yVal.split(":"); 
					yVal = parseInt(res[0]);
					yVal2 = parseInt(res[1])
		
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
	<!--Right side body content starts from here-->
		      <div class="rightsidecontainer">
			<div class="insidepage-heading"> RESOURCES >> <span class="content">Date/Time Settings</span></div>
			<!--tab srt-->
			<div class="searchresult-container">
			  <div class="infoheader">
			    <div id="tabs">
			      <ul>
				<li><a href="#tabs-1">"""+get_ethernet+""" Traffic Data</a></li>
			      </ul>
				
				<div id="tabs-1">

				<div class="form-container">
				<div class="topinputwrap">

			<div id="chartContainer" style="height: 300px; width:100%;"></div>

			</div>
			</div>
			<p>&nbsp;</p>
			</div>
			</div>
			</div>
			</div>
			</div>
			</div>


	<!--Footer starts from here-->
	    <div class="insidefooter footer_content">&copy; 2013 Opslag FS2</div>
	    <!-- Footer ends here-->
	  </div>
	  <!--inside body wrapper end-->
	</div>
	<!--body wrapper end-->



	</body>
	</html>
	"""

else:
	import left_nav
	print """
	<!--Right side body content starts from here-->
                      <div class="rightsidecontainer">
                        <div class="insidepage-heading"> RESOURCES >> <span class="content">Date/Time Settings</span></div>
                        <!--tab srt-->
                        <div class="searchresult-container">
                          <div class="infoheader">
                            <div id="tabs">
                              <ul>
                                <li><a href="#tabs-1">Traffic Data</a></li>
                              </ul>
                                
                                <div id="tabs-1">

                                <div class="form-container">
                                <div class="topinputwrap">

                        <div style="text-align:center; margin:20px;"> Error! Could not display ethernet data.</div>

                        </div>
                        </div>
                        <p>&nbsp;</p>
                        </div>
                        </div>
                        </div>
                        </div>
                        </div>
                        </div>


        <!--Footer starts from here-->
            <div class="insidefooter footer_content">&copy; 2013 Opslag FS2</div>
            <!-- Footer ends here-->
          </div>
          <!--inside body wrapper end-->
        </div>
	        <!--body wrapper end-->



        </body>
        </html>
        """

	

