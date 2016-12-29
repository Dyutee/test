#!/usr/bin/python
import cgitb, os, sys, cgi, include_files
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
	from tools import db
	import snapshotschedule
	form = cgi.FieldStorage()

	check_ha = tools.check_ha()

	querystring = os.environ['QUERY_STRING'];
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

	disk_name_list = ''
	display_list = 'none'
	disk_list_status = ''
	disk_remove_status = ''
	display_blank = 'block'
	
	#------------------Snapshot Schedule output Message From Tabs-3--------------------
	if(form.getvalue("action")):
               if(form.getvalue("action") == 'snap_value'):
                       print"""<div id = 'id_trace'>"""
                       print "Successfully Schedule the Snapshot!"
                       print "</div>"
               else:
                       print"""<div id = 'id_trace_err'>"""
                       print "Error occured while Scheduling Snapshot!"
                       print "</div>"
	

	#------------------------End------------------------------------------
	#------------------Remove Snapshot Schedule output Message From Tabs-3--------------------
        if(form.getvalue("rem_action")):
               if(form.getvalue("rem_action") == 'rem_value'):

                       print"""<div id = 'id_trace'>"""
                       print "Successfully Remove the Scheduled Snapshot!"
                       print "</div>"
               else:
                       print"""<div id = 'id_trace_err'>"""
                       print "Error occured while Removing Scheduled Snapshot!"
                       print "</div>"



        #------------------------End------------------------------------------

	#----------------------------------------- Create Snapshot Start ---------------------------------------#
	if(form.getvalue("create_snapshot")):
		get_disk_name = form.getvalue("disk_name")
		get_size = form.getvalue("size")
		get_size = get_size+"G"

		create_snap_cmd = snapshot.create_snapshot(disk_name=get_disk_name,size=get_size)
		if(create_snap_cmd == True):
			print "<div id='id_trace'>"
			print "Snapshot created successfully!"
			print "</div>"
		else:
			print "<div id='id_trace_err'>"
			print "Error creating Snapshot!"
			print "</div>"
		
	       #print "<script>location.href = 'iframe_snapshot_page.py#tabs-1';</script>"
	#----------------------------------------- Create Snapshot End ---------------------------------------#

	#----------------------------------------- Delete Snapshot Start ---------------------------------------#
	if(form.getvalue("delete_snapshot")):
		get_snap_to_delete = form.getvalue("hid_snap_name")
		check_snap_mounted = snapshot.test_mount("SNP"+get_snap_to_delete)
		if(check_snap_mounted == True):
			unmount_snap = snapshot.umount_snap("SNP"+get_snap_to_delete)
			if(unmount_snap == True):
				delete_snap_cmd = snapshot.delete_snapshot(snp_name=str("SNP"+get_snap_to_delete).strip())
				#print delete_snap_cmd
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
	if(form.getvalue("share_as_smb")):
		get_snap = form.getvalue("hid_snap_name")
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
	if(form.getvalue("share_as_nfs")):
		get_snap = form.getvalue("hid_snap_name")
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
	if(form.getvalue("unconf_smb")):
		get_snap = form.getvalue("hid_snap_name")
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
	if(form.getvalue("unconf_nfs")):
		get_snap = form.getvalue("hid_snap_name")
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
	#for n in get_nas_lvs["lvs"]:
        #	nw_lv =  """NAS-"""+n['lv_name']+""""""
	#	print 'New LV:'+str(nw_lv)
	#---------------------Scheduled snapshot List--------------------------
	if(form.getvalue("disk_list")):
		disk_name_list = form.getvalue("disk_list")
		#print 'NAME:'+str(disk_name_list)
		
		disk_list_status=snapshotschedule.get(disk_name_list,debug=True)
		#print disk_list_status
		display_blank = 'none'
		display_list = 'block'
		display_list1 = 'block'
		print "<script>location.href = 'iframe_snapshot_page.py#tabs-4';</script>"
		#print disk_list_status

	#--------------End-----------------------------

	#---------------Scheduled snapshot Remove------------------
	if(form.getvalue("remove_snap")):
		get_disk_remove = form.getvalue("hid_disk_name")
		#print get_disk_remove
		#print '<br/>'
		get_time = form.getvalue("hid_snap_time")
		#print get_time
		#print '<br/>'
		status=snapshotschedule.remove_snap_rotate_script(get_disk_remove,get_time,debug=False)
		
		if(status == True):
			print "<div id='id_trace'>"
			print "Snapshot Scheduled deleted successfully!"
			print "</div>"
		else:
			print "<div id='id_trace_err'>"
			print "Error Occurred while deleting Snapshot Scheduled!"
			print "</div>"
		print "<script>location.href = 'iframe_snapshot_page.py#tabs-5';</script>"
	#---------------End-----------------------------

	all_status=snapshotschedule.get_all(debug=True)
	#for x in all_status:
	#	print x['scheduler_time']+'<br/>'


	#call_func = tools.decode_schedule("10 4 24 8 4")
	#print call_func



	#import left_nav
	print
	print """
		<div id="loader-div" style="text-align:center; display:none;" ><img style="margin-top:20%;" src="../images/ajax-loader.gif" /><br/> Loading...</div>
	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer" id="body-div">
		<!--tab srt-->
		<div class="searchresult-container">
		<div style="margin:0 0 0px 0;" class="topinputwrap-heading"><a class="demo" href ="#"><img src ="../images/help_icon1.png" style="width:13px;"><span class="tooltip" >
                 <table border="0">
        <tr>     
        <td class="text_css">This page lets you create, manage and schedule NAS snapshots.</td>
        </tr>
        </table>"""
	if(check_ha == True):
		print"""
	</span></a><span style="color:#fff;margin-left:7px;">Snapshot Information ("""+show_tn+""")</span>
                <span style="float:right; margin:0 0px 0 0;"><a onclick="return onclick_loader();" class="resource_links" href="https://"""+other_node_ip+"""/fs4/py/iframe_snapshot_page.py">"""+show_on+"""</a></span>
                </div>"""
	else:
		print""" </span></a>Snapshot Information</div>"""
	print"""
		  <div class="infoheader">
		    <div id="tabs">
		      <ul>
			<li><a href="#tabs-1">Create Snapshot</a></li>
			<li><a href="#tabs-2">Show Snapshots</a></li>
			<li><a href="#tabs-3">Schedule Snapshots</a></li>
			<li><a href="#tabs-4">List Schedule</a></li>
			<li><a href="#tabs-5">Remove Schedule</a></li>
		      </ul>

		<div id="tabs-1">
		<!--form container starts here-->
		<form name="create_snap_form" method="post" action="" />
		<!--<form name="create_snap_form" method="post" action="iframe_snapshot_page.py#tabs-1" />-->
		<div class="form-container">
		<div class="inputwrap">
		<div class="formleftside-content">

		<table style="width:500px;">
		<tr>
		<td>Disk name</td>
		<!--<td><input type="text" name="disk_name" class = 'textbox' /></td>-->
		<td>
		<div class="styled-select2">
		<select name="disk_name">
		<option value ="sel_disk">Select a disk name</option>"""
	if(get_nas_lvs["lvs"] != [{}]):
		for n in get_nas_lvs["lvs"]:
			print """<option value='NAS-"""+n['lv_name']+"""'>NAS-"""+n['lv_name']+"""</option>"""

	if(get_bio_lvs["lvs"] != [{}]):
		for b in get_bio_lvs["lvs"]:
			print """<option value='BIO"""+b['lv_name']+"""'>BIO"""+b['lv_name']+"""</option>"""

	print """</select></div>
		</tr>

		<tr>
		<td>Enter Size (GB)</td>
		<td><input type="text" name="size" class = 'textbox' style="width:188px;" /></td>
		</tr>

		<tr>
		<td></td>
		<td>
		<button class = 'buttonClass' type="submit" name = 'create_snapshot' value = 'create_snapshot' style = 'float:right; margin:20px 180px 20px 0;' onclick="return validate_snapshot_form2();">Create</button>
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
	if((get_snapshots["lvs"] != []) and (get_snapshots["lvs"] != [{}])):

		print """<nav id="menu_snap">

		<ul>"""

		i=1
		s=1
		for x in get_snapshots["lvs"]:
			#print x
			#exit();
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
			<form name="delete_snap_form" method="post" action="iframe_snapshot_page.py#tabs-2">
			<div style="display: none;" id='proppopUpDiv2"""+str(i)+"""'>
			<h5>Delete """+x['lv_name']+"""<span onclick="popup('proppopUpDiv2"""+str(i)+"""')" style="cursor:pointer;">X</span></h5>
			<div style="border:#D1D1D1 1px solid; text-align:center; height:70px; margin:20px 0 20px 0;">"""
			if((is_smb_configured == True) or (is_nfs_configured == True)):
				print """Cannot delete because the snapshot is busy!<br/><br/>
				<button class="buttonClass" type="button" name = 'local_action_but'  id = 'local_action_but' value = 'Update' style="float:right; margin:0px 200px 0 0; " onclick="popup('proppopUpDiv2"""+str(i)+"""')" >Go Back</button>"""
			else:
				print """Are you sure you want to delete """+x['lv_name']+""" ?<br/><br/>
				<input type="hidden" name="hid_snap_name" value='"""+x['lv_name']+"""' />
				<button class="buttonClass" type="button" name = 'local_action_but'  id = 'local_action_but' value = 'Update' style="float:right; margin:0px 200px 0 0; " onclick="popup('proppopUpDiv2"""+str(i)+"""')" >No</button>
				<button class="buttonClass" type="submit" name = 'delete_snapshot'  id = 'delete_snapshot' value = 'delete_snapshot' style="float:right; " >Yes</button>"""

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
			<td>"""+x["size"].replace("g","G")+"""</td>
			</tr>

			</table>


			</div>"""


			print """<li onclick="return folder_click("""+str(i)+""", """+str(array_len)+""", """+str(s)+""");"><a>"""+x['lv_name']+"""</a>

			<div id='"""+str(i)+"""' style="display:none;">
			<ul>
			
			<form name="smb_or_nfs" method="post" action="iframe_snapshot_page.py#tabs-2">
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
		print """<div style="text-align:center; width:600px;"><span>No Snapshot Found</span>!</div>"""



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
                <form name="create_snap_form1" method="post" action="iframe_snapshot_page.py#tabs-4" />
                <div class="form-container">
                <div class="inputwrap">
                <div class="formleftside-content">
		<table style="width:500px;">
                <tr>
                <td>Disk name</td>
                <!--<td><input type="text" name="disk_name" class = 'textbox' /></td>-->
                <td>
                <div class="styled-select2">
                <select name="disk_list" onchange='this.form.submit()'>
                <option>Select a disk name</option>"""
	if(get_nas_lvs["lvs"] != [{}]):
		for n in get_nas_lvs["lvs"]:
			nw_lv =  """NAS-"""+n['lv_name']+""""""
			print """<option value='"""+nw_lv+"""'"""

			if(disk_name_list !=''):
				if(disk_name_list == nw_lv):
					print"""selected ='selected'"""


			print""">"""+nw_lv+"""</option>"""

	if(get_bio_lvs["lvs"] != [{}]):
		for b in get_bio_lvs["lvs"]:
			bio_lv = """BIO-"""+b['lv_name']+""""""
			print """<option value='"""+bio_lv+"""'"""
			if(disk_name_list !=''):
				if(disk_name_list == bio_lv):
					print """selected = 'selected'"""

			print""">"""+bio_lv+"""</option>"""

        print """</select></div>
                </tr>
		</table>

		<table width = "680" style="margin-top: 13%;">
                <tr>
                <th style="border:#D1D1D1 1px solid;width:22%;">Disk name</th>
                <th style="border:#D1D1D1 1px solid;">Snapshot name</th>
                <th style="border:#D1D1D1 1px solid;">Snapshot size</th>
                <th style="border:#D1D1D1 1px solid;">Max no. of snapshots</th>
                <th style="border:#D1D1D1 1px solid;">Schedule</th>
                <!--<th style="border:#D1D1D1 1px solid;">Scheduled Time</th>-->
                </tr>
		<tr>
		<td  style="border:#D1D1D1 1px solid;padding-top:16%;text-align:center;margin-right:-530px;display:"""+display_blank+"""";" colspan = "5">
		<span>Select the disk to Get Information</span>
		</td>
		</tr>
		"""
		
	if(disk_list_status !=[]):
		for snap_info in disk_list_status:
			decode_sch = tools.decode_schedule(snap_info['scheduler_time'])
			disk_name = snap_info['diskname']
			disk_name = disk_name.replace("'", "")
			snap_name = snap_info['snap_name']
			snap_name = snap_name.replace("'", "")
			snap_size = snap_info['snap_size']
			snap_size = snap_size.replace("'", "")
			print"""
			<tr>
			<td style = "text-align:center;border:#D1D1D1 1px solid;">"""+disk_name+"""</td>
			<td style = "text-align:center;border:#D1D1D1 1px solid;">"""+snap_name+"""</td>
			<td style = "text-align:center;border:#D1D1D1 1px solid;">"""+snap_size+"""</td>
			<td style = "text-align:center;border:#D1D1D1 1px solid;">"""+snap_info['max_snaps']+"""</td>
			<td style = "text-align:center;border:#D1D1D1 1px solid;">"""+decode_sch+"""</td>
			</tr>"""
	else:
		print"""<tr>
                <td style="border:#D1D1D1 1px solid;padding-top: 3%; text-align: center;" colspan = "6"><span>No Information is Available for disk <p style="color:green;">"""+disk_name_list+"""</p></span></td>
                </tr>"""
		
	print"""		</table>
		

		 </div>
                 </div>
                </div>
                <!--form container ends here-->
                <p>&nbsp;</p>
                </div>

		<div id="tabs-5">
                <!--form container starts here-->
                <div class="form-container">
                <div class="inputwrap">
                <div class="formleftside-content">
		<form name = "remove_form" action="" method ="post">
	<table width = "680" style="margin-top: 13%;">
                <tr>
                <th style="border:#D1D1D1 1px solid;width:22%;">Disk name</th>
                <!--<th style="border:#D1D1D1 1px solid;">File Name</th>-->
                <th style="border:#D1D1D1 1px solid;">Snapshot name</th>
                <th style="border:#D1D1D1 1px solid;">Snapshot size</th>
                <th style="border:#D1D1D1 1px solid;">Max no. of snapshots</th>
		<th style="border:#D1D1D1 1px solid;">Schedule</th>
                <th style="border:#D1D1D1 1px solid;">Time</th>
                <th style="border:#D1D1D1 1px solid;">Delete</th>
                </tr>
		"""
		
	if(all_status !=[]):
		for snap_info in all_status:
			decode_sch = tools.decode_schedule(snap_info['scheduler_time'])
			disk_name = snap_info['diskname']
			disk_name = disk_name.replace("'", "")
			snap_name = snap_info['snap_name']
			snap_name = snap_name.replace("'", "")
			snap_size = snap_info['snap_size']
			snap_size = snap_size.replace("'", "")
			snap_time = snap_info['time']
			print"""
                	<form name="remove_snap1" method="post" action="" />
			<tr>
			<input type = "hidden" name = "hid_disk_name" value ='"""+disk_name+"""'>
			<input type = "hidden" name = "hid_snap_time" value = '"""+snap_time+"""'>
			<td style = "text-align:center;border:#D1D1D1 1px solid;">"""+disk_name+"""</td>
			<td style = "text-align:center;border:#D1D1D1 1px solid;">"""+snap_name+"""</td>
			<td style = "text-align:center;border:#D1D1D1 1px solid;">"""+snap_size+"""</td>
			<td style = "text-align:center;border:#D1D1D1 1px solid;">"""+snap_info['max_snaps']+"""</td>
			<td style = "text-align:center;border:#D1D1D1 1px solid;">"""+decode_sch+"""</td>
			<td style = "text-align:center;border:#D1D1D1 1px solid;">"""+snap_time+"""</td>
			<td style="float:right;width:98%;height:114px;margin-top:-3%;text-align:center;border:#D1D1D1 1px solid;"><button type="image" value = "remove" name='remove_snap' style="background: #fff; border: 0px;cursor:pointer;" ><img src="../images/snap_del_but.jpg" style="margin-top:65%;"></button></td> 
			</tr></form>"""
	else:
		print"""<tr>
                <td style="border:#D1D1D1 1px solid;padding-top: 3%; text-align: center;" colspan = "7"><span>No Information is Available</span></td>
                </tr>"""
		
	print"""		</table>


	
        
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
