#!/usr/bin/python
#enable debugging
import traceback

import sys;
sys.path.append('../modules/');
import disp_except;
try:
	import cgitb, sys, common_methods, os, include_files, cgi
	cgitb.enable()
	#-------------------------------------Import modules ------------------------------------------
	sys.path.append('/var/nasexe/python/');
	import ads
	import smb, tools, commons
	from tools import acl
	from fs2global import *;
	#-----------------------------------------End--------------------------------------------------
	form = cgi.FieldStorage()

	ads_sep=ads.get_separator()
	#print ads_sep
	#print 'Content-Type: text/html'
	#-------------------------Assigned empty value for the given value------------------------------------------------
	get_share = ''
	sharepath = ''
	grant_user = ''
	set_path_acl = ''
	read_check =''
	read_per = ''
	write_check = ''
	execute_check = ''
	write_per = ''
	execute_per = ''
	display_rwx = "none"
	display_acl_but = "none"
	perm_path = ''
	owner_name = ''
	group_name = ''
	path_owner = ''
	reset_chk_but = ''
	reset_chk = ''
	alldisabled = '';
	ads_separator = '';
	ads_separator = tools.get_ads_separator();

	domainsarray = [];
	domainname = '';
	avail_users_style = 'none';
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
	display_table = 'none'
	#------------------------------------------------------------------------End--------------------------------------------------------------------
	#set_group = 'root'
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

	#--------------Display for User And Group Code Comment BY Sanjeev date 19-09-2014 Not needed-----------------------
	#get_all_users = manage_users.get_smb_users()
	#print get_all_users

	#get_all_groups = manage_users.get_sys_groups()
	#print get_all_groups
	#--------------------------End------------------------------------
	#-------------get auth mode and get all users---------------------------
	connstatus = common_methods.conn_status();

	domainsarray = common_methods.get_all_domains();

	all_users_list  = common_methods.get_users_string();
	all_groups_list = common_methods.get_groups_string();

	smb_all_users_array  = [];
	smb_all_groups_array = [];

	# if userslist is not empty
	#if (all_users_list['id'] == str(0)):
	if (all_users_list['id'] == 0):
		smb_all_users_array  = all_users_list['users'];
		smbuserslength       = len(smb_all_users_array);

	# if groupslist id not empty
	#if (all_groups_list['id'] == str(0)):
	if (all_groups_list['id'] == 0):
		smb_all_groups_array = all_groups_list['groups'];
		smbgroupslength      = len(smb_all_groups_array);
	#---------------------End-------------------------------------
	#--------Comment BY Sanjeev date 19-09-2014 Not needed ----------
	#user_group_list = [];

	#for user_lst in get_all_users['users']:
		
	#	user_name = '[U]'+str(user_lst)
		#print 'UU:'+str(user_name)
		
	#	user_group_list.append(user_name);
	#print '<br/>'
	#print get_all_groups
	#for group_lst  in get_all_groups['groups']:
	#	group_name = '[G]'+str(group_lst)
	#	user_group_list.append(group_name)
	#------------------End----------------------
	#print get_all_users
	#for t in user_group_list:
	#	print t
	##
	#print user_group_list
	#---------------------------End------------------------------------

	#-------------------------Get Log Path-------------------------------
	array_user = []
	array_group = []
	array_ads_user = []
	array_ads_group =[]
	querystring = os.environ['QUERY_STRING'];
	#print querystring
	if (querystring.find('share_name=') >= 0):
		if (querystring.find('&dom=') > 0):
			get_share = querystring[querystring.find('share_name=') + len('share_name='):querystring.find('&dom=')];

		else:
			get_share = querystring[querystring.find('share_name=') + len('share_name='):];
	#--------------End---------------------------------------
	#sharepath = '';

	#-----------------This code use for Check Option-----------------------------
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
				#print get_users
				if (get_users != ''):
					get_users = get_users.strip();
					if(get_users == ''):
						get_users = ''
					else:
					
						get_users = '[U]' + get_users;
						checkuserexists = tempstring.find(':::' + get_users + ':::');
						get_usersinternal = common_methods.replace_chars(get_users, 'chartotext');
						get_disp_users    = get_users[get_users.find('\\') + 1:];

						check_users = '"' + get_users + '"';
						if (checkuserexists < 0):
							get_usersinternal = get_usersinternal.replace('[DOT]', '.')
							get_usersinternal = get_usersinternal.replace('[DOLLAR]', '$')
							#print get_usersinternal
							#array_user.append(get_disp_users)
							array_user.append(get_usersinternal)
							#get_users_string += '<option value = "' + get_usersinternal + '">' + get_disp_users + '</option>';

		if (ug == 'groups'):
			avail_users_style = 'block';

			get_groups_array = [];
			get_groups_array = common_methods.read_file('aclsearchgroupsfile.txt');

			for get_groups in get_groups_array:
				get_groups12 = '[G]'+get_groups
				#print get_groups12
				if (get_groups != ''):
					get_groups = get_groups.strip();
					get_groups = '[G]' + get_groups;
					#print 'TEST:'+str(get_groups)

					checkuserexists = tempstring.find(':::' + get_groups + ':::');
					#print checkuserexists
					get_groupsinternal = common_methods.replace_chars(get_groups, 'chartotext');
					#print get_groupsinternal
					get_disp_groups    = get_groups[get_groups.find('\\') + 1:];
					
					#-New:[G]mygroup New:[G]group.netweb New:[G]vtl---------
					get_disp_ads_groups = '[G]'+ get_disp_groups
					#print 'New:'+str(get_disp_ads_groups)
					

					if (checkuserexists < 0):
						get_groupsinternal = get_groupsinternal.replace('[DOT]', '.')
						get_groupsinternal = get_groupsinternal.replace('[DOLLAR]', '$')
						array_group.append(get_groupsinternal)
						#array_ads_group.append(get_disp_ads_groups)
						#print array_group
						#get_groups_string += '<option value = "' + get_groupsinternal + '">' + get_disp_groups + '</option>';

	sharedetails = tools.get_share(get_share);

	assgroupsarray = [];
	assgroupsarray = common_methods.read_file('aclassgroupsfile');

	users_dropdown = '';

	share_path = ''
	line_path = ''
	set_path = ''
	if (sharedetails['id'] == 0):
		sharesinfo = sharedetails['share'];
		sharepath  = sharesinfo['path'];
		share_path = sharesinfo['path'];
		#print share_path
		sharepath  = sharepath.replace('/storage/', '');

	lpath = ''
        acldisabled = ''
        check_log_path = tools.get_string_from_file('SMBLOGPATH=', '/var/nasconf/smb-log.conf')
        if (check_log_path != 'not found'):
                temparr = [];
                temparr = check_log_path.split('=');
                d12   = temparr[0]
                lpath = temparr[1]
        if (share_path == lpath):
                acldisabled = 'disabled'

		#print sharepath
	#print '<br/>'
	read_file = open('acl_path.txt', 'r')
	for line in read_file:

		line_path = line
	set_path = line_path
	#-------------------ADD Updated Path---------------
	#---------------Compare Path-----------------------
	if sharepath not in  set_path:
	
		set_path = ''
	else:
		set_path =set_path

	#------------------End------------------------------
	nw_path = []
	if(form.getvalue('selected_file')):
		set_path =form.getvalue('selected_file')
		filetowrite = "acl_path.txt"
		acl_cont = []
		acl_cont.append(set_path)
		commons.write_file(filetowrite, acl_cont)
	#----------------------End---------------
	check_path_exists = tools.is_dir_exist('/storage/'+set_path)
	perms_info = ''
	lis_info = {}
	owner_perms = ''
	group_perms = ''
	other_perms = ''
	if(check_path_exists == True):
		#print share_path
		lis_info = acl.get_acl('/storage/'+set_path)
		#print '<br/>'
	#------------------permissiion----------------------
		perms_info = acl.get_acl('/storage/'+set_path)
		owner_perms = perms_info['d_user']
		group_perms = perms_info['d_group']
		other_perms = perms_info['d_other']
		set_owner = perms_info['owner']
		set_group = perms_info['group']
		
		
	else:
		common_methods.sendtologs('ERROR', 'Get Acl', 'UI', '"set_acl_page.py, tools.acl.get_acl()" ' + str(perms_info));

	if(lis_info != {}):
		lis_info = lis_info['acl']
		#print lis_info
	else:
		lis_info = {}

	#-------------------------End-----------------------------------

	acl_dict = {}
	acl_ads_dict = {}
	chk_dict = {}
	acl_perm ={}
	chk_perm ={}
	#acl_fax = {}
	#print 'SET'+str(set_path)
	#-------------------Set User----------------------------
	if(form.getvalue('set')):
		set_path = form.getvalue('selected_file')
		#print 'SET P:'+str(set_path)
		get_hid_k_val = form.getvalue("hid_k_val")
		avail_user = form.getvalue('avail[]')
		grant_user = form.getvalue('grant_users[]')
		#print 'Avail:'+str(avail_user)
		#print '<br/>'
		#print 'Grant:'+str(grant_user)
		if(isinstance(grant_user, str) == True ):
			grant_user = [grant_user]
			#grant_user = grant_user.replace('[DOT]', '.')
			#grant_user = grant_user.replace('[U]', '')
			#grant_user =grant_user.replace('[G]', '')
		
		#print """<script>location.href = 'main.py?page=acl&"""+querystring+"""#subtabs-2';</script>"""
		display_rwx = "block"
	#---------------------------End------------------------------------



	#----------------------Set Acl---------------------------------
	if(form.getvalue('set_acl')):
		select_domain = form.getvalue('domainslist')
		select_domain_sep = select_domain[:select_domain.find('-')]
		#print select_domain_sep
		set_path_acl = form.getvalue('selected_file')
		set_path = set_path_acl
		#print 'SET P ACL:'+str(set_path_acl)
		set_path_acl_add = '/storage/'+set_path_acl
		
		avail_user_acl = form.getvalue('avail[]')
		#print avail_user_acl
		get_hid_k_val = form.getvalue("hid_k_val")
		grant_user = form.getvalue('grant_users[]')
		#print grant_user
		#print '<br/>'
		#print 'GRANT USER:'+str(grant_user)
		recr_val = form.getvalue('o_recursive') 
		if(isinstance(grant_user, str) == True ):
			grant_user = [grant_user]
		
		#for group_lst  in get_all_groups['groups']:
		#	group_lst = '[G]'+str()
		#	print '<br/>'
		#	print 'GROUP:'+str(group_lst)
		#	print '<br/>'
			#print '<br/>'
			#print '<br/>'
		for u in grant_user:
			u = u.replace('[U]', '')
			u = u.replace('[G]', '@')
			u = u.replace('[DOT]', '.')
			#print 'Auth User:'+str(u)
			#chk_dict[u+'_chk_read']=""
			#chk_dict[u+'_chk_write']=""
			#chk_dict[u+'_chk_execute']=""
			#print '<br/>'
			if((form.getvalue(u+'o_read') == "on") and (form.getvalue(u+'o_write') == "on") and (form.getvalue(u+'o_execute') == "on" )):
				acl_dict.update({u:'rwx'})
				chk_dict.update({u+'_chk_read':'checked',u+'_chk_write':'checked',u+'_chk_execute':'checked'})
				

			if((form.getvalue(u+'o_read') == "on") and (form.getvalue(u+'o_write') == None) and (form.getvalue(u+'o_execute') == None )):	
				acl_dict.update({u:'r--'})
				chk_dict.update({u+'_chk_read':'checked',u+'_chk_write':'',u+'_chk_execute':''})
				

			if((form.getvalue(u+'o_read') == "on") and (form.getvalue(u+'o_write') == "on") and (form.getvalue(u+'o_execute') == None )):
				acl_dict.update({u:'rw-'})
				chk_dict.update({u+'_chk_read':'checked',u+'_chk_write':'checked',u+'_chk_execute':''})
			
			if((form.getvalue(u+'o_read') == None) and (form.getvalue(u+'o_write') == "on") and (form.getvalue(u+'o_execute') == "on" )):
				acl_dict.update({u:'-wx'})
				chk_dict.update({u+'_chk_read':'',u+'_chk_write':'checked',u+'_chk_execute':'checked'})

			if((form.getvalue(u+'o_read') == "on") and (form.getvalue(u+'o_write') == None) and (form.getvalue(u+'o_execute') == "on" )):
				acl_dict.update({u:'r-x'})
				chk_dict.update({u+'_chk_read':'checked',u+'_chk_write':'',u+'_chk_execute':'checked'})
			
			if((form.getvalue(u+'o_read') == None) and (form.getvalue(u+'o_write') == None) and (form.getvalue(u+'o_execute') == "on" )):
				acl_dict.update({u:'--x'})
				chk_dict.update({u+'_chk_read':'',u+'_chk_write':'',u+'_chk_execute':'checked'})

			if((form.getvalue(u+'o_read') == None) and (form.getvalue(u+'o_write') == None) and (form.getvalue(u+'o_execute') == None )):
				acl_dict.update({u:'---'})
				chk_dict.update({u+'_chk_read':'',u+'_chk_write':'',u+'_chk_execute':''})
			
			if((form.getvalue(u+'o_read') == None) and (form.getvalue(u+'o_write') == "on") and (form.getvalue(u+'o_execute') == None )):
				acl_dict.update({u:'-w-'})
				chk_dict.update({u+'_chk_read':'',u+'_chk_write':'checked',u+'_chk_execute':''})
		
		#print chk_dict	
		#print 'CHK:'+str(acl_ads_dict)
		#print '<br/>'
		#print '<br/>'
		#print '<br/>'
		#print 'CHK1:'+'/'+str(select_domain_sep)+str(acl_dict)
		check_append_status = acl.attr(set_path_acl_add, op='get')
                #print check_append_status
                if(check_append_status == True):
                        print """<script>jAlert("<img src='../images/info.gif' style='margin-bottom: -21px; margin-left: -35px;'><div>Append Mode is enabled for this path, can't set the ACL!</div>" , 'Append Alert ');</script>"""
		else:
