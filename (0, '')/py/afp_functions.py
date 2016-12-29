#!/usr/bin/python

import sys, commands, os, common_methods, share_details, string, cgitb, cgi

selected_share = share_details.share
selected_share_path  = share_details.path

sys.path.append('/var/nasexe/python/')
from fs2global import *

afp_conf_file_path = afp_conf_file
filetowrite = afp_share_conf_dir+selected_share

#print afp_conf_file
#print afp_share_conf_dir

def configure(dict_value):
	all_dict_values = dict_value
	afp_read_only = all_dict_values['afp_read_only']
	permission_type = all_dict_values['permission_type']
	afp_advance = all_dict_values['afp_advance']
	afp_host_allow = all_dict_values['afp_host_allow']
	afp_host_deny = all_dict_values['afp_host_deny']
	afp_umask = all_dict_values['afp_umask']
	afp_file_perm = all_dict_values['afp_file_perm']
	afp_dir_perm = all_dict_values['afp_dir_perm']
	afp_grant_users = all_dict_values['afp_grant_users']
	afp_grant_groups = all_dict_values['afp_grant_groups']

	if(permission_type == 'guest'):
		uam_list = 'uams_guest.so'
	elif(permission_type == 'valid_user'):
		uam_list = 'uams_dhx2.so'

		if(afp_grant_users!=None):
			check_agu = isinstance(afp_grant_users, str)
			concat_users = ''
			if(check_agu==False):
				afp_grant_users = list(set(afp_grant_users))
				for val in afp_grant_users:
					if(val!=afp_grant_users[-1]):
						comma_not = ","
					else:
						comma_not = ""
					concat_users = concat_users+'"'+val+'"'+comma_not
			else:
				concat_users = '"'+afp_grant_users+'"'

		if(afp_grant_groups!=None):
			check_agg = isinstance(afp_grant_groups, str)
			concat_groups = ''
			if(check_agg==False):
				afp_grant_groups = list(set(afp_grant_groups))
				for val in afp_grant_groups:
					if(val!=afp_grant_groups[-1]):
						comma_not = ","
					else:
						comma_not = ""
					concat_groups = concat_groups+'"'+val+'"'+comma_not
			else:
				concat_groups = '"'+afp_grant_groups+'"'

		if((afp_grant_users!=None) and (afp_grant_groups!=None)):
			concat_users_groups = concat_users+","+concat_groups

		if((afp_grant_users!=None) and (afp_grant_groups==None)):
			concat_users_groups = concat_users

		if((afp_grant_users==None) and (afp_grant_groups!=None)):
			concat_users_groups = concat_groups

	entry_array = []


	entry_array.append("["+selected_share+"]")
	entry_array.append("path="+selected_share_path)

	if(afp_read_only == 'on'):
		entry_array.append("read only=yes")
	entry_array.append("uam list="+uam_list)
	if(permission_type == 'valid_user'):
		if((afp_grant_users!=None) or (afp_grant_groups!=None)):
			entry_array.append("valid users="+concat_users_groups)

	if((afp_file_perm!='') and (afp_file_perm!=None)):
		entry_array.append("file perm="+afp_file_perm)
	else:
		entry_array.append("file perm=0755")

	if((afp_dir_perm!='') and (afp_dir_perm!=None)):
		entry_array.append("directory perm="+afp_dir_perm)
	else:
		entry_array.append("directory perm=0755")
	if(afp_advance == 'on'):
		if(afp_host_allow!=None):
			find_comma = afp_host_allow.find(',')
			if(find_comma!=-1):
				split_ha = string.split(afp_host_allow, ",")
				split_ha = list(set(split_ha))
				concat_split_ha = ''
				for a in split_ha:
					if(a!=''):
						if(a!=split_ha[-1]):
							comma_not = ","
						else:
							comma_not = ""
						concat_split_ha = concat_split_ha+a+comma_not
						concat_split_ha_list = string.split(concat_split_ha, ",")
			else:
				concat_split_ha = afp_host_allow
				concat_split_ha_list = [concat_split_ha]

			#print concat_split_ha_list
			entry_array.append("hosts allow="+concat_split_ha)

		if(afp_host_deny!=None):
			find_comma = afp_host_deny.find(',')
			if(find_comma!=-1):
				split_hd = string.split(afp_host_deny, ",")
				split_hd = list(set(split_hd))
				concat_split_hd = ''
				for b in split_hd:
					if(b!=''):
						if(b!=split_hd[-1]):
							comma_not = ","
						else:
							comma_not = ""
						concat_split_hd = concat_split_hd+b+comma_not
						concat_split_hd_list = string.split(concat_split_hd, ",")
			else:
				concat_split_hd = afp_host_deny
				concat_split_hd_list = [concat_split_hd]
			#print "<br/>"
			#print concat_split_hd_list
			#print "<br/>"
			if(afp_host_allow!=None):
				reduced_list_hd = list(set(concat_split_hd_list) - set(concat_split_ha_list))
				#print reduced_list_hd
				#print "<br/>"
				concat_split_reduced = ''
				for c in reduced_list_hd:
					if(c!=''):
						if(c!=reduced_list_hd[-1]):
							comma_not = ","
						else:
							comma_not = ""
						concat_split_reduced = concat_split_reduced+c+comma_not

			else:
				concat_split_reduced = concat_split_hd

			#print concat_split_reduced
			if(concat_split_reduced!=''):
				entry_array.append("hosts deny="+concat_split_reduced)

		if((afp_host_allow!=None) or (afp_host_deny!=None) or (afp_umask!=None)):
			if(afp_umask!=None):
				entry_array.append("umask="+afp_umask)
			elif(afp_umask==None):
				entry_array.append("umask=0000")

	commands.getstatusoutput("sudo chmod 777 "+afp_conf_file_path)
	if "include = "+afp_share_conf_dir+selected_share+"\n" not in open(afp_conf_file_path).read():
		fo = open(afp_conf_file_path, 'a')
		fo.write("include = "+afp_share_conf_dir+selected_share+"\n")
		fo.close()
	commands.getstatusoutput("sudo chmod 644 "+afp_conf_file_path)

	common_methods.write_file(filetowrite, entry_array)


