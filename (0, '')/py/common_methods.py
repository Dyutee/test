#!/usr/bin/python
import cgitb, commands, os, sys, datetime, subprocess
import code, signal, cgi, proc, threading

from tempfile import mkstemp
from shutil import move
from os import remove, close
from email.message import Message
from email.header import Header

sys.path.append('/var/nasexe/storage/');
from lvm_infos import *
from functions import *

sys.path.append('/var/nasexe/python/');
from fs2global import *;
from tools import *

import authentication
import ftp_auth, db_logs;
import anon_ftp;
import afp, acl;

sys.path.append('../modules/');
import disp_except;

import storage_op, manage_users, ads, fs2nis, smb;

cgitb.enable()
print 'Content-type: text/html';
print

global session_user;

now = datetime.datetime.now();
ads_domain = '';
ads_status = '';
nis_status = '';

#ads_domainline = commands.getstatusoutput('wbinfo --own-domain');

#if (ads_domainline[0] == 0):
#	ads_domain = str(ads_domainline[1]);

# declare ads server ip. change here if you want to change the ip of the ads server
ads_serverip = '192.168.0.249';
nis_serverip = '192.168.0.121';
remote_ip = os.environ["REMOTE_ADDR"]
server_ip = os.environ["SERVER_ADDR"];

file_missing = "<div align = 'center' style = 'margin-top: 10%; color: darkred; font: 14px Arial;'>Missing a file! Can't open this page.</div>";

auth_user = 'Full Access';
browser = os.environ.get("HTTP_USER_AGENT", "N/A").upper();
browser = 'xxx' + browser;

index_of_msie    = browser.find('MSIE');
index_of_mozilla = browser.find('MOZILLA');
index_of_firefox = browser.find('FIREFOX');
index_of_chrome  = browser.find('CHROMIUM');

#test_for_smb = commands.getoutput('sudo grep "true" /var/www/global_files/smb_global_options_file');
#test_for_smb = get_string_from_file('true', '/var/www/global_files/smb_global_options_file');
log_file     = '/var/log/weblog/weblog.log';

# initialize all the variables with corresponding messages
show_acl_error = "<div style = 'margin-top: 10%; margin-left: auto; margin-right: auto; text-align: center; border: 0px solid #736f6e; vertical-align: center; color: darkred; font: 16px Arial;'>Can\'t enable ACL for this share! Either \'Append mode\' or \'Log Path\' is enabled.</div>";

acl_message = "<div style = 'margin-top: 2%; margin-left: auto; margin-right: auto; text-align: center; border: 0px solid #736f6e; vertical-align: center; color: darkred; font: 16px Arial;'>You can work with ACL option only under local connection! Change the authentication in Advanced Setup -> Authentication.</div>";

acl_error = "<div style = 'margin-top: 2%; margin-left: auto; margin-right: auto; text-align: center; border: 0px solid #736f6e; vertical-align: center; color: darkred; font: 16px Arial;'>You can't work with ACL option since 'Append mode' is enabled for this path! Disable append mode from Basic Setup -> NAS Settings -> Configure Share -> Append Mode.</div>";

append_mode_error = "<div style = 'display: <?= append_mode_style ?>; margin-top: 2%; margin-left: auto; margin-right: auto; text-align: center; border: 0px solid #736f6e; vertical-align: center; color: darkred; font: 16px Arial;'>You can't work with Append mode when ADS is connected!</div>";

wait_for_response = "<div align = 'center' id = 'response' style = 'color: darkred; font-style: italic; margin-right: auto; margin-left: auto;'><div align = 'center' id = 'wait' style = 'display: none;'><img src = '../images/arrows32.gif'> Processing...</div></div>";

def getsystemperature():
	systemperature = commands.getstatusoutput('sensors|grep "Core 0"');

        if (systemperature[0] == 0):
                tempstring = systemperature[1];
                temperature = tempstring[tempstring.find('Core 0:') + len('Core 0:'):tempstring.find(' C')];

                if (temperature.find('+') >= 0):
                        temperature = temperature.replace('+', '');

                temperature = temperature.strip();

		return temperature;

	else:
		return false;

def importall():
	import cgitb, os, sys;

# methods to read the shares from the file and return the shares array
def get_shares_array():
	try:
		shares_file = '/var/www/global_files/shares_global_file';

		shares_array = [];
		shares_array = read_file(shares_file);

		return shares_array;

	except Exception as e:
		disp_except.display_exception(e);

def get_share_names():
	shares_array = [];
	names_array  = [];

	shares_array = get_shares_array();

	if (len(shares_array) > 0):
		for shares in shares_array:
			name = shares[:shares.find(':')];

			names_array.append(name);

	return names_array;

# method to set the image icon in every option
def getimageicon():
	try:
		image_icon = "<img name = 'id_help' src = '../images/img_help1.png' border = '0' onmouseover = 'return show_underline();'>";
		return image_icon;

	except Exception as e:
		disp_except.display_exception(e);

# get the connection status depending on the corresponding server status by calling the server status method.
def conn_status():
	try:
		connstatus = 'local';

		testconn = authentication.get_auth_type()
		#sync_users = authentication.sync_user_credentials()

		#if (sync_users['id'] != 0):
		#	sendtologs('INFO', 'Sync User Credentials', 'UI', '"common_methods.py, sync_users = authentication.sync_user_credentials(); " ' + str(sync_users));
	
		auth_type   = testconn['type'];
		auth_status = testconn['status'];

		if (auth_type == 'nis'):
			connstatus = 'nis is running';

		elif (auth_type == 'ads'):
			connstatus = 'Join is OK';
		
		return connstatus;

	except Exception as e:
		disp_except.display_exception(e);

