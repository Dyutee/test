#!/usr/bin/python
import cgitb, commands, common_methods, share_details, sys

sys.path.append('/var/nasexe/python/');
import smb;
from fs2global import *;

cgitb.enable();
message = '';
adsdomain = common_methods.ads_domain;

# create a userslist groupslist from the method get_users_string() defined in common_methods.py
all_users_list  = common_methods.get_users_string();
all_groups_list = common_methods.get_groups_string();

smb_all_users_array  = [];
smb_all_groups_array = [];

domainsarray            = [];
available_domains_array = [];
params_array            = [];
userdomainsstring       = '';
groupdomainsstring      = '';

# if userslist is not empty
if (all_users_list['id'] == 0):
	if (share_details.connstatus == 'Join is OK'):
		smb_all_users_array = common_methods.read_file('/tmp/adsusersfile');

	else:
                smb_all_users_array  = all_users_list['users'];

# if groupslist id not empty
if (all_groups_list['id'] == 0):
	if (share_details.connstatus == 'Join is OK'):
		smb_all_groups_array = common_methods.read_file('/tmp/adsgroupsfile');

	else:
                smb_all_groups_array = all_groups_list['groups'];

if (share_details.connstatus == 'Join is OK'):
	domainsarray = common_methods.get_all_domains();

	if (len(domainsarray) > 0):
		for i in domainsarray:
			i = i.strip();
			#checkdomain = commands.getstatusoutput('wbinfo -g|grep "^%s"' % i);
			checkdomain = commands.getstatusoutput('sudo cat /tmp/adsgroupsfile | grep "^%s"' % i);

			if (checkdomain[0] == 0):
				available_domains_array.append(i);

	if (len(available_domains_array) > 1):
		smb_all_users_array  = [];
		smb_all_groups_array = [];

		for domains in available_domains_array:
			usersfiletocreate  = '/tmp/' + domains + '_users.txt';
			groupsfiletocreate = '/tmp/' + domains + '_groups.txt';

			usersofdomainres  = commands.getstatusoutput('sudo cat /tmp/adsusersfile|grep "^%s" > %s' % (domains, usersfiletocreate));
			groupsofdomainres = commands.getstatusoutput('sudo cat /tmp/adsgroupsfile|grep "^%s" > %s' % (domains, groupsfiletocreate));

			userdomainsstringline = commands.getstatusoutput('sudo grep "^%s" /tmp/adsusersfile' % domains);

			if (userdomainsstringline[0] == 0):
				userdomainsstring = userdomainsstringline[1].strip();
				userdomainsstring = userdomainsstring.replace('\n', ':');
				userdomainsstring = userdomainsstring + '<DOMAIN_SEPARATOR>';

smb_full_users_string  = '';
smb_full_groups_string = '';

if (len(smb_all_users_array) > 0):
	for smbusers in smb_all_users_array:
		smbusers = smbusers.strip();
		smbusers = common_methods.replace_chars(smbusers, 'chartotext');

		if (len(domainsarray) == 1):
			smbusers = smbusers[smbusers.find('+') + 1:];
			smbusers = smbusers.strip();

		smb_full_users_string += smbusers + ':';

	smb_full_users_string = smb_full_users_string[:smb_full_users_string.rfind(':')];
	smb_full_users_string = smb_full_users_string.strip();

	#smb_full_users_string = ':'.join(smb_all_users_array);

if (len(smb_all_groups_array) > 0):
	for smbgroups in smb_all_groups_array:
		smbgroups = smbgroups.strip();
		smbgroups = common_methods.replace_chars(smbgroups, 'chartotext');

		#if (len(domainsarray))
		smb_full_groups_string += smbgroups + ':';

	smb_full_groups_string = smb_full_groups_string[:smb_full_groups_string.rfind(':')];
	smb_full_groups_string = smb_full_groups_string.strip();
	#smb_full_groups_string = ':'.join(smb_all_groups_array);

# check log path so that if the current share is enabled as log path, then auditing should not be allowed on the 
# same share path. that share should become a readonly share
check_log_path_command = 'sudo grep "SMBLOGPATH=" /var/nasconf/smb-log.conf';
check_log_path         = commands.getoutput(check_log_path_command);

