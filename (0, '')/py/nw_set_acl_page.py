#!/usr/bin/python
import cgitb, sys, header, common_methods, os
cgitb.enable()

sys.path.append('/var/nasexe/python/');
import smb, tools
from tools import acl
from fs2global import *;


#print 'Content-Type: text/html'

get_share = '';
sharepath = '';
grant_user = ''
set_path = ''
read_check =''
read_per = ''
write_check = ''
execute_check = ''
write_per = ''
execute_per = ''
display_rwx = "none"
display_acl_but = "none"
users_style  = 'none';
owner_name = ''
group_name = ''
path_owner = ''
reset_chk_but = ''
reset_chk = ''
alldisabled = '';
ads_separator = '';
ads_separator = tools.get_ads_separator();
userslength = 0;
groupslength = 0;
domainsarray = [];
domainname = '';
avail_users_style = 'none';
users_list_style = 'none';
groups_list_style = 'none';
users_from_list = [];
groups_from_list = [];
recr_val = ''
recur_info = ''
ug = '';
get_users_string = '';
get_groups_string = '';
o_read_val = 0
o_write_val = 0
o_execute_val = 0
g_read_val = 0
g_write_val = 0
g_execute_val = 0
ot_read_val = 0
ot_write_val = 0
ot_execute_val = 0
get_sub_inherit = "no"
'''
chk_o_read =""
chk_o_write =""
chk_o_exe =""
chk_g_read =""
chk_g_write =""
chk_g_exe =""
chk_ot_read =""
chk_ot_write =""
chk_ot_read =""
'''
"""
get_hid_k_val = header.form.getvalue("hid_k_val")
l=1
while(l<int(get_hid_k_val)):
	#print l
	#if(header.form.getvalue('o_read'+str(l)) == ""):
		#globals()["checked_read" + str(l)] = ""
		#print sanjeev
	chk = "checked_read"+str(l)
	if(chk == "checked_read"+str(l)):
		print chk

	l=l+1
"""
smbuserslength  = 0;
smbgroupslength = 0

assusrfile = 'aclassusersfile';
assgrpfile = 'aclassgroupsfile';

sys.path.append('/var/nasexe/python/')
import manage_users

#############Display for User And Group Code ##############
get_all_users = manage_users.get_smb_users()

get_all_groups = manage_users.get_sys_groups()
#print get_all_groups

############ get auth mode and get all users##############
connstatus = common_methods.conn_status();

domainsarray = common_methods.get_all_domains();

all_users_list  = common_methods.get_users_string();
all_groups_list = common_methods.get_groups_string();

smb_all_users_array  = [];
smb_all_groups_array = [];

# if userslist is not empty
if (all_users_list['id'] == 0):
	smb_all_users_array  = all_users_list['users'];
        smbuserslength       = len(smb_all_users_array);

# if groupslist id not empty
if (all_groups_list['id'] == 0):
	smb_all_groups_array = all_groups_list['groups'];
        smbgroupslength      = len(smb_all_groups_array);
#########End############################################

user_group_list = [];

for user_lst in get_all_users['users']:
	
	user_name = '[U]'+str(user_lst)
	#print user_name
	
	user_group_list.append(user_name);
#print '<br/>'
#print get_all_groups
for group_lst  in get_all_groups['groups']:
	group_name = '[G]'+str(group_lst)
	user_group_list.append(group_name)
#print get_all_users
#for t in user_group_list:
#	print t
##
#print user_group_list
################End########################################

################Get Log Path#############################
querystring = os.environ['QUERY_STRING'];
#print querystring
if (querystring.find('share_name=') >= 0):
	if (querystring.find('&dom=') > 0):
		get_share = querystring[querystring.find('share_name=') + len('share_name='):querystring.find('&dom=')];

	else:
		get_share = querystring[querystring.find('share_name=') + len('share_name='):];
###################End##################################
#sharepath = '';

###############This code use for Check Option##########
if (querystring.find('ug=') >= 0):
        ug = querystring[querystring.find('ug=') + len('ug='):querystring.find('&share_name')];

if (ug != ''):
	validuser_checked = 'checked';

	assusrarray = common_methods.read_file(assusrfile);
	assgrparray = common_methods.read_file(assgrpfile);

	if (len(assusrarray) > 0):
		for assu in assusrarray:
			assu = assu.replace('%20', ' ');
			assu = assu.strip();

			assu_internal = assu;
			disp_assu = assu;

			users_from_list.append(assu);
			#user_name.append(assu);

	if (len(assgrparray) > 0):
		for assg in assgrparray:
			assg = assg.replace('%20', ' ');
			assg = assg.strip();

			assg_internal = assg;

			groups_from_list.append(assg);

	domainname = querystring[querystring.find('&dom=') + len('&dom='):];
	domainname = domainname.strip();

	tempstring = '';

	if (len(groups_from_list) > 0):
		for gfl in groups_from_list:
			tempstring += gfl + ':::';

	tempstring = tempstring.strip();
	tempstring = ':::' + tempstring;

	if (ug == 'users'):
		avail_users_style = 'block';

		get_users_array = [];
		get_users_array = common_methods.read_file('aclsearchusersfile.txt');

		get_users_array = list(set(get_users_array) - set(groups_from_list));

		for get_users in get_users_array:
			if (get_users != ''):
				get_users = get_users.strip();
				get_users = '[U]' + get_users;

				checkuserexists = tempstring.find(':::' + get_users + ':::');
				get_usersinternal = common_methods.replace_chars(get_users, 'chartotext');
				get_disp_users    = get_users[get_users.find('\\') + 1:];

				check_users = '"' + get_users + '"';
				
				if (checkuserexists < 0):
					get_users_string += '<option value = "' + get_usersinternal + '">' + get_disp_users + '</option>';

	if (ug == 'groups'):
		avail_users_style = 'block';

		get_groups_array = [];
		get_groups_array = common_methods.read_file('aclsearchgroupsfile.txt');

		for get_groups in get_groups_array:
			if (get_groups != ''):
				get_groups = get_groups.strip();
				get_groups = '[G]' + get_groups;

				checkuserexists = tempstring.find(':::' + get_groups + ':::');
				get_groupsinternal = common_methods.replace_chars(get_groups, 'chartotext');
				get_disp_groups    = get_groups[get_groups.find('\\') + 1:];

				if (checkuserexists < 0):
					get_groups_string += '<option value = "' + get_groupsinternal + '">' + get_disp_groups + '</option>';

