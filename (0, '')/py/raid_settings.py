#!/usr/bin/python
import traceback

import sys;
sys.path.append('../modules/');
import disp_except;

try:
	import cgitb, header, os, sys, commands, traceback, common_methods, system_info
	cgitb.enable()

	sys.path.append('/var/nasexe/storage')
	sys.path.append('/var/nasexe/python/');
	import storage_op, createnasdisk
	from lvm_infos import *
	from functions import *

	sys.path.append('/var/nasexe/')
	import storage

	log_array = [];
	#log_file = common_methods.log_file;
	logstring = '';
	#-------------------------Add Volume---------------------------
	if(header.form.getvalue("submit_create_vol")):
		get_disks = header.form.getvalue("volume_array[]")
		#print get_disks
		check_str = isinstance(get_disks, str)
		#print check_str
		if(check_str==True):
			get_disks = [get_disks]
		get_vg_name = header.form.getvalue("x")
		#print get_vg_name
		test_name = storage_op.test_vgname(get_vg_name)
		#print test_name

		#ss = str(test_name)+" Volume Name"
		#logstring = str(common_methods.now) + '<<>>From: ' + common_methods.remote_ip + '<<>>' + str(ss);
		#log_array.append(logstring);

		if(test_name == True):
			create_vg = storage_op.vgcreate(get_disks, get_vg_name)
			#print create_vg

			ss = str(create_vg)+" Creating Volume"
			logstring = str(common_methods.now) + '<<>>From: ' + common_methods.remote_ip + '<<>>' + str(ss);
			log_array.append(logstring);

			if(create_vg==True):
				autostatus = createnasdisk.autocreatenasdisk(get_vg_name, 'rrd_data', '300GB');

				if (autostatus == 'success'):
					os.chdir('/storage/rrd_data/');

					commands.getoutput('sudo mkdir -p rrddata/db/');
					commands.getoutput('sudo mkdir -p rrddata/db/network/');
					commands.getoutput('sudo mkdir -p rrddata/db/disks/');

					commands.getoutput('sudo mkdir -p rrddata/png/');
					commands.getoutput('sudo mkdir -p rrddata/png/temperature/');
					commands.getoutput('sudo mkdir -p rrddata/png/network/');
					commands.getoutput('sudo mkdir -p rrddata/png/disks/');
					commands.getoutput('sudo mkdir -p rrddata/png/memory/');
				print"""<div id = 'id_trace'>"""
				print " Volume Successfully Created!"
				print "</div>"
			else:
				print"""<div id = 'id_trace_err' >"""
				print "Error occured while creating Volume!"
				print "</div>"
		else:
			print"""<div id = 'id_trace_err' >"""
			print "Enter Different Volume Name"
			print "</div>"

		print "<script>location.href = 'main.py?page=rs#tabs-2';</script>"

		common_methods.append_file(log_file, log_array);


	#---------------------------------End------------------------------------------------------

	#----------------------------------Remove Volume------------------------------------------
	if(header.form.getvalue("submit_remove_vol")):
		get_vg_n = header.form.getvalue("used_volumes_array[]")
		check_get_vg_n = isinstance(get_vg_n, str)

		if(check_get_vg_n == True):
			remove_vg = storage_op.vg_remove(get_vg_n)
		else:
			get_vg_n = set(get_vg_n)
			for value in get_vg_n:
				remove_vg = storage_op.vg_remove(value)

		ss = str(remove_vg)+" Removing Volume"
		logstring = str(common_methods.now) + '<<>>From: ' + common_methods.remote_ip + '<<>>' + str(ss);
		log_array.append(logstring);
		common_methods.append_file(log_file, log_array);

		if(remove_vg == True):
			print"""<div id = 'id_trace'>"""
			print " Volume Successfully Deleted!"
			print "</div>"
		else:
			print"""<div id = 'id_trace_err' >"""
			print "Error occured while deleting Volume!"
			print "</div>"

		print "<script>location.href = 'main.py?page=rs#tabs-3';</script>"

	#------------------------------------End----------------------------------------------------

	vg_info = storage.get_pvs()
	vgs_info = storage.get_vgs()
	nas_info = storage.get_lvs()
	free_d = storage.free_disks()
	#----------------------------------------------------------------------------------------------

	import left_nav
	print
	print """

	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer">
		<div class="insidepage-heading">Raid Configuration >> <span class="content">Raid/Volume Set Options</span></div>
		<!--tab srt-->
		<div class="searchresult-container">
		  <div class="infoheader">
		    <div id="tabs">
		      <ul>
			<li><a href="#tabs-2">Add Volume</a></li>
			<li><a href="#tabs-3">Remove Volume</a></li>
		      </ul>
		      <div id="tabs-2">
		<!--form container starts here-->
		<div class="form-container">
		  <!--<div class="topinputwrap-heading">Add Volume Group</div>-->
		  <div class="inputwrap">
		 <div class="formleftside-content">
	<table class="border" width = "685" border = "0"  cellspacing = "0" cellpadding = "0">"""
	if(free_d!=[]):
		print """<tr class='readonly'>
		<td width = "311" class = "table_content" height = "35px" valign = "middle" bgcolor = "#f5f5f5">
		<input type = 'checkbox' name='select_all_free_disks' id = 'id_select_free_disks' title = 'Check this to select all' onclick = 'return select_all_disks();'>
		</td>
		<td width = "311"  height = "35px" valign = "middle" bgcolor = "#f5f5f5">
		<font color = "#EC1F27">Disk</font>
		</td>
		<td width = "311"  height = "35px" valign = "middle" bgcolor = "#f5f5f5">
		<font color = "#EC1F27">Size</font>
		</td>
		</tr>
		<form name = 'add_volume' action = '' method = 'POST'>"""

		for z in free_d:
			print """<tr>
			<td width = "311" class = "table_content" height = "35px" valign = "middle" bgcolor = "#f5f5f5">
			<input type = 'checkbox' name = 'volume_array[]' id = 'id_volume_array' value = '"""+z["disk"]+"""' onclick="return show_input_textbox();">
			</td>
			<td width = "311" class = "table_content" height = "35px" valign = "middle" bgcolor = "#f5f5f5">"""
			print z["disk"]
			print """</td>
			<td width = "311" class = "table_content" height = "35px" valign = "middle" bgcolor = "#f5f5f5">"""
			gb_size = str(int(z["size"])/1048576)+" GB"

			print gb_size
			print """</td>
			</tr>"""
		print """
		<tr>
		<td></td>
		<td align="center"></td>
		<td align="center"><input type="hidden" id="x" name="x" value="Volume Name"  onfocus="if (this.value == 'Volume Name') this.value = '';" onblur="if (this.value == '') this.value = 'Volume Name';" style="width:120px;"/></td>
		</tr>

		<input type= 'hidden' name = 'hid_size' value = ''>

		</table>
		<table align = 'center' width = '685'>
		<tr>
		<td>
		<!--<BR><input class = 'input1' type = 'button' name = 'action_but' value = 'Create volume' onclick = 'return validate_create_vol_form();'>-->
		<BR><!--<input type="submit" name="submit_create_vol" value="Create Volume" class = "input1" onclick = "return validate_create_vol_form();" />-->
		<!--<div style="margin-right:2%;"><span id="button-one"><button type = 'submit' name="submit_create_vol" value="Create Volume" onclick = "return validate_create_vol_form();"  style = 'width:100px; background-color:#ffffff; border:none; float: right;font-size: 100%;' title="Create"><a style="font-size:85%;  width: 115%;">Create Volume</a></button></span></div>-->

	<div style = "float:right;">
	 <button class="button_example" type="submit" name = 'submit_create_vol' value = 'Create Volume' onclick = "return validate_create_vol_form();" >Create Volume</button></div>


		<input type = 'hidden' name = 'hid_page' value = ''>
		<input type = 'hidden' name = 'proceed_page' value = 'proceed'>
	</td></tr></table>
		</form>"""
	else:
		print "<div style='font-size:14px; font-weight:bold; text-align:center;'><span style='text-align: center; float: left; padding-left: 100%; width: 95%;color:#2C2222;'> No free disks available!</span> </div>"

	print """
		</td>
		</tr>
		</table>
		
		


		</div>
		  </div>
		</div>
		<!--form container ends here-->
		<p>&nbsp;</p>
		      </div>

		      <!--<div id="tabs-1">


			 <div id="subtabs">

			  <ul>
			    <li><a href="#subtabs-1">Configure Raid Set</a></li>
			    <li><a href="#subtabs-2">Configure Volume Set</a></li>

			    <li><a href="#subtabs-3">Configure Physical Drives</a></li>

			    <li><a href="#subtabs-4">Information</a></li>

			  </ul>
			 <div id="subtabs-1">
			 <div id="subsubtabs">

			  <ul>

			    <li><a href="#subsubtabs-1">Create Raid</a></li>

			    <li><a href="#subsubtabs-2">Delete Raid</a></li>

			    <li><a href="#subsubtabs-3">Expand Raid</a></li>
			    <li><a href="#subsubtabs-4">Offline Raid</a></li>
			   <li><a href="#subsubtabs-5">Activate Raid</a></li>
			  <li><a href="#subsubtabs-6">Create hotspare</a></li>
			  <li><a href="#subsubtabs-7">Delete hotspare</a></li>


			  </ul>

			  <div id="subsubtabs-1">

			Create Raid

			  </div>
			<div id="subsubtabs-2">

			Delete Raid

			  </div>
			<div id="subsubtabs-3">

			Expand Raid

			  </div>

			<div id="subsubtabs-4">

			Offline Raid

			  </div>

		<div id="subsubtabs-5">

			Activate Raid

			  </div>

		<div id="subsubtabs-6">

			Create hotspare

			  </div>

		<div id="subsubtabs-7">

			Delete hotspare

			  </div>
		</div>

		</div>
			 <div id="subtabs-2">
	<div>

			Configure Volume		

			  </div>

			  </div>


	  <div id="subtabs-3">
				<div>

			Physical Drives 

				</div>
			  </div>

	  <div id="subtabs-4">
				<div>

			Information

				</div>
			  </div>

		

	</div>

		<p>&nbsp;</p>
		</div>-->
		<div id="tabs-3">
		<!--form container starts here-->
		<div class="form-container">
		  <!--<div class="topinputwrap-heading">Remove Volume Group</div>-->
		  <div class="inputwrap">
		 <div class="formleftside-content">
		 <table width = "685" border = "0" cellspacing = "0" cellpadding = "0" class = "border">"""


	if(vg_info["pvs"]!=[{}]):
		print """<tr>
		<td width = '1%'  height = "35px" valign = "middle">
		<input type = 'checkbox' name = 'select_all' title = 'Click to select all' id = 'id_select_all' onclick = 'return select_all_volumes();'>
		</td>
		<td  height = "35px" valign = "middle">
		<font color = "#EC1F27">Disk</font>
		</td>
		<td  height = "35px" valign = "middle">
		<font color = "#EC1F27">Volume</font>
		</td>
		<td></td>
		</tr>
		<form name = 'remove_vol' action = '' method = 'POST'>"""

		for y in vg_info["pvs"]:
			print """<tr>
			<td class = "table_content" height = "35px" valign = "middle">"""
			if (y['used'] == '0g'):
				disabledstr = '';

			else:
				disabledstr = 'disabled';

			print"""<input type = 'checkbox' value = '"""+y["vg_name"]+"""' name = 'used_volumes_array[]' id = 'id_used_volumes' """ + disabledstr + """>"""
			print"""</td>
			<td class = "table_content" height = "35px" valign = "middle">"""
			for x in vg_info["pvs"]:
				if(x["vg_name"]==y["vg_name"]):
					print x["pv_name"]
			print """</td>
			<td class = "table_content" height = "35px" valign = "middle">"""
			print y["vg_name"]
			print """</td>

				</tr>"""
		print """
			</table><BR>
			<table align = 'center' width = '685'>
			<tr>
			<td>
			<!--<input class = 'input1' type = 'submit' name = 'submit_remove_vol' value = 'Remove selected' onclick = 'return confirm_delete_volume();'>-->
			<!--<div style="margin-right:2%;"><span id="button-one"><button type = 'submit' name = 'submit_remove_vol' value = 'Remove selected' onclick = 'return confirm_delete_volume();' style = 'width:100px; background-color:#ffffff; border:none; float: right;font-size: 100%;' title="Remove"><a style="font-size:85%;  width: 115%;">Remove selected</a></button></span></div>-->
	<div style="float:right;margin-top:-3%;">
		<button class="button_example" type="submit" name = 'submit_remove_vol' value = 'Remove selected' onclick = 'return confirm_delete_volume();'>Remove</button></div>


			</td></tr></table>
			</form> 
			</tr>"""
	else:
		print "<div style='width:100%;padding:15px 0 23px 266px; font-size:14px; font-weight:bold;color:#2C2222;'>No disks available! </div>"

	print """
									</table>"""
		
	print"""        </div>
		  </div>
		</div>
		<!--form container ends here-->
		<p>&nbsp;</p>
		      </div>
		
	<!--<div id="tabs-4">
		<div class="form-container">
		  <div class="topinputwrap-heading">Volume Group Information</div>
		  <div class="inputwrap">
		 <div class="formleftside-content">
		
		 Volume Information

		</div>
		  </div>
		</div>
		<p>&nbsp;</p>
		      </div>-->

		
		</div>
		    </div>
		  </div>
		</div>
		<!--form container ends here-->
		<!--form container starts here-->
		<!--form container ends here-->
	      </div>
	      <!--Right side body content ends here-->
	    </div>
	    <!--Footer starts from here-->
	    <div class="insidefooter footer_content">&copy; 2013 Opslag FS2</div>
	    <!-- Footer ends here-->
	  </div>
	  <!--inside body wrapper end-->
	</div>
	<!--body wrapper end-->
	</body>
	</html>

	<!-- ####### Sub Tabs Start ####### -->

	<script>
	$("#tabs, #subtabs").tabs();
	$("#tabs, #subsubtabs").tabs();
	</script>

	<!-- ####### Sub Tabs End ####### -->

	"""

except Exception as e:
	disp_except.display_exception(e);
