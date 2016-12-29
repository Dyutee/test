#!/usr/bin/python
import cgitb, sys, common_methods, os, commands, include_files, cgi
cgitb.enable()

sys.path.append('../modules/');
import disp_except;

try:
	#################################################
        ################ import modules #################
        #################################################
	sys.path.append('/var/nasexe/python/');
	import quota, tools, authentication;
	from tools import db
	from fs2global import *
	#--------------------- END --------------------#
	
	check_ha = tools.check_ha()

	#################################################
        ################ default values #################
        #################################################
	alldisabled         = '';
	users_list_style    = 'none';
	s_users_list_style  = 'none';
	s_groups_list_style = 'none';
	results_style       = 'none';
	groups_list_style   = 'none';
	ads_separator       = '';
	found               = '';
	statmessage         = '';
	response            = '';

	quotafiletoread = '/tmp/tmpquotafile';
	formname = '';

	user_checked  = '';
	group_checked = '';

	get_users_string = '';
	get_groups_string = '';

	get_s_users_string = '';
	get_s_groups_string = '';

	users_dropdown = '';
	groups_dropdown = '';

	domainsarray      = [];
	quotauserslength  = 0;
	quotagroupslength = 0;
	#--------------------- END --------------------#

	#################################################
        ############### Connection Status ###############
        #################################################
	conn_status = authentication.get_auth_type()
	if(conn_status["type"] == "ads"):
		connstatus = 'Join is OK'
	elif(conn_status["type"] == "nis"):
		connstatus = 'nis is running'
	elif(conn_status["type"] == "local"):
		connstatus = 'local'
	elif(conn_status["type"] == "ldap"):
		connstatus = 'ldap'
	#--------------------- END --------------------#
	if (connstatus == 'Join is OK'):
		ads_separator = '\\';

	image_icon = common_methods.getimageicon();
	adsdomain    = '';

	button_lable = 'Show Details';
	buttdisabled = 'disabled';

	user_quota_style   = 'table';
	search_quota_style = 'none';

	querystring = os.environ["QUERY_STRING"];

	if (querystring.find('&st=') > 0):
		response = querystring[querystring.find('&st=') + len('&st='):];

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
	
	assigned_user = '';
	user_group    = '';

	ug = '';

	domainsarray = common_methods.get_all_domains();
	domainname = '';

	quota_array = [];

	if (all_users_list['id'] == 0):
		all_users_array  = all_users_list['users'];
		quotauserslength = len(all_users_array);

	if (all_groups_list['id'] == 0):
		all_groups_array  = all_groups_list['groups'];
		quotagroupslength = len(all_groups_array);

	if (querystring.find('&ug=') > 0):
		ug = querystring[querystring.find('&ug=') + len('&ug='):querystring.find('&dom=')];

	if (querystring.find('&dom=') > 0):
		domainname = querystring[querystring.find('&dom=') + len('&dom='):];
		domainname = domainname.strip();

	if (querystring.find('fn=') >= 0):
		formname = querystring[querystring.find('fn=') + len('fn='):querystring.find('&page=')];

	if (querystring.find('&up=') > 0):
		assigned_user = querystring[querystring.find('&up=') + len('&up='):];

	if (querystring.find('&ug=') >= 0):
		if (querystring.find('&dom=') >= 0):
			user_group = querystring[querystring.find('&ug=') + len('&ug='):querystring.find('&dom=')];

		else:
			user_group = querystring[querystring.find('&ug=') + len('&ug='):querystring.find('&up=')];

	if (user_group == 'all'):
		results_style = 'table';

	if (assigned_user != ''):
		assigned_user = assigned_user.replace('[AND]', '&');
		assigned_user = assigned_user.replace('[HASH]', '#');
		assigned_user = assigned_user.replace('[DOLLAR]', '$');
		assigned_user = assigned_user.replace("[SQUOTE]", "'");
		assigned_user = assigned_user.replace("[DOT]", ".");

		if (user_group == 'user'):
			assigned_user = assigned_user.replace("%20"," ")
			#assigned_user = assigned_user.encode('string-escape')
			#assigned_user = assigned_user.replace("\\\\","\\")
			assigned_user = repr(assigned_user)[1:-1]
			assigned_user = assigned_user.replace("\\\\","\\")
			quota_dict = quota.show(user_group, usrname=assigned_user)

		elif (user_group == 'group'):
			assigned_user = assigned_user.replace("%20"," ")
			#assigned_user = assigned_user.encode('string-escape')
			#assigned_user = assigned_user.replace("\\\\","\\")
			assigned_user = repr(assigned_user)[1:-1]
			assigned_user = assigned_user.replace("\\\\","\\")
			quota_dict = quota.show(user_group, grpname=assigned_user)

		results_style = 'table';
		
		if (quota_dict['id'] == 0):
			quota_array = quota_dict['quota'];

	assusrfile = 'quotaassusersfile';
	assgrpfile = 'quotaassgroupsfile';

	assusrarray = [];
	assgrparray = [];

	users_from_list  = [];
	groups_from_list = [];


	if (ug == 'users' or ug == 'groups'):
		assusrarray = common_methods.read_file(assusrfile);
		assgrparray = common_methods.read_file(assgrpfile);

		if (formname != 'quotadet'):
			if (len(assusrarray) > 0):
				for assu in assusrarray:
					assu = assu.replace('%20', ' ');
					assu = assu.strip();

					assu_internal = assu;
					disp_assu = assu;
			
					users_from_list.append(assu);

			if (len(assgrparray) > 0):
				for assg in assgrparray:
					assg = assg.replace('%20', ' ');
					assg = assg.strip();

					assg_internal = assg;
					disp_assg = assg.replace('@', '');

					groups_from_list.append(disp_assg);

	if (user_group == 'user'):
		user_checked = 'checked';

	elif (user_group == 'group'):
		group_checked = 'checked';

        if (ug == 'users'):
		user_checked = 'checked';

		if (formname != 'quotadet'):
	                users_list_style    = 'table';
        	        groups_list_style   = 'none';
			s_users_list_style  = 'none';
			s_groups_list_style = 'none';

		if (formname == 'quotadet'):
			users_list_style   = 'none';
        	        groups_list_style  = 'none';
			s_users_list_style = 'table';
			s_groups_list_style = 'none';

        	get_users_array   = [];
        	get_s_users_array = [];

                get_users_array   = common_methods.read_file('quotasearchusersfile.txt');
		get_s_users_array = common_methods.read_file('s_quotasearchusersfile.txt');

		get_users_array.sort();
		get_s_users_array.sort();

		if (formname == 'quotadet'):
			if (len(get_s_users_array) > 0):
				for get_users in get_s_users_array:
					if (get_users != ''):
						get_users = get_users.strip();

						get_usersinternal = common_methods.replace_chars(get_users, 'chartotext');
						get_disp_users    = get_users[get_users.find('\\') + 1:];

						get_s_users_string += '<option value = "' + get_usersinternal + '">' + get_disp_users + '</option>';

		else:
			if (len(get_users_array) > 0):
				for get_users in get_users_array:
					if (get_users != ''):
						get_users = get_users.strip();

						get_usersinternal = common_methods.replace_chars(get_users, 'chartotext');
						get_disp_users    = get_users[get_users.find('\\') + 1:];

						get_users_string += '<option value = "' + get_usersinternal + '">' + get_disp_users + '</option>';

        if (ug == 'groups'):
		group_checked = 'checked';

		if (formname != 'quotadet'):
	                groups_list_style  = 'table';
        	        users_list_style   = 'none';
			s_users_list_style  = 'none';
			s_groups_list_style = 'none';

		if (formname == 'quotadet'):
	                groups_list_style  = 'none';
        	        users_list_style   = 'none';
			s_users_list_style  = 'none';
			s_groups_list_style = 'table';

        	get_groups_array = [];
        	get_s_groups_array = [];

                get_groups_array = common_methods.read_file('quotasearchgroupsfile.txt');
                get_s_groups_array = common_methods.read_file('s_quotasearchgroupsfile.txt');

		get_groups_array.sort();
		get_s_groups_array.sort();

		if (formname == 'quotadet'):
			if (len(get_s_groups_array) > 0):
				for get_groups in get_s_groups_array:
					if (get_groups != ''):
						get_groups = get_groups.strip();

						get_groupsinternal = common_methods.replace_chars(get_groups, 'chartotext');
						get_disp_groups    = get_groups[get_groups.find('\\') + 1:];

						get_s_groups_string += '<option value = "' + get_groupsinternal + '">' + get_disp_groups + '</option>';

		else:
			if (len(get_groups_array) > 0):
				for get_groups in get_groups_array:
					if (get_groups != ''):
						get_groups = get_groups.strip();

						get_groupsinternal = common_methods.replace_chars(get_groups, 'chartotext');
						get_disp_groups    = get_groups[get_groups.find('\\') + 1:];

						get_groups_string += '<option value = "' + get_groupsinternal + '">' + get_disp_groups + '</option>';

	if (len(users_from_list) > 0):
		for assu in users_from_list:
			assu = assu.strip();

			users_dropdown += '<option value = "' + assu + '" selected>' + assu + '</option>';

	if (len(groups_from_list) > 0):
		for assg in groups_from_list:
			assg = assg.strip();

			groups_dropdown += '<option value = "' + assg + '" selected>' + assg + '</option>';
		
	if (response == 'y'):
               	statmessage = 'Success !';
	        id_divname  = 'id_trace';

       	elif (response == 'n'):
               	statmessage = 'Failed !';
                id_divname  = 'id_trace_err';

	################################################
        ################ Check HA Status ###############
        ################################################
        sys_node_name = tools.get_ha_nodename()
        if(sys_node_name == "node1"):
                other_node = "node2"
                show_tn = "Node1"
                show_on = "Node2"
        else:
                other_node = "node1"
                show_tn = "Node2"
                show_on = "Node1"

        query="select * from network_ifaces where (name='eth1' and node='"+other_node+"')"
        status=db.sql_execute(query)
        for x in status["output"]:
                other_node_ip = x["ip"]
	#--------------------- END --------------------#

	print
	print """
		<div id="loader-div" style="text-align:center; display:none;" ><img style="margin-top:20%;" src="../images/ajax-loader.gif" /><br/> Loading...</div>
	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer" style="width:730px;" id="body-div">"""
	
        if (statmessage != ''):
                print """<div id='""" + id_divname + """'>"""
                print statmessage;
                print """</div>"""

	print"""	<!--tab srt-->
		<div class="searchresult-container">
		<div style="margin:0 0 0px 0;" class="topinputwrap-heading"><a class="demo" href ="#"><img src ="../images/help_icon1.png" style="width:13px;"><span class="tooltip" >
                 <table border="0">
        <tr>     
        <td class="text_css">On this page, you can assign disk quota to users and groups. You can also view the details for the quotas assigned.</td>
        </tr>
        </table>"""
	if(check_ha ==True):
		print"""
	</span></a> Quota ("""+show_tn+""")
                <span style="float:right; margin:0;"><a onclick="return onclick_loader();" class="resource_links" href="https://"""+other_node_ip+"""/fs4/py/iframe_user_quota.py">"""+show_on+"""</a></span>
                        </div>"""
	else:
		print""" </span></a><p class = "gap_text">Quota</p></div>"""
	print"""
		  <div class="infoheader">
		    <div id="tabs">
		      <ul>
			<li><a href="#tabs-1">User Quota</a></li>
			<li><a href="#tabs-2">User Quota Details</a></li>
		      </ul>
	<div id="tabs-1">

		<!--form container starts here-->
		<div class="form-container">
		  <div class="inputwrap">"""
	print """	<form name = 'user_quota' method = 'post' action = 'add_user_quota.py'>
				<table width = "90%" cellspacing = "0" cellpadding = "0" name = 'disp_tables' id = 'id_user_quota' style = 'font-weight: bold; margin-left: 8%;' class = 'outer_border' border = '0'>
				<tr>
					<td style="color:#666666; font-weight:600;">
						Choose a domain:
						<select name = 'domainslist'>"""
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

	print """</select><BR><BR>
		
						
					</td>
				</tr>
				<tr>
					<td>
						<!--Assign quota for USERS-->
					</td>
				</tr>
				<tr>
					<td valign = 'top'>"""
	#if (quotauserslength == 0):
	#	print 'No USERS!';
	#	print """</td>"""

	#else:
	print """<B style="color:#666666; font-weight:600;">Available Users:</B><BR><input id = 'sssavailable' name = 'ads_user_text' type="text" class = 'textbox' value = '' onclick = 'document.getElementById("available").style.display = "none"; document.getElementById("available_groups").style.display = "none";' style = 'width: 60%;'><input class = 'input1' type = 'button' name = 'getusers' value = 'Check'  onclick = 'return get_user_suggestions(document.getElementById("granted").options, document.getElementById("granted_groups").options, "", "", document.user_quota.domainslist.value, this.form.sssavailable.value, "users", document.user_quota.hid_separator.value, "", "quota", \"""" + str(quotauserslength) + """", \"""" + connstatus + """");' """ + alldisabled + """ >"""

        print """<select class = 'input' style = 'width: 200px; height: 300px; display: """ + users_list_style + """;' id = 'available' name = 'avail_users' multiple onclick = 'return move_users(this.form.available, this.form.granted, "1");' onkeydown = 'return get_key();' """ + alldisabled + """>"""
       	print get_users_string;

        print """
        </select>"""
	print """</td><td>"""
	print """<select class = 'input' style ="margin-top: 2%; float: right; width:350px; height:140px;" id = 'granted' name = 'grant_users[]' multiple onclick = "return move_users(this.form.granted, this.form.available, '2');" """ + alldisabled + """>""";
        print users_dropdown;

       	print """                                                                       
                                                                                </select>"""


	print """
					
					</td>
				</tr>
				<tr>
					<td height = '25px'></td>
				</tr>
				<tr>
					<td>
						<!--Assign quota for GROUPS-->
					</td>
				</tr>
				<tr>
					<td valign = 'top'>"""

	#if (quotagroupslength == 0):
	#	print 'No GROUPS!';
	#	print """</td>"""

	#else:
	print """<B style="color:#666666; font-weight:600;">Available Groups:</B><BR>
        <input id = 'ssavailable_groups' name = 'ads_group_text' type="text" class = 'textbox' value = '' onclick = 'document.getElementById("available_groups").style.display = "none"; document.getElementById("available").style.display = "none";' style = 'width: 60%;'><input class = 'input1' type = 'button' name = 'getgroups' size ="10" value = 'Check' onclick = 'return get_user_suggestions(document.getElementById("granted").options, document.getElementById("granted_groups").options, "", "", document.user_quota.domainslist.value, this.form.ssavailable_groups.value, "groups", document.user_quota.hid_separator.value, "", "quota", \"""" + str(quotagroupslength) + """", \"""" + connstatus + """");' """ + alldisabled + """ /><!--<input class = 'input1' type = 'button' name = 'move' value = '>' onclick = "move_group_to_dropdown(this.form.available_groups, this.form.granted_groups, '1');\" """ + alldisabled + """>-->""";

	print """<select class = 'input' style = 'display: """ + groups_list_style + """; width: 200px; height: 300px;' id = 'available_groups' name = 'avail_groups' multiple onclick = 'return move_groups(this.form.available_groups, this.form.granted_groups, "1");' """ + alldisabled + """>"""
        print get_groups_string;
	print """</td><td>"""

	print """
        </select>"""
	print """<select class = 'input' style = 'margin-top: 2%; float: right; width:350px;height:140px;' id = 'granted_groups' name = 'grant_groups[]' multiple onclick = "return move_groups(this.form.granted_groups, this.form.available_groups, '2');" """ + alldisabled + """>""";
	print groups_dropdown;

	print """</select>"""



	print """				</td>
				</tr>
			<tr><td colspan = '2' height = 25px'></td></tr>
			<tr>
				<td colspan = '2' style="color:#666666; font-weight:600;">
					Enter size for quota: <input type = 'text' class = 'textbox' name = 'disk_size' style = 'width: 5%;' /> <B>GB</B>
				</td>
			</tr>
				<tr>
					<td align = 'right' colspan = '2'>"""
	print common_methods.wait_for_response;

	print """<BR><BR><div class="buttonWrapper"><button class="buttonClass" type = "submit" name = 'conf'  id = 'id_conf' value = 'enablesmbconf'  onclick ='return validate_user_quota_form();' style="float:right;">Apply</button></div>"""
	print """					</td>
				</tr>
				</table>

			<input type = 'hidden' name = 'hid_separator' value = '""" + ads_separator + """' />
			</form>""" #% (use_manual);

	print """  </div>
	</div>
	<!--form container ends here-->
	<p>&nbsp;</p>
	</div>

	<div id="tabs-2">

		<!--form container starts here-->
		<div class="form-container">
		  <div class="inputwrap">
			<form name = 'search_user_quota' method = 'post' action = 'search_user_quota.py'>
			<table align = 'center' width = '90%' style = 'margin-left: 4%;'>"""
	if (quotauserslength < 1000 and quotagroupslength < 1000):
		print """	<tr>
				<td>
					<input type = 'radio' name = 'search_user' value = 'all' onclick = 'return validate_search_quota("Show Details", "all", "all");'> <B style="color:#666666; font-weight:600;">Show All</B><BR><BR>
				</td>
			</tr>"""
	print """			<tr>
				<td>
					<input type = 'radio' name = 'search_user' value = 'user' onclick = 'return show_search_users_list();' """ + user_checked + """> <B style="color:#666666; font-weight:600;">Users</B><BR><BR>
					<div id = 'id_search_user_list' style = 'width: 100%; margin-left: 6%; display: """ + s_users_list_style + """;'>"""
	print """			<B>Choose a domain:</B><select name = 'domainslist'>"""
	
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
	print """		</select><BR><BR>
					<input id = 's_sssavailable' name = 'ads_user_text' type="text" class = 'input' value = '' onclick = 'document.getElementById("s_available").style.display = "none"; document.getElementById("s_available_groups").style.display = "none";' style = 'width: 40%;'><input class = 'input1' type = 'button' name = 'getusers' value = 'Check'  onclick = 'return get_user_suggestions("", "", "", "", document.search_user_quota.domainslist.value, this.form.s_sssavailable.value, "users", document.search_user_quota.hid_separator.value, "", "quotadet", \"""" + str(quotauserslength) + """", \"""" + connstatus + """");' """ + alldisabled + """ >"""

	if (get_s_users_string != ''):
		print """<select class = 'input' id = 's_available' name = 'user_list' onkeydown = 'return get_key();' """ + alldisabled + """ onchange = 'return validate_search_quota("Show Details", document.search_user_quota.user_list.value, "user");'>"""
		print "<option value = ''>Choose a USER</option>"
	        print get_s_users_string;

        	print """
        </select></div>"""
	print """
				</td>
			</tr>
			<tr>
				<td>
					<input type = 'radio' name = 'search_user' value = 'group' onclick = 'return show_search_users_list();' """ + group_checked + """> <B style="color:#666666; font-weight:600;">Groups</B><BR><BR>
					<div id = 'id_search_group_list' style = 'width: 100%; margin-left: 6%; display: """ + s_groups_list_style + """;'>"""
        print """                       <B>Choose a domain:</B><select name = 'domainslist1'>"""
	
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
        print """               </select><BR><BR>"""

	print """<input id = 's_ssavailable_groups' name = 'ads_group_text' type="text" class = 'input' value = '' onclick = 'document.getElementById("s_available_groups").style.display = "none"; document.getElementById("s_available").style.display = "none";' style = 'width: 40%;'><input class = 'input1' type = 'button' name = 'getgroups' size ="10" value = 'Check' onclick = 'return get_user_suggestions("", "", "", "", document.search_user_quota.domainslist1.value, this.form.s_ssavailable_groups.value, "groups", document.search_user_quota.hid_separator.value, "", "quotadet", \"""" + str(quotagroupslength) + """", \"""" + connstatus + """");' """ + alldisabled + """ />"""
	
	if (get_s_groups_string != ''):
	        print """<select class = 'input' id = 's_available_groups' name = 'group_list' onchange = 'return validate_search_quota("Show Details", document.search_user_quota.group_list.value, "group");' """ + alldisabled + """>"""
		print """<option value = ''>Choose a GROUP</option>"""
	        print get_s_groups_string;

        	print """
        </select>"""
        print """</td><td>"""

	sno = 1;
	checkboxstring = 'S.No.';

	if (user_group == 'all'):
		checkboxstring = "<input id = 'id_select_all' type = 'checkbox' name = 'selectall' onclick = 'return select_all_quotas();'>";

	print """
				</div>	<BR><BR>
				</td>
			</tr>
			</table>
			<table id = 'id_results_table' align = 'center' width = '90%' border = '1' style = 'margin-left: 4%; border: 1px solid #999999; color: #999999; border-collapse: collapse; display: """ + results_style + """'>
			<tr>
				<td width = '3%' align = 'center'>"""
	print checkboxstring;
	print """			</td>
				<td width = '40%' align = 'center'>
					<B>User/Group</B>
				</td>
				<td width = '20%' align = 'center'>
					<B>Disk(s)</B>
				</td>
				<td width = '10%' align = 'center'>
					<B>Allocated space</B>
				</td>
				<td width = '10%' align = 'center'>
					<B>Used space</B>
				</td>
			</tr>"""
	if (user_group == 'all'):
		quotafiletoread = '/tmp/tmpquotafile';
		quota_array = common_methods.read_file(quotafiletoread);
		
		if (len(quota_array) > 0):
			for quota_details in quota_array:
				temp = [];
				temp = quota_details.split(':::');

				usergroup     = temp[0];
				disk_name     = temp[1];
				alloted_space = temp[2];
				used_space    = temp[3];

				disk_name = disk_name.replace(':', ' / ');
				print """<tr>
						<td height = '35px' align = 'center'>"""
				print "<input id = 'id_del_quota' type = 'checkbox' name = 'delete_option[]' value = '" + usergroup + "' />";
				print """</td>
						<td height = '35px'>"""
				print usergroup;
				print """</td>
					<td height = '35px'>"""
				print disk_name;
				print """</td>
					<td height = '35px'>"""
				print alloted_space;
				print """</td>
					<td height = '35px'>"""
				print used_space;
				print """</td></tr>"""

				sno = sno + 1;

		else:
			print """<tr><td colspan = '5' align = 'center'><B>No details found !</B></td></tr>"""

	else:
		if (len(quota_array) > 0):
			disks_string  = '';
			usergroup     = assigned_user;

			print """
			<tr>
			<td height = '35px'>"""
			print sno;
			print """</td>
				<td height = '35px'>"""
			print	usergroup;
			print	"""</td>"""

			for quota_details in quota_array:
				disk_name     = quota_details['disk_name'];
				alloted_space = quota_details['limit'];
				used_space    = quota_details['used_space'];

				string = quota_details;
				string = str(string);

				if (string.find("'limit': '0'") < 0):
					disp_diskname = disk_name[disk_name.rfind('/') + 1:];
					disks_string += disp_diskname + ' / ';
				
				else:
					found = 'no';

			if (found == 'no'):
				if (user_group == 'user'):
					print """<td colspan = '4' align = 'center'><B>No details found for the selected user!</B></td>""";

				elif (user_group == 'group'):
					print """<td colspan = '4' align = 'center'><B>No details found for the selected group!</B></td>""";

			if (found != 'no'):
				disks_string = disks_string[:disks_string.rfind('/')];
				disks_string = disks_string.strip();
				print """<td height = '35px'>"""
				print disks_string;
				print """</td>"""
				print """<td height = '35px' align = 'right'>"""
				print alloted_space;
				print "</td><td height = '35px' align = 'right'>"""
				print used_space;
				print """</td>"""

			print """</tr>"""

			sno = sno + 1;

		else:
			if (user_group == 'user'):
				print """<tr><td colspan = '5' align = 'center'><B>No details found for the selected user!</B></td></tr>""";

			elif (user_group == 'group'):
				print """<tr><td colspan = '5' align = 'center'><B>No details found for the selected group!</B></td></tr>""";

	print """</table>"""

	if (len(quota_array) > 0 and found != 'no'):
		print """<table align = 'center' width = '90%' style = 'display: """ + results_style + """;'>
			<tr>
				<td align = 'right'>
					<BR><button class="buttonClass" type="submit" name = 'deletequota'  id = 'id_delquota' value = 'Delete Quota'  onclick = 'return validate_search_quota("Delete Quota", document.search_user_quota.usergroup.value, document.search_user_quota.ugtext.value);' style = 'margin-right: 2%;'>Delete</button>
				</td>
			</tr>
			</table>"""
	print """	<BR><input type = 'hidden' name = 'hid_separator' value = '""" + ads_separator + """' />
			<input type = 'hidden' name = 'delete_search' value = '' />
			<input type = 'hidden' name = 'ugtext' value = '""" + user_group + """' />
			<!--<input type = 'hidden' name = 'usergroup' value = """+repr(assigned_user)+""" />-->

			<div style="display:none;"><textarea name="usergroup">"""+assigned_user+"""</textarea></div>
			</form>
			  </div>
	</div>
	<!--form container ends here-->
	<p>&nbsp;</p>
	</div>
	</div>




	  </div>
	</div>
	</div>
	"""

except Exception as e:
	disp_except.display_exception(e);
