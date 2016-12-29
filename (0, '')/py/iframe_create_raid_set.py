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
	form = cgi.FieldStorage()
        sys.path.append('/var/nasexe/python/')
        import tools
        from tools import db
	from tools import raid_controller

	sys.path.append("/var/nasexe/python/tools/")
	import raid
	import datetime
	now = datetime.datetime.now()
	import time
	#--------------------- END --------------------#

	#--- Raid Controller Name
	raid_cont_name = raid_controller.raid_c()

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

	################################################
        ################# Identify Disk ################
        ################################################
	readonly_raid_set = ""
	get_selected_raid = ''
	if(form.getvalue("identify_disk")):
		get_index = form.getvalue("identify_disk")
		start_blinking = raid.idendify_drive('0000',int(get_index))
		time.sleep(20)
		stop_blinking = raid.idendify_drive('0000',0)
	#--------------------- END --------------------#

	################################################
        ################ Create Hotspare ###############
        ################################################
	if(form.getvalue("create_hotspare")):
		get_raid_set = form.getvalue("select_raid_set")
		get_disk = form.getvalue("select_disk")
		get_hotspare_type = form.getvalue("select_hotspare_type")
		if((get_raid_set == "select-raid") or (get_disk == "select-disk") or (get_hotspare_type == "select-hotspare")):
			print "<div id='id_trace_err'>"
                        print "Select all the values!"
			print "</div>"
		else:
			create_hotspare_cmd = raid.create_hotspare(ctrl_passwd='0000',free_disk_index=int(get_disk),hs_type=int(get_hotspare_type),raid_index=int(get_raid_set),enc_index=0,debug=True)
			if(create_hotspare_cmd == True):
				print "<div id='id_trace'>"
                                print "Successfully created Hot Spare!"
                                print "</div>"
			else:
				print "<div id='id_trace_err'>"
                                print "Error creating Hot Spare!"
                                print "</div>"
	#--------------------- END --------------------#

	################################################
        ################ Delete Hotspare ###############
        ################################################
	if(form.getvalue("delete_hotspare")):
		get_index = form.getvalue("hotspare_id")
		if(get_index != None):
			delete_hotspare_cmd = raid.delete_hotspare(ctrl_passwd='0000',hsd_index=get_index,debug=False)
			if(delete_hotspare_cmd == True):
				print "<div id='id_trace'>"
                                print "Successfully deleted Hot Spare!"
                                print "</div>"
			else:
				print "<div id='id_trace_err'>"
                                print "Error deleting Hot Spare!"
                                print "</div>"
		else:
			print "<div id='id_trace_err'>"
			print "Select a Hotspare to delete!"
			print "</div>"
	#--------------------- END --------------------#

	################################################
        ################ Create RAID Set ###############
        ################################################
	if(form.getvalue("create_raid_set")):
		get_indexes = form.getvalue("volume_array[]")
		get_raid_name = form.getvalue("raid_set_name")
		if(get_indexes != None):
			if(isinstance(get_indexes,str) == True):
				get_indexes = [get_indexes]	
			if(get_raid_name == None):
				get_raid_name = ""

			create_raid_set_cmd = raid.create_raidset("0000",get_indexes,name=get_raid_name,debug=False)
			if(create_raid_set_cmd == True):
				print "<div id='id_trace'>"
				print "Successfully created RAID Set!"
				print "</div>"
			else:
				print "<div id='id_trace_err'>"
				print "Error creating RAID Set!"
				print "</div>"
		else:
			print "<div id='id_trace_err'>"
			print "Select Disk(s)!"
			print "</div>"
	#--------------------- END --------------------#

	################################################
        ################ Delete RAID Set ###############
        ################################################
	if(form.getvalue("delete_raid_set")):
		get_indexes = form.getvalue("volume_array2")
		if(get_indexes != None):
			if(isinstance(get_indexes,str) == True):
				get_indexes = int(get_indexes)
				delete_raid_set_cmd = raid.delete_raidset("0000",get_indexes,debug=False)
				if(delete_raid_set_cmd == True):
					print "<div id='id_trace'>"
					print "Successfully deleted RAID Set!"
					print "</div>"
				else:
					print "<div id='id_trace_err'>"
					print "Error deleting RAID Set!"
					print "</div>"
		else:
			print "<div id='id_trace_err'>"
			print "Select a Raidset!"
			print "</div>"
	#--------------------- END --------------------#

	#--- Get Free Disks
	free_disks = raid.get_free_disks()
	#--- Get all RAID set
	raid_sets = raid.get_all_rsf_info()
	#--- Get Hotspare disks
	hs_disks = raid.get_hotspare_disks()

	print
	print """
		<div id="loader-div" style="text-align:center; display:none;" ><img style="margin-top:20%;" src="../images/ajax-loader.gif" /><br/> Loading...</div>
	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer" id="body-div">"""
	if raid_cont_name != "ARECA":
		print """<div style="width:700px; text-align:center; margin:200px 0 0 0; color:#8A0808; font-size:16px;">Use third party RAID Manager!</div>"""
	else:
		print """
			<!--tab srt-->
			<div class="searchresult-container">
			<div style="margin:0 0 0px 0;" class="topinputwrap-heading"><a class="demo" href ="#"><img src ="../images/help_icon1.png" style="width:13px;"><span class="tooltip" >
			 <table border="0">
		<tr>
		<td class="text_css">This page allows you to create and delete RAID sets and hot spares.</td>
		</tr>
		</table>"""
		if(check_ha == True):
			
			print"""</span></a><span class = "gap_text" style="color:#fff;margin-left:7px;">Raid Information ("""+show_tn+""")</span>
			<span style="float:right; margin:0 0px 0 0;"><a onclick="return onclick_loader();" class="resource_links" href="https://"""+other_node_ip+"""/fs4/py/iframe_create_raid_set.py">"""+show_on+"""</a></span>
			</div>"""
		else:
			print"""</span></a>Raid Information </div>"""
		print"""
			  <div class="infoheader">
			    <div id="tabs">
			      <ul>
				<li><a href="#tabs-1">Create RAID Set</a></li>
				<li><a href="#tabs-2">Delete RAID Set</a></li>
				<li><a href="#tabs-3">Create Hot Spare</a></li>
				<li><a href="#tabs-4">Delete Hot Spare</a></li>
			      </ul>

		<div id="tabs-1">
		<!--form container starts here-->
		<div class="form-container">
		<div class="inputwrap">
		<div class="formleftside-content">"""
		if(free_disks != []):
			print """<form name="add_volume" method="POST" action="iframe_create_raid_set.py#tabs-1" >
			<table width="600px">
			<tr>
			<th style="border:#D1D1D1 1px solid; padding:5px;"><input type = 'checkbox' name='select_all_free_disks' id = 'id_select_free_disks' title = 'Check this to select all' onclick = 'return select_all_disks();'></th>
			<th style="border:#D1D1D1 1px solid; padding:5px;">Disk</th>
			<th style="border:#D1D1D1 1px solid; padding:5px;">Size</th>
			<th style="border:#D1D1D1 1px solid; padding:5px;">Identify Disk</th>
			</tr>"""

			for x in free_disks:
				print """<tr>
				<td align="center" style="border:#D1D1D1 1px solid; padding:5px;"><input type = 'checkbox' name = 'volume_array[]' id = 'id_volume_array' value='"""+x["#"]+"""'></td>
				<td align="center" style="border:#D1D1D1 1px solid; padding:5px;">"""+x["Enc#"]+' '+x["Slot#"]+' '+x["ModelName"]+"""</td>
				<td align="center" style="border:#D1D1D1 1px solid; padding:5px;">"""+x["Capacity"]+"""</td>
				<td align="center" style="border:#D1D1D1 1px solid; padding:5px;"><button class="buttonClass" type = 'submit' name = 'identify_disk' value = '"""+x["#"]+"""' onclick="alert('The LED will blink for 20 seconds!');">Identify</button></td>
				</tr>"""

			print"""</table>	

			<table width="600px" style="margin:0px 0 10px 0; border:#D1D1D1 1px solid; padding:0 0 0 10px; background-color:#D1D1D1;">
			<tr>
			<td>RAID Set Name</td>
			<td><input class="textbox" type="text" name="raid_set_name" /></td>
			</tr>
			</table>

			<table width="600px">
			<tr>
			<td><button class="buttonClass" type = 'submit' name = 'create_raid_set' value = 'create_raid_set' style="float:right;" >Create Raid set</button></td>
			</tr>
			</table>

			</form>"""
		else:
			print """<div style="text-align:center; margin:10px 0 10px 0; width:600px;">No free disk available!</div>"""

		print """</div>
		</div>
		</div>
		<!--form container ends here-->
		<p>&nbsp;</p>
		</div>

			
		<div id="tabs-2">
		<!--form container starts here-->
		<div class="form-container">
		<div class="inputwrap">
		<div class="formleftside-content">

		<form name="delete_raid_set_form" method="post" action="iframe_create_raid_set.py#tabs-2">
		<table width="600px">
		<tr>
		<th style="border:#D1D1D1 1px solid; padding:5px;">Select RAID Set</th>
		<th style="border:#D1D1D1 1px solid; padding:5px;">RAID set</th>
		<th style="border:#D1D1D1 1px solid; padding:5px;">No. of Disks</th>
		<th style="border:#D1D1D1 1px solid; padding:5px;">Size</th>
		<th style="border:#D1D1D1 1px solid; padding:5px;">State</th>
		</tr>"""

		for r in raid_sets:
			check_raidset = raid.is_raidset_empty(r["#"])
			if(check_raidset == False):
				readonly_raid_set = "disabled"
			print """<tr>
			<td align="center" style="border:#D1D1D1 1px solid; padding:5px;"><input type = 'radio' name = 'volume_array2' id = 'id_volume_array2' value='"""+r["#"]+"""' """+readonly_raid_set+"""></td>
			<td align="center" style="border:#D1D1D1 1px solid; padding:5px;">"""+r["Name"]+"""</td>
			<td align="center" style="border:#D1D1D1 1px solid; padding:5px;">"""+r["Disks"]+"""</td>
			<td align="center" style="border:#D1D1D1 1px solid; padding:5px;">"""+r["TotalCap"]+"""</td>
			<td align="center" style="border:#D1D1D1 1px solid; padding:5px;">"""+r["State"]+"""</td>
			</tr>"""

		print """</table>	

		<table width="600px">
		<tr>
		<td><button class="buttonClass" type = 'submit' name = 'delete_raid_set' value = 'delete_raid_set' style="float:right;" onclick=" return confirm('Are you sure you want to delete this Raid Set?');">Delete</button></td>
		</tr>
		</table>
		</form>

		</div>
		</div>
		</div>
		<!--form container ends here-->
		<p>&nbsp;</p>
		</div>

		<div id="tabs-3">
		<!--form container starts here-->
		<div class="form-container">
		<div class="inputwrap">
		<div class="formleftside-content">"""
		if(free_disks != []):
			print """<form name="create_hotspare" method="POST" action="iframe_create_raid_set.py#tabs-3" >
			<table width="600px">
			<tr>
			<th align="left">Select RAID Set</th>
			<td>

			<div class="styled-select2">
			<select name="select_raid_set" >
			<option value='select-raid'>Select RAID Set</option>"""
			for r in raid_sets:
				if(r["Name"] != "PassThroughDisk"):
					print """<option value='"""+r["#"]+"""'>"""+r["Name"]+"""</option>"""

			print """</select>
			</div>

			</td>
			</tr>

			<tr>
			<th align="left">Select Disk</th>
			<td>
			<div class="styled-select2">
			<select name="select_disk" >
			<option value='select-disk'>Select Disk</option>"""
			for x in free_disks:
				print """<option value='"""+x["#"]+"""'>"""+x["Enc#"]+' '+x["Slot#"]+' '+x["ModelName"]+"""["""+x["Capacity"]+"""]</option>"""

			print """</select>
			</td>
			</tr>

			<tr>
			<th align="left">Select Hot Spare Type</th>
			<td>
			<div class="styled-select2">
			<select name="select_hotspare_type" >
			<option value='select-hotspare'>Select Hot Spare Type</option>
			<option value='0'>Global Hot Spare</option>
			<option value='1'>Dedicated to RaidSet</option>
			<option value='2'>Dedicated to Enclosure</option>
			</select>
			</td>
			</tr>


			</table>	

			<table width="600px" style="margin:0px 0 10px 0; border:#D1D1D1 1px solid; padding:0 0 0 10px; background-color:#D1D1D1;">
			</table>

			<table width="600px">
			<tr>
			<td><button class="buttonClass" type = 'submit' name = 'create_hotspare' value = 'create_hotspare' style="float:right;" >Create Hotspare</button></td>
			</tr>
			</table>

			</form>"""
		else:
			print """<div style="text-align:center; margin:10px 0 10px 0; width:600px;">No free disk available!</div>"""

		print """</div>
		</div>
		</div>
		<!--form container ends here-->
		<p>&nbsp;</p>
		</div>

		
		<div id="tabs-4">
		<!--form container starts here-->
		<div class="form-container">
		<div class="inputwrap">
		<div class="formleftside-content">"""
		if(hs_disks != []):
			print """<form name="delete_hotspare" method="POST" action="iframe_create_raid_set.py#tabs-4" >
			<table width="600px">
			<tr>
			<th style="border:#D1D1D1 1px solid; padding:5px;">Select Hot Spare</th>
			<th style="border:#D1D1D1 1px solid; padding:5px;">Hot Spare</th>
			<th style="border:#D1D1D1 1px solid; padding:5px;">Disk</th>
			<th style="border:#D1D1D1 1px solid; padding:5px;">Size</th>
			</tr>"""
			for disks in hs_disks:
				print """<tr>
				<td align="center" style="border:#D1D1D1 1px solid; padding:5px;"><input type="radio" name="hotspare_id" value='"""+disks["#"]+"""' /></td>
				<td align="center" style="border:#D1D1D1 1px solid; padding:5px;">"""+disks["Usage"]+"""</td>
				<td align="center" style="border:#D1D1D1 1px solid; padding:5px;">"""+disks["ModelName"]+"""</td>
				<td align="center" style="border:#D1D1D1 1px solid; padding:5px;">"""+disks["Capacity"]+"""</td>
				</tr>"""
			print"""</table>	

			<table width="600px" style="margin:0px 0 10px 0; border:#D1D1D1 1px solid; padding:0 0 0 10px; background-color:#D1D1D1;">
			</table>

			<table width="600px">
			<tr>
			<td><button class="buttonClass" type = 'submit' name = 'delete_hotspare' value = 'delete_hotspare' style="float:right;" onclick=" return confirm('Are you sure you want to delete this Hot Spare?');">Delete Hot Spare</button></td>
			</tr>
			</table>

			</form>"""
		else:
			print """<div style="text-align:center; margin:10px 0 10px 0; width:600px;">No Hot Spare available!</div>"""

		print """</div>
		</div>
		</div>
		<!--form container ends here-->
		<p>&nbsp;</p>
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
