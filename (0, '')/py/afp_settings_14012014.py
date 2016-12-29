#!/usr/bin/python
import cgitb, sys, header, common_methods, string, os
cgitb.enable()


sys.path.append('/var/nasexe/python/')
import tools
from fs2global import *
import afp

#print 'Content-Type: text/html'

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

get_share = header.form.getvalue("share_name")
domainsarray = common_methods.get_all_domains()

get_sharess = tools.get_all_shares(debug=True)
for x in get_sharess["shares"]:
	if x["name"] == get_share:
		selected_share =  x["name"]
		selected_share_path = x["path"]

#print selected_share
#print selected_share_path 

get_users_string = ''


#------------------------------------ Configure AFP New Start ----------------------------------------#
if(header.form.getvalue('action_but')):
	afp_read_only = header.form.getvalue('read_only')
	permission_type = header.form.getvalue('afp_priv')
	afp_advance = header.form.getvalue('advanced_per')
	afp_host_allow = header.form.getvalue('host_allow')
	afp_host_deny = header.form.getvalue('host_deny')
	afp_umask = header.form.getvalue('umask')
	afp_file_perm = header.form.getvalue('file_perm')
	afp_dir_perm = header.form.getvalue('dir_perm')
	afp_grant_users = header.form.getvalue('grant_users[]')
	afp_grant_groups = header.form.getvalue('grant_groups[]')
	
	afp_file_perm = "0755"
	afp_dir_perm = "0755"

	dict_value = {'afp_read_only':afp_read_only, 'permission_type':permission_type, 'afp_advance':afp_advance, 'afp_host_allow':afp_host_allow, 'afp_host_deny':afp_host_deny, 'afp_umask':afp_umask, 'afp_file_perm':afp_file_perm, 'afp_dir_perm':afp_dir_perm, 'afp_grant_users':afp_grant_users, 'afp_grant_groups':afp_grant_groups, 'selected_share':selected_share, 'selected_share_path':selected_share_path}

	print dict_value
	
	conf_afp_cmd = afp.configure(dict_value)
	if(conf_afp_cmd == None):
		print "<div id='id_trace'>"
		print "AFP configured successfully!"
		print "</div>"
#------------------------------------ Configure AFP New End ----------------------------------------#

#------------------------------------ Unconfigure AFP New Start ----------------------------------------#
if(header.form.getvalue("unc_action_but")):
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

assusrfile = 'assusersfile';
assgrpfile = 'assgroupsfile';

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

if(header.form.getvalue("ro")):
	read_only_val = header.form.getvalue("ro")

if(read_only_val == "true"):
	check_ro = "checked"

if(header.form.getvalue("dom")):
	get_domain_val = header.form.getvalue("dom")
	#print get_domain_val

if (ug != ''):
        validuser_checked = 'checked';

        assusrarray = common_methods.read_file(assusrfile);
        assgrparray = common_methods.read_file(assgrpfile);

        if (len(assusrarray) > 0):
                for assu in assusrarray:
                        #assu_internal = common_methods.replace_chars(assu, 'chartotext');
                        assu = assu.replace('%20', ' ');
                        assu = assu.strip();

                        assu_internal = assu;
                        disp_assu     = assu[assu.find('+') + 1:];

                        users_dropdown += '<option value = "' + assu_internal + '" selected>' + disp_assu + '</option>';

        if (len(assgrparray) > 0):
                for assg in assgrparray:
                        #assg_internal = common_methods.replace_chars(assg, 'chartotext');
                        assg = assg.replace('%20', ' ');
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
                get_users_array = common_methods.read_file('searchusersfile.txt');


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
		get_groups_array = common_methods.read_file('searchgroupsfile.txt');

		for get_groups in get_groups_array:
			if (get_groups != ''):
				get_groups = get_groups.strip();

				get_groupsinternal = common_methods.replace_chars(get_groups, 'chartotext');
				get_disp_groups    = get_groups[get_groups.find('\\') + 1:];

				if (get_groups not in ftp_groups_list):
					get_groups_string += '<option value = "' + get_groupsinternal + '">' + get_disp_groups + '</option>';



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
	


