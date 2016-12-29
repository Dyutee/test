#!/usr/bin/python
import cgitb, sys, common_methods, sys, cgi, os, include_files
cgitb.enable()
form = cgi.FieldStorage()

#print 'Content-Type: text/html'

sys.path.append('../modules/');
import disp_except;

try:
	#################################################
        ################ import modules #################
        #################################################
	sys.path.append('/var/nasexe/python/')
	from fs2global import *
	import ftp_auth, ftp, anon_ftp, tools, commons, cli_utils
	#--------------------- END --------------------#

	form = cgi.FieldStorage()

	querystring = os.environ['QUERY_STRING'];
	checkmount = {'id': -1};

	users_dropdown       = '';
	groups_dropdown      = '';
	getdomain            = '';
	ftpreadonly_checked  = '';
	ftpreadonly_disabled = '';

        # initialize all the required variables
        ftpshare       = '';
        ftppath        = '';
        ftpcomm        = '';
        enable_ftp     = '';
        ftpusers_list  = '';
        ftpgroups_list = '';
        ftpreadonly    = '';
        ftpoptions     = '';
	statmessage    = '';

	ads_separator = '';

	connstatus = common_methods.conn_status();

	if (connstatus == 'Join is OK'):
		ads_separator = '\\';

	ftp_users_dropdown  = '';
	ftp_groups_dropdown = '';

	valid_user = '';
	write_ip_disabled = '';

	anonymous_checked     = 'checked';
	authenticated_checked = '';
	ug = '';

	users_list_style  = 'none';
	groups_list_style = 'none';

	valid_users_style = 'none';
	valid_groups_style = 'none';

	ftp_users_table_style = 'none';
	ftp_params_table_style = 'table';

	get_users_string = '';
	get_groups_string = '';

	alldisabled = '';
	
	querystring = os.environ['QUERY_STRING'];

	if (querystring.find('&ro=') > 0):
		get_share = querystring[querystring.find('share_name=') + len('share_name='):querystring.find('&ro=')];

	elif (querystring.find('&mess=') > 0):
		get_share = querystring[querystring.find('share_name=') + len('share_name='):querystring.find('&mess=')];

	else:
		get_share = querystring[querystring.find('share_name=') + len('share_name='):];

	if (querystring.find('ug=') >= 0):
		ug = querystring[querystring.find('ug=') + len('ug='):querystring.find('&share_name=')];

	if (querystring.find('&dom=') > 0):
		getdomain = querystring[querystring.find('&dom=') + len('&dom='):];
		getdomain = getdomain.strip();

	sharedetails = tools.get_share(get_share);
	get_share = form.getvalue("share_name")
	status = ftp_auth.is_configured(get_share)

	if (sharedetails['id'] == 0):
		sharedict = sharedetails['share'];

		sharepath = sharedict['path'];
		comment   = sharedict['comment'];
	
		temp = [];
		temp = sharepath.split('/');

		diskname = temp[2];
		diskname = diskname.strip();
		checkmount = cli_utils.is_disk_mounted(diskname);

	get_display_dict = ftp_auth.get_status(get_share)

        ftpassignedusersarray  = [];
        ftpassignedgroupsarray = [];

        # initialize the default state of the checkbox and display style and set the default values for the input boxes
	check_ftp_status          = get_display_dict['enable_ftp_checked'];

	ftpaccess_ip = '';
	ftpwrite_ip  = '';

	ftp_users_list  = '';
	ftp_groups_list = '';

	if (check_ftp_status == 'checked'):
		ftpreadonly_disabled      = get_display_dict['readonly_disable']
		ftpreadonly_checked       = get_display_dict['readonly_checked']
		anonymous_checked         = get_display_dict['anonymous_checked'];
		ftpaccess_ip              = get_display_dict['ftpaccess_ip']
		ftpwrite_ip               = get_display_dict['ftpwrite_ip']
		authenticated_checked     = get_display_dict['authenticated_checked'];
		ftp_users_list            = get_display_dict['ftp_users_list']
		ftp_groups_list           = get_display_dict['ftp_groups_list']
		write_ip_disabled         = get_display_dict['write_ip_disabled']
		write_ip_background       = get_display_dict['write_ip_background']
		ftp_params_table_style    = get_display_dict['ftp_params_table_style']
		ftp_users_table_style     = get_display_dict['ftp_users_table_style']
		ftp_assigned_users_array  = get_display_dict['ftp_assigned_users_string']
		ftp_assigned_groups_array = get_display_dict['ftp_assigned_groups_string']

	domainsarray = [];
	domainsarray = common_methods.get_all_domains();

	assusrfile = 'ftpassusersfile';
	assgrpfile = 'ftpassgroupsfile';

	assusrstring = '';
	assgrpstring = '';

	assusrarray = [];
	assgrparray = [];

	domainname = querystring[querystring.find('&dom=') + len('&dom='):];
	
	users_from_list  = [];
	groups_from_list = [];

	if (ug != ''):
		authenticated_checked = 'checked';
		ftpreadonly_checked   = '';
		ftpreadonly_disabled = 'disabled';
		anonymous_checked = '';

		ftp_users_table_style = 'table';
		ftp_params_table_style = 'none';
		
		assusrarray = common_methods.read_file(assusrfile);
		assgrparray = common_methods.read_file(assgrpfile);

		if (len(assusrarray) > 0):
			for assu in assusrarray:
				assu = assu.replace('%20', ' ');
				assu = assu.replace('%27', '\'');
				assu = assu.strip();

				assu_internal = assu;
				disp_assu = assu;

				users_from_list.append(assu);

		if (len(assgrparray) > 0):
			for assg in assgrparray:
				assg = assg.replace('%20', ' ');
				assg = assg.replace('%27', '\'');
				assg = assg.strip();

				assg_internal = assg;
				groups_from_list.append(assg);

		domainname = querystring[querystring.find('&dom=') + len('&dom='):];
		get_share  = querystring[querystring.find('share_name=') + len('share_name='):querystring.find('&ro=')];
		readonly   = querystring[querystring.rfind('&ro=') + len('&ro='):querystring.rfind('&v=')];
		visible    = querystring[querystring.rfind('&v=') + len('&v='):querystring.find('&dom=')];

		domainname = domainname.strip();
		readonly   = readonly.strip();
		visible    = visible.strip();

		if (ug == 'users'):
			ftp_users_table_style = 'table';
			ftp_params_table_style = 'none';
			users_list_style   = 'table';
			groups_list_style  = 'none';

			get_users_array = [];
			get_users_array = common_methods.read_file('ftpsearchusersfile.txt');
			get_users_array.sort();

			for get_users in get_users_array:
				if (get_users != ''):
					get_users = get_users.strip();

					get_usersinternal = common_methods.replace_chars(get_users, 'chartotext');
					get_disp_users    = get_users[get_users.find('\\') + 1:];

					if (get_users not in ftp_users_list):
						get_users_string += '<option value = "' + get_usersinternal + '">' + get_disp_users + '</option>';

		if (ug == 'groups'):
			ftp_users_table_style = 'table';
			ftp_params_table_style = 'none';
			groups_list_style  = 'table';
			users_list_style   = 'none';

			get_groups_array = [];
			get_groups_array = common_methods.read_file('ftpsearchgroupsfile.txt');
			get_groups_array.sort();

			for get_groups in get_groups_array:
				if (get_groups != ''):
					get_groups = get_groups.strip();

					get_groupsinternal = common_methods.replace_chars(get_groups, 'chartotext');
					get_disp_groups    = get_groups[get_groups.find('\\') + 1:];

					if (get_groups not in ftp_groups_list):
						get_groups_string += '<option value = "' + get_groupsinternal + '">' + get_disp_groups + '</option>';

		if (readonly == 'true'):
			writable_checked = 'checked';

		if (visible == 'true'):
			visible_checked = 'checked';

        ftp_access_ip = ''
        ftp_write_ip = ''

        ftp_assigned_users_string  = '';
        ftp_assigned_groups_string = '';

	if (check_ftp_status == 'checked'):
		if (anonymous_checked == 'checked' and ftpwrite_ip == '' and ftpreadonly_checked == ''):
			ftpwrite_ip  = '*';
			ftpaccess_ip = '*';

		if (anonymous_checked == 'checked' and ftpaccess_ip == '' and ftpreadonly_checked == ''):
			ftpaccess_ip = '*';

	if (ftpreadonly_checked == 'checked' and ftpwrite_ip == ''):
		write_ip_disabled   = 'disabled';

	if (ftpwrite_ip != ''):
		ftpreadonly_checked = '';

        ##########################
        #MOhan Sir
        ##########################
        # in readonly mode, the write ip text box is disabled and shaded
        ftpreadonly = '';

        log_file = common_methods.log_file;
        log_array = [];

        all_users_list  = '';
        all_groups_list = '';

        # get the uesrs list and groups list from the method get_users_string() defined in common_methods.py
        # the output will be in dictionary format
        all_users_list  = common_methods.get_users_string();
        all_groups_list = common_methods.get_groups_string();

	ftp_users_length  = 0;
	ftp_groups_length = 0;	

        separator = '';

        ftp_all_users_array  = [];
        ftp_all_groups_array = [];

	# if userslist is not empty
	if (all_users_list['id'] == 0):
		ftp_all_users_array  = all_users_list['users'];
		ftp_users_length     = len(ftp_all_users_array);

	# if groupslist id not empty
	if (all_groups_list['id'] == 0):
		ftp_all_groups_array = all_groups_list['groups'];
		ftp_groups_length    = len(ftp_all_groups_array);
	
        ads_users_string  = '';
        ads_groups_string = '';
	ftpuserslength = ''
	ftpgroupslength = ''

	check_shares1 = '';
	check_shares2 = '';

	if (authenticated_checked == 'checked'):
	        ftpreadonly_disabled      = 'disabled';
                ftpreadonly_checked = '';

		ftpassignedusersarray  = get_display_dict['ftp_users_list'];
		ftpassignedgroupsarray = get_display_dict['ftp_groups_list'];

                if (len(ftpassignedusersarray) > 0):
                        for ftpusers in ftpassignedusersarray:
                                if (ftpusers.find('\\') > 0):
                                        ftp_user_only = ftpusers[ftpusers.find('\\') + 1:];

                                else:
                                        ftp_user_only = ftpusers[ftpusers.find('+') + 1:];
				
				users_from_list.append(ftpusers);
	
                if (len(ftpassignedgroupsarray) > 0):
                        for ftpgroups in ftpassignedgroupsarray:
                                if (ftpgroups.find('\\') > 0):
                                        ftp_group_only = ftpgroups[ftpgroups.find('\\') + 1:];

                                else:
                                        ftp_group_only = ftpgroups[ftpgroups.find('+') + 1:];

				groups_from_list.append(ftpgroups);

	users_from_list.sort();
	users_from_list = list(set(users_from_list));

	groups_from_list.sort();
	groups_from_list = list(set(groups_from_list));
	
	div_idname = '';

	for assusers in users_from_list:
		ftp_users_dropdown += '<option value = "' + assusers + '" selected>' + assusers + '</option>';

	for assgroups in groups_from_list:
		ftp_groups_dropdown += '<option value = "' + assgroups + '" selected>' + assgroups + '</option>';

	if (checkmount['id'] != 0):
		#alldisabled = 'disabled';
		alldisabled = ''

	if (querystring.find('&mess=') > 0):
		if (check_ftp_status == 'checked'):
			statmessage = 'Configured FTP !';
			div_idname = 'id_trace';

		else:
			statmessage = 'Failed to Configure FTP!';
			div_idname = 'id_trace_err';

	if (querystring.find('&mess1=') > 0):
		if (check_ftp_status == ''):
			statmessage = 'Unconfigured FTP!';
			div_idname = 'id_trace';

		else:
			statmessage = 'Could not Unconfigure FTP !';
			div_idname = 'id_trace_err';

	get_share = form.getvalue("share_name")

        if (statmessage != ''):
                print """<div id='""" + div_idname + """'>"""
                print statmessage;
                print """</div>"""

	print
	print """

	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer">
		<!--<div class="insidepage-heading">Nas >> <span class="content">Configure Information</span></div>-->"""

	print """	<!--tab srt-->
		<div class="searchresult-container">
		  <div class="infoheader">
		    <div id="tabs">
		      <!--<ul>
			<li><a href="#tabs-1">FTP Settings</a></li>
		      </ul>-->
		      <div id="tabs-1">

		<!--form container starts here-->
		<!--<div class="form-container">-->
		<div style="padding:10px; background-color:#e9e5e5; border-bottom:#D1D1D1 1px solid; font-weight:bold;">FTP Settings for '"""+get_share+"""' 
<!--<a href = 'main.py?page=cs'><img style="float:right; padding:0;" title = 'Back to shares' src = '../images/gobacktoshares.png' /></a>-->
</div>
		  <div class="inputwrap">



<form name = 'set_ftp_params' method = 'POST' action = 'set_ftp_params.py'>
<table width="100%" style="padding:20px 0 0 0;">

<tr>
	<td valign="top" class="formrightside-content"><input type = 'checkbox' name = 'ftp_read_only' """ + ftpreadonly_checked + """ """ + ftpreadonly_disabled + """ onclick = 'return enable_disable_option(document.set_ftp_params.ftp_read_only.checked, document.set_ftp_params.ftp_write_ip);' /> Read only</td>

	<td>
	<span style="color:darkred; font-weight:600; margin-left: 41px;">Choose Mode</span><BR><BR>
	<table>
	<tr>
		<td class="formleftside-content"><input type = 'radio' name = 'choose_ftp_options' value = 'anonymous' id ="anon" onclick = 'return set_ftp_parameters();' """ + anonymous_checked + """ > Anonymous Mode</td>
	</tr>
	<tr>
		<td class="formleftside-content"><input type = 'radio' name = 'choose_ftp_options' value = 'authenticated' id ="anon" onclick = 'return set_ftp_parameters();' """ + authenticated_checked + """> Authenticated Mode</td>
	</tr>
	</table>
	</td>

</tr>

</table>

<div width = '100%' id = 'ftp_params_table' style = 'display: """ + ftp_params_table_style + """; '>
<table width="50%" style="margin:20px 0 0 20px;">

<tr>
<td>
<table width="100%">
<tr>
        <!--<td style="background-color:#BDBDBD; height:30px; color:#000; padding:0 0 0 10px;">Anonymous Mode</td>-->
        <td style="color:darkred; font-weight:600;">Anonymous Mode</td>
</tr>
</table>

</td>
</tr>
</table>
<table>
<tr>
	<td class="formleftside-content">Access IP:</td>
	<td><input class = 'textbox' name = 'ftp_access_ip' id = 'id_access_ip' style="margin-left: -81px;" value = '""" + ftpaccess_ip + """' ></td>
</tr>

<tr>
	<td class="formleftside-content">Write IP:</td>
	<td> <input class = 'textbox' name = 'ftp_write_ip' id = 'id_write_ip' style="margin-left: -81px;" value = '""" + ftpwrite_ip + """' ></td>
</tr>

</table>
</div>

<div width = '100%' id = 'ftp_users_list' style = 'display: """ + ftp_users_table_style + """;'>
<table width="90%" style="margin:20px 0 0 20px;">

<tr>
<td>
<table width="100%">
<tr>
        <!--<td style="background-color:#BDBDBD; height:30px; color:#000; padding:0 0 0 10px;">Authenticated Mode</td>-->
        <td style="color:#666666; font-weight:600;">Authenticated Mode</td>
</tr>
</table>

<table width="90%" style="margin:0px 0 0 30px; ">

<tr>
	<td style="padding-top: 3%;"><B style="color:#666666; font-weight:600;">Choose a domain:</B> """
	domainsarray.sort();

	print """
	<div class="styled-select2" style="width:184px;">
	<select name = 'domainslist'>
	<option value ='sel_domain'>Select Domain</option>
	"""
	domainsarray.sort();

	for domainname in domainsarray:
		domainname = domainname.strip();

		users_file_to_count  = user_files_dir + domainname + '-users.txt';
		groups_file_to_count = user_files_dir + domainname + '-groups.txt';

		usersfilesarray  = common_methods.read_file(users_file_to_count);
		groupsfilesarray = common_methods.read_file(groups_file_to_count);

		if (domainname == getdomain):
			print """<option value = '""" + domainname + """-""" + str(len(usersfilesarray)) + """-""" + str(len(groupsfilesarray)) + """' selected>""" + domainname + """ (""" + str(len(usersfilesarray)) + """, """ + str(len(groupsfilesarray)) + """)</option>"""

		else:
			print """<option value = '""" + domainname + """-""" + str(len(usersfilesarray)) + """-""" + str(len(groupsfilesarray)) + """'>""" + domainname + """ (""" + str(len(usersfilesarray)) + """, """ + str(len(groupsfilesarray)) + """)</option>"""

	print """	</select></div>"""
	print """</td>
	<td></td>
</tr>

<tr>
	<td style="padding:20px 0 0 0;">
	<strong style="color:darkred">Users List:</strong><BR><BR>
	
	<table width="100%">	
	<tr>
	<td valign="top">
	<br/>"""
	print """<B style="color:#666666; font-weight:600;">Available Users:</B><BR><input id = 'sssavailable' name = 'ads_user_text' type="text" class = 'input' value = '' onclick = 'document.getElementById("available").style.display = "none"; document.getElementById("available_groups").style.display = "none";'><input class = 'input1' type = 'button' name = 'getusers' value = 'Check'  onclick = 'return get_user_suggestions(document.getElementById("granted").options, document.getElementById("granted_groups").options, "", "", document.set_ftp_params.domainslist.value, this.form.sssavailable.value, "users", document.set_ftp_params.hid_separator.value, \"""" + get_share + """", "ftp", \"""" + str(ftp_users_length) + """", \"""" + connstatus + """");' >"""
        print """<select class = "input" style = "width: 200px; height: 300px; display: """ + users_list_style + """;" id = "available" name = "avail_users" multiple onclick = 'return move_users(this.form.available, this.form.granted, "1");' onkeydown = "return get_key();" >"""
	print get_users_string;
	print """
</select>"""

	print """</td>

	<td>
	<B style="color:#666666;font-weight:600;">Authorized Users:</B><br/>
	<select class = "input" style ="width:300px; height:140px;" id = "granted" name = "grant_users[]" multiple onclick = "return move_users(this.form.granted, this.form.available, '2');" >""";
	print ftp_users_dropdown;
	print """</select>
	</td>

	</tr>
	</table>
	</td>

</tr>

<tr>
	<td style="padding:20px 0 0 0;">
	<strong style="color:darkred">Groups List:</strong><BR><BR>
	
	<table width="100%">	
	<tr>
	<td valign="top">
	<B style="color:#666666; font-weight:600;">Available Groups:</B><br/>
<input id = 'ssavailable_groups' name = 'ads_group_text' type="text" class = 'input' value = '' onclick = 'document.getElementById("available_groups").style.display = "none"; document.getElementById("available").style.display = "none";'><input class = 'input1' type = 'button' name = 'getgroups' size ="10" value = 'Check' onclick = 'return get_user_suggestions(document.getElementById("granted").options, document.getElementById("granted_groups").options, "", "", document.set_ftp_params.domainslist.value, this.form.ssavailable_groups.value, "groups", document.set_ftp_params.hid_separator.value, \"""" + get_share + """", "ftp", \"""" + str(ftp_groups_length) + """", \"""" + connstatus + """");' />"""
	print """<select class = 'input' style = 'display: """ + groups_list_style + """; width: 200px; height: 300px;' id = 'available_groups' name = 'avail_groups' multiple onclick = 'return move_groups(this.form.available_groups, this.form.granted_groups, "1");' """ + alldisabled + """>"""
        print get_groups_string;

	print """</select></td>

	<td>
	<B style="color:#666666; font-weight:600;">Authorized Groups:</B><br/>
	<select class = 'input' style = 'width:300px;height:140px;' id = 'granted_groups' name = 'grant_groups[]' multiple onclick = "return move_groups(this.form.granted_groups, this.form.available_groups, '2');" %s>""" % alldisabled;
        print ftp_groups_dropdown;

	print """</select></td>
	</tr>
	</table>
	</td>

</tr>


</table>
</table>
</div>"""
	if (check_ftp_status == 'checked'):
		print """<button class="buttonClass" type = "submit"  name="unconf" value="unconfigure" onclick ="return ftp_update_validation();" style="float:right; margin:20px 135px 0 0;" >Remove</button>"""
		print """<button class="buttonClass" type = "submit"  name="conf" value="configure" onclick ="return ftp_update_validation();" style="float:right; margin:20px 10px 0 0;" >Update</button>"""
	else:
		print """<button class="buttonClass" type = "submit"  name="conf" value="configure" onclick ="return ftp_update_validation();" style="float:right; margin:20px 135px 0 0;" >Configure</button>"""
	print """<input type = "hidden" name = 'hid_separator' value = '""" + ads_separator + """' />
<input type = "hidden" name = 'hid_share' value = '""" + get_share + """' />
</form>

		  </div>
	</div>
	<!--form container ends here-->
	<p>&nbsp;</p>
	      <!--</div>-->

	  </div>
	</div>
	</div>
	"""

except Exception as e:
        disp_except.display_exception(e);
