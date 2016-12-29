#!/usr/bin/python
import cgitb, cgi, common_methods, commands, os

cgitb.enable();
form = cgi.FieldStorage();

lfile = form.getvalue('file');
print
print """
	<link rel = 'stylesheet' href = '../css/style.css' />"""

print """<center><div><button class = 'button_example' type="button" name = 'close' value = 'Close Window' onclick = 'window.close();'>Close Window</button>

</div></center><BR>"""

print """<textarea readonly style = 'border: 1px solid; width: 100%; height: 100%;'>"""

for line in reversed(open(lfile).readlines()):
	print line.rstrip();

print """</textarea>""";
