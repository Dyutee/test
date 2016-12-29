#!/usr/bin/python
import cgitb, sys, include_files, cgi
cgitb.enable()
form = cgi.FieldStorage()
sys.path.append('../modules/')
import disp_except;

sys.path.append("/var/nasexe/python/")
import authentication
import fs2nis
import ads
import openldap

try:
	###########################################
        ############# import modules ##############
        ###########################################
	import os, commands, string
	sys.path.append('/var/www/fs4/py/')
	import common_methods
	image_icon = common_methods.getimageicon()
	sys.path.append('/var/nasexe/python/')
	import ads, fs2nis, manage_users

	session_user = common_methods.get_session_user();

	hiduserslist = 'No Local Users';
	local_users_list  = manage_users.get_smb_users();

	if(local_users_list["id"] == 2):
		local_users_list = {'id': 2, 'desc': 'ERROR: Unable to get all SMB system users.', 'users':''} 
	localusersarray = local_users_list['users'];
	sizeoflocalusersarray = len(localusersarray);

	if (local_users_list['users'] != []):
		hiduserslist = local_users_list['users'];

	if (session_user != ''):
		if(form.getvalue("execution")):
			get_execution = form.getvalue("execution")
			get_execvalue = form.getvalue("execval")
			if(get_execution == "success"):
				print"<div id = 'id_trace'>"
				print get_execvalue
				print "</div>"
			else:
				print"""<div id = 'id_trace_err'>"""
				print get_execvalue
				print "</div>"

	####### Read IP & Domain values from 'nis_connect' file #######
	ip_value = ''
	domain_value = ''
	read_nis_connect_file = open('nis_connect', 'r')
	for line in read_nis_connect_file:
		if(line != ''):
			split_line = string.split(line)
			ip_value = split_line[0]
			domain_value = split_line[1]
		else:
			ip_value = ''
			domain_value = ''
	read_nis_connect_file.close()
	####### End #######     

	####### Read Username, Password, FQDN & DNS values from 'ads_connect' file #######
	user_value = ''
	pass_value = ''
	fqdn_value = ''
	dns_value = ''
	read_ads_connect_file = open('ads_connect', 'r')
	for line in read_ads_connect_file:
		if(line != ''):
			split_ads_line = string.split(line)
			user_value = split_ads_line[0]
			pass_value = ''
			fqdn_value = split_ads_line[2]
			dns_value = split_ads_line[3]
		else:
			user_value = ''
			pass_value = ''
			fqdn_value = ''
			dns_value = ''
	read_ads_connect_file.close()
	####### End #######

	############################################
	############# Default Values ###############
	############################################
	get_ldap_infos = {'admindn': '', 'ldapservername': '', 'portno': '', 'sambadomainname': '', 'ldapserverip': '', 'ldapversion': '3', 'ldapgroupsuffix': '', 'sambaadminpasswd': '', 'ldapusersuffix': '', 'ssl': False, 'ldapidmapsuffix': '', 'sambaadminuser': '', 'sambaserverip': '', 'adminpasswd': '', 'searchbase': '', 'ldapmachinesuffix': '', 'sambaservername': '', 'sysdomainname': ''}
	get_ads_val = {'admin_passwd': '', 'admin_user': '', 'domain': '', 'dns_ip': ''}

	############################################
	###### Get Authentication Type Start #######
	############################################
	get_auth_type = authentication.get_auth_type()
	if(get_auth_type["status"] == True):
		if(get_auth_type["type"] == "nis"):
			get_nis_val = fs2nis.get_nis_info()
			ip_value = get_nis_val["server_ip"]
			domain_value = get_nis_val["domain_name"]

			display_local = "none"
                	display_nis = "block"
                	display_ads = "none"
	                display_ldap = "none"
	                display_ldap_adv = "none"
	                check_ldap_adv = ''
        	        check_local = ''
                	check_nis = "checked = checked"
                	check_ads = ''
			check_ldap = ''

		elif(get_auth_type["type"] == "ads"):
			get_ads_val = ads.get_infos()
			user_value = get_ads_val["admin_user"]
                        pass_value = get_ads_val["admin_passwd"]
                        fqdn_value = get_ads_val["domain"]
                        dns_value = get_ads_val["dns_ip"]

			display_local = "none"
			display_nis = "none"
			display_ads = "block"
			display_ldap = "none"
	                display_ldap_adv = "none"
	                check_ldap_adv = ''
			check_local = ''
			check_nis = ''
			check_ads = "checked = checked"
			check_ldap = ''

		elif(get_auth_type["type"] == "local"):
			display_local = "block"
			display_nis = "none"
			display_ads = "none"
			display_ldap = "none"
	                display_ldap_adv = "none"
	                check_ldap_adv = ''
			check_local = "checked = checked"
			check_nis = ''
			check_ads = ''
			check_ldap = ''

		elif(get_auth_type["type"] == "ldap"):
			get_ldap_infos = openldap.get_infos()
			display_local = "none"
			display_nis = "none"
			display_ads = "none"
			display_ldap = "block"
	                display_ldap_adv = "block"
	                check_ldap_adv = "checked = checked"
			check_local = ''
			check_nis = ''
			check_ads = ''
			check_ldap = "checked = checked"

	if(get_auth_type["status"] == False):
		if(get_auth_type["type"] == "nis"):
			get_nis_val = fs2nis.get_nis_info()
			ip_value = get_nis_val["server_ip"]
			domain_value = get_nis_val["domain_name"]

			display_local = "none"
                	display_nis = "block"
                	display_ads = "none"
	                display_ldap = "none"
	                display_ldap_adv = "none"
	                check_ldap_adv = ''
        	        check_local = ''
                	check_nis = "checked = checked"
                	check_ads = ''
			check_ldap = ''

		elif(get_auth_type["type"] == "ads"):
			get_ads_val = ads.get_infos()
			user_value = get_ads_val["admin_user"]
                        pass_value = get_ads_val["admin_passwd"]
                        fqdn_value = get_ads_val["domain"]
                        dns_value = get_ads_val["dns_ip"]

			display_local = "none"
			display_nis = "none"
			display_ads = "block"
			display_ldap = "none"
	                display_ldap_adv = "none"
	                check_ldap_adv = ''
			check_local = ''
			check_nis = ''
			check_ads = "checked = checked"
			check_ldap = ''

		elif(get_auth_type["type"] == "local"):
			display_local = "block"
			display_nis = "none"
			display_ads = "none"
			display_ldap = "none"
	                display_ldap_adv = "none"
	                check_ldap_adv = ''
			check_local = "checked = checked"
			check_nis = ''
			check_ads = ''
			check_ldap = ''

		elif(get_auth_type["type"] == "ldap"):
			get_ldap_infos = openldap.get_infos()
			display_local = "none"
			display_nis = "none"
			display_ads = "none"
			display_ldap = "block"
	                display_ldap_adv = "block"
	                check_ldap_adv = "checked = checked"
			check_local = ''
			check_nis = ''
			check_ads = ''
			check_ldap = "checked = checked"
	############################################
	####### Get Authentication Type End ########
	############################################


	print common_methods.wait_for_response;

	sys.path.append("/var/nasexe/python/")
        import tools

	check_ha = tools.check_ha()

        from tools import db
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

	if(form.getvalue("testaction")):
		print """<iframe src='https://192.168.0.59/fs4/py/testaction.py' style="width:795px; border:none; min-height: 500px; height:auto !important; height: 500px;" ></iframe>"""

	#print 'Content-Type: text/html'
	print
	if not get_auth_type["status"]:
		print """<div id="error_div" style="text-align:center; background:#FA5858; border:#FE2E2E 1px solid; width:94%; padding:7px; float:right; margin:5px 5px 0 0; color:#FFF; cursor:pointer;" onclick="return clicking_div();">Configured to """+get_auth_type["type"]+""" but connection is not active! <span title="close" style="float:right;">X</span></div>"""
	elif get_auth_type["status"] and get_auth_type["type"] != "local":
		print """<div id="error_div" style="text-align:center; background:#31B404; border:#298A08 1px solid; width:94%; padding:7px; float:right; margin:5px 5px 0 0; color:#FFF; cursor:pointer;" onclick="return clicking_div();">"""+get_auth_type["type"]+""" connection is active! <span title="close" style="float:right; color:#000;">X</span></div>"""
	print """
		<div id="loader-div" style="text-align:center; display:none;" ><img style="margin-top:20%;" src="../images/ajax-loader.gif" /><br/> Loading...</div>
	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer" id="body-div">
		<!--tab srt-->
		<div class="searchresult-container">
		<div style="margin:0 0 0px 0;" class="topinputwrap-heading">
		<a class="demo" href ="#"><img src ="../images/help_icon1.png" style="width:13px;"><span class="tooltip" >
                 <table border="0">
        <tr>     
        <td class="text_css">This page lets you configure different authentication methods for NAS shares.</td>
        </tr>
        </table>"""
	if(check_ha == True):
		print"""
			</span></a> Authentication ("""+show_tn+""")
                <span style="float:right; margin:0;"><a onclick="return onclick_loader();" class="resource_links" href="https://"""+other_node_ip+"""/fs4/py/iframe_copy_authentication.py">"""+show_on+"""</a></span>
                        </div>"""
	else:
		print"""
                        </span></a><p class = "gap_text">Authentication</p></div>"""
	print"""
		  <div class="infoheader">
		    <div id="tabs">
		      <ul style="display:none;">
			<li><a href="#tabs-1">Authentication Method</a></li>
		      </ul>
		      <div id="tabs-1">

		<!--form container starts here-->

		<form name = 'setup_auth' method = 'POST' action='nis_auth.py'>
		<div class="form-container" style="border:none;">
		  <!--<div class="topinputwrap-heading">Choose a Server for Authentication</div>-->
		<div class="inputwrap">
		<input type = 'radio' """+check_local+""" name = 'auth_type'  value = 'Local' onclick = "return choose_option('local');" style="margin:0 0 0 5px;color: #666666;"> Local Server<br/><br/>
		<input type = 'radio' """+check_nis+""" name = 'auth_type'  value = 'NIS' onclick = "return choose_option('nis');" style="margin:0 0 0 5px;color: #666666;"> Network Information Server (NIS)<br/><br/>
		<input type = 'radio' """+check_ads+""" name = 'auth_type'  value = 'ADS/DC' onclick = "return choose_option('adc');" style="margin:0 0 0 5px;color: #666666;"> Active Directory Server (ADS/DC)<br/><br/>
		<input type = 'radio' """+check_ldap+""" name = 'auth_type'  value = 'LDAP' onclick = "return choose_option('ldap');" style="margin:0 0 0 5px;color: #666666;"> LDAP

	<!-- ####### LOCAL AUTHENTICATION START ####### -->
		
		<table align = 'right' id = 'local_auth_table' style = 'margin:30px 300px 20px 0; border:#BDBDBD 1px solid; display:"""+display_local+"""; '>
		<tr>
		<td>

		<table width="300">
		<tr>
		<td style="background-color:#BDBDBD; height:30px; color:#000; padding:0 0 0 10px;">Local Authentication</td>
		</tr>

		<tr>
		<td>

		<table width="300" style="padding:0 0 0 10px;">
		<tr>
		<td></td>
		<td><button class="buttonClass" type="submit" name = 'local_action_but'  id = 'local_action_but' value = 'Apply'  onclick = 'validate_local_auth();'>Apply</button> </td>
		</tr>
		</table>

		</tr>
		</table>

		</td>
		</tr>
		</table>

	<!-- ####### LOCAL AUTHENTICATION ENDS ####### -->

	<!-- ####### NIS AUTHENTICATION START ####### -->
		
		<table align = 'right' id = 'nis_auth_table' style = 'margin:30px 300px 20px 0; border:#BDBDBD 1px solid; display:"""+display_nis+"""; '>
		<tr>
		<td>

		<table width="300">
		<tr>
		<td style="background-color:#BDBDBD; height:30px; color:#000; padding:0 0 0 10px;">NIS Authentication</td>
		</tr>

		<tr>
		<td>

		<table width="300" style="padding:0 0 0 10px;">
		<tr>
		<td width="30%">IP</td>
		<td> <input class='textbox' type='text' name='ip_add' value='"""+ip_value+"""' /></td>
		<input class='textbox' type='hidden' name='ip_add_hid' value='"""+ip_value+"""' />
		</tr>

		<tr>
		<td>Domain</td>
		<td> <input class='textbox' type='text' name='domain' value='"""+domain_value+"""' /></td>
		<input class='textbox' type='hidden' name='domain_hid' value='"""+domain_value+"""' />
		</tr>

		<tr>
		<td></td>
		<td><button class="buttonClass" type = 'submit' name = 'nis_action_but' value = 'Apply' onclick = 'return validate_new_nis_form(\"""" + str(sizeoflocalusersarray) + """");'>Apply</button> 

		<button class="buttonClass" type = 'button' onclick = 'return auth_reset("nis");' name = 'rnis_reset' value = 'Reset NIS Values' style ="width:87px;">Reset</button></td>
		</tr>
		</table>

		</tr>
		</table>

		</td>
		</tr>
		</table>

	<!-- ####### NIS AUTHENTICATION ENDS ####### -->

	<!-- ####### ADS AUTHENTICATION START ####### -->
		
		<table align = 'right' id = 'ads_auth_table' style = 'margin:30px 300px 20px 0; border:#BDBDBD 1px solid; display:"""+display_ads+"""; '
		<tr>
		<td>

		<table width="300">
		<tr>
		<td style="background-color:#BDBDBD; height:30px; color:#000; padding:0 0 0 10px;">ADS Authentication</td>
		</tr>

		<tr>
		<td>

		<table width="300" style="padding:0 0 0 10px;">
		<tr>
		<td width="30%">Username</td>
		<td><input class='textbox' type = 'text' name = 'username' id = 'username' value = '"""+user_value+"""' /></td>
		<input class='textbox' type = 'hidden' name = 'u_hid' value = '"""+user_value+"""' />
		</tr>

		<tr>
		<td>Password</td>
		<td><input class='textbox' type = 'password' name = 'password' id = 'password' value = '"""+pass_value+"""' /></td>
		<input class='textbox' type = 'hidden' name = 'p_hid' value = '"""+pass_value+"""' />
		</tr>

		<tr>
		<td width="30%">FQDN</td>
		<td><input class='textbox' type = 'text' name = 'fqn' id = 'fqn' value = '"""+fqdn_value+"""' ></td>
		<input class='textbox' type = 'hidden' name = 'f_hid' value = '"""+fqdn_value+"""' >
		</tr>

		<tr>
		<td>DNS</td>
		<td><input class='textbox' type = 'text' name = 'dns' id = 'dns' value = '"""+dns_value+"""' ></td>
		<input class='textbox' type = 'hidden' name = 'd_hid' value = '"""+dns_value+"""' >
		</tr>

		<tr>
		<td></td>
		<td><button class="buttonClass" type = 'submit' name = 'ads_action_but' value = 'Apply' onclick = 'return validate_ads_form(\"""" + str(sizeoflocalusersarray) + """");'>Apply</button>

		<button class="buttonClass" type = 'button' onclick = 'return auth_reset("ads");'  name = 'ads_reset' value = 'Reset ADS connection' style="width:87px;">Reset</button></td>
		</tr>
		</table>

		</tr>
		</table>

		</td>
		</tr>
		</table>
		
		<input type = 'hidden' name = 'hid_ads_connection' value = ''>
		<input type = 'hidden' name = 'hid_nis_connection' value = ''>
		<input type = 'hidden' name = 'hid_users_present' value = ''>

	<!-- ####### ADS AUTHENTICATION ENDS ####### -->

	<!-- ####### LDAP AUTHENTICATION START ####### -->
		
		<table align = 'right' id = 'ldap_auth_table' style = 'margin:30px 100px 20px 0; border:#BDBDBD 1px solid; display:"""+display_ldap+"""; '>
		<tr>
		<td>

		<table width="500">
		<tr>
		<td style="background-color:#BDBDBD; height:30px; color:#000; padding:0 0 0 10px;">LDAP Authentication</td>
		</tr>

		<tr>
		<td>

		<table width="500" style="padding:0 0 0 10px;">
		<tr>
		<td width="30%">LDAP Server IP address</td>
		<td> <input class='textbox' type='text' name='ldapserverip' id='lsipa' value='"""+get_ldap_infos["ldapserverip"]+"""' style="width:187px;"/></td>
		<input class='textbox' type='hidden' name='ldapserverip_hid' value='"""+get_ldap_infos["ldapserverip"]+"""'/>
		</tr>

		<tr>
		<td width="40%">LDAP Server Name</td>
		<td> <input class='textbox' type='text' name='ldapservername' id='lsn' value='"""+get_ldap_infos["ldapservername"]+"""' style="width:187px;"/></td>
		<input class='textbox' type='hidden' name='ldapservername_hid' value='"""+get_ldap_infos["ldapservername"]+"""' />
		</tr>

		<tr>
		<td>Search Base</td>
		<td> <input class='textbox' type='text' name='searchbase' value='"""+get_ldap_infos["searchbase"]+"""' style="width:187px;"/></td>
		<input class='textbox' type='hidden' name='searchbase_hid' value='"""+get_ldap_infos["searchbase"]+"""' />
		</tr>

		<tr>
		<td>Admin DN</td>
		<td> <input class='textbox' type='text' name='admindn' value='"""+get_ldap_infos["admindn"]+"""' style="width:187px;"/></td>
		<input class='textbox' type='hidden' name='admindn_hid' value='"""+get_ldap_infos["admindn"]+"""' />
		</tr>

		<tr>
		<td>Admin Password</td>
		<td> <input class='textbox' type='password' name='adminpasswd' value='"""+get_ldap_infos["adminpasswd"]+"""' style="width:187px;"/></td>
		<input class='textbox' type='hidden' name='adminpasswd_hid' value='"""+get_ldap_infos["adminpasswd"]+"""' />
		</tr>

		<tr>
		<td>Samba Server IP Address</td>
		<td> <input class='textbox' type='text' name='sambaserverip' id='ssipa' value='"""+get_ldap_infos["sambaserverip"]+"""' style="width:187px;"/> 
		<input class='textbox' type='hidden' name='sambaserverip_hid' value='"""+get_ldap_infos["sambaserverip"]+"""' /> 
		<a style="background-color:#58ACFA; padding:3px; color:#FFF; cursor:pointer; font-size:10px; border:#2E9AFE 1px solid;" onclick="return copy_textbox_content('lsipa','ssipa');">Same as LDAP</a>
		</td>
		</tr>

		<tr>
		<td>Samba Server Name</td>
		<td> <input class='textbox' type='text' name='sambaservername' id='ssn' value='"""+get_ldap_infos["sambaservername"]+"""' style="width:187px;"/>
		<input class='textbox' type='hidden' name='sambaservername_hid' value='"""+get_ldap_infos["sambaservername"]+"""' "/>
		<a style="background-color:#58ACFA; padding:3px; color:#FFF; cursor:pointer; font-size:10px; border:#2E9AFE 1px solid;" onclick="return copy_textbox_content('lsn','ssn');">Same as LDAP</a>
		</td>
		</tr>

		<tr>
		<td>Samba Admin User</td>
		<td> <input class='textbox' type='text' name='sambaadminuser' value='"""+get_ldap_infos["sambaadminuser"]+"""' style="width:187px;"/></td>
		<input class='textbox' type='hidden' name='sambaadminuser_hid' value='"""+get_ldap_infos["sambaadminuser"]+"""' />
		</tr>

		<tr>
		<td>Samba Admin Password</td>
		<td> <input class='textbox' type='password' name='sambaadminpasswd' value='"""+get_ldap_infos["sambaadminpasswd"]+"""' style="width:187px;"/></td>
		<input class='textbox' type='hidden' name='sambaadminpasswd_hid' value='"""+get_ldap_infos["sambaadminpasswd"]+"""' />
		</tr>

		<tr>
		<td>Samba Domain Name</td>
		<td> <input class='textbox' type='text' name='sambadomainname' value='"""+get_ldap_infos["sambadomainname"]+"""' style="width:187px;"/></td>
		<input class='textbox' type='hidden' name='sambadomainname_hid' value='"""+get_ldap_infos["sambadomainname"]+"""'/></td>
		</tr>

		<tr>
		<td>System Domain Name</td>
		<td> <input class='textbox' type='text' name='sysdomainname' value='"""+get_ldap_infos["sysdomainname"]+"""' style="width:187px;"/></td>
		<input class='textbox' type='hidden' name='sysdomainname_hid' value='"""+get_ldap_infos["sysdomainname"]+"""' />
		</tr>

		<tr>
		<td><input type="checkbox" name="advance_option" id="advance_option" """+check_ldap_adv+""" onclick="return adv_option_show();"> <strong>Advanced Options</strong></td>
		<td> </td>
		</tr>

		</table>
		</td>
		</tr>

		<tr>
		<td>
		<table width="400px" style="margin:0 0 0 100px; display:"""+display_ldap_adv+""";" id="adv_option_table">
		<tr>
		<td width="50%">Port No</td>
		<td><input class='textbox' type='text' name='portno' value='"""+get_ldap_infos["portno"]+"""' style="width:187px;"/></td>
		<input class='textbox' type='hidden' name='portno_hid' value='"""+get_ldap_infos["portno"]+"""' />
		</tr>

		<tr>
		<td width="30%">SSL</td>
		<td>
		<div class="styled-select2">
		<select name="ssl">
		<option value='True'"""
	if(get_ldap_infos["ssl"] == True):
		print "selected"

	print """>True</option>
		<option value="False" selected>False</option>
		</select>
		</div>
		</td>
		<input class='textbox' type='hidden' name='ssl_hid' value='"""+str(get_ldap_infos["ssl"])+"""' />
		</tr>

		<tr>
		<td width="30%">LDAP User Suffix</td>
		<td><input class='textbox' type='text' name='ldapusersuffix' value='"""+get_ldap_infos["ldapusersuffix"]+"""' style="width:187px;" /></td>
		<input class='textbox' type='hidden' name='ldapusersuffix_hid' value='"""+get_ldap_infos["ldapusersuffix"]+"""' />
		</tr>

		<tr>
		<td width="30%">LDAP Group Suffix</td>
		<td><input class='textbox' type='text' name='ldapgroupsuffix' value='"""+get_ldap_infos["ldapgroupsuffix"]+"""' style="width:187px;"/></td>
		<input class='textbox' type='hidden' name='ldapgroupsuffix_hid' value='"""+get_ldap_infos["ldapgroupsuffix"]+"""' />
		</tr>

		<tr>
		<td width="30%">LDAP Machine Suffix</td>
		<td><input class='textbox' type='text' name='ldapmachinesuffix' value='"""+get_ldap_infos["ldapmachinesuffix"]+"""' style="width:187px;"/></td>
		<input class='textbox' type='hidden' name='ldapmachinesuffix_hid' value='"""+get_ldap_infos["ldapmachinesuffix"]+"""' />
		</tr>

		<tr>
		<td width="30%">LDAP IDMAP Suffix</td>
		<td><input class='textbox' type='text' name='ldapidmapsuffix' value='"""+get_ldap_infos["ldapidmapsuffix"]+"""' style="width:187px;"/></td>
		<input class='textbox' type='hidden' name='ldapidmapsuffix_hid' value='"""+get_ldap_infos["ldapidmapsuffix"]+"""'/>
		</tr>

		<tr>
		<td width="30%">LDAP Version</td>
		<td><input class='textbox' type='text' name='ldapversion' value='3' readonly style="width:187px;"/></td>
		</tr>

		</table>
		</td>
		</tr>

		<tr><td>
		<table width="400px" style="margin:20px 0 0 160px;">
		<tr>
		<td></td>
		<td>
		<button class="buttonClass" type = 'button' onclick = 'return auth_reset("ldap");' style="float:right; margin:0 160px 0 0;" name = 'ldap_reset' value = 'ldap_reset'>Reset</button>
		<button class="buttonClass" type = 'submit' name = 'ldap_action_but' value = 'ldap_action_but' style="float:right; margin:0 7px 0 0;" onclick="return validate_ldap_form();">Apply</button> 

		</td>
		</tr>
		</table>
		</td></tr>

		</table>

		</td>
		</tr>
		</table>

	<!-- ####### LDAP AUTHENTICATION ENDS ####### -->

		</div>
		</div>
		</form>
		<!--form container ends here-->
		<p>&nbsp;</p>
		      </div>
		    </div>
		  </div>
		</div>
	"""
except Exception as e:
        disp_except.display_exception(e);
