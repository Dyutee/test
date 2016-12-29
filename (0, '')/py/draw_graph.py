#!/usr/bin/python
import cgitb, os, cgi,sys, datetime
cgitb.enable()
sys.path.append('/var/nasexe/python/');
import tools

print 'Content-type: text/html'
print
print"""
<script src="../js/jquery1.7.js"></script>
<script type="text/javascript" src="../js/jquery.flot.min.js"></script>
<script type="text/javascript" src="../js/jquery.flot.time.js"></script>
<script type="text/javascript" src="../js/jshashtable-2.1.js"></script>
<script type="text/javascript" src="../js/jquery.numberformatter-1.2.3.min.js"></script>
<script type="text/javascript" src="../js/jquery.flot.symbol.js"></script>
<script type="text/javascript" src="../js/jquery.flot.axislabels.js"></script>


<script>
	var data = [];
	var updateInterval = 1000;
	timeseriesarray = new Array();

	function drawGraph(data_set)
	{
		var totalPoints = data_set.length;
		var now = new Date().getTime();

		function GetData()
		{
			data.shift();

			while (data.length < totalPoints)
			{
				for (var index in data_set)
				{
					id = data_set[index];

					x = id['x'];
					y = id['y'];
	
					timeseriesarray.push(x);
					var temp = [now += updateInterval, y];
					data.push(temp);
				}
			}
		}

		var options =
		{
			series:
			{
				lines:
				{
					show: true,
					lineWidth: 1.5,
					fill: true
				}
			},

			xaxis:
			{
				mode: "time",
				tickSize: [5, "second"],
				tickFormatter: function(v, axis)
				{
					var date = new Date(v);

					if (date.getSeconds() % 10 == 0)
					{
						var hours   = date.getHours() < 10 ? "0" + date.getHours() : date.getHours();
						var minutes = date.getMinutes() < 10 ? "0" + date.getMinutes() : date.getMinutes();
						var seconds = date.getSeconds() < 10 ? "0" + date.getSeconds() : date.getSeconds();

						//return hours + ":" + minutes + ":" + seconds;
						return hours + ":" + minutes;
					}

					else
					{
						return "";
					}
				},

				axisLabel: "Time",
				axisLabelUseCanvas: true,
				axisLabelFontSizePixels: 12,
				axisLabelFontFamily: 'Verdana, Arial',
				axisLabelPadding: 10
			},

			yaxis:
			{
				min: 40,
				max: 100,
				tickSize: 5,
				tickFormatter: function(v, axis)
				{
					if (v % 10 == 0)
					{
						return v;
					}

					else
					{
						return "";
					}
				},

				axisLabel: "CPU Temperature",
				axisLabelUseCanvas: true,
				axisLabelFontSizePixels: 12,
				axisLabelFontFamily: 'Verdana, Arial',
				axisLabelPadding: 6
			},

			legend:
			{
				labelBoxBorderColor: "#fff"
			},

			grid:
			{
				backgroundColor: "#000000",
				tickColor: "#008040"
			}
		};

		$(document).ready(function()
		{
			GetData();

			dataset = 
			[
				{
					label: "CPU",
					data: data,
					color: "#00FF00"
				}
			];

			$.plot($("#flot-placeholder1"), dataset, options);

			function update()
			{
				GetData();

				$.plot($("#flot-placeholder1"), dataset, options)
				setTimeout(update, updateInterval);
			}

			update();
		});
	}
</script>
<!-- HTML -->"""
currdatetime = datetime.datetime.now();
currdatetime = currdatetime.strftime("%Y-%m-%d %H:%M:%S");
currdate = currdatetime[:currdatetime.find(' ')];
currdate = str(currdate).strip();

data = [];
filetoread = 'tempfile_' + currdate;

dataarray = [];

fileexists = tools.check_file_exists(filetoread);

if (fileexists == 'exists'):
	for line in open(filetoread, 'r'):
		dataarray.append(line);

if (len(dataarray) > 0):
	for entry in dataarray:
		entry = entry.strip();

		timeseries  = entry[:entry.find(':::')];
		temperature = entry[entry.find(':::') + 3:];
	
		tempdata = {'x': timeseries, 'y': temperature};
		data.append(tempdata);

print """<div id="flot-placeholder1" style="width:550px;height:300px;margin:0 auto"></div>"""
print """<script type="text/javascript">
	drawGraph(""" + str(data) + """);
</script>"""
