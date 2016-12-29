#!/usr/bin/python
import cgitb, cgi, common_methods, sys, os,header

sys.path.append('/var/nasexe/python/');
from fs2global import *;
from tools import *;

cgitb.enable();

querystring = os.environ["QUERY_STRING"];

form = cgi.FieldStorage();

usrstring = '';
grpstring = '';

ass_users_array  = [];
ass_groups_array = [];

ads_separator = '';
ads_separator = get_ads_separator();

if (querystring.find('&ugs') > 0):
	usrstring = querystring[querystring.find('&ugs=') + len('&ugs='):querystring.find('&ggs=')];

if (querystring.find('&ggs=') > 0):
	grpstring = querystring[querystring.find('&ggs=') + len('&ggs='):];

if (usrstring != ''):
	usrstring       = usrstring[:usrstring.rfind(':::')];
	ass_users_array = usrstring.split(':::');

if (grpstring != ''):
	grpstring        = grpstring[:grpstring.rfind(':::')];
	ass_groups_array = grpstring.split(':::');

usrfiletowrite = open('assusersfile', 'w');
grpfiletowrite = open('assgroupsfile', 'w');

if (len(ass_users_array) > 0):
	for au in ass_users_array:
		usrfiletowrite.write(au);
		usrfiletowrite.write('\n');

	usrfiletowrite.close();
		
if (len(ass_groups_array) > 0):
	for ag in ass_groups_array:
		grpfiletowrite.write(ag);
		grpfiletowrite.write('\n');

	grpfiletowrite.close();

if (querystring.find('fs=') >= 0):
	full_userstring = querystring[querystring.find('fs=') + len('fs='):querystring.find('&ug=')];

	full_userstring = common_methods.replace_chars(full_userstring, 'texttochar');

if (querystring.find('ug=') > 0):
	usergroup = querystring[querystring.find('ug=') + len('ug='):querystring.find('&s=')];

if (querystring.find('s=') > 0):
	sharename = querystring[querystring.find('&s=') + len('&s='):querystring.find('&ro=')];

if (querystring.rfind('&ro=') > 0):
	readonly = querystring[querystring.find('&ro=') + len('&ro='):querystring.find('&v=')];

if (querystring.rfind('&v=') > 0):
	visible = querystring[querystring.find('&v=') + len('&v='):querystring.find('&ugs=')];

domain  = full_userstring[:full_userstring.find(ads_separator)];
adsuser = full_userstring[full_userstring.find(ads_separator) + 1:];

domain  = domain.strip();
adsuser = adsuser.strip();

if (usergroup == 'users'):
	checkusersfile = check_file_exits('adsusersfile');

	if (checkusersfile == 'exists'):
		#get_user = commands.getstatusoutput('sudo grep "^%s" adsusersfile' % full_userstring);
		#get_user = get_string_from_file(full_userstring, 'adsusersfile');

		users_file = user_files_dir + domain + '-users.txt'
                get_user = get_string_from_file(full_userstring, users_file)
		
		userfiletowrite = open('searchusersfile.txt', 'w');

		if (get_user != 'not found'):
			userfiletowrite.write(get_user);
			userfiletowrite.write("\n");

if (usergroup == 'groups'):
	checkgroupsfile = check_file_exits('adsgroupsfile');

	if (checkgroupsfile == 'exists'):
		#get_group = commands.getstatusoutput('sudo grep "^%s" adsgroupsfile' % full_userstring);
		#get_group = get_string_from_file(full_userstring, 'adsgroupsfile');

		groups_file = user_files_dir + domain + '-groups.txt';
                get_group = get_string_from_file(full_userstring, groups_file);

		groupfiletowrite = open('searchgroupsfile.txt', 'w');

		if (get_group != 'not found'):
			groupfiletowrite.write(get_group);
			groupfiletowrite.write("\n");

print "<script>location.href = 'afp_settings.py?ug=%s&share_name=%s&ro=%s&v=%s&dom=%s';</script>" % (usergroup, sharename, readonly, visible, domain);