sharedetails = tools.get_share(get_share);

assgroupsarray = [];
assgroupsarray = common_methods.read_file('aclassgroupsfile');

################SET OWNERSHIP NEW#########################
assusr = 'root';
assgrp = 'root';
disp_share_path = '';

if (querystring.find('share_name=') >= 0):
        if (querystring.find('&ro=') > 0):
                share_name = querystring[querystring.find('share_name=') + len('share_name='):querystring.find('&ro=')];

        elif (querystring.find('&dom=') > 0):
                share_name = querystring[querystring.find('share_name=') + len('share_name='):querystring.find('&dom=')];

        else:
                share_name = querystring[querystring.find('share_name=') + len('share_name='):];

        if (querystring.find('&ug=') > 0):
                ug = querystring[querystring.find('&ug=') + len('&ug='):querystring.find('&share_name')];

#print share_name;

if (share_name != ''):
        share_path = common_methods.get_share_path('^' + share_name + ':');

        if (share_path != 1):
                disp_share_path = share_path.replace('/storage/', '');

        else:
                share_path = '';

if (share_path != ''):
	get_ownership_status = acl.get_acl(share_path);

	if (get_ownership_status != {}):
		assusr     = get_ownership_status['owner'];
		assgrp     = get_ownership_status['group'];
		share_path = get_ownership_status['path'];


else:
	common_methods.sendtologs('ERROR', 'Get Share Path', 'UI', '"perms_ownership.py, common_methods.get_share_path()", Could not get path');


usersfiletoread  = 'ownssearchusersfile.txt';
groupsfiletoread = 'ownssearchgroupsfile.txt';

assusrfile = 'ownsassusersfile';
assgrpfile = 'ownsassgroupsfile';

assusrarray = [];
assgrparray = [];

users_from_list  = [];
groups_from_list = [];

get_users_string = '';
get_groups_string = '';

usersarray  = [];
groupsarray = [];

if (ug != ''):
	domainname = querystring[querystring.find('&dom=') + len('&dom='):];
	domainname = domainname.strip();

	assusrarray = common_methods.read_file(assusrfile);
	assgrparray = common_methods.read_file(assgrpfile);

	users_style = 'table';
	groups_style = 'table';

	if (len(assusrarray) > 0):
		for i in assusrarray:
			assusr = i;

	if (len(assgrparray) > 0):
		for i in assgrparray:
			assgrp = i;


	if (assusr != ''):
		assusr = assusr.strip();
		groups_style = 'table';

	if (assgrp != ''):
		assgrp = assgrp.strip();
		users_style = 'table';

	if (assusr == ''):
		assusr = get_ownership_status['owner'];

	if (assgrp == ''):
		assgrp = get_ownership_status['group'];

	if (ug == 'users'):
		usersarray  = common_methods.read_file(usersfiletoread);
		usersarray.sort();
		userarray = list(set(usersarray));

		users_list_style = 'block';
		users_style = 'table';

		groups_list_style = 'none';
		groups_style = 'none';

		if (len(usersarray) > 0):
			users_style = 'table';

			for users in usersarray:
				get_users_string += '<option value = "' + users + '">' + users + '</option>';


	elif (ug == 'groups'):
		groupsarray = common_methods.read_file(groupsfiletoread);
		groupsarray.sort();
		groupsarray = list(set(groupsarray));

		users_list_style = 'block';
		users_style = 'none';

		groups_list_style = 'block';
		groups_style = 'table';

		if (len(groupsarray) > 0):
			groups_style = 'table';

			for groups in groupsarray:
				get_groups_string += '<option value = "' + groups + '">' + groups + '</option>';


####################End##################################

users_dropdown = '';

share_path = ''
if (sharedetails['id'] == 0):
	sharesinfo = sharedetails['share'];
	sharepath  = sharesinfo['path'];
	share_path = sharesinfo['path'];
	sharepath  = sharepath.replace('/storage/', '');

check_path_exists = tools.is_dir_exist(share_path)

if(check_path_exists == True):
	lis_info = acl.get_acl(share_path)
###############permissiion############
	perms_info = acl.get_acl(share_path)
	owner_perms = perms_info['d_user']
	group_perms = perms_info['d_group']
	other_perms = perms_info['d_other']
else:
	common_methods.sendtologs('ERROR', 'Get Acl', 'UI', '"set_acl_page.py, tools.acl.get_acl()" ' + str(perms_info));
#########End#########################

if(lis_info != {}):
	lis_info = lis_info['acl']
else:
	lis_info = {}

##############End##########################################################

acl_dict = {}
chk_dict = {}
acl_perm ={}
chk_perm ={}
#acl_fax = {}
#############Set User######################
if(header.form.getvalue('set')):
	set_path = header.form.getvalue('selected_file')
	get_hid_k_val = header.form.getvalue("hid_k_val")
	avail_user = header.form.getvalue('avail[]')
	grant_user = header.form.getvalue('grant_users[]')
	#print 'Avail:'+str(avail_user)
	#print '<br/>'
	#print 'Grant:'+str(grant_user)
	if(isinstance(grant_user, str) == True ):
		grant_user = [grant_user]
		#grant_user = grant_user.replace('[U]', '')
        	#grant_user =grant_user.replace('[G]', '')
	
	#print """<script>location.href = 'main.py?page=acl&"""+querystring+"""#subtabs-2';</script>"""
	display_rwx = "block"
