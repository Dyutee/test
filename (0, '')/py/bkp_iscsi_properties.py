#!/usr/bin/python
import cgitb, sys, header, common_methods
cgitb.enable()

sys.path.append('/var/nasexe/storage')
import storage_op
import sys,os
from lvm_infos import *
from functions import *
import san_disk_funs

iscsi_status = common_methods.get_iscsi_status();

sys.path.append('/var/nasexe/')
import net_manage_newkernel as net_manage_bond

get_all_iface = net_manage_bond.get_all_ifaces_config()
        #print get_all_iface

if(get_all_iface["id"]==0):
	iface_info = get_all_iface["all_conf"]

target_list =''
display_create = ''
display_delete_target = ''
show_target = ''
initiator_list = ''
show_auth_target = ''
optionsstring = '';
target_select_delete_prop = ''

dd_val = 'None'
burst_length = '1048576'
hd_val = 'None'
idata_val = 'No'
init_val = 'No'
max_busrst_length = '1048576'
max_R2t = '32'
max_receive_data_segment = '1048576'
max_session = '0'
nop_interval = '30'
max_xmi_length  = '1048576'
qued_command = '32'
rsp_timeout = '90'
address_method ='PERIPHERAL'
enabled = '1'
per_portal ='1'
input_grouping ='auto'

random_target=san_disk_funs.get_iscsi_target_name()
remove_targets_list= san_disk_funs.iscsi_list_all_tgt()

select_targets=san_disk_funs.iscsi_list_all_tgt_att()

#----------------------ADD Initiator-----------------------------------#
if(header.form.getvalue('list_targets')):
	target_list = header.form.getvalue('list_targets')
	print "<script>location.href = 'main.py?page=prop_iscsi#tabs-1';</script>"
if(header.form.getvalue('iscsi_ips')):

	ini_target_list = header.form.getvalue('list_targets')
	add_ini = header.form.getvalue('all_portal')
	add_ips = header.form.getvalue('check_portal[]')
	checkall = header.form.getvalue('check_all_portal')
	get_ini_array = [];
	gets_initiator_list = san_disk_funs.iscsi_ini_list(ini_target_list)
	#print 'GET INI:'+str(gets_initiator_list)
	used_disks_name = san_disk_funs.iscsi_used_disks_tgt(ini_target_list)
	if(used_disks_name ==[]):
		 print"""<div id = 'id_trace_err'>"""
                 print "First add the Disk!"
                 print "</div>"
	else:
              	 #print "<script>location.href = 'main.py?page=iscsi_prop#tabs-1';</script>"
	#print used_disks_name
		for l in gets_initiator_list:
			#print 'L'+str(l)
			get_ini1 = l[:l.find('#') + 1]
			get_ini_array.append(get_ini1);
			#print 'INI2:'+str(get_ini_array)


		test_ini = add_ini + '#';
		test_ini = test_ini.strip();

		#print test_ini;
		#print get_ini_array;

		#print 'GET ARRAY'+str(get_ini_array)
		if(add_ini + '#' in get_ini_array):
			#print 'True'
			#print 'Error'

			print"""<div id = 'id_trace_err'>"""
			print "Duplicate Entry!"
			print "</div>"
		else:
			#rint 'True'
		#exit();
			add_ips = str(add_ips);
			add_ips = add_ips.replace('[', '');
			add_ips = add_ips.replace(']', '');
			add_ips = add_ips.replace("'", "");
			add_ips = add_ips.replace(' ', '');

			if (checkall == '*'):
				add_ips = '*';

			ini_ip_string = add_ini + '#' + add_ips;

			#print ini_ip_string;

			check_add_ips = isinstance(add_ips, str)
			#print check_add_ips
			if(check_add_ips == True):
				
				add_initiator=san_disk_funs.iscsi_ini_add(ini_target_list,ini_ip_string)

			#else:
			#       add_ips = set(add_ips)
			#       for ips_val in add_ips:
			#               add_initiator=san_disk_funs.iscsi_ini_add(ini_target_list,ini_ip_string)
			#add_initiator=san_disk_funs.iscsi_ini_add(ini_target_list,ini_ip_string)
				if(add_initiator == True):
					print"""<div id = 'id_trace'>"""
					print "Successfully Added the Initiator!"
					print "</div>"
					print "<script>location.href = 'main.py?page=prop_iscsi#tabs-1';</script>"
				else:
					print"""<div id = 'id_trace_err'>"""
					print "Error occured while Adding !"
					print "</div>"
					print "<script>location.href = 'main.py?page=prop_iscsi#tabs-1';</script>"