# get the users to authenticate from the corresponding servers
def get_users_string():
	try:

		connstatus = conn_status();

		if (connstatus == 'local'):
			all_users_list  = manage_users.get_smb_users();

		elif (connstatus == 'Join is OK'):
			all_users_list = ads.get_users();

		elif (connstatus == 'nis is running'):
			all_users_list  = fs2nis.get_users();

		return all_users_list;

	except Exception as e:
		disp_except.display_exception(e);

# get the users to authenticate from the corresponding servers
def get_groups_string():
	try:
		all_groups_list = '';

		connstatus = conn_status();

		if (connstatus == 'local'):
			all_groups_list = manage_users.get_sys_groups();

		elif (connstatus == 'Join is OK'):
			all_groups_list = ads.get_groups();

		elif (connstatus == 'nis is running'):
			all_groups_list = fs2nis.get_groups();

		return all_groups_list;

	except Exception as e:
		disp_except.display_exception(e);

def removeblanklines(filename):
	try:
		commands.getoutput('sudo sed -i "/^$/d" ' + filename);

	except Exception as e:
		disp_except.display_exception(e);

# method to get a part of the string from the main string. takes 4 parameters. string, start text, end text, no. of characters
def substr(string, start, end, chars):
	try:
		indexofstart = 0;
		indexofend   = len(string);

		if (string != ''):
			if (start != ''):
				indexofstart = string.find(start) + len(start);

			if (end != ''):
				indexofend   = string.find(end);

		resultstring = string[indexofstart:indexofend];
		resultstring = resultstring.strip();

		return resultstring;

	except Exception as e:
		disp_except.display_exception(e);

# this method takes the size as input ex: 32GiB, 32MiB, 1TiB and converts it into GB, MB, TB respectively. Output will be 32GB, 32MB, 1TB.
def remove_gib(string):
	try:
		string = string.replace('TiB', 'TB');
		string = string.replace('GiB', 'GB');
		string = string.replace('MiB', 'MB');
		
		string = string.strip();
		
		return string;

	except Exception as e:
		disp_except.display_exception(e);

# this method takes vg1, vg2 as input and returns its size as output
def get_vgsize(vg):
	try:
		get_vg_size = commands.getoutput('sudo /var/nasexe/storage_operation vg-size ' + vg);
        	get_vg_size = remove_gib(get_vg_size);
	        get_vg_size = get_vg_size.strip();

		return get_vg_size;

	except Exception as e:
		disp_except.display_exception(e);
	
# this method takes no input parameters but returns the lv size
def get_lvsize():
	try:
		get_lv_size = commands.getoutput('sudo /var/nasexe/storage_operation lv-size');
        	get_lv_size = remove_gib(get_lv_size);
	        get_lv_size = get_lv_size.strip();

		return get_lv_size;

	except Exception as e:
		disp_except.display_exception(e);

# method to relogin
def relogin():
	print """<script>alert('Please login again!');</script>""";
	print """<script>location.href = '../py/login.py';</script>""";

# method for redirection
def redirect_url():
	print """<script>location.href = '../py/main.py';</script>""";

# change ownership. takes the file path as input and changes the ownership
def change_ownership(filetowrite):
	chown_command = commands.getoutput('sudo chown www-data:www-data ' + filetowrite);

# method to write the array contents to file. this contains two params, the file path and the array having the elements to write to file
def write_file(file_to_write, params_array):
	try:
		if (file_to_write != ''):
			chown_file = commands.getoutput('sudo chown www-data:www-data ' + file_to_write);

			file_handle = open(file_to_write, 'w');

			commands.getoutput('sudo chmod 777 ' + file_to_write);

			for i in params_array:
	        	        status = file_handle.write(i + "\n");

			commands.getoutput('sudo chmod 755 ' + file_to_write);
			file_handle.close()

	except Exception as e:
		disp_except.display_exception(e);

# extract a substring from a string
def getsubstr(string, substr, char):
	try:
		# reduce the string from the index of substr till the end of the string, so that we can exactly get what we want
		temp   = string[string.find(substr) + len(substr):len(string)];
		getchar = temp.find(char);
	
		# if the string doesn't contain '&', then extract the substring till the end of the string
		if (getchar < 0):
			getchar = len(temp);

		substring = temp[:getchar];

		return substring;

	except Exception as e:
		disp_except.display_exception(e);

# method to get page value. gets the page value from the querystringand returns the page value
def getpageval():
	try:
		querystring = os.environ["QUERY_STRING"]

		if (querystring == ''):
			querystring = 'page=sys&c=no';

		elemval = getsubstr(querystring, 'page=', '&');
		pageval = elemval.strip();

		return pageval;

	except Exception as e:
		disp_except.display_exception(e);

# method to append array contents to file. takes two inputs, the file path and the contents in an array. the array is rad line by
# line and the contents are written appended to file
def append_file(file_to_write, params_array):
	try:
		pathonly = file_to_write[:file_to_write.rfind('/')];

		if (file_to_write != '' and len(params_array) > 0):
			chown_command = commands.getoutput('sudo chown www-data:www-data "' + file_to_write + '"');
			commands.getoutput(chown_command);

			chown_command1 = commands.getoutput('sudo chmod 777 "' + file_to_write + '"');
			commands.getoutput(chown_command1);

			file_handle = open(file_to_write, 'a');

			if (len(params_array) == 1):
				for params in params_array:
					file_handle.write(params + "\n");

			elif (len(params_array) > 1):
				for params in params_array:
					file_handle.write(params + "\n");

			file_handle.write("\n");

	except Exception as e:
		disp_except.display_exception(e);

