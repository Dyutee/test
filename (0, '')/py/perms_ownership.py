#!/usr/bin/python
import cgitb, sys, header, common_methods, os, commands
cgitb.enable()

sys.path.append('/var/nasexe/python/');
import tools;
from tools import acl;

from fs2global import *

sys.path.append('../modules/');
import disp_except;

userslength = 0;
groupslength = 0;

all_users_list  = common_methods.get_users_string();
all_groups_list = common_methods.get_groups_string();

if (all_users_list['id'] == 0):
        smb_all_users_array  = all_users_list['users'];
        userslength       = len(smb_all_users_array);

if (all_groups_list['id'] == 0):
        smb_all_groups_array = all_groups_list['groups'];
        groupslength      = len(smb_all_groups_array);

usersfilesarray  = [];
groupsfilesarray = [];

alldisabled = '';
connstatus = common_methods.conn_status();

users_style  = 'none';
groups_style = 'none';

users_list_style = 'none';
groups_list_style = 'none';

ads_separator = '';
ads_separator = tools.get_ads_separator();

domain = '';
domainname = '';

share_name = '';
share_path = '';
ug = '';

domainsarray = [];

domainsarray = common_methods.get_all_domains();

querystring = os.environ['QUERY_STRING'];

assusr = 'root';
assgrp = 'root';
disp_share_path = '';

if (querystring.find('share_name=') >= 0):
        if (querystring.find('&ro=') > 0):
                share_name = querystring[querystring.find('share_name=') + len('share_name='):querystring.find('&ro=')];

        elif (querystring.find('&dom=') > 0):
                share_name = querystring[querystring.find('share_name=') + len('share_name='):querystring.find('&dom=')];

        else:
                share_name = querystring[querystring.find('share_name=') + len('share_name='):];

	if (querystring.find('&ug=') > 0):
		ug = querystring[querystring.find('&ug=') + len('&ug='):querystring.find('&share_name')];

#print share_name;

if (share_name != ''):
	share_path = common_methods.get_share_path('^' + share_name + ':');
	
	if (share_path != 1):
		disp_share_path = share_path.replace('/storage/', '');

	else:
		share_path = '';

