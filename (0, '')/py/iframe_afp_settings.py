#!/usr/bin/python
import cgitb, sys, include_files, cgi
cgitb.enable()
sys.path.append('../modules/')
import disp_except

try:
	#################################################
	################ import modules #################
	#################################################
	import common_methods, string, os
	form = cgi.FieldStorage()
	sys.path.append('/var/nasexe/python/')
	import tools
	from fs2global import *
	import afp
	#--------------------- END --------------------#

	#################################################
	################ default values #################
	#################################################
	get_domain_val = ""
	read_only_val = ""
	display_users_list = "none"
	display_groups_list = "none"
	display_auth_users = "none"
	check_auth_user = ""
	check_guest = "checked"
	check_ro = ""
	ads_separator = ""
	ftp_users_list = ""
	ftp_groups_list = ""
	#--------------------- END --------------------#

	#################################################
	################ get all shares #################
	#################################################
	get_share = form.getvalue("share_name")
	domainsarray = common_methods.get_all_domains()
	get_sharess = tools.get_all_shares(debug=True)
	for x in get_sharess["shares"]:
		if x["name"] == get_share:
			selected_share =  x["name"]
			selected_share_path = x["path"]
	#--------------------- END --------------------#

	get_users_string = ''

	#------------------------------------ Configure AFP New Start ----------------------------------------#
	if(form.getvalue("mess")):
		get_mess = form.getvalue("mess")
		if(get_mess == "afp_yes"):
			print "<div id='id_trace'>"
			print "AFP configures Successfully!"
			print "</div>"

	if(form.getvalue('action_but')):
		afp_read_only = form.getvalue('read_only')
		permission_type = form.getvalue('afp_priv')
		afp_advance = form.getvalue('advanced_per')
		afp_host_allow = form.getvalue('host_allow')
		afp_host_deny = form.getvalue('host_deny')
		afp_umask = form.getvalue('umask')
		afp_file_perm = form.getvalue('file_perm')
		afp_dir_perm = form.getvalue('dir_perm')
		afp_grant_users = form.getvalue('grant_users[]')
		afp_grant_groups = form.getvalue('grant_groups[]')

		if(afp_grant_users != None):
			if(isinstance(afp_grant_users,str) == True):
				afp_grant_users = common_methods.replace_chars(afp_grant_users, 'texttochar');
			else:
				tmp_afp_grant_users = []
				for d in afp_grant_users:
					d = common_methods.replace_chars(d, 'texttochar');
					tmp_afp_grant_users.append(d)
				afp_grant_users = tmp_afp_grant_users

		if(afp_grant_groups != None):
			if(isinstance(afp_grant_groups,str) == True):
				if (afp_grant_groups.find('@') != 0):
					afp_grant_groups = "@"+afp_grant_groups
				afp_grant_groups = common_methods.replace_chars(afp_grant_groups, 'texttochar');
			else:
				tmp_afp_grant_groups = []
				for j in afp_grant_groups:
					if (j.find('@') != 0):
						j = "@"+j
					j = common_methods.replace_chars(j, 'texttochar');
					print j
					tmp_afp_grant_groups.append(j)
				afp_grant_groups = tmp_afp_grant_groups

		if((afp_grant_users == None) and (afp_grant_groups == None)):
			permission_type = "guest"

		afp_file_perm = "0755"
		afp_dir_perm = "0755"

		dict_value = {'afp_read_only':afp_read_only, 'permission_type':permission_type, 'afp_advance':afp_advance, 'afp_host_allow':afp_host_allow, 'afp_host_deny':afp_host_deny, 'afp_umask':afp_umask, 'afp_file_perm':afp_file_perm, 'afp_dir_perm':afp_dir_perm, 'afp_grant_users':afp_grant_users, 'afp_grant_groups':afp_grant_groups, 'selected_share':selected_share, 'selected_share_path':selected_share_path}

		conf_afp_cmd = afp.configure(dict_value)
		print """<script>location.href = 'iframe_afp_settings.py?share_name="""+selected_share+"""&mess=afp_yes';</script>"""
		if(conf_afp_cmd == None):
			print "<div id='id_trace'>"
			print "AFP configured successfully!"
			print "</div>"
	#------------------------------------ Configure AFP New End ----------------------------------------#

	#------------------------------------ Unconfigure AFP New Start ----------------------------------------#
	if(form.getvalue("unc_action_but")):
		unconf_cmd = afp.unconfigure(selected_share)
		if(unconf_cmd == None):
			print "<div id='id_trace'>"
			print "AFP unconfigured successfully!"
			print "</div>"
	#------------------------------------ Unconfigure AFP New End ----------------------------------------#

	#------------------------------------ Get status of AFP Start ----------------------------------------#
	get_display_dict = afp.getstatus(selected_share, selected_share_path)

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
	#------------------------------------ Get status of AFP End ----------------------------------------#
						       
	#---------------------------- Search User/Group -------------------------------#
	ug = ''
	get_users_string  = '';
	get_groups_string = '';

	assusrfile = 'afpassusersfile';
	assgrpfile = 'afpassgroupsfile';

	assusrstring = '';
	assgrpstring = '';

	assusrarray = [];
	assgrparray = [];

	users_dropdown = ''
	groups_dropdown = ''


	querystring = os.environ["QUERY_STRING"];
	domainname = querystring[querystring.find('&dom=') + len('&dom='):];

	if (querystring.find('ug=') >= 0):
		ug = querystring[querystring.find('ug=') + len('ug='):querystring.find('&share_name')];

	if(form.getvalue("ro")):
		read_only_val = form.getvalue("ro")

	if(read_only_val == "true"):
		check_ro = "checked"

	if(form.getvalue("dom")):
		get_domain_val = form.getvalue("dom")
		#print get_domain_val

	if (ug != ''):
		validuser_checked = 'checked';

		assusrarray = common_methods.read_file(assusrfile);
		assgrparray = common_methods.read_file(assgrpfile);
		nw_assgrparray = []
		for g in assgrparray:
			if(g.find('@') == 0):
				nw_assgrparray.append(g)
			else:
				g = '@'+g
				nw_assgrparray.append(g)

		assgrparray = nw_assgrparray
		

		if (len(assusrarray) > 0):
			#---- 14-01-2014 ----#
			new_assusrarray = []
			for n in assusrarray:
				n = n.strip()
				new_assusrarray.append(n)

			assusrarray = new_assusrarray

			if(split_vul1 != ''):
				for b in split_vul1:
					if(b.find('@') == 0):
						assgrparray = assgrparray
					else:
						assusrarray.append(b)

			assusrarray = list(set(assusrarray))
			#---- 14-01-2014 ----#
			
			temp_assusrarray = []
			for assu in assusrarray:
				assu = assu.replace('%20', ' ');
				assu = assu.replace('[AND]', '&');
	                        assu = assu.replace('[HASH]', '#');
        	                assu = assu.replace('[DOLLAR]', '$');
                	        assu = assu.replace("[SQUOTE]", "'");
                	        assu = assu.replace("[DOT]", ".");
				temp_assusrarray.append(assu)
				
			assusrarray = temp_assusrarray
			assusrarray = list(set(assusrarray))
			for assu in assusrarray:
				#assu_internal = common_methods.replace_chars(assu, 'chartotext');
				assu = assu.strip();

				assu_internal = assu;
				disp_assu     = assu[assu.find('+') + 1:];

				users_dropdown += '<option value = "' + assu_internal + '" selected>' + disp_assu + '</option>';

			

		if (len(assgrparray) > 0):
			#---- 14-01-2014 ----#
			new_assgrparray = []
			for c in assgrparray:
				c = c.strip()
				new_assgrparray.append(c)

			assgrparray = new_assgrparray

			if(split_vul1 != ''):
				for b in split_vul1:
					if(b.find('@') == 0):
						assgrparray.append(b)

			assgrparray = list(set(assgrparray))
			#---- 14-01-2014 ----#

			temp_assgrparray = []
			for assg in assgrparray:
				assg = assg.replace('%20', ' ');
				assg = assg.replace('[AND]', '&');
	                        assg = assg.replace('[HASH]', '#');
        	                assg = assg.replace('[DOLLAR]', '$');
                	        assg = assg.replace("[SQUOTE]", "'");
                	        assg = assg.replace("[DOT]", ".");
				temp_assgrparray.append(assg)

			assgrparray = temp_assgrparray
			assgrparray = list(set(assgrparray))

			for assg in assgrparray:
				#assg_internal = common_methods.replace_chars(assg, 'chartotext');
				assg = assg.replace('%20', ' ');
				assg = assg.replace('[AND]', '&');
	                        assg = assg.replace('[HASH]', '#');
        	                assg = assg.replace('[DOLLAR]', '$');
                	        assg = assg.replace("[SQUOTE]", "'");
                	        assg = assg.replace("[DOT]", ".");
				assg = assg.strip();

				assg_internal = assg;
				#disp_assg     = assg[assg.find('+') + 1:];
				disp_assg = assg.replace('@', '');

				if (assg.find('@') == 0):
					groups_dropdown += '<option value = "' + assg_internal + '" selected>' + disp_assg + '</option>';

				else:
					groups_dropdown += '<option value = "@' + assg_internal + '" selected>' + disp_assg + '</option>';

		domainname = querystring[querystring.find('&dom=') + len('&dom='):];
		get_share  = querystring[querystring.find('share_name=') + len('share_name='):querystring.find('&ro=')];
		readonly   = querystring[querystring.rfind('&ro=') + len('&ro='):querystring.rfind('&v=')];
		visible    = querystring[querystring.rfind('&v=') + len('&v='):querystring.find('&dom=')];

		domainname = domainname.strip();
		readonly   = readonly.strip();
		visible    = visible.strip();

		if (ug == 'users'):
			valid_users_style  = 'table';
			valid_groups_style = 'table';
			users_list_style   = 'table';
			groups_list_style  = 'none';

			get_users_array = [];
			get_users_array = common_methods.read_file('afpsearchusersfile.txt');

			new_get_users_array = []
			for l in get_users_array:
				l = l.strip()
				new_get_users_array.append(l)

			a_b = list(set(new_get_users_array) - set(assusrarray))
			get_users_array = a_b

			for get_users in get_users_array:
				if (get_users != ''):
					get_users = get_users.strip();

					get_usersinternal = common_methods.replace_chars(get_users, 'chartotext');
					get_disp_users    = get_users[get_users.find('\\') + 1:];

					if (get_users not in ftp_users_list):
						get_users_string += '<option value = "' + get_usersinternal + '">' + get_disp_users + '</option>';

					#get_usersinternal = common_methods.replace_chars(get_users, 'chartotext');
					#get_disp_users    = get_users[get_users.find('+') + 1:];

					#get_users_string += '<option value = "'+get_usersinternal+'">'+get_disp_users+'</option>';
		
			display_users_list = "block"


		if (ug == 'groups'):
			valid_groups_style = 'table';
			valid_users_style  = 'table';
			groups_list_style  = 'table';
			users_list_style   = 'none';

			get_groups_array = [];
			get_groups_array = common_methods.read_file('afpsearchgroupsfile.txt');

			new_get_groups_array = []
			for l in get_groups_array:
				l = l.strip()
				if (l.find('@') != 0):
					l = "@"+l
				new_get_groups_array.append(l)

			print new_get_groups_array
			print assgrparray

			a_b_g = list(set(new_get_groups_array) - set(assgrparray))
			get_groups_array = a_b_g


			for get_groups in get_groups_array:
				if (get_groups != ''):
					get_groups = get_groups.strip();

					get_groupsinternal = common_methods.replace_chars(get_groups, 'chartotext');
					get_disp_groups    = get_groups[get_groups.find('\\') + 1:];

					if (get_groups not in ftp_groups_list):
						get_groups_string += '<option value = "' + get_groupsinternal.replace("@","").strip() + '">' + get_disp_groups.replace("@","").strip() + '</option>';



			#get_groups_array = [];
			#get_groups_array = common_methods.read_file('searchgroupsfile.txt');

			#for get_groups in get_groups_array:
			#        if (get_groups != ''):
			#                get_groupsinternal = common_methods.replace_chars(get_groups, 'chartotext');
			#                get_disp_groups    = get_groups[get_groups.find('+') + 1:];

			#                if (get_groups.find('@') >= 0):
			#                        get_groups_string += '<option value = "' + get_groupsinternal + '">' + get_disp_groups + '</option>';

			#                else:
			#                        get_groups_string += '<option value = "@'+get_groupsinternal.strip()+'">'+get_disp_groups.strip()+'</option>';
		
			display_groups_list = "block"



		
		display_auth_users = "block"
		check_auth_user = "checked"
		check_guest = ""

		priv_checked = "checked"
		afp_users_style = "block"
		
	else:
		if(split_vul1 != ''):
			assusrarray = []
			assgrparray = []
			for t in split_vul1:
				if(t.find('@') != 0):
					assusrarray.append(t)
				else:
					assgrparray.append(t)
		
			assusrarray = list(set(assusrarray))	
			assgrparray = list(set(assgrparray))
			for u in assusrarray:
				u = u.replace('[AND]', '&');
	                        u = u.replace('[HASH]', '#');
        	                u = u.replace('[DOLLAR]', '$');
                	        u = u.replace("[SQUOTE]", "'");
                	        u = u.replace("[DOT]", ".");

				users_dropdown += '<option value = "' + u + '" selected>' + u + '</option>'
			
			for y in assgrparray:
				y = y.replace('[AND]', '&');
	                        y = y.replace('[HASH]', '#');
        	                y = y.replace('[DOLLAR]', '$');
                	        y = y.replace("[SQUOTE]", "'");
                	        y = y.replace("[DOT]", ".");


				if (y.find('@') == 0):
					groups_dropdown += '<option value = "'+y+'" selected>'+y.replace('@','')+'</option>';
				else:
					groups_dropdown += '<option value = "@'+y+'" selected>'+y+'</option>'
		else:
			users_dropdown = ''
			groups_dropdown = ''

	afp_status = afp.is_configured(selected_share)		

	conn = common_methods.conn_status()

	print
	print """

	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer">
		<!--<div class="insidepage-heading">NAS >> <span class="content">Configure Information</span></div>-->
		<!--tab srt-->
		<div class="searchresult-container">
		  <div class="infoheader">
		    <div id="tabs">
		      <!--<ul>
			<li><a href="#tabs-1">AFP Settings</a></li>
		      </ul>-->
		      <div id="tabs-1">

		<!--form container starts here-->
		<!--<div class="form-container">-->
		<div style="padding:10px; background-color:#e9e5e5; border-bottom:#D1D1D1 1px solid; font-weight:bold;">AFP Settings for '"""+get_share+"""' 
<!--<a href = 'main.py?page=cs'><img style="float:right; padding:0px;" title = 'Back to shares' src = '../images/gobacktoshares.png' /></a>-->
</div>

		  <div class="inputwrap">"""

	if((conn == "nis is running") or (conn == "Join is OK")):
		if(conn == "nis is running"):
			print """<p style="text-align:center; margin:20px;">System is connected to NIS server. <a href='main.py?page=auth' style="text-decoration:underline;" >Change Authentication</a></p>"""
		if(conn == "Join is OK"):
			print """<p style="text-align:center; margin:20px;">System is connected to ADS server. <a href='main.py?page=auth' style="text-decoration:underline;" >Change Authentication</a></p>"""

	else:
		print """<form name = 'afp_form' method = 'POST' action='iframe_afp_settings.py?share_name="""+get_share+"""' onsubmit = 'return validate_share_afp();' >
		<table width="100%" style="padding:20px 0 0 0;">

		<tr>
			<td valign="top" class="formrightside-content"><input type = 'checkbox' name = 'read_only' """+afp_readonly_checked+""" /> Read Only</td>

			<td>
			<span style="color:#585858; font-weight:600;">User Access Permission</span>
			<table>
			<tr>
				<td class="formleftside-content" style="margin-left: 0%;"><input type = 'radio' name = 'afp_priv' value = 'guest' id ="anon" onclick = 'return show_afp_users_groups();' """+guest_checked+""" > Guest</td>
			</tr>
			<tr>
				<td class="formleftside-content" style="margin-left: 0%;"><input type = 'radio' name = 'afp_priv' value = 'valid_user' id ="anon" onclick = 'return show_afp_users_groups();' """+priv_checked+""" > Authenticated User</td>
			</tr>
			</table>
			</td>

		</tr>

		</table>

		<div width = '100%' id = 'afp_users_list' style = 'display:"""+afp_users_style+""";'>
		<table width="90%" style="margin:20px 0 0 20px;">

		<tr>
		<td>
		<!--<table width="100%">
		<tr>
			<td style="background-color:#BDBDBD; height:30px; color:#000; padding:0 0 0 10px;">Authenticated User</td>
		</tr>
		</table>-->

		</td>
		</tr>

		<table width="90%" style="margin:0px 0 0 30px; ">

		<tr>
			<td class="formrightside-content">Choose Domain
		<select name = 'domainslist' >"""
		for domains in domainsarray:
			domains = domains.strip();
			print """<option value='"""+domains+"""'"""
			if(domains == get_domain_val.strip()):
				print """selected"""

			print """>"""+domains+"""</option>"""

		print """
				</select>
			</td>
			<td></td>
		</tr>

		<tr>
			<td style="padding:20px 0 0 0;">
			<b style="color:darkred;">Users List</b>
			
			<table width="100%">    
			<tr>
			<td valign="top" class="formrightside-content">Available<br/>
			<!--<input class = 'input' name = 'ftp_access_ip' id = 'id_access_ip' value = '' >
			<input type="submit" name="Check" value="Check User" />-->

		<input id = 'sssavailable' name = 'ads_user_text' type="text" class = 'input' value = '' onclick = 'document.getElementById("available").style.display = "none"; document.getElementById("available_groups").style.display = "none";'>

		<input class = 'input1' type = 'button' name = 'getusers' value = 'Check User'  onclick = 'return get_user_sugg_afp(document.getElementById("granted").options, document.getElementById("granted_groups").options, document.afp_form.read_only.checked, "no", document.afp_form.domainslist.value, this.form.sssavailable.value, "users");' >

		<div id="suggest" style="visibility:hidden;border:#000000 1px solid;width:150px;"></div>
		<select class = 'input' style = 'width: 200px; height: 300px; display: """+display_users_list+""";' id = 'available' name = 'avail_users' multiple onclick = 'return move_users(this.form.available, this.form.granted, "1");' onkeydown = 'return get_key();' >"""
		print get_users_string


		print """</select>
			</td>

			<td style="color: #666666;">
			Authorized<br/>
			<select multiple style="width:200px; height:100px;" id = 'granted' name = 'grant_users[]' onclick = "return move_users(this.form.granted, this.form.available, '2');">"""
		print users_dropdown

		#for u_val in split_vul1:
		#	if(u_val[0]!='@'):
		#		print """<option value = '""" + u_val + """' selected >""" + u_val + """</option>"""

		print """        </select>
			</td>

			</tr>
			</table>
			</td>

		</tr>

		<tr>
			<td style="padding:20px 0 0 0;">
			<b style ="color:darkred;">Groups List</b>
			
			<table width="100%">    
			<tr>
			<td valign="top" class="formrightside-content">
			Available<br/>
			<!--<input class = 'input' name = 'ftp_access_ip' id = 'id_access_ip' value = '' >
			<input type="submit" name="Check" value="Check Group" />-->

		<input id = 'ssavailable_groups' name = 'ads_group_text' type="text" class = 'input' value = '' onclick = 'document.getElementById("available_groups").style.display = "none"; document.getElementById("available").style.display = "none";'>

		<input class = 'input1' type = 'button' name = 'getgroups' value = 'Check Group'  onclick = 'return get_user_sugg_afp(document.getElementById("granted").options, document.getElementById("granted_groups").options, document.afp_form.read_only.checked, "no", document.afp_form.domainslist.value, this.form.ssavailable_groups.value, "groups");' >

		<div id="suggest" style="visibility:hidden;border:#000000 1px solid;width:150px;"></div>
		<select class = 'input' style = 'width: 200px; height: 300px; display: """+display_groups_list+""";' id = 'available_groups' name = 'avail_groups' multiple onclick = 'return move_groups(this.form.available_groups, this.form.granted_groups, "1");' onkeydown = 'return get_key();' >"""
		print get_groups_string



		print """</select>
			</td>

			<td style="color: #666666;">
			Authorized<br/>
			<!--<select multiple style="width:200px; height:100px;">
				<option></option>
			</select>-->

			<select multiple style="width:200px; height:100px;" id = 'granted_groups' name = 'grant_groups[]' onclick = "return move_groups(this.form.granted_groups, this.form.available_groups, '2');">"""
		print groups_dropdown

		print """</select>
			</td>

			</tr>
			</table>
			</td>

		</tr>


		</table>
		</div>                                                                                                         

		<table style="margin:30px 0 0 0;">
		<tr>
			<td style="color:#585858; font-weight:600;"><input type = 'checkbox'  name = 'advanced_per' onclick = 'return show_advance_per(this.checked);' """+advanced_checked+""" >  Advance Permission</td>
		</tr>
		</table>

		<div  width = '100%' id = 'afp_advanced_list' style = 'display:"""+advanced_display_style+"""; margin:20px 0 0 0;' >
		<table style="margin:0 0 0 40px; width:50%;">
		<tr>
			<td>Host Allow</td>
			<td><input type='text' name='host_allow' id='host_allow' value='"""+host_allow_val+"""'/></td>
		</tr>

		<tr>
			<td>Host Deny</td>
			<td><input type='text' name='host_deny' id='host_deny' value='"""+host_deny_val+"""' /></td>
		</tr>

		<tr>
			<td>Umask</td>
			<td><input type='text' name='umask' id='umask' value='"""+umask_val+"""'/></td>
			<input type='hidden' name='file_perm' value='"""+file_perm_val+"""' />
			<input type='hidden' name='dir_perm' value='"""+dir_perm_val+"""' />
			<input type='hidden' name='hid_share' value='"""+get_share+"""' />
			<input type='hidden' name='hid_separator' value='"""+ads_separator+"""' />

		</tr>

		</table>
		</div>"""

		if(afp_status == True):
			print """<button class="buttonClass" type = 'submit'  name="unc_action_but" value="submit_afp" style="float:right; margin:0 135px 0 0;">Unconfigure</button>
			<button class="buttonClass" type = 'submit'  name="action_but" value="submit_afp" onclick = "return validate_dns_conf();" style="float:right; margin:0 10px 0 0;">Re-configure</button>"""
		else:
			print """<button class="buttonClass" type = 'submit'  name="action_but" value="submit_afp" onclick = "return validate_dns_conf();" style="float:right;  margin:0 135px 0 0;">Configure</button>"""
			


		print """</table>



		</form>"""


	print """
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
