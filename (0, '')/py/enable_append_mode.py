#!/usr/bin/python
import commands, common_methods, cgitb, cgi, os
cgitb.enable();

log_array = [];
log_file = common_methods.log_file;

# get the session user from the common_methods.py
session_user = common_methods.get_session_user();

# get the url from javascript
querystring = os.environ['QUERY_STRING'];

if (session_user != ''):
	# retrieve the mode and path from the querystring
	mode = common_methods.substr(querystring, 'mode=', '&', '');
	path = common_methods.substr(querystring, 'path=', '', '');

	# if 'enable append mode' option is checked
	if (mode == 'true'):
		# bash command to set attribute for a path
		enable_apm_command = 'sudo chattr -R +a "/storage/' + path + '"';
		status = commands.getstatusoutput(enable_apm_command);

		if (status[0] == 0):
			print "<script>alert('Append mode enabled for [%s]');</script>" % path;

			# generate a string for log file
		        log_string = str(common_methods.now) + '||From: ' + common_methods.remote_ip + '<<>>Append mode enabled for [' + path + ']<<>>' + str(status);
		        log_array.append(log_string);

		else:
		        log_string = str(common_methods.now) + '||From: ' + common_methods.remote_ip + '<<>>Append mode FAILED for [' + path + ']<<>>' + str(status);
		        log_array.append(log_string);

			print '<script>alert("COULD NOT ENABLE APPEND MODE: %s");</script>' % status[1];

	else:
		# disabling append mode command
                disable_apm_command = 'sudo chattr -R -a "/storage/' + path + '"';
                status = commands.getstatusoutput(disable_apm_command);

                if (status[0] == 0):
                        print "<script>alert('Append mode disabled for [%s]');</script>" % path;

		        log_string = str(common_methods.now) + '||From: ' + common_methods.remote_ip + '<<>>Append mode DISABLED for [' + path + ']<<>>' + str(status);
		        log_array.append(log_string);

                else:
                        print '<script>alert("COULD NOT DISABLE APPEND MODE: %s");</script>' % status[1];

		        log_string = str(common_methods.now) + '||From: ' + common_methods.remote_ip + '<<>>DISABLE append mode FAILED for [' + path + ']<<>>' + str(status);
		        log_array.append(log_string);

	common_methods.append_file(log_file, log_array);

	print "<script>location.href = 'main.py?page=share_det&act=append_mode_done';</script>";
		
else:
	common_methods.relogin();

