#!/usr/bin/python
import cgitb, cgi, common_methods, os, sys

cgitb.enable()

sys.path.append('/var/nasexe/python/');
from tools import acl;
from fs2global import *;

sys.path.append('../modules/');
import disp_except;

try:
	session_user = common_methods.get_session_user();

	if (session_user != ''):
		form = cgi.FieldStorage();

		share_name = form.getvalue('hid_s_name');
		share_path = form.getvalue('acl_path');
		set_owner  = form.getvalue('assd_user');
		set_group  = form.getvalue('assd_group');
		recursive  = form.getvalue('inherit_ownership');

		resetowner = form.getvalue('reset_ownership');

		share_path1 = '/storage/' + share_path;

		if (recursive == 'on'):
			recursive = 'YES';

		else:
			recursive = 'NO';

		if (resetowner == 'ResetOwner'):
			set_owner = 'root';
			set_group = 'root';

		ownership_status = acl.set_ownership(share_path1, set_owner, set_group, recursive);

		if (ownership_status == True):
			print "<script>location.href = 'main.py?page=acl&action=own_value#tabs-4';</script>"
			#if (resetowner == 'ResetOwner'):
			#	print "<script>alert('Re-Set Ownership successful !');</script>";

			#else:
			#	print "<script>alert('Ownership set to [%s] !');</script>" % share_path;

		#else:
		#	common_methods.sendtologs('ERROR', 'Set Ownership', 'UI', '"change_ownership.py " ' + str(ownership_status));

		print "<script>location.href = 'main.py?page=acl&share_name=%s#subtabs-4';</script>" % share_name;

	else:
		common_methods.relogin();

except Exception as e:
	disp_except.display_exception(e);
