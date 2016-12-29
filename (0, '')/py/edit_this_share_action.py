#!/usr/bin/python
import cgi, common_methods, commands, cgitb, sys

sys.path.append('/var/nasexe/python/');
import smb;

cgitb.enable();
print 'Content-type: text/html';
print

form = cgi.FieldStorage();
	
session_user = common_methods.get_session_user();

if (session_user != ''):
	share   = form.getvalue('share_name');
	comment = form.getvalue('comment');
	path    = form.getvalue('share_path');

	path = '/storage/' + path;

	if (comment == None):
		comment = '';

	shareline = share + ':' + path + ':' + comment;
	shareline = shareline.replace('/', '\\/');

	checksmbshare = commands.getstatusoutput('ls "/var/nasconf/smbconf/%s"' % share);

	if (checksmbshare[0] == 0):
		shareinput = smb.show(share);

		sharedetails = shareinput['share'];

		sharedetails['comment'] = comment;

		status = smb.configure(sharedetails);

		if (status['id'] == 0):
			print '<script>alert("%s");</script>' % str(status['desc']);

	else:
		status = commands.getstatusoutput('sudo sed -i "s/^%s:.*/%s/g" /var/www/global_files/shares_global_file' % (share, shareline));

		if (status[0] == 0):
			print """<script>alert('Modified comment for "%s"!');</script>""" % share;

	print "<script>location.href = 'show_shares.py?s1=%s';</script>" % share;

else:
	common_methods.relogin();

