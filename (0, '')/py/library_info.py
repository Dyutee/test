#!/usr/bin/python
#_*_ coding: UTF-8 _*_
#enable debugging

import cgitb, os, sys, commands, common_methods, cgi, traceback, string
cgitb.enable()

sys.path.append('/var/nasexe/python/')
import mhvtl

#print 'Content-type: text/html'
form = cgi.FieldStorage()

get_id = form.getvalue("lib_id")
get_st = form.getvalue("st")
get_lib_sg_dev = form.getvalue("lib_sg_dev")

#print get_id
#print "<br/>"
#print get_st
#print "<br/>"
#print get_lib_sg_dev

if(get_st == 'online'):
	status = mhvtl.get_vtl_lib_status_os(get_id,get_lib_sg_dev)
elif(get_st == 'offline'):
	status = mhvtl.get_vtl_lib_status_conf(get_id)


print
               
print """ <html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>..::Tyrone Opslag FS2::..</title>
<script language = 'javascript' src = '../js/commons.js'></script>
<script type="text/javascript" src="../js/jquery.min(1).js"></script>

<link href = "../css/style.css" rel = "stylesheet" type = "text/css" />
<link href = "../css/jquery.alerts.css" rel = "stylesheet" type = "text/css" />
<link rel = 'important.gif' href = '../images/important.gif  ' />


<script type="text/javascript" src="../js/jquery.alerts.js"></script>


<script type="text/javascript">
var helperPopup = new Popup('helper'); // Pass an ID to link with an existing DIV in page
helperPopup.autoHide = false;
helperPopup.position = "below right";
helperPopup.constrainToScreen = false;
</script>




<script language = 'javascript' src = '../js/jquery-latest-fade.js'></script>



</head>
<body >"""
if(get_st == 'offline'):
	print """<table>
	<tr>
	<th class="border" align='center' style='background-color:#585858; color:#FFF;'>
	<table>

	<tr>
	<th class="border" align='center' style='background-color:#585858; color:#FFF;'>
	<tr>
	<th align='center' style='background-color:#585858; color:#FFF;'>Slots Status</th>
	</tr>
	</th>
	</tr>
	</table>
	
	<table>
	<tr>
	<th class="border" align='center' style='background-color:#585858; color:#FFF; width:20%;'>Status</th>
	<th class="border" align='center' style='background-color:#585858; color:#FFF; width:20%;'>Tape Name</th>
	<th class="border" align='center' style='background-color:#585858; color:#FFF; width:20%;'>Density</th>
	<th class="border" align='center' style='background-color:#585858; color:#FFF; width:20%;'>Total Size (MB)</th>
	<th class="border" align='center' style='background-color:#585858; color:#FFF; width:20%;'>Free Size (MB)</th>
	</tr>

	</table>
	</th>

	<th class="border" align='center' style='background-color:#585858; color:#FFF;'>Drives</th>
	<th class="border" align='center' style='background-color:#585858; color:#FFF;'>Maps</th>
	<th class="border" align='center' style='background-color:#585858; color:#FFF;'>Free Slots</th>
	<th class="border" align='center' style='background-color:#585858; color:#FFF;'>Total Slots</th>
        </tr>


	<tr>
	<td class="border" align='left'>"""
	for x in status['slots_status']:
		print """
		<table>
		<tr>"""
		#if(len(x) > 1):
		for y in x:
			print """<td align="left" style="width:20%;" >"""+str(y)+"""</td>"""

		print """</tr>
		</table>"""

	print """</td>
	<td class="border" align='center' valign='top'>"""+str(status['drives'])+"""</td>
	<td class="border" align='center' valign='top'>"""+str(status['maps'])+"""</td>
	<td class="border" align='center' valign='top'>"""+str(status['free_slots'])+"""</td>
	<td class="border" align='center' valign='top'>"""+str(status['total_slots'])+"""</td>
	</tr>
		"""

	print """</table>"""
else:
	vtl_status = status['vtl_status']
	print """<table>
	<tr>
	<th class="border" align='center' style='background-color:#585858; color:#FFF;'>
	<table>

	<tr>
	<th class="border" align='center' style='background-color:#585858; color:#FFF;'>
	<tr>
	<th align='center' style='background-color:#585858; color:#FFF;'>Slots Status</th>
	</tr>
	</th>
	</tr>
	</table>
	
	<table>
	<tr>
	<th class="border" align='center' style='background-color:#585858; color:#FFF; width:20%;'>Status</th>
	<th class="border" align='center' style='background-color:#585858; color:#FFF; width:20%;'>Tape Name</th>
	<th class="border" align='center' style='background-color:#585858; color:#FFF; width:20%;'>Density</th>
	<th class="border" align='center' style='background-color:#585858; color:#FFF; width:20%;'>Total Size (MB)</th>
	<th class="border" align='center' style='background-color:#585858; color:#FFF; width:20%;'>Free Size (MB)</th>
	</tr>

	</table>
	</th>

	<th class="border" align='center' style='background-color:#585858; color:#FFF;'>Drives</th>
	<th class="border" align='center' style='background-color:#585858; color:#FFF;'>Maps</th>
	<th class="border" align='center' style='background-color:#585858; color:#FFF;'>Free Slots</th>
	<th class="border" align='center' style='background-color:#585858; color:#FFF;'>Total Slots</th>
        </tr>


	<tr>
	<td class="border" align='left'>"""
	for x in vtl_status['slots_status']:
		print """
		<table>
		<tr>"""
		for y in x:
			print """<td align="left" style="width:20%;" >"""
			if(str(y).find('=') != -1):
				split_y = string.split(y,'=')
				print split_y[1]
			else:
				print str(y)
			"""</td>"""

		print """</tr>
		</table>"""

	print """</td>
	<td class="border" align='center' valign='top'>"""+str(vtl_status['drives'])+"""</td>
	<td class="border" align='center' valign='top'>"""+str(vtl_status['maps'])+"""</td>
	<td class="border" align='center' valign='top'>"""+str(vtl_status['free_slots'])+"""</td>
	<td class="border" align='center' valign='top'>"""+str(vtl_status['slots'])+"""</td>
	</tr>
		"""

	print """</table>"""

print """</body>
</html>

"""