lpath = '';

if (check_log_path != ''):
	temp = [];
	temp = check_log_path.split('=');

	d12   = temp[0];
	lpath = temp[1];

# check whether a SMB is enabled for a share or not
#check_current_share_command = 'sudo grep "\[' + share_details.share + '\]" /var/nasconf/shares';
#current_share = commands.getoutput(check_current_share_command);

current_share = commands.getstatusoutput('ls %s/%s' % (smb_share_conf_dir, share_details.share));

domain_only       = '';
smbdisabled       = '';
writable_checked  = 'checked';
guest_checked     = '';
public_checked    = 'checked';
validuser_checked = '';
visible_checked   = '';
conn_text         = '';

valid_user = '';
use_smb    = '';
smb_line   = '';

# the details of the share are retrieved from the /tmp/details_of_share file 
smb_line = commands.getoutput('sudo grep "use_smb=" /tmp/details_of_share');

# condition if SMB is enabled
if (smb_line != ''):
	writable_line   = commands.getoutput('sudo grep "writable=" /tmp/details_of_share');
	browsable_line  = commands.getoutput('sudo grep "browsable=" /tmp/details_of_share');
	guest_ok_line   = commands.getoutput('sudo grep "guest_ok=" /tmp/details_of_share');
	public_line     = commands.getoutput('sudo grep "public=" /tmp/details_of_share');
	valid_user_line = commands.getoutput('sudo grep "valid_users=" /tmp/details_of_share');

	writable   = writable_line[writable_line.find('=') + 1:];
	browsable  = browsable_line[browsable_line.find('=') + 1:];
	public     = public_line[public_line.find('=') + 1:];
	guest_ok   = guest_ok_line[guest_ok_line.find('=') + 1:];
	
	# depending on the values retrieved, the form should show the values set and it should also 
	# retain the state of the checkbox, radio elements whether they are selected or not...
	if (valid_user_line != ''):
		valid_user = valid_user_line[valid_user_line.find('=') + 1:];
		valid_user = valid_user.strip();

	if (writable_line == 'writable=yes'):
		writable_checked = '';

	if (browsable_line == 'browsable=yes'):
		visible_checked = 'checked';

	if (public_line == 'public=yes' or guest_ok_line == 'guest_ok=yes'):
		public_checked = 'checked';

	if (valid_user != '' and public_line != 'public=yes'):
		validuser_checked = 'checked';

smb_selected  = '';
smb_opt_style = 'none';

check_string       = '';
valid_users_style = 'none';

# lpath is the log path value. if the path of the share and the log path is matched, then the other features of the smb
# except the permissions and ownership should be disabled.
if (share_details.path == lpath):
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

	delete_entry_command = 'sudo /var/nasexe/delete_entry "full_audit:" share_conf_file /var/nasconf/';
	commands.getoutput(delete_entry_command);

# get the authenticated users from the share details page
valid_user = valid_user.replace('" "', '"xxx"');
valid_user = valid_user.strip();

users_array = [];

users_only_array  = [];
groups_only_array = [];
users_dropdown    = '';
groups_dropdown   = '';

if (valid_user != ''):
	users_array = valid_user.split('xxx');
	elemtoremove = '';

	if (len(users_array) > 0 and len(smb_all_users_array) > 0):
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

				if (share_details.connstatus == 'Join is OK'):
					if (users.find('+') > 0):
						only_users = users[users.find('+') + 1:];

					else:
						only_users = users[users.find('\\') + 1:];

					users = common_methods.replace_chars(users, 'chartotext');

					# generate a dropdown for assigned ads users
					users_dropdown = users_dropdown + "<option value = '" + users + "' selected title = '" + users + "'>" + only_users + "</option>";
						
					users_only_array.append(only_users);

				elif (share_details.connstatus == 'nis is running'):
					# generate a dropdown for assigned nis users
					users_dropdown = users_dropdown + "<option value = '" + users + "' selected title = '" + users + "'>" + users + "</option>";

				elif (share_details.connstatus == 'local connection'):
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
					if (share_details.connstatus == 'Join is OK'):
						if (groups.find('+') > 0):
							only_groups = groups[groups.find('+') + 1:];
						
						else:
							only_groups = groups[groups.find('\\') + 1:];

						groups = common_methods.replace_chars(groups, 'chartotext');

						# generate a dropdown for assigned ads groups
						groups_dropdown = groups_dropdown + "<option value = '@" + groups + "' selected title = '" + groups + "'>" + only_groups + "</option>";
						groups_only_array.append(only_groups);

					elif (share_details.connstatus == 'nis is running'):
						# generate a dropdown for assigned nis groups
						groups_dropdown = groups_dropdown + "<option value = '@" + groups + "' selected title = '" + groups + "'>" + groups + "</option>";
						groupslist = groups_dropdown.replace('<', '[');

					elif (share_details.connstatus == 'local connection'):
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
		
