#!/usr/bin/python
import cgi, cgitb, commands, common_methods, datetime, sys
sys.path.append('/var/nasexe/python/');
import tools

cgitb.enable();

print 'Content-type: text/html';
print

form = cgi.FieldStorage();

string = form.getvalue('hid_error');

params_array = [];
params_array.append(string);

datenow = str(datetime.datetime.now());
datenow = datenow[:datenow.find(' ')];
filetowrite = '../downloads/BUG-REPORT_%s' % str(datenow);

commands.getoutput('sudo chmod 777 %s' % filetowrite);

fh = open(filetowrite, 'a');

fh.write(string);
fh.write("\n");
fh.write("---------------------------------------------------\n\n");
fh.close();

print "<script>alert('Added to logs!');</script>";
print "<script>location.href = 'error.py?from=bg';</script>";
