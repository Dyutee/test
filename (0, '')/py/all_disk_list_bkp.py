#!/usr/bin/python
import cgitb, header, sys
cgitb.enable()
sys.path.append('../modules/')
import disp_except;

import os, commands, common_methods, system_info, string
try:
	sys.path.append('/var/nasexe/storage/')
	import storage_op
	from lvm_infos import *
	from functions import *

	sys.path.append('/var/nasexe/')
	import storage

	sys.path.append('/var/nasexe/python/')
	import tools
#---------------------------------Update & Delete Disk-------------------------------------------
	if(header.form.getvalue("delete_disk")):
		get_lv = header.form.getvalue("hid_lv_name")
		get_lv_type = header.form.getvalue("hid_lv_type")
		if(get_lv_type == "NAS"):
			remove_lv = storage_op.lvremove(get_lv)
			logstatus = common_methods.sendtologs('Success', 'Succefully deleted the '+get_lv+' NAS Disk', 'all_disk_list.py', str(remove_lv));
		if(get_lv_type == "VTL"):
			remove_lv = storage_op.lvremove(get_lv,debug='no',type1='VTL')	
			logstatus = common_methods.sendtologs('Success', 'Succefully deleted the '+get_lv+' VTL Disk', 'all_disk_list.py', str(remove_lv));
		if(get_lv_type == "BIO"):
			remove_lv = storage_op.lvremove(get_lv,debug='no',type1='BIO')
			logstatus = common_methods.sendtologs('Success', 'Succefully deleted the '+get_lv+' BIO Disk', 'all_disk_list.py', str(remove_lv));
		#else:
		#	remove_lv = ''

		if(remove_lv == True):
			print""" <div id = 'id_trace' >"""
			print "Disk deleted successfully!"
			print "</div>"
		else:
			print""" <div id = 'id_trace_err' >"""
			print "Error deleting disk!"
			print "</div>"
			logstatus = common_methods.sendtologs('Error', 'Error Occurred while deleting the Disk', 'all_disk_list.py', str(remove_lv));

	if(header.form.getvalue("submit_update")):
		#update_volume = form.getvalue("update_volume")
		disk_type = header.form.getvalue("disk_type")
		update_disk = header.form.getvalue("update_disk")
		print update_disk
		update_size = header.form.getvalue("update_size")
		size_info = header.form.getvalue("size_info")
		size_info = size_info.replace('GB', '')
		increase_size = float(size_info)+float(update_size)
		increase_size = str(increase_size)+"GB"
		
		if(disk_type == "NAS"):
			update_lv = storage_op.lv_increase(update_disk,increase_size)
			
			logstatus = common_methods.sendtologs('Success', 'Succefully update the '+update_disk+' Nas disk Size', 'all_disk_list.py', str(update_lv));
		elif(disk_type == "VTL"):
			update_lv = storage_op.lv_increase(update_disk,increase_size,type1='VTL')
			logstatus = common_methods.sendtologs('Success', 'Succefully update the '+update_disk+' VTL disk Size', 'all_disk_list.py', str(update_lv));
		elif(disk_type == "BIO"):
			update_lv = storage_op.lv_increase(update_disk,increase_size,type1='BIO')
			logstatus = common_methods.sendtologs('Success', 'Succefully update the '+update_disk+' BIO disk Size', 'all_disk_list.py', str(update_lv));
		elif(disk_type == "FIO"):
			update_lv = storage_op.lv_increase(update_disk,increase_size,type1='FIO')
			logstatus = common_methods.sendtologs('Success', 'Succefully update the FIO '+update_disk+' disk Size', 'all_disk_list.py', str(update_lv));
		else:
			update_lv = "NOT-FOUND"
			logstatus = common_methods.sendtologs('Success', 'Error Occurred while updating the '+update_disk+' Size', 'all_disk_list.py', str(update_lv));
			

		if(update_lv == True):
			print""" <div id = 'id_trace' >"""
			print "You Increase <font color = 'darkred'><b>"+str(update_size)+'GB'+" </b></font> of Size! Your Size <font color = 'darkred'><b>"+str(size_info)+'GB'+"</b></font> is successfully Updated to <font color = 'darkred'><b>"+increase_size+"</b></font>!"
			print "</div>"
		else:
			print""" <div id = 'id_trace_err' >"""
			print "Disk cannot be Identified!"
			print "</div>"

