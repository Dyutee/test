#!/usr/bin/python
import cgitb, cgi, common_methods, commands, sys, include_files

sys.path.append('../modules/');
import disp_except;

sys.path.append('/var/nasexe/python/');
import quota, tools;

try:
	cgitb.enable();

	form = cgi.FieldStorage();
	
	#all_users_list  = common_methods.get_users_string();
	#all_groups_list = common_methods.get_groups_string();
	get_all_users = tools.get_local_users()
	get_all_groups = tools.get_local_groups()
	all_users_list = get_all_users
	all_groups_list = get_all_groups

	local_users_array  = [];
	local_groups_array = [];

	if (all_users_list['id'] == 0):
		if (all_users_list['users'] != ''):
			local_users_array  = all_users_list['users'];

	# if groupslist id not empty
	if (all_groups_list['id'] == 0):
		if (all_groups_list['groups'] != ''):
			local_groups_array = all_groups_list['groups'];
                
	session_user = common_methods.get_session_user();

	tmpfile = '/tmp/tmpquotafile';
	connection = common_methods.conn_status();

	if (session_user != ''):
		user_option = form.getvalue('search_user');

		user_text  = '';
		group_text = '';

		# get the user/group from the search form
		user      = form.getvalue('user_list');
		group     = form.getvalue('group_list');
		action    = form.getvalue('delete_search');
		usertext  = form.getvalue('ugtext');
		usergroup = form.getvalue('usergroup');

		if (user != None):
			user  = user.replace('<PLUS>', '+');

			if (user.find('\\') > 0):
				user = user.replace('\\', '\\\\');

		if (group != None):
			group = group.replace('<PLUS>', '+');

			if (group.find('\\') > 0):
				group = group.replace('\\', '\\\\');

		quota_dict = {};
		quota_array  = [];
		params_array = [];

		if (action == 'Show Details'):
			if (user_option == 'all'):
				user_param = '';
				user_group = 'all';

				quota_array = [];
				

				for users in local_users_array:
					if (connection == 'Join is OK'):
						useridcommand = commands.getstatusoutput('wbinfo --user-info="' + users + '"');
						
						if (useridcommand[0] == 0):
							useridline = useridcommand[1];

							temp = [];
							temp = useridline.split(':');

							i = temp[2];

					else:
						i = users;

					quota_user_dict = quota.show('user', usrname=i);

					if (quota_user_dict['id'] == 0):
						quota_array = quota_user_dict['quota'];

					if (len(quota_array) > 0):
						quota_string = '';

						for squota in quota_array:
							if (squota['limit'] != '0'):
								disk_name = squota['disk_name'];
								disk_name = disk_name[disk_name.rfind('/') + 1:];
		
								quota_string += disk_name + ':';

						quota_string = quota_string[:quota_string.rfind(':')];
	
						quota_string = i + '[U]:::' + quota_string + ':::' + squota['limit'] + ':::' + squota['used_space'];
						quota_string = quota_string.strip();

						if (quota_string.find(':::0:::') < 0):
							params_array.append(quota_string);
				
				for groups in local_groups_array:
					if (connection == 'Join is OK'):
						groupsidcommand = commands.getstatusoutput('wbinfo --group-info="' + groups + '"');

						if (groupsidcommand[0] == 0):
							groupsidline = groupsidcommand[1];

							temp = [];
							temp = groupsidline.split(':');

							i = temp[2];

					else:
						i = groups;

					quota_group_dict = quota.show('group', grpname=i);
					#print quota_group_dict
					#print exit()

					if (quota_group_dict['id'] == 0):
						quota_array = quota_group_dict['quota'];

					if (len(quota_array) > 0):
						quota_string = '';

						for squota in quota_array:
							if (squota['limit'] != '0'):
								disk_name = squota['disk_name'];
								disk_name = disk_name[disk_name.rfind('/') + 1:];
								quota_string += disk_name + ':';

						quota_string = quota_string[:quota_string.rfind(':')];
	
						quota_string = i + '[G]:::' + quota_string + ':::' + squota['limit'] + ':::' + squota['used_space'];
						quota_string = quota_string.strip();

						if (quota_string.find(':::0:::') < 0):
							params_array.append(quota_string);

			elif (user_option == 'user'):
				user_group = 'user';
				user_param = user;
				user_text  = 'user';
				prefix     = '';

				if (connection == 'Join is OK'):
					checkuserline = commands.getstatusoutput('wbinfo -u |head -1');

					if (checkuserline[0] == 0):
						culine = checkuserline[1];

						if (culine.find('\\') > 0):
							prefix = culine[:culine.find('\\') + 1];

						else:
							prefix = culine[:culine.find('+') + 1];

					fulluser = prefix + user_param;

					useridcommand = commands.getstatusoutput('wbinfo --user-info="' + fulluser + '"');
			
					if (useridcommand[0] == 0):
						useridline = useridcommand[1];

						temp = [];
						temp = useridline.split(':');

						user_text  = temp[0];
						user_param = temp[2];

				#quota_dict = quota.show(user_group, usrname=user_param);
				#params_array.append(str(quota_dict));

			elif (user_option == 'group'):
				user_group = 'group';
				user_param = group;
				user_text  = 'group';
				prefix     = '';

				if (connection == 'Join is OK'):
					checkuserline = commands.getstatusoutput('wbinfo -g |head -1');

					if (checkuserline[0] == 0):
						culine = checkuserline[1];

						if (culine.find('\\') > 0):
							prefix = culine[:culine.find('\\') + 1];

						else:
							prefix = culine[:culine.find('+') + 1];

					fulluser = prefix + user_param;

					useridcommand = commands.getstatusoutput('wbinfo --group-info="' + fulluser + '"');

					string = 'wbinfo --group-info="' + fulluser + '"';
					
					if (useridcommand[0] == 0):
						useridline = useridcommand[1];

						temp = [];
						temp = useridline.split(':');

						user_text  = temp[0];
						user_param = temp[2];

				#quota_dict = quota.show(user_group, grpname=user_param);
				#params_array.append(str(quota_dict));

			if (user_text.find('\\') > 0):
				user_text = user_text[user_text.find('\\') + 1:];

			elif (user_text.find('+') > 0):
				user_text = user_text[user_text.find('+') + 1:];
					
			commands.getoutput('sudo rm -rf /tmp/tmpquotafile');
			common_methods.write_file(tmpfile, params_array);

			#print params_array
			#print exit()

			print "<script>location.href = 'iframe_user_quota.py?spain=yes&ug=%s&up=%s#tabs-2';</script>" % (user_group, user_param);
		
		elif (action == 'Delete Quota'):
			statusstring = '';

			user_text_to_del = usertext;
			user_parm_to_del = usergroup

			user_to_del_un = user_parm_to_del

			if (user_text_to_del == 'all'):
				del_users_array = [];
				user_parm_to_del = '';
				users_check_array = form.getvalue('delete_option[]');

				if (str(type(users_check_array)) == "<type 'list'>"):
					for users_check in users_check_array:
						del_users_array.append(users_check);

				else:
					del_users_array.append(users_check_array);

				for lusers in del_users_array:
					if (lusers.strip() != ''):
						if (connection == 'Join is OK'):
							if (lusers.find('[U]') > 0):
								lusers1 = lusers;
								lusers1 = lusers1.replace('[U]', '');
								lusers1 = lusers1.strip();
								usersidcommand = commands.getstatusoutput('wbinfo --user-info="' + lusers1 + '"');

								if (usersidcommand[0] == 0):
									usersidline = usersidcommand[1];

									temp = [];
									temp = usersidline.split(':');

									lu = temp[2];

								status = quota.dele('user', usrname=lu);

								if (status['id'] != 0):
									statusstring += status['desc'] + "\\n";
									common_methods.sendtologs('ERROR', 'Revoke users from quota', 'UI', '"search_user_quota.py" ' + str(statusstring));

								else:
									statusstring += lu + " - Quota Deleted!\\n";

							elif (lusers.find('[G]') > 0):
								lusers1 = lusers;
								lusers1 = lusers1.replace('[G]', '');
								lusers1 = lusers1.strip();
								groupidcommand = commands.getstatusoutput('wbinfo --group-info="' + lusers1 + '"');

								if (groupidcommand[0] == 0):
									groupidline = groupidcommand[1];

									temp = [];
									temp = groupidline.split(':');

									lg = temp[2];

								status = quota.dele('group', grpname=lg);

								if (status['id'] != 0):
									statusstring += status['desc'] + "\\n";
									common_methods.sendtologs('ERROR', 'Revoke groups from quota', 'UI', '"search_user_quota.py" ' + str(statusstring));

								else:
									statusstring += lu + " - Quota Deleted!\\n";

						else:
							if (lusers.find('[U]') > 0):
								lu = lusers.replace('[U]', '');
								lu = lu.strip();
								lu_list = [lu]

								status = quota.dele('user', usrname=lu_list);

								if (status['id'] != 0):
									statusstring += status['desc'] + "\\n";
									common_methods.sendtologs('ERROR', 'Revoke users from quota', 'UI', '"search_user_quota.py" ' + str(statusstring));

								else:
									statusstring += lu + " - Quota Deleted!\\n";

							elif (lusers.find('[G]') > 0):
								lg = lusers.replace('[G]', '');
								lg = lg.strip();
								lg_list = [lg]

								status = quota.dele('group', grpname=lg_list);

								if (status['id'] != 0):
									statusstring += status['desc'] + "\\n";
									common_methods.sendtologs('ERROR', 'Revoke groups from quota', 'UI', '"search_user_quota.py" ' + str(statusstring));

								else:
									statusstring += lg + " - Quota Deleted!\\n";

				if (statusstring.strip() != ''):
					statusstring  = statusstring.strip();

					common_methods.alert(statusstring);

				for users in local_users_array:
					if (connection == 'Join is OK'):
						useridcommand = commands.getstatusoutput('wbinfo --user-info="' + users + '"');
						
						if (useridcommand[0] == 0):
							useridline = useridcommand[1];

							temp = [];
							temp = useridline.split(':');

							i = temp[2];

					else:
						i = users;

					quota_user_dict = quota.show('user', usrname=i);

					if (quota_user_dict['id'] == 0):
						quota_array = quota_user_dict['quota'];

					if (len(quota_array) > 0):
						quota_string = '';

						for squota in quota_array:
							if (squota['limit'] != '0'):
								disk_name = squota['disk_name'];
								disk_name = disk_name[disk_name.rfind('/') + 1:];
		
								quota_string += disk_name + ':';

						quota_string = quota_string[:quota_string.rfind(':')];
	
						quota_string = i + '[U]:::' + quota_string + ':::' + squota['limit'] + ':::' + squota['used_space'];
						quota_string = quota_string.strip();

						if (quota_string.find(':::0:::') < 0):
							params_array.append(quota_string);
				
				for groups in local_groups_array:
					if (connection == 'Join is OK'):
						groupsidcommand = commands.getstatusoutput('wbinfo --group-info="' + groups + '"');

						if (groupsidcommand[0] == 0):
							groupsidline = groupsidcommand[1];

							temp = [];
							temp = groupsidline.split(':');

							i = temp[2];

					else:
						i = groups;

					quota_group_dict = quota.show('group', grpname=i);
					#print quota_group_dict
					#print exit()

					if (quota_group_dict['id'] == 0):
						quota_array = quota_group_dict['quota'];

					if (len(quota_array) > 0):
						quota_string = '';

						for squota in quota_array:
							if (squota['limit'] != '0'):
								disk_name = squota['disk_name'];
								disk_name = disk_name[disk_name.rfind('/') + 1:];
								quota_string += disk_name + ':';

						quota_string = quota_string[:quota_string.rfind(':')];
	
						quota_string = i + '[G]:::' + quota_string + ':::' + squota['limit'] + ':::' + squota['used_space'];
						quota_string = quota_string.strip();

						if (quota_string.find(':::0:::') < 0):
							params_array.append(quota_string);

				common_methods.write_file(tmpfile, params_array);

				print "<script>location.href = 'iframe_user_quota.py?spain=yes&ug=all&up=#tabs-2';</script>";

			else:
				if (user_text_to_del == 'user'):
					if (connection == 'Join is OK'):
						user = commands.getoutput('wbinfo -u|head -1');

						if (user != ''):
							if (user.find('\\') > 0):
								prefix = user[:user.find('\\') + 1];

							else:
								prefix = user[:user.find('+') + 1];

							#user_parm_to_del = prefix + user_parm_to_del;

						usersidcommand = commands.getstatusoutput('wbinfo --user-info="' + user_parm_to_del + '"');

						if (usersidcommand[0] == 0):
							usersidline = usersidcommand[1];

							temp = [];
							temp = usersidline.split(':');

							user_parm_to_del = temp[2];
					user_to_del_un = repr(user_to_del_un)[1:-1]
					user_to_del_un = user_to_del_un.replace("\\\\","\\")
					user_to_del_un = [user_to_del_un]
					#status = quota.dele('user', usrname=user_parm_to_del)
					status = quota.dele('user', usrname=user_to_del_un)
					#print status
					#exit()

				if (user_text_to_del == 'group'):
					if (connection == 'Join is OK'):
						group = commands.getoutput('wbinfo -g|head -1');

						if (group != ''):
							if (group.find('\\') > 0):
								prefix = group[:group.find('\\') + 1];

							else:
								prefix = group[:group.find('+') + 1];

							#user_parm_to_del = prefix + user_parm_to_del;

						groupsidcommand = commands.getstatusoutput('wbinfo --group-info="' + user_parm_to_del + '"');

						if (groupsidcommand[0] == 0):
							groupsidline = groupsidcommand[1];

							temp = [];
							temp = groupsidline.split(':');

							user_parm_to_del = temp[2];
					
					user_to_del_un = repr(user_to_del_un)[1:-1]
					user_to_del_un = user_to_del_un.replace("\\\\","\\")
                                        user_to_del_un = [user_to_del_un]

					#status = quota.dele('group', grpname=user_parm_to_del);
					status = quota.dele('group', grpname=user_to_del_un);

				if (user_text_to_del == 'user' or user_text_to_del == 'group' or user_text_to_del == 'all'):
					if (status['id'] == 0):
						print "<script>alert('Quota deleted!');</script>";

					else:
						print '<script>alert("%s");</script>' % status['desc'];

				print "<script>location.href = 'iframe_user_quota.py#tabs-2';</script>";

	else:
		common_methods.relogin();

except Exception as e:
	disp_except.display_exception(e);
