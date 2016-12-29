#!/usr/bin/python
import cgitb, sys, header, common_methods, os
cgitb.enable()

sys.path.append('/var/nasexe/python/');
import smb, tools
from tools import acl
from fs2global import *;


#print 'Content-Type: text/html'
import left_nav

get_share = '';
sharepath = '';
grant_user = ''
set_path = ''
read_check =''
read_per = ''
write_check = ''
execute_check = ''
write_per = ''
execute_per = ''
display_rwx = "none"
display_acl_but = "none"
owner_name = ''
group_name = ''
path_owner = ''
reset_chk_but = ''
reset_chk = ''
alldisabled = '';
ads_separator = '';

ads_separator = tools.get_ads_separator();

domainsarray = [];
domainname = '';
avail_users_style = 'none';
users_from_list = [];
groups_from_list = [];
recr_val = ''
recur_info = ''
ug = '';
get_users_string = '';
get_groups_string = '';
"""
get_hid_k_val = header.form.getvalue("hid_k_val")
l=1
while(l<int(get_hid_k_val)):
	#print l
	#if(header.form.getvalue('o_read'+str(l)) == ""):
		#globals()["checked_read" + str(l)] = ""
		#print sanjeev
	chk = "checked_read"+str(l)
	if(chk == "checked_read"+str(l)):
		print chk

	l=l+1
"""
smbuserslength  = 0;
smbgroupslength = 0

assusrfile = 'aclassusersfile';
assgrpfile = 'aclassgroupsfile';

sys.path.append('/var/nasexe/python/')
import manage_users

#############Display for User And Group Code ##############
get_all_users = manage_users.get_smb_users()

get_all_groups = manage_users.get_sys_groups()
#print get_all_groups

############ get auth mode and get all users##############
connstatus = common_methods.conn_status();

domainsarray = common_methods.get_all_domains();

all_users_list  = common_methods.get_users_string();
all_groups_list = common_methods.get_groups_string();

smb_all_users_array  = [];
smb_all_groups_array = [];

# if userslist is not empty
if (all_users_list['id'] == 0):
	smb_all_users_array  = all_users_list['users'];
        smbuserslength       = len(smb_all_users_array);

# if groupslist id not empty
if (all_groups_list['id'] == 0):
	smb_all_groups_array = all_groups_list['groups'];
        smbgroupslength      = len(smb_all_groups_array);
#########End############################################

user_group_list = [];

for user_lst in get_all_users['users']:
	user_name = '[U]'+str(user_lst)
	#print user_name
	
	user_group_list.append(user_name);
#print '<br/>'
#print get_all_groups
for group_lst  in get_all_groups['groups']:
	group_name = '[G]'+str(group_lst)
	user_group_list.append(group_name)
#print get_all_users
#for t in user_group_list:
#	print t

################End########################################

################Get Log Path#############################
querystring = os.environ['QUERY_STRING'];

if (querystring.find('share_name=') >= 0):
	if (querystring.find('&dom=') > 0):
		get_share = querystring[querystring.find('share_name=') + len('share_name='):querystring.find('&dom=')];

	else:
		get_share = querystring[querystring.find('share_name=') + len('share_name='):];
###################End##################################
#sharepath = '';

###############This code use for Check Option##########
if (querystring.find('ug=') >= 0):
        ug = querystring[querystring.find('ug=') + len('ug='):querystring.find('&share_name')];