try:
	if (share_path != ''):
		get_ownership_status = acl.get_acl(share_path);

		if (get_ownership_status != {}):
			assusr     = get_ownership_status['owner'];
			assgrp     = get_ownership_status['group'];
			share_path = get_ownership_status['path'];


	else:
		common_methods.sendtologs('ERROR', 'Get Share Path', 'UI', '"perms_ownership.py, common_methods.get_share_path()", Could not get path');

	usersfiletoread  = 'ownssearchusersfile.txt';
	groupsfiletoread = 'ownssearchgroupsfile.txt';

        assusrfile = 'ownsassusersfile';
        assgrpfile = 'ownsassgroupsfile';

	assusrarray = [];
        assgrparray = [];

	users_from_list  = [];
	groups_from_list = [];

	get_users_string = '';
	get_groups_string = '';

	usersarray  = [];
	groupsarray = [];

	if (ug != ''):
		domainname = querystring[querystring.find('&dom=') + len('&dom='):];
		domainname = domainname.strip();

                assusrarray = common_methods.read_file(assusrfile);
                assgrparray = common_methods.read_file(assgrpfile);

		users_style = 'table';
		groups_style = 'table';

		if (len(assusrarray) > 0):
			for i in assusrarray:
				assusr = i;

		if (len(assgrparray) > 0):
			for i in assgrparray:
				assgrp = i;

		if (assusr != ''):
			assusr = assusr.strip();
			groups_style = 'table';

		if (assgrp != ''):
			assgrp = assgrp.strip();
			users_style = 'table';
		if (get_ownership_status != {}):#Edit this line and add a condition #
			if (assusr == ''):
				assusr = get_ownership_status['owner'];

			if (assgrp == ''):
				assgrp = get_ownership_status['group'];

		if (ug == 'users'):
			usersarray  = common_methods.read_file(usersfiletoread);
			usersarray.sort();
			userarray = list(set(usersarray));

			users_list_style = 'block';
			users_style = 'table';

			groups_list_style = 'none';
			groups_style = 'none';

			if (len(usersarray) > 0):
				users_style = 'table';

				for users in usersarray:
					get_users_string += '<option value = "' + users + '">' + users + '</option>';

		elif (ug == 'groups'):
			groupsarray = common_methods.read_file(groupsfiletoread);
			groupsarray.sort();
			groupsarray = list(set(groupsarray));

			users_list_style = 'block';
			users_style = 'none';

			groups_list_style = 'block';
			groups_style = 'table';

			if (len(groupsarray) > 0):
				groups_style = 'table';

				for groups in groupsarray:
					get_groups_string += '<option value = "' + groups + '">' + groups + '</option>';

	#import left_nav;
        print
        print """
	<form name="chang_owner_form" method="post" action="change_ownership.py">
	        <table style="width:90%; margin-left: 5%;" border = '0'>
	<tr>
		<td style="color:#585858; font-weight:600;">
			Log Path:
		</td>
		<td>
			<input class = 'textbox' type = 'text' readonly name = 'acl_path' style = 'width: 90%;' value = '""" + disp_share_path + """'>
		</td>
	</tr>
	<tr>
		<td height = '35px'></td>
	</tr>
        <tr>
                <td width = '20%' style="color:#585858; font-weight:600;">
			Assigned to User:
		</td>
		<td>
		<input type = 'text' class = 'textbox' name = 'assd_user' value = '""" + assusr + """' style = 'width: 60%;margin-top:4%;' />
		<a href = '#' onclick = 'document.getElementById("id_set_owner").style.display = "table"; document.getElementById("id_set_group").style.display = "none";' style = 'text-decoration: underline;'>Change USER</a><BR><BR></td></tr>
		<tr><td colspan = '2'>
		<div id = 'id_set_owner' style = 'margin-left: 8%; width: 90%; border: 0px solid #BDBDBD; display: """ + users_style + """;'>
		<b style ="color:darkred">Choose a domain:</b> <select name = 'udomainslist' onchange = 'document.chang_owner_form.hid_domain.value = document.chang_owner_form.udomainslist.value;'>"""
	if (len(domainsarray) > 0):
		for domains in domainsarray:
			domains = domains.strip();

			users_file_to_count  = user_files_dir + domains + '-users.txt';
	                groups_file_to_count = user_files_dir + domains + '-groups.txt';

        	        usersfilesarray  = common_methods.read_file(users_file_to_count);
                	groupsfilesarray = common_methods.read_file(groups_file_to_count);

			if (domains == domainname):
				print """<option value = '""" + domains + """-""" + str(len(usersfilesarray)) + """-""" + str(len(groupsfilesarray)) + """' selected>""" + domains + """ (""" + str(len(usersfilesarray)) + """, """ + str(len(groupsfilesarray)) + """)</option>""";

			else:
				print """<option value = '""" + domains + """-""" + str(len(usersfilesarray)) + """-""" + str(len(groupsfilesarray)) + """'>""" + domains + """ (""" + str(len(usersfilesarray)) + """, """ + str(len(groupsfilesarray)) + """)</option>""";

	print """</select><BR>

		<input id = 's_sssavailable' name = 'ads_user_text' type="text" class = 'input' value = '' onclick = 'document.getElementById("s_available").style.display = "none"; document.getElementById("s_available_groups").style.display = "none";' style = 'width: 40%;'><input class = 'input1' type = 'button' name = 'getusers' value = 'Check'  onclick = 'return get_user_suggestions("", document.getElementById("id_groups_list").value, "", "", document.chang_owner_form.udomainslist.value, this.form.s_sssavailable.value, "users", document.chang_owner_form.hid_separator.value, \"""" + share_name + """", "ownership", \"""" + str(userslength) + """", \"""" + connstatus + """");' """ + alldisabled + """ >"""
        print """<select id = 'id_users_list' name='ass_user' onchange = 'document.chang_owner_form.assd_user.value = document.chang_owner_form.ass_user.value; document.getElementById("id_set_owner").style.display = "none";' style = 'display: """ + users_list_style + """;'>
		<option value = ''>Choose a USER</option>"""
	print get_users_string;
        print """               </select></div>
		</td>
                <td>
                </td>
        </tr>
	<tr>
		<td height = '35px'></td><td></td>
	</tr>
        <tr>
                <td style="color:#585858; font-weight:600;width:23%;">
			Assigned to Group:
		</td>
		<td>
		<input type = 'text' class = 'textbox' name = 'assd_group' value = '""" + assgrp + """' style = 'width: 60%;margin-top:4%;' />
		<a href = '#' onclick = 'document.getElementById("id_set_group").style.display = "table"; document.getElementById("id_set_owner").style.display = "none";' style = 'text-decoration: underline;'>Change GROUP</a><BR><BR></td></tr>
		<tr><td colspan = '2'>
		<div id = 'id_set_group' style = 'margin-left: 8%; width: 90%; border: 0px solid #BDBDBD; display: """ + groups_style + """;'>
		<b style ="color:darkred">Choose a domain:</b> <select name = 'gdomainslist' onchange = 'document.chang_owner_form.hid_domain.value = document.chang_owner_form.gdomainslist.value;'>"""
	if (len(domainsarray) > 0):
		for domains in domainsarray:
			domains = domains.strip();

                        users_file_to_count  = user_files_dir + domains + '-users.txt';
                        groups_file_to_count = user_files_dir + domains + '-groups.txt';

                        usersfilesarray  = common_methods.read_file(users_file_to_count);
                        groupsfilesarray = common_methods.read_file(groups_file_to_count);

			if (domains == domainname):
				print """<option value = '""" + domains + """-""" + str(len(usersfilesarray)) + """-""" + str(len(groupsfilesarray)) + """' selected>""" + domains + """ (""" + str(len(usersfilesarray)) + """, """ + str(len(groupsfilesarray)) + """)</option>""";

			else:
				print """<option value = '""" + domains + """-""" + str(len(usersfilesarray)) + """-""" + str(len(groupsfilesarray)) + """'>""" + domains + """ (""" + str(len(usersfilesarray)) + """, """ + str(len(groupsfilesarray)) + """)</option>""";

	print """</select><BR>
		<input id = 's_ssavailable_groups' name = 'ads_group_text' type="text" class = 'input' value = '' onclick = 'document.getElementById("s_available_groups").style.display = "none"; document.getElementById("s_available").style.display = "none";' style = 'width: 40%;'><input class = 'input1' type = 'button' name = 'getgroups' size ="10" value = 'Check' onclick = 'return get_user_suggestions(document.getElementById("id_users_list").value, "", "", "", document.chang_owner_form.gdomainslist.value, this.form.s_ssavailable_groups.value, "groups", document.chang_owner_form.hid_separator.value, \"""" + share_name + """", "ownership", \"""" + str(groupslength) + """", \"""" + connstatus + """");' """ + alldisabled + """ />
                <select id = 'id_groups_list' name = 'ass_group' onchange = 'document.chang_owner_form.assd_group.value = document.chang_owner_form.ass_group.value; document.getElementById("id_set_group").style.display = "none";' style = 'display: """ + groups_list_style + """;'>
		<option value = ''>Choose a GROUP</option>"""
	print get_groups_string;
        print """
                </select></div>
		</td>
        </tr>

        </table>
<br/>
        <p style="margin-left: 5%;"><input type="checkbox" name="inherit_ownership"><b style ="color:darkred">Inherit Ownership to sub-folders</b></p>

        <input type='hidden' name='hid_s_name' value='""" + share_name + """' />
        <input type='hidden' name='hid_s_path' value='""" + str(share_path) + """' />
	<div style="float: right; margin-top: -6%;">
        <button class="button_example" type="submit" name = 'reset_ownership'  id = 'reset_ownership' value = 'ResetOwner'  style="float:right; margin:20px 10px 10px 0;" onclick="return confirm ('Are you sure you want to Reset Ownership?');">Reset Ownership</button>
<button class="button_example" type="submit" name = 're_assign_ownership'  id = 're_assign_ownership' value = 'Apply'  style="float:right; margin:20px 10px 10px 0;">Re-assign</button>
</div>
	<input type = 'hidden' name = 'hid_separator' value = '""" + str(ads_separator) + """' />
	<input type = 'hidden' name = 'hid_domain' value = '' />
	</form>"""


except Exception as e:
	disp_except.display_exception(e);
