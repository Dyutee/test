#!/usr/bin/python
import cgitb, sys, string, common_methods, include_files, cgi, commands, os
cgitb.enable()
form = cgi.FieldStorage()

sys.path.append('../modules/')
import disp_except;

try:
	#print 'Content-Type: text/html'

	#########################################
	############# import modules ############
	#########################################
	sys.path.append('/var/nasexe/python/')
	import manage_users
	import authentication
	import tools
	from tools import db

	#########################################
	######### Check HA Status Start #########
	#########################################
	check_ha = tools.check_ha()
	sys_node_name = tools.get_ha_nodename()
	if(sys_node_name == "node1"):
		other_node = "node2"
		this_node = "node1"
		show_tn = "Node1"
		show_on = "Node2"
	else:
		other_node = "node1"
		this_node = "node22"
		show_tn = "Node2"
		show_on = "Node1"

	query="select * from network_ifaces where (name='eth1' and node='"+other_node+"')"
	status=db.sql_execute(query)
	for x in status["output"]:
		other_node_ip = x["ip"]

	query2="select * from network_ifaces where (name='eth1' and node='"+this_node+"')"
	status2=db.sql_execute(query2)
	for x in status2["output"]:
		this_node_ip = x["ip"]
	#########################################
	########## Check HA Status End ##########
	#########################################

	#########################################
	############# Default Values ############
	#########################################
	get_sel_user = ''
	get_sel_group = ''
	sub_user_group = {'group': '', 'user_name': '', 'sub_groups': []}
	display_grp_list = "none"
	display_usr_list = "none"
	get_re_usr_list_mod = ''

	#########################################
	######## Force Create User Start ########
	#########################################
	if(form.getvalue("force_create_user")):
		username = form.getvalue("hid_username")
		password = form.getvalue("hid_password")
		if((username != None) and (password != None)):
			new_user ={"user_name":username,"passwd":password,"group":"USER","sub_groups":[]}
			create_user = manage_users.create_user(new_user,force=True)
			if(create_user["id"] == 0):
				if(check_ha == True):
					print """<script>location.href = 'https://"""+other_node_ip+"""/fs4/py/othernodecmd.py?act=force_create_user&username="""+str(username)+"""&password="""+password+"""'</script>"""
				print"""<div id = 'id_trace'>"""
				print create_user["desc"]
				print "</div>"
				logstatus = common_methods.sendtologs('Success', 'Succeffully Added '+username+' in User', 'user_maintenance.py', status['desc']);
			
			else:
				print"""<div id = 'id_trace_err' >"""
				print create_user["desc"]
				print "</div>"
				logstatus = common_methods.sendtologs('Error', 'Error Occurred while Adding '+username+'in User', 'user_maintenance.py', create_user['desc']);
	#########################################
	######### Force Create User End #########
	#########################################

	#########################################
	########### Create User Start ###########
	#########################################
	if(form.getvalue("create_users")):
		username = form.getvalue("username")
		password = form.getvalue("password")
		new_user ={"user_name":username,"passwd":password,"group":"USER","sub_groups":[]}
		create_user = manage_users.create_user(new_user)
		
		if(create_user["id"] == 0):
			if(check_ha == True):
				print """<script>location.href = 'https://"""+other_node_ip+"""/fs4/py/othernodecmd.py?act=create_user&username="""+str(username)+"""&password="""+password+"""'</script>"""

			print"""<div id = 'id_trace'>"""
			print create_user["desc"]
			print "</div>"
			logstatus = common_methods.sendtologs('Success', 'Succeffully Added '+username+' in User', 'user_maintenance.py', status['desc']);
		elif(create_user["id"] == 3):
			print """
			<style>
			#popUpDiv1 {position: fixed; background-color: #fff; min-width: 400px; z-index: 9002; padding: 5px; top:20%; left:35%;}
			#popUpDiv1 h5{width:100%; font-size:15px; color:#0070bd; text-align:center; font-weight:bold;}
			#popUpDiv1 span{ color:#FFFFFF; background-color:#0070bd; padding:1px 3px 0 3px; float:right; cursor:pointer;}
			</style>

	
			<div style="display: block;" id="blanket"></div>
			<div style="display: block;" id='popUpDiv1'>
			<h5>Alert Box <span onclick="popup('popUpDiv1')">X</span></h5>
			<p class="popup">
			User <strong>"""+username+"""</strong> already exists. Do you want to re-create this user?<br/><br/>
			<form name="force_cr_user_form" method="post" action="" >
			<input type="hidden" name="hid_username" value='"""+str(username)+"""' />
			<input type="hidden" name="hid_password" value='"""+str(password)+"""' />
			<button class="buttonClass" type="button" name = 'local_action_but'  id = 'local_action_but' value = 'Update' style="float:right; margin:0px 150px 20px 0; font-size:12px; " onclick="popup('popUpDiv1')" >No</button>
			<button class="buttonClass" type="submit" name = 'force_create_user'  id = 'force_create_user' value = 'force_create_user' style="float:right; font-size:12px;" >Yes</button>

			</form>
			</p>
			</div>
			"""

		else:
			print"""<div id = 'id_trace_err' >"""
			print create_user["desc"]
			print "</div>"
			logstatus = common_methods.sendtologs('Error', 'Error Occurred while Adding '+username+'in User', 'user_maintenance.py', create_user['desc']);
	#########################################
	############ Create User End ############
	#########################################

	#########################################
	########## Create Group Start ###########
	#########################################
	if(form.getvalue("create_group")):
		group = form.getvalue("group")
		create_new_group = manage_users.add_group(group)
		
		if(create_new_group["id"] == 0):
			if(check_ha == True):
				print """<script>location.href = 'https://"""+other_node_ip+"""/fs4/py/othernodecmd.py?act=create_group&group="""+str(group)+"""'</script>"""
			print"""<div id = 'id_trace'>"""
			print create_new_group["desc"]
			print "</div>"
			logstatus = common_methods.sendtologs('Success', 'Succeffully Added '+group+' in Group', 'user_maintenance.py', create_new_group['desc']);

		else:
			print"""<div id = 'id_trace_err' >"""
			print create_new_group["desc"]
			print "</div>"
			logstatus = common_methods.sendtologs('Error', 'Error Occurred while  Creating '+group+'in Group', 'user_maintenance.py', create_new_group['desc']);
	#########################################
	########### Create Group End ############
	#########################################

	#########################################
	########### Manage User Start ###########
	#########################################
	if(form.getvalue("user_list")):
		get_sel_user = form.getvalue("user_list")
		if(get_sel_user != "select-user"):
			get_user_group = manage_users.get_user_info(get_sel_user)
			sub_user_group = get_user_group["user_info"]
			display_grp_list = "block"
	#########################################
	############ Manage User End ############
	#########################################

	#########################################
	########## Manage Group Start ###########
	#########################################
	if(form.getvalue("re_grp_list")):
		get_sel_group = form.getvalue("re_grp_list")
		if(get_sel_group != "select-group"):
			get_re_usr_list = manage_users.get_users_of_group(get_sel_group)
			if get_re_usr_list["id"] == 0:
				get_re_usr_list_mod = get_re_usr_list["users"]
			else:
				get_re_usr_list_mod = {'id': 2, 'users':[]} 
			display_usr_list = "block"
	#########################################
	########### Manage Group End ############
	#########################################

	#########################################
	########## Modify Group Start ###########
	#########################################
	if(form.getvalue("modify_group")):
		get_sel_group = form.getvalue("re_grp_list")
		get_all_users_sub = manage_users.get_smb_users()
		get_all_users_sub = get_all_users_sub["users"]

		grp_modify = form.getvalue("re_grp_list")
		usr_list_modify = form.getvalue("granted_users[]")
		check_usr = isinstance(usr_list_modify, str)
		if(check_usr == True):
			usr_list_modify = string.split(usr_list_modify)

		if(usr_list_modify != None):
			get_available_users = list(set(get_all_users_sub) - set(usr_list_modify))
		else:
			get_available_users = get_all_users_sub

		grp_modify_str = grp_modify
		grp_modify = string.split(grp_modify)

		if((get_available_users != []) or (get_available_users != '')):
			for x in get_available_users:
				delete_usr_from_grp = manage_users.del_user_from_group(grp_modify_str,x)

		if(usr_list_modify != None):
			for n in usr_list_modify:
				add_usr_to_grp = manage_users.add_new_groups_to_user(n,grp_modify)
			
			if(add_usr_to_grp["id"] == 0):
				if(check_ha == True):
					get_available_users = " ".join(str(x) for x in get_available_users)
					usr_list_modify = " ".join(str(x) for x in usr_list_modify)
					grp_modify = " ".join(str(x) for x in grp_modify)
					print """<script>location.href = 'https://"""+other_node_ip+"""/fs4/py/othernodecmd.py?act=modify_group&get_available_users="""+str(get_available_users)+"""&grp_modify_str="""+str(grp_modify_str)+"""&usr_list_modify="""+str(usr_list_modify)+"""&grp_modify="""+str(grp_modify)+"""'</script>"""
				print"""<div id = 'id_trace'>"""
				print add_usr_to_grp["desc"]
				print "</div>"
				logstatus = common_methods.sendtologs('Success', 'Successfully Modified the Group', 'user_maintenance.py', add_usr_to_grp["desc"]);

			else:
				print"""<div id = 'id_trace_err' >"""
				print add_usr_to_grp["desc"]
				print "</div>"
				
				logstatus = common_methods.sendtologs('Error', 'Error Occurred while Modification the Group', 'user_maintenance.py', add_usr_to_grp["desc"]);

		get_re_usr_list = manage_users.get_users_of_group(get_sel_group)
		get_re_usr_list_mod = get_re_usr_list["users"]
	#########################################
	########### Modify Group End ############
	#########################################

	#########################################
	########### Modify User Start ###########
	#########################################
	if(form.getvalue("modify_user")):
		get_re_user_list = form.getvalue("user_list")
		pass_modify = form.getvalue("new_pwd")
		subgrp_modify = form.getvalue("granted_groups[]")
		primary_modify = form.getvalue("primary_group")

		if (pass_modify == None): 
			pass_modify = '' 
		if(subgrp_modify==None):
			subgrp_modify = []
		primary_modify_list = [primary_modify]
		check_subgrp = isinstance(subgrp_modify, str)
		if(check_subgrp == False):
			reduced_subgrp_modify = list(set(subgrp_modify) - set(primary_modify_list))
		elif(check_subgrp == True):
			subgrp_modify = [subgrp_modify]
			reduced_subgrp_modify = list(set(subgrp_modify) - set(primary_modify_list))


		user_info={"user_name":get_re_user_list,"passwd":pass_modify,"group":primary_modify,"sub_groups":reduced_subgrp_modify}

		subgrp_str = " ".join(str(x) for x in reduced_subgrp_modify)

		if(pass_modify == ''):
			change_user_credentials = manage_users.change_credentials(user_info)
		else:
			change_user_credentials = manage_users.change_credentials(user_info,"yes")
		if(change_user_credentials["id"] == 0):
			if(check_ha == True):
				print """<script>location.href = 'https://"""+other_node_ip+"""/fs4/py/othernodecmd.py?act=modify_user&user_name="""+str(get_re_user_list)+"""&passwd="""+str(pass_modify)+"""&group="""+str(primary_modify)+"""&sub_groups="""+subgrp_str+"""'</script>"""
			print"""<div id = 'id_trace'>"""
			print change_user_credentials["desc"]
			print "</div>"

			logstatus = common_methods.sendtologs('Success', 'Successfully Modified '+get_re_user_list+' the User', 'user_maintenance.py',change_user_credentials["desc"]);
		else:
			print"""<div id = 'id_trace_err' >"""
			print change_user_credentials["desc"]
			print "</div>"
			
			logstatus = common_methods.sendtologs('Success', 'Error Occurred while Modify '+get_re_user_list+' the User', 'user_maintenance.py', change_user_credentials["desc"]);
		get_user_group = manage_users.get_user_info(get_sel_user)
		sub_user_group = get_user_group["user_info"]
		display_grp_list = "block"
	#########################################
	############ Modify User End ############
	#########################################

	#########################################
	########### Delete User Start ###########
	#########################################
	if(form.getvalue("delete_user")):
		get_user_to_delete = form.getvalue("usr_to_delete")
		delete_usr_command = manage_users.delete_user(get_user_to_delete)
		if(delete_usr_command["id"] == 0):
			if(check_ha == True):
				print """<script>location.href = 'https://"""+other_node_ip+"""/fs4/py/othernodecmd.py?act=delete_user&get_user_to_delete="""+str(get_user_to_delete)+"""'</script>"""
			print"""<div id = 'id_trace'>"""
			print delete_usr_command["desc"]
			print "</div>"
			logstatus = common_methods.sendtologs('Success', 'Successfully Deleted the '+get_user_to_delete+' From User list', 'user_maintenance.py',delete_usr_command["desc"]);

		else:
			print"""<div id = 'id_trace_err' >"""
			print delete_usr_command["desc"]
			print "</div>"
			logstatus = common_methods.sendtologs('Error', 'Error Occurred while Deleting the '+get_user_to_delete+' From User list', 'user_maintenance.py',delete_usr_command["desc"]);
	#########################################
	############ Delete User End ############
	#########################################

	#########################################
	########## Delete Group Start ###########
	#########################################
	if(form.getvalue("delete_group")):
		get_group_to_delete = form.getvalue("grp_to_delete")
		delete_group_command = manage_users.delete_group(get_group_to_delete)
		if(delete_group_command["id"] == 0):
			ss = delete_group_command
			if(check_ha == True):
				print """<script>location.href = 'https://"""+other_node_ip+"""/fs4/py/othernodecmd.py?act=delete_group&get_group_to_delete="""+str(get_group_to_delete)+"""'</script>"""
			print"""<div id = 'id_trace'>"""
			print delete_group_command["desc"]
			print "</div>"
			logstatus = common_methods.sendtologs('Success', 'Successfully Deleted the '+get_group_to_delete+' From Group list', 'user_maintenance.py',delete_group_command["desc"]);

		else:
			ss = delete_group_command
			print"""<div id = 'id_trace_err' >"""
			print delete_group_command["desc"]
			print "</div>"
			logstatus = common_methods.sendtologs('Error', 'Error Occurred while Deleting the '+get_group_to_delete+' From Group list', 'user_maintenance.py',delete_group_command["desc"]);
	#########################################
	########### Delete Group End ############
	#########################################

	#########################################
	########### Sync Users Start ############
	#########################################
	if(form.getvalue("sync-users")):
		sync_users_cmd = authentication.sync_user_credentials()
		if(sync_users_cmd["id"] == 0):
			if(check_ha == True):
                                print """<script>location.href = 'https://"""+other_node_ip+"""/fs4/py/othernodecmd.py?act=sync_users_grps'</script>"""
			print"""<div id = 'id_trace' >"""
			print sync_users_cmd["desc"]
			print "</div>"
		else:
			print"""<div id = 'id_trace_err' >"""
			print sync_users_cmd["desc"]
			print "</div>"
	#########################################
	############ Sync Users End #############
	#########################################

	if(form.getvalue("execution")):
		get_execution = form.getvalue("execution")
		get_execvalue = form.getvalue("execval")
		if(get_execution == "success"):
			print"<div id = 'id_trace'>"
			print get_execvalue
			print "</div>"
		else:
			print"""<div id = 'id_trace_err'>"""
			print get_execvalue
			print "</div>"

	#------------------------------------- Get all Users Start ---------------------------------------#
	get_all_users = tools.get_local_users()
	if get_all_users["id"] == 2:
		print """<div id="error_div" style="text-align:center; background:#FA5858; border:#FE2E2E 1px solid; width:94%; padding:7px; float:right; margin:5px 5px 0 0; color:#FFF; cursor:pointer;" onclick="return clicking_div();">Unable to get users! <span title="close" style="float:right;">X</span></div>"""
	#------------------------------------- Get all Users End ---------------------------------------#

	#------------------------------------- Get all Group Start ---------------------------------------#
	#get_all_groups = manage_users.get_sys_groups()
	get_all_groups = tools.get_local_groups()
	if get_all_groups["id"] == 2:
		print """<div id="error_div" style="text-align:center; background:#FA5858; border:#FE2E2E 1px solid; width:94%; padding:7px; float:right; margin:5px 5px 0 0; color:#FFF; cursor:pointer;" onclick="return clicking_div();">Unable to get groups! <span title="close" style="float:right;">X</span></div>"""
	#------------------------------------- Get all Group End ---------------------------------------#

	onclick_func = ''
	conn_var = ''
	get_auth_type = authentication.get_auth_type()
	#get_auth_type =  {'status': False, 'type': 'ldap'}
	conn_var = get_auth_type["type"]
	conn_stat = str(get_auth_type["status"])

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
        <td class="text_css">This page allows you to manage, i.e., create, modify or delete local users and groups.</td>
        </tr>
        </table>"""
	if(check_ha == True):
		print"""
	</span></a> Manage Users ("""+show_tn+""")
                <span style="float:right; margin:0;"><a onclick="return onclick_loader();" class="resource_links" href="https://"""+other_node_ip+"""/fs4/py/iframe_user_maintenance.py">"""+show_on+"""</a></span>
                </div>"""
	else:
		print"""  </span></a><p class = "gap_text">Manage Users</p></div>"""
	print"""
		  <div class="infoheader">
		    <div id="tabs">
		      <ul>
			<li><a href="#tabs-1">Create User</a></li>
			<li><a href="#tabs-2">Create Group</a></li>
			<li><a href="#tabs-4">Manage User</a></li>
			<li><a href="#tabs-5">Manage Group</a></li>
			<li><a href="#tabs-6">Delete User</a></li>
			<li><a href="#tabs-7">Delete Group</a></li>
			<li><a href="#tabs-8">Sync Users</a></li>
		      </ul>
		      <div id="tabs-1">

		<!--form container starts here-->
		<div class="form-container">
		<div class="topinputwrap-heading">Create User</div>
		  <div class="inputwrap">
		<form name = 'user_creation' method = 'POST' action = ''>
		<table width="100%" style="padding:0 0 0 10px;">
			<tr>
			<td style="color:#585858; font-weight:600;">User Name</td>
			<td><input class = 'textbox' type = 'text' name = 'username' id = 'username' /></td>
			</tr>
			<tr>
			<td style="color:#585858; font-weight:600;">Password</td>
			<td><input class = 'textbox' type = 'password' name = 'password' id = 'password' /></td>
			</tr>
			<tr>
			<td style="color:#585858; font-weight:600;">Confirm Password</td>
			<td><input class = 'textbox' type = 'password' name = 'c_password' id = 'c_password'></td>
			</tr>

			<tr>
			<td></td>
			<td>

			<button class="buttonClass" type = 'submit'  name = 'create_users' value = 'Create' onclick = 'return validate_user_create_form();' style="float:left; margin:0 0 0 200px;">Create</button>
			</td>
			</tr>
			</table>
			</form>

		  </div>
	</div>
	<!--form container ends here-->
	<p>&nbsp;</p>
	      </div>




		      <div id="tabs-2">

		<!--form container starts here-->
		<div class="form-container">
		<div class="topinputwrap-heading">Create Group</div>
		  <div class="inputwrap">
		<form name = 'add_groups' method = 'POST' action = 'iframe_user_maintenance.py#tabs-2'>
		<table width="100%" style="padding:0 0 0 10px;">
			<tr>
			<td style="color:#585858; font-weight:600;">Group</td>
			<td><input class = 'textbox' type = 'text' name = 'group' id = 'group'></td>
			</tr>

			<tr>
			<td></td>
			<td>

			<button class="buttonClass" type = 'submit'  name = 'create_group' value = 'Create' onclick = 'return validate_group_form(document.add_groups.group.value);' style="float:left; margin:0 0 0 200px;">Create</button>
			</td>
			</tr>
			</table>
			</form>

		  </div>
	</div>
	<!--form container ends here-->
	<p>&nbsp;</p>
	      </div>





	<div id="tabs-4">

		<!--form container starts here-->
		<div class="form-container">
		<div class="topinputwrap-heading">Manage User</div>
		  <div class="inputwrap">

		<form name = 'manage_users' method = 'POST' action = 'iframe_user_maintenance.py#tabs-4'>
		<table width="50%" style="padding:0 0 0 10px;">
			<tr>
			<td style="color:#585858; font-weight:600;">Select User</td>
			<td>
	<div class="styled-select2" style="width:207px;">
	<select name = 'user_list' id = 'user_list' onchange="this.form.submit();">
	<option value = 'select-user'>Select User</option>"""

	for x in get_all_users["users"]:
		print"""<option """
		if(get_sel_user==x):
			print "selected='selected'"
		print """value = '"""+x+"""'>"""+x+"""</option>"""


	print """</select></div>

			</td>
			</tr>
	</table>

	<table width="100%" style='display:"""+display_grp_list+"""; margin:20px 0 0 100px;'>

		<tr>
		<td>Enter New Password</td>
		<td style="padding:0 0 0 30px;"><input class = 'textbox' type = 'password' value = '' name = 'new_pwd' id = 'new_pwd'></td>
		</tr>

		<tr>
		<td style="padding:15px 0 0 0;">Confirm New Password</td>
		<td style="padding:15px 0 0 30px;"><input class = 'textbox' type = 'password' name = 'c_new_pwd' id = 'c_new_pwd' ></td>
		</tr>

		</table>	

		<table width="100%" style='display:"""+display_grp_list+"""; margin:20px 0 0 100px;'>
		<tr>
		<td>
		Available Groups<br/>
		<select class = 'input' id = 'available_groups' name = 'available_groups' style="width:150px; height:100px; margin:5px 0 0 0;" multiple onclick = "return user_maint_move_groups(this.form.available_groups, this.form.granted_groups, '1');">"""
	for g in get_all_groups["groups"]:
		if g not in sub_user_group["sub_groups"]:
			print """<option value = '"""+g+"""'>"""+g+"""</option>"""
		
	print """</select>
		</td>

		
		<td style="padding:0 0 0 50px;">
		User belongs to<br/>
		<select class = 'input' id = 'granted_groups' name = 'granted_groups[]' style="width:150px; height:100px; margin:5px 0 0 0;" multiple onclick = "return user_maint_move_groups(this.form.granted_groups, this.form.available_groups, '2');">"""
	for val in sub_user_group["sub_groups"]:
		print """<option selected = 'selected' value = '"""+val+"""'>"""+val+"""</option>"""

	print """	</select>
		</td>
		</tr>

		<tr>
		<td style="padding:15px 0 0 0;">Choose Primary Group</td>
		<td style="padding:15px 0 0 0;">
		<div class="styled-select2" style="width:207px;">
		<select style="width:221px;" name="primary_group">"""
	for rg in get_all_groups["groups"]:
		print """<option value = '"""+rg+"""'"""
		if(rg == sub_user_group["group"]):
			print "selected = 'selected'"

		print """>"""+rg+"""</option>"""

	print """	</select></div>
		</td>
		</tr>

		<tr>
		<td></td>
		<td>
	<button class="buttonClass" type = "submit"  name="modify_user" value="Apply" style="float:right; margin:20px 0px 20px 0;" onclick ='return modify_user_information();'>Modify</button>
		</td>
		</tr>

		</table>


			</form>

		  </div>
	</div>
	<!--form container ends here-->
	<p>&nbsp;</p>

	</div>


	<div id="tabs-5">

		<!--form container starts here-->
		<div class="form-container">
		<div class="topinputwrap-heading">Manage Group</div>
		  <div class="inputwrap">

	<form name = 'manage_groups' method = 'POST' action = 'iframe_user_maintenance.py#tabs-5'>
		<table width="50%" style="padding:0 0 0 10px;">
			<tr>
			<td style="color:#585858; font-weight:600;">Select User</td>
			<td>
	<div class="styled-select2" style="width:207px;">
	<select name = 're_grp_list' id = 're_grp_list' onchange="this.form.submit();">
	<option value = 'select-group'>Select Group</option>"""

	for grp in get_all_groups["groups"]:
		print"""<option """
		if(get_sel_group == grp):
			print "selected='selected'"
		print """value = '"""+grp+"""'>"""+grp+"""</option>"""


	print """</select></div>

			</td>
			</tr>
	</table>

	<table width="100%" style='display:"""+display_usr_list+"""; margin:20px 0 0 100px;'>
		<tr>
		<td>
		Available Users<br/>
		<select class = 'input' id = 'available_users' name = 'available_users' style="width:150px; height:100px; margin:5px 0 0 0;" multiple 
	onclick = "return move_data(this.form.available_users, this.form.granted_users, '1');">"""
	for xg in get_all_users["users"]:
		if xg not in get_re_usr_list_mod:
			print """<option value = '"""+xg+"""' selected>"""+xg+"""</option>"""

	print """</select>
		</td>

		
		<td style="padding:0 0 0 50px;">
		Users of the Group<br/>
		<select class = 'input' id = 'granted_users' name = 'granted_users[]' style="width:150px; height:100px; margin:5px 0 0 0;" multiple onclick = "return move_data(this.form.granted_users, this.form.available_users, '2');">"""
	for usr in get_re_usr_list_mod:
		print """<option value = '"""+usr+"""' selected>"""+usr+"""</option>"""

	print """       </select>
		</td>
		</tr>

		<tr>
		<td></td>
		<td>
	<button class="buttonClass" type = "submit"  name="modify_group" value="Apply" style="float:right; margin:20px 0px 20px 0;">Modify</button>
		</td>
		</tr>

		</table>



	</form>

		  </div>
	</div>
	<!--form container ends here-->
	<p>&nbsp;</p>

	</div>

	<div id="tabs-6">

		<!--form container starts here-->
		<div class="form-container">
		<div class="topinputwrap-heading">Delete User</div>
		  <div class="inputwrap">

		<form name = 'del_user' method = 'POST' action = 'iframe_user_maintenance.py#tabs-6'>
		<table width="100%" style="padding:0 0 0 10px;">
			<tr>
			<td style="color:#585858; font-weight:600;">Select User to delete</td>
			<td>
	<div class="styled-select2" style="width:207px;margin-left:-14%;">
	<select name = 'usr_to_delete'>
	<option value = 'select-user'>Select User</option>"""
	for du in get_all_users["users"]:
		if du != '':
			print """<option value = '"""+du+"""'>"""+du+"""</option>"""

	print """</select></div>
			</td>
			</tr>

			<tr>
			<td></td>
			<td>

			<button class="buttonClass" type = 'submit'  name = 'delete_user' value = 'Create' onclick = 'return show_users_to_delete(document.del_user.usr_to_delete.value);' style="float:left; margin:0 0 0 200px;">Delete</button>
			</td>
			</tr>
			</table>
			</form>

		  </div>
	</div>
	<!--form container ends here-->
	<p>&nbsp;</p>

	</div>


	<div id="tabs-7">

		<!--form container starts here-->
		<div class="form-container">
		<div class="topinputwrap-heading">Delete Group</div>
		  <div class="inputwrap">

		<form name = 'del_group' method = 'POST' action = 'iframe_user_maintenance.py#tabs-7'>
		<table width="100%" style="padding:0 0 0 10px;">
			<tr>
			<td style="color:#585858; font-weight:600;">Select Group to delete</td>
			<td>
	<div class="styled-select2" style="width:207px;margin-left:-14%;">
	<select name = 'grp_to_delete' >
	<option value = 'select-user'>Select Group</option>"""
	for dg in get_all_groups["groups"]:
		if(dg != "USER"):
			print """<option value = '"""+dg+"""'>"""+dg+"""</option>"""

	print """</select></div>
			</td>
			</tr>

			<tr>
			<td></td>
			<td>

			<button class="buttonClass" type = 'submit'  name = 'delete_group' value = 'Create' onclick = 'return show_users_of_group(document.del_group.grp_to_delete.value);' style="float:left; margin:0 0 0 200px;">Delete</button>
			</td>
			</tr>
			</table>
			</form>

		  </div>
	</div>
	<!--form container ends here-->
	<p>&nbsp;</p>

	</div>




	<div id="tabs-8">

		<!--form container starts here-->
		<div class="form-container">
		<div class="topinputwrap-heading">Sync Users</div>
		  <div class="inputwrap">

		<form name = 'sync_users' method = 'POST' action = 'iframe_user_maintenance.py#tabs-8'>
		<img  style="display:none;" src="../images/sync-loading.GIF" />
		<table style="border:#D1D1D1 1px solid; width:100px; margin:0 0 20px 300px;">
		<tr>
		<th style="border:#D1D1D1 1px solid; background-color:#D1D1D1; padding:5px;"><p id="sync-content">Sync Users</p></th>
		</tr>

		<tr>
		<td>
			<div id="restart-service-div" style="width:100px;">
	                <button onclick="return onclick_sync_loader('"""+conn_var+"""','"""+conn_stat+"""');" type="submit" name="sync-users" value="sync-users" style="border:none; background-color:#FFF; cursor:pointer;">
                        <img id="sync-static" src="../images/sync_users_icon.png" alt="sync users" /><img id="sync-loading" style="display:none;" src="../images/sync-loading.GIF" alt="sync users" /></button><br/>
        		</div>
		</td>
		</tr>
		</table>



			</form>

		  </div>
	</div>
	<!--form container ends here-->
	<p>&nbsp;</p>

	</div>


	</div>

	  </div>
	</div>
	</div>
	"""
except Exception as e:
	disp_except.display_exception(e);