if (ug != ''):
	validuser_checked = 'checked';

	assusrarray = common_methods.read_file(assusrfile);
	assgrparray = common_methods.read_file(assgrpfile);

	if (len(assusrarray) > 0):
		for assu in assusrarray:
			assu = assu.replace('%20', ' ');
			assu = assu.strip();

			assu_internal = assu;
			disp_assu = assu;

			users_from_list.append(assu);
			#user_name.append(assu);

	if (len(assgrparray) > 0):
		for assg in assgrparray:
			assg = assg.replace('%20', ' ');
			assg = assg.strip();

			assg_internal = assg;

			groups_from_list.append(assg);

	domainname = querystring[querystring.find('&dom=') + len('&dom='):];
	domainname = domainname.strip();

	tempstring = '';

	if (len(groups_from_list) > 0):
		for gfl in groups_from_list:
			tempstring += gfl + ':::';

	tempstring = tempstring.strip();
	tempstring = ':::' + tempstring;

	if (ug == 'users'):
		avail_users_style = 'block';

		get_users_array = [];
		get_users_array = common_methods.read_file('aclsearchusersfile.txt');

		get_users_array = list(set(get_users_array) - set(groups_from_list));

		for get_users in get_users_array:
			if (get_users != ''):
				get_users = get_users.strip();
				get_users = '[U]' + get_users;

				checkuserexists = tempstring.find(':::' + get_users + ':::');
				get_usersinternal = common_methods.replace_chars(get_users, 'chartotext');
				get_disp_users    = get_users[get_users.find('\\') + 1:];

				check_users = '"' + get_users + '"';
				
				if (checkuserexists < 0):
					get_users_string += '<option value = "' + get_usersinternal + '">' + get_disp_users + '</option>';

	if (ug == 'groups'):
		avail_users_style = 'block';

		get_groups_array = [];
		get_groups_array = common_methods.read_file('aclsearchgroupsfile.txt');

		for get_groups in get_groups_array:
			if (get_groups != ''):
				get_groups = get_groups.strip();
				get_groups = '[G]' + get_groups;

				checkuserexists = tempstring.find(':::' + get_groups + ':::');
				get_groupsinternal = common_methods.replace_chars(get_groups, 'chartotext');
				get_disp_groups    = get_groups[get_groups.find('\\') + 1:];

				if (checkuserexists < 0):
					get_groups_string += '<option value = "' + get_groupsinternal + '">' + get_disp_groups + '</option>';

sharedetails = tools.get_share(get_share);

assgroupsarray = [];
assgroupsarray = common_methods.read_file('aclassgroupsfile');

users_dropdown = '';

share_path = ''
if (sharedetails['id'] == 0):
	sharesinfo = sharedetails['share'];

	sharepath    = sharesinfo['path'];
	share_path    = sharesinfo['path'];
	sharepath = sharepath.replace('/storage/', '');

lis_info = acl.get_acl(share_path)
if(lis_info != {}):
	lis_info = lis_info['acl']
else:
	lis_info = {}
	print lis_info
##############End##########################################################
#############Set User For Permission######################
if(header.form.getvalue('set')):
	set_path = header.form.getvalue('selected_file')
	#set_path_add = '/storage/'+set_path
	get_hid_k_val = header.form.getvalue("hid_k_val")
                        #print globals()["checked_read" + str(i)]
                        #print globals()["checked" + str(j)] = ''
                        #print globals()["checked" + str(i)]
         #       l=l+1
	#	print 'L:'+str(l)
	#print set_path
	#print '<br/>'
	#if(set_path == None):
	#	set_path =sharepath
	avail_user = header.form.getvalue('avail[]')
	#print 'Aval User:'+str(avail_user)
	grant_user = header.form.getvalue('grant_users[]')
	if(isinstance(grant_user, str) == True ):
		grant_user = [grant_user]
	#print 'GRANT:'+str(grant_user)
	#print '<br/>'
	display_rwx = "block"

