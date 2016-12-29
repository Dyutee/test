#!/usr/bin/python
import share_details, commands, common_methods, share_smb_settings, sys, cgi, header, tracedebug, os

selected_share = share_details.share
selected_share_path  = share_details.path

sys.path.append('../modules/');
import disp_except;

sys.path.append('/var/nasexe/python/')
from fs2global import *
import anon_ftp
import ftp_auth
import commons

form = cgi.FieldStorage()

try:
	sys.path.append('/var/nasexe/python');
	import ftp;
	## New##
	ftp_access_ip = ''
	ftp_write_ip = ''
	sharename= ''
	
	ftp_assigned_users_string  = '';
	ftp_assigned_groups_string = '';

	if(header.form.getvalue("ftp_button")):
		auth_file = ftp_share_conf_dir+selected_share+".auth"
		anon_file = ftp_share_conf_dir+selected_share+".anon"
		check_auth_file_existance = os.path.isfile(auth_file)
		check_anon_file_existance = os.path.isfile(anon_file)

		enable_ftp = header.form.getvalue("enable_ftp")
		access_ip = header.form.getvalue("ftp_access_ip")
		write_ip = header.form.getvalue("ftp_write_ip")
		grant_users =header.form.getvalue("grant_users[]")
		grant_groups =header.form.getvalue("grant_groups[]")
		selected_mode = header.form.getvalue("choose_ftp_options")

		#ftp_mount = commons.unmount_ftp(selected_share);

		new_gu_array = [];
		new_gg_array = [];

		a = grant_users;
		b = grant_groups;

		a = str(a);
		b = str(b);

		if (a.find('[') == 0):
			if (len(grant_users) > 0):
				grant_users = [gu.replace('[AND]', '&') for gu in grant_users];
				grant_users = [gu.replace('[HASH]', '#') for gu in grant_users];
				grant_users = [gu.replace('[DOLLAR]', '$') for gu in grant_users];
				grant_users = [gu.replace('\\\\', '\\') for gu in grant_users];

		else:
			if (grant_users != None):
				grant_users = grant_users.replace('[AND]', '&');
				grant_users = grant_users.replace('[HASH]', '#');
				grant_users = grant_users.replace('[DOLLAR]', '$');
				grant_users = grant_users.replace('\\\\', '\\');

			"""
			if (str(grant_users).find('[AND]') > 0):
				grant_users = str(grant_users).replace('[AND]', '&');

			if (str(grant_users).find('[HASH]') > 0):
				grant_users = str(grant_users).replace('[HASH]', '#');

			if (str(grant_users).find('[DOLLAR]') > 0):
				grant_users = str(grant_users).replace('[DOLLAR]', '$');
			"""

		if (b.find('[') == 0):
			if (len(grant_groups) > 0):
				grant_groups = [gg.replace('[AND]', '&') for gg in grant_groups];
				grant_groups = [gg.replace('[HASH]', '#') for gg in grant_groups];
				grant_groups = [gg.replace('[DOLLAR]', '$') for gg in grant_groups];
				grant_groups = [gg.replace('\\\\', '\\') for gg in grant_groups];

		else:
			if (grant_groups != None):
				grant_groups = grant_groups.replace('[AND]', '&');
				grant_groups = grant_groups.replace('[HASH]', '#');
				grant_groups = grant_groups.replace('[DOLLAR]', '$');
				grant_groups = grant_groups.replace('\\\\', '\\');

			"""
			if (str(grant_groups).find('[AND]') > 0):
				grant_groups = str(grant_groups).replace('[AND]', '&');

			if (str(grant_groups).find('[HASH]') > 0):
				grant_groups = str(grant_groups).replace('[HASH]', '#');

			if (str(grant_groups).find('[DOLLAR]') > 0):
				grant_groups = str(grant_groups).replace('[DOLLAR]', '$');
			"""

		dict_value = {'sharename':selected_share,'ftp_access_ip':access_ip, 'ftp_write_ip':write_ip}
		dict_values_auth = {'sharename':selected_share, 'ftp_grant_users':grant_users, 'ftp_grant_groups':grant_groups}
		#dict_values_auth = {'sharename':selected_share, 'ftp_grant_users':new_gu_array, 'ftp_grant_groups':new_gg_array}

		if(enable_ftp == "on"):
			if(selected_mode == "anonymous"):
				if((check_anon_file_existance == False) and (check_auth_file_existance == True)):
					call_unmount = commons.unmount_ftp(selected_share)
					#print "UNMOUNT : "+str(call_unmount)
					#print "<br/>"
	
				ftp_auth.unconfigure(selected_share)
				anon_ftp.anonymous_configure(dict_value)

				if((check_anon_file_existance == False) and (check_auth_file_existance == True)):
                                        call_mount = commons.mount_ftp(selected_share)
					#print "MOUNT : "+str(call_mount)
					#print "<br/>"

				####### Restart the ProFTP when user press the "OK" confirmation button. #######

				print """<script>

				var r =confirm("The Active connections will be Reset for making the configuration changes. Do you want to Restart Pro FTP?");
				if(r==true)
				{
					alert("Pro FTP is Restarting!");

					$.ajax({
					type: 'POST',
					url: 'restart-proftpd.py',
					data: 'proceed_page=proceed',

					success: function(html)
					{
						$('#response').html(html);
					}
					});
				}
				else
				{
					alert("You choose not to restart Pro FTP this time but, you need to restart it to make changes occur!");
				}


				</script>"""
				####### END #######


			elif(selected_mode == "authenticated"):
				if((check_anon_file_existance == True) and (check_auth_file_existance == False)):
					call_unmount = commons.unmount_ftp(selected_share)
					#print "UNMOUNT : "+str(call_unmount)
					#print "<br/>"
	
				anon_ftp.anonymous_unconfigure(selected_share)
				ftp_auth.configure(dict_values_auth)

				if((check_anon_file_existance == True) and (check_auth_file_existance == False)):
                                        call_mount = commons.mount_ftp(selected_share)
					#print "MOUNT : "+str(call_mount)
					#print "<br/>"

			if((check_anon_file_existance == False) and (check_auth_file_existance == False)):
				call_mount = commons.mount_ftp(selected_share)
				#print "MOUNT : "+str(call_mount)



			print "<script>location.href = 'show_shares.py?s1=%s&act=share_ftp_done';</script>" % selected_share;

		else:
			call_unmount = commons.unmount_ftp(selected_share)
			#print call_unmount
			anon_ftp.anonymous_unconfigure(selected_share)
			ftp_auth.unconfigure(selected_share)

	get_display_dict = ftp_auth.get_status(selected_share)
	
	ftpassignedusersarray  = [];
	ftpassignedgroupsarray = [];

	# initialize the default state of the checkbox and display style and set the default values for the input boxes
	enable_ftp_checked = get_display_dict['enable_ftp_checked']
	ftp_main_table_style = get_display_dict['ftp_main_table_style']
	readonly_disable = get_display_dict['readonly_disable']
	readonly_checked = get_display_dict['readonly_checked']
	anonymous_checked = get_display_dict['anonymous_checked']
	authenticated_checked = get_display_dict['authenticated_checked']
	ftp_params_table_style = get_display_dict['ftp_params_table_style']
	ftpaccess_ip = get_display_dict['ftpaccess_ip']
	ftpwrite_ip = get_display_dict['ftpwrite_ip']
	ftp_users_table_style = get_display_dict['ftp_users_table_style']
	ftp_users_list = get_display_dict['ftp_users_list']
	ftp_groups_list = get_display_dict['ftp_groups_list']
	write_ip_disabled   = get_display_dict['write_ip_disabled']
	write_ip_background = get_display_dict['write_ip_background']
	ftp_assigned_users_array = get_display_dict['ftp_assigned_users_string']
	ftp_assigned_groups_array = get_display_dict['ftp_assigned_groups_string']
	#ftp_assigned_users_array = get_display_dict['ftp_assigned_users_array']
	#ftp_assigned_groups_array = get_display_dict['ftp_assigned_groups_array']
	#ads_domain_for_ftp = get_display_dict['ads_domain_for_ftp']
		
	if (len(ftp_assigned_users_array) > 0):
		for ftpu in ftp_assigned_users_array:
			if (ftpu.find('\\') > 0):
				ftpu = ftpu[ftpu.find('\\') + 1:];

			else:
				ftpu = ftpu[ftpu.find('+') + 1:];

			ftp_assigned_users_string += ftpu + ':';

		ftp_assigned_users_string = ftp_assigned_users_string[:ftp_assigned_users_string.rfind(':')];

	if (len(ftp_assigned_groups_array) > 0):
		for ftpg in ftp_assigned_groups_array:
			if (ftpg.find('\\') > 0):
				ftpg = ftpg[ftpg.find('\\') + 1:];

			else:
				ftpg = ftpg[ftpg.find('+') + 1:];

			ftp_assigned_groups_string += ftpg + ':';

		ftp_assigned_groups_string = ftp_assigned_groups_string[:ftp_assigned_groups_string.rfind(':')];

	##########################
	#MOhan Sir
	##########################
	# in readonly mode, the write ip text box is disabled and shaded
	ftpreadonly = '';

	log_file = common_methods.log_file;
	log_array = [];

	all_users_list  = '';
	all_groups_list = '';

	# get the uesrs list and groups list from the method get_users_string() defined in common_methods.py
	# the output will be in dictionary format
	all_users_list  = common_methods.get_users_string();
	all_groups_list = common_methods.get_groups_string();

	separator = '';

	ftp_all_users_array  = [];
	ftp_all_groups_array = [];

	ads_users_string  = '';
	ads_groups_string = '';

	# create ftp_all_users_array from the all_users_list dictionary
	if (all_users_list['id'] == 0):
		if (share_details.connstatus == 'Join is OK'):
			ftp_all_users_array = common_methods.read_file('/tmp/adsusersfile');

		else:
			ftp_all_users_array  = all_users_list['users']

		ftp_all_users_array = list(set(ftp_all_users_array) - set(ftp_users_list))

	# create ftp_all_groups_array from the all_groups_list dictionary
	if (all_groups_list['id'] == 0):
		if (share_details.connstatus == 'Join is OK'):
			ftp_all_groups_array = common_methods.read_file('/tmp/adsgroupsfile');

		else:
			ftp_all_groups_array = all_groups_list['groups'];

		ftp_all_groups_array = list(set(ftp_all_groups_array) - set(ftp_groups_list))

	if (len(ftp_all_users_array) > 0):
		ads_users_string = ':'.join(ftp_all_users_array);

	if (len(ftp_all_groups_array) > 0):
		ads_groups_string = ':'.join(ftp_all_groups_array);

	# copy the 'share' from share_details.py
	share_1 = share_details.share;
	path_1 = '/storage/' + share_details.path;
	 
	# initialize all the required variables
	ftpshare       = '';
	ftppath        = '';
	ftpcomm        = '';
	enable_ftp     = '';
	ftpusers_list  = '';
	ftpgroups_list = '';
	#ftpaccess_ip   = '';
	#ftpwrite_ip    = '';
	ftpreadonly    = '';
	ftpoptions     = '';

	sharename = share_details.share;

	check_shares1 = '';
	check_shares2 = '';

	if (check_shares1 != '' or check_shares2 != ''):
		getftpvalues = ftp.get(sharename);

		logstring = str(common_methods.now) + '<<>>From: ' + common_methods.remote_ip + '<<>>' + str(getftpvalues) + '<<>>Retrieved the ftp configuration';
		log_array.append(logstring);

		common_methods.append_file(log_file, log_array);

		ftpusers_line  = '';
		ftpgroups_line = '';

		enableftp     = getftpvalues['enableftp'];
		getftpmode    = getftpvalues['mode'];
		getftptype    = getftpvalues['ftp_type'];

		#if (getftptype == 'anonymous' and enableftp == 'on'):
			#ftpaccess_ip           = getftpvalues['ftpreadip'];
			#ftpwrite_ip            = getftpvalues['ftpwriteip'];
			#anonymous_checked      = 'checked';
			#ftp_params_table_style = 'table';

		#if (enableftp == 'on'):
			#enable_ftp_checked   = 'checked';
			#ftp_main_table_style = 'table';

		if (getftpmode == 'RO'):
			readonly_checked    = 'checked';
			write_ip_disabled   = 'disabled';
			write_ip_background = 'darkred';
			#ftp_params_table_style = 'table';

		if (getftpmode == 'RW'):
			readonly_checked = '';

		if (getftptype == 'authenticated'):
			#authenticated_checked = 'checked';
			readonly_disable      = 'disabled';
			#ftp_users_table_style = 'table';
			readonly_checked = '';

			ftpusers_line  = getftpvalues['ftpusers'];
			ftpgroups_line = getftpvalues['ftpgroups'];

			if (ftpgroups_line != ''):
				ftpgroups_line = ftpgroups_line.replace(' @', 'xxx@');

		ftp_users_array  = [];
		ftp_groups_array = [];

		ftp_users_array  = ftpusers_line.split(' ');
		ftp_groups_array = ftpgroups_line.split('xxx');

		# if the selected share is authenticated for ftp
		#if (authenticated_checked == 'checked'):
		#	if (len(ftp_users_array) > 0):
		#		for remusers in ftp_users_array:
		#			if (remusers.find('@') >= 0):
		#				remusers = remusers.replace('@', '');

		#			remusers = remusers.strip();
		
		#			if (ftp_all_users_array.index(remusers) >= 0):
		#				ftp_all_users_array.pop(ftp_all_users_array.index(remusers));

		#	if (len(ftp_groups_array) > 0):
		#		for remgroups in ftp_groups_array:
		#			if (remgroups.find('@') >= 0):
		#				remgroups = remgroups.replace('@', '');

		#			remgroups = remgroups.strip();

		#			if (ftp_all_groups_array.index(remgroups) >= 0):
		#				ftp_all_groups_array.pop(ftp_all_groups_array.index(remgroups));

		if (len(ftp_users_array) > 0):
			for ftpusers in ftp_users_array:
				#ftp_user_only = ftpusers;
				if (ftpusers.find('\\') > 0):
					ftp_user_only = ftpusers[ftpusers.find('\\') + 1:];

				else:
					ftp_user_only = ftpusers[ftpusers.find('+') + 1:];

				#if (ftp_user_only != ''):
					#ftp_users_list = ftp_users_list + '<option value = \'' + ftpusers + '\' selected title = \'' + ftpusers + '\'>' + ftp_user_only + '</option>';

				ftp_assigned_users_array.append(ftp_user_only);

		if (len(ftp_groups_array) > 0):
			for ftpgroups in ftp_groups_array:
				#ftp_group_only = ftpgroups;

				if (ftpgroups.find('\\') > 0):
					ftp_group_only = ftpgroups[ftpgroups.find('\\') + 1:];

				else:
					ftp_group_only = ftpgroups[ftpgroups.find('+') + 1:];

				#if (ftp_group_only != ''):
					#ftp_group_only = ftp_group_only.replace('@', '');
					#ftp_groups_list = ftp_groups_list + '<option value = \'' + ftpgroups + '\' selected title = \'' + ftpgroups + '\'>' + ftp_group_only + '</option>';

				ftp_assigned_groups_array.append(ftp_group_only);

		# construct a string from the created arrays
		if (len(ftp_assigned_users_array) > 0):
			ftp_assigned_users_string  = ':'.join(ftp_assigned_users_array);

		if (len(ftp_assigned_groups_array) > 0):
			ftp_assigned_groups_string = ':'.join(ftp_assigned_groups_array);

	print """		<form name = 'set_ftp_params' method = 'POST'>
				<table width = "685" border = "0" cellspacing = "0" cellpadding = "0" name = 'disp_tables' id = 'id_ftp_settings' style = 'display:  """ + share_details.share_ftp_style + """; """ + share_details.stylestring + """;'>
				<tr>
				<td>
				<table align = 'center' width = '100%'>
					<tr>"""
	print common_methods.th_begin;
	print """					<td width = "669" height = "33px" align = "left" valign = "middle" class = "right_bg rightsidemenuheading">
							<a class = 'link' href = 'ftp_help.php' onclick = "window.open('ftp_help.php', 'help', 'location = no, height = 500, width = 600, scrollbars = 1'); return false;">""" + common_methods.getimageicon() + """ </a>
							FTP settings
						</td>"""
	print common_methods.th_end;
	print """				</tr>
					<tr>
						<td colspan = "3" align = "left" valign = "top">
						<table width = "685" border = "0" cellspacing = "0" cellpadding = "0">
						<td>
							<input type = 'checkbox' name = 'enable_ftp' onclick = 'return show_ftp_params();'  """ + enable_ftp_checked + ' ' + share_smb_settings.smbdisabled + """ """ + share_details.alldisabled + """><B>Enable FTP access to this share</B>
						</td>
					</tr>
				</table>
				<div width = '100%' id = 'id_ftp_parameters' style = 'display:  """ + ftp_main_table_style + """;'>
				<table width = '100%'>
					<tr>
						<td colspan = '2'>
							<input type = 'checkbox' name = 'ftp_read_only' onclick = 'return set_ftp_parameters();'  """ + readonly_disable + ' ' + readonly_checked + ' ' + share_smb_settings.smbdisabled + """ """ + share_details.alldisabled + """><B>Read only</B><BR><BR>"""
							
	print """<input type = 'radio' name = 'choose_ftp_options' value = 'anonymous' id ="anon" onclick = 'return set_ftp_parameters();' """ + anonymous_checked + ' ' + share_smb_settings.smbdisabled + """ """ + share_details.alldisabled + """><B>Anonymous mode</B><BR>
							<input type = 'radio' name = 'choose_ftp_options' id ="auth" value = 'authenticated' onclick = 'return set_ftp_parameters();' """ + authenticated_checked + ' ' + share_smb_settings.smbdisabled + """ """ + share_details.alldisabled + """><B>Authenticated user</B><BR><BR>
						</td>
					</tr>
				</table>
				</div>
				<div width = '100%' id = 'ftp_params_table' style = 'display:  """ + ftp_params_table_style + """; font-weight: bold;'>
				<table style = 'font-weight: bold;'>
					<tr>
						<td>
							Allow access IP
						</td>
						<td>
							<input class = 'input' name = 'ftp_access_ip' id = 'id_access_ip' value = '""" + ftpaccess_ip + """' size = '55'""" + share_smb_settings.smbdisabled + """ """ + share_details.alldisabled + """>
						</td>
					</tr>
					<tr>
						<td>
							Allow write IP
						</td>
						<td>
							<input class = 'input' name = 'ftp_write_ip' id = 'id_write_ip' value = '""" + ftpwrite_ip + """' style = 'background:  """ + write_ip_background + """;' size = '55'  """ + write_ip_disabled + ' ' + share_smb_settings.smbdisabled + """ """ + share_details.alldisabled + """>
						</td>
					</tr>
				</table>
				</div>"""
				
	# if the number of ftp users are more than 1000, a user list is created and sent to javascript 
	# to display the users starting with the character entered
	if (len(ftp_all_users_array) > 1000):
		ads_users_only_string = '';

		for adsu in ftp_all_users_array:
			if (adsu.find('\\') > 0):
				adsu = adsu[adsu.find('\\') + 1:];

			else:
				adsu = adsu[adsu.find('+') + 1:];

			adsu = adsu.strip();
			ads_users_only_string += adsu + ':';


		ads_users_only_string = ads_users_only_string[:ads_users_only_string.rfind(':')];

		count_usr = 1000;
		user_message = '<BR><font color = \'darkred\' style = \'italic\'>Too many users.<BR>Please type the user name in the text box.</font>';

	else:
		count_usr = 2;
				
		ads_users_only_string = '';
		user_message = '';

	# if the number of ftp groups are more than 1000, a group list is created and sent to javascript 
	# to display the users starting with the character entered
	if (len(ftp_all_groups_array) > 1000):
		count_grp = 1000;

		ads_groups_only_string = '';

		for adsg in ftp_all_groups_array:
			if (adsg.find('\\') > 0):
				adsg = adsg[adsg.find('\\') + 1:];

			else:
				adsg = adsg[adsg.find('+') + 1:];

			adsg = adsg.strip();
			ads_groups_only_string += adsg + ':';

		ads_groups_only_string = ads_groups_only_string[:ads_groups_only_string.rfind(':')];

		group_message = '<BR><font color = \'darkred\' style = \'italic\'>Too many groups.<BR>Please enter a specific group name in the text box.</font>';
		avail_group_visible = 'visible';
		group_dropdown_style = 'hidden';

	else:
		count_grp = 2;

		ads_groups_only_string = '';
		group_message = '';
		avail_group_visible = 'hidden';
		group_dropdown_style = 'visible';
				
	print """			<div align = 'center' width = '100%'>
				<table width = '100%'>
						<tr>
							<td>
							</td>
							<td>
								<div width = '100%' id = 'ftp_users_list' style = 'display:  """ + ftp_users_table_style + """;' align = 'center'>
								<table width = '100%'>
									<tr>
										<td colspan = '2'>
											<B>Users list:</B>""" + user_message + """<BR>
										</td>
									</tr>
									<tr>
										<td>
											<B>Available:</B>
										</td>
										<td>
											<B>Authorized:</B>
										</td>
									</tr>
									<tr>
										<td>"""
								
	# if the users count is more than 1000, then a text box is displayed in the place of a dropdown.
	# as the user types the user name, a list of users will be displayed starting with the characters he entered
	if (len(ftp_all_users_array) > 1000):
		print """<input id = 'ftp_available' name = 'ftp_ads_user_text' type="text" class = 'input' value = '' oninput = 'generate_user_list(document.getElementById("ftp_available"), document.getElementById("ftp_autosuggest"), "%s", "users", "set_ftp_params");' onclick = 'document.getElementById("ftp_autosuggest").style.display = "none";'> <input class = 'input1' type = 'button' name = '' value = '>' onclick = "ftp_move_text_to_dropdown(this.form.ftp_available, this.form.ftp_granted, '1');"  %s %s>""" % (ads_users_only_string, share_smb_settings.smbdisabled, share_details.alldisabled);

		print """<select class = 'input' style = 'width: 250px; height: 350px; display: none;' id = 'ftp_autosuggest' name = 'avail_users' multiple onclick = 'return set_user(this.form.ftp_available, this.form.ftp_autosuggest, this.form.ftp_autosuggest.value);' """ + share_smb_settings.smbdisabled + """ """ + share_details.alldisabled + """>"""
											
		print ftp_users_list 
									
		print """									</select>"""
								

	else:
		print """<select class = 'input' style = 'width: 200px; height: 150px;' id = 'ftp_available' name = 'avail_users' multiple onclick = "return ftp_move_users(this.form.ftp_available, this.form.ftp_granted, '1');"  """ + share_smb_settings.smbdisabled + """ """ + share_details.alldisabled + """>"""
											
		users_only = '';

		for users in ftp_all_users_array:
			if (share_details.connstatus == 'Join is OK'):
				# when in ads connection, the users are displayed in '<WORKGROUP>+<username>' format
				if (users.find('+') > 0):
					separator = '+';
					users_only = users[users.find('+') + 1:];

				if (users.find('\\') > 0):
					separator = '\\';
					users_only = users[users.find('\\') + 1:];

			if (share_details.connstatus == 'nis is running'):
				users_only = users;

			if (share_details.connstatus == 'local connection'):
				users_only = users;

			print """<option value = '""" + users + """' title = '""" + users + """'>""" + users_only + """</option>"""
		print """</select>"""
									
	print """									</td>
										<td>
											<select class = 'input' style = 'width: 200px; height: 150px;' id = 'ftp_granted' name = 'grant_users[]' multiple onclick = "return ftp_move_users(this.form.ftp_granted, this.form.ftp_available, '%s');" %s %s>""" % (count_usr, share_smb_settings.smbdisabled, share_details.alldisabled);

	if (ftp_users_list != ' '):
		for n in ftp_users_list:
			if (n.find('+') > 0):
				n1 = n[n.find('+') + 1:];

			else:
				n1 = n[n.find('\\') + 1:];

			print """<option value = '"""+n+"""' selected>"""+n1+"""</option>""" 
											
	print """</select>
								</td>
									</tr>
						<tr>
						<td colspan = '2'>
							<BR><B>Groups list:</B>""" + group_message + """<BR>
						</td>
					</tr>
					<tr>
						<td>
							<B>Available:</B>
						</td>
						<td>
							<B>Authorized:</B>
						</td>
					</tr>
					<tr>
						<td>"""
					
	# if the groups count is more than 1000, then a text box is displayed in the place of a dropdown.
	# as the user types the group name, a list of groups will be displayed starting with the characters he entered
	if (len(ftp_all_groups_array) > 1000):
		print """<input id = 'ftp_available_groups' name = 'ftp_ads_group_text' type="text" class = 'input' value = '' oninput = 'generate_user_list(document.getElementById("ftp_available_groups"), document.getElementById("ftp_g_autosuggest"), "%s", "groups", "set_ftp_params");' onclick = 'document.getElementById("ftp_g_autosuggest").style.display = "none";'> <input class = 'input1' type = 'button' name = '' value = '>' onclick = "ftp_move_group_to_dropdown(this.form.ftp_available_groups, this.form.ftp_granted_groups, '1');" %s %s>""" % (ads_groups_only_string, share_smb_settings.smbdisabled, share_details.alldisabled);
		print """<select class = 'input' style = 'width: 250px; height: 350px; display: none;' id = 'ftp_g_autosuggest' name = 'avail_groups' multiple onclick = 'return set_user(this.form.ftp_available_groups, this.form.ftp_g_autosuggest, this.form.ftp_g_autosuggest.value);'  """ + share_smb_settings.smbdisabled + """ """ + share_details.alldisabled + """>"""
		print ftp_groups_list 
		print """</select>"""
						
	else:
		print """<select class = 'input' style = 'width: 200px; height: 150px;' id = 'ftp_available_groups' name = 'avail_groups' multiple onclick = "return ftp_move_groups(this.form.ftp_available_groups, this.form.ftp_granted_groups, '1');" """ +  share_smb_settings.smbdisabled + """ """ + share_details.alldisabled + """>"""
		groups_only = '';

		for groups in ftp_all_groups_array:
			if (share_details.connstatus == 'Join is OK'):
				# when in ads connection, the groups are displayed in '<WORKGROUP>+<groupname>' format
				if (groups.find('+') > 0):
					groups_only = groups[groups.find('+') + 1:];

				if (groups.find('\\') > 0):
					groups_only = groups[groups.find('\\') + 1:];

			if (share_details.connstatus == 'nis is running'):
				groups_only = groups;

			if (share_details.connstatus == 'local connection'):
				groups_only = groups;

			ftp_groups_to_check = '@' + groups;

			print """<option value = '""" + groups + """' title = '""" + groups + """'>""" + groups_only + """</option>"""
									
		print """</select>"""
					
					
	print """					</td>
						<td>
							<select class = 'input' style = 'width: 200px; height: 150px;' id = 'ftp_granted_groups' name = 'grant_groups[]' multiple onclick = "return ftp_move_groups(this.form.ftp_granted_groups, this.form.ftp_available_groups, '%s');" %s %s>""" % (count_grp, share_smb_settings.smbdisabled, share_details.alldisabled)

	if (ftp_groups_list != ' '):
		for n in ftp_groups_list:
			if (n.find('+') > 0):
				n1 = n[n.find('+') + 1:];

			else:
				n1 = n[n.find('\\') + 1:];

			print """<option value = '"""+n+"""' selected>"""+n1+"""</option>"""
							
	print """						</select>
						</td>
					</tr>
				</table>
				</div>
				</td>
				</tr>
				</table>
				</div><BR>
				<table width = '100%' align = 'center'>
					<tr align = 'right'>
						<td>"""
	print common_methods.share_ftp_wait;
	print """					</td>
						<td align = 'right'>
							 <!--<input class = 'input1' type = 'button' name = 'ftp_button' value = 'Apply' onclick = 'return validate_ftp_parameters();' """ + share_smb_settings.smbdisabled + """>-->

<!--<input class = 'input1' type = 'submit' name = 'ftp_button' onclick ="return ftp_update_validation();" value = 'Apply' """ + share_details.alldisabled + """>-->
        <span style="margin-left: 54%;" ><span id="button-one"><button type = 'submit' name="ftp_button" value="Apply" onclick ="return ftp_update_validation();" """ + share_details.alldisabled +""" style = 'width:65px; background-color:#E8E8E8; border:none; float: right;font-size: 86%; ' title="Apply"><a style="font-size:85%;">Apply</a></button></span></span>


							<input type = 'hidden' name = 'proceed_page' value = 'proceed'>
							<input type = 'hidden' name = 'hid_share' value = '"""+share_1+"""'>
							<input type = 'hidden' name = 'hid_path' value = '"""+path_1+"""'>
							<input type = 'hidden' name = 'hid_comment' value = 'comment_1'>
							<input type = 'hidden' name = 'hid_ads_users' value = '""" + ads_users_only_string + """'>
							<input type = 'hidden' name = 'hid_ads_groups' value = '""" + ads_groups_only_string + """'>
							<input type = 'hidden' name = 'hidadsusers' value = '""" + ads_users_string + """'>
							<input type = 'hidden' name = 'hidadsgroups' value = '""" + ads_groups_string + """'>
							<input type = 'hidden' name = 'hid_ftp_assigned_users' value = '"""+str(ftp_assigned_users_string)+"""'>
							<input type = 'hidden' name = 'hid_ftp_assigned_groups' value = '"""+str(ftp_assigned_groups_string)+"""'>
							<input type = 'hidden' name = 'hid_ftp_domain' value = '"""+ads_domain_for_ftp+"""'>
						</td>
					</tr>
				</form>
				</table>
				</td>
				</tr>
				</table><BR>
				</td></tr></table>
	""" 
#% (share_1, path_1, ftp_assigned_users_string, ftp_assigned_groups_string, ads_domain_for_ftp);

except Exception as e:
	disp_except.display_exception(e);
