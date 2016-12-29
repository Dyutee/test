#!/usr/bin/python
import cgitb, commands, common_methods, os, sys, cgi

sys.path.append('../modules/');
import disp_except;

sys.path.append('/var/nasexe/python/');
import cli_utils;

sys.path.append('/var/nasexe/storage/');
import storage_op;
from lvm_infos import *;
from functions import *;

cgitb.enable();

form = cgi.FieldStorage()

try:
	log_array = [];
	log_file = common_methods.log_file;

	# default state of the radio button set for 'No root squash'
	no_root_checked = 'checked';

	# get the connection status (ads, nis or local) declared in common_methods.py
	connstatus = common_methods.conn_status();

	# Needs to be removed after testing
	#connstatus = 'Join is OK';
	########################

	#send the connection status to log
	log_string = str(common_methods.now) + '<<>>From: ' + common_methods.remote_ip + '<<>>' + 'AUTHENTICATION: ' + str(connstatus);
	log_array.append(log_string);

	# get the querystring from the url when redirected from show_shares.py(see the script show_shares.py)
	querystring = os.environ["QUERY_STRING"];
	querystring = querystring.replace('%20', ' ');

	page      = common_methods.getsubstr(querystring, 'page=', '&');
	from_page = common_methods.getsubstr(querystring, '&from_page=', '&');

	# all_users_list, all_groups_list is a dictionary output from the method get_users_string() in common_methods.py
	all_users_list  = '';
	all_groups_list = '';

	all_users_list  = common_methods.get_users_string();
	all_groups_list = common_methods.get_groups_string();

	log_string = str(common_methods.now) + '<<>>From: ' + common_methods.remote_ip + '<<>>' + 'USERS: ' + str(all_users_list);
	log_array.append(log_string);

	log_string = str(common_methods.now) + '<<>>From: ' + common_methods.remote_ip + '<<>>' + 'GROUPS: ' + str(all_groups_list);
	log_array.append(log_string);

	common_methods.append_file(log_file, log_array);

	all_users_array  = [];
	all_groups_array = [];

	# if all_users_list is not empty, then create all_users_array from all_users_list dictionary
	if (all_users_list['id'] == 0):
		if (common_methods.conn_status == 'Join is Ok'):
			all_users_array = common_methods.read_file('adsusersfile');

		else:
			all_users_array  = all_users_list['users'];

	# if all_groups_list is not empty, then create all_groups_array from all_groups_list dictionary
	if (all_groups_list['id'] == 0):
		if (common_methods.conn_status == 'Join is OK'):
			all_groups_array = common_methods.read_file('adsgroupsfile');

		else:
			all_groups_array = all_groups_list['groups'];

	# get the basic details of a share from the /tmp/details_of_share file
	sharestring   = commands.getoutput('sudo grep "sharename=" /tmp/details_of_share');
	pathstring    = commands.getoutput('sudo grep "sharepath=" /tmp/details_of_share');
	commentstring = commands.getoutput('sudo grep "sharecomm=" /tmp/details_of_share');

	share   = sharestring[sharestring.find('=') + 1:];
	path    = pathstring[pathstring.find('=') + 1:];
	comment = commentstring[commentstring.find('=') + 1:];

	if (path.find('/storage/') < 0):
		path = '/storage/' + path;

	diskname = path[path.find('/storage/') + len('/storage/'):path.rfind('/')];

	if (diskname != ''):
		diskname = diskname.strip();

	checkmount = cli_utils.is_disk_mounted(diskname);

	mounteddisksstring = '';

	alldisabled  = '';
	mountmessage = '';
	stylestring  = '';

	if (checkmount['id'] == 0):
		mounteddisksstring = ':' + diskname + ':';
		alldisabled = '';

	else:
		alldisabled = 'disabled';
		mountmessage = '<font color = \'darkred\' size = \'2\'>You can\'t configure this share, since the disk on which it is created is not mounted. Run \'Rescan Volumes\' and \'Remount Volumes\' from \'Maintenance\' menu</font>';
		stylestring = 'background: #FFF; opacity: 0.6';

	# get the response from the querystring to decide the display style of the forms last submitted
	response  = common_methods.getsubstr(querystring, '&act=', '&');

	# define default styles for the visibility of the form elements
	edit_share_style  = 'table';
	share_smb_style   = 'table';
	share_acl_style   = 'none';
	reset_acl_style   = 'none';
	append_mode_style = 'none';
	share_perms_style = 'none';
	share_owns_style  = 'none';
	share_afp_style   = 'none';
	share_perms_style = 'none';
	share_owns_style  = 'none';
	share_nfs_style   = 'none';
	share_ftp_style   = 'none';

	append_mode = '';

	audit_options_enabled = 'disabled';

	# when each feature is enabled, the control should come back to the same form from where the values are submitted
	if (response == 'edit_share_done'):
		edit_share_style = 'table';

	if (response == 'share_smb_done'):
		share_smb_style  = 'table';
		edit_share_style = 'none';

	if (response == 'share_acl_done'):
		share_acl_style  = 'table';
		edit_share_style = 'none';

	if (response == 'reset_acl_done'):
		reset_acl_style  = 'table';
		edit_share_style = 'none';

	if (response == 'append_mode_done'):
		append_mode_style = 'table';
		edit_share_style  = 'none';
		
	if (response == 'share_afp_done'):
		share_afp_style   = 'table';
		edit_share_style  = 'none';

	if (response == 'share_perms_done'):
		share_perms_style = 'table';
		edit_share_style  = 'none';

	if (response == 'share_own_done'):
		share_owns_style  = 'table';
		edit_share_style  = 'none';

	if (response == 'share_nfs_done'):
		share_nfs_style   = 'table';
		edit_share_style  = 'none';

	if (response == 'share_ftp_done'):
		share_ftp_style   = 'table';
		edit_share_style  = 'none';

	if (response == 'del_share_done'):
		edit_share_style = 'none';

	# initialize an empty array for shares
	shares_array = [];

	# nas disks array is created using the get_nas_disks() method defined in common_methods.py
	nas_disks_array = common_methods.get_nas_disks();

	details_style = '';

	if (path.find('/storage/') < 0):
		path = '/storage/' + path;

	append_mode = common_methods.get_appendmode(path);

	details_style = 'none';

	if (share != ''):
		details_style = 'block';

	"""
	=============================================================
	Created the nas disks array in common_methods.py.
	=============================================================
	"""
	nas_disks_array = common_methods.get_nas_disks();

	for nas_disks in nas_disks_array:
		temp = [];
		temp = nas_disks.split('/');
		nas_disk = nas_disks.strip();

	# create shares array from  shares_global_file
	permission = commands.getoutput('sudo chmod 777 /var/www/global_files/shares_global_file')
	shares_file  = '/var/www/global_files/shares_global_file';
	shares_array = common_methods.read_file(shares_file);

	# nas disks array is not empty and page is of share_details then show the dropdown below
	if (len(nas_disks_array) > 0 and page == 'share_det'):
		print """<div width = '685' align = 'center' id = 'details_title' style = 'display: """ + details_style + """;'>
		<font face = 'Arial' size = '3'><B><I><U>Details of share '""" + share + """'</U></I></B></font>

	<select id = 'id_options' class = 'textbox' name = 'options' style = 'width: 20%;' onchange = 'return show_table(document.getElementById("id_options").value);'>
		<option value = ''>---</option>
		<option value = 'id_edit_this_share'>Edit this share</option>
		<option value = 'id_smb_settings'>SMB settings</option>
		<!--<option value = 'id_acl_settings'>ACL settings</option>-->
		<!--<option value = 'id_reset_acl'>Reset ACL settings</option>-->
		<option value = 'id_append_mode'>Append mode</option>
		<option value = 'id_afp_settings'>AFP settings</options>
		<option value = 'id_share_permissions'>Share permissions</option>
		<option value = 'id_share_ownership'>Share ownership</option>
		<option value = 'id_nfs_settings'>NFS settings</option>
		<option value = 'id_ftp_settings'>FTP settings</option>
	</select>
	""" + mountmessage + """
	</div>""";

	print """</td>
	 <td valign = "top" align = "left" width = "30px"></td>

	<td valign = "top" align = "left" width = "695px">"""

	#print """<div style = 'background: gray; height: 50%; width: 695px; position: absolute; opacity: 0.5;'></div>"""
	if (page == 'share'):
		import nas_settings;

	if (page == 'share_det'):
		import share_maintenance;
		#import user_quota;

		comment = comment.replace("\\'", "'");

		import edit_this_share;
		import share_smb_settings;

		print common_methods.append_mode_wait

		import append_mode_settings;
		import share_afp_settings;
		import set_share_permissions;
		#import set_share_ownership;
		import set_nfs_settings;
		#import set_ftp_settings;
		import set_acl;
		import reset_acl_settings

except Exception as e:
	disp_except.display_exception(e);

