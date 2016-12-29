#!/usr/bin/python
import cgitb, cgi, common_methods, sys, os, include_files

# import the python modules
sys.path.append('/var/nasexe/python/');
from fs2global import *;
from tools import *;

cgitb.enable();

# get the querystring from the url posted
querystring = os.environ["QUERY_STRING"];

# get the form field data
form = cgi.FieldStorage();

# initialize the necessary variables
usrstring = '';
grpstring = '';
domain    = '';
ads_separator = '';
ads_separator = get_ads_separator();

# get the connection/authentication status
connstatus = common_methods.conn_status();

# declare 2 arrays for users displayed in assigned users dropdown and assigned groups dropdown
ass_users_array  = [];
ass_groups_array = [];

# retrieve the variable values from the querystring
if (querystring.find('&ugs') > 0):
	usrstring = querystring[querystring.find('&ugs=') + len('&ugs='):querystring.find('&ggs=')];

#
if (querystring.find('&ggs=') > 0):
	grpstring = querystring[querystring.find('&ggs=') + len('&ggs='):querystring.find('&fn=')];

#
if (querystring.find('&fn=') > 0):
	formname = querystring[querystring.find('&fn=') + len('&fn='):querystring.find('&dom=')];

#
if (querystring.find('&dom=') > 0):
	domain = querystring[querystring.find('&dom=') + len('&dom='):];
	domain = domain.strip();

#
if (usrstring != ''):
	usrstring       = usrstring[:usrstring.rfind(':::')];
	ass_users_array = usrstring.split(':::');

#
if (grpstring != ''):
	grpstring        = grpstring[:grpstring.rfind(':::')];
	ass_groups_array = grpstring.split(':::');

#
if (formname == 'acl'):
	usrfiletowrite = open('aclassusersfile', 'w');
	grpfiletowrite = open('aclassgroupsfile', 'w');

#
elif (formname == 'smb'):
	usrfiletowrite = open('smbassusersfile', 'w');
	grpfiletowrite = open('smbassgroupsfile', 'w');

#
elif (formname == 'ftp'):
	usrfiletowrite = open('ftpassusersfile', 'w');
	grpfiletowrite = open('ftpassgroupsfile', 'w');

#
elif (formname == 'quota'):
	usrfiletowrite = open('quotaassusersfile', 'w');
	grpfiletowrite = open('quotaassgroupsfile', 'w');

#
elif (formname == 'afp'):
	usrfiletowrite = open('afpassusersfile', 'w');
	grpfiletowrite = open('afpassgroupsfile', 'w');

#
elif (formname == 'ownership'):
	usrfiletowrite = open('ownsassusersfile', 'w');
	grpfiletowrite = open('ownsassgroupsfile', 'w');

#
if (len(ass_users_array) > 0):
	for au in ass_users_array:
		au = common_methods.replace_chars(au, 'texttochar');

		usrfiletowrite.write(au);
		usrfiletowrite.write('\n');

	usrfiletowrite.close();

#		
if (len(ass_groups_array) > 0):
	for ag in ass_groups_array:
		ag = common_methods.replace_chars(ag, 'texttochar');

		grpfiletowrite.write(ag);
		grpfiletowrite.write('\n');

	grpfiletowrite.close();

#
if (querystring.find('fs=') >= 0):
	full_userstring = querystring[querystring.find('fs=') + len('fs='):querystring.find('&ug=')];

	full_userstring = common_methods.replace_chars(full_userstring, 'texttochar');

#
if (querystring.find('ug=') > 0):
	usergroup = querystring[querystring.find('ug=') + len('ug='):querystring.find('&s=')];

#
if (querystring.find('s=') > 0):
	sharename = querystring[querystring.find('&s=') + len('&s='):querystring.find('&ro=')];

#
if (querystring.rfind('&ro=') > 0):
	readonly = querystring[querystring.find('&ro=') + len('&ro='):querystring.find('&v=')];

#
if (querystring.rfind('&v=') > 0):
	visible = querystring[querystring.find('&v=') + len('&v='):querystring.find('&ugs=')];

#
if (ads_separator == '\\'):
	ads_separator = '\\\\';

#
full_userstring = full_userstring.strip();

#
if (usergroup == 'users'):
	full_userstring = common_methods.replace_chars(full_userstring, 'texttochar');

	users_file = user_files_dir + domain + '-users.txt';

	if (connstatus == 'Join is OK'):
		if (domain == 'local'):
			searchuserstring = '^' + full_userstring;
	
		else:
			#searchuserstring = '^' + domain + ads_separator + full_userstring;
			searchuserstring = '^' + full_userstring;

		get_user = get_string_from_file(searchuserstring, users_file);

	else:
		get_user = get_string_from_file('^' + full_userstring, users_file);

	if (get_user == 'not found'):
		common_methods.sendtologs('ERROR', 'Search Users', 'UI', '"get_users_string.py, tools.get_string_from_file()", USER NOT FOUND ');


	if (formname == 'acl'):
		userfiletowrite = open('aclsearchusersfile.txt', 'w');

	elif (formname == 'smb'):
		userfiletowrite = open('smbsearchusersfile.txt', 'w');

	elif (formname == 'ftp'):
		userfiletowrite = open('ftpsearchusersfile.txt', 'w');

	elif (formname == 'quota'):
		userfiletowrite = open('quotasearchusersfile.txt', 'w');

	elif (formname == 'quotadet'):
		userfiletowrite = open('s_quotasearchusersfile.txt', 'w');

	elif (formname == 'afp'):
		userfiletowrite = open('afpsearchusersfile.txt', 'w');

	elif (formname == 'ownership'):
		userfiletowrite = open('ownssearchusersfile.txt', 'w');

	if (get_user != 'not found'):
		userfiletowrite.write(get_user);
		userfiletowrite.write("\n");

