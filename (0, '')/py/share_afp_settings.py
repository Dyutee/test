#!/usr/bin/python
import cgitb, commands, sys, share_details, common_methods, os, cgi, header, string

################################################################## NEW CODE ##################################################################

selected_share = share_details.share
selected_share_path  = share_details.path

sys.path.append('/var/nasexe/python/')
from fs2global import *
import afp

#all_afp_shares = afp.get_all_shares()
#print all_afp_shares
#delete_all_shares = afp.delete_all_shares()

status=afp_status()                                ####### Check the Status of AFP #######                     

if(status['desc']!='INFO: afpd is running.'):      ####### If AFP is not running #######
	status=afp_start()                         ####### then Start AFP        #######

afp_conf_file_path = afp_conf_file
filetowrite = afp_share_conf_dir+selected_share;

if(header.form.getvalue('action_but')):
	afp_enable = header.form.getvalue('use_afp')

	if(afp_enable == 'on'):

		afp_read_only = header.form.getvalue('read_only')
		permission_type = header.form.getvalue('afp_priv')
		afp_advance = header.form.getvalue('advanced_per')
		afp_host_allow = header.form.getvalue('host_allow')
		afp_host_deny = header.form.getvalue('host_deny')
		afp_umask = header.form.getvalue('umask')
		afp_file_perm = header.form.getvalue('file_perm')
		afp_dir_perm = header.form.getvalue('dir_perm')
		afp_grant_users = header.form.getvalue('afp_grant_users[]')
		afp_grant_groups = header.form.getvalue('afp_grant_groups[]')

		dict_value = {'afp_read_only':afp_read_only, 'permission_type':permission_type, 'afp_advance':afp_advance, 'afp_host_allow':afp_host_allow, 'afp_host_deny':afp_host_deny, 'afp_umask':afp_umask, 'afp_file_perm':afp_file_perm, 'afp_dir_perm':afp_dir_perm, 'afp_grant_users':afp_grant_users, 'afp_grant_groups':afp_grant_groups, 'selected_share':selected_share, 'selected_share_path':selected_share_path}

		afp.configure(dict_value)       ####### To configure AFP, call configure() function from afp_functions.py #######	
		print "<script>location.href = 'show_shares.py?s1=%s&act=share_afp_done&fl=output';</script>" % selected_share;
	else:
		entry_array = [];
		afp.unconfigure(selected_share) ####### To unconfigure AFP, call unconfigure() function from afp_functions.py #######
		print "<script>location.href = 'show_shares.py?s1=%s&act=share_afp_done&fl=output';</script>" % selected_share;

get_display_dict = afp.getstatus(selected_share, selected_share_path) # To get status of AFP, call getstatus() function from afp_functions.py #

guest_checked = get_display_dict['guest_checked']
afp_readonly_checked = get_display_dict['afp_readonly_checked']
afp_checked = get_display_dict['afp_checked']
priv_checked = get_display_dict['priv_checked']
afp_users_style = get_display_dict['afp_users_style']
advanced_checked = get_display_dict['advanced_checked']
advanced_display_style = get_display_dict['advanced_display_style']
host_allow_val = get_display_dict['host_allow_val']
host_deny_val = get_display_dict['host_deny_val']
umask_val = get_display_dict['umask_val']
file_perm_val = get_display_dict['file_perm_val']
dir_perm_val = get_display_dict['dir_perm_val']
split_vul1 = get_display_dict['split_vul1']
afp_style = get_display_dict['afp_style']

################################################################### END ######################################################################

all_users_list  = '';
all_groups_list = '';
afp_all_users_array = ''
afp_all_groups_array = ''

# create a userslist groupslist from the method get_users_string() defined in common_methods.py
all_users_list  = common_methods.get_users_string();
all_groups_list = common_methods.get_groups_string();

# if userslist is not empty
if (all_users_list['id'] == 0):
	if (all_users_list['users'] != ''):
		afp_all_users_array  = all_users_list['users'];

# if groupslist id not empty
if (all_groups_list['id'] == 0):
	if (all_groups_list['groups'] != ''):
		afp_all_groups_array = all_groups_list['groups'];

# copy the share name from share_details.py
share_1 = share_details.share;
path_1  = share_details.path;


# get the existing values set for afp
afp_share_line_command = 'sudo grep "^' + share_1 + ':" /var/www/global_files/afp_param_global_file';
afp_share_line = commands.getoutput(afp_share_line_command);

afp_users  = '';
afp_groups = '';

# default values for afp parameters
use_afp = 'off';
afp_readonly = '';
afp_priv   = '';