#---------------------------------End--------------------------------#
#-------------------Check Session is Active or Not--------------------
ses_ip = ''

#-------------------End-----------------------------------------------

#---------------------- Delete Initiator------------------------------#
if(header.form.getvalue('choose_list')):
	show_target = header.form.getvalue('choose_list')

	#-------------Check Session is Active or not---------------#
        sesion_tar =san_disk_funs.iscsi_session(show_target)
	#------------------End-------------------------------------#

	print "<script>location.href = 'main.py?page=prop_iscsi#tabs-2';</script>"
	initiator_list = san_disk_funs.iscsi_ini_list(show_target)

if(header.form.getvalue('delete_initiator')):
	show_list_target = header.form.getvalue('choose_list')

	#---------------Check Session is Active or not--------------#
        sesion_tar =san_disk_funs.iscsi_session(show_list_target)
	#-----------------End---------------------------------------#

	ini_name = header.form.getvalue('initr_list')
	#abc = []
	check_used_disk = san_disk_funs.iscsi_used_disks_tgt(show_list_target)

	if(sesion_tar ==[]):
		remove_ini = san_disk_funs.iscsi_ini_del(show_list_target,ini_name)
		if(remove_ini == True):
			
			print"""<div id = 'id_trace'>"""
			print "Successfully Deleted the Initiator!"
			print "</div>"
			print "<script>location.href = 'main.py?page=prop_iscsi#tabs-2';</script>"
		else:

			print"""<div id = 'id_trace_err'>"""
			print "Error Occurred while deleting Initiator!"
			print "</div>"
			print "<script>location.href = 'main.py?page=prop_iscsi#tabs-2';</script>"
	else:
		print"""<div id = 'id_trace_err'>"""
		print "First logout from Session !"
		print "</div>"
		print "<script>location.href = 'main.py?page=prop_iscsi#tabs-2';</script>"
#--------------------------------End-----------------------------#
#-----------------------Authentication User----------------------#
optionsstring = '';
if(header.form.getvalue('auth_list')):
	show_auth_target = header.form.getvalue('auth_list')
	
	print "<script>location.href = 'main.py?page=prop_iscsi#tabs-4';</script>"

	for target_list_all in select_targets:
		#print target_list_all

		if(target_list_all['target']==show_auth_target):
			for key_list in target_list_all:
				if str(key_list).__contains__("IncomingUser"):
					#print key_list + ":" + target_list_all[key_list];
					#print 'Incoming User:'+str(incoming_user_list) 
					target_get_list = target_list_all[key_list]
					#print target_get_list
					target_get_list = target_get_list.strip();
					replace_key = target_get_list.replace(' ', '/')
					if (replace_key != ''):
                                        	optionsstring += "<option value = '" + replace_key + "' selected>" + replace_key + "</option>";

                                        print replace_key



if(header.form.getvalue('iscsi_user')):
	show_auth_target = header.form.getvalue('auth_list')
	print "<script>location.href = 'main.py?page=prop_iscsi#tabs-4';</script>"
	incoming_usr_list = []
	incoming_usr_list = header.form.getvalue('in_usr_pwd_list[]')

	checkforbraces = str(incoming_usr_list).find('[');

	if (checkforbraces < 0):
		iu = header.form.getvalue('in_usr_pwd_list[]');

		iu = iu.replace('/', ' ');
		iu = "'" + iu + "'";

                iu = 'IncomingUser=' + iu;

		#print iu + '<BR>'

		addincominguser = san_disk_funs.iscsi_set_tgt_attr(target=show_auth_target,attr=iu)
		if(addincominguser == True):
			print"""<div id = 'id_trace'>"""
			print "Successfully Add the Incoming User!"
			print "</div>"
			print "<script>location.href = 'main.py?page=prop_iscsi#tabs-4';</script>"
		else:
			print"""<div id = 'id_trace_err'>"""
			print "Error occured while Adding !"
			print "</div>"
			print "<script>location.href = 'main.py?page=prop_iscsi#tabs-4';</script>"
#------------------------------End-------------------------------#
#-----------------------Target Properties------------------------#

