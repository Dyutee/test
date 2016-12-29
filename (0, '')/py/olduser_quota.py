#!/usr/bin/python
import commands, common_methods, os, sys

sys.path.append('../modules/');
import disp_except;

connstatus = common_methods.conn_status();

try:
	image_icon = common_methods.getimageicon();
	adsdomain    = '';

	if (connstatus == 'Join is OK'):
		adsdomaincommand = commands.getstatusoutput('wbinfo --own-domain');

		if (adsdomaincommand[0] == 0):
			adsdomain = adsdomaincommand[1];
			
			if (adsdomain != ''):
				adsdomain = adsdomain.strip();

	button_lable = 'Show Details';
	buttdisabled = 'disabled';

	user_quota_style   = 'none';
	search_quota_style = 'none';

	querystring = os.environ["QUERY_STRING"];

	response  = common_methods.getsubstr(querystring, '&act=', '&');

	use_manual = '';
	all_users_list  = '';
	all_groups_list = '';

	all_users_list  = common_methods.get_users_string();
	all_groups_list = common_methods.get_groups_string();

	all_users_array  = [];
	all_groups_array = [];

	ads_users_only_string  = '';
	ads_groups_only_string = '';

	full_users_string  = '';
	full_groups_string = '';

	ads_users_string  = '';
	ads_groups_string = '';

	user_message  = '';
	group_message = '';

	if (all_users_list['id'] == 0):
		if (connstatus == 'Join is OK'):
			checkusersfile  = commands.getstatusoutput('ls /tmp/adsusersfile');

			if (checkusersfile[0] == 0):
				all_users_array  = open('/tmp/adsusersfile', 'r');
				quotauserslength = common_methods.get_users_count();

		else:
			all_users_array  = all_users_list['users'];
			quotauserslength = len(all_users_array);

	if (all_groups_list['id'] == 0):
		if (connstatus == 'Join is OK'):
			checkgroupsfile = commands.getstatusoutput('ls /tmp/adsgroupsfile');

			if (checkgroupsfile[0] == 0):
				all_groups_array  = open('/tmp/adsgroupsfile', 'r');
				quotagroupslength = common_methods.get_groups_count();

		else:
			all_groups_array  = all_groups_list['groups'];
			quotagroupslength = len(all_groups_array);

	if (response == 'search_quota_done'):
		search_quota_style = 'table';
		user_quota_style   = 'none';

	if (response == 'user_quota_done'):
		user_quota_style   = 'table';
		search_quota_style = 'none';

	if (connstatus == 'Join is OK'):
		if (quotauserslength > 1000):
			user_message = '<BR><font color = \'darkred\' style = \'italic\'>Too many users.<BR>Type the beginning characters of the user name in the text box and click \'Get Users\' button.</font>';

		if (quotagroupslength > 1000):
			group_message = '<BR><font color = \'darkred\' style = \'italic\'>Too many groups.<BR>Type the beginning characters of the group name in the text box and click \'Get Groups\' button./font>';

	print common_methods.wait_for_response ;
	print """			<form name = 'user_quota' method = 'POST'>
					<table width = "685" border = "0" cellspacing = "0" cellpadding = "0" name = 'disp_tables' id = 'id_user_quota' style = 'font-weight: bold; display:  """ + user_quota_style + """;' class = 'outer_border'>
					<tr>
						<td height = "33px" width = "8" align = "left">
							<img src = "../images/rightside_left.jpg" width = "8" height = "33" />
						</td>
						<td width = "669" height = "33px" align = "left" valign = "middle" class = "right_bg rightsidemenuheading">
							<!--<a class = 'link' href = 'user_quota_help.php' onclick = "window.open('user_quota_help.php', 'help', 'location = no, height = 500, width = 600'); return false;">""" + common_methods.getimageicon() + """ </a>-->
						<div id="item_2" class="item" style="width: 14%;">         
                        """+image_icon+""" User Quota
                        <div class="tooltip_description" style="display:none" title="User Quota">
                                <span>This gives information about the resources that are being used by the system.</span><br/><br/>
                                <table border="0">
                                <tr class="spaceUnder">
                                <td valign="top" align="left"><strong style="color:#b2b2b2; padding:0px 2px 0px 2px;">Select Quota:</strong></td>
                                <td>Choose an option for User/Group for the quota to be assigned.</td>
                                </tr>
                                <tr class="spaceUnder">
                                <td valign="top" align="left"><strong style="color:#cccccc; padding:0px 2px 0px 2px;">Select user/group:</strong></td>
                                <td>Choose a user/group from the dropdown, and</td>
                             </tr>

                                <tr class="spaceUnder">
                                <td valign="top" align="left"><strong style="color:#cccccc; padding:0px 2px 0px 2px;">Quota Size:</strong></td>
                                <td>Enter the size you want to allocate space for the selected user/group.</td>
                             </tr>

                                </table>
                                </div></div>

						</td>
						<td height = "33px" width = "8" align = "right">
							<img src = "../images/rightside_right.jpg" />
						</td>
					</tr>
					<tr>
						<td colspan = "3" align = "left" valign = "top">
							<table width = "685" cellspacing = "0" cellpadding = "0" border = '0'>
							<tr>
								<td width = "172" class = "table_heading" height = "70px" valign = "middle">
									<input type = 'radio' name = 'user' value = 'user' onclick = 'return show_users_list();' checked>Users
								</td>
								<td class = "table_content" height = "70px" valign = "middle" colspan = "3">"""
							
	if (quotauserslength == 0):
		print 'No users!';

	elif (quotauserslength > 1000):
		print """<input id = 'quota_available' name = 'ads_user_text' type="text" class = 'input' value = '' oninput = 'generate_user_list(document.getElementById("quota_available"), document.getElementById("quota_autosuggest"), \"""" + ads_users_only_string + """", "users", "user_quota");' onclick = 'document.getElementById("quota_autosuggest").style.display = "none";' style = 'width: 50%;'> <input id = 'id_ubutton' class = 'input1' type = 'button' name = 'move' value = '>'  onclick = "move_quota_text_to_dropdown(this.form.quota_available, this.form.id_user_list, '1');\" >""";

        	print """<div id="suggest" style="visibility:hidden;border:#000000 1px solid;width:150px;"></div>
                                                                <select class = 'input' style = 'position: absolute; display: none; width: 300px; height: 300px;' id = 'quota_autosuggest' name = 'avail_users' multiple onclick = 'return set_user(this.form.quota_available, this.form.quota_autosuggest, this.form.quota_autosuggest.value);' onkeydown = 'return get_key();' >"""
	        print """</select>"""
		print """<select id = 'id_user_list' class = 'input' name = 'user_list[]' style = 'display: table; width: 500px; height: 150px;' multiple></select>"""

	else:
		print """<select id = 'id_user_list' class = 'input' name = 'user_list[]' style = 'display: table; width: 500px; height: 150px;' multiple>"""
							
		for local_users in all_users_array:
			if (local_users != ''):
				if (connstatus == 'Join is OK'):
					local_users = common_methods.replace_chars(local_users, 'texttochar');

					useridcommand = commands.getstatusoutput('wbinfo --user-info="' + local_users + '"');

					if (useridcommand[0] == 0):
						local_usersline = useridcommand[1].strip();
						
						temp = [];
						temp = local_usersline.split(':');

						local_users_id = temp[2];

				if (local_users.find('\\') > 0):
					users_only = local_users[local_users.find('\\') + 1:];

				elif (local_users.find('+') > 0):
					users_only = local_users[local_users.find('+') + 1:];

				else:
					users_only = local_users;
			
				if (connstatus == 'Join is OK'):
					print """<option value = '""" + local_users_id + """'>""" + users_only + """</option>"""

				else:
					print """<option value = '""" + local_users + """'>""" + users_only + """</option>"""

		print """</select>"""
								
	print """							</td>
							</tr>
							<tr>
								<td width = "172" class = "table_heading" height = "70px" valign = "middle">
									<input type = 'radio' name = 'user' value = 'group' onclick = 'return show_users_list();'>Groups&nbsp;&nbsp;&nbsp;
								</td>
								<td class = "table_content" height = "70px" valign = "middle" colspan = "3">"""
	if (quotagroupslength == 0):
		print 'No groups!';
								
	elif (quotagroupslength > 1000):
		print """<input id = 'quota_available_groups' name = 'ads_group_text' type="text" class = 'input' value = '' oninput = 'generate_user_list(document.getElementById("quota_available_groups"), document.getElementById("g_quota_autosuggest"), \"""" + ads_groups_only_string + """", "groups", "user_quota");' onclick = 'document.getElementById("g_quota_autosuggest").style.display = "none";' style = "display: none; width: 50%;"><input id = 'id_gbutton' class = 'input1' type = 'button' name = 'move' value = '>'  onclick = "move_quota_group_to_dropdown(this.form.quota_available_groups, this.form.id_group_list, '1');\" style = "display: none;">""";

        	print """<div id="suggest" style="visibility:hidden;border:#000000 1px solid;width:150px;"></div>
                                                                <select class = 'input' style = 'display: none; width: 300px; height: 300px;' id = 'g_quota_autosuggest' name = 'avail_groups' multiple onclick = 'return set_user(this.form.quota_available_groups, this.form.g_quota_autosuggest, this.form.g_quota_autosuggest.value);' onkeydown = 'return get_key();' >"""
	        print """</select>"""

		print """<select id = 'id_group_list' class = 'input' name = 'group_list[]' style = 'display: none; width: 500px; height: 150px;' multiple></select>"""

	else:
		print """<select id = 'id_group_list' class = 'input' name = 'group_list[]' style = 'display: none; width: 500px; height: 150px;' multiple>"""
				
		for local_groups in all_groups_array:
			if (local_groups != '' and local_groups != 'USER'):
				if (connstatus == 'Join is OK'):
					"""
					local_groups = local_groups.replace('[AND]', '&');
					local_groups = local_groups.replace('[HASH]', '#');
					local_groups = local_groups.replace('[DOLLAR]', '$');
					"""

					groupidcommand = commands.getstatusoutput('wbinfo --group-info="' + local_groups + '"');

					if (groupidcommand[0] == 0):
						local_groups_line = groupidcommand[1];

						temp = [];
						temp = local_groups_line.split(':');

						local_groups_id = temp[2];

				if (local_groups.find('\\') > 0):
					groups_only = local_groups[local_groups.find('\\') + 1:];

				elif (local_groups.find('+') > 0):
					groups_only = local_groups[local_groups.find('+') + 1:];

				else:
					groups_only = local_groups;

				if (connstatus == 'Join is OK'):
					print """<option value = '""" + local_groups_id + """'>""" + groups_only + """</option>""";

				else:
					print """<option value = '""" + local_groups + """'>""" + groups_only + """</option>""";
		
		print """</select><BR><BR>"""

	print """							</td>
							</tr>
							<tr>
								<td width = "172" class = "table_heading" height = "70px" valign = "middle">
									Size
								</td>
								<td class = "table_content" height = "70px" valign = "middle" colspan = "3">
									<input class = 'input' type = 'text' name = 'disk_size' style = 'width: 100px;'> GB
								</td>
							</tr>
							<tr>
								<td colspan = '5' align = 'right' width = '685'>
									<BR><!--<input class = 'input1' type = 'button' name = 'action_but' value = 'pply' onclick = 'return validate_user_quota_form();'>-->
										
		
		<!--<input class = 'input1' type = 'button' name = 'cancel' value = 'Cancel' onclick = 'location.href = "main.php?page=share";'>-->
		                                            <span style="margin-right:2%;"><span id="button-one"><button type = 'button'  name = 'cancel' value = 'Cancel' onclick = "location.href='main.py?page=share';" style = 'width:73px; background-color:#E8E8E8; border:none; float:right;font-size: 100%; ' title="Cancel"><a style="font-size:75%;width:100%;"  >Cancel</a></button></span>	
							<span style="margin-left: 54%;" ><span id="button-one"><button type = 'button' name="action_but" value="Apply" onclick ="return validate_user_quota_form();" style = 'width:65px; background-color:#E8E8E8; border:none; float:right;font-size: 86%; ' title="Apply"><a style="font-size:85%;">Apply</a></button></span>
									<input type = 'hidden' name = 'proceed_page' value = 'proceed'>
								</td>
							</tr>
						</table>
						</td>
					</tr>
				</table>
				<input type = 'hidden' name = 'hid_manual' value = '"""+use_manual+"""'/>
				<input type = 'hidden' name = 'hid_ads_users_only' value = '""" + ads_users_only_string + """'/>
				<input type = 'hidden' name = 'hid_ads_groups_only' value = '""" + ads_groups_only_string + """'/>
				<input type = 'hidden' name = 'ads_users_string' value = '""" + full_users_string + """'/>
				<input type = 'hidden' name = 'ads_groups_string' value = '""" + full_groups_string + """'/>
				<input type = 'hidden' name = 'adsdomain' value = '""" + adsdomain + """'/>
				</form>""" #% (use_manual);
	print common_methods.user_quota_wait;
				
	from_page = common_methods.getsubstr(querystring, '&from_page=', '&');

	allchecked     = '';
	users_checked  = '';
	users_style    = '';
	groups_style   = 'none';
	user_parm      = '';
	quota_string   = '';
	user_text      = '';
	groups_checked = '';
	quota_array = [];

	if (from_page == 'add_quota_page'):
		user_parm   = common_methods.getsubstr(querystring, '&up=', '&');
		user_text   = common_methods.getsubstr(querystring, '&ug=', '&');

		if (user_parm != ''):
			user_parm = user_parm.replace('%20', ' ');

			"""
			user_parm = user_parm.replace('[AND]', '&');
			user_parm = user_parm.replace('[HASH]', '#');
			user_parm = user_parm.replace('[DOLLAR]', '$');
			"""

		openfile = '/tmp/tmpquotafile';
		quota_string = commands.getoutput('sudo grep "\'quota\':" ' +  openfile);

		quota_string = quota_string[quota_string.find('[{') + 2:quota_string.find('}]')];
		quota_string = quota_string.strip();

		quota_array = quota_string.split('}, {');

		if (user_text == 'all'):
			allchecked     = 'checked';
			users_checked  = '';
			groups_checked = '';

			users_style  = 'none';
			groups_style = 'none';

		elif (user_text == 'user'):
			allchecked     = '';
			users_checked  = 'checked';
			groups_checked = '';

			users_style  = 'table';
			groups_style = 'none';

		elif (user_text == 'group'):
			allchecked     = 'checked';
			users_checked  = '';
			groups_checked = 'checked';

			users_style  = 'none';
			groups_style = 'table';

				
	print """			<form name = 'search_user_quota' method = 'POST'>
					<table width = "685" border = "0" cellspacing = "0" cellpadding = "0" name = 'disp_tables' id = 'id_user_details' style = 'font-weight: bold; display:  """ + search_quota_style + """;'>
					<tr>
						<td height = "33px" width = "8" align = "left">
							<img src = "../images/rightside_left.jpg" width = "8" height = "33" />
						</td>
						<td width = "669" height = "33px" align = "left" valign = "middle" class = "right_bg rightsidemenuheading">
							<!--<a class = 'link' href = 'user_quota_details_help.php' onclick = "window.open('user_quota_details_help.php', 'help', 'location = no, height = 500, width = 600'); return false;">""" + common_methods.getimageicon() + """ </a>-->
							<div id="item_2" class="item" style="width:21%;">         
                        """+image_icon+""" User Quota Details
                        <div class="tooltip_description" style="display:none" title="User Quota Details">
                                <span>This gives information about the resources that are being used by the system.</span><br/><br/>
                                <table border="0">
                                <tr class="spaceUnder">
                                <td valign="top" align="left"><strong style="color:#b2b2b2; padding:0px 2px 0px 2px;">Show all:</strong></td>
                                <td>Choose an option for User/Group for the quota to be assigned.</td>
                                </tr>
                                <tr class="spaceUnder">
                                <td valign="top" align="left"><strong style="color:#cccccc; padding:0px 2px 0px 2px;">Users:</strong></td>
                                <td>Choose a user/group from the dropdown</td>
                             </tr>

                                <tr class="spaceUnder">
                                <td valign="top" align="left"><strong style="color:#cccccc; padding:0px 2px 0px 2px;">Groups:</strong></td>
                                <td>Here you can see the details of the quota assigned to specific users/groups</td>
                             </tr>

                                </table>
                                </div></div>

						</td>
						<td height = "33px" width = "8" align = "right">
							<img src = "../images/rightside_right.jpg" />
						</td>
					</tr>
					<tr>
						<td colspan = "3" align = "left" valign = "top">
							<table width = "685" border = "0" cellspacing = "0" cellpadding = "0" class = 'outer_border'><tr><td>"""
	users_checked = '';

	if (connstatus == 'Join is OK'):
		if (quotauserslength < 1000 and quotagroupslength < 1000):
			users_style = 'none';
			print """
			
								<input type = 'radio' name = 'search_user' value = 'all' onclick = 'return validate_search_quota("Show Details");' """ + allchecked + """> Show All"""

		else:
			users_checked = 'checked';
			users_style = 'table';

			print """<font color = 'darkred'>Users list exceded 1000. Please type the username in the textbox</font>"""

	else:
		users_style = 'none';
		print """<input type = 'radio' name = 'search_user' value = 'all' onclick = 'return validate_search_quota("Show Details");' """ + allchecked + """> Show All"""

	print """						</td></tr><tr>
								<td width = "172" class = "table_heading" height = "70px" valign = "middle">
							<input type = 'radio' name = 'search_user' value = 'user' onclick = 'return show_search_users_list();' """ + users_checked + """>Users
								</td>
								<td class = "table_content" height = "30px" valign = "middle" colspan = "2">"""
								
	if (groups_style == 'table'):
		users_style = 'none';

	if (quotauserslength == 0):
		print 'No users!';
								
	elif (quotauserslength > 1000):
		#users_style = 'table';

		print """<input id = 'id_search_user_list' name = 'user_list' type="text" class = 'input' value = '' oninput = 'generate_user_list(document.getElementById("id_search_user_list"), document.getElementById("search_quota_autosuggest"), \"""" + ads_users_only_string + """", "users", "search_user_quota");' onclick = 'document.getElementById("search_quota_autosuggest").style.display = "none";' style = 'display: """ + users_style + """; width: 50%;'> <input id = 'id_subutton' class = 'input1' type = 'button' name = 'search' value = 'Go'  onclick = 'return validate_search_quota("Show Details");' style = 'display:""" + users_style + """;'>""";	

		print """<select class = 'input' style = 'position: absolute; display: none; width: 300px; height: 300px;' id = 'search_quota_autosuggest' name = 'avail_users' multiple onclick = 'return set_user(this.form.id_search_user_list, this.form.search_quota_autosuggest, this.form.search_quota_autosuggest.value);' onkeydown = 'return get_key();' >"""

	else:
		print """<select id = 'id_search_user_list' class = 'input' name = 'user_list' style = 'display: """ + users_style + """; width: 100%;' onchange = 'return validate_search_quota("Show Details");'>
		<option value = ''>---</option>"""
					
		for local_users in all_users_array:
			if (connstatus == 'Join is OK'):
				"""
				local_users = local_users.replace('[AND]', '&');
				local_users = local_users.replace('[HASH]', '#');
				local_users = local_users.replace('[DOLLAR]', '$');
				"""

				useridcommand = commands.getstatusoutput('wbinfo --user-info="' + local_users + '"');

				if (useridcommand[0] == 0):
					local_usersline = useridcommand[1].strip();
						
					temp = [];
					temp = local_usersline.split(':');

					users_text     = temp[0];
					local_users_id = temp[2];

					if (users_text.find('\\') > 0):
						users_text = users_text[users_text.find('\\') + 1:];

					else:
						users_text = users_text[users_text.find('+') + 1:];

					"""
					users_text = users_text.replace('&', '[AND]');
					users_text = users_text.replace('#', '[HASH]');
					users_text = users_text.replace('$', '[DOLLAR]');
					"""
				
			if (local_users.find('\\') > 0):
				users_only = local_users[local_users.find('\\') + 1:];

			elif (local_users.find('+') > 0):
				users_only = local_users[local_users.find('+') + 1:];

			else:
				users_only = local_users;

			if (connstatus == 'Join is OK'):
				#if (local_users == user_parm):
				#	print """<option value = '""" + local_users_id + """' selected>""" + users_only + """</option>""";

				#else:
				print """<option value = '""" + local_users_id + """***""" + users_text + """'>""" + users_only + """</option>""";
		
			else:
				#if (local_users == user_parm):
				#	print """<option value = '""" + local_users + """' selected>""" + users_only + """</option>""";

				#else:
				print """<option value = '""" + local_users +"""'>""" + users_only + """</option>""";
		
				
		print """</select>""";
							
	print """							
								</td>
							</tr>
							<tr>
								<td width = "172" class = "table_heading" height = "70px" valign = "middle">
									<input type = 'radio' name = 'search_user' value = 'group' onclick = 'return show_search_users_list("Show Details");' """ + groups_checked + """>Groups&nbsp;&nbsp;&nbsp;
								</td>
								<td class = "table_content" height = "70px" valign = "middle" colspan = "2">"""
	if (quotagroupslength == 0):
		print 'No groups!';
								

	elif (quotagroupslength > 1000 and connstatus == 'Join is OK'):
		print """<input id = 'id_search_group_list' name = 'group_list' type="text" class = 'input' value = '' oninput = 'generate_user_list(document.getElementById("id_search_group_list"), document.getElementById("search_g_quota_autosuggest"), \"""" + ads_groups_only_string + """", "groups", "search_user_quota");' onclick = 'document.getElementById("search_g_quota_autosuggest").style.display = "none";' style = "display: """ + groups_style + """; width: 50%;"><input id = 'id_sgbutton' class = 'input1' type = 'button' name = 'move' value = 'Go'  onclick = 'return validate_search_quota("Show Details");' style = "display: """ + groups_style + """;">""";

                print """<div id="suggest" style="visibility:hidden;border:#000000 1px solid;width:150px;"></div>
                                                                <select class = 'input' style = 'display: none; width: 300px; height: 300px;' id = 'search_g_quota_autosuggest' name = 'avail_groups' multiple onclick = 'return set_user(this.form.id_search_group_list, this.form.search_g_quota_autosuggest, this.form.search_g_quota_autosuggest.value);' onkeydown = 'return get_key();' >"""

	else:
		print """<select id = 'id_search_group_list' class = 'input' name = 'group_list' style = 'display:  """ + groups_style + """; width: 100%;' onchange = 'return validate_search_quota("Show Details");'>
			<option value = '' selected>---</option>"""
							
		for local_groups in all_groups_array:
			if (local_groups != 'USER'):
				if (connstatus == 'Join is OK'):
					"""
					local_groups = local_groups.replace('[AND]', '&');
					local_groups = local_groups.replace('[HASH]', '#');
					local_groups = local_groups.replace('[DOLLAR]', '$');
					"""

					groupidcommand = commands.getstatusoutput('wbinfo --group-info="' + local_groups + '"');

					if (groupidcommand[0] == 0):
						local_groups_line = groupidcommand[1];

						temp = [];
						temp = local_groups_line.split(':');

						groups_text     = temp[0];
						local_groups_id = temp[2];

						if (groups_text.find('\\') > 0):
							groups_text = groups_text[groups_text.find('\\') + 1:];

						else:
							groups_text = groups_text[groups_text.find('+') + 1:];

						"""
						groups_text = groups_text.replace('&', '[AND]');
						groups_text = groups_text.replace('#', '[HASH]');
						groups_text = groups_text.replace('$', '[DOLLAR]');
						"""

				if (local_groups.find('\\') > 0):
					groups_only = local_groups[local_groups.find('\\') + 1:];

				elif (local_groups.find('+') > 0):
					groups_only = local_groups[local_groups.find('+') + 1:];

				else:
					groups_only = local_groups;

				if (connstatus == 'Join is OK'):
					#if (local_groups == user_parm):
					#	print """<option value = '""" + local_groups_id + """' selected>""" + groups_only + """</option>""";
							
					#else:
					print """<option value = '""" + local_groups_id + """***""" + groups_text + """'>""" + groups_only + """</option>""";

				else:
					print """<option value = '""" + local_groups + """'>""" + groups_only + """</option>""";

		print """</select>""";
							
	print """							</td>
							</tr>
							<tr>
								<td colspan = '3' class = "table_content" height = "70px" valign = "middle" colspan = "2">"""
						
	index_of_disk = quota_string.find('/storage/');

	if (index_of_disk != '' and quota_string != ''):
		button_lable = 'Delete Quota';
						
		print """<table id = 'id_quota_details' width = "685" border = "0" cellspacing = "0" cellpadding = "0" class = 'border' align = 'center'>
							<tr>
								<td width = "2%" class = "table_heading" height = "35px" valign = "middle">
									SNo
								</td>
								<td width = "30%" class = "table_heading" height = "35px" valign = "middle">"""
		print 								 user_text.capitalize(); 
		print """						</td>
								<td width = "20%" class = "table_heading" height = "35px" valign = "middle">
									Disk
								</td>
								<td width = "2%" class = "table_heading" height = "35px" valign = "middle">
									Allocated Space
								</td>
								<td width = "2%" class = "table_heading" height = "35px" valign = "middle">
									Used Space
								</td>
							</tr>"""
							
		count = 1;

		#if (quota_string.find('\'quota\': []') >= 0):
		#	quota_array = [];

		if (len(quota_array) > 0):
			buttdisabled = '';

			for quota_vals in quota_array:
				use_percent   = quota_vals[quota_vals.find('used_space') + len('used_space'):quota_vals.find(',')];
				use_percent   = use_percent.replace('\'', '');
				use_percent   = use_percent.replace(':', '');
				use_percent   = use_percent.strip();
				alloted_space = quota_vals[quota_vals.find(':') + 1:quota_vals.rfind(':')];
				quota_disk    = quota_vals[quota_vals.rfind(':') + 1:];

				use_percent   = use_percent.strip();

				alloted_space = alloted_space[alloted_space.find('\'limit\': \'') + len('\'limit\': \''):alloted_space.rfind('\',')];
				alloted_space = alloted_space.strip();

				quota_disk    = quota_disk.replace('/storage/', '');
				quota_disk    = quota_disk.replace('\'', '');
				quota_disk    = quota_disk.strip();

				if ((user_text == 'user' or user_text == 'group') and use_percent != '[]' and alloted_space != '0'):
					if (user_parm.find('\\') > 0):
						user_only = user_parm[user_parm.find('\\') + 1:];

					elif (user_parm.find('+') > 0):
						user_only = user_parm[user_parm.find('+') + 1:];

					else:
						user_only = user_parm;

					print """							<tr>
											<td class = "table_content" height = "35px" valign = "middle">"""
					print								 count 
					print """						</td>
											<td class = "table_content" height = "35px" valign = "middle">"""
					print								 user_only 
					print """						</td>
											<td class = "table_content" height = "35px" valign = "middle">"""
					print								 quota_disk 
					print """						</td>
											<td class = "table_content" height = "35px" valign = "middle">"""
					print								 alloted_space 
					print """							</td>
											<td class = "table_content" height = "35px" valign = "middle">"""
					print								 use_percent 
					print """						</td>
										</tr>"""
							
					count = count + 1;

				else:
					print "<tr><td colspan = '5' align = 'center' style = 'font-size: 12px;'><B>No quota allocated for " + user_text + " '" + user_parm + "'!</B></td></tr>";
							
		print """				</table>"""

	if (user_text == 'all'):
		count = 1;

		print """<table id = 'id_quota_details' width = "685" border = "0" cellspacing = "0" cellpadding = "0" class = 'border' align = 'center'>
							<tr>
								<td width = "2%" class = "table_heading" height = "35px" valign = "middle">
									SNo
								</td>
								<td width = "30%" class = "table_heading" height = "35px" valign = "middle">"""
		print """			 User/Group """
		print """		</td>
								<td width = "20%" class = "table_heading" height = "35px" valign = "middle">
									Disk
								</td>
								<td width = "2%" class = "table_heading" height = "35px" valign = "middle">
									Allocated Space
								</td>
								<td width = "2%" class = "table_heading" height = "35px" valign = "middle">
									Used Space
								</td>
							</tr>"""
		contentsarray = [];
		contentsarray = common_methods.read_file('/tmp/tmpquotafile');

		if (len(contentsarray) > 0):
			buttdisabled = '';

			for rows in contentsarray:
				temp = [];
				temp = rows.split(':');

				if (connstatus == 'Join is OK'):
					usergroup = temp[4];

					if (usergroup.find('\\') > 0):
						usergroup = usergroup[usergroup.find('\\') + 1:];

					else:
						usergroup = usergroup[usergroup.find('+') + 1:];

				else:
					usergroup = temp[0];

				diskname  = temp[1];
				allspace  = temp[2];
				usespace  = temp[3];

				diskname = diskname[diskname.rfind('/') + 1:];

				print """<tr><td class = "table_content" height = "35px" valign = "middle">""";
				print 		count;
				print """</td>"""
				print """<td class = "table_content" height = "35px" valign = "middle">""";
				print 		usergroup;
				print """</td>""";
				print """<td class = "table_content" height = "35px" valign = "middle">""";
				print 		diskname;
				print """</td>""";	
				print """<td class = "table_content" height = "35px" valign = "middle">""";
				print 		allspace;
				print """</td>""";
				print """<td class = "table_content" height = "35px" valign = "middle">""";
				print 		usespace;
				print """</td></tr>""";

				count = count + 1;
		
		else:
			buttdisabled = 'disabled';
			print """<tr><td colspan = '5' align = 'center'><B>Could not find quota details!</B></td></tr>""";

		print "</table>""";	
							
	#else:
	#	if (user_parm != '' and from_page == 'add_quota_page'):
	#		print '<B>No quota allocated for ' + user_parm + ' "' + user_text + '"!</B>';
						
	print """					</td>
					</tr>
					<tr>
						<td colspan = '3' align = 'right'>
							<BR><!--<input class = 'input1' type = 'button' name = 'search' value = 'show Details' onclick = 'return validate_search_quota();'>-->
							<!--<input class = 'input1' type = 'button' name = 'cancel' value = 'Cancel' onclick = 'location.href = "main.php?page=share";'>-->
							    <span style="margin-right:2%;"><span id="button-one"><button type = 'button'  name = 'cancel' value = 'Cancel' onclick = 'location.href = "main.py?page=nas&act=search_quota_done";' style = 'width:74px; background-color:#E8E8E8; border:none;float:right;font-size: 100%; ' title="Cancel"><a style="font-size:75%; width:100%;"  >Cancel</a></button></span>
							        <!--<span style="margin-left: 54%;" ><span id="button-one"><button type = 'button' name="search" value=\"""" + button_lable + """" onclick ="return validate_search_quota();" style = 'width:88px; background-color:#E8E8E8; border:none; float: right;font-size: 86%; ' title=\"""" + button_lable + """"><a id = 'id_button_lable' style="font-size:89%;width:100%;">""" + button_lable + """</a></button></span></span>-->
								<span style="margin-left: 54%;" ><span id="button-one"><button type = 'button' name="search" value="Delete Quota" onclick ="return validate_search_quota('Delete Quota');" style = 'width:88px; background-color:#E8E8E8; border:none; float: right;font-size: 86%; ' title="Delete Quota" """ + buttdisabled + """><a id = 'id_button_lable' style="font-size:89%;width:100%;">Delete Quota</a></button></span></span>"""
	"""
	user_parm = user_parm.replace('&', '[AND]');
	user_parm = user_parm.replace('#', '[HASH]');
	user_parm = user_parm.replace('$', '[DOLLAR]');
	"""
	print """

							<input type = 'hidden' name = 'hid_action' value = '"""+button_lable+"""'>
							<input type = 'hidden' name = 'proceed_page' value = 'proceed'>
							<input type = 'hidden' name = 'hid_user_text' value = '"""+user_text+"""'>
							<input type = 'hidden' name = 'hid_user_parm' value = '"""+user_parm+"""'>
						</td>
					</tr>
				</table>
				</form>
			</td>
			</tr>
			</table><BR>"""
# % (button_lable, button_lable, user_text, user_parm);

except Exception as e:
	disp_except.display_exception(e);
