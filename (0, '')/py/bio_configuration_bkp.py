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
        		print""" <div id = 'id_trace' >"""
                	print " BIO Disk " " <b><font color ='darkred'>"+ getdisk +"</font></b> " "  Successfully created!"
			print "</div>"
			logstatus = common_methods.sendtologs('Success', 'Successfuly Created the '+getdisk+' Bio Disk', 'bio_configuration.py', str(create_bio));
		else:
			print""" <div id = 'id_trace_err' >"""

                	print "Please Enter a Valid Bio configuration data!"
                	print "</div>"
			logstatus = common_methods.sendtologs('Error', 'Error Occurred while Creating the '+getdisk+' Bio Disk', 'bio_configuration.py', str(create_bio));
		#print """<script>javascript:parent.jQuery.fancybox.close();</script>""";

               
	print """ <html>
	<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<title>..::Tyrone Opslag FS2::..</title>
	<script src="../js/jquery1.7.js"></script>
	<script language = 'javascript' src = '../js/commons.js'></script>
	<link href = "../css/jquery.alerts.css" rel = "stylesheet" type = "text/css" />
	<link href = "../css/style.css" rel = "stylesheet" type = "text/css" />
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
       	<table width = '100%' style = 'font-weight: bold;margin-top: 6%;'>
	<tr>
	<td width = "296" height = "35px" valign = "middle">
	<b><i><font color ="darkred" style="font-size:18px;" >Bio Disk Configuration</font></i></b> <br/> <br/></td><td><font color ="darkred">Available Size:</font><font color = "green" style = "text-decoration:blink;">"""+free_sizes+"""</font></td></tr></table><br/><br/><br/>"""


	#vg_info = get_pvs()
	vgs_info = storage.get_vgs()
	print """ 
		<form name = 'bio_config' id = 'bio_configs' method = 'POST' action="">
		
		<div style="margin-left: 24%;margin-top: 12%;">
		<table width="150" cellspacing="0" cellpadding="0" border="0" style="margin-top:-73px;margin-left:5%;">
					<tr>
						<td valign="top" align="left" colspan="3">
						<table width="366" align="center" cellspacing="0" cellpadding="0" border="0" >
									<tbody>
		<tr>
		<td width = "172" class = "table_heading" height = "35px" valign = "middle">

		<span style="margin-left: 17%;color:#666666;"><b>Volume</b>:</span>

		</td>

		<td><input type="text" style="font-weight:lighter; text-align:center; margin-top:5%; margin-left:25%;"name="volume_nas" id ='volume_nas' readonly size ="8" value=""" + volume_info + """  ></td>
		</tr>

		<tr>
			<td width = "172" class = "table_heading" height = "35px" valign = "middle">
		<span style="margin-left: 17%;color:#666666;"><b>Disk</b>:</span>
			</td>
			<td width = "172" class = "table_content" height = "35px" valign = "middle" >
				<input lass = 'textbox' size ="8" type = 'text' style = "margin-left:25%;"  name = 'disk' id ='disk' value = '' oninput = 'enable_apply_button();'>
				<input type = 'hidden' name = 'old_ip_val' value = ''>
			</td>
		</tr>
		<tr>
			<td width = "172" class = "table_heading" height = "35px" valign = "middle">
		<span style="margin-left: 17%;color:#666666;"><b>Size</b>:</span>
			</td>
			<td width = "172" class = "table_content" height = "35px" valign = "middle" >

				<input lass = 'textbox' onkeypress="return isNumberKey(event)"  size="8" type = 'text' name = 'size' id ='size' value = "" oninput = 'enable_apply_button();' style="margin-left: 25%;">
	
		<td><input type="text" style="font-weight:lighter; text-align:center; margin-top:5%; margin-left:25%;"name="gb_mb" readonly size ="1" value="GB"  ></td>
	<!--<td valign = 'middle'>
							<select class = 'input' name = 'gb_mb' style = ' margin-right: 20px; margin-left:32%;'>                                                                                 
								<option value = 'select' >Select</option>	                                                                    
								<option value = 'GB'>GB</option>
								<option value = 'TB'>TB</option>
							</select>
						</td>-->

	<input type = 'hidden' name = 'old_nm_val' value = ''>
	</td>
		</tr>
		<tr>
		 <td><input type ="hidden" name="free_size" value="""+free_sizes+"""></td>
		</tr>

		<tr>

<td><span  style="margin-left: 15%;"><input type="checkbox" name="chck" id="adv_chk" onclick = 'return nas_advance_config() ' /></span></td>
			<td width = "172" class = "table_heading" height = "35px" valign = "middle"><span style="margin-left: -50%;color:#EC1F27;">Advance Option:</span></td>
		</tr>
		<tr>
		<td width = "0" id = "adv_txt1" height = "35px" valign = "middle "style = 'display:none;'><span style="margin-left:18%;color:#666666;">Format Option:</span><td width = "172" class = "table_content" height = "35px" valign = "middle" ><input type= "text"  size = "8" name = "adv1" id = "inpt1_adv1" onclick="enable()" style = 'display: none; margin-left:25%;'/></td></tr>
<tr>
	<td width = "0" id ="adv_txt2"  height = "35px" valign = "middle" style = 'display:none;'><span style="margin-left:18%;color:#666666;">Mount Option:</span><td width = "172" class = "table_content" height = "35px" valign = "middle" ><input type= "text" size ="8" name= "adv2" id = "inpt2_adv2" onclick="enable()"  style = 'display: none;margin-left: 25%;'/></td>
		</tr>
		<tr>
			<td>
			</td>
                        </tr>
                        <tr>
                                <td>
                                </td>
                        </tr>
                        <tr>
                                <td colspan = '4' align = 'right'>

	<!--<div style="margin-left: 54%;" ><span id="button-one"><button type = 'submit' name="submit" id="id_create_but" value="Create" onclick ="return validate_nas_configuration();" style = 'width:62px; background-color:#E8E8E8; border:none; float: right;font-size: 86%; ' title="Create"><a style="font-size:100%;">Create</a></button></span></div>-->
	<div>
	<button class="button_example" type="submit" name = 'submit'  id = 'id_create_but' value = 'Create' onclick = 'return validate_bio_configuration();'>Create</button></div>






                                </td>
                        </tr>
                        </tbody>
			</table>

		</table>
		
	</div>
                </form>
	</table>
          
        </body>
	</html>"""


except Exception as e:
        disp_except.display_exception(e)