############End###########################
#################### Set Acl################
if(header.form.getvalue('set_acl')):
	set_path_acl = header.form.getvalue('selected_file')
	set_path_acl_add = '/storage/'+set_path_acl
	avail_user_acl = header.form.getvalue('avail')
	get_hid_k_val = header.form.getvalue("hid_k_val")
	grant_user = header.form.getvalue('grant_users[]')
	recr_val = header.form.getvalue('o_recursive') 
	if(isinstance(grant_user, str) == True ):
                grant_user = [grant_user]
	
	#for group_lst  in get_all_groups['groups']:
	#	group_lst = '[G]'+str()
	#	print '<br/>'
	#	print 'GROUP:'+str(group_lst)
	#	print '<br/>'
	for u in grant_user:
		u = u.replace('[U]', '')
		u = u.replace('[G]', '@')
		
		#chk_dict[u+'_chk_read']=""
		#chk_dict[u+'_chk_write']=""
		#chk_dict[u+'_chk_execute']=""
		if((header.form.getvalue(u+'o_read') == "on") and (header.form.getvalue(u+'o_write') == "on") and (header.form.getvalue(u+'o_execute') == "on" )):
			acl_dict.update({u:'rwx'})
			chk_dict.update({u+'_chk_read':'checked',u+'_chk_write':'checked',u+'_chk_execute':'checked'})
			

		if((header.form.getvalue(u+'o_read') == "on") and (header.form.getvalue(u+'o_write') == None) and (header.form.getvalue(u+'o_execute') == None )):	
			acl_dict.update({u:'r--'})
			chk_dict.update({u+'_chk_read':'checked',u+'_chk_write':'',u+'_chk_execute':''})
			

		if((header.form.getvalue(u+'o_read') == "on") and (header.form.getvalue(u+'o_write') == "on") and (header.form.getvalue(u+'o_execute') == None )):
			acl_dict.update({u:'rw-'})
			chk_dict.update({u+'_chk_read':'checked',u+'_chk_write':'checked',u+'_chk_execute':''})
		
		if((header.form.getvalue(u+'o_read') == None) and (header.form.getvalue(u+'o_write') == "on") and (header.form.getvalue(u+'o_execute') == "on" )):
			acl_dict.update({u:'-wx'})
			chk_dict.update({u+'_chk_read':'',u+'_chk_write':'checked',u+'_chk_execute':'checked'})

		if((header.form.getvalue(u+'o_read') == "on") and (header.form.getvalue(u+'o_write') == None) and (header.form.getvalue(u+'o_execute') == "on" )):
			acl_dict.update({u:'r-x'})
			chk_dict.update({u+'_chk_read':'checked',u+'_chk_write':'',u+'_chk_execute':'checked'})
		
		if((header.form.getvalue(u+'o_read') == None) and (header.form.getvalue(u+'o_write') == None) and (header.form.getvalue(u+'o_execute') == "on" )):
			acl_dict.update({u:'--x'})
			chk_dict.update({u+'_chk_read':'',u+'_chk_write':'',u+'_chk_execute':'checked'})

		if((header.form.getvalue(u+'o_read') == None) and (header.form.getvalue(u+'o_write') == None) and (header.form.getvalue(u+'o_execute') == None )):
			acl_dict.update({u:'---'})
			chk_dict.update({u+'_chk_read':'',u+'_chk_write':'',u+'_chk_execute':''})
		
		if((header.form.getvalue(u+'o_read') == None) and (header.form.getvalue(u+'o_write') == "on") and (header.form.getvalue(u+'o_execute') == None )):
			acl_dict.update({u:'-w-'})
			chk_dict.update({u+'_chk_read':'',u+'_chk_write':'checked',u+'_chk_execute':''})

	
	#print chk_dict	
	#print 'CHK:'+str(chk_dict)
	set_acl_code = acl.set_acl(set_path_acl_add,acl_dict,recr_val)
	#print "SET:"+str(set_acl_code)
	if(set_acl_code == True):
	
		print "<div id='id_trace'>"
                print "Acl successfully Set!"
                print "</div>"
		logstatus = common_methods.sendtologs('Success', 'Acl Succefully set', 'UI','set_acl_page.py'+ str(set_acl_code));
        else:
                print "<div id='id_trace_err'>"
                print "Error Occured while Setting the acl!"
                print "</div>"
		logstatus = common_methods.sendtologs('Error', 'Error Occured during set the Acl', 'UI','set_acl_page.py'+ str(set_acl_code));
	
	#print "<script>location.href = 'main.py?page=acl#subtabs-3';</script>"
	print """<script>location.href = 'main.py?page=acl&"""+querystring+"""#subtabs-2';</script>"""
	#print "<script>location.href = 'set_acl_page.py?share_name=%s#subtabs-2';</script>" % share_name;

	display_rwx = "block"
##############End###########################

###################Set Owner #########################
if(header.form.getvalue("set_owner")):
	path_owner= header.form.getvalue("selected_file")
	path_owner_add = '/storage/'+path_owner
	owner_name = header.form.getvalue("acl_owner")
	
	group_name = header.form.getvalue("acl_group")
	recur_info = header.form.getvalue("acl_chk_info")
	owner_cmd = acl.set_ownership(path_owner_add,owner_name,group_name,recur_info)
	#print "Owner Cmd:"+str(owner_cmd)
	if(owner_cmd == True):
		print"<div id = 'id_trace'>"
		print "Succesfully Set the Ownership"
                print "</div>"
		
        else:
                print"<div id = 'id_trace_err'>"
                print "Error Occured While Setting the Ownership"
		print "</div>"
	#print "<script>location.href = 'main.py?page=acl#subtabs-3';</script>"

##################End#################################

######################Reset Acl######################
if(header.form.getvalue("reset_acl")):
	path_reset = header.form.getvalue("selected_file")
	path_reset =  '/storage/'+path_reset
	reset_chk = header.form.getvalue("check_reset")


	reset_acl_func =acl.reset_acl(path_reset,reset_chk) 
	
	if(reset_acl_func == True):
                print"<div id = 'id_trace'>"
                print "Succesfully Reset the Acl"
                print "</div>"
		logstatus = common_methods.sendtologs('Success', 'Acl Succefully Reset', 'UI','set_acl_page.py'+ str(reset_acl_func));
        else:
                print"<div id = 'id_trace_err'>"
                print "Error Occured While Resetting the Acl"
                print "</div>"
		logstatus = common_methods.sendtologs('Error', 'Error Occured while Reseting Acl', 'UI','set_acl_page.py'+ str(reset_acl_func));
	print """<script>location.href = 'main.py?page=acl&"""+querystring+"""#subtabs-6';</script>"""

#####################End#############################


###########Acl User Permission##################################

