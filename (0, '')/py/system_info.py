#!/usr/bin/python

import sys, commands, os, string, cgitb, cgi, memory_information, opslag_info, hashlib

sys.path.append('/var/nasexe/storage')
import storage_op
from lvm_infos import *
from functions import *

sys.path.append('/var/nasexe/storage/');
import san_disk_funs;


sys.path.append('/var/nasexe/python')
import storage_op

from fs2global import *
def read_file(filename):
        if (filename != ''):
                contents = [];

                with open(filename, 'r') as f:
                        for line in f:
                                line = line.replace('\n\n', '\n');
                                contents.append(line);

def read_file2(filename):
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


def substr(string, start, end, chars):
                
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

def sensor_cpu_info():
	cpu1_temp_command = 'NA'
	cpu2_temp_command = 'NA'

	cpu1_temp_command = commands.getoutput("sudo ipmitool sdr|grep -i 'cpu1 temp'|awk -F '|' {\'print $3\'}|sed 's/ //g'")

	if (cpu1_temp_command != 'NA'):
		cpu1_temp_command = cpu1_temp_command.strip();

	
		
	cpu2_temp_command = commands.getoutput("sudo ipmitool sdr|grep -i 'cpu2 temp'|awk -F '|' {\'print $3\'}|sed 's/ //g'")
	
	if (cpu2_temp_command != 'NA'):
		cpu2_temp_command = cpu2_temp_command.strip();


	cpu_temp_command = 'CPU1: ' + cpu1_temp_command + '\n' + 'CPU2: ' + cpu2_temp_command
	return cpu_temp_command;

def sensor_temp_info():
	check_areca_card_command = commands.getoutput('sudo lspci|grep -i "areca"');

	if (check_areca_card_command != ''):
        	show_temperature_command = commands.getoutput('sudo /var/nasexe/sw_r_set temp');

        	outputarray = [];
        	outputarray = show_temperature_command.split('&');

        	raid_cpuline        = outputarray[0];
        	raid_controllerline = outputarray[1];

        	raid_cpu = raid_cpuline[raid_cpuline.find(':') + 1:] + 'C';
        	raid_controller = raid_controllerline[raid_controllerline.find(':') + 1:] + 'C';

		if (raid_cpu.find('(Celsius)') > 0):
			raid_cpu = raid_cpu.replace('(Celsius)', '');

			#print 'RAID1:'+str(raid_cpu)

		if (raid_controller.find('(Celsius)') > 0):
			raid_controller = raid_controller.replace('(Celsius)', '');

			#print 'RAID2:'+str(raid_controller)
			display_temperature = 'RAID CONTROLLER:' + raid_controller + '\n' + 'RAID CPU: ' + raid_cpu

			return display_temperature;

		else:
			raid_cpu = 'Areca card not detected!';
			raid_controller = 'Areca card not detected!';
	
	



def fan_info():
	fan_info = commands.getstatusoutput("sudo ipmitool sdr|egrep -i 'Fan[0-9]'")

#print temp
	fanarray = [];

	fanstring      = fan_info[1];
	fanarray       = fanstring.split('\n');
	fan_name_speed = '';

	for i in fanarray:
        	name  = i[:i.find('|')];
        	speed = i[i.find('|') + 1:i.rfind('|')];
        	speed = speed.replace("RPM", "")

        	name = name.strip();
        	speed = speed.strip();
		fan_name_speed += name + ':' + speed + ' | ';

	fan_name_speed = fan_name_speed[:fan_name_speed.rfind('|')].strip();
	return fan_name_speed;


def power_supply():
	power_supply_command = commands.getoutput("ipmitool sdr|grep 'Power Supply'|awk -F '|' '{print $3}'")


	return power_supply_command

def intrusion_status():
	intrusion_command = commands.getoutput("ipmitool sdr|grep Intrusion|awk -F '|' '{print $3}'")

	return intrusion_command
