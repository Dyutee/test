#!/usr/bin/python
import cgitb, cgi, common_methods, commands, sys, os;
cgitb.enable();

# append the python modules path to the exceutable path and import required modules
sys.path.append('/var/nasexe/python/');
import logs, db_logs, tools;

#from 

sys.path.append('/var/www/fs4/modules/');
import disp_except;

form = cgi.FieldStorage();

log_array = [];
log_file  = common_methods.log_file;

action = '';

querystring = os.environ['QUERY_STRING'];

db_logs.get_rows_from_table('logs');

try:
	session_user = common_methods.get_session_user();

	if (session_user != ''):
		#action  = form.getvalue('action_but1');

		if (querystring.find('action_but1=') > 0):
			action = querystring[querystring.find('action_but1=') + len('action_but1='):];
			action = action.replace('%20', ' ');

		if (action == 'Get Web Logs'):
			filetowrite = '/var/www/fs4/downloads/fs2weblogs.txt';
			logfiletowrite = open(filetowrite, 'w');
			logstring = '';
			status = db_logs.get_rows_from_table('logs');

			if (status != 'ERROR'):
				for info_dict in status:
					errdate  = info_dict['tstamp'];
					errtype  = info_dict['type'];
					message  = info_dict['msg'];
					logsrc   = info_dict['log_src'];
					moreinfo = info_dict['more_info'];

					logstring = str(errdate) + '<<>>' + str(errtype) + '<<>>' + str(message) + '<<>>' + str(logsrc) + '<<>>' + str(moreinfo);
					logfiletowrite.write(logstring + '\n');

				compress_status = tools.compress(filetowrite);

			log_string = str(common_methods.now) + '<<>>From: ' + common_methods.remote_ip + '<<>>' + action + '<<>>' + str(status);

			log_array.append(log_string);
			common_methods.append_file(log_file, log_array);

			if (status == 'success'):
				print "<script>alert('Retrieved web logs!');</script>";

			else:
				print "<script>alert('%s');</script>" % str(status);

			#print "<script>location.href = 'download.py?f=wl';</script>";
			print "<script>location.href = 'main.py?page=logs';</script>";

		# if the user clicks on 'Get System Info' button
		if (action == 'Get System Info'):
			status = logs.sys_status();

			log_string = str(common_methods.now) + '<<>>From: ' + common_methods.remote_ip + '<<>>' + action + '<<>>' + str(status);

			log_array.append(log_string);
			common_methods.append_file(log_file, log_array);

			if (status['id'] == 0):
				print "<script>alert('Retrieved system info successfully!');</script>";

			else:
				print '<script>alert("%s");</script>' % str(status['desc']);

			print "<script>location.href = 'main.py?page=logs&frompage=sysinfo';</script>";

		if (action == 'Clear Logs'):
			commands.getoutput('sudo chmod -R 755 /var/log');

			status = logs.clear_logs();

			log_string = str(common_methods.now) + '<<>>From: ' + common_methods.remote_ip + '<<>>' + action + '<<>>' + str(status);

			log_array.append(log_string);
			common_methods.append_file(log_file, log_array);

			if (status['id'] == 0):
				print "<script>alert('Logs Cleared!');</script>";

			else:
				print '<script>alert("%s");</script>' % str(status['desc']);

			print "<script>location.href = 'main.py?page=logs';</script>";

		if (action == 'Get Entire Logs'):
			frompage = '';
			status = logs.get_logs();

			log_string = str(common_methods.now) + '<<>>From: ' + common_methods.remote_ip + '<<>>' + action + '<<>>' + str(status);

			log_array.append(log_string);
			common_methods.append_file(log_file, log_array);

			if (status['id'] == 0):
				print "<script>alert('Retrieved the log file!');</script>";

			else:
				print '<script>alert("%s");</script>' % status['desc'];

			print "<script>location.href = 'main.py?page=logs';</script>";

	else:
		common_methods.relogin();

except Exception as e:
	disp_except.display_exception(e);
