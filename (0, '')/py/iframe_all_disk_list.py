#!/usr/bin/python
import cgitb,  sys
cgitb.enable()
sys.path.append('../modules/')
import disp_except;

try:
	#################################################
        ################ import modules #################
        #################################################
	import os, commands, common_methods, system_info, string, include_files, cgi
	sys.path.append('/var/nasexe/storage/')
	import storage_op
	import san_disk_funs
	from lvm_infos import *
	from functions import *
	form = cgi.FieldStorage()
	sys.path.append('/var/nasexe/')
	import storage
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
	import mhvtl


	################################################
        ################# Delete Image #################
        ################################################
	if(form.getvalue("delete_image")):
		get_con_rm = form.getvalue("hid_con_name")
		get_img_rm = form.getvalue("hid_img_name")

		check_file = os.path.isfile('/storage/FIO/'+get_con_rm+'/'+get_img_rm)

		if(check_file==True):
			rm_image = commands.getstatusoutput('sudo rm -rf /storage/FIO/'+get_con_rm+'/'+get_img_rm)

			if(rm_image[0]==0):
				print"""<div id = 'id_trace'>"""
				print """Image '"""+get_img_rm+"""' removed Successfully!"""
				print "</div>"
			else:
				print"""<div id = 'id_trace_err' >"""
				print """Error Deleting Image '"""+get_img_rm+"""'!"""
				print "</div>"

		else:
			print"""<div id = 'id_trace_err' >"""
			print """Image not Found!"""
			print "</div>"
	#--------------------- END --------------------#

	################################################
        ################# Create Image #################
        ################################################
	if(form.getvalue("create_image")):
		get_vol_chk = form.getvalue("volume_con")
		get_img_name = form.getvalue("img_name")
		get_img_size = form.getvalue("img_size")

		if(get_img_name != None and get_img_size != None):
			get_img_size = get_img_size+'GB'
			mod_img_name = "TYRFS-"+str(get_img_name)
			test_img_name = storage.storage_op.test_image(mod_img_name)
			if test_img_name  == True:
				call_cr_img = storage.storage_op.fio_image_create(get_img_name,get_vol_chk,get_img_size)

				if(call_cr_img == True):
					print"""<div id = 'id_trace'>"""
					print """Image '"""+get_img_name+"""' created Successfully!"""
					print "</div>"
				else:
					print"""<div id = 'id_trace_err' >"""
					print """Error Creating Image '"""+get_img_name+"""' !"""
					print "</div>"

			else:
				print"""<div id = 'id_trace_err' >"""
				print """Image '"""+get_img_name+"""' already Exists !"""
				print "</div>"
		else:
			print"""<div id = 'id_trace_err' >"""
			print """Error: Enter both Image name & Image size!"""
			print "</div>"
	#--------------------- END --------------------#

	################################################
        ############## Add BIO disk to SAN #############
        ################################################
	if(form.getvalue("add_to_san")):
		get_radio = form.getvalue("select_disk")
		get_lv_name = form.getvalue("select_lv")
		get_san_name = form.getvalue("s_name")
		get_san_blocksize = form.getvalue("select_block")
		get_hid_vg_name = form.getvalue("hid_vg_name")
	
		if(get_san_name != None and get_san_blocksize != "select-size"):
			if(get_radio == 'BIO'):
				get_path = '/dev/'+get_hid_vg_name+'/BIO-'+str(get_lv_name)
				disk_type = 'BIO'
			if(get_radio == 'FIO'):
				split_gln = string.split(get_lv_name, ':')
				get_path = '/storage/FIO/'+split_gln[1]+'/'+split_gln[0]
				disk_type = 'FIO'

			call_add_func = san_disk_funs.add_disk_san(get_path,get_san_name,get_san_blocksize,type=disk_type)
			if(call_add_func == True):
				print"""<div id = 'id_trace'>"""
				print """Successfully added '"""+get_lv_name+"""' to SAN!"""
				print "</div>"
			else:
				print"""<div id = 'id_trace_err' >"""
				print """Error adding '"""+get_lv_name+"""' to SAN!"""
				print "</div>"
		else:
                        print"""<div id = 'id_trace_err' >"""
                        print """Error: Enter both SAN Name & size!"""
                        print "</div>"
	#--------------------- END --------------------#

	################################################
        ############# Add FIO Image to SAN #############
        ################################################
	if(form.getvalue("add_to_san_fio")):
                get_image_type = form.getvalue("select_disk")
                get_image_name = form.getvalue("image_name")
                get_lv_name = form.getvalue("select_lv")
                get_san_name = form.getvalue("san_name")
                get_san_blocksize = form.getvalue("select_block")

		if(get_san_name != None and get_san_blocksize != "select-size"):
			get_path = '/storage/FIO/'+get_lv_name+'/'+get_image_name

			call_add_func = san_disk_funs.add_disk_san(get_path,get_san_name,get_san_blocksize,type=get_image_type)
			if(call_add_func == True):
				print"""<div id = 'id_trace'>"""
				print """Successfully added '"""+get_lv_name+"""' to SAN!"""
				print "</div>"
			else:
				print"""<div id = 'id_trace_err' >"""
				print """Error adding '"""+get_lv_name+"""' to SAN!"""
				print "</div>"


		else:
			print"""<div id = 'id_trace_err' >"""
                        print """Error: Enter both SAN Name & size!"""
                        print "</div>"
	#--------------------- END --------------------#

	################################################
        ############### Remove from SAN ################
        ################################################
	if(form.getvalue("delete_san_but")):
		san_val = form.getvalue("delete_option_san")
		split_san = string.split(san_val,":")
		remove_san =san_disk_funs.remove_disk_san(split_san[0],split_san[1])

		if(remove_san== True):
			print"""<div id = 'id_trace'>"""
			print "Successfully removed from SAN !"
			print "</div>"
		else:
			print"""<div id = 'id_trace_err'>"""
			print "Error occured while removing form SAN  !"
			print "</div>"
	#--------------------- END --------------------#

	################################################
        ################# Delete Disk ##################
        ################################################
	if(form.getvalue("delete_disk")):
		get_lv = form.getvalue("hid_lv_name")
		get_lv_type = form.getvalue("hid_lv_type")
		if(get_lv_type == "NAS"):
			remove_lv = storage_op.lvremove(get_lv)
			logstatus = common_methods.sendtologs('Success', 'Succefully deleted the '+get_lv+' NAS Disk', 'all_disk_list.py', str(remove_lv));
		if(get_lv_type == "VTL"):
			remove_lv = storage_op.lvremove(get_lv,debug='no',type1='VTL')	
			logstatus = common_methods.sendtologs('Success', 'Succefully deleted the '+get_lv+' VTL Disk', 'all_disk_list.py', str(remove_lv));
		if(get_lv_type == "BIO"):
			remove_lv = storage_op.lvremove(get_lv,debug='no',type1='BIO')
			logstatus = common_methods.sendtologs('Success', 'Succefully deleted the '+get_lv+' BIO Disk', 'all_disk_list.py', str(remove_lv));
		if(get_lv_type == "FIO"):
			remove_lv = storage_op.lvremove(get_lv,debug='no',type1='FIO')
			logstatus = common_methods.sendtologs('Success', 'Succefully deleted the '+get_lv+' FIO Disk', 'all_disk_list.py', str(remove_lv));
		if(remove_lv == True):
			print""" <div id = 'id_trace' >"""
			print "Disk deleted successfully!"
			print "</div>"
		else:
			print""" <div id = 'id_trace_err' >"""
			print "Error deleting disk!"
			print "</div>"
			logstatus = common_methods.sendtologs('Error', 'Error Occurred while deleting the Disk', 'all_disk_list.py', str(remove_lv));
	#--------------------- END --------------------#

	################################################
        ################ Increase Size #################
        ################################################
	if(form.getvalue("submit_update")):
		#update_volume = form.getvalue("update_volume")
		disk_type = form.getvalue("disk_type")
		update_disk = form.getvalue("update_disk")
		update_size = form.getvalue("update_size")
		try:
			testup = float(update_size)
		
			if(update_size != None):
				size_info = form.getvalue("size_info")
				size_info = size_info.replace('GB', '')
				increase_size = float(size_info)+float(update_size)
				increase_size = str(increase_size)+"GB"
				if((float(update_size) != 0.0) and (float(update_size) > 0)):
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
				else:
					print""" <div id = 'id_trace_err' >"""
					print "Enter size greater than zero!"
					print "</div>"
			else:
				print""" <div id = 'id_trace_err' >"""
				print "Error: Enter size to increase!"
				print "</div>"
		except:
			print""" <div id = 'id_trace_err' >"""
			print "Error: Only integers allowed!"
			print "</div>"
	#--------------------- END --------------------#

	#--- Get VGS
	vg_info = get_vgs()

	################################################
        ############## Filter Conditions ###############
        ################################################
	type_list=['NAS','BIO','FIO','VTL']
	st=storage_op.list_all_disks()

	get_vol_name = "ALL"
	get_vol_type = "ALL"

	condition = st
	condition_len = st
	array_len = len(condition_len)
	if(form.getvalue("volume_sel")):
		get_vol_name = form.getvalue("volume_sel")
		get_vol_type = form.getvalue("disk_type")
		subarray = []

		if((get_vol_name == "ALL") and (get_vol_type == "ALL")):
			condition = st

		elif((get_vol_name == "ALL") or (get_vol_type == "ALL")):
			if(get_vol_name == "ALL"):
				if condition != []:	
					for u in condition:
						if (u['type'] == get_vol_type):
							subarray.append(u)

			if(get_vol_type == "ALL"):
				if condition != []:	
					if (('vg_name' in condition[0].keys()) and ('type' in condition[0].keys())):
						for u in condition:
							if (u['vg_name'] == get_vol_name):
								subarray.append(u)

			condition = subarray


		else:
			if condition != []:	
				if (('vg_name' in condition[0].keys()) and ('type' in condition[0].keys())):
					for u in condition:
						if (u['vg_name'] == get_vol_name):
							if (u['type'] == get_vol_type):
								subarray.append(u)

			condition = subarray

		array_len = len(condition)
	#--------------------- END --------------------#

	image_icon = common_methods.getimageicon();

	log_array = [];
	log_file = common_methods.log_file;
	logstring = '';

	vg = '';

	nas_info = get_lvs()

	################################################
        ################# Delete Disk ##################
        ################################################
	if(form.getvalue("delete_but")):
		get_lv = form.getvalue("delete_option[]")
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
	#--------------------- END --------------------#

	#--- Get VGS
	vg_info = get_vgs()

	#--- Get LVS
	nas_info = get_lvs()

	for free_vg in vg_info["vgs"]:
		if(free_vg != {}):
			free_vg = free_vg["free_size"]

	#--- Get all Shares
	get_shares = tools.get_all_shares(debug=True)

	#--- Get all VTLS
	get_all_vtls = mhvtl.get_all_vtls()


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
        <td class="text_css">This page displays all the disks present on the system. You can also perform several actions on those disks, such as view the details of those disks, increase their size or delete them.</td>
        </tr>
        </table>"""
	if(check_ha == True):
	
		print"""</span></a> Disk Information ("""+show_tn+""")
                <span style="float:right; margin:0;"><a onclick="return onclick_loader();" class="resource_links" href="https://"""+other_node_ip+"""/fs4/py/iframe_all_disk_list.py">"""+show_on+"""</a></span>

                </div>"""
	else:
		print """</span></a><p class = "gap_text">Disk Information</p></div>"""
	print"""
		  <div class="infoheader">
		    <div id="tabs">
		      <ul>
			<li><a href="#tabs-1">Disk List</a></li>
			<li><a href="#tabs-2">Images List</a></li>
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
	<ul>
	"""

	if(array_len != 0):
		if 'size' in st[0].keys():

			#array_len = 5
			multi = 1
			i=1
			s=1
			san_list = san_disk_funs.list_all_disk_att()
			for y in condition:

                                vtl_var = "no"
				if(y["type"] == "VTL"):
					for o in get_all_vtls['vtl_libs']:
						lib_home_dir = o['lib_home_dir'].strip()
						lib_home_dir = lib_home_dir[:lib_home_dir.rfind('/')]
						lib_home_dir = lib_home_dir[lib_home_dir.rfind('/')+1:]
						if(lib_home_dir == y["lv_name"]):
							vtl_var = "yes"


				san_name = ''
				add_san_var = ''
				if(y["type"] == "BIO"):
					if san_list != []:
						for g in san_list:
							if 'd_name' in g.keys():
								f_name = g['filename']
								f_name = f_name[f_name.rfind('-')+1:]
								f_name = g["d_name"]
								if(f_name == y["type"]+"-"+y["lv_name"]):
									add_san_var = "yes"

							for keys in g:
								if (str(keys) == 'd_name'):
									filename = g['filename']
									filename = filename[filename.rfind('-')+1:]
									filename = g["d_name"]
									if(filename == y["type"]+"-"+y["lv_name"]):
										san_name = g["name"]
				
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
				if(y["type"] == "NAS"):
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
				print_protocols = 'No-Protocols'
				if(y["type"] == "NAS"):
					if(get_protocols == "No Protocols"):
						print_protocols = "No-Protocols"

					else:
						proto = ''
						for a in get_protocols:
							proto = proto+str(a)+'&nbsp;'

						print_protocols = proto
						#print_protocols = "No-Protocols"
				
				#--------------------------- FIO Disk Start ---------------------------#
				get_images = []
				un_use = ''
				if(y["type"] == "FIO"):
					get_images = storage_op.list_size_images(y['lv_name'])

					size_lv = storage.get_size_lv(y['lv_name'],type2='FIO')
					images = get_images
					tot_vir_size=0.0
					tot_disk_size=0.0
					if len(images) ==0:
						re={'lvsize':size_lv,'vmsize':tot_vir_size,'dsize':tot_disk_size}

					for vm in images:
						siz_t=vm['size']
						t_v=storage_op.convert_size(siz_t)
						tot_vir_size+=t_v
						siz_d=vm['used']
						t_d=storage_op.convert_size(siz_d)
						tot_disk_size+=t_d

					re={'lvsize':size_lv,'vmsize':tot_vir_size,'dsize':tot_disk_size}

					u_siz = re['vmsize']
					lv_siz1 = re['lvsize']
					un_use = lv_siz1 - u_siz
				#--------------------------- FIO Disk End ---------------------------#


				if((print_protocols != "No-Protocols") or (checkforshares != '')):
					border_bottom = 'style="border-bottom:#DF0101 1px solid;"'
				else:
					#border_bottom = ''
					border_bottom = 'style="border-bottom:#04B404 1px solid;"'

				if(add_san_var == "yes"):
					border_bottom = 'style="border-bottom:#DF0101 1px solid;"'

				if(get_images!=[]):
					border_bottom = 'style="border-bottom:#DF0101 1px solid;"'

				if(vtl_var == "yes"):
					border_bottom = 'style="border-bottom:#DF0101 1px solid;"'


				if(y["type"] != "SNP"):
					print """<li """+border_bottom+""" onclick="return folder_click("""+str(i)+""", """+str(array_len)+""", """+str(s)+""");"><a>"""+y["lv_name"]+"""</a>"""

				print """<style>
					#popUpDiv1"""+str(i)+""" {position: fixed; background-color: #fff; min-width: 400px; z-index: 9002; padding: 5px; top:100px !important;}
					#popUpDiv1"""+str(i)+""" h5{width:100%; font-size:15px; color:#0070bd; text-align:center; font-weight:bold;}
					#popUpDiv1"""+str(i)+""" span{ color:#FFFFFF; background-color:#0070bd; padding:1px 3px 0 3px; float:right;}

					#popUpDiv2"""+str(i)+""" {position: fixed; background-color: #fff; min-width: 400px; z-index: 9002; padding: 5px; top:100px !important;}
					#popUpDiv2"""+str(i)+""" h5{width:100%; font-size:15px; color:#0070bd; text-align:center; font-weight:bold;}
					#popUpDiv2"""+str(i)+""" span{ color:#FFFFFF; background-color:#0070bd; padding:1px 3px 0 3px; float:right;}

					#popUpDiv3"""+str(i)+""" {position: fixed; background-color: #fff; min-width: 400px; z-index: 9002; padding: 5px; top:100px !important;}
					#popUpDiv3"""+str(i)+""" h5{width:100%; font-size:15px; color:#0070bd; text-align:center; font-weight:bold;}
					#popUpDiv3"""+str(i)+""" span{ color:#FFFFFF; background-color:#0070bd; padding:1px 3px 0 3px; float:right;}

					#popUpDiv4"""+str(i)+""" {position: fixed; background-color: #fff; min-width: 400px; z-index: 9002; padding: 5px; top:100px !important;}
					#popUpDiv4"""+str(i)+""" h5{width:100%; font-size:15px; color:#0070bd; text-align:center; font-weight:bold;}
					#popUpDiv4"""+str(i)+""" span{ color:#FFFFFF; background-color:#0070bd; padding:1px 3px 0 3px; float:right;}

					#popUpDiv5"""+str(i)+""" {position: fixed; background-color: #fff; min-width: 400px; z-index: 9002; padding: 5px; top:100px !important;}
					#popUpDiv5"""+str(i)+""" h5{width:100%; font-size:15px; color:#0070bd; text-align:center; font-weight:bold;}
					#popUpDiv5"""+str(i)+""" span{ color:#FFFFFF; background-color:#0070bd; padding:1px 3px 0 3px; float:right;}

					#popUpDiv6"""+str(i)+""" {position: fixed; background-color: #fff; min-width: 400px; z-index: 9002; padding: 5px; top:100px !important;}
					#popUpDiv6"""+str(i)+""" h5{width:100%; font-size:15px; color:#0070bd; text-align:center; font-weight:bold;}
					#popUpDiv6"""+str(i)+""" span{ color:#FFFFFF; background-color:#0070bd; padding:1px 3px 0 3px; float:right;}

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
					<form name="update_disk_size" action="iframe_all_disk_list.py#tabs-1" method="post" >
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
					<td align="left">Increase Size (GB)</td>
					<td align="left"><input class="textbox" type="text" style = "text-align:center;" name="update_size" />

					<input type="hidden" name="size_info" value='"""+size+"""' />
					<input type="hidden" name="update_disk" value='"""+y['lv_name']+"""' />
					<input type="hidden" name="disk_type" value='"""+y['type']+"""' />
					</td>
					</tr>

					</table>
				
					<button class="buttonClass" type="submit" name="submit_update" id="id_create_but" value = "Update" onclick ="return select_submit('update_disk');" style="float:right; margin:10px 20px 10px 10px;" >Update</button>
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
				#print print_protocols
				#print "<br/>"
				#print checkforshares
				#print "<br/>"
				#print add_san_var
				#print "<br/>"
				#print get_images
				#print "<br/>"
				if((print_protocols != "No-Protocols") or (checkforshares != '') or (add_san_var == "yes") or (get_images != []) or (vtl_var == "yes")):
					print """Cannot Delete because the disk is BUSY!<br/><br/>
					<button class="buttonClass" type="button" name = 'local_action_but'  id = 'local_action_but' value = 'Update' style="float:right; margin:0px 150px 0 0; " onclick="popup('popUpDiv3"""+str(i)+"""')" >Go Back</button>"""
				else:
					print """Are you sure you want to delete """+y['lv_name']+"""?<br/><br/>
				<button class="buttonClass" type="button" name = 'local_action_but'  id = 'local_action_but' value = 'Update' style="float:right; margin:0px 100px 0 0; " onclick="popup('popUpDiv3"""+str(i)+"""')" >No</button>
				<input type="hidden" name="hid_lv_name" value='"""+y['lv_name']+"""'>
				<input type="hidden" name="hid_lv_type" value='"""+y['type']+"""'>
				<button class="buttonClass" type="submit" name = 'delete_disk'  id = 'delete_disk' value = 'Update' style="float:right; margin:0 10px 0 0;" >Yes</button>"""

				print """</div>
				</p>
				</form>
				</div>
				
				<div style="display: none;" id='popUpDiv6"""+str(i)+"""'>
				<form name="delete_disk_form" method="post" action="">
				<h5>Add Image to """+y['lv_name']+"""<span onclick="popup('popUpDiv6"""+str(i)+"""')">X</span></h5>
				<p class="popup">"""
				if(un_use != 0.0):
					print """<div style="border:#D1D1D1 1px solid; text-align:center; height:150px; margin-bottom:20px;">

					<table width="100%" style="text-align:center; padding:20px; ">

					<tr>
					<td align="left" width="45%">Enter Image Name</td>
					<td align="left"><input class = 'textbox' type = '' name = 'img_name' id = 'group' style="float:left; width:187px;"></td>
					</tr>

					<tr>
					<td align="left" width="45%">Enter Image Size (GB)<br/>"""
					if(un_use != ''):
						print """<font style="color:#B45F04;">(MAX """+str(un_use)+"""GB available)</font>"""

					print """</td>
					<td align="left"><input class = 'textbox' type = 'text' name = 'img_size' id = 'group' style="float:left; width:187px;"></td>
					</tr>

					<input type="hidden" name="volume_con" value='"""+y["lv_name"]+"""' />
					<tr>
					<td align="left" width="45%"></td>
					<td align="left">
					<button class="buttonClass" style="float:right; margin:10px 5px 0 0; width:120px;" type="submit" name = 'create_image'  id = 'create_image' value = 'create_image'>Create Image</button>
					</td>
					</tr>

					</table>

					</div>"""
				else:
					print """ No space Available in """+y["lv_name"]+""" """
				
				print """</p>
				</form>
				</div>

				<div style="display: none;" id='popUpDiv5"""+str(i)+"""'>
				<form name="delete_disk_form" method="post" action="">
				<h5>Remove """+y['lv_name']+""" from SAN<span onclick="popup('popUpDiv5"""+str(i)+"""')">X</span></h5>
				<p class="popup">
				<div style="border:#D1D1D1 1px solid; text-align:center; height:70px; margin-bottom:20px;">
				Are you sure you want to remove """+y['lv_name']+""" from SAN?<br/><br/>
				<button class="buttonClass" type="button" name = 'local_action_but'  id = 'local_action_but' value = 'Update' style="float:right; margin:0px 100px 0 0; " onclick="popup('popUpDiv5"""+str(i)+"""')" >No</button>
				<input type="hidden" name="delete_option_san" value='"""+san_name+':'+y['type']+"""'>
				<button class="buttonClass" type="submit" name = 'delete_san_but'  id = 'delete_san_but' value = 'delete_san_but' style="float:right; margin:0 10px 0 0;" >Yes</button>"""

				print """</div>
				</p>
				</form>
				</div>

				<div style="display: none;" id='popUpDiv4"""+str(i)+"""'>
				<form name="add_to_san" method="POST" >
				<h5>Add """+y["lv_name"]+""" to SAN<span onclick="popup('popUpDiv4"""+str(i)+"""')">X</span></h5>
				<p class="popup">
				<div style="border:#D1D1D1 1px solid; text-align:center; height:150px; margin-bottom:20px;">

				<table width="100%" style="text-align:center; padding:20px; ">

				<tr>
				<td align="left" width="45%">Enter Name</td>
				<td align="left"><input type="text" class="textbox" name="s_name" id="s_name" style="width:187px;" /></td>
				</tr>

				<tr>
				<td align="left" width="45%">Block Size</td>
				<td align="left">
				<div class="styled-select2">
				<select name='select_block' id="select_block">
				<option value='select-size'>Select Size</option>
				<option>512</option>
				<option>4096</option>
				</select>
				</div>
				</td>
				</tr>
				<input type="hidden" name='select_disk' value='"""+y["type"]+"""' />
				<input type="hidden" name='select_lv' value='"""+y["lv_name"]+"""' />
				<input type="hidden" name='hid_vg_name' value='"""+y['vg_name']+"""' />

				<tr>
				<td align="left" width="45%"></td>
				<td align="left">
				<button class="buttonClass" style="float:right; margin:10px 20px 0 0;" type="submit" name = 'add_to_san'  id = 'add_to_san' value = 'add_to_san'  >Add to SAN</button>
				</td>
				</tr>

				</table>
				</div>
				</p>
				</form>
				</div>

				<div id='"""+str(i)+"""' style="display:none;">
				<ul>

				<li><a href="#" onclick="popup('popUpDiv1"""+str(i)+"""')">Increase Size</a></li>
				<li><a href="#" onclick="popup('popUpDiv2"""+str(i)+"""')">Information</a></li>"""
				if(y['type'] == "BIO"):
					if(add_san_var == "yes"):
						print """<li><a href="#" onclick="popup('popUpDiv5"""+str(i)+"""')">Remove from SAN</a></li>"""
					else:
						print """<li><a href="#" onclick="popup('popUpDiv4"""+str(i)+"""')">Add to SAN</a></li>"""

				if(y["type"] == "FIO"):
					print """<li><a href="#" onclick="popup('popUpDiv6"""+str(i)+"""')">Add Image</a></li>"""
					
				print """<li><a href="#" onclick="popup('popUpDiv3"""+str(i)+"""')">Delete</a></li>

				</ul>
				</div>

				</li>"""
				i=i+1

			print """
			</ul>

			</nav>"""

		else:
			print """<div style="text-align:center; ">No Disk Found !</div>"""

	else:
		print """<div style="text-align:center; ">No Disk Found !</div>"""

	print"""


		</div>
		  </div>
		</div>
		<!--form container ends here-->
		</form>
		<p>&nbsp;</p>
		      </div>

	<div id="tabs-2">
	<div class="form-container">
	<div class="inputwrap">
	<div class="formrightside-content">

	"""

	def copyf(dictlist, key, valuelist):
	      return [dictio for dictio in dictlist if dictio[key] in valuelist]

	all_images = []
	if(array_len != 0):
		if 'size' in st[0].keys():
			valuelist = ['FIO']
			fio_st = copyf(st, 'type', valuelist)

			for n in fio_st:
				get_images = storage_op.list_size_images(n["lv_name"])
				if(get_images != []):
					for b in get_images:
						b['lv_name']=n["lv_name"]
						all_images.append(b)

	if(all_images != []):
		print """<nav id="menu_image">

		<div style="width:700px; float:right; text-align:right; margin:0 0 10px 0;">
                <hr style="width:50px; float:left; display:block; border:#DF0101 1px solid; margin:10px 0 0 550px;"></hr>Image is busy<br/>
                <hr style="width:50px; float:left; display:block; border:#04B404 1px solid; margin:10px 0 0 550px;"></hr>Image is free<br/><br/>
                </div>

                <ul>"""
		
		image_array_len = 4000+len(all_images)
                r=4001
                t=4001
                for k in all_images:
			san_list = san_disk_funs.list_all_disk_att()
			add_san_img = ''
			img_san_name = ''
			if san_list != []:
                                for g in san_list:
                                        if 'filename' in g.keys():
                                                f_name = g['filename']
                                                f_name = f_name[f_name.rfind('/')+1:]
                                                if(f_name == k["name"]):
                                                        add_san_img = "yes"
							img_san_name = g["name"]


			#if 'filename' in k.keys():
			#	file_name = k['filename']
			#	file_name = file_name[file_name.rfind('/')+1:]
			#	if(file_name == k["name"]):
			#		add_san_img = "yes"

			if(add_san_img == "yes"):
                                border_bottom_img = 'style="border-bottom:#DF0101 1px solid;"'
			else:
				border_bottom_img = 'style="border-bottom:#04B404 1px solid;"'

                        print """
                        <style>
                        #proppopUpDiv69"""+str(r)+""" {position: fixed; background-color: #fff; width: 400px; z-index: 9002; padding: 5px;}
                        #proppopUpDiv69"""+str(r)+""" h5{width:100%; font-size:15px; color:#0070bd; text-align:center; font-weight:bold;}
                        #proppopUpDiv69"""+str(r)+""" span{ color:#FFFFFF; background-color:#0070bd; padding:1px 3px 0 3px; float:right;}
                        #proppopUpDiv69"""+str(r)+""" ul.idTabs{list-style:none; border:none; width:400px; margin:5px 0 0 0;}
                        #proppopUpDiv69"""+str(r)+""" ul.idTabs li{display:inline;}
                        #proppopUpDiv69"""+str(r)+""" ul.idTabs li a.link_tabs{display:inline; border:none; background-color:#D1D1D1; padding:10px;}
                        #proppopUpDiv69"""+str(r)+""" ul.idTabs li a.link_tabs:hover{background-color:#cfbdbd;}
                        
                        #proppopUpDiv67"""+str(r)+""" {position: fixed; background-color: #fff; width: 400px; z-index: 9002; padding: 5px;}
                        #proppopUpDiv67"""+str(r)+""" h5{width:100%; font-size:15px; color:#0070bd; text-align:center; font-weight:bold;}
                        #proppopUpDiv67"""+str(r)+""" span{ color:#FFFFFF; background-color:#0070bd; padding:1px 3px 0 3px; float:right; cursor:pointer;}
                        #proppopUpDiv67"""+str(r)+""" ul.idTabs{list-style:none; border:none; width:400px; margin:5px 0 0 0;}
                        #proppopUpDiv67"""+str(r)+""" ul.idTabs li{display:inline;}
                        #proppopUpDiv67"""+str(r)+""" ul.idTabs li a.link_tabs{display:inline; border:none; background-color:#D1D1D1; padding:10px;}
                        #proppopUpDiv67"""+str(r)+""" ul.idTabs li a.link_tabs:hover{background-color:#cfbdbd;}

			#propopUpDiv55"""+str(r)+""" {position: fixed; background-color: #fff; min-width: 400px; z-index: 9002; padding: 5px; top:100px !important;}
                        #propopUpDiv55"""+str(r)+""" h5{width:100%; font-size:15px; color:#0070bd; text-align:center; font-weight:bold;}
                        #propopUpDiv55"""+str(r)+""" span{ color:#FFFFFF; background-color:#0070bd; padding:1px 3px 0 3px; float:right; cursor:pointer;}
                        
                        </style>

			<div style="display: none;" id='proppopUpDiv67"""+str(r)+"""'>
                        <form name="delete_disk_form" method="post" action="">
                        <h5>Delete """+k['name']+"""<span onclick="popup2('proppopUpDiv67"""+str(r)+"""')">X</span></h5>
                        <p class="popup">
                        <div style="border:#D1D1D1 1px solid; text-align:center; height:70px; margin-bottom:20px;">"""
                        if(add_san_img == "yes"):
                                print """Cannot Delete because the image is BUSY!<br/><br/>
                                <button class="buttonClass" type="button" name = 'local_action_but'  id = 'local_action_but' value = 'Update' style="float:right; margin:0px 150px 0 0; " onclick="popup2('proppopUpDiv67"""+str(r)+"""')" >Go Back</button>"""
                        else:
                                print """Are you sure you want to delete """+k['name']+"""?<br/><br/>
                        <button class="buttonClass" type="button" name = 'local_action_but'  id = 'local_action_but' value = 'Update' style="float:right; margin:0px 100px 0 0; " onclick="popup2('proppopUpDiv67"""+str(r)+"""')" >No</button>
                        <input type="hidden" name="hid_con_name" value='"""+k['lv_name']+"""'>
                        <input type="hidden" name="hid_img_name" value='"""+k['name']+"""'>
                        <button class="buttonClass" type="submit" name = 'delete_image'  id = 'delete_image' value = 'delete_image' style="float:right; margin:0 10px 0 0;" >Yes</button>"""

                        print """</div>
                        </p>
                        </form>
                        </div>


			<div style="display: none;" id='propopUpDiv55"""+str(r)+"""'>
                        <form name="delete_disk_form" method="post" action="">
                        <h5>Remove """+k['name']+""" from SAN<span onclick="popup2('propopUpDiv55"""+str(r)+"""')">X</span></h5>
                        <p class="popup">
                        <div style="border:#D1D1D1 1px solid; text-align:center; height:70px; margin-bottom:20px;">
                        Are you sure you want to remove """+k['name']+""" from SAN?<br/><br/>
                        <button class="buttonClass" type="button" name = 'local_action_but'  id = 'local_action_but' value = 'Update' style="float:right; margin:0px 100px 0 0; " onclick="popup2('propopUpDiv55"""+str(r)+"""')" >No</button>
                        <input type="hidden" name="delete_option_san" value='"""+img_san_name+':FIO'"""'>
                        <button class="buttonClass" type="submit" name = 'delete_san_but'  id = 'delete_san_but' value = 'delete_san_but' style="float:right; margin:0 10px 0 0;" >Yes</button>"""

                        print """</div>
                        </p>
                        </form>
                        </div>


                        <div style="display: none;" id="blanket2"></div>
                        <form name="delete_snap_form" method="post" action="iframe_all_disk_list.py#tabs-2">

                        <div style="display: none;" id='proppopUpDiv69"""+str(r)+"""'>
			<form name="add_to_san_form" method="POST" action="iframe_all_disk_list.py#tabs-2" >
                        <h5>Add """+k['name']+""" to SAN<span onclick="popup2('proppopUpDiv69"""+str(r)+"""')" style="cursor:pointer;">X</span></h5>
			<p class="popup">
                        <div style="border:#D1D1D1 1px solid; text-align:center; height:150px; margin-bottom:20px;">

			<table width="100%" style="text-align:center; padding:20px; ">

                        <tr>
                        <td align="left" width="45%">Enter Name</td>
                        <td align="left"><input type="text" class="textbox" name="san_name" style="width:187px;" /></td>
                        </tr>

                        <tr>
                        <td align="left" width="45%">Block Size</td>
                        <td align="left">
                        <div class="styled-select2">
                        <select name='select_block' id="select_block">
                        <option value='select-size'>Select Size</option>
                        <option>512</option>
                        <option>4096</option>
                        </select>
                        </div>
                        </td>
                        </tr>
                        <input type="hidden" name='select_disk' value='FIO' />
                        <input type="hidden" name='select_lv' value='"""+k["lv_name"]+"""' />
                        <input type="hidden" name='image_name' value='"""+k["name"]+"""' />

                        <tr>
                        <td align="left" width="45%"></td>
                        <td align="left">
                        <button class="buttonClass" style="float:right; margin:10px 20px 0 0;" type="submit" name = 'add_to_san_fio'  id = 'add_to_san_fio' value = 'add_to_san_fio'  >Add to SAN</button>
                        </td>
                        </tr>

                        </table>
                        </div>
                        </p>
                        </form>
              			 


                        </div>"""


                        print """<li """+border_bottom_img+""" onclick="return folder_click("""+str(r)+""", """+str(image_array_len)+""", """+str(t)+""");"><a>"""+k['name']+"""</a>

                        <div id='"""+str(r)+"""' style="display:none;">
                        <ul>
                        
                        <form name="smb_or_nfs" method="post" action="main.py?page=ss#tabs-2">"""
			if(add_san_img == "yes"):
                        	print """<li><a onclick="popup2('propopUpDiv55"""+str(r)+"""')" href="#">Remove from SAN</a></li>"""
			else:
                        	print """<li><a onclick="popup2('proppopUpDiv69"""+str(r)+"""')" href="#">Add to SAN</a></li>"""

                        print """<li><a onclick="popup2('proppopUpDiv67"""+str(r)+"""')" href="#">Delete</a></li>
                        </form>
                        </ul>
                        </div>

                        </li>"""
                        r=r+1

                print """


                </ul>

                </nav>


                """

	else:
		print """<div style="text-align:center; width:665px;">No Image Found!</div>"""


	print """</div>
	</div>
	</div>
	<p>&nbsp;</p>
	</div>
		
	"""
except Exception as e:
        disp_except.display_exception(e);
