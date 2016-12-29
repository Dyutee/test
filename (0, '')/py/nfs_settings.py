#!/usr/bin/python
import cgi, common_methods, cgitb, sys, datetime, include_files
cgitb.enable();

sys.path.append('/var/nasexe/python/');
import nfs;
import tools

form = cgi.FieldStorage();

use_nfs = 'off';

# get all the values from the nfs form
sharename      = form.getvalue('hid_share');
sharepath      = form.getvalue('hid_path');
comment        = form.getvalue('hid_comment');
use_nfs        = form.getvalue('conf');

#-----------------------------ha--------------------------------#
par_share_det = tools.get_share(sharename,debug=False)
share_ha_nodename = par_share_det["share"]["node"]
#-----------------------------ha--------------------------------#


if (sharepath.find('/storage/') < 0):
	sharepath = '/storage/' + sharepath;

log_array = [];
log_file = common_methods.log_file;

# if 'enable nfs' option is checked, read the remaining elements from the form
if (use_nfs == 'configure' or use_nfs == 'reconf'):
	use_nfs = 'on';
	access_ip      = form.getvalue('access_ip');
	write_ip       = form.getvalue('write_ip');
	insecure       = form.getvalue('insecure');
	synchronous    = form.getvalue('synchronous');
	ins_locks      = form.getvalue('ins_locks');
	no_root        = form.getvalue('no_root');
	optionalparams = form.getvalue('granted_optional[]');

	optionalparamstring = '';

	if (str(type(optionalparams)) == "<type 'list'>"):
		for opts in optionalparams:
			optionalparamstring += opts + ',';

		optionalparamstring = optionalparamstring[:optionalparamstring.rfind(',')];

	else:
		optionalparamstring = optionalparams;

	if (insecure == None):
		insecure = 'off';

	if (synchronous == None):
		synchronous = 'off';

	if (ins_locks == None):
		ins_locks = 'off';

	if (access_ip == None):
		access_ip = '';

	if (write_ip == None):
		write_ip = '';

	if (no_root == 'no_root'):
		no_root = 'on';

	if (no_root == 'all_squash'):
		no_root = 'off';

	if (optionalparamstring == None):
		optionalparamstring = '';

	if (access_ip != None):
		access_ip = access_ip.replace(' ', '');

	if (write_ip != None):
		write_ip  = write_ip.replace(' ', '');

	if (optionalparamstring != None):
		optionalparamstring = optionalparamstring.strip();

	if (comment == None):
		comment = 'nfs share';

	# create an empty dictionary with all the required keys
	inputstring = {"read_ips":"","write_ips":"","share_name":"","share_path":"","share_desc":"","use_nfs":"","insecure":"","sync":"","insecure_locks":"","no_root_squash":"","additional_nfs_parameters":""};

	# assign the form inputs to each key
	inputstring["read_ips"]                  = access_ip;
	inputstring["write_ips"]                 = write_ip;
	inputstring["share_name"]                = sharename;
	inputstring["share_path"]                = sharepath;
	inputstring["share_desc"]                = comment;
	inputstring["use_nfs"]                   = use_nfs;
	inputstring["insecure"]                  = insecure;
	inputstring["sync"]                      = synchronous;
	inputstring["insecure_locks"]            = ins_locks;
	inputstring["no_root_squash"]            = no_root;
	inputstring["additional_nfs_parameters"] = optionalparamstring;

	# call the nfs.configure module with the dictionary 'inputstring' as the input
	status = nfs.configure(inputstring,share_ha_nodename);
	
	log_string = str(common_methods.now) + '||From: ' + common_methods.remote_ip + '<<>>' + str(inputstring) + '<<>>' + str(status);
	log_array.append(log_string);

	common_methods.append_file(log_file, log_array);

	# the output is also a dictionary, with 2 fields, the status id and the status message
	if (status['id'] == 0):
		print "<script>alert('Configured NFS for share [%s]!');</script>" % sharename;

	else:
		print "<script>alert('%s');</script>" % status['desc'];

# if 'enable nfs' option is unchecked
else:
	# call the nfs.unconfigure module with share path as the input
	status = nfs.unconfigure(sharepath,share_ha_nodename);

	if (status['id'] == 0):
		print "<script>alert('UnConfigured NFS for share [%s]!');</script>" % sharename;

	else:
		print "<script>alert('%s');</script>" % status['desc'];

# remove the '/storage/' from the full path
sharepath = sharepath.replace('/storage/', '');
#print "<script>location.href = 'nfs_settings_page.py?share_name=%s';</script>" % sharename;
print "<script>location.href = 'iframe_nfs_settings_page.py?share_name=%s';</script>" % sharename;
