#!/usr/bin/python
#_*_ coding: UTF-8 _*_
#enable debugging

import cgitb, os, sys, commands, common_methods, cgi, traceback
cgitb.enable()

#print 'Content-type: text/html'
print

sys.path.append('../modules/')
import disp_except
import os

try:
	querystring = os.environ['QUERY_STRING'];
	sys.path.append('/var/nasexe/storage')
	import storage_op
	from lvm_infos import *
	from functions import *

	sys.path.append('/var/nasexe/')
	import storage

	log_array = [];
	log_file = common_methods.log_file;
	logstring = '';

	vgs_info = storage.get_vgs()
	vtl_info = storage.get_lvs(type1='BIO')
	form = cgi.FieldStorage()
	volume_info= form.getvalue("volume")

	if (querystring.find('&free_size=') > 0):
		free_size = querystring[querystring.find('&free_size=') + len('&free_size='):];
		free_sizes= str(free_size)

	if(form.getvalue("submit")):
        	getdisk = form.getvalue("disk")
        	getsize = form.getvalue("size")
		getsize_value = form.getvalue("gb_mb")
		getfull_size = getsize+getsize_value
		getformat = form.getvalue("adv1")
		getmount= form.getvalue("adv2")

		create_bio = storage_op.lvcreate(volume_info,getdisk,getfull_size,type1='BIO')	
		
		
		if(create_bio == True):
        		print""" <div id = 'id_trace_small' >"""
                	print " BIO Disk " + getdisk +"  Successfully created!"
			print "</div><br/>"
			logstatus = common_methods.sendtologs('Success', 'Successfuly Created the '+getdisk+' Bio Disk', 'bio_configuration.py', str(create_bio));
		else:
			print""" <div id = 'id_trace_err_small' >"""

                	print "Please Enter a Valid Bio configuration data!"
                	print "</div><br/>"
			logstatus = common_methods.sendtologs('Error', 'Error Occurred while Creating the '+getdisk+' Bio Disk', 'bio_configuration.py', str(create_bio));
		#print """<script>javascript:parent.jQuery.fancybox.close();</script>""";

	get_vol_name = form.getvalue("volume")
	get_free_size = form.getvalue("free_size")

               
	print """ <html>
	<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<title>..::Tyrone Opslag FS2::..</title>
	<script src="../js/jquery1.7.js"></script>
	<script language = 'javascript' src = '../js/commons.js'></script>
	<link href = "../css/jquery.alerts.css" rel = "stylesheet" type = "text/css" />
	<link href = "../css/style.css" rel = "stylesheet" type = "text/css" />
	<link href="../css/style_new.css" rel="stylesheet" type="text/css"/>
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
                $("#id_trace_err_small").fadeOut(2000);
                $("#id_trace_small").fadeOut(2000);
                }
	);
	}
	var tim = window.setTimeout("hideMessage()", 10000);  // 10000 milliseconds = 10 seconds
	</script>

	<script language = 'javascript' src = '../js/jquery-latest-fade.js'></script>



	<style type="text/css">

	.button_example{
	border:1px solid #7c5b2b; -webkit-border-radius: 3px; -moz-border-radius: 3px;border-radius: 3px;font-size:9px;font-family:arial, helvetica, sans-serif; padding: 2px 10px 4px 10px; text-decoration:none; display:inline-block;text-shadow: -1px -1px 0 rgba(0,0,0,0.3); color: #FFFFFF;
	 background-color: #a67939; background-image: -webkit-gradient(linear, left top, left bottom, from(#a67939), to(#845108));
	 background-image: -webkit-linear-gradient(top, #a67939, #845108);
	 background-image: -moz-linear-gradient(top, #a67939, #845108);
	 background-image: -ms-linear-gradient(top, #a67939, #845108);
	 background-image: -o-linear-gradient(top, #a67939, #845108);
	 background-image: linear-gradient(to bottom, #a67939, #845108);filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr=#a67939, endColorstr=#845108);
	cursor:pointer;
	}

	.button_example:hover{
	 border:1px solid #5a421f;
	 background-color: #805d2c; background-image: -webkit-gradient(linear, left top, left bottom, from(#805d2c), to(#543305));
	 background-image: -webkit-linear-gradient(top, #805d2c, #543305);
	 background-image: -moz-linear-gradient(top, #805d2c, #543305);
	 background-image: -ms-linear-gradient(top, #805d2c, #543305);
	 background-image: -o-linear-gradient(top, #805d2c, #543305);
	 background-image: linear-gradient(to bottom, #805d2c, #543305);filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr=#805d2c, endColorstr=#543305);
	}
	</style>
	</head>
	<body onload = 'document.bio_config.action_but.disabled = "true";'>
	"""

	#vg_info = get_pvs()
	vgs_info = storage.get_vgs()
	print """ 

	<form name = 'bio_config' method = 'POST' action = ''>

<table width="90%" style="margin:20px 0 0 20px; text-align:center; border:#D1D1D1 1px solid;"">
<tr>
<td style=" background-color:#D1D1D1; padding:5px;">Create BIO Disk</td>
</tr>
</table>

<table width="90%" style="margin:0px 0 0 20px; border-top:#D1D1D1 1px solid; border-right:#D1D1D1 1px solid; border-left:#D1D1D1 1px solid; font-size:12px;">
<tr>
<th align="left" style="padding:5px;">Selected Volume</th>
<td>"""+get_vol_name+"""</td>
<input type="hidden" name="hid_volume" value='"""+get_vol_name+"""' />
</tr>

<tr>
<th align="left" style="padding:5px;">Available size in Volume</th>
<td>"""+get_free_size+"""</td>
</tr>

<tr>
<th align="left" style="padding:5px;">Enter Disk Name</th>
<td><input class = 'textbox' type = 'text' name = 'disk' id = 'disk' style="width:187px;"></td>    
</tr>

<tr>
<th align="left" style="padding:5px;">Enter Disk Size (GB)</th>
<td><input class = 'textbox' type = 'text' name = 'size' onkeypress="return isNumberKey(event)" id = 'size' style="width:187px;"></td>    
<input type ="hidden" name="free_size2" value="""+str(get_free_size)+""">
<input type="hidden" name="gb_mb" value="GB"  >
</tr>

<tr>
<td><input type="checkbox" name="advance_option" id="adv_chk" onclick = 'return nas_advance_config2() ' /> Advance Options</td>
<td></td>    
    
</tr>

</table>

<table id="adv_txt1"  width="90%" style="margin:0px 0 0 20px; padding:0 0 0 20px; border-left:#D1D1D1 1px solid; border-right:#D1D1D1 1px solid; font-size:12px; display:none;">

<tr>
<th align="right">Format Option</th>
<td><input type= "text" class="textbox" name = "adv1" id = "inpt1_adv1" onclick="enable()" style="width:187px;"/></td>
</tr>

<tr>
<th align="right">Mount Option</th>
<td><input type= "text" class="textbox" name= "adv2" id = "inpt2_adv2" onclick="enable()" style="width:187px;"/></td>
</tr>

</table>

<table width="90%" style="margin:0px 0 0 20px; border-left:#D1D1D1 1px solid; border-right:#D1D1D1 1px solid; border-bottom:#D1D1D1 1px solid; font-size:12px;">
<tr>
<td>
<button class="buttonClass" style="float:right; margin:0 30px 20px 0; font-size:12px;" type="submit" name = 'submit'  id = 'submit' value = 'submit'  onclick = 'return validate_bio_configuration();'>Create</button>
</td>
</tr>


</table>
</form>














          
        </body>
	</html>"""


except Exception as e:
        disp_except.display_exception(e)
