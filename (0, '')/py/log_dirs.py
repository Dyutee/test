#!/usr/bin/python
import cgitb, common_methods, os, commands, cgi, sys;
cgitb.enable();

sys.path.append('/var/nasexe/python/');
import acl;
        
sys.path.append('../modules/');
import disp_except;

print """
<script language = 'javascript' src = '../js/commons.js'></script>
<link rel = 'stylesheet' href = '../css/design.css' />
<link rel = 'stylesheet' href = '../css/content.css' />
<link rel = 'stylesheet' href = '../css/style.css' />
"""

try:
	numarray = [];

	querystring = os.environ['QUERY_STRING'];

	path_acl = '/var/log';

	full_path_temp = '';

	path_line = commands.getoutput('sudo grep "sess_path=" /var/nasconf/sess_path_file');
	path      = path_line[path_line.find('=') + 1:];

	path_list = '';
	dir_name  = '';
	full_path = '';
	count     = 0;
	dot_path  = '';
	dname     = '';
	get_path  = '';
	path_for_get_details = '';
		
	if (querystring.find('dir_name=') >= 0):
		dir_name = common_methods.getsubstr(querystring, 'dir_name=', '&');

		dir_name = dir_name.strip();
		dir_name = dir_name.replace('%20', ' ');

	if (querystring.find('&path=') >= 0):
		full_path = common_methods.getsubstr(querystring, 'path=', '&');

	if (querystring.find('&count=') >= 0):
		count     = common_methods.getsubstr(querystring, 'count=', '&');

	if (querystring.find('&dot_path=') >= 0):
		dot_path  = common_methods.getsubstr(querystring, 'dot_path=', '&');

	if (querystring.find('dname=') >= 0):
		dname     = common_methods.getsubstr(querystring, 'dname=', '&');

	if (querystring.find('spath=') >= 0):
		get_path  = common_methods.getsubstr(querystring, 'spath=', '&');

	if (querystring.find('full_path=') >= 0):
		path_for_get_details = common_methods.getsubstr(querystring, 'full_path=', '&') + '/' + dname;

	if (path_for_get_details == '/'):
		path_for_get_details = get_path;
		
	if (path_for_get_details == ''):
		path_for_get_details = path;

	path_for_get_details = path_for_get_details + '$$';
	path_for_get_details = path_for_get_details.replace('/$$', '');
	path_for_get_details = path_for_get_details.replace('$$', '');
	path_for_get_details = path_for_get_details.strip();

	ppath = path_for_get_details;

	get_acl_users_command  = acl.get_user(ppath);
	get_acl_groups_command = acl.get_group(ppath);

	uarray = [];
	garray = [];
	params_array = [];

	if (full_path == ''):
		full_path = path;

	path_array = [];
	path_array.append('sess_path=' + full_path);

	filetowrite = '/var/nasconf/sess_path_file';
	common_methods.write_file(filetowrite, path_array);

	if (count == ''):
		count = 0;

	params_array = [];

	limit = 1;
	lbreak = '';
	rowcount = 6;

	print """<table border = '0' align = 'center' width = '100%'>""";
	print """	<tr>""";
		
	if (count == 0):
		full_path = full_path;

		params_array.append(full_path);

		dir_path_file = open('/var/www/global_files/dir_path_file', 'w');
		dir_path_file.write(full_path);

		get_contents_command = 'sudo /var/nasexe/show_dirs_files ' + full_path;
		commands.getoutput(get_contents_command);

		dirs_file = '/var/nasconf/directory_structure_output1';
		dirs_array = common_methods.read_file(dirs_file);

		count = int(count) + 1;

		full_path = full_path.replace('\n', '');

		if (len(dirs_array) == 0):
			print '<B>No files/folders!</B>';

		if (len(dirs_array) > 0):
			for dirs in dirs_array:
				numarray.append(rowcount);

				#if (limit == 6 or limit == 12 or limit == 18 or limit == 24 or limit == 30 or limit == 36 or limit == 42 or limit == 48 or limit == 54 or limit == 60):
				if (limit in numarray):
					lbreak = '</tr><tr>';

				else:
					lbreak = '';

				dirs = dirs.strip();

				test_dirs = '#' + dirs;
				index_of_d = test_dirs.find('d');

				if (index_of_d == 1):
					img_text = '<img src = \'../images/folder-icon.png\'>';

				else:
					img_text = '<img src = \'../images/file-icon.png\'>';

				dirs = dirs[dirs.find(' ') + 1:];
				dirs = dirs.strip();
				dirs = dirs.replace(' ', '%20');
				dir_display = dirs.replace('%20', ' ');
				
				if (index_of_d == 1):
					print """<td>%s <a style = "margin-right: 15px;" class = 'share_link' href = 'log_dirs.py?dir_name=%s&count=%s&full_path=%s&dname=%s&result=result&spath=%s' ondblclick = 'return false;' onclick = 'return show_lpath("%s", "%s", "dir");'>%s</a></td>%s""" % (img_text, dirs, count, full_path, dirs, path_acl, full_path, dirs, dir_display, lbreak);

				else:
					print """<td>%s <a style = "margin-right: 15px;" class = 'share_link' href = '#' ondblclick = 'return false;' onclick = 'return show_lpath("%s", "%s/%s", "file");'>%s</a></td>%s""" % (img_text, full_path, path_for_get_details, dir_display, dir_display, lbreak);

				limit = limit + 1;
				rowcount = rowcount + 6;

				print """<input type = 'hidden' name = 'pathgetfile' value = '%s/%s'>""" % (path_for_get_details, dir_display);

	elif (count > 0):
		get_latest_path_command = 'sudo tail -1 /var/www/global_files/dir_path_file';
		get_latest_path = commands.getoutput(get_latest_path_command);

		full_path = get_latest_path;

		if (dot_path == '2dots'):
			full_path = full_path[:full_path.rfind('/')];
			path_file = open('/var/www/global_files/dir_path_file', 'a');
			path_file.write("\n" + full_path);

			full_path_temp = full_path;

		else:
			full_path = full_path + '/' + dir_name;

		get_dir_contents_command = 'sudo /var/nasexe/show_dirs_files ' + full_path;
		commands.getoutput(get_dir_contents_command);

		dirs_file = '/var/nasconf/directory_structure_output1';
		dirs_array = common_methods.read_file(dirs_file);

		path1 = path;

		if (full_path != path1):
			base_name_command = 'sudo basename "' + full_path + '"';
			base_name = commands.getoutput(base_name_command);
			base_name = base_name.strip();

			print  """<a style = "margin-right: 15px;" class = 'share_link' href = 'log_dirs.py?dir_name=%s&count=%s&dot_path=2dots&spath=%s' ondblclick = 'return false;' onclick = 'return show_lpath("%s", "2dots");'><img width = '35' height = '20' src = '../images/backButton.jpg' border = '0' title = 'Back'></a>""" % (base_name, count, path_acl, full_path);

		count = int(count) + 1;

		if (len(dirs_array) > 0):
			for dirs in dirs_array:
				numarray.append(rowcount);

				#if (limit == 6 or limit == 12 or limit == 18 or limit == 24 or limit == 30 or limit == 36 or limit == 42 or limit == 48 or limit == 54 or limit == 60):
				if (limit in numarray):
					lbreak = '</tr><tr>';

				else:
					lbreak = '';

				dirs = dirs.strip();

				test_dirs = '#' + dirs;
				index_of_d = test_dirs.find('d');

				if (index_of_d == 1):
					img_text = '<img src = \'../images/folder-icon.png\'>';

				else:
					img_text = '<img src = \'../images/file-icon.png\'>';

				dirs = dirs[dirs.find(' ') + 1:];
				dirs = dirs.strip();
				dirs = dirs.replace(' ', '%20');
				dir_display = dirs.replace('%20', ' ');

				if (index_of_d == 1):
					print """<td>%s <a style = "margin-right: 15px;" class = 'share_link' href = 'log_dirs.py?dir_name=%s&count=%s&full_path=%s&dname=%s&result=result&spath=%s' ondblclick = 'return false;' onclick = 'return show_lpath("%s", "%s", "dir");'>%s</a></td>%s""" % (img_text, dirs, count, full_path, dirs, path_acl, full_path, dirs, dir_display, lbreak);

				else:
					print """<td>%s <a style = "margin-right: 15px;" class = 'share_link' href = '#' ondblclick = 'return false;' onclick = 'return show_lpath("%s", "%s/%s", "file");'>%s</a>%s""" % (img_text, full_path, path_for_get_details, dir_display, dir_display, lbreak);

				print """<input type = 'hidden' name = 'pathgetfile' value = '%s/%s'></td>""" % (path_for_get_details, dir_display);

				limit = limit + 1;
				rowcount = rowcount + 6;

		params_array = [];

		disk_file = open('/var/www/global_files/dir_path_file', 'a');
		disk_file.write("\n" + full_path);

	print """</tr></table>""";

	print """<BR><BR><center><div><!--<span id="button-one"><button type = 'button'  name = 'Close' value = 'Close Window' onclick = 'window.close();' style = 'background-color:#ffffff; border:none; float: center;font-size: 100%;' title="View Logs"><a href = '#'  style="font-size:80%;  width: 100%;">Close Window</a></button></span>-->
<button class = 'button_example' type="button" name = 'close' value = 'Close Window' onclick = 'window.close();'>Close Window</button>

</div></center>"""

except Exception as e:
	disp_except.display_exception(e);