if (common_methods.test_for_smb == '' and share_details.connstatus == 'Join is OK'):
	message = 'Please check the \'Use SMB\' option in Basic Setup -> SMB Settings for ADS';

	print """<form name = 'share_edit' id = 'id_smb_form'>
	<table width = "685" border = "0" cellspacing = "0" cellpadding = "0" name = 'disp_tables' id = 'id_smb_settings' style = 'background: #000; opacity: 0.5;' class = 'outer_border'>
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
						<input type = 'checkbox' name = 'use_smb' onclick = "window.alert('Check the \'Use SMB\' option in Basic Setup > SMB Settings for ADS.'); return false;" """ + smb_selected + """ """ + share_details.alldisabled + """>&nbsp;<B>Use SMB</B>
					</td>
				</tr>
				</table>
			</td>
		</tr>
	</table>
	</form>"""

else:
	if (len(smb_all_users_array) > 1000 and share_details.connstatus == 'Join is OK'):
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

		user_message = '<BR><font color = \'darkred\' style = \'italic\'>Too many users.<BR>Type the beginning characters of the user name in the text box and click \'Get Users\' button.</font>';

	else:
		count_usr = 2;
			
		ads_users_only_string = '';
		user_message = '';

	#if (len(ads_groups_array) > 1000):
	if (len(smb_all_groups_array) > 1000 and share_details.connstatus == 'Join is OK'):
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

		group_message = '<BR><font color = \'darkred\' style = \'italic\'>Too many groups.<BR>Type the beginning specific group name in the text box.</font>';

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
	
	check_log_path = commands.getoutput('sudo grep "' + lpath + '$" /var/nasconf/smb-log.conf');

	use_smb_opt = '';

	exist_audits_array = [];
	audits_array       = [];
	audit_dropdown     = '';
	recycle_opt        = '';
	audit_recycle      = '';
	recycle_path1      = '';
	audit_option       = '';

	if (current_share[0] == 0):
		use_smb_opt        = commands.getoutput('sudo grep "use_smb=" /tmp/details_of_share');
		users_list_line    = commands.getoutput('sudo grep "valid_users=" /tmp/details_of_share');
		audit_recycle_line = commands.getoutput('sudo grep "vfs objects=" /tmp/details_of_share');
		audit_line         = commands.getoutput('sudo grep "auditoption=" /tmp/details_of_share');
		recycle_line       = commands.getoutput('sudo grep "recycle_repo=" /tmp/details_of_share');

		users_list_line    = users_list_line.strip();
		audit_recycle_line = audit_recycle_line.strip();
		audit_line         = audit_line.strip();
		recycle_line       = recycle_line.strip();

		check_string  = users_list_line[users_list_line.find('=') + 1:];

		if (audit_recycle_line != ''):
			audit_recycle = audit_recycle_line[audit_recycle_line.find('=') + 1:];

		if (audit_line != ''):
			audit_option = audit_line[audit_line.find('=') + 1:];
			audit_option = audit_option.strip();
			audits_array = audit_option.split(' ');

		if (recycle_line != ''):
			recycle_opt   = recycle_line[recycle_line.find('=') + 1:];

		if (audit_option != ''):
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

				if (test_array.index(exist_audits) >= 0):
					exist_audits_array.append(conn_text);
					audit_options_array.pop(audit_options_array.index(conn_text));

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

	check_string = check_string.strip();

	if (check_string != '' and public_line != 'public=yes'):
		valid_users_style = 'table';

	if (use_smb_opt == 'use_smb=on'):
		smb_selected  = 'checked';
		smb_opt_style = 'block';
	
	elif (use_smb_opt == 'use_smb=off'):
		smb_selected  = '';
		smb_opt_style = 'none';

	temp = [];
	temp = check_log_path.split('=');

	d1       = temp[0];
	log_path = temp[1];

	print common_methods.wait_for_response;

	print """<form name = 'share_edit' method = 'POST' id = 'id_smb_form' action = 'edit_shares.py'>
	<!--<table width = "685" border = "0" cellspacing = "0" cellpadding = "0" name = 'disp_tables' id = 'id_smb_settings' style = 'display: """ + share_details.share_smb_style + """; """ + share_details.stylestring + """;' class = 'outer_border'>-->
	<table width = "685" border = "0" cellspacing = "0" cellpadding = "0" name = 'disp_tables' id = 'id_smb_settings' """ + share_details.stylestring + """;' class = 'outer_border'>
		<tr>
			<td height = "33px" width = "8" align = "left">
				<img src = "../images/rightside_left.jpg" width = "8" height = "33" />
			</td>
			<td width = "669" height = "33px" align = "left" valign = "middle" class = "right_bg rightsidemenuheading">
				<a class = 'link' href = 'smb_settings_help.php' onclick = "window.open('smb_settings_help.php', 'help', 'location = no, height = 500, width = 600, scrollbars = 1'); return false;"><?= $image_icon ?></a>
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
				<td width = "1%" class = "table_heading" height = "70px" valign = "middle">"""
