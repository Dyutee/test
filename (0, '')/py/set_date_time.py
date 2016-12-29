#!/usr/bin/python
import header, cgitb, ntp_client_conf, commands, common_methods, cgi, sys, os

sys.path.append('../modules/');
import disp_except;

sys.path.append('/var/nasexe/python/tools/')
import ntp

cgitb.enable();

querystring = os.environ['QUERY_STRING'];

try:
	existing_ntp_server = ntp_client_conf.server();
	mode_to_file = '';
	params_array = [];

	if (querystring.find('mode=ntp_time') > 0):
		if (existing_ntp_server == ''):
			existing_ntp_server = querystring[querystring.find('&ntp_server=') + len('&ntp_server='):];
			existing_ntp_server = existing_ntp_server.strip();
	
		mode_to_file = 'MODE=ntp_time';

		st=ntp_client_conf.enable_ntp(existing_ntp_server)
			
		commands.getoutput('sudo pkill ntp');
		settime = commands.getstatusoutput('sudo ntpdate "%s"' % existing_ntp_server);

		if (settime[0] == 0):
			params_array.append(mode_to_file);
			common_methods.write_file('/var/nasconf/set_date_global', params_array);
			print "<script>alert('Date/Time in sync with NTP server!')</script>";

		else:
			print "<script> alert('unable to connect to time server %s !')</script>" % existing_ntp_server;

	else:
		mode = header.form.getvalue('set_mode');

		if (mode == "manual"):
			setNewDate    = header.form.getvalue("setDate")
			mode_to_file = 'MODE=manual';

			# if date is already set for ntp, then disable ntp first and then set the date
			if (existing_ntp_server != ''):
				ntp_client_conf.disable_ntp(existing_ntp_server)
			
			# use the system date command to set the date
			getDate = commands.getoutput('sudo date --set="' + setNewDate + '"');

			# check whether the string 'IST' or 'UTC' is present
			check_for_date = getDate.find('IST');
			check_for_utc  = getDate.find('UTC');

			# if there is 'IST' then it is clear that date/time is changed
			if (check_for_date > 0 or check_for_utc > 0):
				print "<script>alert('Changed the system date/time!')</script>";
				params_array.append(mode_to_file);
				common_methods.write_file('/var/nasconf/set_date_global', params_array);

			else:
				print "<script>alert('Could not set date/time!')</script>";
			
		# if the mode selected is 'PC time'
		if (mode == "pc_time"):
			setSystemDate = header.form.getvalue("hid_pc_time")
			# entry to write to file
			mode_to_file = 'MODE=pc_time';

			# if ntp date/time is enabled, then disable it first
			if (existing_ntp_server != ''):
				ntp_client_conf.disable_ntp(existing_ntp_server)

			# use the system date command to set the date
			getDate = commands.getoutput('sudo date --set="' + setSystemDate + '"')

			# check whether the string 'IST' or 'UTC' is present
			check_for_date = getDate.find('IST');
			check_for_utc  = getDate.find('UTC');

			# if there is 'IST' then it is clear that date/time is changed
			if (check_for_date > 0 or check_for_utc > 0):
				print "<script>alert('System date/time set to local system time!')</script>";

				params_array.append(mode_to_file);
				common_methods.write_file('/var/nasconf/set_date_global', params_array);

			else:
				print "<script>alert('Could not set time!')</script>";

	print """<script>location.href = 'main.py?page=date';</script>""";

except Exception as e:
	disp_except.display_exception(e);