# retreive the afp parameters from afp line
if (afp_share_line != ''):
	temp = [];
	temp = afp_share_line.split(':');

	afp_share    = temp[0];
	use_afp      = temp[1];
	afp_readonly = temp[2];
	afp_priv     = temp[3];
	afp_users    = temp[4];
	afp_groups   = temp[5];

	if (afp_groups == '@'):
		afp_groups = '';		

if (afp_priv == 'valid_user'):
	afp_advanced_style = 'none'

elif (afp_priv == 'guest' or afp_priv == ''):
	afp_advanced_style = 'none'
	

ads_domain_name = 'EXAMPLE';

# create arrays of already assigned users and groups
afp_users_array  = afp_users.split(',');
afp_groups_array = afp_groups.split(',');

# create corresponding dropdowns to be displayed in assigned user/groups dropdown list box
afp_users_dropdown = '';
afp_groups_dropdown = '';

# if the user has selected the 'authenticated user' option, then read the assigned users/groups array and
# remove the elements of the local afp users array 
print """
		<form name = 'afp_form' method = 'POST' action='' onsubmit = 'return validate_share_afp();' >
			<table width = "685" border = "0" cellspacing = "0" cellpadding = "0" name = 'disp_tables' id = 'id_afp_settings' style = 'display:  """ + share_details.share_afp_style + """; """ + share_details.stylestring + """;'>
			<tr>
				<td>
			<table width = '100%'>
				<tr>
					<td height = "33px" width = "8" align = "left">
						<img src = "../images/rightside_left.jpg" width = "8" height = "33" />
					</td>
					<td width = "669" height = "33px" align = "left" valign = "middle" class = "right_bg rightsidemenuheading">
						<a class = 'link' href = 'afp_help.php' onclick = "window.open('afp_help.php', 'help', 'location = no, height = 500, width = 600, scrollbars = 1'); return false;">""" + common_methods.getimageicon()
print  """ </a>
						AFP settings
					</td>
					<td height = "33px" width = "8" align = "right">
						<img src = "../images/rightside_right.jpg" />
					</td>
				</tr>
				<tr>
					<td colspan = '3'>
						<input type = 'checkbox' name = 'use_afp' onclick = 'return show_afp_params();' """ + afp_checked + """ """ + share_details.alldisabled + """>&nbsp;<B>Enable AFP</B>
					</td>
				</tr>
			</table>
				<BR><div width = '100%' id = 'afp_params' style = 'display: """+afp_style+""";'>
				<table width = '100%' style = 'font-weight: bold;'>
					<tr>
						<td>
							<input type = 'checkbox' name = 'read_only' """ + afp_readonly_checked + """ """ + share_details.alldisabled + """>&nbsp;<B>Read only</B><BR>
						</td>
					</tr>
					<tr>
						<td>
							<BR><B>User access permissions</B>:<BR>
							<input type = 'radio' name = 'afp_priv' value = 'guest'  guest_checked  onclick = 'return show_afp_users_groups();' """ + guest_checked + """ """ + share_details.alldisabled + """><B>Guest</B><BR>
							<input type = 'radio' name = 'afp_priv' value = 'valid_user' onclick = 'return show_afp_users_groups();' """ + priv_checked + """ """ + share_details.alldisabled + """><B>Authenticated User</B><br/>
						</td>
					</tr>

					<tr>
					<td></td>
					</tr>

					<tr>
						<td>


							<div  width = '100%' id = 'afp_users_list' style = 'display:  """ + afp_users_style + """;' align = 'center'>"""
							
# users can authenticate to afp only when authentication method is set to local authentication
if (share_details.connstatus == 'nis is running'):
	 print """<table width = '100%' align = 'center' style = 'color: darkred;'>
                <tr>
                        <td align = 'center'>
                                Authentication is set to NIS!
                        </td>
                </tr>
                </table>"""


