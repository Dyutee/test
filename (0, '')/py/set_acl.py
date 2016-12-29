#!/usr/bin/python
#_*_ coding: UTF-8 _*_                                          
        
#enable debugging                                        
import cgitb, header, os, common_methods, commands, sys
cgitb.enable()                  

sys.path.append('../modules/');
import disp_except;

image_icon = common_methods.getimageicon();
set_id = '';
check_pacl = '';
path_acl = '';

blurstyle = '';
disabled  = '';
mountmess = '';

share_path = '';
share_1 = '';

acl_dropdown_style = 'none';
share_acl_style    = 'none';

connstatus = common_methods.conn_status();

if (connstatus == 'local connection'):
	try:
		sys.path.append('/var/nasexe/python/');
		import cli_utils;

		shares_array = common_methods.get_shares_array();

		# get the query string in the url 
		querystring = os.environ['QUERY_STRING'];

		# get the action parameter from the url coming from the action page
		if (querystring.find('&act=') >= 0):
			response = common_methods.getsubstr(querystring, '&act=', '&');
			
			# if the query string is coming from the action page of acl, then the acl options
			if (response == 'share_acl_done'):
				set_id             = 'id_acl_settings';
				share_acl_style    = 'table';
				add_users_style    = 'none';
				acl_dropdown_style = 'table';

		# get the acl path from the querystring
		if (querystring.find('&pacl=') >= 0):
			path_acl = common_methods.getsubstr(querystring, '&pacl=', '&');

			check_pacl = 'SMBLOGPATH=/storage/' + path_acl;
			check_pacl = check_pacl.strip();

		# check whether the share is set as log path or not.
		log_path_command = 'sudo grep "SMBLOGPATH=" /var/nasconf/smb-log.conf';
		log_path = commands.getoutput(log_path_command);

		if (log_path != ''):
			log_path = log_path.strip();

		checkdiskmount = path_acl[:path_acl.find('/')];

		mounteddisk = cli_utils.is_disk_mounted(checkdiskmount);

		if (mounteddisk['id'] > 0):
			blurstyle = 'background: #FFF; opacity: 0.6';
			disabled = 'disabled';
			mountmess = '<font color = \'darkred\' size = \'2\'>You can\'t set ACL for this share, since the disk on which it is created is not mounted. Run \'Rescan Volumes\' and \'Remount Volumes\' from \'Maintenance\' menu</font>';

		#print str(mountmess) + '<BR>';
		print """<table width = "685" border = "0" cellspacing = "0" cellpadding = "0" style = 'border-collapse: collapse; display: """ + acl_dropdown_style + """;' class = 'outer_border' id = 'id_acl_settings'>
					<tr>
						<td class = 'table_heading' width = '20%'>
							Choose a share
						</td>
						<td>
							<form name = 'choose_share'>
							<select class = 'textbox' name = 'share_list' style = 'width: 99%;' onchange = 'return set_acl_params(document.choose_share.share_list.value, "");'>
							<option value = ''>--</option>"""
		if (len(shares_array) > 0):
			for shares in shares_array:
				share_1    = shares[:shares.find(':')];
				share_path = shares[shares.find(':') + 1:shares.rfind(':')];
				comment    = shares[shares.rfind(':') + 1:];

				share_1    = share_1.strip();
				share_path = share_path.strip();
				comment    = comment.strip();

				share_path = share_path[share_path.find('/storage/') + len('/storage/'):];

				# if ACL is set for the selected path, then the choosen path is shown in selected state
				if (path_acl == share_path):
					print """<option value = '""" + share_path + """' selected>""" + share_1 + """ - """ + share_path + """</option>"""

				else:
					print """<option value = '""" + share_path + """'>""" + share_1 + """ - """ + share_path + """</option>"""
		print """		</select></form>
		</td></tr></table>"""

		append_mode = '';

		if (querystring.find('pacl') > 0):
			share_path = common_methods.getsubstr(querystring, '&pacl=', '&');

		if (share_path != ''):
			if (share_path.find('/storage/') < 0):
				share_path = '/storage/' + share_path;

			append_mode = common_methods.get_appendmode(share_path);

		if (log_path != check_pacl and append_mode != 'a'):
			print """<form name = 'access_control_form' method = 'POST'>
			<table width = "685" cellspacing = "0" cellpadding = "0" name = 'disp_tables' id = '""" + set_id + """' style = 'display: """ + share_acl_style + """; border-collapse: collapse; """ + blurstyle + """;' class = 'outer_border' border = '0'>
				<tr>
					<td height = "33px" width = "8" align = "left">
						<img src = "../images/rightside_left.jpg" width = "8" height = "33" />
					</td>
					<td width = "669" height = "33px" align = "left" valign = "middle" class = "right_bg rightsidemenuheading">
						<!--<a class = 'link' href = 'access_control_settings_help.php' onclick = "window.open('access_control_settings_help.php', 'help', 'location = no, height = 500, width = 600, scrollbars = 1'); return false;"></a>-->
						<div id="item_2" class="item">         
			"""+image_icon+""" ACL Settings
			<div class="tooltip_description" style="display:none" title="Access Control Settings">
				<span>This gives information about the resources that are being used by the system.</span><br/><br/>
				<table border="0">
				<tr class="spaceUnder">
				<td valign="top" align="left"><strong style="color:#b2b2b2; padding:0px 2px 0px 2px;">ACL:</strong></td>
				<td>Form here you can specify User and group level access to sub folders and files inside a shared folder.  All you have to do is to select the file/folders and then select the users from the ‘Available Users’ column and move them to ‘Authorized users’ column. Once added you can one by one set the permissions for the users.</td>
				</tr>
				</table>
				</div></div>

					</td>
					<td height = "33px" width = "8" align = "right">
						<img src = "../images/rightside_right.jpg" />
					</td>
				</tr>"""
			print """		<tr>
					<td colspan = "3" align = "left" valign = "top">
					<table width = "685" border = "0" cellspacing = "0" cellpadding = "0">
					<tr>
					<td class = "table_heading" height = "70px" valign = "middle" colspan = '2'>
						Contents:
					</td>
					<td class = "table_heading" height = "70px" valign = "middle" colspan = '2' align = 'right'>
					</td>
				</tr>
				<tr>
					<td class = "table_heading" valign = "middle" colspan = '8' align = 'center'>"""
			print """
				<!-- create 3 iframes each for files and folder structure, users and groups, user permissions -->
				<!-- first iframe is for file/folder structure -->
				<iframe width = '99.9%' frameborder = 0 name = 'directories' id = 'id_contents' src = 'show_dir1.py?share=""" + share_1 + """&path=""" + path_acl + """&spath=""" + path_acl + """&dd=""" + disabled + """' style = 'border: 1px solid #BDBDBD; font: 12px Arial white;' class = 'textbox' onload = 'return set_size();'></iframe>"""
			print """			<input type = 'hidden' name = 'hid_dir_file'>
					</td>
				</tr>
				<tr>
					<td class = "table_heading" height = "70px" valign = "middle" colspan = '8' align = 'center'>
						<input class = 'input' type = 'text' readonly name = 'selected_file' style = 'width: 99%;' value = '""" + path_acl + """' onchange = 'return showalert();' >
					</td>
				</tr>
				<tr>
					<td class = "table_heading" valign = "middle" colspan = '3'>
						<BR>Users & Groups:<BR>
						<!-- second iframe is for users and groups for assigning users to a particular share -->
						<iframe frameborder = 0 name = 'users_groups_frame' id = 'id_users_list' src = 'users_groups.py?aclpath=""" + path_acl + """&dd=""" + disabled + """' style = 'border: 1px solid #BDBDBD; font: 12px Arial white;' class = 'textbox' onload = 'return set_size();'></iframe>
					</td>
					<td class = "table_heading" valign = "middle" colspan = '3'>
						<BR>Permissions:<BR>
						<!-- third iframe is for showing permission options -->
						<iframe frameborder = '0' name = 'user_permissions' id = 'id_perms_list' src = 'user_permissions.py?dd=""" + disabled + """' style = 'border: 1px solid #BDBDBD; font: 12px Arial white;' class = 'textbox' onload = 'return set_size();'></iframe>
					</td>
				</tr>
				<!--<tr>
					<td class = "table_heading" height = "70px" valign = "middle" align = 'right' colspan = '3'>
						<input class = 'input1' type = 'button' name = 'reload' value = 'Get authorized users' title = 'Get granted users' onclick = 'parent.users_groups_frame.location.reload(true);'>
					</td>
				</tr>-->
				<tr>
					<td colspan = '4'>
						<input type = 'hidden' name = 'users_groups' style = 'width: 100%;'>
					</td>
				</tr>
				<tr>
					<td align = 'right' colspan = '8'>
						<BR><!--<input class = 'input1' type = 'button' name = 'action_but' value = 'Apply' onclick = 'return validate_access_control_form();' >-->
							<span style="margin-left: 54%;" ><span id="button-one"><button type = 'button' name="action_but" value="Apply" onclick ="return validate_access_control_form();" style = 'width:65px; background-color:#E8E8E8; border:none; float: right;font-size: 86%; ' title="Apply\" """ + disabled + """><a style="font-size:85%;">Apply</a></button></span></span>
						<input type = 'hidden' name = 'proceed_page' value = 'proceed'>
						<input type = 'hidden' name = 'hid_share' value = ''>
						<input type = 'hidden' name = 'hid_comment' value = ''>
						<input type = 'hidden' name = 'hid_path' value = ''>
						<input type = 'hidden' name = 'hid_users[]'>
						<input type = 'hidden' name = 'hid_page' value = ''>
					</td>
				</tr>
			</table>
			</form>
			</td>
			</tr>
			</table>
			"""

		else:
			print """<table width = "685" cellspacing = "0" cellpadding = "0" name = 'disp_tables' id = '""" + set_id + """' style = 'display: """ + share_acl_style + """; border-collapse: collapse;' class = 'outer_border' border = '0'><tr><td>"""

			print common_methods.show_acl_error;

			print """</td></tr></table>"""
	except Exception as e:
		disp_except.display_exception(e);

else:
	commands.getoutput('sudo rm -rf /tmp/getusers');

	print """
	<table width = "685" cellspacing = "0" cellpadding = "0" name = 'disp_tables' id = 'id_acl_settings' style = 'display: """ + share_acl_style + """; border-collapse: collapse; """ + blurstyle + """;' class = 'outer_border' border = '0'>
		<tr>
			<td align = 'center'>"""
	print common_methods.acl_message;
	print """	</td>
		</tr>
	</table>"""