audit_disabled = '';

get_recycle_path = commands.getoutput('grep "recycle:repository=/storage/' + share_details.path + '/$" /var/nasconf/shares');

if (get_recycle_path != ''):
	audit_disabled = 'disabled';
	print "<font color = 'darkred'><B>*</B> This share is used as a recycle path.</font>";

print """
 <!--Right side body content starts from here-->
      <div class="rightsidecontainer">
	<div class="insidepage-heading">Nas >> <span class="content">Configure Information</span></div>
	<!--tab srt-->
	<div class="searchresult-container">
	  <div class="infoheader">
	    <div id="tabs">
	      <ul>
		<li><a href="#tabs-1">SMB Settings</a></li>
	      </ul>
	      <div id="tabs-1">

	<!--form container starts here-->
	<form name = 'share_edit' method = 'POST' id = 'id_smb_form' action = 'edit_shares.py'>
	<div class="form-container">
	<div class="topinputwrap-heading">SMB Settings for '"""+get_share+"""'</div>
	  <div class="topinputwrap">
	<table width="100%" style="padding:0 0 0 10px;">
                <tr>
                <td><input type='checkbox' name='use_smb' onclick = 'return show_smb_params();' /> Use SMB</td>
                <td></td>
                </tr>
	</table>

	<div width = '100%' id = 'smb_params' style='display:none;'>
	<table width="100%" style="padding:30px 0 0 30px;">

                <tr>

				<tr>
					<td>
						<input type = 'checkbox' name = 'read_only' """ + writable_checked + """ """ + smbdisabled + """ """ + share_details.alldisabled + """>&nbsp;<B>Read only</B><BR>
						<input  type = 'checkbox' name = 'visible' """ + visible_checked + """ """ + smbdisabled + """ """ + share_details.alldisabled + """>&nbsp;<B>Visible</B><BR><BR>
						<!-- option for auditing/recycling -->
						<input id = 'id_select_adv' type = 'checkbox' name = 'aud_recycle' """ + audrecycle_checked + """ onclick = 'return show_hide(document.getElementById("id_select_adv").checked, document.getElementById("id_adv_feature"));' """ + audit_disabled +  """ """ + share_details.alldisabled + """>&nbsp;<B>Auditing / Recycling</B>
						<div id = 'id_adv_feature' style = 'margin-left: 2%; display: """ + aud_disp_style + """;'>
							<BR><input id = 'id_auditing' type = 'checkbox' name = 'enable_audit' """ + auditing_checked + """ onclick = 'return show_hide(document.getElementById("id_auditing").checked, document.getElementById("id_file_ops"));' """ + auditdisabled + """ """ + share_details.alldisabled + """>&nbsp;<B>Enable Auditing</B> """ + auditmessage + """<div id = 'id_file_ops' style = 'margin-left: 2%; display: """ + file_dir_style + """;'>
								<BR><B>File / Dir operations:</B><BR>
								<select id = 'id_avail_options' class = 'textbox' name = 'file_options' multiple style = 'height: 100px; width: 25%;' onclick = 'return move_users(this.form.id_avail_options, id_assign_options, "1");' """ + share_details.alldisabled + """>"""

