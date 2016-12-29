#!/usr/bin/python
import cgitb, sys, include_files
cgitb.enable()
sys.path.append('../modules/')
import disp_except
try:
	#################################################
	################ import modules #################
	#################################################
	import common_methods, os
	sys.path.append('/var/nasexe/python/');
	import smb, tools;
	from fs2global import *;
	from tools import smb_logpath
	#--------------------- END --------------------#

	#################################################
	############ Check Log Path is set ##############
	#################################################
	log_path_status = smb_logpath.is_set()
        if(log_path_status == True):
		enable_audit_mess = ""
		disable_en_audit = ""
	else:
		enable_audit_mess = "[<font style='color:#DF0101;'>SMB Log Path is not enabled!</font> <a target='_parent' href='main.py?page=logs#tabs-4' style='text-decoration:underline;'>Enable Now</a>]"
		disable_en_audit = "disabled"
	#--------------------- END --------------------#


	# import navigation part on the left hand side
	path    = '';
	comment = '';

	message = '';
	statmessage = '';

	# get the authentication mode (connection status ie., ADS, NIS, local)
	connstatus = common_methods.conn_status();

	# get the querystring from the url submitted to this page
	querystring = os.environ["QUERY_STRING"];
	get_share = '';
	ug = '';
	readonly = '';
	visible  = '';

	domain_only       = '';
	smbdisabled       = '';
	writable_checked  = '';
	guest_checked     = '';
	public_checked    = 'checked';
	validuser_checked = '';
	visible_checked   = 'checked';
	conn_text         = '';
	alldisabled       = '';
	domainname        = '';
	users_dropdown    = '';
	groups_dropdown   = '';

	ads_separator = '';

	# decide the separator between the domain name and user name when connection is set to ADS
	if (connstatus == 'Join is OK'):
		ads_separator = '\\';

	users_from_list  = [];
	groups_from_list = [];

	use_smb           = 'off';
	public            = '';
	valid_user = '';
	smb_line   = '';
	share_details = [];

	# declare an array for shares
	all_shares_array = [];

	# function for getting all the shares is defined in '/var/nasexe/python/tools/__init__.py', get_all_shares module
	get_allshares = tools.get_all_shares();

	# create a dictionary for shares
	if (get_allshares['id'] == 0):
		all_shares_dicts_array = get_allshares['shares'];

		if (len(all_shares_dicts_array) > 0):
			for shares_dict in all_shares_dicts_array:
				sharesstring = shares_dict['name'] + '-' + shares_dict['path'];

				all_shares_array.append(sharesstring);
	else:
		# send the error message to database
		common_methods.sendtologs('ERROR', 'Get Shares', 'UI', '"smb_settings.py, tools.get_all_shares()" ' + str(get_allshares['desc']));

	if (querystring.find('share_name=') >= 0):
		if (querystring.find('&ro=') > 0):
			get_share = querystring[querystring.find('share_name=') + len('share_name='):querystring.find('&ro=')];

		elif (querystring.find('&dom=') > 0):
			get_share = querystring[querystring.find('share_name=') + len('share_name='):querystring.find('&dom=')];

		else:
			get_share = querystring[querystring.find('share_name=') + len('share_name='):];

	par_share_det = tools.get_share(get_share,debug=False)
        get_ha_nodename = par_share_det["share"]["node"]

	if (get_share == ''):
		print "<script>location.href = 'main.py?page=cs';</script>";
		
	if (querystring.find('ug=') >= 0):
		ug = querystring[querystring.find('ug=') + len('ug='):querystring.find('&share_name')];

	valid_users_style  = 'none';
	valid_groups_style = 'none';

	users_list_style  = 'none';
	groups_list_style = 'none';

	audit_option = '';
	recycle_opt        = '';

	sharesmbdetails = smb.show(get_share,get_ha_nodename);

	smb_line = sharesmbdetails['share'];
		
	use_smb  = smb_line['use_smb'];

	# condition if SMB is enabled
	writable      = smb_line['writable'];
	browsable     = smb_line['browsable'];
	public        = smb_line['public'];
	guest_ok      = smb_line['guest_ok'];
	valid_user    = smb_line['valid_users'];
	audit_option  = smb_line['audit_enable'];
	recycle_opt   = smb_line['recycle_enable'];
	recycle_path  = smb_line['recycle_repo'];

	# depending on the values retrieved, the form should show the values set and it should also 
	# retain the state of the checkbox, radio elements whether they are selected or not...
	if (writable == 'yes'):
		writable_checked = '';

	if (browsable == 'yes'):
		visible_checked = 'checked';

	if (public == 'yes' or guest_ok == 'yes'):
		public_checked = 'checked';

	if (valid_user != '' and public != 'yes'):
		validuser_checked = 'checked';

	get_users_string  = '';
	get_groups_string = '';

	assusrfile = 'smbassusersfile';
	assgrpfile = 'smbassgroupsfile';

	assusrstring = '';
	assgrpstring = '';

	assusrarray = [];
	assgrparray = [];

	if (querystring.find('&mess=') > 0):
		domainname = querystring[querystring.find('&dom=') + len('&dom='):querystring.find('&mess=')];

	else:
		domainname = querystring[querystring.find('&dom=') + len('&dom='):];

	if (ug != ''):
		validuser_checked = 'checked';

		assusrarray = common_methods.read_file(assusrfile);
		assgrparray = common_methods.read_file(assgrpfile);

		if (len(assusrarray) > 0):
			for assu in assusrarray:
				assu = assu.replace('%20', ' ');
				assu = assu.replace('[DOLLAR]', '$')
				assu = assu.strip();

				assu_internal = assu;
				disp_assu = assu;

				users_from_list.append(assu);

		if (len(assgrparray) > 0):
			for assg in assgrparray:
				assg = assg.replace('%20', ' ');
				assg = assg.strip();

				assg_internal = assg;
				groups_from_list.append(assg);

		if (querystring.find('&mess=') > 0):
			domainname = querystring[querystring.find('&dom=') + len('&dom='):querystring.find('&mess=')];

		else:
			domainname = querystring[querystring.find('&dom=') + len('&dom='):];
		get_share  = querystring[querystring.find('share_name=') + len('share_name='):querystring.find('&ro=')];
		readonly   = querystring[querystring.rfind('&ro=') + len('&ro='):querystring.rfind('&v=')];
		visible    = querystring[querystring.rfind('&v=') + len('&v='):querystring.find('&dom=')];

		domainname = domainname.strip();
		readonly   = readonly.strip();
		visible    = visible.strip();

		if (ug == 'users'):
			valid_users_style  = 'table';
			valid_groups_style = 'table';
			users_list_style   = 'table';
			groups_list_style  = 'none';

			get_users_array = [];
			get_users_array = common_methods.read_file('smbsearchusersfile.txt');
			get_users_array.sort();

			for get_users in get_users_array:
				if (get_users != ''):
					get_users = get_users.strip();

					get_usersinternal = common_methods.replace_chars(get_users, 'chartotext');
					get_disp_users    = get_users[get_users.find('\\') + 1:];

					check_users = '"' + get_users + '"';
					
					if (valid_user.find(check_users) < 0):
						get_users_string += '<option value = "' + get_usersinternal + '">' + get_disp_users + '</option>';

		if (ug == 'groups'):
			valid_groups_style = 'table';
			valid_users_style  = 'table';
			groups_list_style  = 'table';
			users_list_style   = 'none';

			get_groups_array = [];
			get_groups_array = common_methods.read_file('smbsearchgroupsfile.txt');
			get_groups_array.sort();

			for get_groups in get_groups_array:
				if (get_groups != ''):
					get_groups = get_groups.strip();

					check = '"@' + get_groups + '"';
					check_ass_groups = valid_user.find(check);

					get_groupsinternal = common_methods.replace_chars(get_groups, 'chartotext');
					get_disp_groups    = get_groups[get_groups.find('\\') + 1:];

					if (check_ass_groups < 0):
						get_groups_string += '<option value = "@' + get_groupsinternal + '">' + get_disp_groups + '</option>';

		if (readonly == 'true'):
			writable_checked = 'checked';

		if (visible == 'true'):
			visible_checked = 'checked';

	if (get_share != ''):
		get_share = get_share.strip();

	# create a userslist groupslist from the method get_users_string() defined in common_methods.py
	all_users_list  = common_methods.get_users_string();
	all_groups_list = common_methods.get_groups_string();

	smb_all_users_array  = [];
	smb_all_groups_array = [];

	domainsarray            = [];
	available_domains_array = [];
	params_array            = [];

	domainsarray = common_methods.get_all_domains();

	smbuserslength  = 0;
	smbgroupslength = 0

	# if userslist is not empty
	if (all_users_list['id'] == 0):
		smb_all_users_array  = all_users_list['users'];
		smbuserslength       = len(smb_all_users_array);

	else:
		common_methods.sendtologs('INFO', 'Get Users', 'UI', '"smb_settings.py, all_users_list  = common_methods.get_users_string(); " ' + str(all_users_list['desc']));

	# if groupslist id not empty
	if (all_groups_list['id'] == 0):
		smb_all_groups_array = all_groups_list['groups'];
		smbgroupslength      = len(smb_all_groups_array);

	else:
		common_methods.sendtologs('INFO', 'Get Groups', 'UI', '"smb_settings.py, all_groups_list  = common_methods.get_groups_string(); " ' + str(all_groups_list['desc']));

	smb_full_users_string  = '';
	smb_full_groups_string = '';

	check_log_path = tools.get_string_from_file('SMBLOGPATH=', '/var/nasconf/smb-log.conf');

	lpath = '';

	if (check_log_path != 'not found'):
		temp = [];
		temp = check_log_path.split('=');

		d12   = temp[0];
		lpath = temp[1];

	smb_selected  = '';
	smb_opt_style = 'none';

	check_string       = 'not found';

	# lpath is the log path value. if the path of the share and the log path is matched, then the other features of the smb
	# except the permissions and ownership should be disabled.
	sharename = get_share;
	sharedetails = tools.get_share(sharename);

	if (sharedetails['id'] == 0):
		sharesinfo = sharedetails['share'];

		comment = sharesinfo['comment'];
		path    = sharesinfo['path'];

	button_disabled = ''

	if (path == lpath):
		smbdisabled      = 'disabled';
		smb_selected     = 'checked';
		writable_checked = 'checked';
		visible_checked  = 'checked';
		button_disabled = 'disabled'

	auditdisabled = '';
	auditmessage  = '';
	file_dir_style = 'none';

	# if log path is not set for the share then auditing can't be set.
	# since for auditing, log path should be enabled
	if (lpath == ''):
		auditdisabled    = 'disabled';
		auditing_checked = '';
		file_dir_style   = 'none';
		auditmessage     = '  <B>(Please set smb log path to enable auditing option.)</B>';

		tools.delete_entry_from_file('full_audit:', 'share_conf_file', '/var/nasconf/');

	# get the authenticated users from the share details page
	valid_user = valid_user.replace('" "', '"xxx"');
	valid_user = valid_user.strip();

	users_array = [];

	users_only_array  = [];
	groups_only_array = [];

	if (valid_user != ''):
		users_array = valid_user.split('xxx');
		elemtoremove = '';

		if (len(users_array) > 0):
			for i in users_array:
				if (i != ''):
					i = i.replace('"', '');
					i = i.strip();

					if (i.find('@') < 0):
						try:
							elemtoremove = smb_all_users_array.index(i);

						except Exception as e:
							print '';

						else:
							smb_all_users_array.pop(elemtoremove);

					elif (i.find('@') == 0):
						t = i.replace('@', '');

						try:
							elemtoremove = smb_all_groups_array.index(t);

						except:
							print

						else:
							smb_all_groups_array.pop(elemtoremove);
	if (len(users_array) > 0):
		for users in users_array:
			if (users != ''):
				users = users.strip();

				userstemp = users.replace('"', '');
				userstemp = userstemp.strip();

				index_of_at = users.find('@');

				if (index_of_at < 0):
					users = users.replace('"', '');

					if (connstatus == 'Join is OK'):
						if (users.find('+') > 0):
							only_users = users[users.find('+') + 1:];

						else:
							only_users = users[users.find('\\') + 1:];

						disp_users = users;
						users = common_methods.replace_chars(users, 'chartotext');

						users_from_list.append(users);
						users_only_array.append(only_users);

					elif (connstatus == 'nis is running'):
						# generate a dropdown for assigned nis users
						users_from_list.append(users);	

					elif (connstatus == 'local'):
						# generate a dropdown for assigned local users
						users_from_list.append(users);

				# if the value of $user var has '@' in it, then that should be assigned to group variable.
				if (index_of_at > 0):
					users = users.replace('"', '');

					groups = users;

					if (groups != ''):
						if (connstatus == 'Join is OK'):
							if (groups.find('+') > 0):
								only_groups = groups[groups.find('+') + 1:];
							
							else:
								only_groups = groups[groups.find('\\') + 1:];

							disp_groups = groups[groups.find('@') + 1:];

							groups = common_methods.replace_chars(groups, 'chartotext');

							groups_from_list.append(disp_groups);
							groups_only_array.append(only_groups);

						elif (connstatus == 'nis is running'):
							groups_from_list.append(groups);

						elif (connstatus == 'local'):
							groups_from_list.append(groups);

	# assigned users
	assigned_users_string  = '';
	assigned_groups_string = '';
	ads_users_only_string  = '';
	ads_groups_only_string = '';
	smb_users_only         = '';
	smb_groups_only        = '';

	users_from_list.sort();
	users_from_list = list(set(users_from_list));

	groups_from_list.sort();
	groups_from_list = list(set(groups_from_list));

	for listusers in users_from_list:
		if (listusers != None):
			listusers = listusers.replace('[AND]', '&');
	                listusers = listusers.replace('[HASH]', '#');
        	        listusers = listusers.replace('[DOLLAR]', '$');
                	listusers = listusers.replace("[SQUOTE]", "'");

			users_dropdown += "<option value = '" + listusers + "' selected>" + listusers + "</option>";

	for listgroups in groups_from_list:
		if (listgroups != None):
			listgroups = listgroups.replace('[AND]', '&');
	                listgroups = listgroups.replace('[HASH]', '#');
        	        listgroups = listgroups.replace('[DOLLAR]', '$');
                	listgroups = listgroups.replace("[SQUOTE]", "'");

			if (listgroups.find('@') == 0):
				disp_groups = listgroups[listgroups.find('@') + 1:];

			else:
				disp_groups = listgroups;

			listgroups = common_methods.replace_chars(listgroups, 'chartotext');

			groups_dropdown += '<option value = "' + listgroups + '" selected>' + disp_groups + '</option>';

	if (len(users_only_array) > 0):
		for assusers in users_only_array:
			assusers = common_methods.replace_chars(assusers, 'chartotext');
			assusers = assusers.strip();

			assigned_users_string += assusers + ':';

		assigned_users_string = assigned_users_string[:assigned_users_string.rfind(':')];
		assigned_users_string = assigned_users_string.strip();

	if (len(groups_only_array) > 0):
		for assgroups in groups_only_array:
			assgroups = common_methods.replace_chars(assgroups, 'chartotext');
			assgroups = assgroups.strip();

			assigned_groups_string += assgroups + ':';

		assigned_groups_string = assigned_groups_string[:assigned_groups_string.rfind(':')];
		assigned_groups_string = assigned_groups_string.strip();

	test_for_smb = tools.get_string_from_file('true', '/var/www/global_files/smb_global_options_file');

	id_divname = '';

	if (querystring.find('&mess=') > 0):
		if (use_smb == 'on'):
			statmessage = 'Configured SMB !';
			id_divname  = 'id_trace';

		else:
			statmessage = 'Failed to Configure SMB !';
			id_divname  = 'id_trace_err';

	if (querystring.find('&mess1=') > 0):
		if (use_smb == 'off'):
			statmessage = 'Unconfigured SMB !';
			id_divname  = 'id_trace';

		else:
			statmessage = 'Failed to Unconfigure SMB !';
			id_divname  = 'id_trace_err';

	par_share_det = tools.get_share(get_share,debug=False)
	get_ha_nodename = par_share_det["share"]["node"]

	if (test_for_smb == '' and connstatus == 'Join is OK'):
		message = '<div style = "margin-left: 20%; margin-top: 10%; font: 13px Arial; color: darkred;">Please check the \'Use SMB\' option in Basic Setup -> SMB Settings for ADS</div>';


		print message;

		print """<form name = 'share_edit' id = 'id_smb_form' action = 'edit_shares.py' method = 'post'>
		<table width = "685" border = "0" cellspacing = "0" cellpadding = "0" name = 'disp_tables' id = 'id_smb_settings' style = 'display: none; background: #000; opacity: 0.5;' class = 'outer_border'>
			<tr>
				<td height = "33px" width = "8" align = "left">
					<img src = "../images/rightside_left.jpg" width = "8" height = "33" />
				</td>
				<td width = "669" height = "33px" align = "left" valign = "middle" class = "right_bg rightsidemenuheading">
					<a class = 'link' href = 'smb_settings_help.php' onclick = "window.open('smb_settings_help.php', 'help', 'location = no, height = 500, width = 600, scrollbars = 1'); return false;">""" + common_methods.getimageicon() + """</a>
					SMB settings
				</td>
				<td height = "33px" width = "8" align = "right">
					<img src = "../images/rightside_right.jpg" />
				</td>
			</tr>
			<tr>
				<td colspan = "3" align = "left" valign = "top">
					<table width = "685" border = "0" cellspacing = "0" cellpadding = "0">
					<tr>
						<td width = "1%" class = "table_heading" height = "70px" valign = "middle">
							<input type = 'checkbox' name = 'use_smb' onclick = "window.alert('Check the \'Use SMB\' option in Basic Setup > SMB Settings for ADS.'); return false;" """ + smb_selected + """ """ + alldisabled + """>&nbsp;<B>Use SMB</B>
						</td>
					</tr>
					</table>
				</td>
			</tr>
		</table>
		</form>"""

	else:
		audit_options_array = [];

		audit_options_array.append('connect:Connect');
		audit_options_array.append('disconnect:Disconnect');
		audit_options_array.append('opendir:Open dir');
		audit_options_array.append('mkdir:Make dir');
		audit_options_array.append('rmdir:Remove dir');
		audit_options_array.append('closedir:Close dir');
		audit_options_array.append('open:Open');
		audit_options_array.append('close:Close');
		audit_options_array.append('read:Read');
		audit_options_array.append('pread:PRead');
		audit_options_array.append('write:Write');
		audit_options_array.append('pwrite:PWrite');
		audit_options_array.append('sendfile:Send file');
		audit_options_array.append('rename:Rename');
		audit_options_array.append('unlink:Unlink');
		audit_options_array.append('chmod:Change mod');
		
		test_array = [];

		for audit_options in audit_options_array:
			options = audit_options[:audit_options.find(':')];

			options = options.strip();
			test_array.append(options);

		audrecycle_checked = '';
		auditing_checked   = '';
		recycle_checked    = '';

		aud_disp_style     = 'none';
		recycle_style      = 'none';
		file_dir_style     = 'none';
		
		exist_audits_array = [];
		audits_array       = [];
		audit_dropdown     = '';
		audit_recycle      = '';
		recycle_path1      = '';

		audit_option = audit_option.strip();

		if (audit_option == 'yes'):
			audits_array = smb_line['audit_opts'].split(' ');

			for exist_audits in audits_array:
				exist_audits = exist_audits.strip();

				if (exist_audits == 'connect'):
					conn_text = 'connect:Connect';

				if (exist_audits == 'disconnect'):
					conn_text = 'disconnect:Disconnect';
			
				if (exist_audits == 'opendir'):
					conn_text = 'opendir:Open dir';

				if (exist_audits == 'mkdir'):
					conn_text = 'mkdir:Make dir';

				if (exist_audits == 'rmdir'):
					conn_text = 'rmdir:Remove dir';

				if (exist_audits == 'closedir'):
					conn_text = 'closedir:Close dir';

				if (exist_audits == 'open'):
					conn_text = 'open:Open';

				if (exist_audits == 'close'):
					conn_text = 'close:Close';

				if (exist_audits == 'read'):
					conn_text = 'read:Read';

				if (exist_audits == 'pread'):
					conn_text = 'pread:PRead';

				if (exist_audits == 'write'):
					conn_text = 'write:Write';

				if (exist_audits == 'pwrite'):
					conn_text = 'pwrite:PWrite';

				if (exist_audits == 'sendfile'):
					conn_text = 'sendfile:Send file';

				if (exist_audits == 'rename'):
					conn_text = 'rename:Rename';

				if (exist_audits == 'unlink'):
					conn_text = 'unlink:Unlink';

				if (exist_audits == 'chmod'):
					conn_text = 'chmod:Change mod';

				try:
					if (test_array.index(exist_audits) >= 0):
						exist_audits_array.append(conn_text);
						audit_options_array.pop(audit_options_array.index(conn_text));

				except:
					print

			# generate a dropdown with value and lable for the assigned features list box
			for exist_audits in exist_audits_array:
				value = exist_audits[:exist_audits.find(':')];
				lable = exist_audits[exist_audits.find(':') + 1:];

				audit_dropdown = audit_dropdown + "<option value = '" + value + "' selected>" + lable + "</option>";

			audit_dropdown = audit_dropdown.strip();

			# check the condition for audit and recycle
			if (audit_option != 'no' and recycle_opt != 'no'):
				audrecycle_checked = 'checked';
				auditing_checked   = 'checked';
				recycle_checked    = 'checked';

				file_dir_style     = 'block';
				aud_disp_style     = 'block';
				recycle_style      = 'block';

			if (audit_option == 'yes' and recycle_opt == 'no'):
				audrecycle_checked    = 'checked';
				auditing_checked      = 'checked';

				file_dir_style     = 'block';
				aud_disp_style     = 'block';
				recycle_style      = 'none';

			if (recycle_opt != 'no'):
				audrecycle_checked = 'checked';
				recycle_checked    = 'checked';

				aud_disp_style     = 'block';
				recycle_style      = 'block';

			if (audit_option == 'yes' or recycle_opt == 'yes'):
				recycle_path = smb_line['recycle_repo'];

				recycle_path1 = recycle_path[recycle_path.find('/storage/') + len('/storage/'):];
				recycle_path1 = recycle_path1.strip();

		if(smb_line["recycle_repo"] == ''):
			recycle_chk = ""
			aud_rec_chk = ""
			recycle_style = "none"
			aud_disp_style = "none"
		else:
			recycle_chk = "checked"
			aud_rec_chk = "checked"
			recycle_style = "block"
			aud_disp_style = "block"

		if (public == 'no' and valid_user != ''):
			valid_users_style  = 'table';
			valid_groups_style = 'table';

		if (use_smb == 'on'):
			smb_selected  = 'checked';
			smb_opt_style = 'block';
		
		elif (use_smb == 'off'):
			smb_selected  = '';
			smb_opt_style = 'none';

		print common_methods.wait_for_response;
		usersfilesarray = [];

		print
		print """

	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer">
		<!--<div class="insidepage-heading">NAS >> <span class="content">Configure Information</span></div>-->"""

		if (statmessage != ''):
			print """<div id='""" + id_divname + """'>"""
			print statmessage;
			print """</div>"""

		print """<!--tab srt-->
		<div class="searchresult-container">
		  <div class="infoheader">
		    <div id="tabs">
		      <!--<ul>
			<li><a href="#tabs-1">SMB Settings</a></li>
		      </ul>-->
		      <div id="tabs-1">

		<!--form container starts here-->
		<!--<div class="form-container">-->
		<div style="padding:10px; background-color:#e9e5e5; border-bottom:#D1D1D1 1px solid; font-weight:bold;">SMB Settings for '"""+get_share+"""' 
<!--<a href = 'main.py?page=cs'><img style="float:right; padding:0px;" title = 'Back to shares' src = '../images/gobacktoshares.png' /></a>-->
</div>

		<!--<div class="view_option" style = 'border: 0px solid;'><a href = 'main.py?page=cs'><img title = 'Back to shares' src = '../images/gobacktoshares.png' /></a></div>-->
		<form name = 'share_edit' method = 'post' action = 'edit_shares.py'>
		  <div class="inputwrap">
		<!--<table width="100%" style="padding:0 0 0 10px;">
			<tr>
			<td>
				<input type='checkbox' name='use_smb' onclick = 'return show_smb_params();' /> Use SMB
			</td>
			<td></td>
			</tr>
		</table>-->

		<div width = '100%' id = 'smb_params'>
		<table width="100%" style="padding:30px 0 0 30px;">
		<tr>
		<td>
		<td>
		</tr>
			<tr>
			<td class="formrightside-content"><input type = 'checkbox' name = 'read_only' """ + writable_checked + """ """ + smbdisabled + """ """ + alldisabled + """>&nbsp;Read only</td>
			<td></td>
			</tr>

			<tr>
			<td class="formrightside-content"><input  type = 'checkbox' name = 'visible' """ + visible_checked + """ """ + smbdisabled + """ """ + alldisabled + """>&nbsp;Visible <br/><br/>
	<div style = "float:right;width:45%;margin-top:-14%;">
	<BR><B style = "color:darkred;">User access permissions:</B><BR><BR>
							<input type = 'radio' name = 'priv' value = 'public' onclick = 'return show_smb_users_groups();' """ + public_checked + """ """+smbdisabled+""">Public<BR>
							<input type = 'radio' name = 'priv' value = 'valid_user' onclick = 'return show_smb_users_groups();' """ + validuser_checked + """ """+smbdisabled+"""> Authenticated User
							<input type = 'hidden' name = 'hid_message' value = ''>
	<input type="hidden" name="get_ha_nodename" value='"""+get_ha_nodename+"""' />

							<div  width = '100%' id = 'users_list' style = 'display: """ + valid_users_style + """; margin-left:-100%; '>
							<table style="margin-left:0;"><tr>
								<td colspan = '2'>
									<BR><!--<B style="color:#EC1F27;">Users list:</B>--><B style="color:darkred;">Users list:</B><BR>"""

		domainsarray.sort();
		
		print """        <BR><B>Choose a domain:</B><div class="styled-select2" style="width:184px;"><select name = 'domainslist'>
		<option value ='sel_domain'>Select Domain</option>
		"""
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

		print """        </select></div><BR/><BR />"""
		print """</td>
									</tr>
									<tr>
										<td>
											<!--<B Style="color:#999999;">Available:</B>-->
										</td>
										<td>
											<!--<B style ="color:#999999;">Authorized:</B>-->
										</td>
									</tr>
									<tr>
										<td valign = 'top'><div style="margin-top:20%;">"""

		# if the number of users are more than 1000 then a textbox will appear in the place of dropdown.
		# the user has to enter the smb user he wants to see. as he types, a list of names will appear from which he can select
		print """<B>Available Users:</B><BR><input id = 'sssavailable' name = 'ads_user_text' type="text" class = 'textbox' value = '' onclick = 'document.getElementById("available").style.display = "none"; document.getElementById("available_groups").style.display = "none";'><input class = 'input1' type = 'button' name = 'getusers' value = 'Check'  onclick = 'return get_user_suggestions(document.getElementById("granted").options, document.getElementById("granted_groups").options, document.share_edit.read_only.checked, document.share_edit.visible.checked, document.share_edit.domainslist.value, this.form.sssavailable.value, "users", document.share_edit.hid_separator.value, \"""" + get_share + """", "smb", \"""" + str(smbuserslength) + """", \"""" + connstatus + """");' """ + alldisabled + """ >"""


		print """<select class = 'input' style = 'width: 200px; height: 300px; display: """ + users_list_style + """;' id = 'available' name = 'avail_users' multiple onclick = 'return move_users(this.form.available, this.form.granted, "1");' onkeydown = 'return get_key();' """ + alldisabled + """>"""
		print get_users_string;

		print """
		</select>
										</div></td>
										<td></td><td><B>Authorized Users:</B> <BR><div style="float: right;">
											<select class = 'input' style ="width:300px; height:140px;" id = 'granted' name = 'grant_users[]' multiple onclick = "return move_users(this.form.granted, this.form.available, '2');" """ + alldisabled + """>""";
		print users_dropdown;

		print """									
											</select>
										</div></td>
									</tr>
									<tr>
										<td align = 'right'>
										</td>
									</tr>
									<tr>
										<td></td>
									</tr>
									</table></div>
									<div id = 'groups_list1' style="display: """ + valid_groups_style + """;margin-left:-99%;">
									<table style="margin-top:0;">
									<tr>
										<td colspan = '2'>
										<BR><!--<B style="color:#EC1F27;">Groups list:</B>--><B style="color:darkred;">Groups list:</B><br/>
										</td>
									</tr>
									<!--<tr>
										<td>
											<B style="color:#999999;">Available:</B>
										</td>
										<td>
											<B style="color:#999999;">Authorized:</B>
										</td>
									</tr>-->
									<tr>
										<td><div style="margin-top:0;">"""


		# if the number of groups are more than 1000 then a text box will appear in place of the dropdown
		# the user needs to enter the name of the smb group he wants to see. the names will be displayed below starting with the characters he entered.
		print """<B>Available Groups:</B><BR>
		<input id = 'ssavailable_groups' name = 'ads_group_text' type="text" class = 'textbox' value = '' onclick = 'document.getElementById("available_groups").style.display = "none"; document.getElementById("available").style.display = "none";'><input class = 'input1' type = 'button' name = 'getgroups' size ="10" value = 'Check' onclick = 'return get_user_suggestions(document.getElementById("granted").options, document.getElementById("granted_groups").options, document.share_edit.read_only.checked, document.share_edit.visible.checked, document.share_edit.domainslist.value, this.form.ssavailable_groups.value, "groups", document.share_edit.hid_separator.value, \"""" + get_share + """", "smb", \"""" + str(smbgroupslength) + """", \"""" + connstatus + """");' """ + alldisabled + """ /><!--<input class = 'input1' type = 'button' name = 'move' value = '>' onclick = "move_group_to_dropdown(this.form.available_groups, this.form.granted_groups, '1');\" """ + alldisabled + """>-->""";

		print """<select class = 'input' style = 'display: """ + groups_list_style + """; width: 200px; height: 300px;' id = 'available_groups' name = 'avail_groups' multiple onclick = 'return move_groups(this.form.available_groups, this.form.granted_groups, "1");' """ + alldisabled + """>"""
		print get_groups_string;
			
		print """
		</select>
								</div></td>
											<td><B style="margin-left: 30px;">Authorized Groups:</B> <BR><div style="float: right;margin-left:30px;" >
												<select class = 'input' style = 'width:300px;height:140px;' id = 'granted_groups' name = 'grant_groups[]' multiple onclick = "return move_groups(this.form.granted_groups, this.form.available_groups, '2');" %s>""" % alldisabled;
		print groups_dropdown;

		print """</select>
										</div></td>
									</tr>
								</table>
							</div>
								</div>
							</td>
						</tr>
					</table><BR>
				<BR><div style = 'margin-left: 4%;color:darkred;'><B>Auditing/Recycling:</B></div><BR>

				<input id = 'id_select_adv' type = 'checkbox' name = 'aud_recycle' onclick = 'return show_hide(document.getElementById("id_select_adv").checked, document.getElementById("id_adv_feature"));' style = 'margin-left: 4%;' """+aud_rec_chk+""" """ + audrecycle_checked + """ """+smbdisabled+"""> <b style="color:#7F7979;">Enable Auditing/Recycling</b><br/><br/>

		<div id = 'id_adv_feature' style = 'margin-left: 6%; display:""" + aud_disp_style + """;color:#7F7979;'>
		<input id = 'id_auditing' """+disable_en_audit+""" type = 'checkbox' name = 'enable_audit' onclick = 'return show_hide(document.getElementById("id_auditing").checked, document.getElementById("id_file_ops"));' """ + auditing_checked + """>&nbsp; <B>Enable Auditing</B> """+enable_audit_mess+""" <div id = 'id_file_ops' style = 'width: 100%; margin-left: 2%; display: """ + file_dir_style + """;'>

		<br/><B>File / Dir operations:</b><br/>
										<select id = 'id_avail_options' class = 'textbox' name = 'file_options[]' multiple style = 'height: 100px; width: 20%;' onclick = 'return move_users(this.form.id_avail_options, id_assign_options, "1");' >"""

		for audit_opts in audit_options_array:
			value = audit_opts[:audit_opts.find(':')];
			lable = audit_opts[audit_opts.find(':') + 1:];

			print """<option value = '""" + value + """'>""" + lable + """</option>""";

		print """</select>
										<select id = 'id_assign_options' class = 'textbox' name = 'file_options[]' multiple style = 'height: 100px; width: 20%;' onclick = 'return move_users(this.form.id_assign_options, this.form.id_avail_options, "2");'>"""
		print audit_dropdown;
		print """
									       </select>
									</div><br/>

		<input id = 'id_enable_recycle' type = 'checkbox' name = 'enable_recycle' onclick = 'return show_hide(document.getElementById("id_enable_recycle").checked, document.getElementById("id_recycle_options"));' """+recycle_chk+"""""" + recycle_checked + """>&nbsp; <B>Enable Recycling</B><br/><br/>

		<div id = 'id_recycle_options' style = 'display: """ + recycle_style + """; margin-left: 2%;'>
		<B>Recycle Path</B>
		<select class = 'textbox' name = 'recycle_path' style = 'width: 60%;' >"""
		if (len(all_shares_array) > 0):
			for sharestring in all_shares_array:
				share_name = sharestring[:sharestring.find('-')].strip();
				share_path = sharestring[sharestring.find('-') + 1:].strip();
				disp_sharepath = share_path.replace('/storage/', '');

				if (share_name != get_share):
					if (recycle_path == share_path):
						print """<option value = '""" + disp_sharepath + """' selected>""" + share_name + """ - """ + disp_sharepath + """</option>""";

					else:
						print """<option value = '""" + disp_sharepath + """'>""" + share_name + """ - """ + disp_sharepath + """</option>""";

		print """</select>
		</div>
		</div>


				<table align = 'center' width = '100%'>
					<tr>
						<td>"""
		print common_methods.wait_for_response;
		share   = get_share.strip();
		path    = path.replace('/storage/', '');
		path    = path.strip();

		comment = comment.replace('\n', '');
		comment = comment.strip();

		print """
						</td>


		</div>

				</td>
				<td></td>
				</tr>

			</table>
			<input type = 'hidden' name = 'hid_separator' value = '""" + ads_separator + """' />
			<input type = 'hidden' name = 'hid_share' value = '""" + get_share + """' />
			<input type = 'hidden' name = 'hid_path' value = '""" + path + """' />
			<input type = 'hidden' name = 'hid_comment' value = '""" + comment + """' />"""
		print common_methods.wait_for_response;
		print """	</div>"""

		if (use_smb == 'on'):
			print """
			<button """+button_disabled+""" class="buttonClass" type="submit" name = 'removeconf'  value = 'removeconf'  style="float:right; margin:0 120px 0 0;">Remove</button>
			<button """+button_disabled+""" class="buttonClass" type = "submit"  name="reconf" value="reconf" style="float:right; margin:0 10px 0 0;" >Update</button>"""

		else:
			print """<button """+button_disabled+""" class="buttonClass" type="submit"  name='conf' value='conf' style="float:right; margin:0 120px 0 0;" >Configure</button>"""

		print """	</div>"""





		print """          </div>
	<p>&nbsp;</p>
	</div>
	</form>"""
	print """<!--form container ends here-->
	      <!--</div>-->

	  </div>
	</div>
	</div>
	"""
except Exception as e:
	disp_except.display_exception(e);