def cpu_info():

	cpu_model_command = commands.getoutput( 'sudo /var/nasexe/disp_cpu_model');
	cpu_model_command = cpu_model_command.replace(':', '').strip();

	memory_display = commands.getoutput('sudo /var/nasexe/packet_memory memory');
	memory_array = [];
	used_array   = [];
	memory_array = memory_display.split(' ');
	memory_param_array = memory_array[1].split(':');

	total_array = memory_param_array[0].split('-');
	used_array  = memory_param_array[1].split('-');
	free_array  = memory_param_array[2].split('-');

	total = total_array[0];
	used  = used_array[0];
	free  = free_array[0];

	server = commands.getoutput('sudo hostname')

	string = commands.getoutput('sudo uptime');
	uptime = substr(string, 'up', ',', '');
	uarray = [];
	upminute = uptime;
	uphour   = '';
	if (uptime.find(':') > 0):
        	uarray = uptime.split(':');
	        uphour   = uarray[0];
		upminute = uarray[1];

	upminute = upminute.replace(' min', '');

	hstring = '';
	mstring = '';

	if (uphour != ''):
        	hstring = 'hour, ';

	if (upminute != ''):
        	mstring = 'minute';

	if (uphour > 1 and uphour.strip() != ''):
        	hstring = 'hours, ';

	if (upminute > 1):
        	mstring = 'minutes';
	up_time_string = uphour + ' ' + hstring + upminute + ' ' + mstring;

	#print "CPU : "+cpu_model_command
	cpu_model = "\n\nCPU : "+cpu_model_command+"\n\nMemory (MB) : "+total+"\n\nHostname : "+server+"\n\nUptime : "+up_time_string

	return cpu_model

def ip_info():
	#remote_ip = os.environ["REMOTE_ADDR"]
	#server_ip = os.environ["SERVER_ADDR"]

	#ip_info = "SERVER : "+server_ip+"\n\nREMOTE : "+remote_ip
	
	sys.path.append('/var/nasexe/')
        import net_manage as net_manage_bond

	get_all_iface = net_manage_bond.get_all_ifaces_config()
	if(get_all_iface["id"]==0):
                iface_info = get_all_iface["all_conf"]
                #print iface_info

        elif(get_all_iface["id"]==2):
                iface_info = [{'status': '', 'iface': '', 'netmask': '', 'address': '', 'model': '', 'gateway': ''}]

	ip_info = '\n\nINTERFACE\t\tIP ADDRESS\t\tNETMASK\n----------------------------------------------------------------\n\n'
	for x in iface_info:
		ip_line = x["iface"]+"\t\t\t"+x["address"]+"\t\t"+x["netmask"]+"\n\n"
		ip_info = ip_info+ip_line
	
	return ip_info

def change_password(password):
	
	password =  password
		
	enpassword = password.encode("base64", "strict")

	filetowrite = '/root/usersfile'
	fh = open(filetowrite, 'w')
	pwdstring = 'Password='+enpassword
	fh.write(pwdstring)
	fh.close()

def change_web_password(password):
	password     = hashlib.md5(password).hexdigest()
	#fullpassword = 'Full Access:' + password;

	changestatus = commands.getstatusoutput('sed -i "s/Full Access\:.*/Full Access\:%s/" /var/www/global_files/users_file' % password);

def status_info():
        #remote_ip = os.environ["REMOTE_ADDR"]
        #server_ip = os.environ["SERVER_ADDR"]

        #ip_info = "SERVER : "+server_ip+"\n\nREMOTE : "+remote_ip

        sys.path.append('/var/nasexe/')
        import net_manage as net_manage_bond

        get_all_iface = net_manage_bond.get_all_ifaces_config()
        if(get_all_iface["id"]==0):
                iface_info = get_all_iface["all_conf"]
                #print iface_info

        elif(get_all_iface["id"]==2): 
                iface_info = [{'status': '', 'iface': '', 'netmask': '', 'address': '', 'model': '', 'gateway': ''}]
    
        status_info = ''
        for x in iface_info: 
		status_line = "\t\t"+x["iface"]+"\t\t\t"+x["address"]+"\t\t\t"+x["status"]+"\n\n"
                status_info = status_info+status_line
		
		#for y in x["slave_ifaces_status"]:
               	#	print x["slave_ifaces"][count]+"-"+y+"<br/>"
                 #       count =count + 1
        
        return status_info