# method to read a file. takes the file path as the input and stores the content in an array. and returns the array as output
def read_file(filename):
	try:
		if (filename != ''):
			contents = [];
		
			commands.getoutput('sudo chown -R www-data:www-data "%s"' % filename);

			with open(filename, 'r') as f:
				for line in f:
					if (line != ""):
						contents.append(line);
			
			commands.getoutput('sudo chown -R root:root "%s"' % filename);

		else:
			return false;

		return contents;
		fclose(file_handle);

	except Exception as e:
		disp_except.display_exception(e);

# method to get the day of the week. this takes the week no. as the input and returns the day of the week as output
def find_day_of_week(dow):
	try:
		day = '*';

		if (dow != ''):
			if (dow == 0):
				day = 'Sun';

			if (dow == 1):
				day = 'Mon';

			if (dow == 2):
				day = 'Tue';

			if (dow == 3):
				day = 'Wed';

			if (dow == 4):
				day = 'Thu';

			if (dow == 5):
				day = 'Fri';

			if (dow == 6):
				day = 'Sat';

		return day;

	except Exception as e:
		disp_except.display_exception(e);

# method to get the month name. takes the month no. as input and return the month name
def find_month_name(mon):
	try:
		month = '*';

		if (mon == 1):
			month = 'Jan';

		if (mon == 2):
			month = 'Feb';

		if (mon == 3):
			month = 'Mar';

		if (mon == 4):
			month = 'Apr';

		if (mon == 5):
			month = 'May';

		if (mon == 6):
			month = 'Jun';

		if (mon == 7):
			month = 'Jul';

		if (mon == 8):
			month = 'Aug';

		if (mon == 9):
			month = 'Sep';

		if (mon == 10):
			month = 'Oct';

		if (mon == 11):
			month = 'Nov';

		if (mon == 12):
			month = 'Dec';

		return month;

	except Exception as e:
		disp_except.display_exception(e);

# method to display the string basing on disk type
def display_string(disk_type):
	try:
		if (disk_type == 'iSCSI'):
			article = 'an';

		else:
			article = 'a';
	
		display_string = "<div style = 'margin-top: 10%; margin-bottom: 20%; margin-right: auto; margin-left: auto; border: 0px solid #736f6e; font: 16px arial; color: darkred; text-align: center'>To create " + article + "  " + disk_type + " disk, create a volume group in Raid -> Raid Settings</div>";

		return display_string;

	except Exception as e:
		disp_except.display_exception(e);

# method to convert GB to TB. if GB exceeds 1024, then the unit is displayed as TB. input is size, the converted size is the output
def convert_unit(size):
	try:
		size = floatval(size);

		if (size / 1024 >= 1):
			size_to_float = size / 1024;
			size_to_float = round(size_to_float, 3);
			unit = 'TB';
	
		else:
			size_to_float = size;
			unit = 'GB';

		return_size = size_to_float.unit;

		return return_size;

	except Exception as e:
		disp_except.display_exception(e);

# this method takes target, disk, active_sessions_string as params and gives the active disks in string format as output
def get_target_status(target, disk, active_sessions_string):
	try:
		active_disks_string = '';

		if (target != ''):
			check_target = target + '->iqn';
			index_of_active_target = strpos(active_sessions_string, check_target);
	
		if (trim(index_of_active_target) != ''):
			active_disks_string = disk;

		return active_disks_string;

	except Exception as e:
		disp_except.display_exception(e);

# method to get eths from bond. takes device as input and gives the binded eths in string format as output
def get_eths_from_bond(device):
	try:
		get_eth_string = commands.getoutput('sudo /var/nasexe/list_binded_eth ' + device);
		get_eth_string = get_eth_string.strip();

		replace_string = 'Slave Interface: ';

		get_eth_string = get_eth_string.replace(replace_string, '');
		get_eth_string = get_eth_string + 'xxx';
		get_eth_string = get_eth_string.replace(':xxx', '');
		get_eth_string = get_eth_string.replace('xxx', '');
		get_eth_string = get_eth_string.strip();

		return get_eth_string;

	except Exception as e:
		disp_except.display_exception(e);

# takes a string as input and displays the alert with the string
def alert(string):
	print """<script>alert("%s");</script>""" % string;