if(header.form.getvalue('target_prop_delete')):
	target_select_delete_prop = header.form.getvalue('target_prop_delete')
	print "<script>location.href = 'main.py?page=prop_iscsi#tabs-5';</script>"
if(header.form.getvalue('iscsi_props')):

	target_select_prop_name = header.form.getvalue('target_prop_delete')
	data_digest = header.form.getvalue('ddigest')
	burst_len = header.form.getvalue('fbl')
	header_dig = header.form.getvalue('hd')
	im_data = header.form.getvalue('idata')
	in_r2t  = header.form.getvalue('initr2t')
	max_burst_len = header.form.getvalue('mbl')
	max_out = header.form.getvalue('mor2t')
	max_receive_data = header.form.getvalue('mrdsl')
	max_sess = header.form.getvalue('max_conn')
	max_xmit = header.form.getvalue('medsl')
	nop_intervals = header.form.getvalue('nopinterval')
	qued_comm = header.form.getvalue('qc')
	rsp_time = header.form.getvalue('rspto')
	attrstring = '';

	iscsi_prop_name = 'DataDigest='+str(data_digest)
	blength         = 'FirstBurstLength='+str(burst_len);
	headerdigest = 'HeaderDigest='+str(header_dig)
	imd_data = 'ImmediateData='+str(im_data)
	in_r2 = 'InitialR2T='+str(in_r2t)
	max_bursts_len = 'MaxBurstLength='+str(max_burst_len)
	max_receive_d = 'MaxRecvDataSegmentLength='+str(max_receive_data)
	max_sess_n = 'MaxSessions='+str(max_sess)
	max_xmit_len = 'MaxXmitDataSegmentLength='+str(max_xmit)
	nop_inter = 'NopInTimeout='+str(nop_intervals)
	qued_con = 'QueuedCommands='+str(qued_comm)
	rsp_times = 'RspTimeout=' +str(rsp_time)

	attrstring = '"'+ iscsi_prop_name + ','+ blength +','+headerdigest +','+ in_r2 + ',' + max_bursts_len + ','+ max_receive_d + ',' + max_sess_n + ',' + max_xmit_len + ',' + nop_inter + ',' + qued_con + ',' + rsp_times +'"'
	target_set_attribute = san_disk_funs.iscsi_set_tgt_attr(target=target_select_prop_name, attr=attrstring)

	if(target_set_attribute == True):
		print"""<div id = 'id_trace'>"""
		print "Successfully Set the Target!"
		print "</div>"
		print "<script>location.href = 'main.py?page=prop_iscsi#tabs-5';</script>"
	else:
		print"""<div id = 'id_trace_err'>"""
		print "Error occured while Set the Target !"
		print "</div>"
		print "<script>location.href = 'main.py?page=prop_iscsi#tabs-5';</script>"
#--------------------------------End-------------------------------------------#

import left_nav