if(header.form.getvalue("acl_user_del")):
	info_path = header.form.getvalue("selected_file")
	info_path_add = '/storage/'+info_path
	select_check_user = header.form.getvalue("user_remove")
	print 'Rem:'+str(select_check_user)
	inf_recr = header.form.getvalue("o_recursive")
	for acl_info_perm in lis_info:
		print acl_info_perm
		if((header.form.getvalue(acl_info_perm+'o_read') == "on") and (header.form.getvalue(acl_info_perm+'o_write') == "on") and (header.form.getvalue(acl_info_perm+'o_execute') == "on" )):
			acl_perm.update({acl_info_perm:'rwx'})
			chk_perm.update({acl_info_perm+'_chk_read':'checked',acl_info_perm+'_chk_write':'checked',acl_info_perm+'_chk_execute':'checked'})
			

		if((header.form.getvalue(acl_info_perm+'o_read') == "on") and (header.form.getvalue(acl_info_perm+'o_write') == None) and (header.form.getvalue(acl_info_perm+'o_execute') == None )):	
			acl_perm.update({acl_info_perm:'r--'})
			chk_perm.update({acl_info_perm+'_chk_read':'checked',acl_info_perm+'_chk_write':'',acl_info_perm+'_chk_execute':''})
			

		if((header.form.getvalue(acl_info_perm+'o_read') == "on") and (header.form.getvalue(acl_info_perm+'o_write') == "on") and (header.form.getvalue(acl_info_perm+'o_execute') == None )):
			acl_perm.update({acl_info_perm:'rw-'})
			chk_perm.update({acl_info_perm+'_chk_read':'checked',acl_info_perm+'_chk_write':'checked',acl_info_perm+'_chk_execute':''})
		
		if((header.form.getvalue(acl_info_perm+'o_read') == None) and (header.form.getvalue(acl_info_perm+'o_write') == "on") and (header.form.getvalue(acl_info_perm+'o_execute') == "on" )):
			acl_perm.update({acl_info_perm:'-wx'})
			chk_perm.update({acl_info_perm+'_chk_read':'',acl_info_perm+'_chk_write':'checked',acl_info_perm+'_chk_execute':'checked'})

		if((header.form.getvalue(acl_info_perm+'o_read') == "on") and (header.form.getvalue(acl_info_perm+'o_write') == None) and (header.form.getvalue(acl_info_perm+'o_execute') == "on" )):
			acl_perm.update({acl_info_perm:'r-x'})
			chk_perm.update({acl_info_perm+'_chk_read':'checked',acl_info_perm+'_chk_write':'',acl_info_perm+'_chk_execute':'checked'})
		
		if((header.form.getvalue(acl_info_perm+'o_read') == None) and (header.form.getvalue(acl_info_perm+'o_write') == None) and (header.form.getvalue(acl_info_perm+'o_execute') == "on" )):
			acl_perm.update({acl_info_perm:'--x'})
			chk_perm.update({acl_info_perm+'_chk_read':'',acl_info_perm+'_chk_write':'',acl_info_perm+'_chk_execute':'checked'})

		if((header.form.getvalue(acl_info_perm+'o_read') == None) and (header.form.getvalue(acl_info_perm+'o_write') == None) and (header.form.getvalue(acl_info_perm+'o_execute') == None )):
			acl_perm.update({acl_info_perm:'---'})
			chk_perm.update({acl_info_perm+'_chk_read':'',acl_info_perm+'_chk_write':'',acl_info_perm+'_chk_execute':''})
		
		if((header.form.getvalue(acl_info_perm+'o_read') == None) and (header.form.getvalue(acl_info_perm+'o_write') == "on") and (header.form.getvalue(acl_info_perm+'o_execute') == None )):
			acl_perm.update({acl_info_perm:'-w-'})
			chk_perm.update({acl_info_perm+'_chk_read':'',acl_info_perm+'_chk_write':'checked',acl_info_perm+'_chk_execute':''})
	
	set_acl_perms = acl.set_acl(info_path_add,acl_perm,inf_recr)

	if(set_acl_perms == True):
                print"<div id = 'id_trace'>"
                print "Succesfully Set the Permission"
                print "</div>"
		logstatus = common_methods.sendtologs('Success', 'Succefully Update the Acl User Permission', 'UI','set_acl_page.py'+ str(set_acl_perms));
        else:
                print"<div id = 'id_trace_err'>"
                print "Error Occured While Setting the Permission"
                print "</div>"
		logstatus = common_methods.sendtologs('Error', 'Error Occurred during Update the Acl User Permission', 'UI','set_acl_page.py'+ str(set_acl_perms));

	
        #print "SET:"+str(set_acl_perms)
	print """<script>location.href = 'main.py?page=acl&"""+querystring+"""#subtabs-5';</script>"""
#############End#####################################

##################Change Permission############################
if(header.form.getvalue("change_perm_but")):
	perm_path = header.form.getvalue("selected_file")
	perm_path_add = '/storage/'+perm_path
	
	print 'PATH:'+str(perm_path_add)
        get_o_read = header.form.getvalue("o_read")
        get_o_write = header.form.getvalue("o_write")
        get_o_execute = header.form.getvalue("o_execute")
        get_g_read = header.form.getvalue("g_read")
        get_g_write = header.form.getvalue("g_write")
        get_g_execute = header.form.getvalue("g_execute")
        get_ot_read = header.form.getvalue("ot_read")
        get_ot_write = header.form.getvalue("ot_write")
        get_ot_execute = header.form.getvalue("ot_execute")
        get_sub_inherit = header.form.getvalue("sub_inherit")
        #get_hid_share_name = header.form.getvalue("hid_share_name")
        #get_hid_share_path = header.form.getvalue("hid_share_path")
	if(get_o_read == "on"):
                #chk_o_read = "checked"
                o_read_val = 4
        if(get_o_write == "on"):

                #chk_o_write = "checked"
                o_write_val = 2
        if(get_o_execute == "on"):

                #chk_o_exe = "checked"
                o_execute_val = 1

        if(get_g_read == "on"):

                #chk_g_read = "checked"
                g_read_val = 4
        if(get_g_write == "on"):
                #chk_g_write = "checked"
                g_write_val = 2
        if(get_g_execute == "on"):
                #chk_o_exe = "checked"
                g_execute_val = 1

        if(get_ot_read == "on"):
                #chk_ot_read = "checked"
                ot_read_val = 4
        if(get_ot_write == "on"):
                #chk_ot_write = "checked"
                ot_write_val = 2
        if(get_ot_execute == "on"):
                #chk_ot_exe = "checked"
                ot_execute_val = 1
        owner_perm = o_read_val+o_write_val+o_execute_val
        group_perm = g_read_val+g_write_val+g_execute_val
	other_perm = ot_read_val+ot_write_val+ot_execute_val

        share_permission = str(owner_perm)+str(group_perm)+str(other_perm)
	print share_permission
        if(get_sub_inherit == "on"):
                get_sub_inherit = "YES"
	else:
		get_sub_inherit = "NO"
	
	#check_path_exists = 
        set_perm_cmd = acl.set_permissions(perm_path_add,per=share_permission,recur=get_sub_inherit)

        if(set_perm_cmd == True):
                print "<div id='id_trace'>"
                print "Permission changed successfully!"
                print "</div>"
		logstatus = common_methods.sendtologs('Success', 'Succefully Change the Share Permission', 'UI','set_acl_page.py'+ str(set_perm_cmd));
        else:
                print "<div id='id_trace_err'>"
                print "Error setting permission!"
                print "</div>"
		
		logstatus = common_methods.sendtologs('Error', 'Error Occurred Change the Share Permission', 'UI','set_acl_page.py'+ str(set_perm_cmd));


	print """<script>location.href = 'main.py?page=acl&"""+querystring+"""#subtabs-3';</script>"""
