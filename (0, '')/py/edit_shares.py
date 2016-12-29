#!/usr/bin/python
import cgitb, cgi, common_methods, sys, commands, include_files
cgitb.enable();

# retrieve the session user from common_methods.py
session_user = common_methods.get_session_user();

# create an instance of FieldStorage()
form = cgi.FieldStorage();

# include the /var/nasexe/python/ path to import the modules and call the methods of the python scripts
sys.path.append('/var/nasexe/python/');
import smb;
import tools

#get_ha_nodename = tools.get_ha_nodename()

# write output to log file declared in common_methods.py
log_array = [];
log_file = common_methods.log_file;
outputstring = '';
status = '';

# get the values submitted from the form
use_smb = form.getvalue('conf');

if (use_smb == None):
	use_smb = form.getvalue('reconf');

remove_conf = form.getvalue('removeconf');

sharefileperms = '0755';
sharedirsperms = '0665';
domainname = '';

message = '';

if (session_user != ''):
	# get data from all fields
	share   = form.getvalue('hid_share');

	checksmb = commands.getstatusoutput('ls "/var/nasconf/smbconf/%s"' % share);

	if (checksmb[0] == 0):
		getsharesinfo = smb.show(share);

		sharesinfo = getsharesinfo['share'];

		sharefileperms = sharesinfo['file_perm'];
		sharedirsperms = sharesinfo['dir_perm'];

		# create one empty dictionary with the key names
	sharesinput = {"name":"","path":"","comment":"","writable":"","browsable":"","guest_ok":"","public":"","valid_users":"","use_smb":"","recycle_enable":"","recycle_repo":"","audit_enable":"", "audit_opts":"", "file_perm":sharefileperms, "dir_perm":sharedirsperms};
	
	# if smb option is clicked then get the other values of the smb form.
	#if (use_smb == 'enablesmbconf' or use_smb == 'editsmbconf'):

	get_ha_nodename	  = form.getvalue('get_ha_nodename')
	par_share_det = tools.get_share(share,debug=False)
        share_ha_nodename = par_share_det["share"]["node"]

	if (use_smb == 'conf' or use_smb == 'reconf'):
		#smb.unconfigure(share,get_ha_nodename);

		# get data from the form
		comment           = form.getvalue('hid_comm');
		path              = form.getvalue('hid_path');
		read_only         = form.getvalue('read_only');
		visible           = form.getvalue('visible');
		privileges        = form.getvalue('priv');
		recycle_opt       = form.getvalue('enable_recycle');
		audit_opt         = form.getvalue('enable_audit');
		audit_recycle_opt = form.getvalue('aud_recycle');
		domainname        = form.getvalue('domainslist');
		
		if (domainname == 'local'):
			domainname = '';

		# comment should not be None
		if (comment == None):
			comment = '';

		if (visible == None):
			visible = '';

		comment = comment.replace("\\'", "");

		vfs_obj        = '';
		full_audit     = '';
		recycle_string = '';

		granted_users_array  = [];
		granted_groups_array = [];

		granted_users_array  = form.getvalue('grant_users[]');
		granted_groups_array = form.getvalue('grant_groups[]');

		smbusers_list = '';

		# form a string of users enclosed with double quotes and separated by a single space
		if (str(type(granted_users_array)) == "<type 'list'>"):
			if (len(granted_users_array) > 0):
				for gusers in granted_users_array:
					if (gusers != '' or gusers != None):
						gusers = gusers.strip();
						smbusers_list += '"' + gusers + '"' + ' ';

		else:
			if (granted_users_array != None):
				smbusers_list += '"' + str(granted_users_array) + '"' + ' ';

		# form a string of groups enclosed with double quotes and separated by a single space
		if (str(type(granted_groups_array)) == "<type 'list'>"):
			if (len(granted_groups_array) > 0):
				for ggroups in granted_groups_array:
					if (ggroups != '' or ggroups != None):
						if (ggroups.find('@') != 0):
							ggroups = '@' + ggroups;

						ggroups = ggroups.strip();
						smbusers_list += '"' + ggroups + '"' + ' ';

		else:
			if (granted_groups_array != None):
				granted_groups_array = str(granted_groups_array);

				if (granted_groups_array.find('@') != 0):
					granted_groups_array = '@' + granted_groups_array;

				smbusers_list += '"' + granted_groups_array + '"' + ' ';

		smbusers_list = common_methods.replace_chars(smbusers_list, 'texttochar');

		# remove trailing spaces and following spaces from smbusers_list
		smbusers_list = smbusers_list.strip();

		recycle_enable = 'no';
		recycle_path   = '';
		audit_string   = '';
		audit_enable   = 'no';

		# if audit/recycle option is checked
		if (audit_recycle_opt == 'on'):

			# if audit option is checked
			if (audit_opt == 'on'):
				audit_string = form.getvalue('file_options[]');
				audit_string = str(audit_string);
				audit_string = audit_string[audit_string.find('[') + 1:audit_string.find(']')];
				audit_string = audit_string.replace('\'', '');
				audit_string = audit_string.replace(',', '');
				audit_enable = 'yes';
				audit_string = audit_string.strip();

			# if recycle option is checked
			if (recycle_opt == 'on'):
				recycle_enable = 'yes';
				recycle_path   = '/storage/' + form.getvalue('recycle_path');

		# default values for the options.
		writable       = 'yes'; # readonly option should be checked by default
		browsable      = 'no';  
		guestok        = 'no'; # guest option is checked by default
		tpublic        = 'no';
		tuse_smb       = 'no';
		
		if (read_only == 'on'):
			writable = 'no';

		if (visible == 'on'):
			browsable = 'yes';

		if (privileges == 'public' or privileges == 'guest' or privileges == ''):
			tpublic       = 'yes';
			guestok       = 'yes';
			smbusers_list = '';

		#if (use_smb == 'enablesmbconf' or use_smb == 'editsmbconf'):
		if (use_smb == 'conf' or use_smb == 'reconf'):
			tuse_smb = 'yes';

		checkstorage = path.find('/storage/');

		if (checkstorage < 0):
			path = '/storage/' + path;

		smbusers_list = common_methods.replace_chars(smbusers_list, 'texttochar');
		smbusers_list = smbusers_list.strip();

		# update the dictionary assigning each value for a key 
		sharesinput['name']           = share;
		sharesinput['path']           = path;
		sharesinput['comment']        = comment;
		sharesinput['writable']       = writable;
		sharesinput['browsable']      = browsable;
		sharesinput['guest_ok']       = guestok;
		sharesinput['public']         = tpublic;
		sharesinput['valid_users']    = smbusers_list;
		sharesinput['use_smb']        = tuse_smb;
		sharesinput['recycle_enable'] = recycle_enable;
		sharesinput['recycle_repo']   = recycle_path;
		sharesinput['audit_enable']   = audit_enable;
		sharesinput['audit_opts']     = audit_string;

		# input the dictionary to the function configure() of smb module
		status = smb.configure(sharesinput,share_ha_nodename);

		outarray = [];
		# check the return status

		if (status['id'] == 0):
			commands.getoutput('sudo sed -i "/^$/d" /etc/samba/smb.conf');
			
		else:
			common_methods.sendtologs('ERROR', 'Enable SMB Settings', 'UI', '"edit_shares.py", ' + str(status['desc']));
			#print '<script>alert("Could not configure SMB for share [%s]! %s");</script>' % (share, status['desc']);
			#print "<div id='id_trace_err'>"
			#print "Error Occured while Setting the SMB!"
                	#print "</div>"

	elif (remove_conf == 'removeconf'):
		status = smb.unconfigure(share,share_ha_nodename);

		if (status['id'] == 0):
			print "<script>alert('Unconfigured SMB for [%s]!');</script>" % share;

		else:
			print "<script>alert('Unconfigure SMB FAILED for [%s]! %s');</script>" % (share, status['desc']);

	# create the log string to write to log file
	log_string = str(common_methods.now) + '<<>>From: ' + common_methods.remote_ip + '<<>>' + str(sharesinput) + '<<>>' + str(status);
	log_array.append(log_string);

	common_methods.append_file(log_file, log_array);
		
	#print "<script>location.href = 'show_shares.py?s1=%s&act=share_smb_done&stat=y';</script>" % share;
	if (remove_conf == 'removeconf'):
		#print "<script>location.href = 'smb_settings.py?uu=&share_name=%s&dom=%s&mess1=%s';</script>" % (share, domainname, message);
		#print "<script>location.href = 'main.py?page=smb_set&uu=&share_name=%s&dom=%s&mess1=%s';</script>" % (share, domainname, message);
		print "<script>location.href = 'iframe_smb_settings.py?uu=&share_name=%s&dom=%s&mess1=%s';</script>" % (share, domainname, message);

	else:
		#print "<script>location.href = 'smb_settings.py?uu=&share_name=%s&dom=%s&mess=%s';</script>" % (share, domainname, message);
		#print "<script>location.href = 'main.py?page=smb_set&uu=&share_name=%s&dom=%s&mess=%s';</script>" % (share, domainname, message);
		print "<script>location.href = 'iframe_smb_settings.py?uu=&share_name=%s&dom=%s&mess=%s';</script>" % (share, domainname, message);

else:
	common_methods.relogin();