def scan_volume():
	pvscan_command = commands.getstatusoutput('sudo pvscan > /dev/null')
	vgscan_command = commands.getstatusoutput('sudo vgscan --ignorelockingfailure > /dev/null')
	vgchange_command = commands.getstatusoutput('sudo vgchange -aly --ignorelockingfailure > /dev/null')
	lvscan_command = commands.getstatusoutput('sudo lvscan > /dev/null')

	message1 = ''
	message2 = ''
	message3 = ''
	message4 = ''
	return_val = ''

	if(pvscan_command[0] == 0):
		message1 = 'success'
	else:
		err_msg1 = 'Error in Pvscan! '
	if(vgscan_command[0]== 0):
		message2 = 'success'
	else:
		err_msg2 = 'Error in Vgscan! '
	if(vgchange_command[0]==0):
		message3 = 'success'
	else:
		err_msg3 ='Error in Vgchange! '
	if(lvscan_command[0]==0):
		message4 = 'success'
	else:
		err_msg4 = 'Error in Lvscan! '
	
	if(message1 and message2 and message3 and message4 == 'success'):
		return_val = "scanned successfull"

	else:

		if(message1!='success'):
			return_val += err_msg1

		if(message2!='success'):
			return_val += err_msg2

		if(message3!='success'):
			return_val += err_msg3

		if(message4!='success'):
			return_val += err_msg4

	return return_val
	
def remount():
	remount_command = commands.getstatusoutput('sudo /etc/init.d/storage')
	return remount_command[0]

def volume_info():
	sys.path.append('/var/nasexe/python')
	import storage
	vg_info = storage.get_pvs()
	print vg_info
	nas_info = storage.get_lvs()
	volume_info= ''
	#volume_info1 = ''
	if(vg_info["pvs"]!=[{}]):
		for x in vg_info["pvs"]:
			#print x
			new_free = x["free_size"]
                        free_size = new_free.replace("g", "GB")
			size = x["size"]
			size = size.replace("g", "GB")
			volume_line = "\t\t"+x["vg_name"]+"\t\t"+free_size+"\t\t"+size+"\n\n"
			volume_info = volume_info+volume_line
	
	return volume_info
	
def disk_info():
	sys.path.append('/var/nasexe/python')
	import storage
	vg_info = storage.get_pvs()
        print vg_info
        nas_info = storage.get_lvs()
	disk_info = ''
			
	if(nas_info["lvs"]!=[{}]):
		for y in nas_info["lvs"]:
			size = y["size"]
			size = size.replace("g", "GB")
			disk_line ="\t\t"+y["lv_name"]+"\t\t"+size+"\n\n"
			disk_info = disk_info+disk_line

	return disk_info

def usage_info():
#	cpu_info_command = 'coreall::80.96 core0::73.31 core1::60.60 core2::75.26 core3::61.68 core4::94.02 core5::92.28 core6::94.77 core7::94.38';
	status, cpu_info_command = commands.getstatusoutput('/var/nasexe/cpu_info')
	cpu_info_array   = cpu_info_command.split(' ')
	avg_used_percentarray = cpu_info_array[1].split(':')
	avg_used_percent = avg_used_percentarray[1].strip()
	indexofdot = avg_used_percent.find('.')
	if (indexofdot < 1):
        	avg_used_percent = '0' + avg_used_percent

	avg_used_percent = avg_used_percent + '%'

	memory_info = memory_information.mem_information()

	cpu_info = "\n\nCPU Usage : "+avg_used_percent+"\n\nUsed Memory (MB) : "+memory_info["used"]+"\n\nFree Memory : "+memory_info["free"]

	return cpu_info


def os_info():
	os_info = "\n\nOS : "+opslag_info.getos('oss')+"\n\nVersion : "+opslag_info.getos('version')+"\n\nBuild : "+opslag_info.getos('build')+"\n\nModel : "+opslag_info.getos('model')+"\n\nSerial : "+opslag_info.getos('serial')+"\n\nDispatch Date : "+opslag_info.getos('disp_date')
	
	return os_info


def dns_info():
	dns_file = open('/etc/resolv.conf', 'r')
        lines = dns_file.readlines()
        count_lines=0
        for line in lines:
                count_lines += 1

        if(count_lines==2):
                new_string=''
                for line in lines:
                        split_dns_lines = string.split(line)
                        new_string = new_string + split_dns_lines[1]+" "

                split_new_string = string.split(new_string)
                split_new_string1 = split_new_string[0]
                #print split_new_string1
                #exit;
                split_new_string2 = split_new_string[1]

        elif(count_lines==1):
                for line in lines:
                        split_dns_lines = string.split(line)

                split_new_string = split_dns_lines[1]
                split_new_string1 = split_new_string
                split_new_string2 = ''

        elif(count_lines==0):
                split_new_string1 = ''
                split_new_string2 = ''
        else:
                new_string=''
                for line in lines:
                        split_dns_lines = string.split(line)
                        new_string = new_string + split_dns_lines[1]+" "
	
		split_new_string = string.split(new_string)
                split_new_string1 = split_new_string[0]
                #print split_new_string1
                #exit;
                split_new_string2 = split_new_string[1]

        dns_file.close()

	dns_string = "\n\nPrimary DNS : "+split_new_string1+"\n\nSecondary DNS : "+split_new_string2

	return dns_string