for audit_options in audit_options_array:
	temp = [];
	temp = audit_options.split(':');

	value = temp[0];
	lable = temp[1];
					
	#if (!in_array(audit_options, exist_audits_array)):
	#if (audit_options_array.index(audit_options) < 0 ):
	print "<option value = '" + value + "'>" + lable + "</option>";
print """</select>
								<select id = 'id_assign_options' class = 'textbox' name = 'file_options[]' multiple style = 'height: 100px; width: 25%;' onclick = 'return move_users(this.form.id_assign_options, this.form.id_avail_options, "2");' """ + share_details.alldisabled + """>"""
print audit_dropdown
print """								</select>
							</div><BR>
							<input id = 'id_enable_recycle' type = 'checkbox' name = 'enable_recycle' """ + recycle_checked + """ onclick = 'return show_hide(document.getElementById("id_enable_recycle").checked, document.getElementById("id_recycle_options"));' """ + smbdisabled + """ """ + share_details.alldisabled + """>&nbsp;<B>Enable Recycling</B><BR>
							<div id = 'id_recycle_options' style = 'display: """ + recycle_style + """; margin-left: 2%;'>
								<BR><table align = 'left' width = '100%'>

								<tr>
									<td height = '35px' class = 'table_heading' width = '20%'>
										Recycle path
									</td>
									<td>
										<select class = 'textbox' name = 'recycle_path' """ + smbdisabled + """ style = 'width: 60%;' """ + share_details.alldisabled + """>"""
path = share_details.path.replace('/storage/', '');

if (recycle_path1 != ''):
	print """<option value = '""" + recycle_path1 + """' selected>""" + recycle_path1 + """</option>""";
		
else:
	print """<option value = '""" + path + """/Trash/'>""" + path + """/Trash/</option>""";

if (guest_checked == '' and public_checked == '' and validuser_checked == ''):
	guest_checked = 'checked';

if (len(share_details.shares_array) > 0):
	for shares in share_details.shares_array:
		temp = [];
		temp = shares.split(':');

		d1           = temp[0];
		recycle_path = temp[1];
		d2           = temp[2];

		recycle_path = recycle_path[recycle_path.find('/storage/') + len('/storage/'):];
		recycle_path = recycle_path + '/';

		if (recycle_path != share_details.path + '/'):
			if (recycle_path == recycle_path1):
				print """"<option value = '""" + recycle_path + """' selected>""" + recycle_path + """</option>""";
	
			else:
				print """<option value = '""" + recycle_path + """'>""" + recycle_path + """</option>""";

print """									</td>
								</tr>
								</table>
							</div>
						</div>
					</td>
				</tr>
				<tr>
					<td>
					</td>
				</tr>
				<tr>
					<td>
						<BR><B>User access permissions</B>:<BR><BR>
						<input type = 'radio' name = 'priv' value = 'public' """ + public_checked + """ onclick = 'return show_smb_users_groups();' """ + share_details.alldisabled + """><B> Public</B><BR>
						<input type = 'radio' name = 'priv' value = 'valid_user' """ + validuser_checked + """ onclick = 'return show_smb_users_groups();' """ + share_details.alldisabled + """><B> Authenticated User</B>
						<input type = 'hidden' name = 'hid_message' value = '""" + message + """'>
					</td>
				</tr>
				<tr>
					<td>
						<div  width = '100%' id = 'users_list' style = 'display: """ + valid_users_style + """;'>
						<table>
							<tr>
								<td colspan = '2'>
									<BR><B>Users list:</B>""" + user_message + """<BR>"""