######################End###################################


###############Reset Single user#######################

for reset_info in lis_info:
	reset_lis_info =  reset_info + 'reset_single';
	if(header.form.getvalue(reset_info+"reset_single")):
		reset_path = header.form.getvalue('selected_file')
       		reset_path_add = '/storage/'+reset_path
		#print reset_path_add
		user_r = reset_info + 'reset_single'
		user_res = user_r.replace('reset_single', '')
		user_res_name = user_res.strip()
		#print user_res_name
		reset_cmd = acl.reset_acl_user(path=reset_path_add, user=user_res_name)
		#print reset_cmd
		if(reset_cmd == True):
                	print "<div id='id_trace'>"
                	print "successfully Reset the User!"
                	print "</div>"
			
			logstatus = common_methods.sendtologs('Success', 'Succefully Reset the Single User', 'UI','set_acl_page.py'+ str(reset_cmd));
        	else:
                	print "<div id='id_trace_err'>"
                	print "Error Occured while Reseting!"
                	print "</div>"
			
			logstatus = common_methods.sendtologs('Error', 'Error Occurred while Reset the Single User', 'UI','set_acl_page.py'+ str(reset_cmd));
		#print header.form.getvalue(reset_info+'reset_single')
		print """<script>location.href = 'main.py?page=acl&"""+querystring+"""#subtabs-5';</script>"""

################End###################################

if (len(grant_user) > 0):
	for gu in grant_user:
		groups_from_list.append(gu);

groups_from_list.sort();
#for get_user_arr in get_users_array:
	
#	user_add_array = '[U]'+str(get_user_arr)
#	print 'UARRAY:'+str(user_add_array)
#	if(isinstance(user_add_array, str) == True ):
#                user_add_array = [user_add_array]
#groups_from_list = list(set(user_add_array)-set(groups_from_list));
groups_from_list = list(set(groups_from_list));
#print 'GLIST:'+str(groups_from_list)
for keys in lis_info:
	if (keys.find('@') == 0):
		keys = keys.replace('@', '[G]');

	else:
		keys = '[U]' + keys;

	groups_from_list.append(keys);

groups_from_list.sort();
groups_from_list = list(set(groups_from_list));

for groups in groups_from_list:
	users_dropdown += '<option value = "' + groups + '" selected>' + groups + '</option>'; 
print get_users_string

##########################New Owneship############################






#################################################################
import left_nav
print """
      <!--Right side body content starts from here-->
      <div class="rightsidecontainer" style="overflow:hidden;">
	<div class="insidepage-heading">NAS >> <span class="content">Acl Configuration</span></div>
	<div style="padding:5px;font-weight:bold;"><a href = 'main.py?page=cs'><img style="float:right; padding:0 10px 2px 0;" title = 'Back to shares' src = '../images/gobacktoshares.png' /></a></div>
	<!--tab srt-->
	<div class="searchresult-container">
	  <div class="infoheader">
	    <div id="tabs">
	      <ul>
		<li><a href="#tabs-1">Acl Configuration</a></li>
	      </ul>
<div id="tabs-1">

	<!--form container starts here-->
	<form name = 'access_control_form'>
	<div id="subtabs">

                  <ul>
                    <li><a href="#subtabs-1">Acl Path</a></li>
                    <li><a href="#subtabs-2">Set Acl</a></li>
		    <li><a href="#subtabs-3">Share Permission</a></li>
                    <li><a href="#subtabs-4">Ownership</a></li>
		    <li><a href="#subtabs-5">Acl User Info</a></li>
		    <li><a href="#subtabs-6">Reset Acl</a></li>
                  </ul>
	 <div id="subtabs-1">


	  <table width="100%">

	<tr>
	<td>Folder:</td>
	<td colspan = '4'>
	<iframe style = 'border: 1px solid;' onload = '' src = 'show_dir1.py?share_name=""" + get_share + """&path=""" + sharepath + """&s=s'></iframe>
	</td>
	</tr>
	  <tr>
          <td>Log Path:</td>
		<!--access_control_form.selected_file-->
	  <td colspan = '4'><input type="text" name = "selected_file" readonly value = '""" + sharepath + """' style = 'width:70%;'></td>
	</tr>
	</table>
	<!--<div style="float:right;margin-top:-3%;">
	<button class="button_example" type="button" name = 'submit'  id = 'id_create_but' value = 'Acl'><a href="main.py?page=acl#subtabs-2">Next</a></button></div>-->

          </div>
</form>


<div id="subtabs-2">
<form name= "user_acl" method = "post" action='main.py?page=acl&"""+querystring+"""#subtabs-2'>
 <table style="width:100%; margin:20px 0 0 0; ">
	 <tr>
          <td style ="color:darkred;"><b>Log Path</b>:</td>
                <!--access_control_form.selected_file-->
          <td colspan = '4'>"""
if(set_path !=''):
	print"""<input type="text" name = "selected_file" readonly value = '""" +set_path+ """' style = 'width:70%;'>"""
else:

	print"""<input type="text" name = "selected_file" readonly value = '""" + sharepath + """' style = 'width:70%;'>"""

print"""</td>
        </tr>
	<tr><td height = '25px'></td></tr>
	<tr>
		<td style ="color:darkred;">Choose a domain: <select name = 'domainslist'>"""