def unconfigure(sharename):
	remove_file = commands.getoutput('sudo rm '+afp_share_conf_dir+sharename)
	
	new_line = ''
	line_to_replace = ''
	filepath = afp_conf_file[:afp_conf_file.rfind('/') + 1]
	afpfile  = afp_conf_file[afp_conf_file.rfind('/') + 1:]

	fo = open(afp_conf_file, 'r')
	for line in fo:
		if (line.find(afp_share_conf_dir+sharename) >= 0):
			line_to_replace = line.strip()
		if(line_to_replace != ''):
			delete_entry = commands.getoutput('sudo /var/nasexe/delete_entry "%s" %s %s' % (line_to_replace, afpfile, filepath))
	fo.close()
	
	
def getstatus():
	check_file_existance = os.path.isfile(afp_share_conf_dir+selected_share)      ####### Checks if the file exists or not #######

	############### Default Values ###############
	guest_checked = '';
	afp_readonly_checked = '';
	afp_checked='';
	priv_checked='';
	afp_users_style='none';
	advanced_checked=''
	advanced_display_style='none'
	host_allow_val = ''
	host_deny_val = ''
	umask_val = ''
	file_perm_val = ''
	dir_perm_val = ''
	split_vul1 = ''
	afp_style = 'none'
	################### End ######################
	
	if(check_file_existance==True):
		if(os.path.getsize(afp_share_conf_dir+selected_share)>0):
			afp_checked='checked'
			afp_style='block'
	
			if 'read only' in open(afp_share_conf_dir+selected_share).read():
				afp_readonly_checked='checked'
	
			if 'uam list=uams_guest.so' in open(afp_share_conf_dir+selected_share).read():
				guest_checked='checked'
	
			if 'uam list=uams_dhx2.so' in open(afp_share_conf_dir+selected_share).read():
				priv_checked='checked'
				afp_users_style='block'
	
			if 'hosts allow' in open(afp_share_conf_dir+selected_share).read():
				advanced_checked='checked'
				advanced_display_style='block'
				host_allow_line = commands.getoutput('sudo grep "hosts allow" "'+afp_share_conf_dir+selected_share+'"')
				split_hal = string.split(host_allow_line,"=")
				host_allow_val = split_hal[1]
	
			if 'hosts deny' in open(afp_share_conf_dir+selected_share).read():
				advanced_checked='checked'
				advanced_display_style='block'
				host_deny_line = commands.getoutput('sudo grep "hosts deny" "'+afp_share_conf_dir+selected_share+'"')
				split_hdl = string.split(host_deny_line,"=")
				host_deny_val = split_hdl[1]
	
			if 'umask' in open(afp_share_conf_dir+selected_share).read():
				advanced_checked='checked'
				advanced_display_style='block'
				umask_line = commands.getoutput('sudo grep "umask" "'+afp_share_conf_dir+selected_share+'"')
				split_umask = string.split(umask_line,"=")
				umask_val = split_umask[1]
	
			if 'file perm' in open(afp_share_conf_dir+selected_share).read():
				file_perm_line = commands.getoutput('sudo grep "file perm" "'+afp_share_conf_dir+selected_share+'"')
				split_fpl = string.split(file_perm_line,"=")
				file_perm_val = split_fpl[1]
		
			if 'directory perm' in open(afp_share_conf_dir+selected_share).read():
				dir_perm_line = commands.getoutput('sudo grep "directory perm" "'+afp_share_conf_dir+selected_share+'"')
				split_dpl = string.split(dir_perm_line,"=")
				dir_perm_val = split_dpl[1]
		
			if 'valid users' in open(afp_share_conf_dir+selected_share).read():
				valid_users_line = commands.getoutput('sudo grep "valid users" "'+afp_share_conf_dir+selected_share+'"')
				valid_users_line = valid_users_line.replace('"', '')
				split_vul = string.split(valid_users_line,"=")
				split_vul1 = string.split(split_vul[1],",")
	
		else:
			guest_checked = 'checked'
	else:
		guest_checked = 'checked'
	

	display_styles = {'guest_checked':guest_checked, 'afp_readonly_checked':afp_readonly_checked, 'afp_checked':afp_checked, 'priv_checked':priv_checked, 'afp_users_style':afp_users_style, 'advanced_checked':advanced_checked, 'advanced_display_style':advanced_display_style, 'host_allow_val':host_allow_val, 'host_deny_val':host_deny_val, 'umask_val':umask_val, 'file_perm_val':file_perm_val, 'dir_perm_val':dir_perm_val, 'split_vul1':split_vul1, 'afp_style':afp_style} 

	return display_styles
