#!/usr/bin/python
import cgitb, cgi, commands, common_methods, sys, include_files

sys.path.append('../modules/');
import disp_except;

logarray  = [];
logfile   = common_methods.log_file;
logstring = '';

cgitb.enable();

form = cgi.FieldStorage();
stat = '';

try:
	# set the executable path to python modules in nasexe
	sys.path.append('/var/nasexe/python');
	import quota;

	connection = common_methods.conn_status();

	session_user = common_methods.get_session_user();

	if (session_user != ''):
		# get the users and groups list into an array
		users_array  = [];
		groups_array = [];

		user_string = ''
		group_string = '';

		users_array  = form.getvalue('grant_users[]');
		groups_array = form.getvalue('grant_groups[]');
		domainname   = form.getvalue('domainslist');

		"""
		if (user_string.strip() != ''):
			user_string = user_string.replace('<PLUS>', '+');

		if (group_string.strip() != ''):
			group_string = group_string.replace('<PLUS>', '+');

		# split user_string into users_array
		if (user_string != ''):
			users_array  = user_string.split('$$');

		# split group_string into groups_array
		if (group_string != ''):
			groups_array = group_string.split('$$');
		"""

		# get the disk list and the disk size
		disk   = form.getvalue('disk_list');
		size   = form.getvalue('disk_size');

		m_size = int(size) * 1024;

		quota_size = str(m_size) + 'M';

		status_string = '';

		# if option selected is user, then pass users list as parameter
		if (str(type(users_array)) == "<type 'list'>"):
			if (len(users_array) > 0):
				# prepare user list for the parameter to the bash script
				user_group = 'user';
				username   = 'usrname';
				
				new_usr_array = []
				for user_param in users_array:
					user_param = user_param.strip();

					if (user_param != ''):
						user_param = user_param.replace('[AND]', '&');
						user_param = user_param.replace('[HASH]', '#');
						user_param = user_param.replace('[DOLLAR]', '$');
						user_param = user_param.replace("[SQUOTE]", "'");
						user_param = user_param.replace("[DOT]", ".");
						if (connection == 'Join is OK'):
							#user_param = user_param.replace('[AND]', '&');
							#user_param = user_param.replace('[HASH]', '#');
							#user_param = user_param.replace('[DOLLAR]', '$');
							#user_param = user_param.replace("[SQUOTE]", "'");
							#user_param = user_param.replace("[DOT]", ".");

							user_param_un = user_param
							#user_param_raw = user_param_un.encode('string-escape')
							user_param_raw = repr(user_param_un)[1:-1]
							new_usr_array.append(user_param_raw)

							userparamline = commands.getstatusoutput('wbinfo --user-info="' + user_param + '"');

							if (userparamline[0] == 0):
								user_param_line = userparamline[1].strip();
								
								temp = [];
								temp = user_param_line.split(':');

								user_param_text = temp[0];
								user_param      = temp[2];

							else:
								logstring = str(common_methods.now) + '<<>>Script: add_user_quota.py, wbinfo --user-info<<>>' + userparamline[1];
								logarray.append(logstring);
						else:
							user_param_un = user_param
							user_param_raw = repr(user_param_un)[1:-1]
							new_usr_array.append(user_param_raw)
						
						#print user_group
						#print exit()
						#status = quota.add(user_group, quota_size, usrname=user_param);
						

						#if (status['id'] == 0):
						#	status_string += 'Quota allocated to users [' + user_param + ']\\n';

						#else:
						#	common_methods.sendtologs('ERROR', 'Add User Quota', 'UI', '"add_user_quota.py" ' + str(status));

				status = quota.add(user_group, quota_size, usrname=new_usr_array)
				if (status['id'] == 0):
					status_string += 'Quota allocated to users [' + str(new_usr_array) + ']\\n';
				else:
					common_methods.sendtologs('ERROR', 'Add User Quota', 'UI', '"add_user_quota.py" ' + str(status));


				if (status_string != ''):
					status_string = status_string.strip();

				if (status_string != ''):
					stat = 'y';

				else:
					stat = 'n';

		else:
			if (users_array != None):
				user_param = str(users_array);

				user_group = 'user';
				username   = 'usrname';

				user_param = user_param.replace('[AND]', '&');
				user_param = user_param.replace('[HASH]', '#');
				user_param = user_param.replace('[DOLLAR]', '$');
				user_param = user_param.replace("[SQUOTE]", "'");
				user_param = user_param.replace("[DOT]", ".");
				if (connection == 'Join is OK'):
					#user_param = user_param.replace('[AND]', '&');
					#user_param = user_param.replace('[HASH]', '#');
					#user_param = user_param.replace('[DOLLAR]', '$');
					#user_param = user_param.replace("[SQUOTE]", "'");
					#user_param = user_param.replace("[DOT]", ".");

					user_param_un = user_param

                                        userparamline = commands.getstatusoutput('wbinfo --user-info="' + user_param + '"');

                                        if (userparamline[0] == 0):
	                                        user_param_line = userparamline[1].strip()
                                                temp = [];
                                                temp = user_param_line.split(':');

                                                user_param_text = temp[0];
                                                user_param      = temp[2];

                                        else:
                                        	logstring = str(common_methods.now) + '<<>>Script: add_user_quota.py, wbinfo --user-info<<>>' + userparamline[1];
                                                logarray.append(logstring);
				else:
					user_param_un = user_param

				#user_param_raw = user_param_un.encode('string-escape')
				#print user_param_un
				user_param_raw = repr(user_param_un)[1:-1]
				user_param_list = [user_param_raw]
				#print "<br/>"
				#print user_param_list
				#print "<br/>"
				#print exit()
                                #status = quota.add(user_group, quota_size, usrname=user_param);
                                status = quota.add(user_group, quota_size, usrname=user_param_list);

                                if (status['id'] == 0):
                                	status_string += 'Quota allocated to users [' + str(user_param_list) + ']\\n';

                                else:
                                	common_methods.sendtologs('ERROR', 'Add User Quota', 'UI', '"add_user_quota.py" ' + str(status));

                                if (status_string != ''):
                                        status_string = status_string.strip();

				if (status_string != ''):
					stat = 'y';

				else:
					stat = 'n';

		# if option selected is group, then group list is passed as parameter
		if (str(type(groups_array)) == "<type 'list'>"):
			if (len(groups_array) > 0):
				# prepare the group list for the parameter to the bash script
				user_group = 'group';
				username   = 'grpname';
				
				new_grp_array = []
				#print groups_array
				for userparam in groups_array:
					if (userparam != ''):
						userparam = userparam.strip();

						userparam = userparam.replace('[AND]', '&');
						userparam = userparam.replace('[HASH]', '#');
						userparam = userparam.replace('[DOLLAR]', '$');
						userparam = userparam.replace("[SQUOTE]", "'");
						userparam = userparam.replace("[DOT]", ".");
						if (connection == 'Join is OK'):
							#userparam = userparam.replace('[AND]', '&');
							#userparam = userparam.replace('[HASH]', '#');
							#userparam = userparam.replace('[DOLLAR]', '$');
							#userparam = userparam.replace("[SQUOTE]", "'");
							#userparam = userparam.replace("[DOT]", ".");

							user_param_un = userparam
                                                        #user_param_raw = user_param_un.encode('string-escape')
							user_param_raw = repr(user_param_un)[1:-1]
                                                        new_grp_array.append(user_param_raw)

							userparamline = commands.getstatusoutput('wbinfo --group-info="' + userparam + '"');

							if (userparamline[0] == 0):
								user_param_line = userparamline[1].strip();
								
								temp = [];
								temp = user_param_line.split(':');

								user_param_text = temp[0];
								userparam      = temp[2];

							else:
								logstring = str(common_methods.now) + '<<>>Script: add_user_quota.py, wbinfo --group-info<<>>' + userparamline[1];
								logarray.append(logstring);
						else:
							user_param_un = userparam
							user_param_raw = repr(user_param_un)[1:-1]
							new_grp_array.append(user_param_raw)

						#status = quota.add(user_group, quota_size, grpname=userparam);

						#if (status['id'] == 0):
						#	status_string += 'Quota allocated to groups [' + userparam + ']\\n';

						#else:
						#	common_methods.sendtologs('ERROR', 'Add Group Quota', 'UI', '"add_user_quota.py" ' + str(status));
				#print new_grp_array
				status = quota.add(user_group, quota_size, grpname=new_grp_array);
				if (status['id'] == 0):
					status_string += 'Quota allocated to groups [' + str(new_grp_array) + ']\\n';

				else:
					common_methods.sendtologs('ERROR', 'Add Group Quota', 'UI', '"add_user_quota.py" ' + str(status));

				if (status_string != ''):
					status_string = status_string.strip();

				if (status_string != ''):
					stat = 'y';

				else:
					stat = 'n';

		else:
			if (str(groups_array) != None):
				# prepare the group list for the parameter to the bash script
				user_group = 'group';
				username   = 'grpname';

				userparam = str(groups_array);

				if (userparam != ''):
					userparam = userparam.strip();

					userparam = userparam.replace('[AND]', '&');
					userparam = userparam.replace('[HASH]', '#');
					userparam = userparam.replace('[DOLLAR]', '$');
					userparam = userparam.replace("[SQUOTE]", "'");
					userparam = userparam.replace("[DOT]", ".");
					if (connection == 'Join is OK'):
						#userparam = userparam.replace('[AND]', '&');
						#userparam = userparam.replace('[HASH]', '#');
						#userparam = userparam.replace('[DOLLAR]', '$');
						#userparam = userparam.replace("[SQUOTE]", "'");
						#userparam = userparam.replace("[DOT]", ".");

						user_param_un = userparam

						userparamline = commands.getstatusoutput('wbinfo --group-info="' + userparam + '"');

						if (userparamline[0] == 0):
							user_param_line = userparamline[1].strip();
								
							temp = [];
							temp = user_param_line.split(':');

							user_param_text = temp[0];
							userparam      = temp[2];

						else:
							logstring = str(common_methods.now) + '<<>>Script: add_user_quota.py, wbinfo --group-info<<>>' + userparamline[1];
							logarray.append(logstring);
					else:
						user_param_un = userparam

					#print user_param_un
					#print "<br/>"

					#user_param_raw = user_param_un.encode('string-escape')
					user_param_raw = repr(user_param_un)[1:-1]
	                                user_param_list = [user_param_raw]

					#print user_group
					#print "<br/>"
					#print quota_size
					#print "<br/>"
					#print user_param_list
					#print "<br/>"
					status = quota.add(user_group, quota_size, grpname=user_param_list);
					#print status

					if (status['id'] == 0):
						status_string += 'Quota allocated to groups [' + userparam + ']\\n';

					else:
						common_methods.sendtologs('ERROR', 'Add Group Quota', 'UI', '"add_user_quota.py" ' + str(status));

					if (status_string != ''):
						status_string = status_string.strip();

					if (status_string != ''):
						stat = 'y';

					else:
						stat = 'n';

		print "<script>location.href = 'iframe_user_quota.py?dom=%s&st=%s';</script>" % (domainname, stat);

	else:
		common_methods.relogin();

except Exception as e:
	disp_except.display_exception(e);