if (len(domainsarray) > 0):
	for domains in domainsarray:
		domains = domains.strip();

                users_file_to_count  = user_files_dir + domains + '-users.txt';
                groups_file_to_count = user_files_dir + domains + '-groups.txt';

                usersfilesarray  = common_methods.read_file(users_file_to_count);
                groupsfilesarray = common_methods.read_file(groups_file_to_count);

		if (domains == domainname):
			print """<option value = '""" + domains + """-""" + str(len(usersfilesarray)) + """-""" + str(len(groupsfilesarray)) + """' selected>""" + domains + """ (""" + str(len(usersfilesarray)) + """, """ + str(len(groupsfilesarray)) + """)</option>""";

		else:
			print """<option value = '""" + domains + """-""" + str(len(usersfilesarray)) + """-""" + str(len(groupsfilesarray)) + """'>""" + domains + """ (""" + str(len(usersfilesarray)) + """, """ + str(len(groupsfilesarray)) + """)</option>""";

print """</select></td></tr>
	<tr>
	<td style ="color:darkred;"><B>Available:</B><BR>
	<input id = 'sssavailable' name = 'ads_user_text' type="text" class = 'input' value = '' onclick = 'document.getElementById("available").style.display = "none"; document.getElementById("available_groups").style.display = "none";'>
<input class = 'input1' type = 'button' name = 'getusers' value = 'Check User'  onclick = 'return get_user_suggestions("", document.getElementById("granted").options, "", "", document.user_acl.domainslist.value, this.form.sssavailable.value, "users", document.user_acl.hid_separator.value, \"""" + get_share + """", "acl", \"""" + str(smbuserslength) + """", \"""" + connstatus + """");' """ + alldisabled + """ >		
<input class = 'input1' type = 'button' name = 'getusers' value = 'Check Group'  onclick = 'return get_user_suggestions("", document.getElementById("granted").options, "", "", document.user_acl.domainslist.value, this.form.sssavailable.value, "groups", document.user_acl.hid_separator.value, \"""" + get_share + """", "acl", \"""" + str(smbgroupslength) + """", \"""" + connstatus + """");' """ + alldisabled + """ >"""		
print """<select name ="avail[]" multiple class="user" id ="avail_id" onkeydown = 'return get_key();' style ='width:200px;height:300px; display: """ + avail_users_style + """;'>"""

if (ug == 'users'):
	#get_users_string = list(set(user_group_list)-set(grant_user))
	#print
	#print get_users_string 
	print get_users_string

elif (ug == 'groups'):
	print get_groups_string;

print"""	</select></td>"""

print """<td><input type = 'button' name = 'moveusers' value = '>' onclick = 'return move_users(this.form.avail_id, this.form.granted, "1");'><br />"""

print """<input type = 'button' name = 'moveusers' value = '<' onclick = 'return move_users(this.form.granted, this.form.avail_id, "2");'><br /></td>"""
print """	<td style ="color:darkred;"><B>Authorised:</B><BR>
	<select id = 'granted' name ="grant_users[]" multiple  selected style ='width:200px;height:300px;margin-right:83%;'>"""
print users_dropdown;
#for auth_user_info in lis_info:
#	print auth_user_info
print """	</select></td>"""

print """ 	<td>
        <button class="button_example" type="submit" name = 'set' id = "set_id" value = 'Acl'>Set</button></td>

	</tr>
	</table>
	 <!--<div style="float:right;margin-top:-3%;">
        <button class="button_example" type="submit" name = 'set_cl' value = 'Acl' onclick =''>Set Acl</button></div>-->
<table id = 'id_table' style="width:100%; margin:20px 0 0 0;border:1px;">


        <tr>
                <td style ="color:#EC1F27; display:"""+display_rwx+""";float:left;">User/Group</td>
                <td style ="color:#EC1F27; display:"""+display_rwx+""";margin-left:20%;">Read</td>
                <td style ="color:#EC1F27; display:"""+display_rwx+""";margin-left:35%;margin-top:-2%;">Write</td>
                <td style ="color:#EC1F27; display:"""+display_rwx+""";margin-left:51%;margin-top:-2%;">Execute</td>
        </tr>"""
if(grant_user == None):
	print"""<th align="left" style="color:darkgreen;""></th>"""
else:
	k = 1
	for users_list in grant_user:
		#users_list = users_list.replace('[', '')
		#users_list = users_list.replace(']', '')
		users_list = users_list.replace('[U]', '')
		users_list = users_list.replace('[G]', '@')
		#if '[U]' in users_list:

		#	users_list = users_list.replace('[U]', '')
		#if '[G]'in users_list:
		#	users_list = users_list.replace('[G]', '')

	
		
		print"""<tr>
				<td align="left" style="color:darkgreen;""><div style="margin-top: 2%;">"""+users_list+"""</div></td >
				
		</tr>
		<tr style="border:solid 1px;">"""
		
		print"""<td style="float:right;width:79%;margin-top:-2%;"><input type="checkbox" name='"""+users_list+"""o_read'"""
		if(chk_dict != {}):
			print chk_dict[users_list+'_chk_read']

		if(lis_info != {}):
			if users_list in lis_info:
				if 'r' in lis_info[users_list]:
					print "checked"
		#else:
               		#print """ """+users_list+"""o_read """
		print """></td>"""

		print"""<td style="float:right;width:64%;margin-top:-2%;"><input type="checkbox" name='"""+users_list+"""o_write'"""
		if(chk_dict != {}):
                        print chk_dict[users_list+'_chk_write']

		if(lis_info != {}):
			if users_list in lis_info:
				if 'w' in lis_info[users_list]:
					print "checked"


		print """></td>"""
		print"""<td style="float:right;width:47%;margin-top:-2%;"><input type="checkbox" name='"""+users_list+"""o_execute'"""
		if(chk_dict != {}):
                        print chk_dict[users_list+'_chk_execute']

		if(lis_info != {}):
			if users_list in lis_info:
				if 'x' in lis_info[users_list]:
					print "checked"


		print """></td>"""
		print """</tr> """
		k = k+1

	print"""<td><input type="hidden" name="hid_k_val" value='"""+str(k)+"""'></td>"""

print"""
<tr>"""
if(recr_val == "on"):
	recr_chk = "checked"
	recr_val = "yes"
else:
	recr_chk = ""
	recr_val = "no"

print"""<td style ="color:#EC1F27;display:"""+display_rwx+""";"><b>Recursive</b>:<input type="checkbox" name='o_recursive' """+recr_chk+""" /></td>"""


