#!/usr/bin/python
import cgitb, cgi, commands;
cgitb.enable();

form = cgi.FieldStorage();
line = '';

print 'Content-type: text/html'
print

username  = form.getvalue('u');
usergroup = form.getvalue('ug');
groupname = '';

usersarray  = [];

username = username.replace('[PLUS]', '+');

if (usergroup == 'user'):
	searchforuser = commands.getstatusoutput('sudo grep "^%s" /tmp/adsusers' % username);

	if (searchforuser[0] == 0):
		line       = searchforuser[1];
		usersarray = line.split('\n');

	else:
		print 'Could not get users!';

if (usergroup == 'group'):
	searchforgroup = commands.getstatusoutput('sudo grep "^%s" /tmp/adsgroups' % username);

	if (searchforgroup[0] == 0):
		line        = searchforgroup[1];
		usersarray = line.split('\n');

	else:
		print 'Could not get groups';

if (len(usersarray) > 0):
	for line in usersarray:
		if (usergroup == 'user'):
			print """<a href = "#" onclick = 'window.document.getElementById("id_smbusers_list").html = true; window.document.getElementById("id_smbusers_list").htmlText = "line"; document.getElementById("id_smbusers_list").style.display = "none";'>""" + line + """</a><BR>""";

		if (usergroup == 'group'):
			groupname = username;

			print """<a href = "#" onclick = 'window.document.getElementById("id_smbgroups_list").innerHTML = "line"; document.getElementById("id_smbgroups_list").style.display = "none";'>""" + line + """</a><BR>""";