if (iscsi_status > 0):

	print
	print """
	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer">
		<div class="insidepage-heading">I-Scsi >> <span class="content">I-Scsi Configuration</span></div>
		<!--tab srt-->
		<div class="searchresult-container">
		  <div class="infoheader">
		    <div id="tabs">
		      <ul>
			<li><a href="#tabs-1">Add Initiator</a></li>
			<li><a href="#tabs-2">Delete Initiator</a></li>
			<li><a href="#tabs-3">Initiator List</a></li>
			<li><a href="#tabs-4">Authentication</a></li>
			<li><a href="#tabs-5">Target Properties</a></li>
		      </ul>
		      <div id="tabs-1">

		<!--form container starts here-->
		<div class="form-container">
		  <div class="topinputwrap-heading">Add Initiator </div>
		  <div class="inputwrap">
		    <div class="formrightside-content">
		<form name = 'add_ips_form' method = 'POST'>

		  <table width = "685" border = "0" cellspacing = "0" cellpadding = "0">
								<tr>
									<td width = '23%' height = "35px" >
										Choose a target
									</td>
									<td>
			<div class="styled-select2" style="width:518px;">
			<select name = 'list_targets' class = 'input' style = 'width:103%;'>
			<option value = 'list_ini_val'>Select Target</option>"""

	for z in remove_targets_list:
		print """<option value = '"""+z+"""'"""
		if(target_list !=''):
			if(target_list == z):
				print """selected = 'selected'"""
		print """>"""+z+"""</option>"""



	print """</select></div>
	</td>
	</tr>"""


	print"""

	<tr>
							<td width = '30%' class = "table_heading" height = "35px" valign = "middle">
								Enter initiator name
							</td>
							<td class = "table_content" height = "35px" valign = "middle">
								<input id = 'id_add_props' class = 'textbox' type = 'text' name = 'all_portal' style = 'width: 96%;'>
							</td>
						</tr>


						<tr>

	<td>
						<input type= "hidden" name = "ini_list" value= '"""+target_list+"""'>
						</td>
						</tr>

	<tr>
							<td height = "35px" valign = "middle" style ="color:Black;font-family:serif;">
								Check the portal(s)
							</td>
	</tr>
	</table>
	<table width = "685" border = "1" cellspacing = "0" cellpadding = "0" style="border-style:ridge;">
	<tr style = 'background-color:#999999; font-weight: bold;'>
									<td height = "30px" valign = "middle" style = 'color: #FFF;text-align:center;'>
										Device
									</td>
									<td height = "30px" valign = "middle" style = 'color: #FFF;text-align:center;'>
										IP
									</td>
									<td height = "30px" valign = "middle" style = 'color: #FFF;text-align:center;'>
										Status
									</td>

									<td height = "30px" valign = "middle" style = 'color: #FFF;text-align:center;'>
										Select
									</td>
								</tr>"""


	for ip_info in iface_info:
		#print ip_info
		device_info = ip_info['iface']
		#print device_info
		ip_information = ip_info['address']
		status_info = ip_info['status']

		#print ip_information +'<br/>'

		print"""<tr>
		<td style = "text-align:center;">

		"""+device_info+"""
		</td>
		<td style = "text-align:center;">

		"""+ip_information+""" 
		</td>
		<td style = "text-align:center;">
		"""+status_info+"""
		</td>
		<td height = "35px" valign = "middle" style = "text-align:center;">
		<input type = 'checkbox' name = 'check_portal[]' value = '""" + ip_information + """' onclick = 'return uncheck_all();'>
		</td>
		</tr>

	"""
	print"""</table>


	<table>
	<tr>
	<td colspan = "2">
	<input type = 'checkbox' name = 'check_all_portal' value = '*' onclick = 'return uncheck_all();'><B>Add All</B>
	<div>
	<td style="width: 5%; padding-left: 39%;">
	<button class = 'buttonClass' type="submit" name = 'iscsi_ips' value = 'Apply' onclick = 'return validate_add_initiator();'>Apply</button></td></div>
	</td></tr></table>
						


	</form>"""


	print"""
		   </div>
		  </div>
		</div>
		<!--form container ends here-->
		<p>&nbsp;</p>
		      </div>
		      <div id="tabs-2">
		<!--form container starts here-->
		<div class="form-container">
		  <div class="topinputwrap-heading">Delete Initiator</div>
		  <div class="inputwrap">
		<div class="formrightside-content">
		<form name = 'del_initr_from_target' action = '#' method = 'POST'>
		<table width = "685" border = "0" cellspacing = "0" cellpadding = "0" id = "id_del_ini">
											<tr>
											<td width = '23%' height = "35px" valign = "middle">
												Choose Target
											</td>
											<td class = "table_content" height = "35px" valign = "middle">
			 <div class="styled-select2" style="width:518px;">
			<select class = 'input' name = 'choose_list' onchange='this.form.submit()' style = 'width:103%;'>

			<option value = 'choose_list_val'>Select Target</option>"""

	for choose_list in remove_targets_list:
		print """<option value = '"""+choose_list+"""'"""
		if(show_target !=''):
			if(show_target == choose_list):
				print """selected = 'selected'"""
		print """>"""+choose_list+"""</option>"""

	print"""</select></div>
	</td>
	</tr>"""

	print"""
										<tr>
											<td width = '23%' class = "table_heading" height = "35px" valign = "middle">
												Choose initiator
											</td>
											<td class = "table_content" height = "35px" valign = "middle">
			<div class="styled-select2" style="width:518px;">
			<select class = 'input' name = 'initr_list' style = 'width:103%;'>
			<option value = 'initr_list_val'>Select Initiator</option>"""

	for ini_list in initiator_list:
		#if(ini_list == '*#*'):
		#	ini_list = '*'
		
		#	print """<option value = '"""+ini_list+"""'>"""+ini_list+"""</option>"""
		#else:
			
		print """<option value = '"""+ini_list+"""'>"""+ini_list+"""</option>"""
		

	print"""</select></div>
	</td>
	</tr>"""
	print"""<tr>
	<td>
	<div>
	<td style="float:right;"> 
	<button class = 'buttonClass' type="submit" name = 'delete_initiator' value = 'Remove initiator' onclick = 'return validate_remove_ini();'>Delete</button>
	</td>
	</div>
	</tr>"""
	print"""</table>
	</form>
	"""




	print"""	</div>
		</div>
		</div>
		<!--form container ends here-->
		<p>&nbsp;</p>
		      </div>

		  <div id="tabs-3">
		<!--form container starts here-->
		<div class="form-container">
		  <div class="topinputwrap-heading">Initiator List</div>
		  <div class="inputwrap">

		<div class="formrightside-content">
		<form name = 'list_initr_from_target' method = 'POST'>

		 <table width = "685" cellspacing = "1" cellpadding = "0" border = "1" id = 'id_list_info' style="border-style: inset;">
							<tr style = 'background-color:#999999;font-weight: bold;'>
							<td height = "35px" valign = "middle" style = 'color: #FFF;'>Target</td>
							<td height = "35px" valign = "middle" style = 'color: #FFF;'>Disks</td>
							<td height = "35px" valign = "middle" style = 'color: #FFF;'>Initiators</td>
						</tr>"""


	if(remove_targets_list!=[]):
		for tar_list_info in remove_targets_list:

			print"""<tr>
			<td height = "35px" valign = "middle" style="font-family: Times New Roman;">
									 

			 """+tar_list_info+"""
			</td>&nbsp;&nbsp;"""

			print"""<td height = "35px" valign = "middle" style="text-align:center;">"""

			used_disks_info = san_disk_funs.iscsi_used_disks_tgt(tar_list_info)

			replace_disk0 = str(used_disks_info).replace('[]', '')
			replace_disk1 = str(replace_disk0).replace('[', '')
			replace_disk2 = str(replace_disk1).replace(']', '')
			used_disk_info = str(replace_disk2).replace("'", '')
			print used_disk_info
			#for disks_ini_list in alldisk:
				#print disks_ini_list
			#       print""" """+disks_ini_list+"""<br>"""
			print"""</td>"""

			getinilist = san_disk_funs.iscsi_ini_list(tar_list_info)
			#print getinilist
			replace_get_ini = str(getinilist).replace('[]', '')
			#print 'rep1:'+replace_get_ini
			#print '<br/>'
			get_initiator = str(replace_get_ini).replace('[', '')
			get_initiator1 = str(get_initiator).replace(']', '')
			get_initiator2 = str(get_initiator1).replace("'", '')
			#print 'GET I:'+ get_initiator2
			get_initiator3 = str(get_initiator2).replace('*', 'Access for all ip(*)' )

			get_initiator3 = get_initiator3.replace(',', '<BR>');
			get_initiator4= get_initiator3.replace('#', ' through ')
			
			get_initiator5 = get_initiator4.replace('Access for all ip(*) through Access for all ip(*)', 'Access for all ip(*)') 
			print"""
			<td height = "35px" valign = "middle" style="width:25%;">"""
			print""" """+str(get_initiator5)+"""
			</td>"""


			print"""</tr>"""
	else:
		print"""<tr>
		<td colspan = '3' align = 'center' height="50px;">
		<marquee behavior="alternate" direction= "right"><b><font size="5">No Information is available</font></b></marquee>
		</td>
		</tr>"""

	print"""</table></form>
		</div>
		</div>
		</div>
		<!--form container ends here-->
		<p>&nbsp;</p>
		      </div>
		 <div id="tabs-4">
		<!--form container starts here-->
		<div class="form-container">
		  <div class="topinputwrap-heading">Authentication</div>
		  <div class="inputwrap">
		<div class="formrightside-content">
		<form name = 'add_users' method = 'POST'>
		<table width = "685" border = "0" cellspacing = "0" cellpadding = "0" id = 'id_auth_prop'>

		<tr>
			<td width = '23%' class = "table_heading" height = "35px" valign = "middle">
			Choose Target
			</td>
			<td class = "table_content" height = "35px" valign = "middle">
			<div class="styled-select2" style="width:518px;">
			<select class = 'input' name = 'auth_list' onchange='this.form.submit()' onclick = 'document.getElementById("id_remove_users").disabled = false;' style = 'width:531px;'>

			<option value = 'auth_list_val'>Select Target</option>"""

	for auth_target in remove_targets_list:
		print """<option value = '"""+auth_target+"""'"""
		if(show_auth_target !=''):
			if(show_auth_target == auth_target):
				print """selected = 'selected'"""
		print """>"""+auth_target+"""</option>"""

	print"""</select></div>
		</td>
		</tr>"""

	print"""
						
						<tr>
							<td colspan = '2' class = "table_heading" height = "35px" valign = "middle">
								<font color="Black"><B>Incoming user:</B></font>
							</td>
						</tr>
						<tr>
							<td class = "table_heading" height = "35px" valign = "middle">
								Username
							</td>
							<td class = "table_content" height = "35px" valign = "middle">
								<input id = 'id_incoming_usr' class = "textbox" type = 'text' name = 'in_user' style = 'width: 80%;'>
							</td>
						</tr>
						<tr>
							<td class = "table_heading" height = "35px" valign = "middle">
								Password
							</td>
							<td class = "table_content" height = "35px" valign = "middle">
								<input id = 'id_incoming_pwd' class = 'textbox' type = 'password' name = 'in_pwd' style = 'width: 80%;'>&nbsp;<a style = 'font-weight: bold; font: 13px Arial; text-decoration: none;' href = '#zzz' onclick = 'return add_usr_pwd(document.getElementById("id_incoming_usr").value, document.getElementById("id_incoming_pwd").value, "IN");'><img style = 'border: 1px solid #BDBDBD;' src = '../images/plus.png' /></a>
							</td>
						</tr>


	<tr>
							<td>
							</td>
							<td class = "table_content" height = "35px" valign = "middle">
								<select id = 'id_in_users_array' class = 'input' name = 'in_usr_pwd_list[]' style = 'width: 90%; height: 100px;' multiple>"""
	if (optionsstring != ''):
		print optionsstring;


	print """
							
								</select><BR>
								<!--<a style = 'color: #424242; font-weight: bold; text-decoration: none; font-style: italic;' href = '#zzz' onclick = 'return remove_users("IN");'>Remove user(s)</a> <?= $remove_users_wait1 ?>-->
	<button class = 'buttonClass' type="submit" name = 'remove_user'  id = 'id_remove_users' value = 'Remove User' onclick = 'return remove_users("IN");'>Remove User</button>

							</td>
						</tr>


	<tr>
							<td colspan = '3' align = 'right'>

	<button class = 'buttonClass' type='submit' name = 'iscsi_user' value = 'Apply' onclick = 'return validate_iscsi_users();'>Apply</button>
							</td>
						</tr>





	"""




	print"""
	</table></form>


		</div>
		</div>
		</div>
		<!--form container ends here-->
		<p>&nbsp;</p>
		      </div>
		 <div id="tabs-5">
		<!--form container starts here-->
		<div class="form-container">
		  <div class="topinputwrap-heading">Target Properties</div>
		  <div class="inputwrap">
		<div class="formrightside-content">
		<form name = 'add_properties1' method = 'POST'>
		<table width = "685" border = "0" cellspacing = "0" cellpadding = "0" name = 'disp_tables' id = 'id_target_properties'>

	<tr>
			<td width = '23%' class = "table_heading" height = "35px" valign = "middle">
			Select target
			</td>
			<td class = "table_content" height = "35px" valign = "middle">
			<div class="styled-select2" style="width:518px;">
			<select class = 'input' name = 'target_prop_delete' onchange = 'this.form.submit();' style = 'width:531px;'>
			<option value='prop_val'>Select Target</option>"""

	for  prop_target_det in remove_targets_list:
		print """<option value = '"""+prop_target_det+"""'"""
		if(target_select_delete_prop !=''):
			if(target_select_delete_prop == prop_target_det):
				print """selected = 'selected'"""
		print """>"""+prop_target_det+"""</option>"""


	print"""</select></div>
	</td>
	</tr>"""

	if (select_targets != [{}]):
		for target_prop in select_targets:
			#print 'tar1:'+str(target_prop['target'])
			#print '<br/>'
			#print 'tar2:'+str(target_select_delete_prop)

			if(target_prop['target']==target_select_delete_prop):
				#print target_prop
				dd_val = target_prop['DataDigest']
				#print dd_val
				burst_length = target_prop['FirstBurstLength']
				#print burst_length
				hd_val = target_prop['HeaderDigest']
				idata_val = target_prop['ImmediateData']
				init_val = target_prop['InitialR2T']
				max_busrst_length = target_prop['MaxBurstLength']
				max_R2t = target_prop['MaxOutstandingR2T']
				max_receive_data_segment = target_prop['MaxRecvDataSegmentLength']
				max_session = target_prop['MaxSessions']
				nop_interval = target_prop['NopInInterval']
				max_xmi_length = target_prop['MaxXmitDataSegmentLength']
				qued_command = target_prop['QueuedCommands']
				rsp_timeout = target_prop['RspTimeout']
				address_method = target_prop['addr_method']
				enabled = target_prop['enabled']
				per_portal= target_prop['per_portal_acl']
				input_grouping = target_prop['io_grouping_type']

	print"""<tr>

			<td width = '40%' class = "table_heading" height = "35px" valign = "middle">
				Data digest
			</td>
			<td class = "table_content" height = "35px" valign = "middle">
				<div class="styled-select2" style="width:118px;">
				<select class = 'input' name = 'ddigest'>"""

	if (dd_val == 'None'):

		print"""<option value = 'None' selected>None</option>""";
		print"""<option value = 'CRC32C'>CRC32C</option>""";


	elif (dd_val == 'CRC32C'):

		print"""<option value = 'None'>None</option>""";
		print"""<option value = 'CRC32C' selected>CRC32C</option>""";


	else:

		print"""<option value = 'None' selected>None</option>""";
		print"""<option value = 'CRC32C'>CRC32C</option>""";


	print"""</select></div>
	</td>
	</tr>"""
	print"""<tr>
		<td class = "table_heading" height = "35px" valign = "middle">
			First burst length
		</td>
		<td class = "table_content" height = "35px" valign = "middle">
			<input class = 'textbox' type = 'text' name = 'fbl' value = '"""+burst_length+"""'>
		</td>
		</tr>"""
	print"""<tr>
		<td class = "table_heading" height = "35px" valign = "middle">
			Header digest
		</td>
		<td class = "table_content" height = "35px" valign = "middle">
			<div class="styled-select2" style="width:118px;">
			<select class = 'input' name = 'hd'>"""
	if (hd_val == 'None'):

		print"""<option value = 'None' selected>None</option>""";
		print"""<option value = 'CRC32C'>CRC32C</option>""";

	elif (hd_val == 'CRC32C'):

		print"""<option value = 'None'>None</option>""";
		print"""<option value = 'CRC32C' selected>CRC32C</option>""";


	else:

		print"""<option value = 'None' selected>None</option>""";
		print"""<option value = 'CRC32C'>CRC32C</option>""";

		print"""</select></div>
		</td>
		</tr>"""

	print"""<tr>
			<td class = "table_heading" height = "35px" valign = "middle">
				Immediate data
			</td>
			<td class = "table_content" height = "35px" valign = "middle">
				<div class="styled-select2" style="width:118px;">
				<select class = 'input' name = 'idata'>"""

	if (idata_val == 'Yes' or idata_val == ''):

		print"""<option value = 'Yes' selected>Yes</option>""";
		print"""<option value = 'No'>No</option>""";


	else:

		print"""<option value = 'Yes'>Yes</option>""";
		print"""<option value = 'No' selected>No</option>""";


	print"""</select></div>
	</td>
	</tr>"""
	print"""<tr>
	<td class = "table_heading" height = "35px" valign = "middle">
		Initial R2T
	</td>
	<td class = "table_content" height = "35px" valign = "middle">
		<div class="styled-select2" style="width:118px;">
		<select class = 'input' name = 'initr2t'>"""

	if (init_val == 'No' or init_val == ''):
		
		print"""<option value = 'Yes'>Yes</option>""";
		print"""<option value = 'No' selected>No</option>""";


	else:

		print"""<option value = 'Yes' selected>Yes</option>""";
		print"""<option value = 'No'>No</option>""";

	print"""</select></div>
	</td>
	</tr>"""
	print"""<tr>
			<td class = "table_heading" height = "35px" valign = "middle">
				Max burst length
			</td>
			<td class = "table_content" height = "35px" valign = "middle">
				<input class = 'textbox' type = 'text' name = 'mbl' value = '"""+max_busrst_length+"""'>
			</td>
			</tr>
			<tr>
			<td class = "table_heading" height = "35px" valign = "middle">
				Max outstanding R2T
			</td>
			<td class = "table_content" height = "35px" valign = "middle">
				<input class = 'textbox' type = 'text' name = 'mor2t' value = '"""+max_R2t+"""'>
			</td>
			</tr>
			<tr>
			<td class = "table_heading" height = "35px" valign = "middle">
				Max recv. data segment length
			</td>
			<td class = "table_content" height = "35px" valign = "middle">
				<input class = 'textbox' type = 'text' name = 'mrdsl' value = '"""+max_receive_data_segment+"""'>
			</td>
			</tr>
			<tr>
			<td class = "table_heading" height = "35px" valign = "middle">

		 Max sessions
			</td>
			<td class = "table_content" height = "35px" valign = "middle">
				<input class = 'textbox' type = 'text' name = 'max_conn' value = '"""+max_session+"""'>
			</td>
			</tr>
			<tr>
			<td class = "table_heading" height = "35px" valign = "middle">
				Max xmit data segment length
			</td>
			<td class = "table_content" height = "35px" valign = "middle">
				<input class = 'textbox' type = 'text' name = 'medsl' value = '"""+max_xmi_length+"""'>
			</td>
			</tr>
			<tr>
			<td class = "table_heading" height = "35px" valign = "middle">
				Nop in interval
			</td>
			<td class = "table_content" height = "35px" valign = "middle">
				<input class = 'textbox' type = 'text' name = 'nopinterval' value = '"""+nop_interval+"""'>
			</td>
			</tr>
			<tr>
			<td class = "table_heading" height = "35px" valign = "middle">
				Queued commands
			</td>
			<td class = "table_content" height = "35px" valign = "middle">
				<input class = 'textbox' type = 'text' name = 'qc' value = '"""+qued_command+"""'>
			</td>
			</tr>
			<tr>
			<td class = "table_heading" height = "35px" valign = "middle">
				RSP timeout
	</td>
			<td class = "table_content" height = "35px" valign = "middle">
				<input class = 'textbox' type = 'text' name = 'rspto' value = '"""+rsp_timeout+"""'>
			</td>
			</tr>

			<tr>
			<td class = "table_heading" height = "35px" valign = "middle">
				Address Method
			</td>
			<td class = "table_content" height = "35px" valign = "middle">
				<input class = 'textbox' type = 'text' name = 'addr_method' value = '"""+address_method+"""' readonly>
			</td>
			</tr>

			<tr>
			<td class = "table_heading" height = "35px" valign = "middle">
				Enabled
			</td>
			<td class = "table_content" height = "35px" valign = "middle">
				<input class = 'textbox' type = 'text' name = 'enab' value = '"""+enabled+"""' readonly>
			</td>
			</tr>

			<tr>
			<td class = "table_heading" height = "35px" valign = "middle">
				Per Portal
			</td>
			<td class = "table_content" height = "35px" valign = "middle">
				<input class = 'textbox' type = 'text' name = 'port' value = '"""+per_portal+"""' readonly>
			</td>
	</tr>


			<tr>
			<td class = "table_heading" height = "35px" valign = "middle">
				Io Grouping
			</td>
			<td class = "table_content" height = "35px" valign = "middle">
				<input class = 'textbox' type = 'text' name = 'port' value = '"""+input_grouping+"""' readonly>
			</td>
			</tr>

	<tr>
	<td>
	<div>
	<td style="float:right;">
	<button class = 'buttonClass' type="submit" name = 'iscsi_props' value = 'Apply' onclick = 'return validate_iscsi_props_nw();'>Apply</button></td>
	<!--<button class = 'buttonClass' type="submit" name = 'iscsi_props' value = 'Apply' onclick = 'return validate_iscsi_props(this.form.name, this.form.elements.length);'>Apply</button></td>-->
	</div>
	</td>
	</tr>

	"""

	print"""
	</table></form>
		</div>
		</div>
		</div></div>
		<!--form container ends here-->
		<p>&nbsp;</p>
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
	</div>"""

else:
	print "<div style = 'margin-top: 10%; margin-bottom: 10%; margin-left: auto; margin-right: auto; text-align: center; vertical-align: center; color: darkred; width: 65%; font: 16px Arial;'>Check the 'Enable/Disable i-SCSI' option in Maintenance -><a href ='main.py?page=sr'style ='text-decoration:underline;'>Services</a>.</div>"

print"""
<!--body wrapper end-->
</body>
</html>
"""