#if(select_domain_sep == 'local'):
			set_acl_code = acl.set_acl(set_path_acl_add,acl_dict,recr_val)
			if(set_acl_code == True):
		
				print "<div id='id_trace'>"
				print "ACL successfully Set!"
				print "</div>"
				#logstatus = common_methods.sendtologs('Success', 'Acl Succefully set', 'UI','set_acl_page.py'+ str(set_acl_code));
			else:
				print "<div id='id_trace_err'>"
				print "Disk not mounted!"
				#print "Error Occured while Setting the ACL!"
				print "</div>"

		#else:
		#	if('[G]' in grant_user):
		#		set_acl_ads_code = acl.set_acl(set_path_acl_add,acl_ads_dict,recr_val)
		#print "SET:"+str(set_acl_code)
		#	if(set_acl_ads_code == True):
		
		#		print "<div id='id_trace'>"
		#		print "Acl successfully Set!"
		#		print "</div>"
		#		logstatus = common_methods.sendtologs('Success', 'Acl Succefully set', 'UI','set_acl_page.py'+ str(set_acl_ads_code));
		#	else:
		#		print "<div id='id_trace_err'>"
		#		print "Error Occured while Setting the acl!"
		#		print "</div>"
		#		logstatus = common_methods.sendtologs('Error', 'Error Occured during set the Acl', 'UI','set_acl_page.py'+ str(set_acl_ads_code));
		
		#print "<script>location.href = 'main.py?page=acl#subtabs-3';</script>"
		#print """<script>location.href = 'main.py?page=acl&"""+querystring+"""#subtabs-2';</script>"""
		#print "<script>location.href = 'set_acl_page.py?share_name=%s#subtabs-2';</script>" % share_name;

		display_rwx = "block"
	#-----------------------------------End-------------------------------

	#-----------------Set Owner------------------------------------------


	if(form.getvalue("re_assign_ownership")):
                share_path = form.getvalue('acl_path')
		set_path = share_path
		share_path_add = '/storage/'+share_path
		#print share_path_add
                set_owner  = form.getvalue('assd_user')
		#print set_owner
                set_group  = form.getvalue('assd_group')
		#print set_group
                recursive  = form.getvalue('inherit_ownership')
		#print recursive
		if (recursive == 'on'):
                        recursive = 'YES'
			#print recursive

                else:
                        recursive = 'NO'
			#print recursive
		check_append_status = acl.attr(share_path_add, op='get')
                #print check_append_status
                if(check_append_status == True):
                        print """<script>jAlert("<img src='../images/info.gif' style='margin-bottom: -21px; margin-left: -35px;'><div>Append Mode is enabled for this path, can't set the ownership!</div>" , 'Append Alert ');</script>"""
		else:
			ownership_status = acl.set_ownership(share_path_add, set_owner, set_group, recursive)
			#owner_cmd = acl.set_ownership(path_owner_add,owner_name,group_name,recur_info)
			#print "Owner Cmd:"+str(owner_cmd)
			if(ownership_status == True):
				print"<div id = 'id_trace'>"
				print "Succesfully Set the Ownership"
				print "</div>"
				
			else:
				print"<div id = 'id_trace_err'>"
				print "Error Occured While Setting the Ownership"
				print "</div>"
			print "<script>location.href = 'iframe_set_acl_page.py#subtabs-4';</script>"

	#---------------------------End---------------------------------------
	#---------------------------Reset OwnerShip---------------------------------
	if(form.getvalue('reset_ownership')):
		share_path_o = form.getvalue('acl_path')
		set_path = share_path_o
		share_path_adds = '/storage/'+share_path_o
		set_owner = 'root'
		set_group = 'root'
		
		recursive  = form.getvalue('inherit_ownership')
		if (recursive == 'on'):
                        recursive = 'YES'
                        #print recursive

                else:
                        recursive = 'NO'
                        #print recursive
		check_append_status = acl.attr(share_path_adds, op='get')
                #print check_append_status
                if(check_append_status == True):
                        print """<script>jAlert("<img src='../images/info.gif' style='margin-bottom: -21px; margin-left: -35px;'><div>Append Mode is enabled for this path, can't reset the ownership!</div>" , 'Append Alert ');</script>"""
		else:
		
			ownership_status = acl.set_ownership(share_path_adds, set_owner, set_group, recursive)
			#owner_cmd = acl.set_ownership(path_owner_add,owner_name,group_name,recur_info)
			#print "Owner Cmd:"+str(owner_cmd)
			if(ownership_status == True):
				print"<div id = 'id_trace'>"
				print "Succesfully Re-set the Ownership"
				print "</div>"

			else:
				print"<div id = 'id_trace_err'>"
				print "Error Occured While Re-Setting the Ownership"
				print "</div>"

		
		#print "<script>location.href = 'iframe_set_acl_page.py#subtabs-4';</script>"
	#------------------------------End------------------------------------------
	#--------------------Reset Acl-------------------------------------
	if(form.getvalue("reset_acl")):
		path_reset = form.getvalue("selected_file")
		set_path = path_reset
		path_reset =  '/storage/'+path_reset
		reset_chk = form.getvalue("check_reset")


		reset_acl_func =acl.reset_acl(path_reset,reset_chk) 
		
		if(reset_acl_func == True):
			print"<div id = 'id_trace'>"
			print "Succesfully Remove the ACL"
			print "</div>"
			#logstatus = common_methods.sendtologs('Success', 'Acl Succefully Reset', 'UI','set_acl_page.py'+ str(reset_acl_func));
		else:
			print"<div id = 'id_trace_err'>"
			print "Error Occured While Removing the ACL"
			print "</div>"
			#logstatus = common_methods.sendtologs('Error', 'Error Occured while Reseting Acl', 'UI','set_acl_page.py'+ str(reset_acl_func));
		#print "<script>location.href = 'iframe_set_acl_page.py#subtabs-6';</script>"
		#print """<script>location.href = 'main.py?page=acl&"""+querystring+"""#subtabs-6';</script>"""

	#------------------------------End------------------------------


	#----------------------Acl User Permission--------------------------------

	if(form.getvalue("acl_user_del")):
		info_path = form.getvalue("selected_file")
		set_path = info_path
		#print set_path
		info_path_add = '/storage/'+info_path
		select_check_user = form.getvalue("user_remove")
		#print 'Rem:'+str(select_check_user)
		inf_recr = form.getvalue("o_recursive")
		for acl_info_perm in lis_info:
			#print acl_info_perm
			if((form.getvalue(acl_info_perm+'o_read') == "on") and (form.getvalue(acl_info_perm+'o_write') == "on") and (form.getvalue(acl_info_perm+'o_execute') == "on" )):
				acl_perm.update({acl_info_perm:'rwx'})
				chk_perm.update({acl_info_perm+'_chk_read':'checked',acl_info_perm+'_chk_write':'checked',acl_info_perm+'_chk_execute':'checked'})
				

			if((form.getvalue(acl_info_perm+'o_read') == "on") and (form.getvalue(acl_info_perm+'o_write') == None) and (form.getvalue(acl_info_perm+'o_execute') == None )):	
				acl_perm.update({acl_info_perm:'r--'})
				chk_perm.update({acl_info_perm+'_chk_read':'checked',acl_info_perm+'_chk_write':'',acl_info_perm+'_chk_execute':''})
				

			if((form.getvalue(acl_info_perm+'o_read') == "on") and (form.getvalue(acl_info_perm+'o_write') == "on") and (form.getvalue(acl_info_perm+'o_execute') == None )):
				acl_perm.update({acl_info_perm:'rw-'})
				chk_perm.update({acl_info_perm+'_chk_read':'checked',acl_info_perm+'_chk_write':'checked',acl_info_perm+'_chk_execute':''})
			
			if((form.getvalue(acl_info_perm+'o_read') == None) and (form.getvalue(acl_info_perm+'o_write') == "on") and (form.getvalue(acl_info_perm+'o_execute') == "on" )):
				acl_perm.update({acl_info_perm:'-wx'})
				chk_perm.update({acl_info_perm+'_chk_read':'',acl_info_perm+'_chk_write':'checked',acl_info_perm+'_chk_execute':'checked'})

			if((form.getvalue(acl_info_perm+'o_read') == "on") and (form.getvalue(acl_info_perm+'o_write') == None) and (form.getvalue(acl_info_perm+'o_execute') == "on" )):
				acl_perm.update({acl_info_perm:'r-x'})
				chk_perm.update({acl_info_perm+'_chk_read':'checked',acl_info_perm+'_chk_write':'',acl_info_perm+'_chk_execute':'checked'})
			
			if((form.getvalue(acl_info_perm+'o_read') == None) and (form.getvalue(acl_info_perm+'o_write') == None) and (form.getvalue(acl_info_perm+'o_execute') == "on" )):
				acl_perm.update({acl_info_perm:'--x'})
				chk_perm.update({acl_info_perm+'_chk_read':'',acl_info_perm+'_chk_write':'',acl_info_perm+'_chk_execute':'checked'})

			if((form.getvalue(acl_info_perm+'o_read') == None) and (form.getvalue(acl_info_perm+'o_write') == None) and (form.getvalue(acl_info_perm+'o_execute') == None )):
				acl_perm.update({acl_info_perm:'---'})
				chk_perm.update({acl_info_perm+'_chk_read':'',acl_info_perm+'_chk_write':'',acl_info_perm+'_chk_execute':''})
			
			if((form.getvalue(acl_info_perm+'o_read') == None) and (form.getvalue(acl_info_perm+'o_write') == "on") and (form.getvalue(acl_info_perm+'o_execute') == None )):
				acl_perm.update({acl_info_perm:'-w-'})
				chk_perm.update({acl_info_perm+'_chk_read':'',acl_info_perm+'_chk_write':'checked',acl_info_perm+'_chk_execute':''})
		
		set_acl_perms = acl.set_acl(info_path_add,acl_perm,inf_recr)

		if(set_acl_perms == True):
			print"<div id = 'id_trace'>"
			print "Succesfully Update the Permission"
			print "</div>"
			#logstatus = common_methods.sendtologs('Success', 'Succefully Update the Acl User Permission', 'UI','set_acl_page.py'+ str(set_acl_perms));
		else:
			print"<div id = 'id_trace_err'>"
			print "Error Occured While Updating the Permission"
			print "</div>"
		#print "<script>location.href = 'iframe_set_acl_page.py#subtabs-5';</script>"
			#logstatus = common_methods.sendtologs('Error', 'Error Occurred during Update the Acl User Permission', 'UI','set_acl_page.py'+ str(set_acl_perms));

		
		#print "SET:"+str(set_acl_perms)
		#print """<script>location.href = 'main.py?page=acl&"""+querystring+"""#subtabs-5';</script>"""
		#print "<script>location.href = 'iframe_set_acl_page.py#subtabs-5';</script>"
	#-------------------End--------------------------------------

	#--------------------Change Permission------------------------------
	if(form.getvalue("change_perm_but")):
		perm_path = form.getvalue("selected_file")
		set_path = perm_path
		perm_path_add = '/storage/'+perm_path
		check_append_status = acl.attr(perm_path_add, op='get')
                #print check_append_status
                if(check_append_status == True):
                        print """<script>jAlert("<img src='../images/info.gif' style='margin-bottom: -21px; margin-left: -35px;'><div>Append Mode is enabled for this share, can't set the permissions!</div>" , 'Append Alert ');</script>"""
		else:
			#print 'PATH:'+str(perm_path_add)
			get_o_read = form.getvalue("o_read")
			get_o_write = form.getvalue("o_write")
			get_o_execute = form.getvalue("o_execute")
			get_g_read = form.getvalue("g_read")
			get_g_write = form.getvalue("g_write")
			get_g_execute = form.getvalue("g_execute")
			get_ot_read = form.getvalue("ot_read")
			get_ot_write = form.getvalue("ot_write")
			get_ot_execute = form.getvalue("ot_execute")
			get_sub_inherit = form.getvalue("sub_inherit")
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
			#print share_permission
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
				#logstatus = common_methods.sendtologs('Success', 'Succefully Change the Share Permission', 'UI','set_acl_page.py'+ str(set_perm_cmd));
			else:
				print "<div id='id_trace_err'>"
				print "Error setting permission!"
				print "</div>"
			
			#logstatus = common_methods.sendtologs('Error', 'Error Occurred Change the Share Permission', 'UI','set_acl_page.py'+ str(set_perm_cmd));


		#print """<script>location.href = 'iframe_set_acl_page.py#subtabs-3';</script>"""
	#-------------------End-----------------------------------------------------


	#------------------Reset Single user-----------------------------------------

	for reset_info in lis_info:
		reset_lis_info =  reset_info + 'reset_single';
		if(form.getvalue(reset_info+"reset_single")):
			reset_path = form.getvalue('selected_file')
			set_path = reset_path
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
				print "successfully Remove the User!"
				print "</div>"
				
				#logstatus = common_methods.sendtologs('Success', 'Succefully Reset the Single User', 'UI','set_acl_page.py'+ str(reset_cmd));
			else:
				print "<div id='id_trace_err'>"
				print "Error Occured while Removing!"
				print "</div>"
				
				#logstatus = common_methods.sendtologs('Error', 'Error Occurred while Reset the Single User', 'UI','set_acl_page.py'+ str(reset_cmd));
			#print header.form.getvalue(reset_info+'reset_single')
			#print "<script>location.href = 'iframe_set_acl_page.py#subtabs-5';</script>"
			#print """<script>location.href = 'main.py?page=acl&"""+querystring+"""#subtabs-5';</script>"""

	#------------------------End-----------------------------------------------

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
		#print groups
		users_dropdown += '<option value = "' + groups + '" selected>' + groups + '</option>'; 
	#print users_dropdown
	#print get_users_string

	#----------Set Path 1st tab---------------
	if(form.getvalue('set_p')):
		set_path = form.getvalue('selected_file')
		add_set_path = '/storage/'+set_path
		check_append_status = acl.attr(add_set_path, op='get')
		#print check_append_status
		if(check_append_status == True):
                        print """<script>jAlert("<img src='../images/info.gif' style='margin-bottom: -21px; margin-left: -35px;'><div>Append Mode is enabled for this share, can't set the path!</div>" , 'Append Alert ');</script>"""

		#if(set_path != ''):
		else:
			print"""<div id = 'id_trace'>"""
                	print "Successfully Set the Path!"
                        print "</div>"
		
			
		#set_path = form.getvalue('share_hid_path')
		#print set_path

	#----------End-----------------------
	perms_info = acl.get_acl("/storage/"+set_path)
	owner_perms = perms_info['d_user']
        group_perms = perms_info['d_group']
        other_perms = perms_info['d_other']
	set_owner = perms_info['owner']
	set_group = perms_info['group']
	lis_info = acl.get_acl("/storage/"+set_path)
	#print lis_info
	lis_info = lis_info["acl"]

	if(form.getvalue("action")):
		if(form.getvalue("action") == 'own_value'):
                	print"""<div id = 'id_trace'>"""
                       	print "Successfully Set the Ownership!"
                       	print "</div>"
		else:
                        print"""<div id = 'id_trace_err'>"""
                        print "Error occured while Setting the Ownership!"
                        print "</div>"
		print "<script>location.href = 'iframe_set_acl_page.py#subtabs-4';</script>"
	
	#print 'Array:'+str(array_ads_group)
	#print 'Array:'+str(array_group)
	#import left_nav
	print """
	<!--Right side body content starts from here-->
	      <div class="rightsidecontainer" style="overflow:hidden;">
		<div style="margin:0 0 0px 0;" class="topinputwrap-heading">ACL Settings</div>
		<!--<div style="padding:5px;font-weight:bold;"><a href = 'main.py?page=cs'><img style="float:right; padding:0 10px 2px 0;" title = 'Back to shares' src = '../images/gobacktoshares.png' /></a></div>-->
		<!--tab srt-->
		    <!--<div id="tabs">
		      <ul>
			<li><a href="#tabs-1">ACL Configuration</a></li>
		      </ul>
	<div id="tabs-1">-->
		<div class="searchresult-container">
		  <div class="infoheader">
		<div style="display: none;" id="blanket"></div>
		<!--form container starts here-->
		<form name = 'access_control_form' method="post">
		<div id="subtabs" style="margin-top: -13px;border-right: 1px solid AAAAAA; width: 750px;">

			  <ul>
			    <li><a href="#subtabs-1">Set Share Path</a></li>
			    <li><a href="#subtabs-2">Create ACL</a></li>
			    <li><a href="#subtabs-3">Share Permission</a></li>
			    <li><a href="#subtabs-4">Ownership</a></li>
			    <li><a href="#subtabs-5">ACL User/Group Info</a></li>
			    <li><a href="#subtabs-6">Remove ACL</a></li>
			  </ul>
		 <div id="subtabs-1">"""
	print"""<table width="100%">
		<tr>
		<td style="color:#666666; font-weight:600;">Folder:</td>
		<td colspan = '4'>
		<iframe style = 'border: 1px dotted;' src = 'show_dir1.py?share_name=""" + get_share + """&path=""" + sharepath + """&s=s'></iframe>
		<input type="hidden" name="share_name" value='"""+get_share+"""' />
		</td>
		</tr>
		  <tr>
		  <td style="color:#666666; font-weight:600;">Share Path:</td>
			<!--access_control_form.selected_file-->
		<input type="hidden" name="share_hid_path" value='"""+set_path+"""' />
		  <td colspan = '4'>"""

	if(set_path !=''):
		print"""<input type="text" class = 'textbox' name = "selected_file" readonly value = '""" + set_path + """' style = 'width:51.5%;margin-top:2%;'>"""

	else:
		
		print"""<input type="text" class = 'textbox' name = "selected_file" readonly value = '""" + sharepath + """' style = 'width:51.5%;margin-top:2%;'>"""
	print"""


	</td>
		</tr>
		</table>"""
	print"""<div style="float:right;margin-top:-6%;">
		<div class="buttonWrapper">
		<button class="buttonClass" type="submit" name = 'set_p'  id = 'id_create_but'  value = 'set_p'>Set Path</button></div></div>
		  </div>"""
	print"""
	</form>


	<div id="subtabs-2">
	<form name= "user_acl" method = "post" action=''>"""
	#if(get_all_users['users'] != []):
        print"""<table style="width:100%; margin:20px 0 0 0; ">"""
	#else:
	#	print"""<table style="width:100%; margin:20px 0 0 0;display:none;">"""
	#print """<div style="text-align:center; height:30px; margin:20px 0 20px 0;">No User present For Acl! <a href="main.py?page=mu" style = 'text-decoration:underline;'>Add User</a><br/><br/></div>"""
	print"""
		 <tr>
		  <td style="color:#666666;font-weight:600;">Share Path:</td>
			<!--access_control_form.selected_file-->
		 <input type="hidden" name="share_name" value='"""+get_share+"""' />
		<input type="hidden" name="share_hid_path" value='"""+set_path+"""' />
		  <td colspan = '4'>"""
	if(set_path !=''):
		print"""<input type="text" class = 'textbox' name = "selected_file" readonly value = '""" +set_path+ """' style = 'width:70%;margin-left:-24%;'>"""
	else:

		print"""<input type="text" class = 'textbox' name = "selected_file" readonly value = '""" + sharepath + """' style = 'width:70%;margin-left:-24%;'>"""

	print"""</td>
		</tr>
		<tr><td height = '25px'></td></tr>
		<tr>
			<td style="color:#666666; font-weight:600;">Choose a domain:<div class="styled-select2" style="width:184px;"><select name = 'domainslist'>
		<option value ='sel_domain'>Select Domain</option>
		"""
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

	print """</select></div></td></tr>
		<tr>
		<td style="color:#666666; font-weight:600;">Available:<BR>
		<input id = 'sssavailable' name = 'ads_user_text' type="text" class = 'textbox' value = '' onclick = 'document.getElementById("available").style.display = "none"; document.getElementById("available_groups").style.display = "none";'>
	<input class = 'input1' type = 'button' name = 'getusers' value = 'Check User'  onclick = 'return get_user_suggestions_acl("", document.getElementById("granted").options, "", "", document.user_acl.domainslist.value, this.form.sssavailable.value, "users", document.user_acl.hid_separator.value, \"""" + get_share + """", "acl", \"""" + str(smbuserslength) + """", \"""" + connstatus + """");' """ + alldisabled + """ >		
	<input class = 'input1' type = 'button' name = 'getusers' value = 'Check Group'  onclick = 'return get_user_suggestions_acl("", document.getElementById("granted").options, "", "", document.user_acl.domainslist.value, this.form.sssavailable.value, "groups", document.user_acl.hid_separator.value, \"""" + get_share + """", "acl", \"""" + str(smbgroupslength) + """", \"""" + connstatus + """");' """ + alldisabled + """ >"""		
	print """<select name ="avail[]" multiple class="user" id ="avail_id" onkeydown = 'return get_key();' style ='width:188px;height:196px; display: """ + avail_users_style + """;'>"""

	if (ug == 'users'):	
		get_users1 = list(set(array_user)-set(grant_user))
		#print get_users1
		for lis_user in get_users1:
			print"""<option value = '"""+lis_user+"""'>"""+str(lis_user)+"""</option>"""
		#print get_users_string 

	elif (ug == 'groups'):
	
		get_groups1 = list(set(array_group)-set(grant_user))
		for lis_group in get_groups1:
			print"""<option value = '"""+lis_group+"""'>"""+str(lis_group)+"""</option>"""

		#print get_groups_string;

	print"""	</select></td>"""

	print """<td><input type = 'button' name = 'moveusers' value = '>' onclick = 'return move_users(this.form.avail_id, this.form.granted, "1");'><br />"""

	print """<input type = 'button' name = 'moveusers' value = '<' onclick = 'return move_users(this.form.granted, this.form.avail_id, "2");'><br /></td>"""
	print """	<td style="color:#666666; font-weight:600;">Authorised:<BR>
		<select id = 'granted' name ="grant_users[]" multiple  selected style ='width:330px;height:170px;margin-right:83%;'>"""
	#for groups in groups_from_list:
	#	print """<option value = '"""+groups+"""' selected>"""+groups+"""</option>"""
	print users_dropdown;
	print """	</select></td>"""

	print """ 	<td>
		<div class="buttonWrapper">
		<button """+acldisabled+""" class="buttonClass" type="submit" name = 'set' id = "set_id" value = 'Acl' onclick = 'return validate_set_acl();'>Set</button></div></td>

		</tr>
		</table>
		 <!--<div style="float:right;margin-top:-3%;">
		<button class="buttonClass" type="submit" name = 'set_cl' value = 'Acl' >Set ACL</button></div>-->
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
			#print users_list
			#users_list = users_list.replace('[', '')
			#users_list = users_list.replace(']', '')
			users_list = users_list.replace('[U]', '')
			users_list = users_list.replace('[G]', '@')
			users_list = users_list.replace('[DOT]', '.')
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
		<button """+acldisabled+""" class="buttonClass" type="submit" id = 'id_butt' name = 'set_acl' value = 'acl'>Set Acl</button></div>
		<input type = 'hidden' name = 'hid_separator' value = '""" + ads_separator + """'>
	</form>
	</div>
	<div id="subtabs-3">
	<style>
        #proppopUpDiv7 {position: fixed; background-color: #fff; width: 500px; z-index: 9002; padding: 5px;}
        #proppopUpDiv7 h5{width:100%; font-size:15px; color:#0070bd; text-align:center; font-weight:bold;}
        #proppopUpDiv7 span{ color:#FFFFFF; background-color:#0070bd; padding:1px 3px 0 3px; float:right;}
        #proppopUpDiv7 ul.idTabs{list-style:none; border:none; width:400px; margin:5px 0 0 0;}
        #proppopUpDiv7 ul.idTabs li{display:inline;}
        #proppopUpDiv7 ul.idTabs li a.link_tabs{display:inline; border:none; background-color:#D1D1D1; padding:10px;}
	</style>
	<!--<form name = "perm_form" method = "post" action='iframe_set_acl_page.py#subtabs-3' >-->
	<form name = "perm_form" method = "post" action='' >
        <div style="display: none;" id='proppopUpDiv7'>
        <h5>Confirm Box<span onclick="popup('proppopUpDiv7')" style="cursor:pointer;">X</span></h5>
        <div style="text-align:center; height:70px; margin:20px 0 20px 0;">
        Are you sure you want to Change Permission For Current Share?<br/><br/>
        <button class="button_example" type="button" name = 'local_action_but'  id = 'local_action_but' value = 'info' style="float:right; margin:0px 200px 0 0; " onclick="popup('proppopUpDiv7')" >No</button>
        <button class="button_example" type="submit" name = 'change_perm_but' value = 'change_perm_but' style="float:right; " >Yes</button></div></div>

	<table style="width:84%;margin:20px 0 0 0;">
		
		<tr>
		<input type="hidden" name="share_name" value='"""+get_share+"""' />
		<input type="hidden" name="share_hid_path" value='"""+set_path+"""' />
		<td style="color:#666666; font-weight:600;">Share Path:"""
	if(set_path !=''):
		print """ 
		<input type="text"  class = 'textbox' name = "selected_file" readonly value = '""" + set_path + """' style = 'width:70%;'>"""
	else:
		print"""
		<input type="text"  class = 'textbox' name = "selected_file" readonly value = '""" + sharepath + """' style = 'width:70%;'>"""
	print"""

	</td>
		</tr>
		<tr>
			<th style = "color:DarkOliveGreen;font-family:menu;font-size:14px;"><b style="margin-left:0%;">Read</b></th>
			<th style = "color:DarkOliveGreen;font-family:menu;font-size:14px;float: left; margin-left: -72%;"><b>Write</b></th>
			<th style = "color:DarkOliveGreen;font-family:menu;font-size:14px;float: left; margin-left: -10%;"><b>Execute</b></th>
		</tr>

		<tr>
			<th align="left" style="padding:0 0 0 20px; color:#666666;"><b>Owner</b></th>
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
			<th align="left" style="padding:0 0 0 20px; color:#666666;"><b>Group</b></th>
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
			<th align="left" style="padding:0 0 0 20px;color:#666666;"><b>Other</b></th>
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
		<td style = "color:DarkOliveGreen;font-family:menu;font-size:14px;margin-top:2%;"><input type = "checkbox" name ="sub_inherit"><b>Inherit</b></td>
		</tr>  

		</table>
		<div style="float:right;margin-top:-6%;">
		<div class="buttonWrapper">
		<button """+acldisabled+""" class="buttonClass" type = 'button'  name="change_perm_but" """
	if(set_path !=''):

		print """onclick="popup('proppopUpDiv7')" """

	else:
		print """onclick="return validate_set_acl();" """
	print"""value="change_perm_but" >Apply</button></div></div>

	</form>
	</div>
	<div id="subtabs-4">"""
	#import perms_ownership
	userslength = 0;
	groupslength = 0;

	all_users_list  = common_methods.get_users_string();
	all_groups_list = common_methods.get_groups_string();

	if (all_users_list['id'] == 0):
		smb_all_users_array  = all_users_list['users'];
		userslength       = len(smb_all_users_array);

	if (all_groups_list['id'] == 0):
		smb_all_groups_array = all_groups_list['groups'];
		groupslength      = len(smb_all_groups_array);

	usersfilesarray  = [];
	groupsfilesarray = [];

	#alldisabled = '';
	connstatus = common_methods.conn_status();

	users_style  = 'none';
	groups_style = 'none';

	users_list_style = 'none';
	groups_list_style = 'none';

	#ads_separator = '';
	#ads_separator = tools.get_ads_separator();

	domain = '';
	#domainname = '';

	share_name = '';
	#share_path = '';
	#ug = '';

	#domainsarray = [];

	#domainsarray = common_methods.get_all_domains();

	#querystring = os.environ['QUERY_STRING'];

	assusr = 'root';
	assgrp = 'root';
	get_ownership_status ={}
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
	#if (share_name != ''):
	#	share_path = common_methods.get_share_path('^' + share_name + ':');

	#	if (share_path != 1):
	#		disp_share_path = share_path.replace('/storage/', '');

	#	else:
	#		share_path = '';
	
	if (set_path != ''):
                get_ownership_status = acl.get_acl('/storage/'+set_path);
		#------------modified code on 15-12-14 Check Path is Exit or not------------------------
                if (get_ownership_status != {}):
                        assusr     = get_ownership_status['owner'];
                        assgrp     = get_ownership_status['group'];
			#------------------Add this code---------------------
			chk_path = tools.is_dir_exist(set_path)
			#print 'SET:'+str(chk_path)
			if(chk_path ==True):
                		sharepath  = get_ownership_status['path'];
                		sharepath  = sharepath.replace('/storage/', '');
				share_path = get_ownership_status['path'];
			else:
				ssharepath = 'Path Not Exit'	
			#--------------------End----------------------------


        else:
                common_methods.sendtologs('ERROR', 'Get Share Path', 'UI', '"set_acl_page.py, common_methods.get_share_path()", Could not get path');

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
				#print assusr

                if (len(assgrparray) > 0):
                        for i in assgrparray:
                                assgrp = i;

                if (assusr != ''):
                        assusr = assusr.strip();
                        groups_style = 'table';

                if (assgrp != ''):
                        assgrp = assgrp.strip();
                        users_style = 'table';
                #if (get_ownership_status != {}):#Edit this line and add a condition #
                if (assusr == ''):
                	assusr = get_ownership_status['owner'];
			#assusr = 'reboot'

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
				#print get_users_string
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
                                        get_groups_string += '<option value = "' + groups + '">' + groups + '</option>'	
	print """ 
	<style>
        #proppopUpDiv8 {position: fixed; background-color: #fff; width: 500px; z-index: 9002; padding: 5px;}
        #proppopUpDiv8 h5{width:100%; font-size:15px; color:#0070bd; text-align:center; font-weight:bold;}
        #proppopUpDiv8 span{ color:#FFFFFF; background-color:#0070bd; padding:1px 3px 0 3px; float:right;}
        #proppopUpDiv8 ul.idTabs{list-style:none; border:none; width:400px; margin:5px 0 0 0;}
        #proppopUpDiv8 ul.idTabs li{display:inline;}
        #proppopUpDiv8 ul.idTabs li a.link_tabs{display:inline; border:none; background-color:#D1D1D1; padding:10px;}
	
        #proppopUpDiv9 {position: fixed; background-color: #fff; width: 500px; z-index: 9002; padding: 5px;}
        #proppopUpDiv9 h5{width:100%; font-size:15px; color:#0070bd; text-align:center; font-weight:bold;}
        #proppopUpDiv9 span{ color:#FFFFFF; background-color:#0070bd; padding:1px 3px 0 3px; float:right;}
        #proppopUpDiv9 ul.idTabs{list-style:none; border:none; width:400px; margin:5px 0 0 0;}
        #proppopUpDiv9 ul.idTabs li{display:inline;}
        #proppopUpDiv9 ul.idTabs li a.link_tabs{display:inline; border:none; background-color:#D1D1D1; padding:10px;}

        </style>
        
	<form name="chang_owner_form" method="post" action="">
	
        <div style="display: none;" id='proppopUpDiv8'>
        <h5>Confirm Box<span onclick="popup('proppopUpDiv8')" style="cursor:pointer;">X</span></h5>
        <div style="text-align:center; height:70px; margin:20px 0 20px 0;">
        Are you sure you want to Reset Ownership?<br/><br/>
        <button class="button_example" type="button" name = 'local_action_but'  id = 'local_action_but' value = 'ResetOwner' style="float:right; margin:0px 200px 0 0; " onclick="popup('proppopUpDiv8')" >No</button>
        <button class="button_example" type="submit" name = 'reset_ownership'  id = 'reset_ownership' value = 'ResetOwner' style="float:right; " >Yes</button></div></div>
	<div style="display: none;" id='proppopUpDiv9'>
        <h5>Confirm Box<span onclick="popup('proppopUpDiv9')" style="cursor:pointer;">X</span></h5>
        <div style="text-align:center; height:70px; margin:20px 0 20px 0;">
        Are you sure you want to Set Ownership?<br/><br/>
        <button class="button_example" type="button" name = 'local_action_but'  id = 'local_action_but' value = 'Reset' style="float:right; margin:0px 200px 0 0; " onclick="popup('proppopUpDiv9')" >No</button>
        <button class="button_example" type="submit" name = 're_assign_ownership'  id = 're_assign_ownership' value = 'Apply' style="float:right; " >Yes</button></div></div>


                <table style="width:90%; margin-left: 5%;" border = '0'>
        <tr>
                <td style="color:#666666; font-weight:600;">
                        <b>Share Path</b>:
                </td>
                <td>"""
	if(set_path != ''):
		print"""
                        <input class = 'textbox' type = 'text' readonly name = 'acl_path' style = 'width: 90%;' value = '""" + set_path + """'>"""
	else:
		print"""<input class = 'textbox' type = 'text' readonly name = 'acl_path' style = 'width: 90%;' value = '""" + sharepath + """'>"""
	print"""
                </td>
        </tr>
        <tr>
                <td height = '35px'></td>
        </tr>
        <tr>
                <td width = '20%' style="color:#666666; font-weight:600;">
                        Assigned to User:
                </td>
                <td>
                <input type = 'text' class = 'textbox' readonly name = 'assd_user' value = '""" + assusr + """' style = 'width: 60%;margin-top:4%;' />
                <a href = '#' onclick = 'document.getElementById("id_set_owner").style.display = "table"; document.getElementById("id_set_group").style.display = "none";' style = 'text-decoration: underline;'>Change USER</a><BR><BR></td></tr>
                <tr><td colspan = '2'>
                <div id = 'id_set_owner' style = 'margin-left: 8%; width: 90%; border: 0px solid #BDBDBD; display: """ + users_style + """;'>
                <b style ="color:DarkOliveGreen;font-family: menu;font-size:14px;">Choose a domain:</b> <select name = 'udomainslist' onchange = 'document.chang_owner_form.hid_domain.value = document.chang_owner_form.udomainslist.value;'>"""

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

		 <input id = 's_sssavailable' name = 'ads_user_text' type="text" class = 'input' value = '' onclick = 'document.getElementById("s_available").style.display = "none"; document.getElementById("s_available_groups").style.display = "none";' style = 'width: 40%;'><input class = 'input1' type = 'button' name = 'getusers' value = 'Check'  onclick = 'return get_user_suggestions_acl("", document.getElementById("id_groups_list").value, "", "", document.chang_owner_form.udomainslist.value, this.form.s_sssavailable.value, "users", document.chang_owner_form.hid_separator.value, \"""" + share_name + """", "ownership", \"""" + str(userslength) + """", \"""" + connstatus + """");' """ + alldisabled + """ >"""
        print """<select id = 'id_users_list' name='ass_user' onchange = 'document.chang_owner_form.assd_user.value = document.chang_owner_form.ass_user.value; document.getElementById("id_set_owner").style.display = "none";' style = 'display: """ + users_list_style + """;'>
                <option value = ''>Choose a USER</option>"""
	print get_users_string;
	print """</select></div>

		 </td>
                <td>
                </td>
        </tr>
        <tr>
                <td height = '35px'></td><td></td>
        </tr>
        <tr>
                <td style="color:#666666; font-weight:600;width:23%;">
                        Assigned to Group:
                </td>
                <td>
                <input type = 'text' class = 'textbox' readonly name = 'assd_group' value = '""" + assgrp + """' style = 'width: 60%;margin-top:4%;' />
                <a href = '#' onclick = 'document.getElementById("id_set_group").style.display = "table"; document.getElementById("id_set_owner").style.display = "none";' style = 'text-decoration: underline;'>Change GROUP</a><BR><BR></td></tr>
                <tr><td colspan = '2'>
                <div id = 'id_set_group' style = 'margin-left: 8%; width: 90%; border: 0px solid #BDBDBD; display: """ + groups_style + """;'>
                <b style ="color:DarkOliveGreen;font-family: menu;font-size:14px;">Choose a domain:</b> <select name = 'gdomainslist' onchange = 'document.chang_owner_form.hid_domain.value = document.chang_owner_form.gdomainslist.value;'>"""
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

		<input id = 's_ssavailable_groups' name = 'ads_group_text' type="text" class = 'input' value = '' onclick = 'document.getElementById("s_available_groups").style.display = "none"; document.getElementById("s_available").style.display = "none";' style = 'width: 40%;'><input class = 'input1' type = 'button' name = 'getgroups' size ="10" value = 'Check' onclick = 'return get_user_suggestions_acl(document.getElementById("id_users_list").value, "", "", "", document.chang_owner_form.gdomainslist.value, this.form.s_ssavailable_groups.value, "groups", document.chang_owner_form.hid_separator.value, \"""" + share_name + """", "ownership", \"""" + str(groupslength) + """", \"""" + connstatus + """");' """ + alldisabled + """ />
                <select id = 'id_groups_list' name = 'ass_group' onchange = 'document.chang_owner_form.assd_group.value = document.chang_owner_form.ass_group.value; document.getElementById("id_set_group").style.display = "none";' style = 'display: """ + groups_list_style + """;'>
                <option value = ''>Choose a GROUP</option>"""
	print get_groups_string;
	print """

	 </select></div>
                </td>
        </tr>

        </table>
<br/>
        <p style="margin-left: 5%;"><input type="checkbox" name="inherit_ownership"><b style ="color:DarkOliveGreen;font-family: menu;font-size:14px;">Inherit Ownership to sub-folders</b></p>

        <input type='hidden' name='hid_s_name' value='""" + share_name + """' />
        <input type='hidden' name='hid_s_path' value='""" + str(share_path) + """' />
        <div style="float: right; margin-top: -9%;">
	<div class="buttonWrapper">
        <button """+acldisabled+""" class="buttonClass" type="button" name = 'reset_ownership'  id = 'reset_ownership' """
	if(set_path !=''):
		
		print"""onclick="popup('proppopUpDiv8')"  """

	else:
		print """onclick="return validate_set_acl();" """
	print """value = 'ResetOwner'  style="float:right; margin:20px 10px 10px 0;" >Reset</button></div>
<div class="buttonWrapper">	
<button """+acldisabled+""" class="buttonClass" type="button" name = 're_assign_ownership'  id = 're_assign_ownership' """
	if(set_path !=''):
	
		print """onclick="popup('proppopUpDiv9')" """
	else:
		print """onclick="return validate_set_acl();" """
	print """value = 'Apply'  style="float:right; margin:20px 10px 10px 0;" >Set</button></div>
</div>
        <input type = 'hidden' name = 'hid_separator' value = '""" + str(ads_separator) + """' />
        <input type = 'hidden' name = 'hid_domain' value = '' />
        </form>"""
	print"""
	</div>
	<div id="subtabs-5">
	<style>
        #proppopUpDiv10 {position: fixed; background-color: #fff; width: 500px; z-index: 9002; padding: 5px;}
        #proppopUpDiv10 h5{width:100%; font-size:15px; color:#0070bd; text-align:center; font-weight:bold;}
        #proppopUpDiv10 span{ color:#FFFFFF; background-color:#0070bd; padding:1px 3px 0 3px; float:right;}
        #proppopUpDiv10 ul.idTabs{list-style:none; border:none; width:400px; margin:5px 0 0 0;}
        #proppopUpDiv10 ul.idTabs li{display:inline;}
        #proppopUpDiv10 ul.idTabs li a.link_tabs{display:inline; border:none; background-color:#D1D1D1; padding:10px;}
	</style>
	<form name="acl_info" method="post" action=''>
        <div style="display: none;" id='proppopUpDiv10'>
        <h5>Confirm Box<span onclick="popup('proppopUpDiv10')" style="cursor:pointer;">X</span></h5>
        <div style="text-align:center; height:70px; margin:20px 0 20px 0;">
        Are you sure you want to Update User Permission?<br/><br/>
        <button class="button_example" type="button" name = 'local_action_but'  id = 'local_action_but' value = 'info' style="float:right; margin:0px 200px 0 0; " onclick="popup('proppopUpDiv10')" >No</button>
        <button class="button_example" type="submit" name = 'acl_user_del' value = 'info' style="float:right; " >Yes</button></div></div>"""
	#if(get_all_users['users'] != []):
	print"""<table id = 'id_table' style="width:100%; margin:20px 0 0 0;border:1px;">"""
	#else:
		#print"""<table id = 'id_table' style="width:100%; margin:20px 0 0 0;border:1px;display:none;">"""
		#print """<div style="text-align:center; height:30px; margin:20px 0 20px 0;">No User present For Acl! <a href="main.py?page=mu" style = 'text-decoration:underline;'>Add User</a><br/><br/></div>"""
	print"""
		 <tr>
		<input type="hidden" name="share_name" value='"""+get_share+"""' />
		<input type="hidden" name="share_hid_path" value='"""+set_path+"""' />
		<td style="color:#666666; font-weight:600;"><b>Share Path</b>:"""
	if(set_path !=''):
		print"""
		<input type="text" class = 'textbox' name = "selected_file" readonly value = '""" + set_path + """' style = 'width:50%;margin-bottom:5%;'>"""
	else:
		print"""
		<input type="text" class = 'textbox' name = "selected_file" readonly value = '""" + sharepath + """' style = 'width:50%;margin-bottom:5%;'>"""
	print"""
		  
		</td></tr>

		<tr>
			<!--<td style ="color:#EC1F27;float:left;">Select User</td>-->
			<td style ="color:DarkOliveGreen;font-family:menu;float:left;"><b>User/Group</b></td>
			<td style ="color:DarkOliveGreen;font-family: menu;float:left;margin-left:17%;"><b>Read</b></td>
			<td style ="color:DarkOliveGreen;font-family: menu;float:left;margin-left:12.5%;"><b>Write</b></td>
			<td style ="color:DarkOliveGreen;font-family: menu;float:left;margin-left:60%;margin-top:-2%;"><b>Execute</b></td>
			<td style ="color:DarkOliveGreen;font-family: menu;float:left;margin-left:76%;margin-top:-2%;"><b>Remove</b></td>
		</tr>"""
	if(grant_user == None):
		print"""<th align="left" style="color:darkgreen;""></th>"""
	else:
		k = 1
		if(lis_info !={}):
			for users_list in lis_info:
				
				#print 'chkp:'+str(users_list)
				print"""

					
				<!--<tr>
						<td align="left" style="color:darkgreen;"><div style="margin-top: 2%;"><input type = "checkbox" name = "user_remove" value =''></div></td>
						
				</tr>-->
					<tr>
						<td align="left" style="color:darkgreen;""><div style="margin-top: 2%;">"""+users_list+"""</div></td >
						
				<td><input type="hidden" name='"""+users_list+"""user_value'></td>
				</tr>
				<tr style="border:solid 1px;">"""
				
				print"""<td style="float:right;width:71%;margin-top:-2%;"><input type="checkbox" name='"""+users_list+"""o_read'"""
				if(chk_perm != {}):
					print chk_perm[users_list+'_chk_read']

				if(lis_info != {}):
					if 'r' in lis_info[users_list]:
						print "checked"
				#else:
				#	print """ """+users_list+"""o_read """
				print """></td>"""

				print"""<td style="float:right;width:53.5%;margin-top:-2%;"><input type="checkbox" name='"""+users_list+"""o_write'"""
				if(chk_perm != {}):
					print chk_perm[users_list+'_chk_write']

				if(lis_info != {}):
					if 'w' in lis_info[users_list]:
						print "checked"


				print """></td>"""
				print"""<td style="float:right;margin-right:-18%;margin-top:-2%;"><input type="checkbox" name='"""+users_list+"""o_execute'"""
				if(chk_perm != {}):
					print chk_perm[users_list+'_chk_execute']

				if(lis_info != {}):
					if 'x' in lis_info[users_list]:
						print "checked"


				print """></td>"""
				#print"""<td style="float:right;width:25%;margin-top:-2%;"><input type="submit" name = '"""+users_list+"""reset_single' value = "reset"></td>"""
				print"""<td style="float:right;margin-right:-35%;margin-top:-3%;"><button type="image" value = "reset" name='"""+users_list+"""reset_single' style="background: #fff; border: 0px;cursor:pointer;" ><img src="../images/snap_del_but_small.jpg"></button></td> """
				#print """<td style="float:right;width:27%;margin-top:-3%;border: medium none;"><button><input type="submit" name= '"""+users_list+"""reset_single' style="display: none;" value "reset" ><img src="../images/reset_acl5.png"></button></td>  """
				print """</tr> """
				k = k+1
		else:
			print"""<tr>
                                <td style="border:#D1D1D1 0px solid;padding-top: 3%; text-align: center;" colspan = "3"><span>No Information is Available</span></td>
                                <tr>"""

		print"""<td><input type="hidden" name="hid_k_val" value='"""+str(k)+"""'></td>"""

	print"""
	<tr>"""
	if(recur_info == "on"):
		recr_chk = "checked"
		recur_info = "yes"
	else:
		recr_chk = ""
		recur_info = "no"

	print"""<td style="color:#666666; font-weight:600;"><div style="margin-top: 3%;"><b>Recursive</b>:<input type="checkbox" name='o_recursive' """+recr_chk+""" /></div></td>"""


	print"""</tr>"""
	print"""
		</table>"""
	#if(get_all_users['users'] != []):
	print"""<div style="float:right;margin-top:-6%;">
		<div class="buttonWrapper">
		<button """+acldisabled+""" class="buttonClass" type="button" name = 'acl_user_del' """
	if(set_path !=''):
		print"""onclick="popup('proppopUpDiv10')" """
	else:
		print """onclick="return validate_set_acl();" """

	print """ value = 'info'>Re-assign</button></div></div>"""
	#else:
	#print"""<div style="float:right;margin-top:-3%;display:none;"><button class="button_example" type="submit" name = 'acl_user_del' value = 'info'>Reassign</button></div>"""
	print"""
	</form>
	</div>
	<div id="subtabs-6">
	<style>
        #proppopUpDiv11 {position: fixed; background-color: #fff; width: 500px; z-index: 9002; padding: 5px;}
        #proppopUpDiv11 h5{width:100%; font-size:15px; color:#0070bd; text-align:center; font-weight:bold;}
        #proppopUpDiv11 span{ color:#FFFFFF; background-color:#0070bd; padding:1px 3px 0 3px; float:right;}
        #proppopUpDiv11 ul.idTabs{list-style:none; border:none; width:400px; margin:5px 0 0 0;}
        #proppopUpDiv11 ul.idTabs li{display:inline;}
        #proppopUpDiv11 ul.idTabs li a.link_tabs{display:inline; border:none; background-color:#D1D1D1; padding:10px;}
	</style>
	<form name= "reset_acl_form" method= "post" action=''>
        <div style="display: none;" id='proppopUpDiv11'>
        <h5>Confirm Box<span onclick="popup('proppopUpDiv11')" style="cursor:pointer;">X</span></h5>
        <div style="text-align:center; height:70px; margin:20px 0 20px 0;">
        Are you sure you want to Remove Acl?<br/><br/>
        <button class="button_example" type="button" name = 'local_action_but'  id = 'local_action_but' value = 'ResetOwner' style="float:right; margin:0px 200px 0 0; " onclick="popup('proppopUpDiv11')" >No</button>
        <button class="button_example" type="submit" name = 'reset_acl' value = 'Reset' style="float:right; " >Yes</button>
        </div></div>"""
	#if(get_all_users['users'] != []):
	print"""<table width="70%">"""
	#else:
		
	#print"""<table width="70%" style="display:none;">"""
	#print """<div style="text-align:center; height:30px; margin:20px 0 20px 0;">No User present For Acl! <a href="main.py?page=mu" style = 'text-decoration:underline;'>Add User</a><br/><br/></div>"""
	print"""
		 <tr>
		  <td style="color:#666666; font-weight:600;">Share Path:</td>
			<!--access_control_form.selected_file-->
		<input type="hidden" name="share_name" value='"""+get_share+"""' />
		<input type="hidden" name="share_hid_path" value='"""+set_path+"""' />
		  <td colspan = '4'>"""
	if(set_path !=''):
		print"""<input type="text"  class = 'textbox' name = "selected_file" readonly value = '""" + set_path + """' style = 'width:70%;margin-right:55%;'>"""

	else:
		
		print"""<input type="text" class = 'textbox' name = "selected_file" readonly value = '""" + sharepath + """' style = 'width:70%;margin-right:55%;'>"""
	print"""


	</td>
		</tr>
		<tr>
		<td style="color:#666666; font-weight:600;">Recursive:</td>"""
	if(reset_chk == 'on'):
		reset_chk_but = 'checked'
		reset_chk = "yes"
	else:
		reset_chk_but = ""
		reset_chk = "no"
		
	print"""	<td><input type="checkbox" name= "check_reset" """+reset_chk_but+"""></td>"""
	print"""	</tr>
	</table>"""
	#if(get_all_users['users'] != []):
	print"""<div style="float:right;margin-top:-6%;">
		<div class="buttonWrapper">
		<button """+acldisabled+""" class="buttonClass" type="button" name = 'reset_acl' """
	if(set_path !=''):

		print """onclick="popup('proppopUpDiv11')" """
	else:
		print """onclick="return validate_set_acl();" """

	print"""value = 'Remove' >Remove</button></div></div>"""
	#else:
	#	print"""<div style="float:right;margin-top:-3%;display:none;"><button class="button_example" type="submit" name = 'reset_acl' value = 'Reset' onclick =''>Reset</button></div>"""
	
	print"""
	</form>

	</div>

	</div>
	<!--form container ends here-->
	<input type = 'hidden' name = 'hid_dir_file' />
	</form>
	<p>&nbsp;</p>
	</div>

		<input type="hidden" name="selected_file" value='"""+set_path+"""' id ='set_path_id' />
	  </div>
	</div>
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