############End###########################
acl_dict = {}
chk_dict = {}
#################### Set Acl################
if(header.form.getvalue('set_acl')):
	set_path_acl = header.form.getvalue('selected_file')
	set_path_acl_add = '/storage/'+set_path_acl
	#print set_path_acl
	#print '<br/>'
	avail_user_acl = header.form.getvalue('avail')
	get_hid_k_val = header.form.getvalue("hid_k_val")
	grant_user = header.form.getvalue('grant_users[]')
	recr_val = header.form.getvalue('o_recursive') 
	#print recr_val
	if(isinstance(grant_user, str) == True ):
                grant_user = [grant_user]
	#get_read_val = header.form.getvalue('o_read')
	#get_write_val = header.form.getvalue('o_write')
	

	for u in grant_user:
		u = u.replace('[U]', '')
		u = u.replace('[G]', '')
		#print u
		#print header.form.getvalue(u+'o_read')
		#print recr_val
		if((header.form.getvalue(u+'o_read') == "on") and (header.form.getvalue(u+'o_write') == "on") and (header.form.getvalue(u+'o_execute') == "on" )):
			acl_dict.update({u:'rwx'})
			chk_dict.update({u+'_chk_read':'checked',u+'_chk_write':'checked',u+'_chk_execute':'checked'})
			

		if((header.form.getvalue(u+'o_read') == "on") and (header.form.getvalue(u+'o_write') == None) and (header.form.getvalue(u+'o_execute') == None )):	
			acl_dict.update({u:'r--'})
			chk_dict.update({u+'_chk_read':'checked',u+'_chk_write':'',u+'_chk_execute':''})
			

		if((header.form.getvalue(u+'o_read') == "on") and (header.form.getvalue(u+'o_write') == "on") and (header.form.getvalue(u+'o_execute') == None )):
			acl_dict.update({u:'rw-'})
			chk_dict.update({u+'_chk_read':'checked',u+'_chk_write':'checked',u+'_chk_execute':''})
		
		if((header.form.getvalue(u+'o_read') == None) and (header.form.getvalue(u+'o_write') == "on") and (header.form.getvalue(u+'o_execute') == "on" )):
			acl_dict.update({u:'-wx'})
			chk_dict.update({u+'_chk_read':'',u+'_chk_write':'checked',u+'_chk_execute':'checked'})

		if((header.form.getvalue(u+'o_read') == "on") and (header.form.getvalue(u+'o_write') == None) and (header.form.getvalue(u+'o_execute') == "on" )):
			acl_dict.update({u:'r-x'})
			chk_dict.update({u+'_chk_read':'checked',u+'_chk_write':'',u+'_chk_execute':'checked'})
		
		if((header.form.getvalue(u+'o_read') == None) and (header.form.getvalue(u+'o_write') == None) and (header.form.getvalue(u+'o_execute') == "on" )):
			acl_dict.update({u:'--x'})
			chk_dict.update({u+'_chk_read':'',u+'_chk_write':'',u+'_chk_execute':'checked'})

		if((header.form.getvalue(u+'o_read') == None) and (header.form.getvalue(u+'o_write') == None) and (header.form.getvalue(u+'o_execute') == None )):
			acl_dict.update({u:'---'})
			chk_dict.update({u+'_chk_read':'',u+'_chk_write':'',u+'_chk_execute':''})
		
		if((header.form.getvalue(u+'o_read') == None) and (header.form.getvalue(u+'o_write') == "on") and (header.form.getvalue(u+'o_execute') == None )):
			acl_dict.update({u:'-w-'})
			chk_dict.update({u+'_chk_read':'',u+'_chk_write':'checked',u+'_chk_execute':''})

	
	#print chk_dict	
	#print acl_dict	
	#set_acl_code = acl.set_acl(set_path_acl_add,acl_dict,recr_val)
	#print "SET:"+str(set_acl_code)

	display_rwx = "block"
##############End###########################

###################Set Owner #########################
if(header.form.getvalue("set_owner")):
	path_owner= header.form.getvalue("selected_file")
	path_owner_add = '/storage/'+path_owner
	print path_owner_add
	print '<br/>'
	owner_name = header.form.getvalue("acl_owner")
	print owner_name
	
	print '<br/>'
	group_name = header.form.getvalue("acl_group")
	print group_name

	print '<br/>'
	recur_info = header.form.getvalue("acl_chk_info")
	print recur_info
	#print "<script>location.href = 'main.py?page=acl#subtabs-3';</script>"

##################End#################################

######################Reset Acl######################
if(header.form.getvalue("reset_acl")):
	path_reset = header.form.getvalue("selected_file")
	path_reset =  '/storage/'+path_reset
	reset_chk = header.form.getvalue("check_reset")


	#reset_acl_func =acl.reset_acl(path_reset,reset_chk) 
	#print "RESET:"+str(reset_acl_func)
	

#####################End#############################


###########Acl Info##################################

if(header.form.getvalue("acl_user_del")):
	info_path = header.form.getvalue("selected_file")
	info_path = '/storage/'+info_path
	acl_info_result  = acl.get_acl(info_path)
	acl_info_result = acl_info_result['acl']
	print acl_info_result

#############End#####################################
if (len(grant_user) > 0):
	for gu in grant_user:
		groups_from_list.append(gu);

groups_from_list.sort();
groups_from_list = list(set(groups_from_list));

for groups in groups_from_list:
	users_dropdown += '<option value = "' + groups + '" selected>' + groups + '</option>'; 