def dns_settings(primary, secondary):
	new_primary_dns = primary
	new_secondary_dns = secondary
	dns_conf_file="/etc/resolv.conf"

	if((new_primary_dns==None) and (new_secondary_dns==None)):
		commands.getstatusoutput("sudo chmod 777 "+dns_conf_file)
		dns_file_submit = open(dns_conf_file, 'w')
		dns_file_submit.write('')
		dns_file_submit.close()
		commands.getstatusoutput("sudo chmod 755 "+dns_conf_file)

	elif((new_primary_dns!=None) and (new_secondary_dns==None)):
		primary_dns_string = "nameserver" + " " + new_primary_dns
		commands.getstatusoutput("sudo chmod 777 "+dns_conf_file)
		dns_file_submit = open(dns_conf_file, 'w')
		dns_file_submit.write(primary_dns_string+"\n")
		dns_file_submit.close()
		commands.getstatusoutput("sudo chmod 755 "+dns_conf_file)

	elif((new_primary_dns!=None) and (new_secondary_dns!=None)):
		primary_dns_string = "nameserver" + " " + new_primary_dns
		secondary_dns_string = "nameserver"+ " " + new_secondary_dns
		commands.getstatusoutput("sudo chmod 777 "+dns_conf_file)
		dns_file_submit = open(dns_conf_file, 'w')
		dns_file_submit.write(primary_dns_string+"\n")
		dns_file_submit.write(secondary_dns_string)
		dns_file_submit.close()
		commands.getstatusoutput("sudo chmod 755 "+dns_conf_file)
	

def getdomdetails():
        getdomfile = commands.getstatusoutput('cat /etc/fstab > /tmp/domdetails.txt');

        contents = [];
        dfarray  = [];
        domarray=[];

        if (getdomfile[0] == 0):
                contents = read_file('/tmp/domdetails.txt');

        for i in contents:
                temp = [];

                if (i.find('UUID') == 0):
                        i = i.replace('\t', ' ');
                        temp = i.split(' ');

                        if (temp[1].strip() == '/'):
                                diskline = temp[0];
                                diskid = diskline[diskline.find('=') + 1:].strip();

                                dfarray = commands.getoutput('df -h|grep "%s"|awk -F " " {\'print $2, $3\'}' % diskid).split();
                                #print dfarray

                                totalspace = dfarray[0];
                                print totalspace
                                usedspace  = dfarray[1];
                                print usedspace
				#domsize= totalspace+usedspace


        if (len(dfarray) > 0):
                return dfarray;
		#return domsize

        else:
                return 'fail';


def get_shares_array():
        shares_file = '/var/www/global_files/shares_global_file';

        shares_array = []
        shares_array = read_file2(shares_file)

        return shares_array

def get_shares_array2():
	sys.path.append('/var/nasexe/python/')
	import tools
	get_shares = tools.get_all_shares(debug=True)
	if(get_shares["id"] == 0):
        	get_all_shares = tools.get_share_date_size_info(get_shares['shares'])
	
	return get_all_shares["shares"]

def check_protocols(disk_name):
	get_all_shares = get_shares_array2()
	shares = ''
	share_path = ''
	status = ''

	for x in get_all_shares:
		find_disk_name = str(x["path"]).find(disk_name)
		if(find_disk_name!=-1):
			#split_gas = string.split(x, ":")
			shares += x["name"]+" "
			share_path += x["path"]+" "

	#print shares
	#print share_path

	if(shares!=''):
		split_shares = string.split(shares)
		split_share_path = string.split(share_path)

		SMB_status = check_SMB(split_shares)
		if(SMB_status != 'no'):
			status += SMB_status+" "
		
		for x in split_share_path:
			if (len(x) == x.rfind('/') + 1):
				share_path += x[:x.rfind('/')]+" "

		share_path = string.split(share_path)

		NFS_status = check_NFS(split_shares, share_path)
		if(NFS_status != 'no'):
			status += NFS_status+" "
		#status = SiMB_status+":"+NFS_status

		FTP_status = check_FTP(split_shares)
		if(FTP_status != "no"):
			status += FTP_status+" "

		AFP_status = check_AFP(split_shares)
		if(AFP_status != "no"):
			status += AFP_status+" "

		SMB_LOG_PATH_status = check_SMB_LOG_PATH(share_path)
		if(SMB_LOG_PATH_status != "no"):
			status += SMB_LOG_PATH_status+" "

		AUDIT_status = check_AUDIT(split_shares)
		if(AUDIT_status != "no"):
			status += AUDIT_status

		#print status

		split_status = string.split(status, " ")
		#print split_status
		
		value_to_return = split_status
		if(value_to_return != ['']):
			return value_to_return
		else:
			return "No Protocols"
	else:
		return "No Protocols"