#---------------------------------End-----------------------------------------------------------------

	vg_info = get_vgs()
	#print vg_info

	type_list=['NAS','BIO','FIO','VTL']
	st=storage_op.list_all_disks()

	#if 'size' in st[0].keys():
	#	print True
	#else:
	#	print False

	get_vol_name = "ALL"
	get_vol_type = "ALL"
	#dict_val = get_lvs()
	#condition = dict_val
	#condition_len = dict_val["lvs"]
	condition = st
	condition_len = st
	array_len = len(condition_len)
	if(header.form.getvalue("volume_sel")):
		get_vol_name = header.form.getvalue("volume_sel")
		get_vol_type = header.form.getvalue("disk_type")
		subarray = []

		if((get_vol_name == "ALL") and (get_vol_type == "ALL")):
			condition = st

		elif((get_vol_name == "ALL") or (get_vol_type == "ALL")):
			if(get_vol_name == "ALL"):
				if 'type' in condition[0].keys():	
					for u in condition:
						if (u['type'] == get_vol_type):
							subarray.append(u)

			if(get_vol_type == "ALL"):
				if 'vg_name' in condition[0].keys():
					for u in condition:
						if (u['vg_name'] == get_vol_name):
							subarray.append(u)

			condition = subarray


		else:
			if (('vg_name' in condition[0].keys()) and ('type' in condition[0].keys())):
				for u in condition:
					if (u['vg_name'] == get_vol_name):
						if (u['type'] == get_vol_type):
							subarray.append(u)

			condition = subarray

		array_len = len(condition)

	#print array_len

	#if(header.form.getvalue("disk_type")):
	#       get_vol_type = header.form.getvalue("disk_type")
	#       if(get_vol_type == "ALL"):
	#               condition = st
	#       else:
	#               subarray2 = []
	#               for u in condition:
	#                       if (u['type'] == get_vol_type):
	#                               subarray2.append(u)

	#               condition = subarray2

	#       array_len2 = len(condition)


	image_icon = common_methods.getimageicon();

	log_array = [];
	log_file = common_methods.log_file;
	logstring = '';

	vg = '';

	nas_info = get_lvs()
	#nas_infonas = get_lvs("nas")
	#print nas_info
#---------------------------Delete the Disk-------------------------------------
	if(header.form.getvalue("delete_but")):
		get_lv = header.form.getvalue("delete_option[]")
		#print get_lv
		check_get_lv =isinstance(get_lv, str)

		if(check_get_lv ==True):
			remove_lv = storage_op.lvremove(get_lv)

		else:
			get_lv = set(get_lv)
			for value in get_lv:
				remove_lv = storage_op.lvremove(value)

		ss = remove_lv
		logstring = str(common_methods.now) + '<<>>From: ' + common_methods.remote_ip + '<<>>' + str(ss) + str(" Deleting Volume");
		log_array.append(logstring);
		common_methods.append_file(log_file, log_array);


		if(remove_lv == True):
			print"""<div id = 'id_trace'>"""
			print " Disk <font color='darkred'><b>"+str(get_lv)+"</b></font> Successfully Deleted!"
			print "</div>"
		else:
			print"""<div id = 'id_trace_err'>"""
			print "Error occured while deleting Disk <font color = 'darkred'><b>"+str(get_lv)+"</b></font> !"
			print "</div>"
