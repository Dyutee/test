#!/usr/bin/python
import traceback

import sys;
sys.path.append('../modules/');
import disp_except;

try:
	#################################################
        ################ import modules #################
        #################################################
	import cgitb,  os, sys, commands, traceback, common_methods, system_info, include_files, cgi
	cgitb.enable()
	sys.path.append('/var/nasexe/storage')
	sys.path.append('/var/nasexe/python/');
	import storage_op, createnasdisk
	from lvm_infos import *
	from functions import *
	form = cgi.FieldStorage()
        sys.path.append('/var/nasexe/python/')
        import tools
        from tools import db
	#--------------------- END --------------------#

	################################################
        ################ Check HA Status ###############
        ################################################
	check_ha = tools.check_ha()
        sys_node_name = tools.get_ha_nodename()
        if(sys_node_name == "node1"):
                other_node = "node2"
                show_tn = "Node1"
                show_on = "Node2"
        else:
                other_node = "node1"
                show_tn = "Node2"
                show_on = "Node1"

        query="select * from network_ifaces where (name='eth1' and node='"+other_node+"')"
        status=db.sql_execute(query)
        for x in status["output"]:
                other_node_ip = x["ip"]
	#--------------------- END --------------------#

	sys.path.append('/var/nasexe/')
	import storage

	log_array = [];
	logstring = '';
	################################################
        ################### Add Volume #################
        ################################################
	if(form.getvalue("submit_create_vol")):
		get_disks = form.getvalue("volume_array[]")
		check_str = isinstance(get_disks, str)
		if(check_str==True):
			get_disks = [get_disks]
		get_vg_name = form.getvalue("x")
		test_name = storage_op.test_vgname(get_vg_name)

		if(test_name == True):
			create_vg = storage_op.vgcreate(get_disks, get_vg_name)
			if(create_vg==True):
				print"""<div id = 'id_trace'>"""
				print " Volume Successfully Created!"
				print "</div>"
				logstatus = common_methods.sendtologs('Success', 'Successfully Creating the '+str(get_disks)+' Volume', 'raid_settings_new.py', str(create_vg));
			else:
				print"""<div id = 'id_trace_err' >"""
				print "Error occured while creating Volume!"
				print "</div>"
				logstatus = common_methods.sendtologs('Error', 'Error Occurred while Creating the '+str(get_disks)+' Volume', 'raid_settings_new.py', str(create_vg));
		else:
			print"""<div id = 'id_trace_err' >"""
			print "Enter Different Volume Name"
			print "</div>"

		print "<script>location.href = 'iframe_raid_settings_new.py#tabs-2';</script>"

		common_methods.append_file(log_file, log_array);
	#--------------------- END --------------------#

	################################################
        ################## Remove Volume ###############
        ################################################
	if(form.getvalue("submit_remove_vol")):
		get_vg_n = form.getvalue("used_volumes_array[]")
		check_get_vg_n = isinstance(get_vg_n, str)

		if(check_get_vg_n == True):
			remove_vg = storage_op.vg_remove(get_vg_n)
		else:
			get_vg_n = set(get_vg_n)
			for value in get_vg_n:
				remove_vg = storage_op.vg_remove(value)
		if(remove_vg == True):
			print"""<div id = 'id_trace'>"""
			print " Volume Successfully Deleted!"
			print "</div>"
			logstatus = common_methods.sendtologs('Success', 'Successfully deleted the Volume', 'raid_settings_new.py', str(remove_vg));
		else:
			print"""<div id = 'id_trace_err' >"""
			print "Error occured while deleting Volume!"
			print "</div>"

			logstatus = common_methods.sendtologs('Error', 'Error Occurred while deleting the Volume', 'raid_settings_new.py', str(remove_vg));
		print "<script>location.href = 'iframe_raid_settings_new.py#tabs-3';</script>"
	#--------------------- END --------------------#

	#--- Get PVS
	vg_info = storage.get_pvs()
	#--- Get VGS
	vgs_info = storage.get_vgs()
	#--- Get LVS
	nas_info = storage.get_lvs()
	#--- Get free disks
	free_d = storage.free_disks()

	print
	print """
		<div id="loader-div" style="text-align:center; display:none;" ><img style="margin-top:20%;" src="../images/ajax-loader.gif" /><br/> Loading...</div>
	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer" id="body-div">
		<!--tab srt-->
		<div class="searchresult-container">
		<div class="searchresult-container">
                <div style="margin:0 0 0px 0;" class="topinputwrap-heading"><a class="demo" href ="#"><img src ="../images/help_icon1.png" style="width:13px;"><span class="tooltip" >
                 <table border="0">
        <tr>
        <td class="text_css">This page allows you to create or remove RAID volumes.</td>
        </tr>
        </table>"""
	if(check_ha == True):
		print"""</span></a><span class = "gap_text" style="color:#fff;margin-left:7px;">RAID Information ("""+show_tn+""")</span>
                <span style="float:right; margin:0 0px 0 0;"><a onclick="return onclick_loader();" class="resource_links" href="https://"""+other_node_ip+"""/fs4/py/iframe_raid_settings_new.py">"""+show_on+"""</a></span>

                </div>"""
	else:
		print"""</span></a>Raid Information </div>"""
	print"""
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
	"""
	if(free_d!=[]):
		print """
		<form name = 'add_volume' action = '' method = 'POST'>
		<table width = "685">
		<tr>
		<th style="border:#D1D1D1 1px solid; padding:5px;"><input type = 'checkbox' name='select_all_free_disks' id = 'id_select_free_disks' title = 'Check this to select all' onclick = 'return select_all_disks();'></th>
		<th style="border:#D1D1D1 1px solid; padding:5px;">Disk</th>
		<th style="border:#D1D1D1 1px solid; padding:5px; width:40%;">Size</th>
		</tr>

		"""

		for z in free_d:
			print """
			<tr>
			<td align="center" style="border:#D1D1D1 1px solid; padding:5px;"><input type = 'checkbox' name = 'volume_array[]' id = 'id_volume_array' value = '"""+z["disk"]+"""' onclick="return show_input_textbox();"></td>
			<td align="center" style="border:#D1D1D1 1px solid; padding:5px;">"""
			print z["disk"]
			print """</td>
			<td align="center" style="border:#D1D1D1 1px solid; padding:5px;">"""
			gb_size = str(int(z["size"])/1048576)+" GB"

			print gb_size
			print """</td>
			</tr>"""

		print """
		<tr>
		<td></td>
		<td align="center"></td>
		<td align="right"><input class="textbox" type="hidden" id="x" name="x" value="Volume Name"  onfocus="if (this.value == 'Volume Name') this.value = '';" onblur="if (this.value == '') this.value = 'Volume Name';" style="width:120px;"/></td>
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
	 <button class="buttonClass" type="submit" name = 'submit_create_vol' value = 'Create Volume' onclick = "return validate_create_vol_form();" >Create</button></div>


		<input type = 'hidden' name = 'hid_page' value = ''>
		<input type = 'hidden' name = 'proceed_page' value = 'proceed'>
	</td></tr></table>
		</form>"""
	else:
		#print "<div style='font-size:14px; font-weight:bold; text-align:center;margin-top:19%;'><span style='text-align: center; float: left; padding-left:230px;width:97%;color:#2C2222;'> No free disks available!</span> </div>"
		print"<div style='text-align:center; width:100%;margin-left:220px;'> No free disks available!</div>"

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

	<div id="tabs-3">
	<!--form container starts here-->
	<div class="form-container">
	<!--<div class="topinputwrap-heading">Remove Volume Group</div>-->
	<div class="inputwrap">
	<div class="formleftside-content">
	"""


	if(vg_info["pvs"]!=[{}]):
		print """
		<form name = 'remove_vol' action = '' method = 'POST'>
		<table width = "685" >
		<tr>
		<th style="border:#D1D1D1 1px solid; padding:5px;"><input type = 'checkbox' name = 'select_all' title = 'Click to select all' id = 'id_select_all' onclick = 'return select_all_volumes();'></th>
		<th style="border:#D1D1D1 1px solid;">Disk</th>
		<th style="border:#D1D1D1 1px solid;">Volume</td>
		<th></th>
		</tr>"""

		for y in vg_info["pvs"]:
			if (y['used'] == '0g'):
				disabledstr = ''
			else:
				disabledstr = 'disabled'

			print """
			<tr>
			<td align="center" style="border:#D1D1D1 1px solid; padding:5px;"><input type = 'checkbox' value = '"""+y["vg_name"]+"""' name = 'used_volumes_array[]' id = 'id_used_volumes' """ + disabledstr + """></td>

			<td align="center" style="border:#D1D1D1 1px solid; padding:5px;">"""
			for x in vg_info["pvs"]:
				if(x["vg_name"]==y["vg_name"]):
					print x["pv_name"]
			print """</td>

			<td align="center" style="border:#D1D1D1 1px solid; padding:5px;">"""
			print y["vg_name"]
			print """</td>

				</tr>"""
		print """
			</table><BR>

			<table align = 'center' width = '685'>
			<tr>
			<td>
			<div style="float:right;margin-top:-3%;">
			<button class="buttonClass" type="submit" name = 'submit_remove_vol' value = 'Remove selected' onclick = 'return confirm_delete_volume();'>Remove</button></div>

			</td>
			</tr>
			</table>

			</form> 
			"""
	else:
		#print "<div style='width:100%;padding:15px 0 23px 266px; font-size:14px; font-weight:bold;color:#2C2222;'>No disks available! </div>"
		print"<div style='text-align:center; width:100%;margin-left:220px;'> No disks available!</div>"

		
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

	<!-- ####### Sub Tabs Start ####### -->

	<script>
	$("#tabs, #subtabs").tabs();
	$("#tabs, #subsubtabs").tabs();
	</script>

	<!-- ####### Sub Tabs End ####### -->

	"""

except Exception as e:
	disp_except.display_exception(e);
