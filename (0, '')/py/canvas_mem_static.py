#!/usr/bin/python
import cgitb, os, cgi,sys, datetime
cgitb.enable()
form = cgi.FieldStorage()
sys.path.append('/var/nasexe/python/');
import tools
from tools import db

print 'Content-type: text/html'
print

s_from = form.getvalue("from")
s_to = form.getvalue("to")

#print s_from
#print s_to

query = 'select * from memory_data where timestamp between '+s_from+' and '+s_to+';'
execute=db.sql_execute(query,data=1)
#print execute

#print "<br/>"
#print "<br/>"
data_val = ''
data_val2 = ''
data_val3 = ''
i=1
for x in execute["output"]:
        date_str = ''
        date_str += str(x["timestamp"][6])+str(x["timestamp"][7])+"-"+str(x["timestamp"][4])+str(x["timestamp"][5])+"-"+str(x["timestamp"][:+4])+" "+str(x["timestamp"][8])+str(x["timestamp"][9])+":"+str(x["timestamp"][10])+str(x["timestamp"][11])+":"+str(x["timestamp"][-2:])
        #data_val += '{x:'+str(x["timestamp"])+', y:'+x["temp"]+'},'
        data_val2 += '{x:'+str(i)+', y:'+x["used"]+', label:'+'"'+str(date_str)+'"'+'},'
        data_val3 += '{x:'+str(i)+', y:'+x["free"]+', label:'+'"'+str(date_str)+'"'+'},'
	i += 1
#print data_val2[:-1]



print"""
<!DOCTYPE HTML>
<html>
<head>  
  <script type="text/javascript">
  window.onload = function () {
    var chart = new CanvasJS.Chart("chartContainer",
    {

	                axisX: {                                                
                                title: "Time",
                                labelAngle: -70
                        },
	                axisY: {                                                
                                title: "Memory (MB)"
                        },

      title:{
        text: "Memory Usage Data"
      },
      data: [
      {            
        type: "line",        
	showInLegend: true,
	markerType: "square",
	name: "used memory(MB)",
	dataPoints: ["""+data_val2[:-1]+"""]
      },
      {            
        type: "line",
	showInLegend: true,
	markerType: "square",
	name: "free memory(MB)",        
        dataPoints: ["""+data_val3[:-1]+"""]
      },
        
      ]
    });

    chart.render();
  }
  </script>
  <script type="text/javascript" src="canvas-graph/canvasjs.min.js"></script>
</head>
<body>
<div id="chartContainer" style="height: 350px; width: 99%; border:#585858 1px solid; -webkit-box-shadow: 7px 10px 5px 0px rgba(0,0,0,0.75);
-moz-box-shadow: 7px 10px 5px 0px rgba(0,0,0,0.75); box-shadow: 7px 10px 5px 0px rgba(0,0,0,0.75);"></div>

</body>
</html>
"""

