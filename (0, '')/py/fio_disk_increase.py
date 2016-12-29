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
				
	
	<div style="text-align:center; background-color:#D1D1D1; padding:5px; font-weight:bold; margin:50px 0 0 0; ">Update FIO Disk Size</div>
			
	<table width="70%" style="margin:10px 0 0 70px; font-size:14px;">
	<tr>
	<td>Total Available Size</td>
	<td>"""+availables_size+"""</td>
	</tr>

	
	<tr>
	<td>Previous Size</td>
	<td>"""+disk_size_info+"""</td>
	</tr>

	<tr>
        <td>Volume</td>
        <td>"""+volume_update+"""</td>
        </tr>

        <tr>
        <td>Disk</td>
        <td>"""+disk_info+"""</td>

        <tr>
        <td>Increase size (GB)</td>
        <td><input type="text" class="textbox" name="update_size" onkeypress="return isNumberKey(event)" value=""></td>
        </tr>

	</table>


	<table width="100%">
	<tr>
	<td align="right">
	<button class="button_example" style="float:right; margin:10px 100px 0 0;" type="submit" name = 'submit'  id = 'submit' value = 'submit'  onclick ="return validate_increase_size();">Update</button>
	</td>
	</tr>
	</table>

	</form>
	"""

except Exception as e:
	disp_except.display_exception(e);
        #fh = open('/var/www/fs2/py/temp', 'w');
        #traceback.print_exc(file = fh);
        #fh.write("<BR>");
        #fh.write('<BR><input type = "button" value = "Back" onclick = "location.href = \'/fs2/py/setup_diskmgr_add_disk.py\'">');
        #print "<script>location.href = './error.py';</script>";

