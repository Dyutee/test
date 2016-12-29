#!/usr/bin/python
#_*_ coding: UTF-8 _*_

#enable debugging
import traceback, sys
sys.path.append('/var/www/fs2/modules')
import disp_except;
try:
	import cgitb, os, sys, commands, common_methods, cgi, array, traceback
	cgitb.enable()
	sys.path.append('/var/nasexe/storage')
	import storage_op
	from lvm_infos import *
	from functions import *
	
	sys.path.append('/var/nasexe/')
	import storage

	log_array = [];
        log_file = common_methods.log_file;

	form = cgi.FieldStorage()
	nas_info = storage.get_lvs()
	
	querystring = os.environ['QUERY_STRING'];
	disk_size_info = form.getvalue('size_name')
	disk_size_info = disk_size_info.replace("g", "GB")
	volume_update= form.getvalue("volume")
	disk_info= form.getvalue('disk_name')
	size_info= form.getvalue('size_name')
	#print 'prev:'+str(size_info)
	size_info = size_info.replace('g' , '')
	#print '<br/>'
	#print 'previous:'+str(size_info)
	#print '<br/>'
	vg_info = storage.get_vgs()
	dictionary = vg_info["vgs"]
	for t in dictionary:
		if(t["vg_name"]==volume_update):
			availables_size = t["free_size"]
			availables_size =availables_size.replace("g", "GB")

	if(form.getvalue("submit")):
		update_volume = form.getvalue("update_volume")
		update_disk = form.getvalue("update_disk")
		#print update_disk
		update_size = form.getvalue("update_size")
		#print update_size		
		#print '<br/>'
		#exit();
		update_size = update_size.replace('g', '')
		
		#print 'current:'+str(update_size)
		#print '<br/>'
		
		increase_size = float(size_info)+float(update_size)
		#print 'ADD:'+str(increase_size)
		#exit();
		increase_size = str(increase_size)+"GB"
		
		#print 'increase:'+str(increase_size);
		update_lv = storage_op.lv_increase(update_disk,increase_size, type1='FIO')
		#print update_lv;
		#exit();

		log_string = str(common_methods.now) + '<<>>From: ' + common_methods.remote_ip + '<<>>' + 'AUTHENTICATION: ' + str(update_lv);

		log_array.append(log_string)
		common_methods.append_file(log_file, log_array);
		if(update_lv == True):
			print""" <div id = 'id_trace' >"""
			print "you Increase <font color = 'darkred'><b>"+str(update_size)+'GB'+" </b></font> of Size! Your Size <font color = 'darkred'><b>"+str(size_info)+'GB'+"</b></font> is successfully Updated to <font color = 'darkred'><b>"+increase_size+"</b></font>!"
			print "</div>"
		else:
			print""" <div id = 'id_trace_err' >"""
			print "You Can't decrease the Size!"
			print "</div>"
		#print """<script>javascript:parent.jQuery.fancybox.close();</script>""";

	

	print """
	<head>
	<link href = "../css/style.css" rel = "stylesheet" type = "text/css" />
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

	 <SCRIPT language=Javascript>
      
      function isNumberKey(evt)
      {
         var charCode = (evt.which) ? evt.which : event.keyCode
         if (charCode > 31 && (charCode < 46 || charCode > 57 || charCode == 190))
            return false;

            return true;

      }
     
        </SCRIPT>
 
	<script type = "text/javascript">
	function hideMessage() {
	$(document).ready(
	function(){
	          $("#id_trace_err").fadeOut(2000);
		  $("#id_trace").fadeOut(2000);
		  }
		  );
		 }
	var tim = window.setTimeout("hideMessage()", 10000);  // 10000 milliseconds = 10 seconds
	</script>	
	
	</head>
	<form method="POST" action="" name="add_disk" >
				
				

<td width = "172" class = "table_heading" height = "35px" valign = "middle">
                        <b><i><font color ="darkred" style="font-size:18px;" >Update FIO Disk Size</font></i></td><td><b><i><font color ="#7F0101" style= "margin-left:29%;">Available Size:</font></i></b>&nbsp&nbsp<b><font color ="green" style= "text-decoration:blink;">"""+availables_size+"""</font></b> <br/><br/> </td>
</tr> </table><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
	<br/>
	<br/>
	<br>



	
	<br/>
	<br/>				
	<br/>
	<body>
	<div style="margin-top:-33%;margin-left:19%;" >
	<table>

	<tr>
	<td valign="top" align="left" colspan="3">
	<table width="400" align="center" cellspacing="0" cellpadding="0" border="0" class="uter_border">
	<tbody>

	<tr>
	<td valign="middle" height="35px" class="table_heading" style = 'font: 13px Arial; color: #000000; font-weight: bold;'>
	Previous Size:<font color='darkred'><b style="margin-left: 13%;">"""+disk_size_info+"""</b></font>
	</td>
	</tr>
	
	<tr>
	<td valign="middle" height="35px" class="table_heading" style = 'font: 13px Arial; color: #000000; font-weight: bold;'>
	Volume:
	</td>
	<td> <input type="text" readonly style="text-align:center;" name="update_volume" size="5" value="""+volume_update+""" > </td>
	</tr>

	<tr>
	<td valign="middle" height="35px" class="table_heading" style = 'font: 13px Arial; color: #000000; font-weight: bold;'>
	Disk:
	</td>
	<td><input type="text" readonly style = "text-align:center;"name="update_disk" size="5" value="""+disk_info+"""> </td>

	<tr>
	<td valign="middle" height="35px" class="table_heading" style = 'font: 13px Arial; color: #000000; font-weight: bold;'>
	Increase size:
	</td>
	<td><input type="text" style = "text-align:center;" name="update_size" onkeypress="return isNumberKey(event)" size="5" value=""> </td>
	<td><input type = "text" name="gb"  style = "text-align:center;"size = "1" readonly value= "GB"></td> 
	</tr>

	<tr>
	<td valign="middle" align="right" height="35px" class="table_heading" colspan="4">
<br/><br/><br/>
	<div style="margin-left: 64%;" ><span id="button-one"><button type = 'submit' name="submit" id="id_create_but" value = "Update" onclick ="return validate_increase_size();" style = 'width:65px; background-color:#E8E8E8; border:none; float: left;font-size: 86%; ' title="Update"><a style="font-size:85%;">Update</a></button></span></div>


	<script>opener.location.href = 'nas_disks_list.py'</script>
	</td>
	</tr>
	</tbody></table>
				
			

	</td></tr></tbody></table></div></form>

	"""

except Exception as e:
	disp_except.display_exception(e);
        #fh = open('/var/www/fs2/py/temp', 'w');
        #traceback.print_exc(file = fh);
        #fh.write("<BR>");
        #fh.write('<BR><input type = "button" value = "Back" onclick = "location.href = \'/fs2/py/setup_diskmgr_add_disk.py\'">');
        #print "<script>location.href = './error.py';</script>";

