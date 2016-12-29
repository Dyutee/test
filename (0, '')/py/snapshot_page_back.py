#!/usr/bin/python
import cgitb, header, os, sys
cgitb.enable()

sys.path.append('../modules/')
import disp_except;
try:
	sys.path.append("/var/nasexe/storage/")
	import snapshot
	import lvm_infos


	#----------------------------------------- Create Snapshot Start ---------------------------------------#
	if(header.form.getvalue("create_snapshot")):
		get_disk_name = header.form.getvalue("disk_name")
		get_size = header.form.getvalue("size")

		create_snap_cmd = snapshot.create_snapshot(disk_name=get_disk_name,size=get_size)
		if(create_snap_cmd == True):
			print "<div id='id_trace'>"
			print "Snapshot created successfully!"
			print "</div>"
		else:
			print "<div id='id_trace_err'>"
			print "Error creating Snapshot!"
			print "</div>"
	#----------------------------------------- Create Snapshot End ---------------------------------------#

	#----------------------------------------- Delete Snapshot Start ---------------------------------------#
	if(header.form.getvalue("delete_snapshot")):
		get_snap_to_delete = header.form.getvalue("hid_snap_name")
		delete_snap_cmd = snapshot.delete_snapshot(snp_name=str("SNP"+get_snap_to_delete).strip())
		if(delete_snap_cmd == True):
			print "<div id='id_trace'>"
			print "Snapshot deleted successfully!"
			print "</div>"
		else:
			print "<div id='id_trace_err'>"
			print "Error deleting Snapshot!"
			print "</div>"
	#----------------------------------------- Delete Snapshot End ---------------------------------------#

	get_snapshots = lvm_infos.get_lvs(type1='SNP')
	get_nas_lvs = lvm_infos.get_lvs()
	get_bio_lvs = lvm_infos.get_lvs(type1='BIO')
	#print get_nas_lvs
	#print "<br/>"
	#print get_bio_lvs
	#print get_snapshots

	import left_nav
	print
	print """

	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer">
		<div class="insidepage-heading">Maintenace >> <span class="content">Snapshot Information</span></div>
		<!--tab srt-->
		<div class="searchresult-container">
		  <div class="infoheader">
		    <div id="tabs">
		      <ul>
			<li><a href="#tabs-1">Create Snapshot</a></li>
			<li><a href="#tabs-2">Show Snapshot</a></li>
		      </ul>

		<div id="tabs-1">
		<!--form container starts here-->
		<form name="create_snap_form" method="post" action="main.py?page=ss#tabs-1" />
		<div class="form-container">
		<div class="inputwrap">
		<div class="formleftside-content">

		<table style="width:500px;">
		<tr>
		<td>Select Disk name</td>
		<!--<td><input type="text" name="disk_name" class = 'textbox' /></td>-->
		<td>
		<div class="styled-select2">
		<select name="disk_name">
		<option>Select a Disk</option>"""
	for n in get_nas_lvs["lvs"]:
		print """<option value='NAS-"""+n['lv_name']+"""'>NAS-"""+n['lv_name']+"""</option>"""

	for b in get_bio_lvs["lvs"]:
		print """<option value='BIO"""+b['lv_name']+"""'>BIO"""+b['lv_name']+"""</option>"""

	print """</select></div>
		</tr>

		<tr>
		<td>Enter Size(GB)</td>
		<td><input type="text" name="size" class = 'textbox' style="width:188px;" /></td>
		</tr>

		<tr>
		<td></td>
		<td>
		<button class = 'button_example' type="submit" name = 'create_snapshot' value = 'create_snapshot' style = 'float:right; margin:20px 180px 20px 0;' onclick="return validate_snapshot_form2();">Create Snapshot</button>
		</td>
		</tr>

		</table>

		</div>
		</div>
		</div>
		<!--form container ends here-->
		<p>&nbsp;</p>
		</form>
		</div>


		<div id="tabs-2">
		<!--form container starts here-->
		<div class="form-container">
		<div class="inputwrap">
		<div class="formleftside-content">"""

	if(get_snapshots["lvs"] != []):
		print """<table style="width:650px; border:#D1D1D1 1px solid; margin:0 0 10px 0;">
		<tr>
		<th align="center" style="border-bottom:#D1D1D1 1px solid; padding:5px;">Snapshot Name</th>
		<th align="center" style="border-bottom:#D1D1D1 1px solid; padding:5px;">Volume Name</th>
		<th align="center" style="border-bottom:#D1D1D1 1px solid; padding:5px;">Disk Name</th>
		<th align="center" style="border-bottom:#D1D1D1 1px solid; padding:5px;">Size</th>
		<th align="center" style="border-bottom:#D1D1D1 1px solid; padding:5px;">Action</th>
		</tr>"""

		for i in get_snapshots["lvs"]:
			print """<tr>
			<td style="" align="center">"""+i["lv_name"]+"""</td>
			<td style="" align="center">"""+i["vg_name"]+"""</td>
			<td style="" align="center">"""+i["disk_n"]+"""</td>
			<td style="" align="center">"""+i["size"]+"""</td>
			<form name="delete_snap_form" method="post" action="main.py?page=ss#tabs-2" />
			<input type="hidden" name="hid_snap_name" value='"""+i["lv_name"]+"""' />
			<td style="" align="center">
			<button type="submit" name="delete_snapshot" value="delete_snapshot" style="background-color:#FFF; border:none; cursor:pointer;" title="Delete Snapshot" onclick=" return confirm('Are you sure you want to delete?');"><img src="../images/delete_snap.png" alt="delete snapshot" /></button>
			</td>
			</form>
			</tr>"""

		print """</table>"""

	else:
		print """<p style="width:650px; text-align:center;">No Snapshot Found!</p>"""

	print """	</div>
		</div>
		</div>
		<!--form container ends here-->
		<p>&nbsp;</p>
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
