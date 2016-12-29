#!/usr/bin/python
import cgitb, common_methods, os, commands, cgi, sys;
cgitb.enable();

sys.path.append('/var/nasexe/python/');
import acl 
import cli_utils
import tools
        
sys.path.append('../modules/');
import disp_except;

try:
	print """
	<script language = 'javascript' src = '../js/commons.js'></script>
	<link rel = 'stylesheet' href = '../css/design.css' />"""

	numarray = [];

	session_user = common_methods.get_session_user();
	opath = '';
	querystring = os.environ['QUERY_STRING'];

	path_acl = '';

	if (querystring.find('&path=') > 0):
		path_acl = common_methods.getsubstr(querystring, '&path=', '&');

	if (path_acl != ''):
		path_acl = path_acl.replace('/storage', '');

	disabledstyle = querystring[querystring.find('&dd=') + len('&dd='):];

	full_path_temp = '';

	if (session_user != ''):
		print """<script>parent.users_groups_frame.location.href = 'users_groups.py';</script>""";
		print """<script>parent.user_permissions.location.href = 'user_permissions.py';</script>""";
			
		checktmpsesspathfile = commands.getstatusoutput('sudo ls /var/nasconf/sess_path_file');

		if (checktmpsesspathfile[0] == 0):
			path_line = commands.getoutput('sudo grep "sess_path=" /var/nasconf/sess_path_file');
			path      = path_line[path_line.find('=') + 1:];

		else:
			tarray = [];
			tarray.append('sess_path=');

			common_methods.write_file('/var/nasconf/sess_path_file', tarray);

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

		ppath = '/storage/' + path_for_get_details;

		get_acl_users_command  = acl.get_user(ppath);
		get_acl_groups_command = acl.get_group(ppath);
		
		uarray = [];
		garray = [];
		params_array = [];
		getusers  = '';
		getgroups = '';

		if (get_acl_users_command.find('user:') > 0):
			getusers = get_acl_users_command[get_acl_users_command.find('user:'):get_acl_users_command.rfind('#')];

		if (getusers != ''):
			getusers = getusers.strip();

		if (get_acl_groups_command.find('group:') > 0):
			getgroups = get_acl_groups_command[get_acl_groups_command.find('group:'):get_acl_groups_command.rfind('#')];

		if (getgroups != ''):
			getgroups = getgroups.strip();

		uarray = getusers.split('#');
		garray = getgroups.split('#');

		if (len(uarray) > 0):
			for u in uarray:
				ustring = path_for_get_details + ':' + u;
				ustring = ustring.replace(':user:', ':u:');
				params_array.append(ustring);

		if (len(garray) > 0):
			for g in garray:
				gstring = path_for_get_details + ':' + g;
				gstring = gstring.replace(':group:', ':g:');
				params_array.append(gstring);

		filetowrite = '/tmp/getusers';

		common_methods.write_file(filetowrite, params_array);

		if (full_path == ''):
			full_path = path;

		full_path = full_path.replace('/storage/', '');
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

		print "<table align = 'center' width = '100%'>";
		print " <tr>";

		if (count == 0):
			full_path = '/storage/' + full_path;

			params_array.append(full_path);

			dir_path_file = open('/var/www/global_files/dir_path_file', 'w');
			dir_path_file.write(full_path);

			#get_contents_command = 'sudo /var/nasexe/show_dirs_files ' + full_path;
			get_contents_command = 'su - user1 /var/nasexe/show_dirs_files ' + full_path;
			#print get_contents_command
			commands.getoutput(get_contents_command);

			dirs_file = '/var/nasconf/directory_structure_output1';
			dirs_array = common_methods.read_file(dirs_file);

			count = int(count) + 1;

			full_path = full_path.replace('\n', '');
			#print 'PATH:'+str(full_path)
			#disk_path =full_path[full_path.find('/')+1:full_path.rfind('/')]
			#diskname=disk_path[disk_path.rfind('/')+1:]
			#diskname = full_path[full_path.rfind('/')+1:]
			#print diskname
			#check_disk_mount = cli_utils.is_disk_mounted(diskname,debug="no")
			#print check_disk_mount
			#if(check_disk_mount['id'] == 2):
                        	#err_msg = diskname+str('Disk Not Mounted')
                                #err_msg = 'Disk Not Mounted'
                                #print err_msg
                        #else:
                                #print
			#print full_path
			#--------------modified code on 15-12-2014 Check Path Exit or Not------------------------
			chk_path = tools.is_dir_exist(full_path)
			#exit();
			if(chk_path == True):
                        	list_all_dir = os.listdir(full_path)
			else:
				list_all_dir = ''
			#-----------------------End-------------------------------------------------------------
			#print list_all_dir
			#exit();

			#------------------- New Code Start ---------------------#
                        #list_all_dir = os.listdir(full_path)
			#print list_all_dir
                        #------------------- New Code End ---------------------#


			if (len(dirs_array) == 0):
				print '<B>No files/folders!</B>';
					
			img_text = '<img src = \'../images/folder-icon.png\'>';

                        if (len(dirs_array) > 0):
                                for g in list_all_dir:
                                        numarray.append(rowcount);

                                        if (limit in numarray):
                                                lbreak = '</tr><tr>';

                                        else:
                                                lbreak = '';

                                        g = g.strip();

                                        test_dirs = '#' + g;
                                        index_of_d = test_dirs.find('d');

                                        if (index_of_d == 1):
                                                img_text = '<img src = \'../images/folder-icon.png\'>';

                                        #else:
                                        #       img_text = '<img src = \'../images/file-icon.png\'>';

                                        g = g[g.find(' ') + 1:];
                                        g = g.strip();
                                        g = g.replace(' ', '%20');
                                        dir_display = g.replace('%20', ' ');

                                        full_path1 = full_path.replace('/storage/', '');
                                        if(os.path.isdir(full_path+"/"+g) == True):
                                                print """<td>%s <a class = 'share_link' href = 'show_dir1.py?dir_name=%s&count=%s&full_path=%s&dname=%s&result=result&spath=%s' ondblclick = 'return false;' onclick = 'return show_path("%s", "%s", "dir");'>%s</a><BR></td>%s""" % (img_text, g, count, full_path1, g, path_acl, full_path1, g, dir_display, lbreak);


					#else:
					#	print """<td>%s <a class = 'share_link' href = 'show_dir1.py?full_path=%s&dname=%s&result=result&spath=%s' ondblclick = 'return false;' onclick = 'return show_path("%s", "%s", "file");'>%s</a><BR></td>%s""" % (img_text, full_path1, dirs, path_acl, full_path1, dirs, dir_display, lbreak);

					limit = limit + 1;
					rowcount = rowcount + 6;

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

			#------------------- New Code Start ---------------------#
                        list_all_dir = os.listdir(full_path)
                        #print list_all_dir
                        #------------------- New Code End ---------------------#
			img_text = '<img src = \'../images/folder-icon.png\'>';

			dirs_file = '/var/nasconf/directory_structure_output1';
			dirs_array = common_methods.read_file(dirs_file);
			#print '<br/>'
			dirs_array = str(dirs_array).strip();
			#print '<br/>'

			path1 = '/storage/' + path;

			if (full_path_temp == '/storage'):
				print "<script>parent.location.href = 'main.py?page=nas';</script>";

			if (full_path != path1):
				base_name_command = 'sudo basename "' + full_path + '"';
				base_name = commands.getoutput(base_name_command);
				base_name = base_name.strip();

				full_path1 = full_path.replace('/storage/', '');
				
				print  """<a class = 'share_link' href = 'show_dir1.py?dir_name=%s&count=%s&dot_path=2dots&spath=%s' ondblclick = 'return false;' onclick = 'return show_path("%s", "2dots");'><img width = '35' height = '20' src = '../images/backButton.jpg' border = '0' title = 'Back'></a> | <font face='Arial' size = '2'><B><I><U>%s</U></I></B></font><BR>""" % (base_name, count, path_acl, full_path1, full_path1);

			count = int(count) + 1;
			#print 'DIR:'+str(dirs_array)

			if (len(dirs_array) > 0):
				for g in list_all_dir:
					numarray.append(rowcount);

					if (limit in numarray):
						lbreak = '</tr><tr>';

					else:
						lbreak = '';

					g = g.strip();
					#print 'G:'+str(g)

					test_dirs = '#' + g;
					#print 'DIR1:'+str(test_dirs)
					index_of_d = test_dirs.find('d');
					#print index_of_d

					if (index_of_d == 1):
						img_text = '<img src = \'../images/folder-icon.png\'>';

					#else:
					#	img_text = '<img src = \'../images/file-icon.png\'>';

					#g = g[g.find(' ') + 1:];
					#g = g.strip();
					#g = g.replace(' ', '%20');
					dir_display = g.replace('%20', ' ');

					full_path1 = full_path.replace('/storage/', '');

					#print full_path+"/"+g
					#print os.path.isdir(full_path+"/"+g)
					if(os.path.isdir(full_path+"/"+g) == True):
						print """<td>%s <a class = 'share_link' href = 'show_dir1.py?dir_name=%s&count=%s&full_path=%s&dname=%s&result=result&spath=%s' ondblclick = 'return false;' onclick = 'return show_path("%s", "%s", "dir");'>%s</a><BR></td>%s""" % (img_text, g, count, full_path1, g, path_acl, full_path1, g, dir_display, lbreak);

					#else:
					#	print """<td>%s <a class = 'share_link' href = 'show_dir1.py?full_path=%s&dname=%s&result=result&spath=%s' ondblclick = 'return false;' onclick = 'return show_path("%s", "%s", "file");'>%s</a><BR></td>%s""" % (img_text, full_path1, dirs, path_acl, full_path1, dirs, dir_display, lbreak);

					limit = limit + 1;
					rowcount = rowcount + 6;

			params_array = [];

			disk_file = open('/var/www/global_files/dir_path_file', 'a');
			
			disk_file.write("\n" + full_path);

	else:
		common_methods.relogin();

except Exception as e:
	disp_except.display_exception(e);