def check_SMB(shares_list):
	status = ''
	for x in shares_list:
		sharesconffile = smb_share_conf_dir+x
		check_for_smb = commands.getstatusoutput('ls %s' % sharesconffile)
		if(check_for_smb[0] == 0):
			status += "yes"
		else:
			status += "no"
	find_yes = status.find("yes")
	if(find_yes != -1):
		return "SMB"
	else:
		return "no"


def check_NFS(shares_list, share_path):
	status = ''
	#share_path = "/storage/disk1/sunnyNFS"
	for x in share_path:
		check_for_nfs_command = 'sudo grep \"' + x + '\" /etc/exports';
		check_for_nfs = commands.getoutput(check_for_nfs_command);

		if (check_for_nfs != ''):
			status += "yes"
		else:
			status += "no"

	 
	find_yes = status.find("yes")
	if(find_yes != -1):
		return "NFS"
	else:
		return "no"

def check_FTP(shares_list):
	status = ''
	for x in shares_list:
		check_for_ftp_auth = os.path.isfile(ftp_share_conf_dir+x+".auth")
		check_for_ftp_anon = os.path.isfile(ftp_share_conf_dir+x+".anon")

		if ((check_for_ftp_auth == True) or (check_for_ftp_anon == True)):
			status += "yes"
		else:
			status += "no"

	
	find_yes = status.find("yes")
	if(find_yes != -1):
		return "FTP"
	else:
		return "no"


def check_AFP(shares_list):
	status = ''
	for x in shares_list:
		check_for_afp = os.path.isfile(afp_share_conf_dir+x)

		if (check_for_afp == True ):
			status += "yes"
		else:
			status += "no"

			
	find_yes = status.find("yes")
	if(find_yes != -1):
		return "AFP"
	else:
		return "no"


def check_SMB_LOG_PATH(share_path):
	status = ''
	check_log_path_command = 'sudo grep "SMBLOGPATH=" /var/nasconf/smb-log.conf';
	check_log = commands.getoutput(check_log_path_command);
	lpath = check_log[check_log.find('=') + 1:];
	for x in share_path:
		if (lpath == x):
			status += "yes"
		else:
			status += "no"

	find_yes = status.find("yes")
	if(find_yes != -1):
		return "SMB_LOG_PATH"
	else:
		return "no"

def check_AUDIT(shares_list):
	status = ''
	for x in shares_list:
		check_audit = commands.getstatusoutput('sudo grep "full_audit:success" /var/nasconf/smbconf/"'+x+'"')
		if(check_audit[0] == 0):
			status += "yes"
		else:
			status += "no"

	find_yes = status.find("yes")
	if(find_yes != -1):
		return "AUDIT"
	else:
		return "no"


def get_allprotocol_status():

        check_iscsi = commands.getoutput('sudo echo `cat /sys/kernel/scst_tgt/targets/iscsi/enabled`');
        check_iscsi = check_iscsi.strip();

        check_srp = san_disk_funs.ib_target_status();
        check_fc = san_disk_funs.fc_target_status();

        #iscsi_status = '';
        #srp_status = '';
        #fc_status = '';
        #test_all = ''
        #allprotocolstatus = ''

        if (check_iscsi == '1'):
                iscsi_status = 'iSCSI-SCST target is running at pid';
                iscsi_status = 'Running';
                iscsi_status = 'ISCSI:' +str(iscsi_status)

        else:
                iscsi_status = 'ISCSI:Not Running';
        #return iscsi_status


        if (check_srp > 0):
                srp_status = 'Running';
                srp_status = 'SRP:' +str(srp_status)
        else:
                srp_status = 'SRP:Not Running'

	if(check_fc > 0):
                fc_status = 'Running';
                fc_status = 'FC:' +str(fc_status)

        else:
                fc_status = 'FC:Not Running'

        allprotocolstatus = iscsi_status +'\n\n'+ srp_status+'\n\n'+fc_status

        return allprotocolstatus

