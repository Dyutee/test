#!/usr/bin/python
import common_methods, cgitb, commands, os, sys

sys.path.append('../modules/');
import disp_except;

try:
	numarray = [];
	cgitb.enable();

	print "<html><head>";
	print "<script language = 'javascript' src = '../js/commons.js'></script>";
	print "</head><body>";

	prev_path  = '';
	dir_name   = '';
	nas_dsk    = '';
	dot_path   = '';
	dirs_array = [];
	full_path  = '/storage';
	count      = 0;
	fullpath   = '';

	nasdisksarray = [];

	nasdisksarray = common_methods.get_nas_disks();

	querystring = os.environ["QUERY_STRING"];

	checkstorage = commands.getoutput('cat /var/www/global_files/dir_path_file');
	checkstorage = checkstorage.strip();

	if (querystring.find('dir_name') >= 0):
		dir_name = common_methods.getsubstr(querystring, 'dir_name=', '&');

	if (querystring.find('&dotpath=') > 0):
		dot_path = common_methods.getsubstr(querystring, '&dotpath=', '&');

	if (querystring.find('&count=') > 0):
		count = common_methods.getsubstr(querystring, '&count=', '&');

	if (dot_path == '2dots'):
		#if (dir_name == ''):
		#	dirs_array = [];

		#	for nasdisks in nasdisksarray:
		#		dirs_array.append('dxxx ' + nasdisks);

		count = common_methods.getsubstr(querystring, '&count=', '&');
		#count = int(count) - 1;

	if (querystring.find('&full_path=') > 0):
		full_path = common_methods.getsubstr(querystring, '&full_path=', '&');

	dir_name = dir_name.replace('%20', ' ');

	if (dot_path != '2dots'):
		filetoappend = open('/var/www/global_files/dir_path_file', 'w');
		filetoappend.write(full_path);

	get_disks_command = 'sudo /var/nasexe/show_dirs_files1 "' + full_path + '"';

	if (dot_path == '2dots'):
		get_disks_command = 'sudo /var/nasexe/show_dirs_files1 "/storage/' + full_path + '"';
		#count = int(count) - 1;

	get_disks_command = get_disks_command.replace('%20', ' ');

	commands.getoutput(get_disks_command);

	dirsfile = '/var/nasconf/directory_structure_output2';
	dirs_array = common_methods.read_file(dirsfile);

	limit = 1;
	lbreak = '';
	rowcount = 3;

	params_array = [];

	print "<table align = 'center' width = '100%' border = '1' style = 'border: 1px solid lightgrey; border-collapse: collapse;'>";
	print "	<tr>";

	if (dir_name == '' or full_path == '/storage'):
		dirs_array = [];

		for nasdisks in nasdisksarray:
			dirs_array.append('dxxx ' + nasdisks);

	if (count == 0):
		if (len(dirs_array) > 0):
			count = int(count) + 1;

			for dirs in dirs_array:
				numarray.append(rowcount);

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

				dirs = dirs[dirs.find(' '):];
				dirs = dirs.strip();
				
				if (dirs != 'pub' and dirs != 'share' and dirs != 'ftp'):
					full_path1 = '/storage/' + dirs;
			
					if (dot_path == '2dots'):
						get_latest_path_command = 'sudo tail -1 /var/www/global_files/dir_path_file';
						full_path = commands.getoutput(get_latest_path_command);

						full_path = full_path[0:full_path.rfind('/')];
						prev_path = full_path[0:full_path.rfind('/')];
						prev_path = prev_path[prev_path.rfind('/') + 1:]
						path_file = open('/var/www/global_files/dir_path_file', 'a');
						path_file.write("\n" + full_path);

					full_path = commands.getoutput('sudo tail -1 /var/www/global_files/dir_path_file');

					if (index_of_d == 1):
						print """<td>%s <a style = 'font: 12px Arial; color: #2E2E2E; font-weight: bold; text-decoration: none;' class = 'share_link' href = 'show_dir.py?dir_name=%s&count=%s&full_path=%s&dname=%s' ondblclick = 'return false;' onclick = 'return show_shares_path("%s", "%s", "dir");'>%s</a><BR></td>%s""" % (img_text, dirs, count, full_path1, dirs, full_path1, dirs, dirs, lbreak);

						limit = limit + 1;

				rowcount = rowcount + 3;

		else:
			print "<B>No Files/Folders!</B>";

	else:
		count = int(count) + 1;
		limit = 1;

		full_path = full_path.replace('%20', ' ');

		if (dot_path == '2dots'):
			get_latest_path_command = 'sudo tail -1 /var/www/global_files/dir_path_file';
			full_path = commands.getoutput(get_latest_path_command);

			full_path = full_path[0:full_path.rfind('/')];
			prev_path = full_path[0:full_path.rfind('/')];
			prev_path = prev_path[prev_path.rfind('/') + 1:]
			path_file = open('/var/www/global_files/dir_path_file', 'a');
			path_file.write("\n" + full_path);

			full_path_temp = full_path;

		get_dir_contents_command = 'sudo /var/nasexe/show_dirs_files1 "' + full_path + '"';
		get_dir_contents_command = get_dir_contents_command.replace('%20', ' ');
		commands.getoutput(get_dir_contents_command);

		if (dot_path != '2dots'):
			filetowrite = open('/var/www/global_files/dir_path_file', 'w');
			filetowrite.write(full_path);

		dirs_file = '/var/nasconf/directory_structure_output2';
		dirs_array = common_methods.read_file(dirs_file);
		
		revpath = full_path[0:full_path.rfind('/')];
		prev_path = revpath;
		getfullpath = revpath[revpath.rfind('/') + 1:];
		
		if (prev_path.find('/storage/') == 0):
			prev_path = prev_path[prev_path.find('/storage/') + len('/storage/'):];

		if (full_path.find('/storage/') == 0):
			fullpath = full_path[full_path.find('/storage/') + len('/storage/'):];

		fullpath = fullpath.replace('%20', ' ');

		if (full_path != '/storage'):
			print """<a style = 'font: 12px Arial; color: #2E2E2E; font-weight: bold; text-decoration: none;' href = 'show_dir.py?dir_name=%s&count=%s&sh=sh&com=com&use_manual=use_manual&dotpath=2dots&full_path=%s&dname=' ondblclick = 'return false;' onclick = 'return show_shares_path("%s", "dots", "%s");'><img width = '35' height = '20' src = '../images/backButton.jpg' /></a> | <font face='Arial' size = '2'><B><I><U>%s</U></I></B></font><BR>""" % (getfullpath, count, prev_path, fullpath, prev_path, fullpath);

		if (dir_name == '' or full_path == '/storage'):
			dirs_array = [];

			for nasdisks in nasdisksarray:
				dirs_array.append('dxxx ' + nasdisks);

		if (len(dirs_array) > 0):
			for dirs in dirs_array:
				numarray.append(rowcount);

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
				dirs = dirs.replace(' ', '%20');
				dir_display = dirs.replace('%20', ' ');

				dirs = dirs.strip();
		
				full_path1 = full_path + '/' + dir_display;

				if (index_of_d == 1):
					if (dir_display != 'snapshot' and dir_display != 'pub' and dir_display != 'share' and dir_display != 'ftp'):
						print """<td>%s <a style = 'font: 12px Arial; color: #2E2E2E; font-weight: bold; text-decoration: none;' class = 'share_link' href = 'show_dir.py?dir_name=%s&count=%s&full_path=%s&dname=%s&result=result&spath=' ondblclick = 'return false;' onclick = 'return show_shares_path("%s", "%s", "dir");'>%s</a><BR></td>%s""" % (img_text, dirs, count, full_path1, dirs, full_path1, dirs, dir_display, lbreak);

						limit = limit + 1;

				rowcount = rowcount + 3;

	print "</tr></table>";
	print "</body></html>";

except Exception as e:
	disp_except.display_exception(e);