#---------------------------------End-------------------------------------------------------------------
	vg_info = get_vgs()

	nas_info = get_lvs()
	#print 'Content-Type: text/html'
	for free_vg in vg_info["vgs"]:
		if(free_vg != {}):
			free_vg = free_vg["free_size"]

	get_shares = tools.get_all_shares(debug=True)

	import left_nav
	print
	print """
	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer">
		<div class="insidepage-heading">Raid >> <span class="content">Disk List Information</span></div>
		<!--tab srt-->
		<div class="searchresult-container">
		  <div class="infoheader">
		    <div id="tabs">
		      <ul>
			<li><a href="#tabs-1">Disk List</a></li>
		      </ul>
		      <div id="tabs-1">
		<form name="disk_list_form" action="" method="post">
		<!--form container starts here-->
		<div class="form-container">
		  <div class="inputwrap">
		    <div class="formrightside-content">
	<div id="filter_option">
		<table>
		<tr>
		<td>Filter by volume : </td>
		<td>    
			<div class="styled-select2"> 
			<select name="volume_sel" onchange="select_submit('select_volume');">
			<option>ALL</option>"""
	for x in vg_info["vgs"]:
		if(vg_info["vgs"] != [{}]):
			print """<option"""
			if(x["vg_name"] == get_vol_name):
				print "selected"

			print """>"""+x["vg_name"]+"""</option>"""

	print """
			</select>
			</div>
		</td>

		<td>Filter by Disk Type : </td>
		<td>
			<div class="styled-select2" onchange="select_submit('select_volume');"> 
			<select name="disk_type">
			<option>ALL</option>"""
	for t in type_list:
		print """<option"""
		if(t == get_vol_type):
			print "selected"

		print """>"""+t+"""</option>"""

	print """</select>
			</div>
		</td>
		</tr>
	</table>
	</form>

		</div>

	<nav id="menu_disk">

		<div style="width:700px; float:right; text-align:right; margin:0 0 10px 0;">
		<hr style="width:50px; float:left; display:block; border:#DF0101 1px solid; margin:10px 0 0 550px;"></hr>Disk is busy<br/>
		<hr style="width:50px; float:left; display:block; border:#04B404 1px solid; margin:10px 0 0 550px;"></hr>Disk is free<br/><br/>
		</div>
	<ul>"""

	#if(array_len != 0):
	if 'size' in st[0].keys():

		#array_len = 5
		multi = 1
		i=1
		s=1
		for y in condition:
			new = y["size"]

			if (new.find('g') > 0):
				size = new.replace("g", "");

			if (new.find('t') > 0):
				multi = 1024;
				size = new.replace("t", "")

			size = float(size) * multi;
			size = str(size) + ' GB';

			#checkforshares = commands.getoutput('sudo grep "/%s/" /var/www/global_files/shares_global_file' % y['lv_name']);
			checkforshares = ''

			#------------------------------ Check for shares in NAS Disk Start ------------------------------#
			if(get_shares["shares"] != []):
				for gs in get_shares["shares"]:
					split_path = string.split(gs["path"],"/")
					if(len(split_path) > 2):
						get_disk_from_path = split_path[2]
						if(get_disk_from_path == y["lv_name"]):
							checkforshares = "Shares-Present"
			#------------------------------- Check for shares in NAS Disk End -------------------------------#
					

			disk_name = y["lv_name"]
			get_protocols = system_info.check_protocols(disk_name)
			print_protocols = ''
			if(get_protocols == "No Protocols"):
				print_protocols = "No-Protocols"

			else:
				proto = ''
				for a in get_protocols:
					proto = proto+str(a)+'&nbsp;'

				print_protocols = proto
				#print_protocols = "No-Protocols"

			if((print_protocols != "No-Protocols") or (checkforshares != '')):
				border_bottom = 'style="border-bottom:#DF0101 1px solid;"'
			else:
				#border_bottom = ''
				border_bottom = 'style="border-bottom:#04B404 1px solid;"'


			print """<li """+border_bottom+""" onclick="return folder_click("""+str(i)+""", """+str(array_len)+""", """+str(s)+""");"><a>"""+y["lv_name"]+"""</a>

				<style>
				#popUpDiv1"""+str(i)+""" {position: fixed; background-color: #fff; min-width: 400px; z-index: 9002; padding: 5px;}
				#popUpDiv1"""+str(i)+""" h5{width:100%; font-size:15px; color:#0070bd; text-align:center; font-weight:bold;}
				#popUpDiv1"""+str(i)+""" span{ color:#FFFFFF; background-color:#0070bd; padding:1px 3px 0 3px; float:right;}

				#popUpDiv2"""+str(i)+""" {position: fixed; background-color: #fff; min-width: 400px; z-index: 9002; padding: 5px;}
				#popUpDiv2"""+str(i)+""" h5{width:100%; font-size:15px; color:#0070bd; text-align:center; font-weight:bold;}
				#popUpDiv2"""+str(i)+""" span{ color:#FFFFFF; background-color:#0070bd; padding:1px 3px 0 3px; float:right;}

				#popUpDiv3"""+str(i)+""" {position: fixed; background-color: #fff; min-width: 400px; z-index: 9002; padding: 5px;}
				#popUpDiv3"""+str(i)+""" h5{width:100%; font-size:15px; color:#0070bd; text-align:center; font-weight:bold;}
				#popUpDiv3"""+str(i)+""" span{ color:#FFFFFF; background-color:#0070bd; padding:1px 3px 0 3px; float:right;}

				#popUpDiv4"""+str(i)+""" {position: fixed; background-color: #fff; min-width: 400px; z-index: 9002; padding: 5px;}
				#popUpDiv4"""+str(i)+""" h5{width:100%; font-size:15px; color:#0070bd; text-align:center; font-weight:bold;}
				#popUpDiv4"""+str(i)+""" span{ color:#FFFFFF; background-color:#0070bd; padding:1px 3px 0 3px; float:right;}

				#popUpDiv5"""+str(i)+""" {position: fixed; background-color: #fff; min-width: 400px; z-index: 9002; padding: 5px;}
				#popUpDiv5"""+str(i)+""" h5{width:100%; font-size:15px; color:#0070bd; text-align:center; font-weight:bold;}
				#popUpDiv5"""+str(i)+""" span{ color:#FFFFFF; background-color:#0070bd; padding:1px 3px 0 3px; float:right;}

				</style>"""

			for b in vg_info["vgs"]:
				if(b["vg_name"] == y["vg_name"]):
					new_free = b["free_size"]

			if (new_free.find('g') > 0):
				multi = 1;
				new_free = new_free.replace('g', '');

			if (new_free.find('t') > 0):
				multi = 1024;
				new_free = new_free.replace('t', '');

			free_size = float(new_free) * multi;
			free_size = str(free_size) + ' GB';

			print """<div style="display: none;" id="blanket"></div>
				<div style="display: none;" id='popUpDiv1"""+str(i)+"""'>
				<h5>Increase Size of '"""+y['lv_name']+"""' <span onclick="popup('popUpDiv1"""+str(i)+"""')">X</span></h5>
				<form name="update_disk_size" action="main.py?page=disk_list#tabs-1" method="post" >
				<p class="popup">
				<span style="color:#424242; padding:0 0 10px 5px; background-color:#FFFFFF; font-size:12px; float:left;">Available Size in Volume '"""+y['vg_name']+"""' : """+free_size+"""</span>
				<table width="100%" style="text-align:center; padding:20px; border:#D1D1D1 1px solid;">

				<tr>
				<td align="left" width="45%">Previous Size</td>
				<td align="left">"""+size+"""</td>
				</tr>

				<tr>
				<td align="left">Volume</td>
				<td align="left">"""+y['vg_name']+"""</td>
				</tr>

				<tr>
				<td align="left">Disk</td>
				<td align="left">"""+y['lv_name']+"""</td>
				</tr>

				<tr>
				<td align="left">Increase Size</td>
				<td align="left"><input type="text" style = "text-align:center;" name="update_size" onkeypress="return isNumberKey(event)" size="5" > GB

				<input type="hidden" name="size_info" value='"""+size+"""' />
				<input type="hidden" name="update_disk" value='"""+y['lv_name']+"""' />
				<input type="hidden" name="disk_type" value='"""+y['type']+"""' />
				</td>
				</tr>

				</table>
			
				<button class="button_example" type="submit" name="submit_update" id="id_create_but" value = "Update" onclick ="return select_submit('update_disk');" style="float:right; margin:10px 20px 10px 10px;" >Update</button>
				</p>
				</form>
				</div>

				<div style="display: none;" id='popUpDiv2"""+str(i)+"""'>
				<h5>Information of """+y['lv_name']+"""<span onclick="popup('popUpDiv2"""+str(i)+"""')">X</span></h5>
				<p class="popup">
				<table width="100%" style="text-align:center; padding:20px 20px 20px 80px; margin:0 0 20px 0; border:#D1D1D1 1px solid;">"""

			print """<tr>
				<td align="left" width="45%">Disk Name</td>
				<td align="left">"""+y['lv_name']+"""</td>
				</tr>

				<tr>
				<td align="left" width="45%">Disk Type</td>
				<td align="left">"""+y['type']+"""</td>
				</tr>

				<tr>
				<td align="left" width="45%">Volume Name</td>
				<td align="left">"""+y['vg_name']+"""</td>
				</tr>

				<tr>
				<td align="left" width="45%">Disk Size</td>
				<td align="left">"""+size+"""</td>
				</tr>

				<tr>
				<td align="left" width="45%">Protocols</td>
				<td align="left">"""+print_protocols+"""</td>
				</tr>

				</table>

				</p>
				</div>

				<div style="display: none;" id='popUpDiv3"""+str(i)+"""'>
				<form name="delete_disk_form" method="post" action="">
				<h5>Delete """+y['lv_name']+"""<span onclick="popup('popUpDiv3"""+str(i)+"""')">X</span></h5>
				<p class="popup">
				<div style="border:#D1D1D1 1px solid; text-align:center; height:70px; margin-bottom:20px;">"""
			if((print_protocols != "No-Protocols") or (checkforshares != '')):
				print """Cannot Delete because the disk is BUSY!<br/><br/>
				<button class="button_example" type="button" name = 'local_action_but'  id = 'local_action_but' value = 'Update' style="float:right; margin:0px 150px 0 0; " onclick="popup('popUpDiv3"""+str(i)+"""')" >Go Back</button>"""
			else:
				print """Are you sure you want to delete """+y['lv_name']+"""?<br/><br/>
			<button class="button_example" type="button" name = 'local_action_but'  id = 'local_action_but' value = 'Update' style="float:right; margin:0px 150px 0 0; " onclick="popup('popUpDiv3"""+str(i)+"""')" >No</button>
			<input type="hidden" name="hid_lv_name" value='"""+y['lv_name']+"""'>
			<input type="hidden" name="hid_lv_type" value='"""+y['type']+"""'>
			<button class="button_example" type="submit" name = 'delete_disk'  id = 'delete_disk' value = 'Update' style="float:right; " >Yes</button>"""

			print """</div>
			</p>
			</form>
			</div>

			<div id='"""+str(i)+"""' style="display:none;">
			<ul>

			<li><a href="#" onclick="popup('popUpDiv1"""+str(i)+"""')">Increase Size</a></li>
			<li><a href="#" onclick="popup('popUpDiv2"""+str(i)+"""')">Information</a></li>
			<li><a href="#" onclick="popup('popUpDiv3"""+str(i)+"""')">Delete</a></li>

			</ul>
			</div>

			</li>"""
			i=i+1

		print """
		</ul>

		</nav>"""

	else:
		print """<div style="text-align:center; color:#FE2E2E;">No Disk Found !</div>"""


	print"""


		</div>
		  </div>
		</div>
		<!--form container ends here-->
		</form>
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
	"""
except Exception as e:
        disp_except.display_exception(e);