if (len(available_domains_array) > 1):
	available_domains_array.sort();
	print """<BR><B>Choose a domain:</B>&nbsp;&nbsp;
		<select name = 'domainslist' class = 'textbox' onchange = 'return submit_domainlist();'>"""
	for domains in available_domains_array:
		print """<option value = '""" + domains + """'>""" + domains + """</option>""";

	print """</select><BR /><BR />"""

print """
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

# if the number of users are more than 1000 then a textbox will appear in the place of dropdown.
# the user has to enter the smb user he wants to see. as he types, a list of names will appear from which he can select
if (len(smb_all_users_array) > 1000 and share_details.connstatus == 'Join is OK'):
	print """<input id = 'available' name = 'ads_user_text' type="text" class = 'input' value = '' onclick = 'document.getElementById("autosuggest").style.display = "none";'><input class = 'input1' type = 'button' name = 'getusers' value = 'Get Users'  onclick = "move_text_to_dropdown(this.form.available, this.form.granted, '1');\" """ + share_details.alldisabled + """ > <input class = 'input1' type = 'button' name = 'move' value = '>'  onclick = "move_text_to_dropdown(this.form.available, this.form.granted, '1');\" """ + share_details.alldisabled + """ >""";

	print """<div id="suggest" style="visibility:hidden;border:#000000 1px solid;width:150px;"></div>
								<select class = 'input' style = 'width: 200px; height: 300px;' id = 'autosuggest' name = 'avail_users' multiple onclick = 'return set_user(this.form.available, this.form.autosuggest, this.form.autosuggest.value);' onkeydown = 'return get_key();' """ + share_details.alldisabled + """>"""
	print """</select>"""

else:
	print """<select class = 'input' style = 'width: 200px; height: 150px;' id = 'available' name = 'avail_users' multiple onclick = "return move_users(this.form.available, this.form.granted, '1');\" """ + share_details.alldisabled + """>"""
	if (share_details.connstatus == 'Join is OK'):
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

	if (share_details.connstatus == 'nis is running'):
		for nis_users in smb_all_users_array:
			nis_users_to_check = '"' + nis_users + '"';

			print """<option value = '""" + nis_users + """' title = '""" + nis_users + """'>""" + nis_users + """</option>""";

	if (share_details.connstatus == 'local connection'):
		for local_users in smb_all_users_array:
			print """<option value = '""" + local_users + """' title = '""" + local_users + """'>""" + local_users + """</option>"""

print """
</select>
								</td>
								<td>
									<select class = 'input' style = 'width: 200px; height: 150px;' id = 'granted' name = 'grant_users[]' multiple onclick = "return move_users(this.form.granted, this.form.available, '%s');" %s>""" % (count_usr, share_details.alldisabled);
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


# if the number of groups are more than 1000 then a text box will appear in place of the dropdown
# the user needs to enter the name of the smb group he wants to see. the names will be displayed below starting with the characters he entered.
if (len(smb_all_groups_array) > 1000 and share_details.connstatus == 'Join is OK'):
	print """<input id = 'available_groups' name = 'ads_group_text' type="text" class = 'input' value = '' oninput = 'generate_user_list(document.getElementById("available_groups"), document.getElementById("g_autosuggest"), \"""" + ads_groups_only_string + """", "groups", "share_edit");' onclick = 'document.getElementById("g_autosuggest").style.display = "none";'> <input class = 'input1' type = 'button' name = 'move' value = '>' onclick = "move_group_to_dropdown(this.form.available_groups, this.form.granted_groups, '1');\" """ + share_details.alldisabled + """>""";

	print """<select class = 'input' style = 'width: 200px; height: 300px;' id = 'g_autosuggest' name = 'avail_groups' multiple onclick = 'return set_user(this.form.available_groups, this.form.g_autosuggest, this.form.g_autosuggest.value);' """ + share_details.alldisabled + """>"""
	print groups_dropdown;
	
	print """
	</select>""";