# takes the page value as input and returns the title as output
def get_title(page):
	try:
		title = None;

		if (page == 'date'):
			title = 'Basic Setup > <span class = "hierarchyactive">Date/Time Settings</span>';
			
		if (page == 'sys'):
			title = 'Help > <span class = "hierarchyactive">System Status</span>';
			
		if (page == 'network'):
			title = 'Basic Setup > <span class = "hierarchyactive">Network Settings</span>';
			
		if (page == 'share'):
			title = 'Basic Setup > <span class = "hierarchyactive">NAS Settings</span>';
			
		if (page == 'add_share'):
			title = 'Basic Setup > NAS Settings > <span class = "hierarchyactive"> Create Share</span>';
			
		if (page == 'share_det'):
			title = 'Basic Setup > NAS Settings >  <span class = "hierarchyactive">Configure Share</span>';
			
		if (page == 'quota'):
			title = 'Basic Setup > NAS Settings > <span class = "hierarchyactive"> Quota</span>';
			
		if (page == 'share_inf'):
			title = 'Basic Setup > NAS Settings >  <span class = "hierarchyactive">Shares Info</span>';
			
		if (page == 'chpwd'):
			title = '<span class = "hierarchyactive">Change Password<span class = "hierarchyactive">';
			
		if (page == 'iscsi'):
			title = 'Basic Setup >  <span class = "hierarchyactive"> i-SCSI Settings</span>';
				
		if (page == 'snmp'):
			title = 'Basic Setup > <span class = "hierarchyactive"> SNMP Settings</span>';
			
		if (page == 'smb'):
			title = 'Basic Setup >  <span class = "hierarchyactive"> SMB Settings For ADS</span>';
			
		if (page == 'auth'):
			title = 'Advanced Setup > <span class = "hierarchyactive"> Authentication</span>';
			
		if (page == 'infini'):
			title = 'Advanced Setup >  <span class = "hierarchyactive"> Infiniband Settings</span>';
			
		if (page == 'fc'):
			title = 'Advanced Setup > <span class = "hierarchyactive"> FC Settings</span>';
			
		if (page == 'srp'):
			title = 'Advanced Setup > <span class = "hierarchyactive"> SRP Settings</span>';

		if (page == 'nd'):
			title = 'Volume Configuration > <span class = "hierarchyactive">NAS Disk Configuration</span>';
			
		if (page == 'bd'):
			title = 'Volume Configuration > <span class = "hierarchyactive">Block Disk Configuration</span>';
			
		if (page == 'bckp'):
			title = 'Backup/Restore > <span class = "hierarchyactive"> Backup </span>';
			
		if (page == 'rs'):
			title = 'RAID > <span class = "hierarchyactive"> RAID Settings</span>';
			
		if (page == 'st'):
			title = 'Maintenance > <span class = "hierarchyactive"> Scheduled Tasks </span>';
			   
		if (page == 'updts'):
			title = 'Maintenance > <span class = "hierarchyactive"> Updates </span>';
		
		if (page == 'mu'):
			title = 'Maintenance > <span class = "hierarchyactive"> Manage Users </span>';
			
		if (page == 'sd'):
			title = 'Maintenance > <span class = "hierarchyactive"> Shutdown </span>';
			
		if (page == 'logs'):
			title = 'Maintenance > <span class = "hierarchyactive"> Logs </span>';
			
		if (page == 'fs2'):
			title = 'Maintenance > <span class = "hierarchyactive"> FS2 Backup </span>';
			
		if (page == 'conn'):
			title = 'Maintenance > <span class = "hierarchyactive"> Connections </span>';
			
		if (page == 'ss'):
			title = 'Maintenance > <span class = "hierarchyactive"> Snapshot </span>';
			
		if (page == 'mu'):
			title = 'Maintenance > <span class = "hierarchyactive"> Manage Users </span>';
			
		if (page == 'updts'):
			title = 'Maintenance > <span class = "hierarchyactive"> Updates </span>';
			
		if (page == 'st'):
			title = 'Maintenance > <span class = "hierarchyactive"> Scheduled Tasks </span>';
			
		if (page == 'lb'):
			title = 'Backup > <span class = "hierarchyactive"> Local Backup </span>';
			
		if (page == 'crs'):
			title = 'RAID Settings > <span class = "hierarchyactive"> Create Raidset </span>';
			
		if (page == 'drs'):
			title = 'RAID Settings > <span class = "hierarchyactive"> Delete Raidset </span>';
			
		if (page == 'ers'):
			title = 'RAID Settings > <span class = "hierarchyactive"> Expand Raidset';
			
		if (page == 'ors'):
			title = 'RAID Settings > <span class = "hierarchyactive"> Offline Raidset';
			
		if (page == 'ars'):
			title = 'RAID Settings > <span class = "hierarchyactive"> Activate Raidset';
			
		if (page == 'ch'):
			title = 'RAID Settings > <span class = "hierarchyactive"> Create Hotspare';
			
		if (page == 'dh'):
			title = 'RAID Settings > <span class = "hierarchyactive"> Delete Hotspare';
			
		if (page == 'cvs'):
			title = 'RAID Settings > <span class = "hierarchyactive"> Create Volumeset';
			
		if (page == 'dvs'):
			title = 'RAID Settings > <span class = "hierarchyactive"> Delete Volumeset';
			
		if (page == 'cpt'):
			title = 'RAID Settings > <span class = "hierarchyactive"> Create Passthrough';
			
		if (page == 'dpt'):
			title = 'RAID Settings > <span class = "hierarchyactive"> Delete Passthrough';
			
		if (page == 'mpt'):
			title = 'RAID Settings > <span class = "hierarchyactive"> Modify Passthrough';
			
		if (page == 'id'):
			title = 'RAID Settings > <span class = "hierarchyactive"> Identify Drive';
			
		if (page == 'ri'):
			title = 'RAID Settings > <span class = "hierarchyactive"> Raidset Information';
			
		if (page == 'hi'):
			title = 'RAID Settings > <span class = "hierarchyactive"> Hard Drive Information';
			
		if (page == 'vc'):
			title = 'RAID Settings > <span class = "hierarchyactive"> Create Volumeset';
			
		if (page == 'pc'):
			title = 'RAID Settings > <span class = "hierarchyactive"> Create Passthrough';
			
		if (page == 'pm'):
			title = 'RAID Settings > <span class = "hierarchyactive"> Modify Passthrough';
			
		if (page == 'acl'):
			title = 'Basic Setup > NAS Settings > <span class = "hierarchyactive"> ACL Settings';

		if (page == 'nas'):
			title = 'Basic Setup > <span class = "hierarchyactive"> NAS Settings';	
			
		return title;

	except Exception as e:
		disp_except.display_exception(e);

