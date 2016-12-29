#!/usr/bin/python
#_*_ coding: UTF-8 _*_

#enable debugging

import traceback, sys
sys.path.append('/var/www/fs4/modules')
import disp_except;

try:
	import cgitb, commands, common_methods, share_details, share_smb_settings, subprocess;
	cgitb.enable();

	# create a userslist groupslist from the method get_users_string() defined in common_methods.py
	all_users_list  = common_methods.get_users_string();
	all_groups_list = common_methods.get_groups_string();

	all_users_array  = [];
	all_groups_array = [];

	# if userslist is not empty
	if (all_users_list['id'] == 0):
		if (share_details.connstatus == 'Join is OK'):
			all_users_array = common_methods.read_file('/tmp/adsusersfile');

		else:
			all_users_array  = all_users_list['users'];

	# if groupslist id not empty
	if (all_groups_list['id'] == 0):
		if (share_details.connstatus == 'Join is OK'):
			all_groups_array = common_methods.read_file('/tmp/adsgroupsfile');

		else:
			all_groups_array = all_groups_list['groups'];

	path = share_details.path.strip();
	share = share_details.share.strip();
	comment =  share_details.comment.strip();

	getownercommand = 'sudo /usr/bin/getfacl '  + path;
	
	getownergroup = commands.getstatusoutput(getownercommand);

	owner_set = 'root';
	group_set = 'root';

	if (getownergroup[0] == 0):
		owner_set = common_methods.substr(getownergroup[1], 'owner:', 'group', '');

		if (getownergroup[1].find('flag') > 0):
			group_set = common_methods.substr(getownergroup[1], 'group:', 'flag', '');

		else:
			group_set = common_methods.substr(getownergroup[1], 'group:', '\nuser', '');
		
		owner_set = owner_set.replace('\\134', '\\').strip();
		owner_set = owner_set.replace('\\040', ' ').strip();

		group_set = group_set.replace('\\134', '\\');
		group_set = group_set.replace('\\040', ' ').strip();

		owner_set = owner_set[:owner_set.rfind('#')];

		if (owner_set.find('+') > 0):
			owner_set = owner_set[owner_set.find('+') + 1:];

		if (owner_set.find('\\') > 0):
			owner_set = owner_set[owner_set.find('\\') + 1:];

		if (group_set.find('+') > 0):
			group_set = group_set[group_set.find('+') + 1:];
		
		if (group_set.find('\\') > 0):
			group_set = group_set[group_set.find('\\') + 1:];
		
		owner_set = owner_set.strip();
		group_set = group_set.strip();

	inherit_group_checked = '';

	check_inherit_line = commands.getoutput('sudo grep ^%s: /var/www/global_files/share_owns_global_file' % share );
	inherit_val = check_inherit_line[check_inherit_line.rfind(':') + 1:].strip();

	if (inherit_val == 'true'):
		inherit_group_checked = 'checked';

	print common_methods.share_own_wait;

	print """
	<table width = "685" border = "0" cellspacing = "0" cellpadding = "0" name = 'disp_tables' id = 'id_share_ownership' """ + share_details.stylestring + """;' class = 'outer_border'>"""

	if (share_details.append_mode == 'a'):
		print """<tr><td><div style = 'display: block; margin-top: 2%; margin-left: auto; margin-right: auto; text-align: center; border: 0px solid #736f6e; vertical-align: center; color: darkred; font: 16px Arial;'>You can't set ownership since 'Append mode' is enabled for this path!</div></td></tr>"""; 

	else:
		print """
				<form name = 'change_owner' method = 'POST' action = 'change_ownership.py'>
					<tr>
						<td height = "33px" width = "8" align = "left">
							<img src = "../images/rightside_left.jpg" width = "8" height = "33" />
						</td>
						<td width = "669" height = "33px" align = "left" valign = "middle" class = "right_bg rightsidemenuheading">
							<a class = 'link' href = 'share_owner_help.php' onclick = "window.open('share_owner_help.php', 'help', 'location = no, height = 500, width = 600'); return false;">""" + common_methods.getimageicon() + """</a>"""
		print """
							Share ownership
						</td>
						<td height = "33px" width = "8" align = "right">
							<img src = "../images/rightside_right.jpg" />
						</td>
					</tr>
					<tr>
						<td colspan = "3" align = "left" valign = "top">
						<table width = "685" border = "0" cellspacing = "0" cellpadding = "0">
						<tr>
						<td width = '40%' class = "table_heading" height = "70px" valign = "middle">
							Currently assigned to user
						</td>
						<td class = "table_heading" height = "70px" valign = "middle">"""
		if (len(all_users_array) > 1000):
			print "<input type = 'text' name = 'users' class = 'textbox'>"

		else:
			print """

							<select class = 'input' name = 'users' style = 'width: 90%;' """ + share_smb_settings.smbdisabled + """ """ + share_details.alldisabled + """>
						<option value = 'root'>root</option>"""
							
			for usersval in all_users_array:
				if (usersval != ''):
					if (share_details.connstatus == 'Join is OK'):
						if (usersval.find('[AND]') > 0):
							usersval = usersval.replace('[AND]', '&');

						if (usersval.find('[HASH]') > 0):
							usersval = usersval.replace('[HASH]', '#');

						if (usersval.find('[DOLLAR]') > 0):
							usersval = usersval.replace('[DOLLAR]', '$');

						usersvalline = commands.getstatusoutput('wbinfo --user-info="%s"' % usersval);

						if (usersvalline[0] == 0):
							uidline = usersvalline[1];

							temp = [];
							temp = uidline.split(':');
		
							uid = temp[2];
						
							uid = str(uid).strip();

							if (usersval.find('+') > 0):
								users = usersval[usersval.find('+') + 1:];

							elif (usersval.find('\\') > 0):
								users = usersval[usersval.find('\\') + 1:];

							usersval = uid;

					else:
						users = usersval;
				
					if (users == owner_set):
						print """<option value = '""" + usersval + """' selected title = '""" + users + """'>""" + users + """</option>""";

					else:
						print """<option value = '""" + usersval + """' title = '""" + users + """'>""" + users + """</option>""";
			print """</select>"""
		print'<br>'
		print """					</td>
					</tr>
					<tr>
						<td class = 'table_heading' height = '35px'>
							Currently assigned to group
						</td>
						<td class = "table_heading" height = "70px" valign = "middle">"""
		if (len(all_groups_array) > 1000):
			print """<input type = 'text' class = 'textbox'>""";

		else:
			print """
							<select class = 'input' name = 'groups' style = 'width: 90%;' """ + share_smb_settings.smbdisabled + """ """ + share_details.alldisabled + """>
						<option value = 'root'>root</option>"""
			for groupsval in all_groups_array:
				if (share_details.connstatus == 'Join is OK'):
					if (groupsval.find('[AND]') > 0):
						groupsval = groupsval.replace('[AND]', '&');

					if (groupsval.find('[HASH]') > 0):
						groupsval = groupsval.replace('[HASH]', '#');

					if (groupsval.find('[DOLLAR]') > 0):
						groupsval = groupsval.replace('[DOLLAR]', '$');

					groupsvalline = commands.getstatusoutput('wbinfo --group-info="%s"' % groupsval);

					if (groupsvalline[0] == 0):
						gidline = groupsvalline[1];

						temp = [];
						temp = gidline.split(':');

						gid = temp[2];
						
						gid = str(gid).strip();

						if (groupsval.find('+') > 0):
							groups = groupsval[groupsval.find('+') + 1:];

						elif (groupsval.find('\\') > 0):
							groups = groupsval[groupsval.find('\\') + 1:];

						groupsval = gid;

				else:
					groups = groupsval;

				groups = groups.strip();

				if (groups == group_set):
					print """<option value = '""" + groupsval + """' selected title = '""" + groups + """'>""" + groups + """</option>"""

				else:
					print """<option value = '""" + groupsval + """' title = '""" + groups + """'>""" + groups + """</option>"""
			print """</select>"""
		print '<br>'
		print """					</td>
					</tr>
					<tr>
						<td></td>
					</tr>
					<tr>
						<td></td>
					</tr>
					<tr>
						<td colspan = '2' class = "table_heading" height = "70px" valign = "middle">"""
		print """						<input type = 'checkbox' name = 'inherit' %s %s %s><B>Inherit ownership to sub-folders</B><BR><BR>""" % (inherit_group_checked, share_smb_settings.smbdisabled, share_details.alldisabled)
		print """					</td>
					</tr>
					<tr>
						<td colspan = '2' align = 'right' class = "table_heading" height = "70px" valign = "middle">
							<BR>
							<div style= 'float:right;'>
							<span style="margin-left: 54%;" ><span id="button-one"><button type = 'button' name="reassign" value="Re-Assign" """+ share_smb_settings.smbdisabled +"""onclick ='return validate_ownership("reassign");' """+ share_details.alldisabled + """ style = 'width:65px; background-color:#E8E8E8; border:none; float: left;font-size: 100%; ' title="Re-assign"><a style="font-size:85%;">Re-assign</a></button></span></span>
								<!--<input class = 'input1' type = 'button' name = 'reassign' value = 'Re-Assign' """ + share_smb_settings.smbdisabled + """ onclick = 'return validate_ownership("reassign");' """ + share_details.alldisabled + """>-->"""

		print """
						<span style="margin-left: 54%;" ><span id="button-one"><button type = 'button' name="reset" """+ share_smb_settings.smbdisabled + """ value="Reset Ownership" onclick ='return validate_ownership("reset");' """+ share_details.alldisabled +""" style = 'width:65px; background-color:#E8E8E8; border:none; float: left;font-size: 100%; ' title="Reset"><a style="font-size:85%;">Reset Ownership</a></button></span></span>
	</div>
	<!--					<input class = 'input1' type = 'button' name = 'reset' """ + share_smb_settings.smbdisabled + """ value = 'Reset Ownership' onclick = 'return validate_ownership("reset");' """ + share_details.alldisabled + """>-->"""
								
		print """
							<input type = 'hidden' name = 'hidpage_from' value = 'checked'>
						</td>
					</tr>
					<input type = 'hidden' name = 'hid_path' value = '%s'>
					<input type = 'hidden' name = 'hid_share' value = '%s'>
					<input type = 'hidden' name = 'hid_comment' value = '%s'>
				</table></td></tr>
			</form>""" % (path, share, comment);
	print """</table>"""

except Exception as e:
        disp_except.display_exception(e);