else:
	#print afp_all_users_array
	#print "<br/>"
	#print split_vul1	
	#print "<br/>"
	afp_all_users_array = list(set(afp_all_users_array) - set(split_vul1))
	#print afp_all_users_array
	afp_all_groups_array = ["@"+x for x in afp_all_groups_array]
	afp_all_groups_array = list(set(afp_all_groups_array) - set(split_vul1))

	print """							
	<table width = '100%'>
		<tr>
			<td colspan = '2'>
				<BR><B>Users list:</B>
			</td>
		</tr>
		<tr>
			<td>
				Available:
			</td>
			<td>
				Authorized:
			</td>
		</tr>
		<tr>
			<td>
					<select class = 'input' style = 'width: 200px; height: 150px;' id = 'afp_available' name = 'avail_users' multiple onclick = "return afp_move_users(this.form.afp_available, this.form.afp_granted, '1');\" """ + share_details.alldisabled + """>"""
		

	for local_users in afp_all_users_array:
		local_users_to_check = local_users;

		if (len(afp_users_array) > 0):
			print """<option value = '""" + local_users + """' title = '""" + local_users + """'>""" + local_users + """</option>"""
				
	print """</select>
			</td>
			<td>
				<select class = 'input' style = 'width: 200px; height: 150px;' id = 'afp_granted' name = 'afp_grant_users[]' multiple onclick = "return afp_move_users(this.form.afp_granted, this.form.afp_available, '2');\" """ + share_details.alldisabled + """>"""
				
	for u_val in split_vul1:
		if(u_val[0]!='@'):
			print """<option value = '""" + u_val + """' selected title = '""" + u_val + """'>""" + u_val + """</option>"""	
	#print afp_users_dropdown 
				
	print """				</select>
			</td>
		</tr>
		<tr>
			<td></td>
		</tr>
		<tr>
		<td colspan = '2'>
			<BR><B>Groups list:</B>
		</td>
	</tr>
	<tr>
		<td>
			Available:
		</td>
		<td>
			Authorized:
		</td>
	</tr>
	<tr>
		<td>
			<select class = 'input' style = 'width: 200px; height: 150px;' id = 'afp_available_groups' name = 'avail_groups' multiple onclick = "return afp_move_groups(this.form.afp_available_groups, this.form.afp_granted_groups, '1');\" """ + share_details.alldisabled + """>"""
			
	for local_groups in afp_all_groups_array:
		local_groups_to_check = '@' + local_groups;

		print """<option value = '""" + local_groups + """' title = '""" +  local_groups + """'>""" + local_groups.replace('@', '') + """</option>""";
			
	print """			</select>
		</td>
		<td>
			<select class = 'input' style = 'width: 200px; height: 150px;' id = 'afp_granted_groups' name = 'afp_grant_groups[]' multiple onclick = "return afp_move_groups(this.form.afp_granted_groups, this.form.afp_available_groups, '2');\" """ + share_details.alldisabled + """>"""
			
	for g_val in split_vul1:
                if(g_val[0]=='@'):
                        print """<option value = '""" + g_val + """' selected title = '""" + g_val + """'>""" + g_val.replace('@', '') + """</option>"""
	#print afp_groups_dropdown; 
			
	print """		</select>
		</td>
	</tr>
			</table>
			
			
			</div>
			</td>
		</tr>
					<tr>
                                                <td><br/>
                                                        <input type = 'checkbox' """+advanced_checked+""" name = 'advanced_per' onclick = 'return show_advance_per(this.checked);' """ + share_details.alldisabled + """>&nbsp;<B>Advance Permission</B><BR>
                                                </td>
                                        </tr>
<tr>
<td>

							<div  width = '100%' id = 'afp_advanced_list' style = 'display:"""+advanced_display_style+"""; margin:20px 0 0 0;' align = 'center'>
<table width = '100%' style="margin:0 0 0 40px;">
<tr>
	<td>Host Allow</td>
	<td><input type='text' name='host_allow' id='host_allow' value='"""+host_allow_val+"""' """ + share_details.alldisabled + """/></td>
</tr>

<tr>
	<td>Host Deny</td>
	<td><input type='text' name='host_deny' id='host_deny' value='"""+host_deny_val+"""' """ + share_details.alldisabled + """/></td>
</tr>

<tr>
        <td>Umask</td>
        <td><input type='text' name='umask' id='umask' value='"""+umask_val+"""' """ + share_details.alldisabled + """/></td>
	<input type='hidden' name='file_perm' value='"""+file_perm_val+"""' />
	<input type='hidden' name='dir_perm' value='"""+dir_perm_val+"""' />
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
print common_methods.afp_wait ;
print """		</td>
			<td align = 'right'>
				<BR><!--<input class = 'input1' type = 'submit' name = 'action_but' value = 'Apply' >-->
				
				 <span style="margin-left: 54%;" ><span id="button-one"><button type = 'submit' name="action_but" value="Apply" style = 'width:65px; background-color:#E8E8E8; border:none; float:none;font-size: 86%; ' title="Apply\" """ + share_details.alldisabled + """><a style="font-size:85%;">Apply</a></button></span></span>

				<input type = 'hidden' name = 'proceed_page' value = 'proceed'>
				<input type = 'hidden' name = 'hid_share' value = '"""+share_1+"""'>
				<input type = 'hidden' name = 'hid_share_path' value = '"""+path_1+"""'>
				<input type = 'hidden' name = 'hid_connection_status' value = '"""+share_details.connstatus+"""'>
			</td>
		</tr>
		<input type = 'hidden' name = 'hid_session_user' value = ' session_user '>
	</table>
	</td>
	</tr>
	</table>
	</form>"""