# this method returns the active sessions in array format
def get_active_sessions(type):
	try:
		active_sessions_array = [];

		type = type.lower().strip();

		if (type == 'iscsi'):
			# get the active targets in session
			get_sessions_command = commands.getoutput('sudo /var/nasexe/iscsi_op sessions');
			get_sessions_array = get_sessions_command.split('#');

		if (type == 'srp'):
			# get the active targets in session
			get_sessions_command = commands.getoutput('sudo /var/nasexe/srp_op sessions');
			get_sessions_array = get_sessions_command.split('#');

		if (type == 'fc'):
			# get the active targets in session
			get_sessions_command = commands.getoutput('sudo /var/nasexe/fc_op sessions');
			get_sessions_array = get_sessions_command.split('#');

		# get all the sessions in an array and iterate through each element
		if (len(get_sessions_array) > 0):
			for get_sessions in get_sessions_array:
				get_sessions = get_sessions.strip();

				if (get_sessions != ''):
					get_sessions = get_sessions.strip();
					
					# split the element into active target and initiator(format: [target name]->[initiator])
					get_sessions_array1 = get_sessions.split('->');

					active_target = get_sessions_array1[0].strip();
					initiators    = get_sessions_array1[1].strip();
					
					# if initiator exist, then the session is active and is pushed into active_sessions_array
					if (initiators != ''):
						active_sessions_array.append(get_sessions);
		
		return active_sessions_array;

	except Exception as e:
		disp_except.display_exception(e);

# this method returns the iscsi status
def get_iscsi_status():
	try:
		check_iscsi = commands.getoutput('sudo echo `cat /sys/kernel/scst_tgt/targets/iscsi/enabled`');
		check_iscsi = check_iscsi.strip();

		iscsi_status = '';

		if (check_iscsi == '1'):
			iscsi_status = 'iSCSI-SCST target is running at pid';
	
		index_of_running = iscsi_status.find('target is running at pid');

		return index_of_running;

	except Exception as e:
		disp_except.display_exception(e);

# this method gives the target disks as output
def get_target_disks():
	try:
		show_targets_command = commands.getoutput('sudo /var/nasexe/iscsi_op list_targets');
		show_targets_array   = show_targets_command.split(' ');

		target_disk_array = [];

		if (len(show_targets_array) > 0):
			for show_target in show_targets_array:
				if (show_target != ''):
					find_disk_for_target_command = commands.getoutput('sudo /var/nasexe/iscsi_op used_disks ' + show_target);
					find_idisks_array = find_disk_for_target_command.split(' ');

					if (len(find_idisks_array) > 0):
						for target_disk1 in find_idisks_array:
							if (target_disk1 != ''):
								dummy_array = target_disk1.split(':');
								
								target_disk = dummy_array[0].strip();
								num         = dummy_array[1].strip();

								target_disk_array.append(target_disk);

		return target_disk_array;

	except Exception as e:
		disp_except.display_exception(e);

# this method gets the fc status
def get_fc_status():
	try:
		check_for_fc = commands.getoutput('sudo /etc/init.d/qla2x00t status');
		check_for_fc = check_for_fc.lower().strip();

		return check_for_fc;

	except Exception as e:
		disp_except.display_exception(e);
	
# returns the ib card status.
def check_for_ib_card():
	try:
		check_for_ib = commands.getoutput('sudo /var/nasexe/check_for_ib');
		check_for_ib_array = check_for_ib.split(' ');

		infini_param       = check_for_ib_array[0].strip();

		return infini_param;

	except Exception as e:
		disp_except.display_exception(e);

# method returns srp status
def get_srp_status():
	try:
		check_for_srp = commands.getoutput('sudo /var/nasexe/check_for_srp');
		check_for_srp_array   = check_for_srp.split(' ');

		srp_status = check_for_srp_array[0].strip();

		return srp_status;

	except Exception as e:
		disp_except.display_exception(e);

# method returns ib card with lspci
def check_for_ib_card_lspci():
	try:
		check_for_ib_card = commands.getoutput('sudo /var/nasexe/check_for_ib_card');
		check_for_ib_card = check_for_ib_card.strip();

		return check_for_ib_card;

	except Exception as e:
		disp_except.display_exception(e);

# returns the ipoib status
def check_for_ipoib():
	try:
		check_for_ipoib = commands.getoutput('sudo /var/nasexe/check_for_ipoib');
		check_for_ipoib_array = check_for_ipoib.split(' ');

		return check_for_ipoib_array[0].strip();

	except Exception as e:
		disp_except.display_exception(e);

# returns the ib_chassis status
def get_ib_chassis_status():
	try:
		check_for_ib_chassis = commands.getoutput('sudo /var/nasexe/check_ib_chassis');
		check_for_ib_chassis_array = check_for_ib_chassis.split(' ');

		return check_for_ib_chassis_array[0].strip();

	except Exception as e:
		disp_except.display_exception(e);

# returns the fc disks
def get_zone_disks():
	try:
		show_zone = commands.getoutput('sudo /var/nasexe/fc_op list_targets');
		show_zones_array = show_zone.split(' ');

		zone_disk_array = [];

		if (len(show_zones_array) > 0):
			for zone in show_zones_array:
				if (zone != ''):
					find_disk_for_zone = commands.getoutput('sudo /var/nasexe/fc_op used_disks ' + zone);
					find_fdisks_array = find_disk_for_zone.split(' ');

					if (len(find_fdisks_array) > 0):
						for zone_disks1 in find_fdisks_array:
							if (zone_disks1 != ''):
								dummy_array = zone_disks1.split(':');

								zone_disks = dummy_array[0].strip();
								num = dummy_array[1].strip();

								zone_disk_array.append(zone_disks);

		return zone_disk_array;

	except Exception as e:
		disp_except.display_exception(e);

