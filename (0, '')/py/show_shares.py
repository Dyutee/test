#!/usr/bin/python
import cgitb, cgi, common_methods, commands, os, sys, traceback
cgitb.enable();

print common_methods.wait_message;

response = 'edit_share_done';

sys.path.append('/var/nasexe/python/');
import smb;
from fs2global import *

sys.path.append('/var/www/fs4/modules/');
import disp_except;

querystring = os.environ['QUERY_STRING'];

try:
	log_array = [];
	log_file = common_methods.log_file;

	"""
	when choosing a share from the dropdown of 'Configure share', the share name is passed via the url to this page.
	here the share_name is retrieved from the querystring using the method 'getsubstr' defined in common_methods.py.
	'response' is retrieved to highlight the form or page from which the submission took place.
	"""
	share_name = common_methods.getsubstr(querystring, 's1=', '&');
	response   = common_methods.getsubstr(querystring, '&act=', '&');	
	mdisks = ''

	if (querystring.find('md=') > 0):
		mdisks = querystring[querystring.find('&md=') + len('&md='):];

	# her the share name is checked in '/var/nasconf/shares' file to check for SMB.
	# if found, the details are written to /tmp/details_of_share file.
	#find_share_command = 'sudo grep "\[' + share_name + '\]" /var/nasconf/shares';
	#find_share         = commands.getoutput(find_share_command).strip();

	find_share = commands.getstatusoutput('ls %s%s' % (smb_share_conf_dir, share_name));

	shares_file = '/tmp/details_of_share';

	if (find_share[0] == 0):
		statusline = smb.show(share_name);

		log_string = str(common_methods.now) + '||From: ' + common_methods.remote_ip + '<<>>' + str(statusline) + '<<>>SHOW SHARES';
		log_array.append(log_string);

		common_methods.append_file(log_file, log_array);

		status = statusline['share'];

		sharename_string  = 'sharename=' + status['name'];
		sharepath_string  = 'sharepath=' + status['path'];
		sharecomm_string  = 'sharecomm=' + status['comment'];
		audit_string      = 'auditoption=' + status['audit_opts'];
		browsable_option  = 'browsable=' + status['browsable'];
		recycle_option    = 'recycle=' + status['recycle_enable'];
		use_smb_option    = 'use_smb=' + status['use_smb'];
		writable_option   = 'writable=' + status['writable'];
		recycle_repo_opt  = 'recycle_repo=' + status['recycle_repo'];
		guest_ok_option   = 'guest_ok=' + status['guest_ok'];
		validusers_option = 'valid_users=' + status['valid_users'];
		audit_option      = 'audit_enable=' + status['audit_enable'];
		public_option     = 'public=' + status['public'];
		err_status        = 'err_status=' + str(statusline['id']);
		description       = 'description=' + statusline['desc'];

		share_det_array = [];
		
		share_det_array.append(sharename_string);
		share_det_array.append(sharepath_string);
		share_det_array.append(sharecomm_string);
		share_det_array.append(audit_string);
		share_det_array.append(browsable_option);
		share_det_array.append(recycle_option);
		share_det_array.append(use_smb_option);
		share_det_array.append(writable_option);
		share_det_array.append(recycle_repo_opt);
		share_det_array.append(guest_ok_option);
		share_det_array.append(validusers_option);
		share_det_array.append(audit_option);
		share_det_array.append(public_option);
		share_det_array.append(err_status);
		share_det_array.append(description);

		common_methods.write_file(shares_file, share_det_array);

		print """<script>location.href = 'main.py?page=share_det&act=%s&md=%s'</script>""" % (response, mdisks);

	else:
		# if SMB is not enabled then the share is retrieved from the shares_global_file.
		# the retrieved values are written to /tmp/details_of_share file.
		find_share_command = 'sudo grep "^' + share_name + ':" /var/www/global_files/shares_global_file';
		find_share         = commands.getoutput(find_share_command);

		temp = [];

		# split the fields using the delimiters
		temp = find_share.split(':');

		share   = temp[0];
		path    = temp[1];
		comment = temp[2];

		share_det_array = [];

		path = path.replace('/storage/', '');
		
		flag = '';

		sharename_string  = 'sharename=' + share;
		sharepath_string  = 'sharepath=' + path;
		sharecomm_string  = 'sharecomm=' + comment;

		share_det_array.append(sharename_string);
		share_det_array.append(sharepath_string);
		share_det_array.append(sharecomm_string);

		common_methods.write_file(shares_file, share_det_array);

		print """<script>location.href = 'main.py?page=share_det&from_page=find_share&act=%s&md=%s';</script>""" % (response, mdisks);

except Exception as e:
	disp_except.display_exception(e);
