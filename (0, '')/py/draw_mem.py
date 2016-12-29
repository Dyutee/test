#!/usr/bin/python
import cgitb, os, cgi,sys, commands, common_methods, datetime
cgitb.enable()

sys.path.append('/var/nasexe/python/')
import tools

memory_display = commands.getoutput('sudo /var/nasexe/packet_memory memory');

memory_array = [];
used_array   = [];

memory_array = memory_display.split(' ');

memory_param_array = memory_array[1].split(':');

image_icon = common_methods.getimageicon();

total_array = memory_param_array[0].split('-');
used_array  = memory_param_array[1].split('-');
free_array  = memory_param_array[2].split('-');

total = total_array[0];
used  = used_array[0];
free  = free_array[0];
print used
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
	var totalPoints = 100;
	var updateInterval = 1000;

	function drawGraph(data_set)
	{
		var now = new Date().getTime();

		function GetData()
		{
			data.shift();

			while (data.length < totalPoints)
			{
				for (var index in data_set)
				{
					id = data_set[index];

					y = id['y'];
	
					//var y = Math.random()* 100;
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
					lineWidth: 1.1,
					fill: true
				}
			},

			xaxis:
			{
				mode: "time",
				tickSize: [2, "second"],
				tickFormatter: function(v, axis)
				{
					var date = new Date(v);

					if (date.getSeconds() % 10 == 0)
					{
						var hours   = date.getHours() < 10 ? "0" + date.getHours() : date.getHours();
						var minutes = date.getMinutes() < 10 ? "0" + date.getMinutes() : date.getMinutes();
						var seconds = date.getSeconds() < 10 ? "0" + date.getSeconds() : date.getSeconds();

						return hours + ":" + minutes + ":" + seconds;
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
				min: parseFloat(0.1),
				max: parseFloat(1.5),
				tickSize:0.5,
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

				axisLabel:"Memory Used Graph",
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
					label: "Memory",
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
filetoread = 'memfile_' + currdate;

dataarray = [];

fileexists = tools.check_file_exists(filetoread);

if (fileexists == 'exists'):
        for line in open(filetoread, 'r'):
                dataarray.append(line);

if (len(dataarray) > 0):
        for entry in dataarray:
                entry = entry.strip();

                timeseries  = entry[:entry.find(':::')];
                usedmemory  = entry[entry.find(':::') + 3:];

                tempdata = {'x': timeseries, 'y': usedmemory};
                data.append(tempdata);


print """ <div style="float: none; margin-left: 21%;"><img src = '../images/red_grid.jpg'>Available:"""+total+"""</div>"""
print """ <div style="float: none; margin-left: 21%;"><img src = '../images/red_grid1.jpg'>Free:"""+free+"""</div>"""
print """<div id="flot-placeholder1" style="width:550px;height:300px;margin:0 auto"></div>"""
print """<script type="text/javascript">
	drawGraph(""" + str(data) + """);
</script>"""