# returns the srp disks
def get_group_disks():
	try:
		show_group = commands.getoutput('sudo /var/nasexe/srp_op list_targets');
		show_groups_array = show_group.split(' ');

		group_disk_array = [];

		if (len(show_groups_array) > 0):
			for group in show_groups_array:
				if (group != ''):
					find_disk_for_group = commands.getoutput('sudo /var/nasexe/srp_op used_disks ' + group);
					find_gdisks_array = find_disk_for_group.split(' ');

					if (len(find_gdisks_array) > 0):
						for group_disks1 in find_gdisks_array:
							if (group_disks1 != ''):
								dummy_array = group_disks1.split(':');

								group_disks = dummy_array[0].strip();
								num = dummy_array[1].strip();

								group_disk_array.append(group_disks);
							
		return group_disk_array;

	except Exception as e:
		disp_except.display_exception(e);

# returns the log size
def get_log_size():
	try:
		path = '';

		#check_log_path = commands.getoutput('sudo grep "SMBLOGPATH=" /var/nasconf/smb-log.conf');
		check_log_path = get_string_from_file('SMBLOGPATH=', '/var/nasconf/smb-log.conf');
		check_log_path = check_log_path.strip();

		if (check_log_path != ''):
			dummy_array = check_log_path.split('=');

			d1 = dummy_array[0].strip();
			path = dummy_array[1].strip();

		if (path != ''):
			# if log path is set, then the log size calculation excludes message folder and samba folder in /var/log/
			log_size = commands.getoutput('sudo /var/nasexe/check_log_size path');

		else:
			# if log path is not specified, then log size is calculated taking entire logs into consideration
			log_size = commands.getoutput('sudo /var/nasexe/check_log_size ""');
		

		# trim the log size
		log_size = log_size.strip();

		# extract the log size from the value retreived from log size script
		log_size = log_size[:log_size.find(' ')].strip();

		find_K = log_size.find('K');

		if (find_K > 0):
			log_size = 0;
		
		return log_size;

	except Exception as e:
		disp_except.display_exception(e);

# method reads the iscsi disks file using the read_file method and passes the contents to array
def get_iscsi_disks():
	try:
		iscsi_disks_array = [];

		iscsi_disks_file = '/var/nasconf/iSCSI-disks';
		iscsi_disks_array = read_file(iscsi_disks_file);

		return iscsi_disks_array;

	except Exception as e:
		disp_except.display_exception(e);

# method reads the nas disks file using the read_file method and passes the contents to array
def get_nas_disks():
	try:
		nas_disks_array = [];

		nas_info = get_lv_infos();

		if (nas_info["lvs"] != [{}]):
			for x in nas_info['lvs']:
				if (x['lv_name'].find('NAS-') == 0):
					nasdisks = x['lv_name'].replace('NAS-', '');
					nasdisks = nasdisks.strip();

					if (nasdisks != 'rrd_data'):
						nas_disks_array.append(nasdisks);

		return nas_disks_array;

	except Exception as e:
		disp_except.display_exception(e);

# method reads the ip and searchces in the session file
def get_session_user_old():
	try:
		session = [];
		session_user = '';
		remoteip = cgi.escape(os.environ["REMOTE_ADDR"]);

		searchstring = '^' + remoteip + ':';
		sessionuserstring = get_string_from_file(searchstring, '/tmp/.sessions/sessions.txt');

		if (sessionuserstring != 'not found'):
			session      = sessionuserstring.split(':');
			session_user = session[1].strip();

		return session_user;

	except Exception as e:
		disp_except.display_exception(e);

def get_session_user():
	try:
		remoteip = cgi.escape(os.environ["REMOTE_ADDR"]);
		import MySQLdb
		db = MySQLdb.connect("localhost","root","netweb","fs2" )
		cursor = db.cursor()
		get_sess_user_name = ''
		query = "select username from session where remote_ip = '"+remoteip+"'";
		status = cursor.execute(query)
		data = cursor.fetchone ()
		if(data !=None):
			#for row in data:
			get_sess_user_name =data[0]
			#print 'US:'+str(get_sess_user_name)
			db.commit()
			db.close()
		return get_sess_user_name
	except Exception as e:
		disp_except.display_exception(e);

def downloadfile(filename):
	try:
		print 'Content-type: application/zip';
		print "Content-Disposition: attachment; filename='%s'" % filename;
		print           

		fullpath = '/var/www/fs4/downloads/' + filename;

		#checkfile = commands.getstatusoutput('ls %s' % fullpath);
		checkfile = os.path.isfile(fullpath);
		extension = fullpath[fullpath.rfind('.') + 1:];

		if (checkfile == True): 
			fsize = os.path.getsize(fullpath);
					
			if (extension == 'pdf'):
				print 'pdf';
						
			else:
				Header("Content-type: application/octet-stream");
				Header("Content-Disposition: filename='%s'" % os.path.basename(fullpath));
						
			Header("Content-length: %s" % fsize);
			Header("Cache-control: private"); #use this to open files directly
					
			if (fsize > 0):         
				with open(fullpath, 'r') as f:
					for line in f:
						if (line != ''):
							print line;

	except Exception as e:
		disp_except.display_exception(e);

def get_appendmode(path):
	try:
		append_mode = '';
		testpath = path[:path.rfind('/') + 1];

	        append_mode = get_append_mode(testpath, path);
		append_mode = append_mode.strip();

		return append_mode;

	except Exception as e:
		disp_except.display_exception(e);

def replace(file_path, pattern, subst):
	try:
		# create temp file
		fh, abs_path = mkstemp();
	
		commands.getoutput('chmod 755 "%s"' % abs_path);

		new_file = open(abs_path, 'w');
		old_file = open(file_path);

		for line in old_file:
			new_file.write(line.replace(pattern, subst));
	
		# close temp file
		new_file.close();
		close(fh);
		old_file.close();

		# remove original file
		remove(file_path);
	
		# move new file
		move(abs_path, file_path);

	except Exception as e:
		disp_except.display_exception(e);

