#!/usr/bin/python
import cgitb, cgi, common_methods, commands, sys;

sys.path.append('/var/nasexe/python/');
from fs2global import *;

sys.path.append('../modules/');
import disp_except;

cgitb.enable();
form = cgi.FieldStorage();

try:
	log_array = [];
	log_file = common_methods.log_file;

	log_string = '';

	# get session user from get_session_user() method in common_methods.py
	session_user = common_methods.get_session_user();

	restrict_status_command = '';

	if (session_user != ''):
		# get all the checked owner permission values
		owner_read    = form.getvalue('o_read_perm', 0);
		owner_write   = form.getvalue('o_write_perm', 0);
		owner_execute = form.getvalue('o_exec_perm', 0);

		# get all the checked group permission values
		group_read    = form.getvalue('g_read_perm', 0);
		group_write   = form.getvalue('g_write_perm', 0);
		group_execute = form.getvalue('g_exec_perm', 0);

		# get all the checked other permission values
		other_read    = form.getvalue('oth_read_perm', 0);
		other_write   = form.getvalue('oth_write_perm', 0);
		other_execute = form.getvalue('oth_exec_perm', 0);

		permission_for_path = form.getvalue('hid_path');
		share_name          = form.getvalue('hid_share');
		restrict            = form.getvalue('restrict', 'off');
		inherit             = form.getvalue('inherit', 'off');

		purpose = form.getvalue('purpose');

		permission_for_path = '/storage/' + permission_for_path;

		params_array = [];

		# construct a permission string to write to global file. the parameters restrict and inherit are retreived from this file
		permission_string = share_name + ':' + restrict + ':' + inherit;

		params_array.append(permission_string);

		delete_entry_command = 'sudo /var/nasexe/delete_entry "' + share_name + ':" share_perms_global_file /var/www/global_files';
		commands.getoutput(delete_entry_command);

		common_methods.append_file(common_methods.share_perms_global_file, params_array);
		params_array = [];

		# convert the permissions from symbolic mode (-rwxrwxrwx) to absolute mode (777)
		owner_permission = int(owner_read) + int(owner_write) + int(owner_execute);
		group_permission = int(group_read) + int(group_write) + int(group_execute);
		other_permission = int(other_read) + int(other_write) + int(other_execute);

		file_afp_perms = 'file perm=0' + str(owner_permission) + str(group_permission) + str(other_permission);
		dirs_afp_perms = 'directory perm=0' + str(owner_permission) + str(group_permission) + str(other_permission);

		filepermstosmb = 'create mask=0' + str(owner_permission) + str(group_permission) + str(other_permission);
		dirspermstosmb = 'directory mask=0' + str(owner_permission) + str(group_permission) + str(other_permission);

		filetochange = afp_share_conf_dir + share_name;
		checkafpfile = commands.getstatusoutput('ls %s' % filetochange);

		smbfiletochange = smb_share_conf_dir + share_name;
		checksmbfile = commands.getstatusoutput('ls %s' % smbfiletochange);

		existing_file_perms = '';
		existing_dir_perms  = '';

		smb_file_perms = '';
		smb_dirs_perms = '';
	
		if (purpose == 'afponly'):
			if (checkafpfile[0] == 0):
				filetoread = open(filetochange, 'r');

				for line in filetoread:
					if (line.find('file perm=') >= 0):
						existing_file_perms = line.strip();

				common_methods.replace(filetochange, existing_file_perms, file_afp_perms);

				if (inherit == 'true'):
					filetoread = open(filetochange, 'r');

					for line in filetoread:
						if (line.find('directory perm=') >= 0):
							existing_dir_perms = line.strip();

					common_methods.replace(filetochange, existing_dir_perms, dirs_afp_perms);

		if (purpose == 'smbonly'):
			if (checksmbfile[0] == 0):
				smbfiletoread = open(smbfiletochange, 'r');

				for line in smbfiletoread:
					if (line.find('create mask=') >= 0):
						smb_file_perms = line.strip();

				common_methods.replace(smbfiletochange, smb_file_perms, filepermstosmb);

				if (inherit == 'true'):
					smbfiletoread = open(smbfiletochange, 'r');

					for line in smbfiletoread:
						if (line.find('directory mask=') >= 0):
							smb_dirs_perms = line.strip();

					common_methods.replace(smbfiletochange, smb_dirs_perms, dirspermstosmb);

		if (purpose == 'all'):
			if (checkafpfile[0] == 0):
				filetoread = open(filetochange, 'r');

				for line in filetoread:
					
					if (line.find('file perm=') >= 0):
						existing_file_perms = line.strip();

				common_methods.replace(filetochange, existing_file_perms, file_afp_perms);

				if (inherit == 'true'):
					filetoread = open(filetochange, 'r');

					for line in filetoread:
						if (line.find('directory perm=') >= 0):
							existing_dir_perms = line.strip();

					common_methods.replace(filetochange, existing_dir_perms, dirs_afp_perms);

			if (checksmbfile[0] == 0):
				smbfiletoread = open(smbfiletochange, 'r');

				for line in smbfiletoread:
					if (line.find('create mask=') >= 0):
						smb_file_perms = line.strip();

				common_methods.replace(smbfiletochange, smb_file_perms, filepermstosmb);

				if (inherit == 'true'):
					smbfiletoread = open(smbfiletochange, 'r');

					for line in smbfiletoread:
						if (line.find('directory mask=') >= 0):
							smb_dirs_perms = line.strip();

					common_methods.replace(smbfiletochange, smb_dirs_perms, dirspermstosmb);

			allperms       = str(owner_permission) + str(group_permission) + str(other_permission); 

			# if recursive option is checked
			if (inherit == 'true'):
				perm_command = 'sudo chmod -R ' + str(owner_permission) + str(group_permission) + str(other_permission) + ' "' + permission_for_path + '"';

			else:
				perm_command = 'sudo chmod ' + str(owner_permission) + str(group_permission) + str(other_permission) + ' "' + permission_for_path + '"';

			status = commands.getstatusoutput(perm_command);

			log_string = str(common_methods.now) + '<<>>From: ' + common_methods.remote_ip + '<<>>' + perm_command + '<<>>' + str(status);
			log_array.append(log_string);

		if (purpose == 'local'):
			allperms       = str(owner_permission) + str(group_permission) + str(other_permission); 

			# if recursive option is checked
			if (inherit == 'true'):
				perm_command = 'sudo chmod -R ' + str(owner_permission) + str(group_permission) + str(other_permission) + ' "' + permission_for_path + '"';

			else:
				perm_command = 'sudo chmod ' + str(owner_permission) + str(group_permission) + str(other_permission) + ' "' + permission_for_path + '"';

			status = commands.getstatusoutput(perm_command);

			log_string = str(common_methods.now) + '<<>>From: ' + common_methods.remote_ip + '<<>>' + perm_command + '<<>>' + str(status);
			log_array.append(log_string);

		restrict_status = [0];

		# if restrict option is checked
		if (restrict == 'true'):
			restrict_status_command = 'sudo chmod +t "' + permission_for_path + '"';
			restrict_status         = commands.getstatusoutput(restrict_status_command);
			
		if (status[0] == 0 and restrict_status[0] == 0):
			print "<script>alert('Permissions set for [%s]!');</script>" % share_name;

		else:
			print "<script>alert('Could not set permissions for [%s]!');</script>" % share_name;

		# construct a log string
		log_string = str(common_methods.now) + '<<>>From : ' + common_methods.remote_ip + '<<>>' + restrict_status_command + '<<>>' + str(restrict_status);
		log_array.append(log_string);

		common_methods.append_file(log_file, log_array);

		#print "<script>location.href = 'main.py?page=share_det&act=share_perms_done';</script>";
		print "<script>location.href = 'show_shares.py?s1=%s&act=share_perms_done&opt=%s';</script>" % (share_name, purpose);

	else:
		common_methods.relogin();

except Exception as e:
	disp_except.display_exception(e);