print"""</tr>"""
print"""
        </table>
	<div style="float:right;margin-top:-3%;display:"""+display_rwx+""";">
        <button class="button_example" type="submit" id = 'id_butt' name = 'set_acl' value = 'acl'>Set Acl</button></div>
	<input type = 'hidden' name = 'hid_separator' value = '""" + ads_separator + """'>
</form>
</div>
<div id="subtabs-3">
<form name = "perm_form" method = "post" action='' >
<table style="width:84%;margin:20px 0 0 0;">
	<tr>
	<td>Log Path:<input type="text" name = "selected_file" readonly value = '""" + sharepath + """' style = 'width:70%;'></td>
	</tr>
        <tr>
                <th style = "color:#EC1F27;">Read</th>
                <th style = "color:#EC1F27;float: left; margin-left: -72%;">Write</th>
                <th style = "color:#EC1F27;float: left; margin-left: -10%;">Execute</th>
        </tr>

        <tr>
                <th align="left" style="padding:0 0 0 20px; color:#EC1F27;">Owner</th>
                <th style="float: left; margin-left: -129%;"><input type="checkbox" name="o_read" """
if(perms_info != {}):
	if 'r' in owner_perms:
		print "checked"

#print owner_perms


print"""></th>
                <th style="float: left; margin-left:-64%;"><input type="checkbox" name="o_write" """
if(perms_info !={}):
	if 'w' in owner_perms:
		print "checked"


print"""> </th>
                <th style="float: left;"><input type="checkbox" name="o_execute" """

if(perms_info !={}):
	if 'x' in owner_perms:
		print "checked"

print"""></th>
        </tr>

        <tr>
                <th align="left" style="padding:0 0 0 20px; color:#EC1F27;">Group</th>
                <th style="float: left; margin-left: -129%;"><input type="checkbox" name="g_read" """
if(perms_info != {}):
        if 'r' in group_perms:
                print "checked"


print """></th>
                <th style="float: left; margin-left:-64%;"><input type="checkbox" name="g_write" """
if(perms_info != {}):
        if 'w' in group_perms:
                print "checked"


print"""></th>
                <th style="float: left;"><input type="checkbox" name="g_execute" """
if(perms_info != {}):
        if 'x' in group_perms:
                print "checked"


print"""></th>
        </tr>

        <tr>
                <th align="left" style="padding:0 0 0 20px;color:#EC1F27;">Other</th>
                <th style="float: left; margin-left: -129%;"><input type="checkbox" name="ot_read" """

if(perms_info != {}):
        if 'r' in other_perms:
                print "checked"

print"""></th>
                <th style="float: left; margin-left:-64%;"><input type="checkbox" name="ot_write" """

if(perms_info != {}):
        if 'w' in other_perms:
                print "checked"

print"""></th>
                <th style="float: left;"><input type="checkbox" name="ot_execute" """
if(perms_info != {}):
        if 'x' in other_perms:
                print "checked"


print"""></th>
        </tr>
	<tr>
	<td style = "color:#EC1F27;"><input type = "checkbox" name ="sub_inherit">Inherit</td>
	</tr>  

        </table>
	<div style="float:right;margin-top:-3%;">
	<button class="button_example" type = 'submit'  name="change_perm_but" value="change_perm_but" onclick = "return validate_dns_conf();">Change Permission</button></div>

</form>
</div>
<div id="subtabs-4">
<form name="chang_owner_form" method="post"  action='change_ownership.py'>
        <table width="100%">
        <tr>
          <td>Log Path:</td>
                <!--access_control_form.selected_file-->"""

if(path_owner != ''):

        print"""<td colspan = '4'><input type="text" name = "selected_file" readonly value = '""" + path_owner + """' style = 'width:70%;'></td>"""
else:

        print"""<td colspan = '4'><input type="text" name = "selected_file" readonly value = '""" + sharepath + """' style = 'width:70%;'></td>"""
print"""
        </tr>
        <tr>
                <td style="width: 14%;">Select Owner:</td>
                <td>
	 <input type = 'text' class = 'textbox' name = 'assd_user' value = '""" + assusr + """' style = 'width: 60%;' />
	<a href = '#' onclick = 'document.getElementById("id_set_owner").style.display = "table"; document.getElementById("id_set_group").style.display = "none";' style = 'text-decoration: underline;'>Change USER</a><BR><BR></td></tr>
	<tr><td colspan = '2'>
	<div id = 'id_set_owner' style = 'margin-left: 8%; width: 90%; border: 0px solid #BDBDBD; display: """ + users_style + """;'>
	<b style ="color:darkred">Choose a domain:</b> <select name = 'udomainslist' onchange = 'document.chang_owner_form.hid_domain.value = document.chang_owner_form.udomainslist.value;'>"""
if (len(domainsarray) > 0):
	for domains in domainsarray:
		domains = domains.strip();

		users_file_to_count  = user_files_dir + domains + '-users.txt';
		groups_file_to_count = user_files_dir + domains + '-groups.txt';

		usersfilesarray  = common_methods.read_file(users_file_to_count);
		groupsfilesarray = common_methods.read_file(groups_file_to_count);

		if (domains == domainname):
			print """<option value = '""" + domains + """-""" + str(len(usersfilesarray)) + """-""" + str(len(groupsfilesarray)) + """' selected>""" + domains + """ (""" + str(len(usersfilesarray)) + """, """ + str(len(groupsfilesarray)) + """)</option>""";

		else:
			print """<option value = '""" + domains + """-""" + str(len(usersfilesarray)) + """-""" + str(len(groupsfilesarray)) + """'>""" + domains + """ (""" + str(len(usersfilesarray)) + """, """ + str(len(groupsfilesarray)) + """)</option>""";

print """</select><BR>

<input id = 's_sssavailable' name = 'ads_user_text' type="text" class = 'input' value = '' onclick = 'document.getElementById("s_available").style.display = "none"; document.getElementById("s_available_groups").style.display = "none";' style = 'width: 40%;'><input class = 'input1' type = 'button' name = 'getusers' value = 'Check'  onclick = 'return get_user_suggestions("", document.getElementById("id_groups_list").value, "", "", document.chang_owner_form.udomainslist.value, this.form.s_sssavailable.value, "users", document.chang_owner_form.hid_separator.value, \"""" + share_name + """", "ownership", \"""" + str(userslength) + """", \"""" + connstatus + """");' """ + alldisabled + """ >"""
print """<select id = 'id_users_list' name='ass_user' onchange = 'document.chang_owner_form.assd_user.value = document.chang_owner_form.ass_user.value; document.getElementById("id_set_owner").style.display = "none";' style = 'display: """ + users_list_style + """;'>
	<option value = ''>Choose a USER</option>"""