def get_share_path(sharename):
	try:
		sharestring = '';
		findshare   = get_string_from_file(sharename, '/var/www/global_files/shares_global_file');

		if (findshare != 'not found'):
			sharestring = str(findshare);
			sharepath   = sharestring[sharestring.find(':') + 1:sharestring.rfind(':')];
			sharepath   = sharepath.strip();

			return sharepath;

		else:
			return 1;

	except Exception as e:
		disp_except.display_exception(e);

def get_share_comment(sharename):
	try:
		sharestring = '';
		findshare   = get_string_from_file(sharename, '/var/www/global_files/shares_global_file');

		if (findshare != 'not found'):
			sharestring  = str(findshare);
			sharecomment = sharestring[sharestring.rfind(':') + 1:];
			sharecomment = sharecomment.strip();

			return sharecomment;

		else:
			return 1;

	except Exception as e:
		disp_except.display_exception(e);

def mount_ftp(sharename):
	try:
		mountcommand = '';
		mountstatus  = '';

		message = '';
		sharepath   = get_share_path(sharename);

		authpath = '';
		anonpath = '';

		checkauthpath = '';
		checkanonpath = '';

		pathtomount  = '';
		mountcommand = 'print';

		anonfiletocheck = ftp_share_conf_dir + sharename + '.anon';
		authfiletocheck = ftp_share_conf_dir + sharename + '.auth';

		checkanonfile = os.path.isfile(anonfiletocheck);
		checkauthfile = os.path.isfile(authfiletocheck);

 		if (checkanonfile == True):
			anonpath = ftp_anon_share_base_dir + 'pub/' + sharename;
			mountcommand = 'sudo mount -o bind "' + sharepath + '" "' + anonpath + '"';

		if (checkauthfile == True):
			authpath = ftp_auth_share_base_dir + sharename;
			mountcommand = 'sudo mount -o bind "' + sharepath + '" "' + authpath + '"';

			mountstatus = commands.getstatusoutput(mountcommand);

			if (mountstatus[0] == 0):
				message = 'SUCCESS';

			else:
				message = str(mountstatus[1]);

		return message;

	except Exception as e:
		disp_except.display_exception(e);
	
def mount_ftp_all():
	try:
		logfile  = '/var/log/nas.log';
		logarray = [];

		sharesarray  = [];
		statusstring = '';
		sharesarray  = read_file('/var/www/global_files/shares_global_file');

		if (len(sharesarray) > 0):
			for share in sharesarray:
				if (share.find(':') > 0):
					sharename = share[:share.find(':')];

					if (sharename != ''):
						sharename = sharename.strip();

						mountstatus = mount_ftp(sharename);

						if (mountstatus == 'SUCCESS'):
							statusstring += sharename + '-MOUNT:SUCCESS';

						else:
							statusstring += sharename + '-MOUNT:FAIL';

			logarray.append(statusstring);
			write_file(logfile, logarray);

			return statusstring;

	except Exception as e:
		disp_except.display_exception(e);

def unmount_ftp(sharename):
	try:
		mountcommand = '';
		umountstatus = '';

		message = '';
		sharepath   = get_share_path(sharename);

		authpath = '';
		anonpath = '';

		checkauthpath = '';
		checkanonpath = '';

		pathtomount  = '';
		mountcommand = 'print';

		anonfiletocheck = ftp_share_conf_dir + sharename + '.anon';
		authfiletocheck = ftp_share_conf_dir + sharename + '.auth';

		checkanonfile = os.path.isfile(anonfiletocheck);
		checkauthfile = os.path.isfile(authfiletocheck);

 		if (checkanonfile == True):
			anonpath = ftp_anon_share_base_dir + 'pub/' + sharename;
			mountcommand = 'sudo umount -o bind "' + sharepath + '" "' + anonpath + '"';

		if (checkauthfile == True):
			authpath = ftp_auth_share_base_dir + sharename;
			mountcommand = 'sudo umount -o bind "' + sharepath + '" "' + authpath + '"';

			umountstatus = commands.getstatusoutput(mountcommand);

			if (umountstatus[0] == 0):
				message = 'SUCCESS';

			else:
				message = str(umountstatus[1]);

		return message;

	except Exception as e:
		disp_except.display_exception(e);

def unmount_ftp_all():
	try:
		logfile  = '/var/log/nas.log';
		logarray = [];

		sharesarray  = [];
		statusstring = '';
		sharesarray  = read_file('/var/www/global_files/shares_global_file');

		if (len(sharesarray) > 0):
			for share in sharesarray:
				if (share.find(':') > 0):
					sharename = share[:share.find(':')];

					if (sharename != ''):
						sharename = sharename.strip();

						mountstatus = unmount_ftp(sharename);

						if (mountstatus == 'SUCCESS'):
							statusstring += sharename + '-MOUNT:SUCCESS';

						else:
							statusstring += sharename + '-MOUNT:FAIL';

			logarray.append(statusstring);
			write_file(logfile, logarray);

			return statusstring;

	except Exception as e:
		disp_except.display_exception(e);

"""
---------------------------------------------------
these functions are written to check for the status
of a service. it takes service name as input and
returns the status of the service.
--------------------------------------------------
"""
def check_service_status(service):
	try:
		message = 'NOT RUNNING';

		if (service == 'smb'):
			checkstatus = commands.getstatusoutput('/etc/init.d/samba status');

		if (service == 'ftp'):
			checkstatus = commands.getstatusoutput('/etc/init.d/proftpd status');

		return str(checkstatus);

	except Exception as e:
		disp_except.display_exception(e);

def restartfscron():
	commands.getoutput('pkill fs2-cron');
	commands.getoutput('fs2-cron &');

