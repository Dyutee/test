#!/usr/bin/python
import traceback

import sys;
sys.path.append('../modules/');
import disp_except;

try:
	import cgitb, header, os, sys, commands, traceback, common_methods, system_info
	cgitb.enable()

	sys.path.append("/var/nasexe/python/tools/")
	import raid

	import datetime
	now = datetime.datetime.now()

	import time

	if(header.form.getvalue("create_raid_set")):
		get_indexes = header.form.getvalue("volume_array[]")
		get_raid_name = header.form.getvalue("raid_set_name")
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
			print "Select a Raidset!"
			print "</div>"

	if(header.form.getvalue("delete_raid_set")):
		get_indexes = header.form.getvalue("volume_array2")
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
					print "Error deleted RAID Set!"
					print "</div>"
		else:
			print "<div id='id_trace_err'>"
			print "Select a Raidset!"
			print "</div>"

	free_disks = raid.get_free_disks()
	raid_sets = raid.get_all_rsf_info()

	import left_nav
	print
	print """

	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer">
		<div class="insidepage-heading">Raid Configuration >> <span class="content">Create/Delete RAID Set</span></div>
		<!--tab srt-->
		<div class="searchresult-container">
		  <div class="infoheader">
		    <div id="tabs">
		      <ul>
			<li><a href="#tabs-1">Create RAID Set</a></li>
			<li><a href="#tabs-2">Delete RAID Set</a></li>
		      </ul>

	<div id="tabs-1">
	<!--form container starts here-->
	<div class="form-container">
	<div class="inputwrap">
	<div class="formleftside-content">"""
	if(free_disks != []):
		print """<form name="add_volume" method="POST" action="" >
		<table width="600px">
		<tr>
		<th style="border:#D1D1D1 1px solid; padding:5px;"><input type = 'checkbox' name='select_all_free_disks' id = 'id_select_free_disks' title = 'Check this to select all' onclick = 'return select_all_disks();'></th>
		<th style="border:#D1D1D1 1px solid; padding:5px;">Disk</th>
		<th style="border:#D1D1D1 1px solid; padding:5px;">Size</th>
		</tr>"""

		for x in free_disks:
			print """<tr>
			<td align="center" style="border:#D1D1D1 1px solid; padding:5px;"><input type = 'checkbox' name = 'volume_array[]' id = 'id_volume_array' value='"""+x["#"]+"""'></td>
			<td align="center" style="border:#D1D1D1 1px solid; padding:5px;">"""+x["Enc#"]+' '+x["Slot#"]+' '+x["ModelName"]+"""</td>
			<td align="center" style="border:#D1D1D1 1px solid; padding:5px;">"""+x["Capacity"]+"""</td>
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
		<td><button class="button_example" type = 'submit' name = 'create_raid_set' value = 'create_raid_set' style="float:right;" >Create Raid set</button></td>
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

	<form name="delete_raid_set_form" method="post" action="">
	<table width="600px">
	<tr>
	<th style="border:#D1D1D1 1px solid; padding:5px;">Select RAID Set</th>
	<th style="border:#D1D1D1 1px solid; padding:5px;">RAID set</th>
	<th style="border:#D1D1D1 1px solid; padding:5px;">No. of Disks</th>
	<th style="border:#D1D1D1 1px solid; padding:5px;">Size</th>
	<th style="border:#D1D1D1 1px solid; padding:5px;">State</th>
	</tr>"""

	for r in raid_sets:
		print """<tr>
		<td align="center" style="border:#D1D1D1 1px solid; padding:5px;"><input type = 'radio' name = 'volume_array2' id = 'id_volume_array2' value='"""+r["#"]+"""'></td>
		<td align="center" style="border:#D1D1D1 1px solid; padding:5px;">"""+r["Name"]+"""</td>
		<td align="center" style="border:#D1D1D1 1px solid; padding:5px;">"""+r["Disks"]+"""</td>
		<td align="center" style="border:#D1D1D1 1px solid; padding:5px;">"""+r["TotalCap"]+"""</td>
		<td align="center" style="border:#D1D1D1 1px solid; padding:5px;">"""+r["State"]+"""</td>
		</tr>"""

	print """</table>	

	<table width="600px">
	<tr>
	<td><button class="button_example" type = 'submit' name = 'delete_raid_set' value = 'delete_raid_set' style="float:right;" >Delete Raid set</button></td>
	</tr>
	</table>
	</form>

	</div>
	</div>
	</div>
	<!--form container ends here-->
	<p>&nbsp;</p>
	</div>

		
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
