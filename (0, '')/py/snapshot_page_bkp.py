#!/usr/bin/python
import cgitb, header, os, sys
cgitb.enable()

sys.path.append('../modules/')
import disp_except;
try:
	sys.path.append("/var/nasexe/storage/")
	import snapshot
	import lvm_infos

	sys.path.append('/var/nasexe/python/')
	import smb
	import nfs
	import tools
	import snapshotschedule
	disk_name_list = ''
	display_list = 'none'
	disk_list_status = ''
	display_blank = 'block'
	#------------------Snapshot Schedule output Message From Tabs-3--------------------
	if(header.form.getvalue("action")):
               if(header.form.getvalue("action") == 'snap_value'):

                       print"""<div id = 'id_trace'>"""
                       print "Successfully Schedule the Snapshot!"
                       print "</div>"
               else:
                       print"""<div id = 'id_trace_err'>"""
                       print "Error occured while Scheduling Snapshot!"
                       print "</div>"
	


	#------------------------End------------------------------------------

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
		check_snap_mounted = snapshot.test_mount("SNP"+get_snap_to_delete)
		if(check_snap_mounted == True):
			unmount_snap = snapshot.umount_snap("SNP"+get_snap_to_delete)
			if(unmount_snap == True):
				delete_snap_cmd = snapshot.delete_snapshot(snp_name=str("SNP"+get_snap_to_delete).strip())
				if(delete_snap_cmd == True):
					print "<div id='id_trace'>"
					print "Snapshot deleted successfully!"
					print "</div>"
				else:
					print "<div id='id_trace_err'>"
					print "Error deleting Snapshot!"
					print "</div>"
			else:
				print "<div id='id_trace_err'>"
				print "ERROR: Unable to unmount!"
				print "</div>"

		else:
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

	#----------------------------------------- Share as SMB Start ----------------------------------------#
	if(header.form.getvalue("share_as_smb")):
		get_snap = header.form.getvalue("hid_snap_name")
		sn = "SNP"+get_snap
		check_snap_mounted = snapshot.test_mount(sn)
		if(check_snap_mounted == False):
			mount_snap = snapshot.mount_snap(sn)
		else:
			mount_snap = True
	
		if(mount_snap == True):
			path = "/storage/snapshots/"+str(get_snap)
			smb_dict = {'comment': '', 'audit_opts': '', 'browsable': 'yes', 'recycle_enable': 'no', 'use_smb': 'yes', 'writable': 'no', 'recycle_repo': '', 'guest_ok': 'yes', 'path': path, 'file_perm': '0555', 'name': get_snap, 'dir_perm': '0555', 'valid_users': '', 'audit_enable': 'no', 'public': 'yes'}
			configure_smb = smb.configure(smb_dict)
			if(configure_smb["id"] == 0):
				print "<div id='id_trace'>"
				print configure_smb["desc"]
				print "</div>"
			else:
				print "<div id='id_trace_err'>"
                                print configure_smb["desc"]
                                print "</div>"
		else:
			print "<div id='id_trace_err'>"
			print "ERROR: Unable to mount snapshot!"
			print "</div>"
	#----------------------------------------- Share as SMB End ----------------------------------------#

	#----------------------------------------- Share as NFS Start --------------------------------------#
	if(header.form.getvalue("share_as_nfs")):
		get_snap = header.form.getvalue("hid_snap_name")
                sn = "SNP"+get_snap
                check_snap_mounted = snapshot.test_mount(sn)
                if(check_snap_mounted == False):
                        mount_snap = snapshot.mount_snap(sn)
                else:
                        mount_snap = True

                if(mount_snap == True):
                        path = "/storage/snapshots/"+str(get_snap)
			nfs_dict = {'share_path': path, 'share_desc': '', 'share_name': get_snap, 'insecure': 'on', 'use_nfs': 'on', 'sync': 'off', 'read_ips': '*', 'additional_nfs_parameters': '', 'write_ips': '', 'no_root_squash': 'off', 'insecure_locks': 'off'}
			#print nfs_dict
			configure_nfs = nfs.configure(nfs_dict)
			if(configure_nfs["id"] == 0):
                                print "<div id='id_trace'>"
                                print configure_nfs["desc"]
                                print "</div>"
                        else:
                                print "<div id='id_trace_err'>"
                                print configure_nfs["desc"]
                                print "</div>"
		else:
			print "<div id='id_trace_err'>"
			print "ERROR: Unable to mount snapshot!"
			print "</div>"
	#----------------------------------------- Share as NFS End --------------------------------------#

	#------------------------------------- Unconfigure SMB Start -------------------------------------#
	if(header.form.getvalue("unconf_smb")):
		get_snap = header.form.getvalue("hid_snap_name")
		unconf_cmd = smb.unconfigure(get_snap,debug=False)
		if(unconf_cmd["id"] == 0):
			#tools.delete_entry_from_file('^' + get_snap + ':', 'shares_global_file', '/var/www/global_files/')
                        print "<div id='id_trace'>"
                        print unconf_cmd["desc"]
                        print "</div>"
                else:
                        print "<div id='id_trace_err'>"
                        print unconf_cmd["desc"]
                        print "</div>"
	#------------------------------------- Unconfigure SMB End -------------------------------------#

	#------------------------------------- Unconfigure NFS Start -------------------------------------#
	if(header.form.getvalue("unconf_nfs")):
		get_snap = header.form.getvalue("hid_snap_name")
		path = "/storage/snapshots/"+str(get_snap)
		unconf_cmd = nfs.unconfigure(path)
		if(unconf_cmd["id"] == 0):
			print "<div id='id_trace'>"
			print unconf_cmd["desc"]
			print "</div>"
		else:
			print "<div id='id_trace_err'>"
			print unconf_cmd["desc"]
			print "</div>"
	#------------------------------------- Unconfigure NFS End -------------------------------------#



		


	get_snapshots = lvm_infos.get_lvs(type1='SNP')
	get_nas_lvs = lvm_infos.get_lvs()
	get_bio_lvs = lvm_infos.get_lvs(type1='BIO')
	array_len = len(get_snapshots["lvs"])	
	#print get_nas_lvs
	#print "<br/>"
	#print get_bio_lvs
	#print get_snapshots


	#---------------------Schedule List--------------------------
	if(header.form.getvalue("disk_list")):
		disk_name_list = header.form.getvalue("disk_list")
		print 'NAME:'+str(disk_name_list)
		
		disk_list_status=snapshotschedule.get(disk_name_list,debug=True)
		display_blank = 'none'
		display_list = 'block'
		display_list1 = 'block'
		print "<script>location.href = 'main.py?page=ss#tabs-4';</script>"
		print disk_list_status

	#--------------End-----------------------------

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
			<li><a href="#tabs-3">Snapshot Schedule</a></li>
			<li><a href="#tabs-4">Schedule List</a></li>
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

		print """<nav id="menu_snap">

		<ul>"""

		i=1
		s=1
		for x in get_snapshots["lvs"]:
			is_smb_configured = smb.is_configured(x["lv_name"],debug=False)
			is_nfs_configured = nfs.is_configured("/storage/snapshots/"+x["lv_name"])

			print """
			<style>
			#proppopUpDiv"""+str(i)+""" {position: fixed; background-color: #fff; width: 500px; z-index: 9002; padding: 5px;}
			#proppopUpDiv"""+str(i)+""" h5{width:100%; font-size:15px; color:#0070bd; text-align:center; font-weight:bold;}
			#proppopUpDiv"""+str(i)+""" span{ color:#FFFFFF; background-color:#0070bd; padding:1px 3px 0 3px; float:right;}
			#proppopUpDiv"""+str(i)+""" ul.idTabs{list-style:none; border:none; width:400px; margin:5px 0 0 0;}
			#proppopUpDiv"""+str(i)+""" ul.idTabs li{display:inline;}
			#proppopUpDiv"""+str(i)+""" ul.idTabs li a.link_tabs{display:inline; border:none; background-color:#D1D1D1; padding:10px;}
			#proppopUpDiv"""+str(i)+""" ul.idTabs li a.link_tabs:hover{background-color:#cfbdbd;}
			
			#proppopUpDiv2"""+str(i)+""" {position: fixed; background-color: #fff; width: 500px; z-index: 9002; padding: 5px;}
			#proppopUpDiv2"""+str(i)+""" h5{width:100%; font-size:15px; color:#0070bd; text-align:center; font-weight:bold;}
			#proppopUpDiv2"""+str(i)+""" span{ color:#FFFFFF; background-color:#0070bd; padding:1px 3px 0 3px; float:right;}
			#proppopUpDiv2"""+str(i)+""" ul.idTabs{list-style:none; border:none; width:400px; margin:5px 0 0 0;}
			#proppopUpDiv2"""+str(i)+""" ul.idTabs li{display:inline;}
			#proppopUpDiv2"""+str(i)+""" ul.idTabs li a.link_tabs{display:inline; border:none; background-color:#D1D1D1; padding:10px;}
			#proppopUpDiv2"""+str(i)+""" ul.idTabs li a.link_tabs:hover{background-color:#cfbdbd;}
			
			</style>

			<div style="display: none;" id="blanket"></div>
			<form name="delete_snap_form" method="post" action="main.py?page=ss#tabs-2">
			<div style="display: none;" id='proppopUpDiv2"""+str(i)+"""'>
			<h5>Delete """+x['lv_name']+"""<span onclick="popup('proppopUpDiv2"""+str(i)+"""')" style="cursor:pointer;">X</span></h5>
			<div style="border:#D1D1D1 1px solid; text-align:center; height:70px; margin:20px 0 20px 0;">"""
			if((is_smb_configured == True) or (is_nfs_configured == True)):
				print """Cannot delete because the snapshot is busy!<br/><br/>
				<button class="button_example" type="button" name = 'local_action_but'  id = 'local_action_but' value = 'Update' style="float:right; margin:0px 200px 0 0; " onclick="popup('proppopUpDiv2"""+str(i)+"""')" >Go Back</button>"""
			else:
				print """Are you sure you want to delete """+x['lv_name']+""" ?<br/><br/>
				<input type="hidden" name="hid_snap_name" value='"""+x['lv_name']+"""' />
				<button class="button_example" type="button" name = 'local_action_but'  id = 'local_action_but' value = 'Update' style="float:right; margin:0px 200px 0 0; " onclick="popup('proppopUpDiv2"""+str(i)+"""')" >No</button>
				<button class="button_example" type="submit" name = 'delete_snapshot'  id = 'delete_snapshot' value = 'delete_snapshot' style="float:right; " >Yes</button>"""

			print """</div>
			</form>

			</div>"""

			print """

			<div style="display: none;" id='proppopUpDiv"""+str(i)+"""'>
			<h5>Information of """+x['lv_name']+"""<span onclick="popup('proppopUpDiv"""+str(i)+"""')" style="cursor:pointer;">X</span></h5>
		
			<table style="margin:20px 0 20px 130px; width:300px;">
			<tr>
			<th align="left">Snapshot Name</th>
			<td>"""+x["lv_name"]+"""</td>
			</tr>

			<tr>
			<th align="left">Volume Name</th>
			<td>"""+x["vg_name"]+"""</td>
			</tr>

			<tr>
			<th align="left">Disk Name</th>
			<td>"""+x["disk_n"]+"""</td>
			</tr>

			<tr>
			<th align="left">Size (GB)</th>
			<td>"""+x["size"]+"""</td>
			</tr>

			</table>


			</div>"""


			print """<li onclick="return folder_click("""+str(i)+""", """+str(array_len)+""", """+str(s)+""");"><a>"""+x['lv_name']+"""</a>

			<div id='"""+str(i)+"""' style="display:none;">
			<ul>
			
			<form name="smb_or_nfs" method="post" action="main.py?page=ss#tabs-2">
			<input type="hidden" name="hid_snap_name" value='"""+x['lv_name']+"""' />"""
			if(is_smb_configured == False):
				print """<li><button type="submit" name="share_as_smb" value="share_as_smb" style="border:none; background-color:#FFF; cursor:pointer; margin:0 0 0 7px;"><a>Share as SMB</a></button></li>"""
			else:
				print """<li><button type="submit" name="unconf_smb" value="unconf_smb" style="border:none; background-color:#FFF; cursor:pointer; margin:0 0 0 7px;"><a>Unconfigure SMB</a></button></li>"""
		
			if(is_nfs_configured == False):	
				print """<li><button type="submit" name="share_as_nfs" value="share_as_nfs" style="border:none; background-color:#FFF; cursor:pointer; margin:0 0 0 7px;"><a>Share as NFS</a></button></li>"""
			else:
				print """<li><button type="submit" name="unconf_nfs" value="unconf_nfs" style="border:none; background-color:#FFF; cursor:pointer; margin:0 0 0 7px;"><a>Unconfigure NFS</a></button></li>"""

			print """<li><a onclick="popup('proppopUpDiv"""+str(i)+"""')" href="#">Information</a></li>
			<li><a onclick="popup('proppopUpDiv2"""+str(i)+"""')" href="#">Delete</a></li>
			</form>
			</ul>
			</div>

			</li>"""
			i=i+1

		print """


		</ul>

		</nav>


		"""

	else:
		print """<div style="text-align:center; width:600px;">No Snapshot Found!</div>"""



	print """	</div>
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
	import snap_nw_page1
	print"""	</div>
		 </div>
                </div>
                <!--form container ends here-->
                <p>&nbsp;</p>
                </div>

		<div id="tabs-4">
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
                <select name="disk_list" onchange='this.form.submit()'>
                <option>Select a Disk</option>"""
        for n in get_nas_lvs["lvs"]:
                print """<option value='NAS-"""+n['lv_name']+"""'"""

		if(disk_name_list !=''):
			if(disk_name_list == 'NAS-"""'+n['lv_name']+'"""'):
				print"""selected ='selected'"""


		print""">NAS-"""+n['lv_name']+"""</option>"""

        for b in get_bio_lvs["lvs"]:
                print """<option value='BIO"""+b['lv_name']+"""'"""
		if(disk_name_list !=''):
			if(disk_name_list == 'BIO-"""'+b['lv_name']+'"""'):
				print """selected = 'selected'"""

		print""">BIO"""+b['lv_name']+"""</option>"""

        print """</select></div>
                </tr>
		</table>

		<table width = "680" >
                <tr>
                <th style="border:#D1D1D1 1px solid;">Disk Name</th>
                <th style="border:#D1D1D1 1px solid;">File Name</th>
                <th style="border:#D1D1D1 1px solid;">Snap Name</th>
                <th style="border:#D1D1D1 1px solid;">Snap Size</th>
                <th style="border:#D1D1D1 1px solid;">Max Snap</th>
                </tr>
		"""
		
	if(disk_list_status !=[]):
		for snap_info in disk_list_status:
			print"""
			<tr>
			<th style='border:#D1D1D1 1px solid;display:"""+display_list+""";'>"""+snap_info['diskname']+"""</th>
			
			<th style='border:#D1D1D1 1px solid;display:"""+display_list1+""";'></th>
			<th style='border:#D1D1D1 1px solid;display:"""+display_list1+""";'>"""+snap_info['snap_name']+"""</th>
			<th style='border:#D1D1D1 1px solid;display:"""+display_list1+""";'>"""+snap_info['snap_name']+"""</th>
			<th style='border:#D1D1D1 1px solid;display:"""+display_list1+""";'>"""+snap_info['snap_name']+"""</th>
			</tr>"""
	else:
		print"""<tr>
                <th style="border:#D1D1D1 1px solid;">Select the Disk to get the Information</th>
                </tr>"""
		
	print"""		</table>
		

		 </div>
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