def getxgridvalue(fromrange, torange):
	xgridstring = '';
	datediff = torange - fromrange;

	datediff = str(datediff);
	numdays = 1;

	if (datediff.find('day') > 0):
		noofdays = datediff[:datediff.find(',')];
		noofdays = noofdays.strip();

		numdays = noofdays[:noofdays.find(' ')];
		numdays = numdays.strip();

		gapvalue = int(numdays) * 60;

	else:
		noofhours = datediff[:datediff.find(':')];
		
		if (int(noofhours) > 1):
			gapvalue = int(noofhours) * 2;

		else:
			gapvalue = 10;

	xgridstring = '--x-grid MINUTE:10:HOUR:1:MINUTE:' + str(gapvalue) + ':0:%R';
	return xgridstring;

def unconfigureallshares():
	sharesarray = [];

	sharesarray = get_shares_array();

	if (len(sharesarray) > 0):
		for shares in sharesarray:
			sharename = shares[:shares.find(':')];
			sharepath = shares[shares.find(':') + 1:shares.rfind(':')];

			sharename = sharename.strip();

			checksharesmbconf = smb.show(sharename);

			if (checksharesmbconf['id'] == 0):
				status = smb.unconfigure(sharename);

			checkshareftpconf = ftp_auth.get_status(sharename);

			if (checkshareftpconf['ftp_groups_list'] != '' or checkshareftpconf['ftp_users_list'] != '' or checkshareftpconf['ftpwrite_ip'] != '' or checkshareftpconf['ftpaccess_ip'] != ''):
				ftp_auth.unconfigure(sharename);
				anon_ftp.anonymous_unconfigure(sharename);
			
			getafpstatus = afp.getstatus(sharename, sharepath);

			if (getafpstatus['guest_checked'] == 'checked'):
				afp.unconfigure(sharename);

			checkshareacl = commands.getstatusoutput('sudo getfacl "%s"|grep "mask"' % sharepath);

			if (checkshareacl[0] == 0):
				acl.reset_acl(' -R', sharepath);
				commands.getoutput('rm -rf /tmp/getusers');

def get_lun_number(targetname, diskname):
	try:
		lun_number = -1;

		lunnumberlinestatus = commands.getstatusoutput('cat /etc/scst.conf|sed -n "/TARGET %s\ {/,/}/p"|grep "%s"' % (targetname, diskname));

		if (lunnumberlinestatus[0] == 0):
			lun_number = lunnumberlinestatus[1].strip();
			lun_number = lun_number[lun_number.find('LUN') + len('LUN'):lun_number.find(diskname)];
			lun_number = lun_number.strip();

		return lun_number;

	except Exception as e:
		disp_except.display_exception(e);
		
def replace_chars(text, chartype):
	spcharsfile = '/var/www/fs4/py/specialcharacters.txt';

	chars_array = [];
	chars_array = read_file(spcharsfile);

	for chars in chars_array:
		chars = chars.strip();

		symbol   = chars[:chars.find('->')];
		fullform = chars[chars.find('->') + 2:];

		if (text.find(symbol) >= 0 or text.find(fullform) >= 0):
			if (chartype == 'chartotext'):
				text = text.replace(symbol, fullform);

			if (chartype == 'texttochar'):
				text = text.replace(fullform, symbol);

	return text;

def convert_sec_to_min(val):
	val = int(val);

	resstring = '';
	string    = ' seconds';
	div       = 1;

	if (val >= 60):
		string = ' minute(s)';
		val = val / 60;

	resstring = str(val) + string;

	return resstring;

def get_all_domains():
	domainsarray = [];
	
	logarray   = [];
	log_string = '';

	#get_domains = commands.getstatusoutput('sudo ls %s' % auth_domains_file);
	get_domains = os.path.exists(auth_domains_file);

	if (get_domains == True):
		domainsarray = read_file(auth_domains_file);
		#print domainsarray

	else:
		log_string = str(now) + '<<>>From common_methods.py, function get_all_domains()<<>>' + str(get_domains);
	
	if (len(domainsarray) > 0):
		return domainsarray;

	else:
		error = 'Could not get domains array';
		return error;

def get_users_count():
        try:
		userscount = 0;

                connstatus = conn_status();

                checkusersfile  = commands.getstatusoutput('ls adsusersfile');

                if (checkusersfile[0] == 0):
                        all_users_array = open('adsusersfile', 'r');

                        with open('adsusersfile', 'r') as line:
                                userscount = len(line.readlines());

                return userscount;

        except Exception as e:
                disp_except.display_exception(e);

def get_groups_count():
        try:
		groupscount = 0;

                checkgroupsfile = commands.getstatusoutput('ls adsgroupsfile');

                if (checkgroupsfile[0] == 0):
                        all_groups_array = open('adsgroupsfile', 'r');

                        with open('adsgroupsfile', 'r') as line:
                                groupscount = len(line.readlines());

                return groupscount;

        except Exception as e:
                disp_except.display_exception(e);

def sendtologs(errtype, message, source, moreinfo):
	log_dict = {};
	string   = '';

	log_dict['type']      = errtype;
	log_dict['msg']       = message;
	log_dict['log_src']   = source;
	log_dict['more_info'] = moreinfo;

	status = db_logs.write_log(log_dict);

	if (status['id'] == 0):
		string = 'success';

	else:
		string = str(status['desc']);

	return string;

def cleanup_string(string):
	string = string.replace('#', '');
	string = string.replace('&', '');
	string = string.replace('@', '');
	string = string.replace('*', '');

	return string;

def add(num1, num2, op):
	res = 0;

	if (op == '+'):
		res = num1 + num2;

	elif (op == '-'):
		res = num1 - num2;

	elif (op == '*'):
		res = num1 * num2;

	elif (op == '/'):
		res = num1 / num2;

	return res;
