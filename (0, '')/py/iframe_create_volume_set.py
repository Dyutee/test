#!/usr/bin/python
import traceback

import sys;
sys.path.append('../modules/');
import disp_except;

try:
	#################################################
        ################ import modules #################
        #################################################
	import cgitb,  os, sys, commands, traceback, common_methods, system_info, time, include_files, cgi
	cgitb.enable()
	sys.path.append("/var/nasexe/python/tools/")
        import raid
	form = cgi.FieldStorage()
        sys.path.append('/var/nasexe/python/')
        import tools
        from tools import db
	from tools import raid_controller
	sys.path.append('/var/nasexe/')
        import storage
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
        ############### Selected RAID Set ##############
        ################################################
	get_selected_raid = ''
	raid_set_info = ''
	member_disks_val = ''
	max_capacity_alwd_val = ''
	if(form.getvalue("select_raid_set")):
		get_selected_raid = form.getvalue("select_raid_set")
		if(get_selected_raid != "select-raid"):
			raid_set_info = raid.get_rsf_info(str(get_selected_raid))
			for key in raid_set_info.keys():
				if "Member Disks" in key:
					member_disks_val = raid_set_info[key].strip()
				if "Total Raw Capacity" in key:
					max_capacity_alwd_val = raid_set_info[key].strip()
					max_capacity_alwd_val = max_capacity_alwd_val.replace("GB", "").strip()
		else:
			print "<div id='id_trace_err'>"
			print "Select a RAID Set!"
			print "</div>"
	#--------------------- END --------------------#

	################################################
        ############### Create Volume Set ##############
        ################################################
	if(form.getvalue("create_volume_set")):
		raid_set_no = form.getvalue("select_raid_set")
		name = form.getvalue("vol_set_name")
		raid_level = form.getvalue("volume_raid_level")
		capacity = form.getvalue("enter_volume_capacity")
		fginit = form.getvalue("volume_ini_mode")
		stripe = form.getvalue("volume_stripe_size")
		cache = form.getvalue("volume_cache_mode")
		tag = form.getvalue("tag_cmd_queuing")
		gt2tb = form.getvalue("g2tbvs")

		if(capacity != None):

			if(name == None):
				name = ''
			
			if(fginit == "False"):
				fginit = False
			else:
				fginit = True

			if(cache == "False"):
				cache = False
			else:
				cache = True

			if(tag == "False"):
				tag = False
			else:
				tag = True
			
			if(gt2tb == None):
				gt2tb = ''

			create_vol_set_cmd = raid.create_volset(ctrl_passwd='0000',raid_set_no=str(raid_set_no),raid_level=str(raid_level),capacity=str(capacity),rchannel=0,name=name,gt2tb=str(gt2tb),fginit=fginit,stripe=int(stripe),cache=cache,tag=tag,debug=False)
			if(create_vol_set_cmd == True):
				print "<div id='id_trace'>"
				print "Successfully created Volume Set!"
				print "</div>"
				time.sleep(2)
			else:
				print "<div id='id_trace_err'>"
				print "Error creating Volume Set!"
				print "</div>"
		else:
			print "<div id='id_trace_err'>"
                        print "Enter Volume Capacity!"
                        print "</div>"
	#--------------------- END --------------------#

	################################################
        ############### Delete Volume Set ##############
        ################################################
	if(form.getvalue("delete_raid_set")):
		get_indexes = form.getvalue("vol_set_to_del")
		if(get_indexes != None):
			delete_vol_set_cmd = raid.delete_volset('0000',get_indexes)
			if(delete_vol_set_cmd == True):
				print "<div id='id_trace'>"
				print "Successfully deteled Volume Set!"
				print "</div>"
			else:
				print "<div id='id_trace_err'>"
				print "Error deleting Volume Set!"
				print "</div>"
		else:
			print "<div id='id_trace_err'>"
			print "Select Volume Set to delete!"
			print "</div>"
	#--------------------- END --------------------#

	#--- Get all Volume Set
	vol_sets = raid.get_all_vsf_info()
	#--- Get all RAID Set
	raid_sets = raid.get_all_rsf_info()


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
		<td class="text_css">This page lets you create and delete RAID volume sets.</td>
		</tr>
		</table>"""
		if(check_ha == True):
			print"""
			 </span></a><span class = "gap_text" style="color:#fff;margin-left:7px;">Raid Information ("""+show_tn+""")</span>
			<span style="float:right; margin:0 0px 0 0;"><a onclick="return onclick_loader();" class="resource_links" href="https://"""+other_node_ip+"""/fs4/py/iframe_create_volume_set.py">"""+show_on+"""</a></span>

			</div>"""
		else:
			print """ </span></a>Raid Information</div>"""
		print"""

			  <div class="infoheader">
			    <div id="tabs">
			      <ul>
				<li><a href="#tabs-1">Create Volume Set</a></li>
				<li><a href="#tabs-2">Delete Volume Set</a></li>
			      </ul>

		<div id="tabs-1">
		<!--form container starts here-->
		<div class="form-container">
		<div class="inputwrap">
		<div class="formleftside-content">

		<form name="create_volume_set" method="post" action=""> 
		<table width="600px">
		<tr>
		<th align="left">Select RAID Set</th>
		<td>

		<div class="styled-select2">
		<select name="select_raid_set" onchange="this.form.submit();">
		<option value='select-raid'>Select RAID Set</option>"""
		for r in raid_sets:
			if(r["Name"] != "PassThroughDisk"):
				if not any(d.get('RaidName', None) == r["Name"] for d in vol_sets):
					print """<option value='"""+r["#"]+"""'"""
					if(get_selected_raid == r["#"]):
						print "selected"
					print """>"""+r["Name"]+"""</option>"""

		print """</select>
		</div>

		</td>
		</tr>"""

		if(raid_set_info != ''):
			print """<tr>
			<th align="left">Member Disks</th>
			<td><input class="textbox" type="text" name="member_disks" style="width:187px;" value='"""+member_disks_val+"""' readonly /></td>
			</tr>

			<tr>
			<th align="left">Volume RAID Level</th>
			<td>

			<div class="styled-select2">
			<select name="volume_raid_level">
			<option value="0">RAID 0</option>
			<option value="1">RAID 1+0</option>
			<option value="5">RAID 5</option>
			<option value="6">RAID 6</option>
			</select>
			</div>

			</td>
			</tr>

			<tr>
			<th align="left">Volume Set Name</th>
			<td><input class="textbox" type="text" name="vol_set_name" style="width:187px;" /></td>
			</tr>

			<tr>
			<th align="left">Max Capacity Allowed</th>
			<td><input class="textbox" type="text" name="max_capacity_allowed" style="width:187px;" value='"""+max_capacity_alwd_val+"""' readonly /> GB</td>
			</tr>

			<tr>
			<th align="left">Enter Volume Capacity</th>
			<td><input class="textbox" type="text" name="enter_volume_capacity" style="width:187px;" value='"""+max_capacity_alwd_val+"""' /> GB</td>
			</tr>

			<tr>
			<th align="left">Volume Initialization Mode</th>
			<td>

			<div class="styled-select2">
			<select name="volume_ini_mode">
			<option value="False">Background Initialization</option>
			</select>
			</div>

			</td>
			</tr>

			<tr>
			<th align="left">Volume Stripe Size</th>
			<td>

			<div class="styled-select2">
			<select name="volume_stripe_size">
			<option value="4">4</option>
			<option value="8">8</option>
			<option value="16">16</option>
			<option value="32">32</option>
			<option value="64" selected >64</option>
			<option value="128">128</option>
			</select>
			</div>

			</td>
			</tr>

			<tr>
			<th align="left">Volume Cache Mode</th>
			<td>

			<div class="styled-select2">
			<select name="volume_cache_mode">
			<option value="True">Write Back</option>
			<option value="False" selected>Write Through</option>
			</select>
			</div>

			</td>
			</tr>

			<tr>
			<th align="left">Tagged Command Queuing</th>
			<td>

			<div class="styled-select2">
			<select name="tag_cmd_queuing">
			<option value="True" selected>Enabled</option>
			<option value="False">Disabled</option>
			</select>
			</div>

			</td>
			</tr>

			<!--<tr>
			<th align="left">SCSI channel:SCSI id:SCSI lun</th>
			<td>

			<div class="styled-select2" style="width:42px; float:left;">
			<select name="scsi_channel">
			<option>0</option>
			</select>
			</div>

			<div class="styled-select2" style="width:50px; float:left;">
			<select name="volume_raid_level">
			<option>00</option>
			<option>01</option>
			<option>02</option>
			<option>03</option>
			<option>04</option>
			<option>05</option>
			<option>06</option>
			<option>07</option>
			<option>08</option>
			<option>09</option>
			<option>10</option>
			<option>11</option>
			<option>12</option>
			<option>13</option>
			<option>14</option>
			<option>15</option>
			</select>
			</div>

			<div class="styled-select2" style="width:50px; float:left;">
			<select name="volume_raid_level">
			<option>02</option>
			<option>03</option>
			<option>04</option>
			<option>05</option>
			<option>06</option>
			<option>07</option>
			</select>
			</div>

			</td>
			</tr>-->

			<tr>
			<th align="left">Greater 2 TB Volume Support</th>
			<td>

			<div class="styled-select2">
			<select name="g2tbvs">
			<option value="64BIT" selected>64 bit LBA</option>
			<option value="WIN">4K Block</option>
			<option value="">No</option>
			</select>
			</div>

			</td>
			</tr>"""

		print """</table>"""

		if(raid_set_info != ''):
			print """<table width="600px">
			<tr>
			<td><button class="buttonClass" type = 'submit' name = 'create_volume_set' value = 'create_volume_set' style="float:right; margin:20px 120px 20px 0;" >Create</button></td>
			</tr>
			</table>"""

		print """</form>

		</div>
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

		<form name="delete_volume_set_form" method="post" action="">
		<table width="600px">
		<tr>
		<th style="border:#D1D1D1 1px solid; padding:5px;">Select Volume Set</th>
		<th style="border:#D1D1D1 1px solid; padding:5px;">Volume Set</th>
		<th style="border:#D1D1D1 1px solid; padding:5px;">RAID Set</th>
		<th style="border:#D1D1D1 1px solid; padding:5px;">RAID Level</th>
		<th style="border:#D1D1D1 1px solid; padding:5px;">Size</th>
		<th style="border:#D1D1D1 1px solid; padding:5px;">State</th>
		</tr>"""

		for x in vol_sets:
			print """<tr>
			<td align="center" style="border:#D1D1D1 1px solid; padding:5px;"><input type="radio" name="vol_set_to_del" value='"""+x["#"]+"""' /></td>
			<td align="center" style="border:#D1D1D1 1px solid; padding:5px;">"""+x["Name"]+"""</td>
			<td align="center" style="border:#D1D1D1 1px solid; padding:5px;">"""+x["RaidName"]+"""</td>
			<td align="center" style="border:#D1D1D1 1px solid; padding:5px;">"""+x["Level"]+"""</td>
			<td align="center" style="border:#D1D1D1 1px solid; padding:5px;">"""+x["Capacity"]+"""</td>
			<td align="center" style="border:#D1D1D1 1px solid; padding:5px;">"""+x["State"]+"""</td>
			</tr>"""

		print """</table>	

		<table width="600px">
		<tr>
		<td><button class="buttonClass" type = 'submit' name = 'delete_raid_set' value = 'delete_raid_set' style="float:right;" >Delete</button></td>
		</tr>
		</table>
		</form>


		</div>
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