import left_nav
print
print """

      <!--Right side body content starts from here-->
      <div class="rightsidecontainer">
	<div class="insidepage-heading">Nas >> <span class="content">Configure Information</span></div>
	<!--tab srt-->
	<div class="searchresult-container">
	  <div class="infoheader">
	    <div id="tabs">
	      <ul>
		<li><a href="#tabs-1">AFP Settings</a></li>
	      </ul>
	      <div id="tabs-1">

	<!--form container starts here-->
	<div class="form-container">
	<div style="padding:5px; background-color:#e9e5e5; border-bottom:#D1D1D1 1px solid; font-weight:bold;">AFP Settings for '"""+get_share+"""' <a href = 'main.py?page=cs'><img style="float:right; padding:0 10px 2px 0;" title = 'Back to shares' src = '../images/gobacktoshares.png' /></a></div>

	  <div class="topinputwrap">


<form name = 'afp_form' method = 'POST' action='' onsubmit = 'return validate_share_afp();' >
<table width="100%" style="padding:20px 0 0 0;">

<tr>
        <td valign="top" style="color:#585858; font-weight:600;"><input type = 'checkbox' name = 'read_only' """+afp_readonly_checked+""" /> Read Only</td>

        <td>
        <strong>User Access Permission</strong>
        <table>
        <tr>
                <td><input type = 'radio' name = 'afp_priv' value = 'guest' id ="anon" onclick = 'return show_afp_users_groups();' """+guest_checked+""" > Guest</td>
        </tr>
        <tr>
                <td><input type = 'radio' name = 'afp_priv' value = 'valid_user' id ="anon" onclick = 'return show_afp_users_groups();' """+priv_checked+""" > Authenticated User</td>
        </tr>
        </table>
        </td>

</tr>

</table>

<div width = '100%' id = 'afp_users_list' style = 'display:"""+afp_users_style+""";'>
<table width="90%" style="margin:20px 0 0 20px;">

<tr>
<td>
<table width="100%">
<tr>
        <td style="background-color:#BDBDBD; height:30px; color:#000; padding:0 0 0 10px;">Authenticated User</td>
</tr>
</table>

</td>
</tr>

<table width="90%" style="margin:0px 0 0 30px; ">

<tr>
        <td>Choose Domain
<select name = 'domainslist' >
<option>Select a Domain</option>"""
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
        <strong>Users List</strong>
        
        <table width="100%">    
        <tr>
        <td valign="top">
        Available<br/>
        <!--<input class = 'input' name = 'ftp_access_ip' id = 'id_access_ip' value = '' >
        <input type="submit" name="Check" value="Check User" />-->

<input id = 'sssavailable' name = 'ads_user_text' type="text" class = 'input' value = '' onclick = 'document.getElementById("available").style.display = "none"; document.getElementById("available_groups").style.display = "none";'>

<input class = 'input1' type = 'button' name = 'getusers' value = 'Check User'  onclick = 'return get_user_sugg_afp(document.getElementById("granted").options, document.getElementById("granted_groups").options, document.afp_form.read_only.checked, "no", document.afp_form.domainslist.value, this.form.sssavailable.value, "users");' >

<div id="suggest" style="visibility:hidden;border:#000000 1px solid;width:150px;"></div>
<select class = 'input' style = 'width: 200px; height: 300px; display: """+display_users_list+""";' id = 'available' name = 'avail_users' multiple onclick = 'return move_users(this.form.available, this.form.granted, "1");' onkeydown = 'return get_key();' >"""
print get_users_string


print """</select>
        </td>

        <td>
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
        <strong>Groups List</strong>
        
        <table width="100%">    
        <tr>
        <td valign="top">
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

        <td>
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
</div>

<button class="button_example" type = 'submit'  name="unc_action_but" value="submit_afp" style="float:right; margin:20px 100px 20px 0;">Unconfigure</button>
<button class="button_example" type = 'submit'  name="action_but" value="submit_afp" onclick = "return validate_dns_conf();" style="float:right; margin:20px 10px 20px 0;">Configure</button>


</table>



        </form>
         </div>
</div>
<!--form container ends here-->
<p>&nbsp;</p>
      </div>

  </div>
</div>
</div>
<!--form container ends here-->
<!--form container starts here-->
<!--form container ends here-->
</div>
<!--Right side body content ends here-->
</div>
<!--Footer starts from here-->
<div class="insidefooter footer_content">&copy; 2013 Opslag FS2</div>
<!-- Footer ends here-->
</div>
<!--inside body wrapper end-->
</div>
<!--body wrapper end-->
</body>
</html>
"""