#
if (usergroup == 'groups'):
	full_userstring = common_methods.replace_chars(full_userstring, 'texttochar');

	groups_file = user_files_dir + domain + '-groups.txt';

	if (connstatus == 'Join is OK'):
		if (domain == 'local'):
			searchgroupstring = '^' + full_userstring;

		else:
			#searchgroupstring = '^' + domain + ads_separator + full_userstring;
			searchgroupstring = '^' + full_userstring;

		get_group = get_string_from_file(searchgroupstring, groups_file);

	else:
		get_group = get_string_from_file('^' + full_userstring, groups_file);

	if (get_group == 'not found'):
		common_methods.sendtologs('ERROR', 'Search Groups', 'UI', '"get_users_string.py, tools.get_string_from_file()", GROUP NOT FOUND ');


	if (formname == 'acl'):
		groupfiletowrite = open('aclsearchgroupsfile.txt', 'w');

	elif (formname == 'smb'):
		groupfiletowrite = open('smbsearchgroupsfile.txt', 'w');

	elif (formname == 'ftp'):
		groupfiletowrite = open('ftpsearchgroupsfile.txt', 'w');

	elif (formname == 'quota'):
		groupfiletowrite = open('quotasearchgroupsfile.txt', 'w');

	elif (formname == 'quotadet'):
		groupfiletowrite = open('s_quotasearchgroupsfile.txt', 'w');

	elif (formname == 'afp'):
		groupfiletowrite = open('afpsearchgroupsfile.txt', 'w');

	elif (formname == 'ownership'):
		groupfiletowrite = open('ownssearchgroupsfile.txt', 'w');

	if (get_group != 'not found'):
		groupfiletowrite.write(get_group);
		groupfiletowrite.write("\n");

#
if (formname == 'smb'):
	#print "<script>location.href = 'smb_settings.py?ug=%s&share_name=%s&ro=%s&v=%s&dom=%s';</script>" % (usergroup, sharename, readonly, visible, domain);
	print "<script>location.href = 'iframe_smb_settings.py?ug=%s&share_name=%s&ro=%s&v=%s&dom=%s';</script>" % (usergroup, sharename, readonly, visible, domain);

elif (formname == 'ftp'):
	#print "<script>location.href = 'ftp_settings.py?ug=%s&share_name=%s&ro=%s&v=%s&dom=%s';</script>" % (usergroup, sharename, readonly, visible, domain);
	print "<script>location.href = 'iframe_ftp_settings.py?ug=%s&share_name=%s&ro=%s&v=%s&dom=%s';</script>" % (usergroup, sharename, readonly, visible, domain);

elif (formname == 'quota'):
	print "<script>location.href = 'iframe_user_quota.py?spain=yes&ug=%s&dom=%s';</script>" % (usergroup, domain);

elif (formname == 'quotadet'):
	print "<script>location.href = 'iframe_user_quota.py?fn=%s&page=no&ug=%s&dom=%s#tabs-2';</script>" % (formname, usergroup, domain);

elif (formname == 'afp'):
	#print "<script>location.href = 'afp_settings.py?ug=%s&share_name=%s&ro=%s&v=%s&dom=%s';</script>" % (usergroup, sharename, readonly, visible, domain);
	print "<script>location.href = 'iframe_afp_settings.py?ug=%s&share_name=%s&ro=%s&v=%s&dom=%s';</script>" % (usergroup, sharename, readonly, visible, domain);

elif (formname == 'acl'):
	print "<script>location.href = 'iframe_set_acl_page.py?formname=%s&ug=%s&share_name=%s&dom=%s#subtabs-2';</script>" % (formname, usergroup, sharename, domain);
	#print "<script>location.href = 'main.py?page=acl&formname=%s&ug=%s&share_name=%s&dom=%s#subtabs-2';</script>" % (formname, usergroup, sharename, domain);

elif (formname == 'ownership'):
	print "<script>location.href = 'iframe_set_acl_page.py?formname=%s&ug=%s&share_name=%s&dom=%s#subtabs-4';</script>" % (formname, usergroup, sharename, domain);
	#print "<script>location.href = 'main.py?page=acl&formname=%s&ug=%s&share_name=%s&dom=%s#subtabs-4';</script>" % (formname, usergroup, sharename, domain);