else:
	print """
<select class = 'input' style = 'width: 200px; height: 150px;' id = 'available_groups' name = 'avail_groups' multiple onclick = "return move_groups(this.form.available_groups, this.form.granted_groups, '1');\" """ + share_details.alldisabled + """>"""

	if (share_details.connstatus == 'Join is OK'):
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

	if (share_details.connstatus == 'nis is running'):
		for nis_groups in smb_all_groups_array:
			print """<option value = '@""" + nis_groups + """' title = '""" + nis_groups + """'>""" + nis_groups + """</option>""";

	if (share_details.connstatus == 'local connection'):
		for local_groups in smb_all_groups_array:
			local_groups = local_groups.strip();
			local_groups_to_check = '"@' + local_groups + '"';

			print """<option value = '@""" + local_groups + """' title = '""" + local_groups + """'>""" + local_groups + """</option>""";
print """
</select>
						</td>
									<td>
										<select class = 'input' style = 'width: 200px; height: 150px;' id = 'granted_groups' name = 'grant_groups[]' multiple onclick = "return move_groups(this.form.granted_groups, this.form.available_groups, '%s');" %s>""" % (count_grp, share_details.alldisabled);
print groups_dropdown;

print """</select>
								</td>
							</tr>
						</table>
						</div>
					</td>
				</tr>
			</table>
		</div>
		<table align = 'center' width = '100%'>
			<tr>
				<td>"""
print common_methods.share_smb_wait;

share   = share_details.share.strip();
path    = path.replace('/storage/', '');
path    = path.strip();

comment = share_details.comment.replace('\n', '');
comment = comment.strip();

print """
				</td>
				<td align = 'right'>
					
					<BR><!--<input class = 'input1' type = 'button' name = 'action_but' value = 'Apply' onclick = 'return submit_smb_form();'>-->
					<span style="margin-left: 54%;" ><span id="button-one"><button type = 'button' name="action_but" value="Apply" onclick ="return submit_smb_form();" style = 'width:65px; background-color:#E8E8E8; border:none; float:none;font-size: 86%; ' title="Create\" """ + share_details.alldisabled + """><a style="font-size:85%;">Apply</a></button></span></span>

					<input type = 'hidden' name = 'hid_domain' value = '""" + adsdomain + """'>
					<input type = 'hidden' name = 'hid_ads' value = '""" + common_methods.ads_status + """'>
					<input type = 'hidden' name = 'hid_nis' value = '""" + common_methods.nis_status + """'>
					<input type = 'hidden' name = 'hidpage_from' value = 'checked'>
					<input type = 'hidden' name = 'hid_share' value = '""" + share + """'>
					<input type = 'hidden' name = 'hid_path' value = '""" + path + """'>
					<input type = 'hidden' name = 'hid_comm' value = '""" + comment + """'>
					<input type = 'hidden' name = 'hid_ads_users' value = '""" + ads_users_only_string + """'>
					<input type = 'hidden' name = 'hidadsusers' value = '""" + smb_full_users_string + """'>
					<input type = 'hidden' name = 'hid_ads_groups' value = '""" + ads_groups_only_string + """'>
					<input type = 'hidden' name = 'hidadsgroups' value = '""" + smb_full_groups_string + """'>
					<input type = 'hidden' name = 'hid_ads_domain' value = '""" + adsdomain + """'>
					<input type = 'hidden' name = 'hid_ads_assigned_users' value = '""" + assigned_users_string + """'>
					<input type = 'hidden' name = 'hid_ads_assigned_groups' value = '""" + assigned_groups_string + """'>

					
				</td>
			</tr>
		</table>
	</td></tr></table>
		<input type = 'hidden' name = 'hid_session_user' value = 's'>
		</form>
	</table>"""
# % (common_methods.ads_domain, common_methods.ads_status, common_methods.nis_status, share, path, comment, ads_users_only_string, ads_groups_only_string, common_methods.ads_domain, assigned_users_string, assigned_groups_string);
