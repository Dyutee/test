#!/usr/bin/python
import cgitb, header, os, sys, commands
cgitb.enable()

sys.path.append('../modules/')
import disp_except;
try:
	#if(header.form.getvalue("action")):
	#	if(header.form.getvalue("action") == 'snap_value'):
			
	#		print"""<div id = 'id_trace'>"""
        #        	print "Successfully Schedule the Snapshot!"
        #        	print "</div>"
        #	else:
        #        	print"""<div id = 'id_trace_err'>"""
        #        	print "Error occured while Scheduling Snapshot!"
        #        	print "</div>"
	#		print 'OUTPUT:'+str(New_val)

	
		
	sys.path.append("/var/nasexe/storage/")
	import snapshot
	import lvm_infos
	
	#------------------Snapshot time Import-------------
	sys.path.append('/var/nasexe/python/')
	import smb, commons
	
	from tools import sync
	snap_time=sync.get_time()
	#------------------------End------------------------
	
	#-------------Volume Size--------------------------------
	sys.path.append('/var/nasexe/storage/')
        import storage_op
        from lvm_infos import *
        from functions import *
	vg_info = get_vgs()
	for free_vg in vg_info["vgs"]:
		free_vg = free_vg["free_size"]
	#-----------------------End--------------------------
	#-------------------Snapshot Import-----------------
	sys.path.append('/var/nasexe/python/tools')
	import snapshotschedule
	#-----------------------End--------------------

	#----------------------------------------- Schedule Snapshot Start ---------------------------------------#
	if(header.form.getvalue("sche_snapshot")):
		get_snap_name = header.form.getvalue("snap_name")
		get_disk_name = header.form.getvalue("disk_name")
		get_max_snap = header.form.getvalue("max_snap")
		get_snap_size = header.form.getvalue("snap_size")
		get_snap_add_size = str(get_snap_size)+'G'
		#filetowrite = "/var/nasexe/python/launcher_scripts/usr/snap_rotate_"+get_disk_name+"_"+snap_time
		filetowrite = "/tmp/snap_rotate_"+get_disk_name+"_"+snap_time
		file_cont = []
		file_cont.append("#!/usr/bin/python")
		file_cont.append("import sys")
		file_cont.append("sys.path.append('/var/nasexe/python/tools')")
		file_cont.append("import snapshotschedule")
		#file_cont.append('TRIGGER='"SCHEDULE SNAPSHOT FOR "+str(get_disk_name))
		file_cont.append("TRIGGER='SCHEDULE SNAPSHOT FOR " + str(get_disk_name) + "'")
		file_cont.append('ACTION1='"'LOG'")
		file_cont.append('ACTION2='"''")
		file_cont.append("diskname=""'"+str(get_disk_name)+"'")
		file_cont.append("max_snaps="+str(get_max_snap))
		file_cont.append("snap_size=""'"+str(get_snap_add_size)+"'")
		file_cont.append("snap_name=""'"+str(get_snap_name)+"'")
		file_cont.append("status=snapshotschedule.rotate(diskname,max_snaps,snap_size,snap_name)")
		commons.write_file(filetowrite, file_cont)
		#print file_cont
		move_cmd = commands.getstatusoutput("sudo mv /tmp/snap_rotate_"+get_disk_name+"_"+snap_time+" /var/nasexe/python/launcher_scripts/usr/");
		#sched_status=snapshotschedule.rotate(get_disk_name,get_max_snap,get_snap_add_size)
		#if(sched_status == True):
		#	print""" <div id = 'id_trace' >"""
		#	print "Successfully Scheduled the Snapshot!"
		#	print "</div>"
			#logstatus = common_methods.sendtologs('Success', 'Successfuly Schduled', 'snapshot_schedule.py', str(sched_status));
		#else:
		#	print""" <div id = 'id_trace_err' >"""

		#	print "Error Occurred while Scheduling the Snapshot"
		#	print "</div>"
		#print sched_status

	#----------------------------------------- Schedule Snapshot End ---------------------------------------#



	get_snapshots = lvm_infos.get_lvs(type1='SNP')
	get_nas_lvs = lvm_infos.get_lvs()
	get_bio_lvs = lvm_infos.get_lvs(type1='BIO')
	array_len = len(get_snapshots["lvs"])	
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
			<li><a href="#tabs-1">Snapshot</a></li>
			<li><a href="#tabs-2">Schedule</a></li>
		      </ul>

		<div id="tabs-1">
		<!--form container starts here-->
		<form name="sche_snap_form" method="post" action="" />
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
		<option value = 'disk_val'>Select a Disk</option>"""
	for n in get_nas_lvs["lvs"]:
		print """<option value='NAS-"""+n['lv_name']+"""'>NAS-"""+n['lv_name']+"""</option>"""

	for b in get_bio_lvs["lvs"]:
		print """<option value='BIO"""+b['lv_name']+"""'>BIO"""+b['lv_name']+"""</option>"""

	print """</select></div>
		</tr>
		
		 <tr>
                <td>Snap Name</td>
                <td><input type="text" name="snap_name" class = 'textbox' value = "" style="width:188px;" /></td>
                </tr>

		<tr>
		<td>Max Snaps</td>
		<td><input type="text" name="max_snap" onkeypress="return isNumberKey(event)" class = 'textbox' value = "" style="width:188px;" /></td>
		</tr>
		<tr>
		<td>Snap Size(GB)</td>
		<td><input type="text" name="snap_size"  value = "" onkeypress="return isNumberKey(event)" class = 'textbox' style="width:188px;" /></td>
		<input type ="hidden" name = "free_vol" value = '"""+free_vg+"""'>
		</tr>


		<tr>
		<td></td>
		<td>
		<button class = 'button_example' type="submit" name = 'sche_snapshot' value = 'schedule_snapshot' style = 'float:right; margin:20px 180px 20px 0;' onclick="return validate_snapshot_schedule();">Snapshot</button>
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
	import snap_nw_page1


	print"""		 </div>
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