print """
      <!--Right side body content starts from here-->
      <div class="rightsidecontainer" style="overflow:hidden;">
	<div class="insidepage-heading">NAS >> <span class="content">Acl Configuration</span></div>
	<!--tab srt-->
	<div class="searchresult-container">
	  <div class="infoheader">
	    <div id="tabs">
	      <ul>
		<li><a href="#tabs-1">Acl Configuration</a></li>
	      </ul>
<div id="tabs-1">

	<!--form container starts here-->
	<form name = 'access_control_form'>
	<div id="subtabs">

                  <ul>
                    <li><a href="#subtabs-1">Acl Path</a></li>
                    <li><a href="#subtabs-2">Set Acl</a></li>
                    <li><a href="#subtabs-3">Ownership</a></li>
		    <li><a href="#subtabs-4">Acl Info</a></li>
		    <li><a href="#subtabs-5">Reset Acl</a></li>

                  </ul>
	 <div id="subtabs-1">


	  <table width="100%">

	<tr>
	<td>Folder:</td>
	<td colspan = '4'>
	<iframe style = 'border: 1px solid;' onload = '' src = 'show_dir1.py?share_name=""" + get_share + """&path=""" + sharepath + """&s=s'></iframe>
	</td>
	</tr>
	  <tr>
          <td>Log Path:</td>
		<!--access_control_form.selected_file-->
	  <td colspan = '4'><input type="text" name = "selected_file" readonly value = '""" + sharepath + """' style = 'width:70%;'></td>
	</tr>
	</table>
	<!--<div style="float:right;margin-top:-3%;">
	<button class="button_example" type="button" name = 'submit'  id = 'id_create_but' value = 'Acl'><a href="main.py?page=acl#subtabs-2">Next</a></button></div>-->

          </div>
</form>


<div id="subtabs-2">
<form name= "user_acl" method = "post" action='main.py?page=acl&"""+querystring+"""#subtabs-2'>
 <table style="width:100%; margin:20px 0 0 0; ">
	 <tr>
          <td style ="color:darkred;"><b>Log Path</b>:</td>
                <!--access_control_form.selected_file-->
          <td colspan = '4'>"""
if(set_path !=''):
	print"""<input type="text" name = "selected_file" readonly value = '""" +str(set_path)+ """' style = 'width:70%;'>"""
else:

	print"""<input type="text" name = "selected_file" readonly value = '""" + sharepath + """' style = 'width:70%;'>"""

print"""</td>
        </tr>
	<tr><td height = '25px'></td></tr>
	<tr>
		<td style ="color:darkred;">Choose a domain: <select name = 'domainslist'>"""
if (len(domainsarray) > 0):
	for domains in domainsarray:
		if (domains == domainname):
			print "<option value = '" + domains + "' selected>" + domains + "</option>";

		else:
			print "<option value = '" + domains + "'>" + domains + "</option>";

print """</select></td></tr>
	<tr>
	<td style ="color:darkred;"><B>Available:</B><BR>
	<input id = 'sssavailable' name = 'ads_user_text' type="text" class = 'input' value = '' onclick = 'document.getElementById("available").style.display = "none"; document.getElementById("available_groups").style.display = "none";'>
<input class = 'input1' type = 'button' name = 'getusers' value = 'Check User'  onclick = 'return get_user_suggestions("", document.getElementById("granted").options, "", "", document.user_acl.domainslist.value, this.form.sssavailable.value, "users", document.user_acl.hid_separator.value, \"""" + get_share + """", "acl", \"""" + str(smbuserslength) + """", \"""" + connstatus + """");' """ + alldisabled + """ >		
<input class = 'input1' type = 'button' name = 'getusers' value = 'Check Group'  onclick = 'return get_user_suggestions("", document.getElementById("granted").options, "", "", document.user_acl.domainslist.value, this.form.sssavailable.value, "groups", document.user_acl.hid_separator.value, \"""" + get_share + """", "acl", \"""" + str(smbgroupslength) + """", \"""" + connstatus + """");' """ + alldisabled + """ >"""		
print """<select name ="avail[]" multiple class="user" id ="avail_id" onkeydown = 'return get_key();' style ='width:200px;height:300px; display: """ + avail_users_style + """;'>"""

if (ug == 'users'):
	print get_users_string; 

elif (ug == 'groups'):
	print get_groups_string;

#for all_list in user_group_list:
#	print"""<option value = """+str(all_list)+""">"""+str(all_list)+"""</option>"""
print"""	</select></td>"""