print get_users_string;
print """               </select></div>




		</td>
        </tr>
<tr>
                <td style="width: 14%;">Select Group:</td>
                <td>
                <select name="acl_group" style ='width:200px;margin-right:83%;'>
                <option>root</option>"""
for group_list_info in get_all_groups['groups']:
        print"""
                <option value = '"""+group_list_info+"""'"""
        if(group_name !=''):
                if(group_name == group_list_info):
                        print """selected = 'selected'"""
        print """>"""+group_list_info+"""</option>"""
print"""                </select></td>
        </tr>
        <tr>
        <td>Recursive:</td>"""

if(recur_info == 'on'):
        recr_chk_info = "checked"
        recur_info = "Yes"
else:
        recr_chk_info = ""
        recur_info = "NO"
print"""        <td> <input type = "checkbox" name = "acl_chk_info" """+recr_chk_info+"""></td>"""
print"""
        </tr> 
        </table>
<div style="float:right;margin-top:-3%;">
        <button class="button_example" type="submit" id = 'id_owner' name = 'set_owner' value = 'owner'>Set Owner</button></div>
        </form>
#import perms_ownership
</div>
<div id="subtabs-5">
<form name="acl_info" method="post" action='main.py?page=acl&"""+querystring+"""#subtabs-5'>
<table id = 'id_table' style="width:100%; margin:20px 0 0 0;border:1px;">
	 <tr>
	<td>Log Path:
	<input type="text" name = "selected_file" readonly value = '""" + sharepath + """' style = 'width:50%;margin-bottom:5%;'>
          
	</td></tr>

        <tr>
                <!--<td style ="color:#EC1F27;float:left;">Select User</td>-->
                <td style ="color:#EC1F27;float:left;">User/Group</td>
                <td style ="color:#EC1F27;float:left;margin-left:10%;">Read</td>
                <td style ="color:#EC1F27;float:left;margin-left:19%;">Write</td>
                <td style ="color:#EC1F27;float:left;margin-left:60%;margin-top:-2%;">Execute</td>
                <td style ="color:#EC1F27;float:left;margin-left:75%;margin-top:-2%;">Reset</td>
        </tr>"""
print '<br/>'
if(grant_user == None):
	print"""<th align="left" style="color:darkgreen;""></th>"""
else:
	k = 1
	for users_list in lis_info:
		print"""

			
		<!--<tr>
                                <td align="left" style="color:darkgreen;"><div style="margin-top: 2%;"><input type = "checkbox" name = "user_remove" value =''></div></td>
                                
                </tr>-->
			<tr>
				<td align="left" style="color:darkgreen;""><div style="margin-top: 2%;">"""+users_list+"""</div></td >
				
		<td><input type="hidden" name='"""+users_list+"""user_value'></td>
		</tr>
		<tr style="border:solid 1px;">"""
		
		print"""<td style="float:right;width:78%;margin-top:-2%;"><input type="checkbox" name='"""+users_list+"""o_read'"""
		if(chk_perm != {}):
			print chk_perm[users_list+'_chk_read']

		if(lis_info != {}):
			if 'r' in lis_info[users_list]:
				print "checked"
		#else:
		#	print """ """+users_list+"""o_read """
		print """></td>"""

		print"""<td style="float:right;width:55%;margin-top:-2%;"><input type="checkbox" name='"""+users_list+"""o_write'"""
		if(chk_perm != {}):
                        print chk_perm[users_list+'_chk_write']

		if(lis_info != {}):
			if 'w' in lis_info[users_list]:
				print "checked"


		print """></td>"""
		print"""<td style="float:right;width:38%;margin-top:-2%;"><input type="checkbox" name='"""+users_list+"""o_execute'"""
		if(chk_perm != {}):
                        print chk_perm[users_list+'_chk_execute']

		if(lis_info != {}):
			if 'x' in lis_info[users_list]:
				print "checked"


		print """></td>"""
		#print"""<td style="float:right;width:25%;margin-top:-2%;"><input type="submit" name = '"""+users_list+"""reset_single' value = "reset"></td>"""
		print"""<td style="float:right;width:26%;margin-top:-3%;"><button type="image" value = "reset" name='"""+users_list+"""reset_single' style="background: #fff; border: 0px;cursor:pointer;" ><img src="../images/reset_acl_img2.png"></button></td> """
		#print """<td style="float:right;width:27%;margin-top:-3%;border: medium none;"><button><input type="submit" name= '"""+users_list+"""reset_single' style="display: none;" value "reset" ><img src="../images/reset_acl5.png"></button></td>  """
		print """</tr> """
		k = k+1

	print"""<td><input type="hidden" name="hid_k_val" value='"""+str(k)+"""'></td>"""

print"""
<tr>"""
if(recur_info == "on"):
	recr_chk = "checked"
	recur_info = "yes"
else:
	recr_chk = ""
	recur_info = "no"

print"""<td style ="color:#EC1F27;"><div style="margin-top: 3%;"><b>Recursive</b>:<input type="checkbox" name='o_recursive' """+recr_chk+""" /></div></td>"""


print"""</tr>"""
print"""
        </table>

<div style="float:right;margin-top:-3%;">
        <button class="button_example" type="submit" name = 'acl_user_del' value = 'info'>Reassign</button></div>
</form>
</div>
<div id="subtabs-6">
<form name= "reset_acl_form" method= "post">
	<table width="98%">
	 <tr>
          <td>Log Path:</td>
                <!--access_control_form.selected_file-->
          <td colspan = '4'><input type="text" name = "selected_file" readonly value = '""" + sharepath + """' style = 'width:70%;'></td>
        </tr>
	<tr>
	<td>Recursive:</td>"""
if(reset_chk == 'on'):
	reset_chk_but = 'checked'
	reset_chk = "yes"
else:
	reset_chk_but = ""
	reset_chk = "no"
	
print"""	<td><input type="checkbox" name= "check_reset" """+reset_chk_but+"""></td>"""
print"""	</tr>
</table>
	<div style="float:right;margin-top:-3%;">
        <button class="button_example" type="submit" name = 'reset_acl' value = 'Reset' onclick =''>Reset</button></div>

</form>

</div>

</div>
<!--form container ends here-->
<input type = 'hidden' name = 'hid_dir_file' />
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
<!-- ####### Sub Tabs Start ####### -->

<script>
$("#tabs, #subtabs").tabs();
$("#tabs, #subsubtabs").tabs();
</script>



<!-- ####### Sub Tabs End ####### -->
"""
