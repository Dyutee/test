#!/usr/bin/python
import cgitb, os, cgi, commands, sys, memory_information, common_methods
cgitb.enable()

memory_info = memory_information.mem_information()
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

print free
#used = memory_info["used"]
#print used


print
print"""<html>
  <head>
    <!--<script type='text/javascript' src='http://www.google.com/jsapi'></script>-->
    <script type='text/javascript' src='../js/memory.js'></script>
    <script type='text/javascript'>
      google.load('visualization', '1', {packages:['gauge']});
      google.setOnLoadCallback(drawChart);
    </script>
  </head>

  <body>
	<input type = "hidden" name = "hid" id = "hid_val" value = '"""+free+"""'>
    <div id='chart_div'></div>
    <script type="text/javascript">
  function Timer(){this.t={};this.tick=function(a,b){this.t[a]=[(new Date).getTime(),b]};this.tick("start")}var loadTimer=new Timer;window.jstiming={Timer:Timer,load:loadTimer};if(window.external&&window.external.pageT)window.jstiming.pt=window.external.pageT;if(window.jstiming)window.jstiming.report=function(g,d){var c="";if(window.jstiming.pt){c+="&srt="+window.jstiming.pt;delete window.jstiming.pt}if(window.external&&window.external.tran)c+="&tran="+window.external.tran;var a=g.t,h=a.start;delete a.start;var i=[],e=[];for(var b in a){if(b.indexOf("_")==0)continue;var f=a[b][1];if(f)a[f][0]&&e.push(b+"."+(a[b][0]-a[f][0]));else h&&i.push(b+"."+(a[b][0]-h[0]))}if(d)for(var j in d)c+="&"+j+"="+d[j];(new Image).src=["http://csi.gstatic.com/csi?v=3","&s=gviz&action=",g.name,e.length?"&it="+e.join(",")+c:c,"&rt=",i.join(",")].join("")};
</script>


<script type="text/javascript">

var csi_timer = new window.jstiming.Timer();
csi_timer.name = 'docs_gauge';

google.setOnLoadCallback(drawChart);

function drawChart() {

  csi_timer.tick('load');

   var free_mem = document.getElementById("hid_val").value
  var data = new google.visualization.DataTable();
  data.addColumn('string', 'Label');
  data.addColumn('number', 'Value');
data.addRows(3);
  data.setValue(0, 0, 'Free');
  data.setValue(0, 1, parseInt(free_mem));
  /*data.setValue(1, 0, 'CPU');
  data.setValue(1, 1, 55);
  data.setValue(2, 0, 'Network');
  data.setValue(2, 1, 68);*/

  csi_timer.tick('data');

  var chart = new google.visualization.Gauge(document.getElementById('chart_div'));

  csi_timer.tick('new');

  var options = {width:200, height: 100, redFrom: 90, redTo: 8000,
      yellowFrom:75, yellowTo: 90, minorTicks: 5};
  chart.draw(data, options);

  csi_timer.tick('draw');
  window.jstiming.report(csi_timer);  

  setInterval(function() {
    data.setValue(0, 1, 40 + Math.round(60 * Math.random()));
    chart.draw(data, options);
  });
  /*setInterval(function() {
    data.setValue(1, 1, 40 + Math.round(60 * Math.random()));
    chart.draw(data, options);
  }, 5000);
  setInterval(function() {
    data.setValue(2, 1, 60 + Math.round(20 * Math.random()));
    chart.draw(data, options);
  }, 26000);*/
}
</script>

  </body>
</html>





"""