print """<td><input type = 'button' name = 'moveusers' value = '>' onclick = 'return move_users(this.form.avail_id, this.form.granted, "1");'><br />"""

print """<input type = 'button' name = 'moveusers' value = '<' onclick = 'return move_users(this.form.granted, this.form.avail_id, "2");'><br /></td>"""
print """	<td style ="color:darkred;"><B>Authorised:</B><BR>
	<select id = 'granted' name ="grant_users[]" multiple  style ='width:200px;height:300px;margin-right:83%;'>"""
print users_dropdown;
print """	</select></td>"""

#if(grant_user == None):
#	print"""<option name = "avail_group" selected></option>"""
#else:
#	for x in grant_user:
#		print x
#		print"""
#		<option name = "avail_group" selected>"""+str(x)+"""</option>"""
#print"""	</select></td>
print """ 	<td>
        <button class="button_example" type="submit" name = 'set' id = "set_id" value = 'Acl' onclick ='return set_acl_permission();'>Set</button></td>

	</tr>
	</table>
	 <!--<div style="float:right;margin-top:-3%;">
        <button class="button_example" type="submit" name = 'set_cl' value = 'Acl' onclick =''>Set Acl</button></div>-->
<table id = 'id_table' style="width:100%; margin:20px 0 0 0;border:1px;">


        <tr>
                <td style ="color:#EC1F27; display:"""+display_rwx+""";float:left;">User</td>
                <td style ="color:#EC1F27; display:"""+display_rwx+""";margin-left:20%;">Read</td>
                <td style ="color:#EC1F27; display:"""+display_rwx+""";margin-left:35%;margin-top:-2%;">Write</td>
                <td style ="color:#EC1F27; display:"""+display_rwx+""";margin-left:51%;margin-top:-2%;">Execute</td>
        </tr>"""
if(grant_user == None):
	print"""<th align="left" style="color:darkgreen;""></th>"""
else:
	k = 1
	for users_list in grant_user:
		users_list = users_list.replace('[', '')
		users_list = users_list.replace(']', '')
		users_list = users_list.replace('U', '')
		users_list = users_list.replace('G', '')

	
		
		print"""<tr>
				<td align="left" style="color:darkgreen;""><div style="margin-top: 2%;">"""+users_list+"""</div></td >
				
		</tr>
		<tr style="border:solid 1px;">"""
		
		'''
		rcheckbox_name = users_list + '_o_read';
		#print rcheckbox_name
		wcheckbox_name = users_list + '_o_write';
		xcheckbox_name = users_list + '_o_execute';
		
		#if(read_per == 'on'):
		#	read_check = 'checked'
		read_check_val = users_list+":yes"
		'''
		#print"""<td style="float:right;width:79%;margin-top:-2%;"><input type="checkbox" name='o_read""" + str(k) + """' """ + globals()["checked_read" + str(k)] + """ value='"""+read_check_val+"""'></td>"""
		print"""<td style="float:right;width:79%;margin-top:-2%;"><input type="checkbox" name='"""+users_list+"""o_read'"""
		if(chk_dict != {}):
			print chk_dict[users_list+'_chk_read']

		if(lis_info != {}):
			if 'r' in lis_info[users_list]:
				print "checked"

		print """></td>"""

		#if(write_per == 'on'):
		#	write_check = 'checked'
		print"""<td style="float:right;width:64%;margin-top:-2%;"><input type="checkbox" name='"""+users_list+"""o_write'"""
		if(chk_dict != {}):
                        print chk_dict[users_list+'_chk_write']

		if(lis_info != {}):
			if 'w' in lis_info[users_list]:
				print "checked"


		print """></td>"""
		#if(execute_per == 'on'):
		#	execute_check = 'checked'
		print"""<td style="float:right;width:47%;margin-top:-2%;"><input type="checkbox" name='"""+users_list+"""o_execute'"""
		if(chk_dict != {}):
                        print chk_dict[users_list+'_chk_execute']

		if(lis_info != {}):
			if 'x' in lis_info[users_list]:
				print "checked"


		print """></td>"""
		#if(recr_val == "yes"):
		#	recr_chk = "checked"
		
		#print"""<td style="float:left;margin-top:-2%;margin-left:78%;"><input type="checkbox" name='recr""" + str(k) + """' """+globals()["checked_recr" + str(k)]+"""></td>"""
		#print"""<td><select name = "recr" style="float: left; width: 40%; margin-left: -146%;">
		#	<option>yes</option>
		#	<option>No</option>
		#</select></td>"""
		print """</tr> """
		k = k+1
		#print 'K:'+str(k)

	print"""<td><input type="hidden" name="hid_k_val" value='"""+str(k)+"""'></td>"""

