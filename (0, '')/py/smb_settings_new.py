#!/usr/bin/python
import cgitb, header, sys
cgitb.enable()
sys.path.append('../modules/')
import disp_except;

try:
	import common_methods, os

	sys.path.append('/var/nasexe/python/');
	import smb, tools;
	from fs2global import *;

	#print 'Content-Type: text/html'
	import left_nav

	path    = '';
	comment = '';

	message = '';
	adsdomain = common_methods.ads_domain;
	connstatus = common_methods.conn_status();

	querystring = os.environ["QUERY_STRING"];
	get_share = '';
	ug = '';
	readonly = '';
	visible  = '';

	domain_only       = '';
	smbdisabled       = '';
	writable_checked  = 'checked';
	guest_checked     = '';
	public_checked    = 'checked';
	validuser_checked = '';
	visible_checked   = '';
	conn_text         = '';
	alldisabled       = '';
	domainname        = '';
	users_dropdown    = '';
	groups_dropdown   = '';

	use_smb           = '';
	public            = '';
	valid_user = '';
	smb_line   = '';
	share_details = [];

	if (querystring.find('share_name=') >= 0):
		get_share = querystring[querystring.find('share_name=') + len('share_name='):];

	if (get_share == ''):
		#print "<script>alert('Share name missing!');</script>";
		print "<script>location.href = 'main.py?page=cs';</script>";
		
	if (querystring.find('ug=') >= 0):
		ug = querystring[querystring.find('ug=') + len('ug='):querystring.find('&share_name')];

	valid_users_style  = 'none';
	valid_groups_style = 'none';

	users_list_style  = 'none';
	groups_list_style = 'none';

	sharesmbdetails = smb.show(get_share);

	if (sharesmbdetails['id'] == 0):
		smb_line = sharesmbdetails['share'];
		use_smb  = smb_line['use_smb'];

		# condition if SMB is enabled
		writable   = smb_line['writable'];
		browsable  = smb_line['browsable'];
		public     = smb_line['public'];
		guest_ok   = smb_line['guest_ok'];
		valid_user = smb_line['valid_users'];

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

	assusrfile = 'assusersfile';
	assgrpfile = 'assgroupsfile';

	assusrstring = '';
	assgrpstring = '';

	assusrarray = [];
	assgrparray = [];

	#os.remove('searchusersfile.txt');
	#os.remove('searchgroupsfile.txt');

	domainname = querystring[querystring.find('&dom=') + len('&dom='):];

	if (ug != ''):
		validuser_checked = 'checked';

		assusrarray = common_methods.read_file(assusrfile);
		assgrparray = common_methods.read_file(assgrpfile);

		if (len(assusrarray) > 0):
			for assu in assusrarray:
				assu_internal = common_methods.replace_chars(assu, 'chartotext');
				disp_assu     = assu[assu.find('+') + 1:];
				users_dropdown += '<option value = "' + assu_internal + '" selected>' + disp_assu + '</option>';

		if (len(assgrparray) > 0):
			for assg in assgrparray:
				assg_internal = common_methods.replace_chars(assg, 'chartotext');
				disp_assg     = assg[assg.find('+') + 1:];
				groups_dropdown += '<option value = "@' + assg + '" selected>' + assg + '</option>';

		domainname = querystring[querystring.find('&dom=') + len('&dom='):];
		get_share  = querystring[querystring.find('share_name=') + len('share_name='):querystring.find('&ro=')];
		readonly   = querystring[querystring.rfind('&ro=') + len('&ro='):querystring.rfind('&v=')];
		visible    = querystring[querystring.rfind('&v=') + len('&v='):];

		domainname = domainname.strip();
		readonly   = readonly.strip();
		visible    = visible.strip();

		if (ug == 'users'):
			valid_users_style  = 'table';
			valid_groups_style = 'table';
			users_list_style   = 'table';
			groups_list_style  = 'none';

			get_users_array = [];
			get_users_array = common_methods.read_file('searchusersfile.txt');

			for get_users in get_users_array:
				if (get_users != ''):
					get_usersinternal = common_methods.replace_chars(get_users, 'chartotext');
					get_disp_users    = get_users[get_users.find('+') + 1:];
		
					get_users_string += '<option value = "' + get_usersinternal + '">' + get_disp_users + '</option>';

		if (ug == 'groups'):
			valid_groups_style = 'table';
			valid_users_style  = 'table';
			groups_list_style  = 'table';
			users_list_style   = 'none';

			get_groups_array = [];
			get_groups_array = common_methods.read_file('searchgroupsfile.txt');

			for get_groups in get_groups_array:
				if (get_groups != ''):
					get_groupsinternal = common_methods.replace_chars(get_groups, 'chartotext');
					get_disp_groups    = get_groups[get_groups.find('+') + 1:];
					print get_disp_groups;

					if (get_groups.find('@') >= 0):
						get_groups_string += '<option value = "' + get_groupsinternal + '">' + get_disp_groups + '</option>';

					else:
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

	print all_users_list;

	smb_all_users_array  = [];
	smb_all_groups_array = [];

	domainsarray            = [];
	available_domains_array = [];
	params_array            = [];

	if (connstatus == 'Join is OK'):
		domainsarray = common_methods.get_all_domains();

	smbuserslength  = 0;
	smbgroupslength = 0

	# if userslist is not empty
	if (all_users_list['id'] == 0):
		common_methods.sendtologs('INFO', 'Get Users', 'UI', 'Retrieved the users list at smb_settings.py!');

		if (connstatus == 'Join is OK'):
			#checkusersfile = commands.getstatusoutput('ls adsusersfile');
			adsusersfile   = 'adsusersfile';
			checkusersfile = tools.check_file_exits(adsusersfile);

			if (checkusersfile == 'exists'):
				smb_all_users_array = open('adsusersfile', 'r');
				smbuserslength      = common_methods.get_users_count();

		else:
			smb_all_users_array  = all_users_list['users'];
			smbuserslength       = len(smb_all_users_array);

	# if groupslist id not empty
	if (all_groups_list['id'] == 0):
		common_methods.sendtologs('INFO', 'Get Groups', 'UI', 'Retrieved the groups list at smb_Settings.py!');

		if (connstatus == 'Join is OK'):
			#checkgroupsfile = commands.getstatusoutput('ls adsgroupsfile');
			adsgroupsfile = 'adsgroupsfile';
			checkgroupsfile = tools.check_file_exits(adsgroupsfile);

			if (checkgroupsfile == 'exists'):
				smb_all_groups_array = open('adsgroupsfile', 'r');
				smbgroupslength      = common_methods.get_groups_count();

		else:
			smb_all_groups_array = all_groups_list['groups'];
			smbgroupslength      = len(smb_all_groups_array);

	"""
	if (connstatus == 'Join is OK'):
		get_domains_list = commands.getstatusoutput('sudo wbinfo -m');

		if (get_domains_list[0] == 0):
			domainsarray = get_domains_list[1].split('\n');

		if (len(domainsarray) > 0):
			for i in domainsarray:
				i = i.strip();
				#checkdomain = commands.getstatusoutput('wbinfo -g|grep "^%s"' % i);
				checkdomain = commands.getstatusoutput('cat adsgroupsfile|grep "^%s"' % i);

				if (checkdomain[0] == 0):
					available_domains_array.append(i);

		if (len(available_domains_array) > 1):
			smb_all_users_array  = [];
			smb_all_groups_array = [];

			for domains in available_domains_array:
				usersfiletocreate  = '/tmp/' + domains + '_users.txt';
				groupsfiletocreate = '/tmp/' + domains + '_groups.txt';

				#usersofdomainres  = commands.getstatusoutput('sudo cat /tmp/adsusersfile|grep "^%s" > %s' % (domains, usersfiletocreate));
				#groupsofdomainres = commands.getstatusoutput('sudo cat /tmp/adsgroupsfile|grep "^%s" > %s' % (domains, groupsfiletocreate));
	"""
	smb_full_users_string  = '';
	smb_full_groups_string = '';

	#if (connstatus == 'Join is OK'):
	# check log path so that if the current share is enabled as log path, then auditing should not be allowed on the 
	# same share path. that share should become a readonly share
	#check_log_path_command = 'sudo grep "SMBLOGPATH=" /var/nasconf/smb-log.conf';
	#check_log_path         = commands.getoutput(check_log_path_command);
	check_log_path = tools.get_string_from_file('SMBLOGPATH=', '/var/nasconf/smb-log.conf');

	lpath = '';

	if (check_log_path != 'not found'):
		temp = [];
		temp = check_log_path.split('=');

		d12   = temp[0];
		lpath = temp[1];

	# check whether a SMB is enabled for a share or not

	#{'share': {'comment': '', 'audit_opts': '', 'browsable': 'no', 'recycle_enable': 'no', 'use_smb': 'on', 'writable': 'yes', 'recycle_repo': '', 'guest_ok': 'no', 'path': '/storage/x_test/testshare', 'file_perm': '0755', 'name': 'testshare', 'dir_perm': '0665', 'valid_users': '"CITRITE+vijayalakv" "CITRITE+vijayas" "CITRITE+vijayasulo2" "CITRITE+vijayb" "CITRITE+vijayd" "CITRITE+vijayendra1" "CITRITE+domain admins" "CITRITE+domain computers" "CITRITE+domain controllers"', 'audit_enable': 'no', 'public': 'no'}, 'id': 0, 'desc': 'INFO: configuration information for share testshare get successfully.'} 
	# the details of the share are retrieved from the /tmp/details_of_share file 
	#smb_line = commands.getstatusoutput('sudo grep "use_smb=" /tmp/details_of_share');
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

	if (path == lpath):
		smbdisabled      = 'disabled';
		smb_selected     = 'checked';
		writable_checked = 'checked';
		visible_checked  = 'checked';

	auditdisabled = '';
	auditmessage  = '';

	# if log path is not set for the share then auditing can't be set.
	# since for auditing, log path should be enabled
	if (lpath == ''):
		auditdisabled    = 'disabled';
		auditing_checked = '';
		file_dir_style   = 'none';
		auditmessage     = '  <B>(Please set smb log path to enable auditing option.)</B>';

		#delete_entry_command = 'sudo /var/nasexe/delete_entry "full_audit:" share_conf_file /var/nasconf/';
		#commands.getoutput(delete_entry_command);

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

		if (len(users_array) > 0 and smbuserslength > 0):
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

					elif (i.find('@') >= 0):
						i = i.replace('@', '');

						try:
							elemtoremove = smb_all_groups_array.index(i);

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

						users = common_methods.replace_chars(users, 'chartotext');

						# generate a dropdown for assigned ads users
						users_dropdown = users_dropdown + "<option value = '" + users + "' selected title = '" + users + "'>" + only_users + "</option>";
							
						users_only_array.append(only_users);

					elif (connstatus == 'nis is running'):
						# generate a dropdown for assigned nis users
						users_dropdown = users_dropdown + "<option value = '" + users + "' selected title = '" + users + "'>" + users + "</option>";

					elif (connstatus == 'local connection'):
						# generate a dropdown for assigned local users
						users_dropdown = users_dropdown + "<option value = '" + users + "' selected title = '" + users + "'>" + users + "</option>";

				# if the value of $user var has '@' in it, then that should be assigned to group variable.
				if (index_of_at > 0):
					users = users.replace('"', '');
					users = users.replace('@', '');

					groups = users;

					if (groups == ''):
						groups = d1;

					if (groups != ''):
						if (connstatus == 'Join is OK'):
							if (groups.find('+') > 0):
								only_groups = groups[groups.find('+') + 1:];
							
							else:
								only_groups = groups[groups.find('\\') + 1:];

							groups = common_methods.replace_chars(groups, 'chartotext');

							# generate a dropdown for assigned ads groups
							groups_dropdown = groups_dropdown + "<option value = '@" + groups + "' selected title = '" + groups + "'>" + only_groups + "</option>";
							groups_only_array.append(only_groups);

						elif (connstatus == 'nis is running'):
							# generate a dropdown for assigned nis groups
							groups_dropdown = groups_dropdown + "<option value = '@" + groups + "' selected title = '" + groups + "'>" + groups + "</option>";
							groupslist = groups_dropdown.replace('<', '[');

						elif (connstatus == 'local connection'):
							# generate a dropdown for assigned local groups
							groups_dropdown = groups_dropdown + "<option value = '@" + groups + "' selected title = '" + groups + "'>" + groups + "</option>";

	# assigned users
	assigned_users_string  = '';
	assigned_groups_string = '';
	ads_users_only_string  = '';
	ads_groups_only_string = '';
	smb_users_only         = '';
	smb_groups_only        = '';

	if (len(users_only_array) > 0):
		for assusers in users_only_array:
			assusers = common_methods.replace_chars(assusers, 'chartotext');
			assusers = assusers.strip();

			assigned_users_string += assusers + ':';

		assigned_users_string = assigned_users_string[:assigned_users_string.rfind(':')];
		assigned_users_string = assigned_users_string.strip();

		#assigned_users_string = ':'.join(users_only_array);

	if (len(groups_only_array) > 0):
		for assgroups in groups_only_array:
			assgroups = common_methods.replace_chars(assgroups, 'chartotext');
			assgroups = assgroups.strip();

			assigned_groups_string += assgroups + ':';

		assigned_groups_string = assigned_groups_string[:assigned_groups_string.rfind(':')];
		assigned_groups_string = assigned_groups_string.strip();

		#assigned_groups_string = ':'.join(groups_only_array);
			
	#common_methods.test_for_smb = '';
	#connstatus = 'Join is OK';

	if (common_methods.test_for_smb == '' and connstatus == 'Join is OK'):
		message = '<div style = "margin-left: 20%; margin-top: 10%; font: 13px Arial; color: darkred;">Please check the \'Use SMB\' option in Basic Setup -> SMB Settings for ADS</div>';

		print message;

		print """<form name = 'share_edit' id = 'id_smb_form' action = 'edit_shares.py' method = 'POST'>
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
		if (smbuserslength > 1000 and connstatus == 'Join is OK'):
			count_usr = 1000;

			"""
			for smbusers in smb_all_users_array:
				smbusers = common_methods.replace_chars(smbusers, 'chartotext');
				smbusers = smbusers.strip();

				if (smbusers.find('\\') > 0):
					smb_users_only = smbusers[smbusers.find('\\') + 1:];

				else:
					smb_users_only = smbusers[smbusers.find('+') + 1:];

				ads_users_only_string += smb_users_only + ':';

			ads_users_only_string = ads_users_only_string[:ads_users_only_string.rfind(':')];
			ads_users_only_string = ads_users_only_string.strip();
			"""

			user_message = '<BR><font color = \'darkred\' style = \'italic\'>Too many users.<BR>Please type the user name in the text box.</font>';

		else:
			count_usr = 2;
				
			ads_users_only_string = '';
			user_message = '';

		#if (len(ads_groups_array) > 1000):
		if (smbgroupslength > 1000 and connstatus == 'Join is OK'):
			count_grp = 1000;
			"""
			for smbgroups in smb_all_groups_array:
				smbgroups = common_methods.replace_chars(smbgroups, 'chartotext');
				smbgroups = smbgroups.strip();

				if (smbgroups.find('\\') > 0):
					smb_groups_only = smbgroups[smbgroups.find('\\') + 1:];

				else:
					smb_groups_only = smbgroups[smbgroups.find('+') + 1:];

				ads_groups_only_string += smb_groups_only + ':';

			ads_groups_only_string = ads_groups_only_string[:ads_groups_only_string.rfind(':')];
			ads_groups_only_string = ads_groups_only_string.strip();
			"""

			group_message = '<BR><font color = \'darkred\' style = \'italic\'>Too many groups.<BR>Please enter a specific group name in the text box.</font>';

		else:
			count_grp = 2;

			ads_groups_only_string = '';
			group_message = '';
				
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
		
		#check_log_path = commands.getoutput('sudo grep "' + lpath + '$" /var/nasconf/smb-log.conf');
		#check_log_path = get_string_from_file(lpath + '$', '/var/nasconf/smb-log.conf');

		exist_audits_array = [];
		audits_array       = [];
		audit_dropdown     = '';
		recycle_opt        = '';
		audit_recycle      = '';
		recycle_path1      = '';
		audit_option       = '';

		audit_recycle_line = tools.get_string_from_file('vfs objects=', '/tmp/details_of_share');
		audit_line         = tools.get_string_from_file('auditoption=', '/tmp/details_of_share');
		recycle_line       = tools.get_string_from_file('recycle_repo=', '/tmp/details_of_share');

		audit_recycle_line = audit_recycle_line.strip();
		audit_line         = audit_line.strip();
		recycle_line       = recycle_line.strip();

		if (audit_recycle_line != 'not found'):
			audit_recycle = audit_recycle_line[audit_recycle_line.find('=') + 1:];

		if (audit_line != 'not found'):
			audit_option = audit_line[audit_line.find('=') + 1:];
			audit_option = audit_option.strip();
			audits_array = audit_option.split(' ');

		if (recycle_line != 'not found'):
			recycle_opt   = recycle_line[recycle_line.find('=') + 1:];

		if (audit_option != 'not found'):
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
			if (audit_option != '' and recycle_opt != ''):
				audrecycle_checked = 'checked';
				auditing_checked   = 'checked';
				recycle_checked    = 'checked';

				file_dir_style     = 'block';
				aud_disp_style     = 'block';
				recycle_style      = 'block';

			if (audit_option != '' and recycle_opt == ''):
				audrecycle_checked    = 'checked';
				auditing_checked      = 'checked';

				file_dir_style     = 'block';
				aud_disp_style     = 'block';
				recycle_style      = 'none';

			if (recycle_opt != ''):
				audrecycle_checked = 'checked';
				recycle_checked    = 'checked';

				aud_disp_style     = 'block';
				recycle_style      = 'block';

			if (audit_option != '' or recycle_opt != ''):
				recycle_path = recycle_line[recycle_line.find('=') + 1:];

				recycle_path1 = recycle_path[recycle_path.find('/storage/') + len('/storage/'):];
				recycle_path1 = recycle_path1.strip();

		if (public == 'no'):
			valid_users_style  = 'table';
			valid_groups_style = 'table';

		if (use_smb == 'on'):
			smb_selected  = 'checked';
			smb_opt_style = 'block';
		
		elif (use_smb == 'off'):
			smb_selected  = '';
			smb_opt_style = 'none';

		print common_methods.wait_for_response;

		print
		print """

	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer">
		<div class="insidepage-heading">NAS >> <span class="content">Configure Information</span></div>
		<!--tab srt-->
		<div class="searchresult-container">
		  <div class="infoheader">
		    <div id="tabs">
		      <ul>
			<li><a href="#tabs-1">SMB Settings</a></li>
		      </ul>
		      <div id="tabs-1">

		<!--form container starts here-->
		<div class="form-container">
		<div class="view_option" style = 'border: 0px solid;'><a href = 'main.py?page=cs'><img title = 'Back to shares' src = '../images/go-back-icon.png' /></a></div>
		<form name = 'share_edit' method = 'POST' id = 'id_smb_form' action = 'edit_shares.py'>
		<!--<div class="topinputwrap-heading">SMB Settings for '"""+get_share+"""'</div>-->
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
		<div style="margin-top: -8%;"><font color ="#EC1F27">You are Configuring SMB Settings for</font><b>'<font color="green">"""+get_share+"""</font>'</b></div>
		<td>
		</tr>
			<tr>
			<td style="color:#7F7979;"><input type = 'checkbox' name = 'read_only' """ + writable_checked + """ """ + smbdisabled + """ """ + alldisabled + """>&nbsp;Read only</td>
			<td></td>
			</tr>

			<tr>
			<td style="color:#7F7979;"><input  type = 'checkbox' name = 'visible' """ + visible_checked + """ """ + smbdisabled + """ """ + alldisabled + """>&nbsp;Visible <br/><br/>
	<div style = "float:right;width:45%;margin-top:-14%;">
	<BR><B style = "color:darkred;">User access permissions:</B><BR><BR>
							<input type = 'radio' name = 'priv' value = 'public' onclick = 'return show_smb_users_groups();' """ + public_checked + """>Public<BR>
							<input type = 'radio' name = 'priv' value = 'valid_user' onclick = 'return show_smb_users_groups();' """ + validuser_checked + """> Authenticated User
							<input type = 'hidden' name = 'hid_message' value = ''>

							<div  width = '100%' id = 'users_list' style = 'display: """ + valid_users_style + """; margin-left:-100%; '>
							<table style="margin-left: -9%;"><tr>
								<td colspan = '2'>
									<BR><B style="color:#EC1F27;">Users list:</B><BR>""" + user_message + """<BR>"""

		if (len(domainsarray) > 1):
			domainsarray.sort();

			print """        <BR><select name = 'domainslist' class = 'textbox' onchange = 'return submit_domainlist(document.share_edit.domainslist.value);'>
					<option value = ''>Choose a domain</option>"""

			for domains in domainsarray:
				domains = domains.strip();

				if (domains == domainname):
					print """<option value = '""" + domains + """' selected>""" + domains + """</option>""";

				else:
					print """<option value = '""" + domains + """'>""" + domains + """</option>""";

			print """        </select><BR /><BR />"""
		print """</td>
									</tr>
									<tr>
										<td>
											<B Style="color:#999999;">Available:</B>
										</td>
										<td>
											<B style ="color:#999999;">Authorized:</B>
										</td>
									</tr>
									<tr>
										<td>"""

		# if the number of users are more than 1000 then a textbox will appear in the place of dropdown.
		# the user has to enter the smb user he wants to see. as he types, a list of names will appear from which he can select
		if (smbuserslength > 1000 and connstatus == 'Join is OK'):
			print """<input id = 'sssavailable' name = 'ads_user_text' type="text" class = 'input' value = '' onclick = 'document.getElementById("available").style.display = "none"; document.getElementById("available_groups").style.display = "none";'><input class = 'input1' type = 'button' name = 'getusers' value = 'Get Users'  onclick = 'return get_user_suggestions(document.getElementById("granted").options, document.getElementById("granted_groups").options, document.share_edit.read_only.checked, document.share_edit.visible.checked, document.share_edit.domainslist.value, this.form.sssavailable.value, "users");' """ + alldisabled + """ >
		<!--<input class = 'input1' type = 'button' name = 'move' value = '>'  onclick = "move_text_to_dropdown(this.form.available, this.form.granted, '1');\" """ + alldisabled + """ >-->""";


			print """<div id="suggest" style="visibility:hidden;border:#000000 1px solid;width:150px;"></div>
										<select class = 'input' style = 'width: 200px; height: 300px; display: """ + users_list_style + """;' id = 'available' name = 'avail_users' multiple onclick = 'return move_users(this.form.available, this.form.granted, "1");' onkeydown = 'return get_key();' """ + alldisabled + """>"""
			print get_users_string;
			print """</select>"""

		else:
			print """<select class = 'input' style = 'width: 150px; height: 140px;' id = 'available' name = 'avail_users' multiple onclick = "return move_users(this.form.available, this.form.granted, '1');\" """ + alldisabled + """>"""
			if (connstatus == 'Join is OK'):
				for ads_users in smb_all_users_array:
					#ads_users_to_check = '"' + ads_users + '"';

					if (ads_users.find('+') > 0):
						domain     = ads_users[:ads_users.find('+')];
						users_only = ads_users[ads_users.find('+') + 1:];
						#temp = ads_users.split('+');

					elif (ads_users.find('\\') > 0):
						domain     = ads_users[:ads_users.find('\\')];
						users_only = ads_users[ads_users.find('\\') + 1:];
						#temp = ads_users.split('\\');

					else:
						domain = '';
						usersonly = ads_users;
						#temp = ['', ads_users];

					print """<option value = '""" + ads_users + """' title = '""" + ads_users + """'>""" + users_only + """</option>""";

			if (connstatus == 'nis is running'):
				for nis_users in smb_all_users_array:
					nis_users_to_check = '"' + nis_users + '"';

					print """<option value = '""" + nis_users + """' title = '""" + nis_users + """'>""" + nis_users + """</option>""";

			if (connstatus == 'local connection'):
				for local_users in smb_all_users_array:
					print """<option value = '""" + local_users + """' title = '""" + local_users + """'>""" + local_users + """</option>"""

		print """
		</select>
										</td>
										<td>
											<select class = 'input' style ="width:150px; height:140px;" id = 'granted' name = 'grant_users[]' multiple onclick = "return move_users(this.form.granted, this.form.available, '2');" %s>""" % alldisabled;
		print users_dropdown;

		print """									
											</select>
										</td>
									</tr>
									<tr>
										<td align = 'right'>
										</td>
									</tr>
									<tr>
										<td></td>
									</tr>
									</table></div>
									<div id = 'groups_list1' style="display: """ + valid_groups_style + """;margin-top: -65%;">
									<table style="margin-left: -9%;">
									<tr>
										<td colspan = '2'>
										<BR><B style="color:#EC1F27;">Groups list:</B>""" + group_message + """<BR><br/>
										</td>
									</tr>
									<tr>
										<td>
											<B style="color:#999999;">Available:</B>
										</td>
										<td>
											<B style="color:#999999;">Authorized:</B>
										</td>
									</tr>
									<tr>
										<td>"""


		# if the number of groups are more than 1000 then a text box will appear in place of the dropdown
		# the user needs to enter the name of the smb group he wants to see. the names will be displayed below starting with the characters he entered.
		if (smbgroupslength > 1000 and connstatus == 'Join is OK'):
			print """<input id = 'ssavailable_groups' name = 'ads_group_text' type="text" class = 'input' value = '' onclick = 'document.getElementById("available_groups").style.display = "none"; document.getElementById("available").style.display = "none";'>
		<input class = 'input1' type = 'button' name = 'getgroups' value = 'Get Groups' onclick = 'return get_user_suggestions(document.getElementById("granted").options, document.getElementById("granted_groups").options, document.share_edit.read_only.checked, document.share_edit.visible.checked, document.share_edit.domainslist.value, this.form.ssavailable_groups.value, "groups");' """ + alldisabled + """ />
		<!--<input class = 'input1' type = 'button' name = 'move' value = '>' onclick = "move_group_to_dropdown(this.form.available_groups, this.form.granted_groups, '1');\" """ + alldisabled + """>-->""";

			print """<select class = 'input' style = 'display: """ + groups_list_style + """; width: 200px; height: 300px;' id = 'available_groups' name = 'avail_groups' multiple onclick = 'return move_groups(this.form.available_groups, this.form.granted_groups, "1");' """ + alldisabled + """>"""
			print get_groups_string;
			
			print """
			</select>""";

		else:
			print """
		<select class = 'input' style = 'width:150px; height: 140px;' id = 'available_groups' name = 'avail_groups' multiple onclick = "return move_groups(this.form.available_groups, this.form.granted_groups, '1');\" """ + alldisabled + """>"""

			if (connstatus == 'Join is OK'):
				for ads_groups in smb_all_groups_array:
					#temp = [];

					if (ads_groups.find('+') > 0):
						domain          = ads_groups[:ads_groups.find('+')];
						ads_groups_only = ads_groups[ads_groups.find('+') + 1:];

					elif (ads_groups.find('\\') > 0):
						domain          = ads_groups[:ads_groups.find('\\')];
						ads_groups_only = ads_groups[ads_groups.find('\\') + 1:];

						#temp = ads_groups.split('+');

					else:
						ads_groups_only = ads_groups;
						#temp = ['', ads_groups];

					#d1 = temp[0];
					#ads_groups_only = temp[1];

					ads_groups_to_check = '"@' + ads_groups + '"';

					print """<option value = '@""" + ads_groups + """' title = '""" + ads_groups + """'>""" + ads_groups_only + """</option>""";

			if (connstatus == 'nis is running'):
				for nis_groups in smb_all_groups_array:
					print """<option value = '@""" + nis_groups + """' title = '""" + nis_groups + """'>""" + nis_groups + """</option>""";

			if (connstatus == 'local connection'):
				for local_groups in smb_all_groups_array:
					local_groups = local_groups.strip();
					local_groups_to_check = '"@' + local_groups + '"';

					print """<option value = '@""" + local_groups + """' title = '""" + local_groups + """'>""" + local_groups + """</option>""";
		print """
		</select>
								</td>
											<td>
												<select class = 'input' style = 'width:150px;height:140px;' id = 'granted_groups' name = 'grant_groups[]' multiple onclick = "return move_groups(this.form.granted_groups, this.form.available_groups, '2');" %s>""" % alldisabled;
		print groups_dropdown;

		print """</select>
										</td>
									</tr>
								</table>
							</div>
								</div>
							</td>
						</tr>
					</table><BR>
				<BR><div style = 'margin-left: 4%;color:darkred;'><B>Auditing/Recycling:</B></div><BR>

				<input id = 'id_select_adv' type = 'checkbox' name = 'aud_recycle' onclick = 'return show_hide(document.getElementById("id_select_adv").checked, document.getElementById("id_adv_feature"));' style = 'margin-left: 4%;'> <b style="color:#7F7979;">Enable Auditing/Recycling</b><br/><br/>

		<div id = 'id_adv_feature' style = 'margin-left: 6%; display:none;color:#7F7979;'>
		<input id = 'id_auditing' type = 'checkbox' name = 'enable_audit' onclick = 'return show_hide(document.getElementById("id_auditing").checked, document.getElementById("id_file_ops"));' >&nbsp; Enable Auditing <div id = 'id_file_ops' style = 'margin-left: 2%; display: none;'>

		<br/>File / Dir operations:<br/>
										<select id = 'id_avail_options' class = 'textbox' name = 'file_options' multiple style = 'height: 100px; width: 25%;' onclick = 'return move_users(this.form.id_avail_options, id_assign_options, "1");' >"""

		for audit_opts in audit_options_array:
			value = audit_opts[:audit_opts.find(':')];
			lable = audit_opts[audit_opts.find(':') + 1:];

			print """<option value = '""" + value + """'>""" + lable + """</option>""";

		print """</select>
										<select id = 'id_assign_options' class = 'textbox' name = 'file_options[]' multiple style = 'height: 100px; width: 25%;' onclick = 'return move_users(this.form.id_assign_options, this.form.id_avail_options, "2");'>
									       </select>
									</div><br/>

		<input id = 'id_enable_recycle' type = 'checkbox' name = 'enable_recycle' onclick = 'return show_hide(document.getElementById("id_enable_recycle").checked, document.getElementById("id_recycle_options"));'>&nbsp; Enable Recycling<br/><br/>

		<div id = 'id_recycle_options' style = 'display: none; margin-left: 2%;'>
		Recycle Path
		<select class = 'textbox' name = 'recycle_path' style = 'width: 60%;' >
		<option></option>
		</select>
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
			<input type = 'hidden' name = 'hid_comment' value = '""" + comment + """' />
			<!--<button class="button_example" type="submit" name = 'local_action_but'  id = 'local_action_but' value = 'Apply'  onclick = 'validate_local_auth();' style="float:right; margin:0 100px 10px 0;">Apply</button>
			<button class="button_example" type="button" name = 'cancelbut'  id = 'cancel_but' value = 'Back'  onclick = 'location.href = "main.py?page=cs";' style="float:right; margin:0 100px 10px 0;">Back</button>-->
			<!--<button class="button_example" type="button" name = 'cancelbut'  id = 'cancel_but' value = 'Back'  onclick = 'location.href = "main.py?page=cs";' style="float:right;;">Back</button>&nbsp;&nbsp;&nbsp;-->"""
		print """</div>"""
		print common_methods.wait_for_response;

		if (use_smb == 'on'):
			print """
			<button class="button_example" type="submit" name = 'removeconf'  id = 'id_removeconf' value = 'removesmbconf'  onclick = 'return submit_smb_form("unconf");' style="float:right;">Un-Configure</button>
			<button class="button_example" type="submit" name = 'reconf'  id = 'id_reconf' value = 'editsmbconf'  onclick = 'return submit_smb_form("reconf");' style="float:right;">Re-Configure</button>"""

		else:
			print """<button class="button_example" type = "submit" name = 'conf'  id = 'id_conf' value = 'enablesmbconf'  onclick = 'return submit_smb_form("conf");' style="float:right;">Configure</button>"""

		print """	</div>"""





	print """          </div>
	<p>&nbsp;</p>
	</div>
	</form>
	<!--form container ends here-->
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
