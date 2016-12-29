#!/usr/bin/python
import cgitb, cgi, common_methods, os, sys, datetime, include_files
sys.path.append('/var/nasexe/python/');
import ftp_auth, anon_ftp;
import commons;
from fs2global import *;

cgitb.enable();

sys.path.append('../modules/');
import disp_except;

#print 'Content-type: text/html';
#print;

form = cgi.FieldStorage();

try:
	session_user = common_methods.get_session_user();

	if (session_user != ''):
		enable_ftp = form.getvalue('conf');

		if (enable_ftp == None):
			enable_ftp = form.getvalue('reconf');

		remove_ftp = form.getvalue('unconf');
		selected_share = form.getvalue('hid_share');

		if (enable_ftp == 'configure'):
			auth_file = ftp_share_conf_dir+selected_share+".auth"
			anon_file = ftp_share_conf_dir+selected_share+".anon"
			check_auth_file_existance = os.path.isfile(auth_file)
			check_anon_file_existance = os.path.isfile(anon_file)

			readonly_opt  = form.getvalue("ftp_read_only");
			access_ip     = form.getvalue("ftp_access_ip")
			write_ip      = form.getvalue("ftp_write_ip")
			grant_users   = form.getvalue("grant_users[]")
			grant_groups  = form.getvalue("grant_groups[]")
			selected_mode = form.getvalue("choose_ftp_options")
			domainname    = form.getvalue("domainslist");

			new_gu_array = [];
			new_gg_array = [];

			a = grant_users;
			b = grant_groups;

			a = str(a);
			b = str(b);

			if (a.find('[') == 0):
				if (len(grant_users) > 0):
					grant_users = [common_methods.replace_chars(gu, 'texttochar') for gu in grant_users];
					grant_users = [gu.replace('\\\\', '\\') for gu in grant_users];

			else:
				if (grant_users != None):
					grant_users = common_methods.replace_chars(grant_users, 'texttochar');
					grant_users = grant_users.replace('\\\\', '\\');

			if (b.find('[') == 0):
				if (len(grant_groups) > 0):
					grant_groups = [common_methods.replace_chars(gg, 'texttochar') for gg in grant_groups];
					grant_groups = [gg.replace('\\\\', '\\') for gg in grant_groups];

			else:
				if (grant_groups != None):
					grant_groups = common_methods.replace_chars(grant_groups, 'texttochar');
					grant_groups = grant_groups.replace('\\\\', '\\');

			if (readonly_opt == 'on'):
				write_ip = '';

			dict_value = {'sharename':selected_share,'ftp_access_ip':access_ip, 'ftp_write_ip':write_ip, 'ftpread_only':readonly_opt}
			dict_values_auth = {'sharename':selected_share, 'ftp_grant_users':grant_users, 'ftp_grant_groups':grant_groups}

			if (enable_ftp == "configure"):
				if (selected_mode == "anonymous"):
					if ((check_anon_file_existance == False) and (check_auth_file_existance == True)):
						call_unmount = commons.unmount_ftp(selected_share)

					ftp_auth.unconfigure(selected_share)
					anon_ftp.anonymous_configure(dict_value)

					if ((check_anon_file_existance == False) and (check_auth_file_existance == True)):
						call_mount = commons.mount_ftp(selected_share)

				elif (selected_mode == "authenticated"):
					if ((check_anon_file_existance == True) and (check_auth_file_existance == False)):
						call_unmount = commons.unmount_ftp(selected_share)

					anon_ftp.anonymous_unconfigure(selected_share)
					ftp_auth.configure(dict_values_auth)

					if((check_anon_file_existance == True) and (check_auth_file_existance == False)):
						call_mount = commons.mount_ftp(selected_share)

				if ((check_anon_file_existance == False) and (check_auth_file_existance == False)):
					call_mount = commons.mount_ftp(selected_share)

		if (remove_ftp == 'unconfigure'):
			call_unmount = commons.unmount_ftp(selected_share)
			anon_ftp.anonymous_unconfigure(selected_share)
			ftp_auth.unconfigure(selected_share)

		if (remove_ftp == 'unconfigure'):
			#print "<script>location.href = 'ftp_settings.py?share_name=%s&mess1=';</script>" % selected_share;
			print "<script>location.href = 'iframe_ftp_settings.py?share_name=%s&mess1=';</script>" % selected_share;

		else:
			#print "<script>location.href = 'ftp_settings.py?share_name=%s&mess=';</script>" % selected_share;
			print "<script>location.href = 'iframe_ftp_settings.py?share_name=%s&mess=';</script>" % selected_share;
		
	else:
		common_methods.relogin();

except Exception as e:
	disp_except.display_exception(e);
