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
	import san_disk_funs
	san_list = san_disk_funs.list_all_disk_att()
	#print san_list
	sys.path.append('/var/nasexe/')
	import storage
	
	form = cgi.FieldStorage()
	querystring = os.environ['QUERY_STRING'];
	#print querystring
	thread=form.getvalue('thread');
	device_id = form.getvalue('dev_id')
	san_type = form.getvalue('type')
	threads = form.getvalue('threads')
	usn = form.getvalue('usn')
	thin = form.getvalue('thin')
	cache = form.getvalue('cache')

	'''
		#print """<script>javascript:parent.jQuery.fancybox.close();</script>""";

	
'''
	print """
	<head>
	<link href = "../css/style.css" rel = "stylesheet" type = "text/css" />
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<title>..::Tyrone Opslag FS2::..</title>
	<script language = 'javascript' src = '../js/commons.js'></script>
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

	<div style="text-align:center; background-color:#D1D1D1; padding:5px; font-weight:bold; margin:30px 0 0 0; ">SAN Disk Properties</div>
                        
        <table width="70%" style="margin:10px 0 0 100px; font-size:14px;">
        <tr>
        <td>Device Id</td>
        <td>"""+device_id+"""</td>
        </tr>

        <tr>
        <td>Threads Pool</td>
        <td>"""+thread+"""</td>
        </tr>

        <tr>
        <td>Type</td>
        <td>"""+san_type+"""</td>
        </tr>

        <tr>
        <td>USN Number</td>
        <td>"""+usn+"""</td>
        </tr>

        <tr>
        <td>Cache</td>
        <td>"""+cache+"""</td>
        </tr>

        <tr>
        <td>Thin</td>
        <td>"""+thin+"""</td>
        </tr>

        <tr>
        <td>Threads Num</td>
        <td>"""+threads+"""</td>
        </tr>

	</table>
	"""

except Exception as e:
	disp_except.display_exception(e);