print"""
<tr>"""
if(recr_val == "on"):
	recr_chk = "checked"
	recr_val = "yes"
else:
	recr_chk = ""
	recr_val = "no"

print"""<td style ="color:#EC1F27;"><b>Recursive</b>:<input type="checkbox" name='o_recursive' """+recr_chk+""" /></td>"""


print"""</tr>"""
print"""
        </table>
	<div style="float:right;margin-top:-3%;display:"""+display_rwx+""";">
        <button class="button_example" type="submit" id = 'id_butt' name = 'set_acl' value = 'acl'>Set Acl</button></div>
	<input type = 'hidden' name = 'hid_separator' value = '""" + ads_separator + """'>
</form>
</div>

<div id="subtabs-3">
	<form name="set_owner_form" method="post">
	<table width="100%">
	<tr>
          <td>Log Path:</td>
                <!--access_control_form.selected_file-->"""

if(path_owner != ''):

	print"""<td colspan = '4'><input type="text" name = "selected_file" readonly value = '""" + path_owner + """' style = 'width:70%;'></td>"""
else:
	
	print"""<td colspan = '4'><input type="text" name = "selected_file" readonly value = '""" + sharepath + """' style = 'width:70%;'></td>"""
print"""
        </tr>
	<tr>
		<td style="width: 14%;">Select Owner:</td>
		<td>
		<select name="acl_owner" style ='width:200px;margin-right:83%;'>
		<option>root</option>"""
for owner_list in get_all_users['users']:
	print"""
		<option value = '"""+owner_list+"""'"""
	if(owner_name !=''):
		if(owner_name == owner_list):
			print """selected = 'selected'"""
        print """>"""+owner_list+"""</option>"""
print"""		</select></td>
	</tr>
		
	<tr>
		<td style="width: 14%;">Select Group:</td>
		<td>
		<select name="acl_group" style ='width:200px;margin-right:83%;'>
		<option>root</option>"""
for group_list_info in get_all_groups['groups']:
	print"""
		<option value = '"""+group_list_info+"""'"""
	if(group_name !=''):
		if(group_name == group_list_info):
			print """selected = 'selected'"""
        print """>"""+group_list_info+"""</option>"""
print"""		</select></td>
	</tr>
	<tr>
	<td>Recursive:</td>"""

if(recur_info == 'on'):
	recr_chk_info = "checked"
	recur_info = "Yes"
else:
	recr_chk_info = ""
        recur_info = "NO"
print"""	<td> <input type = "checkbox" name = "acl_chk_info" """+recr_chk_info+"""></td>"""
print"""
	</tr> 
        </table>
	<div style="float:right;margin-top:-3%;">
        <button class="button_example" type="submit" id = 'id_owner' name = 'set_owner' value = 'owner'>Set Owner</button></div>
	</form>
</div>
<div id="subtabs-4">
<form name="acl_info" method="post">
<table id = 'id_table' style="width:100%; margin:20px 0 0 0;border:1px;">
	 <tr>
	</tr>
	<td>Log Path:
	<input type="text" name = "selected_file" readonly value = '""" + sharepath + """' style = 'width:50%;margin-bottom:5%;'>
          
	</td>

        <tr>
                <td style ="color:#EC1F27; display:"""+display_rwx+""";float:left;">User</td>
                <td style ="color:#EC1F27; display:"""+display_rwx+""";margin-left:20%;">Read</td>
                <td style ="color:#EC1F27; display:"""+display_rwx+""";margin-left:35%;margin-top:-2%;">Write</td>
                <td style ="color:#EC1F27; display:"""+display_rwx+""";margin-left:51%;margin-top:-2%;">Execute</td>
        </tr>"""
if(grant_user == None):
	print"""<th align="left" style="color:darkgreen;""></th>"""
