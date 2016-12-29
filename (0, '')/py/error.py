#!/usr/bin/python
import cgitb, common_methods, commands, traceback, os 

cgitb.enable();

#form = cgi.FieldStorage()
print """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>
	<head>
		<title>Error Page</title>
		<script language = 'javascript' src = '../js/commons.js'>
		</script>
		<link rel = 'stylesheet' href = '../css/style.css' />
		<link rel = 'stylesheet' href = '../css/chart_graph.css' />
		<link rel = 'stylesheet' href = '../css/drop-down/*.css' />
		<link rel = 'stylesheet' href = '../css/jquery.alerts.css' />
		<link rel = 'stylesheet' href = '../css/jquery-ui.css' />
		<link rel = 'stylesheet' href = '../css/main.css' />
		<link rel = 'stylesheet' href = '../css/style.css' />
	</head>
	<body>"""

session_user = 'Full Access';
querystring = os.environ['QUERY_STRING'];
frompage = '';

if (querystring.find('from=') >= 0):
	frompage = querystring[querystring.find('from=') + len('from='):];

if (session_user != ''):
	try:
		filetoread = 'temp';

		commands.getoutput('sudo sed -i "/^$/d" %s' % filetoread);

		array = [];

                with open(filetoread, 'r') as f:
	                for line in f:
        		        if (line != ""):
			                array.append(line);

		if (len(array) > 0):
			print """<div style = 'margin-right: 30%; margin-left: 10%; margin-top: 5%; border: 1px solid #BDBDBD; height: 50%; width: 60%; text-align: justify;'>"""
			print array[0] + '...' + '<input id = \'id_showmore\' type = \'button\' value = \'+\' onclick = \'return showhide()\'>';

		print """<div id = 'err_div' align = 'center' style = 'border: 0px solid; width: 75%; text-align: left; display: none;'><BR>"""

		warray = [];
		resstring = '';

		for i in array:
			if (i != ''):
				i = i.replace('\'', '--');
				i = i.replace('"', '--');
				i = i.replace(';', ':');
				i = i.replace('<', '[');
				i = i.replace('>', ']');
				i = i.replace(' ', '...');
				i = i.replace('Traceback', ', Traceback');
				i = i.strip();
				warray.append('[ERROR]' + i + '[/ERROR] ');
				resstring += '[ERROR]' + i + '[/ERROR]';

		print resstring;

		errarray = [];
		resstring = '[BUG]' + resstring + '[/BUG]';
		errarray.append(resstring);

		common_methods.write_file('temp1', errarray);

		fh1 = open('temp1', 'rb');
		fh2 = open('temp1', 'rb');
		print """<form name = 'error_form' method = 'post' action = 'do_write_logs.py'><input id = 'id_hid_error' type = 'hidden' name = 'hid_error' value = '%s'></form>""" % fh1.read();
		print """<center><div align = 'center' id = 'response' style = 'color: darkred; font-style: italic; margin-right: auto; margin-left: auto;'><div align = 'center' id = 'wait' style = 'display: none;'><img src = '../images/arrows32.gif'> Processing...</div></div><BR><input type = "button" value = "Back" onclick = "parent.location.href = 'login.py'">""";
		print """<input type = "button" value = "Send Bug Report" onclick = "location.href = 'mailto:sunny@netwebindia.com?subject=BugReport&body=%s'">""" % fh1.read().strip();
		print """<input type = "button" value = "Add To Logs" onclick = 'return update_to_file("%s");'>""" % fh2.read().strip();
		print "</div></div></form><BR><BR>";

	except Exception as e:
	        fh = open('temp', 'w');
        	fh.write(str(e));
	        traceback.print_exc(file = fh);
        	print "<script>location.href = 'error.py';</script>";


else:
	common_methods.relogin();

print """	</body>
</html>"""
