#!/usr/bin/python
import cgitb, common_methods, cgi, commands, re, sys, include_files
cgitb.enable();
form = cgi.FieldStorage();

sys.path.append('../modules/');
import disp_except;

sys.path.append('/var/nasexe/python/');
import cli_utils, shares, tools, smb;

session_user = 'Full Access';

try:
	if (session_user != ''):
		share_name = form.getvalue('share');
		share_path = form.getvalue('path');
		comment    = form.getvalue('comment');
		use_manual = form.getvalue('use_manual');
		action     = form.getvalue('cancel_but');
		if(len(share_name) > 24):
			if(use_manual == "on"):
				print "<script>parent.location.href = 'iframe_nas_settings.py?val=largeval';</script>"
			else:
				print "<script>location.href = 'iframe_nas_settings.py?val=largeval';</script>"
		else:
			params_array = [];

			if (comment != None):
				comment    = comment.replace ("'", "").strip();

			if (comment == None):
				comment = '';

			if (action == 'Cancel'):
				print "<script>location.href = 'iframe_nas_settings.py';</script>";

			else:
				# check whether share exists or not...
				trace_share = tools.get_share(share_name, debug=True);

				if (trace_share['id'] == 0):
					print "<script>alert('Share already exists!');</script>";
					if(use_manual == "on"):
						print "<script>parent.location.href = 'iframe_nas_settings.py';</script>";
					else:
						print "<script>location.href = 'iframe_nas_settings.py';</script>";

				else:
					sharepathsplit = share_path.split('/');

					disk = sharepathsplit[0];

					checkmount = cli_utils.is_disk_mounted(disk);

					if (checkmount['id'] > 0):
						print "<script>alert('The disk [%s] is not mounted. Please run the [Rescan Volumes], [Remount Volumes] from [TOOLS] option. Could not create share!');</script>" % disk;
						print "<script>parent.location.href = 'main.py?page=nas';</script>";

					else:
						shares_dic = {'name': '', 'path': '', 'comment': ''};
						shares_dic['name']       = share_name;
						shares_dic['path']       = share_path;
						shares_dic['comment']    = comment;
						check_dir_exist = tools.is_dir_exist("/storage/"+shares_dic['path'])
						if(check_dir_exist == True):
							shares_dic['create_dir'] = False
						else:
							shares_dic['create_dir'] = True
							
						createshare_status = tools.create_share(shares_dic);

						if (createshare_status['id'] == 0):
							share_string = share_name + ':/storage/' + share_path + ':' + comment;

							params_array.append(share_string);
							shares_global_file        = '/var/www/global_files/shares_global_file';
							common_methods.append_file(shares_global_file, params_array);
							print "<script>alert('Share Successfully Created!');</script>"
							if(use_manual == "on"):
								print """<script>parent.location.href = 'iframe_nas_settings.py'</script>""";
							else:
								print """<script>location.href = 'iframe_nas_settings.py'</script>""";

						else:
							print "<script>alert('Error during Share Creation!');</script>"
							
							logstatus = common_methods.sendtologs('error', 'Create Share', 'add_share.py', str(createshare_status));
							if(use_manual == "on"):
								print """<script>parent.location.href = 'iframe_nas_settings.py'</script>""";
							else:
								print """<script>location.href = 'iframe_nas_settings.py'</script>""";

except Exception as e:
	disp_except.display_exception(e);