else:
	k = 1
	for users_list in grant_user:
		users_list = users_list.replace('[', '')
		users_list = users_list.replace(']', '')
		users_list = users_list.replace('U', '')
		users_list = users_list.replace('G', '')

	
		
		print"""<tr>
				<td align="left" style="color:darkgreen;""><div style="margin-top: 2%;">"""+users_list+"""</div></td >
				
		</tr>
		<tr style="border:solid 1px;">"""
		
		'''
		rcheckbox_name = users_list + '_o_read';
		#print rcheckbox_name
		wcheckbox_name = users_list + '_o_write';
		xcheckbox_name = users_list + '_o_execute';
		
		#if(read_per == 'on'):
		#	read_check = 'checked'
		read_check_val = users_list+":yes"
		'''
		#print"""<td style="float:right;width:79%;margin-top:-2%;"><input type="checkbox" name='o_read""" + str(k) + """' """ + globals()["checked_read" + str(k)] + """ value='"""+read_check_val+"""'></td>"""
		print"""<td style="float:right;width:79%;margin-top:-2%;"><input type="checkbox" name='"""+users_list+"""o_read'"""
		if(chk_dict != {}):
			print chk_dict[users_list+'_chk_read']

		if(lis_info != {}):
			if 'r' in lis_info[users_list]:
				print "checked"

		print """></td>"""

		#if(write_per == 'on'):
		#	write_check = 'checked'
		print"""<td style="float:right;width:64%;margin-top:-2%;"><input type="checkbox" name='"""+users_list+"""o_write'"""
		if(chk_dict != {}):
                        print chk_dict[users_list+'_chk_write']

		if(lis_info != {}):
			if 'w' in lis_info[users_list]:
				print "checked"


		print """></td>"""
		#if(execute_per == 'on'):
		#	execute_check = 'checked'
		print"""<td style="float:right;width:47%;margin-top:-2%;"><input type="checkbox" name='"""+users_list+"""o_execute'"""
		if(chk_dict != {}):
                        print chk_dict[users_list+'_chk_execute']

		if(lis_info != {}):
			if 'x' in lis_info[users_list]:
				print "checked"


		print """></td>"""
		#if(recr_val == "yes"):
		#	recr_chk = "checked"
		
		#print"""<td style="float:left;margin-top:-2%;margin-left:78%;"><input type="checkbox" name='recr""" + str(k) + """' """+globals()["checked_recr" + str(k)]+"""></td>"""
		#print"""<td><select name = "recr" style="float: left; width: 40%; margin-left: -146%;">
		#	<option>yes</option>
		#	<option>No</option>
		#</select></td>"""
		print """</tr> """
		k = k+1
		#print 'K:'+str(k)

	print"""<td><input type="hidden" name="hid_k_val" value='"""+str(k)+"""'></td>"""

print"""
<tr>"""
if(recr_val == "on"):
	recr_chk = "checked"
	recr_val = "yes"
else:
	recr_chk = ""
	recr_val = "no"

print"""<td style ="color:#EC1F27;"><b>Recursive</b>:<input type="checkbox" name='o_recursive' """+recr_chk+""" /></td>"""


print"""</tr>"""
print"""
        </table>

<div style="float:right;margin-top:-3%;">
        <button class="button_example" type="submit" name = 'acl_user_del' value = 'info'>Reset User</button></div>
</form>
</div>
<div id="subtabs-5">
<form name= "reset_acl_form" method= "post">
	<table width="98%">
	 <tr>
          <td>Log Path:</td>
                <!--access_control_form.selected_file-->
          <td colspan = '4'><input type="text" name = "selected_file" readonly value = '""" + sharepath + """' style = 'width:70%;'></td>
        </tr>
	<tr>
	<td>Recursive:</td>"""
if(reset_chk == 'on'):
	reset_chk_but = 'checked'
	reset_chk = "yes"
else:
	reset_chk_but = ""
	reset_chk = "no"
	
print"""	<td><input type="checkbox" name= "check_reset" """+reset_chk_but+"""></td>"""
print"""	</tr>
</table>
	<div style="float:right;margin-top:-3%;">
        <button class="button_example" type="submit" name = 'reset_acl' value = 'Reset' onclick =''>Reset</button></div>

</form>

</div>

</div>
<!--form container ends here-->
<input type = 'hidden' name = 'hid_dir_file' />
</form>
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
<!-- ####### Sub Tabs Start ####### -->

<script>
$("#tabs, #subtabs").tabs();
$("#tabs, #subsubtabs").tabs();
</script>



<!-- ####### Sub Tabs End ####### -->
"""
