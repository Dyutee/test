#!/usr/bin/python
#_*_ coding: UTF-8 _*_

#enable debugging
import cgitb, header, os, sys, commands, common_methods, error_messages

cgitb.enable()

session_user = common_methods.get_session_user();

if (session_user != ''):
	pageval = common_methods.getpageval();

	if(pageval == 'first'):
                import welcome_p1
	if (pageval == 'chpwd'):
		import change_password		

	if (pageval == 'sys'):
		#import system_status
		import os_info

	if (pageval == 'date'):
		import date_set

	if (pageval == 'network'):
		import network_settings_new

	if (pageval == 'nas'):
		import nas_settings

	if (pageval == 'iscsi'):
		#import iscsi_new_page
		#import iscsi_new
		import new_iscsi
		#import iscsi_settings
		#import iscsi_status
	if (pageval == 'volume_disk'):
                import volume_disk
	if (pageval =='disk_iscsi'):
		import iscsi_disk_target

	if (pageval == 'target_iscsi'):
		#import iscsi_target
		import iframe_iscsi_target

	if (pageval == 'prop_iscsi'):
		import iscsi_properties

	if (pageval == 'ses_iscsi'):
		import iscsi_session

	if (pageval == 'det_iscsi'):
		import iscsi_list
	if (pageval == 'lst_iscsi'):
		import iscsi_configure_list
	
	if (pageval == 'stat_srp'):
		#import srp_status
		#import srp_new
		import new_srp

	if (pageval == 'tar_srp'):
		import srp_target
	
	if (pageval == 'disk_srp'):
		import srp_disk_target

	if (pageval == 'ini_srp'):
		import srp_initiator

	if (pageval == 'inf_srp'):
		import srp_list

	if (pageval == 'sess_srp'):
		import srp_session
	
	if (pageval == 'l_srp'):
		import srp_configure_list

	if (pageval == 'snmp'):
		import snmp

	if (pageval == 'smb'):
		import setup_smb

	if (pageval == 'auth'):
		import copy_authentication

	if (pageval == 'infini'):
		import new_infiniband

	if (pageval == 'status_fc'):
		import new_fc

	if (pageval == 'tar_fc'):
		import fc_target

	if (pageval == 'report'):
		import report_info

	if(pageval == 'cleardata'):
                import clear_data

	if (pageval == 'disk_fc'):
		import fc_disk_target

	if (pageval == 'fc_ini'):
		import fc_initiator

	if (pageval == 'inf_fc'):
		import fc_list

	if (pageval == 'sess_fc'):
		import fc_session
	#if (pageval== 'srp'):
	#	import srp_setting
	if (pageval == 'list_fc'):
		import fc_configure_list

	if (pageval == 'sd'):
		import shutdown

	if (pageval == 'logs'):
		import show_logs

	if (pageval =='fs2'):
		import backup

	if (pageval == 'cs'):
		import configure

	if (pageval == 'csl'):
		import configure_list

	if (pageval =='conn'):
		import connection

	if (pageval =='ss'):
		import snapshot_page

	if (pageval =='su'):
		import snapshot_schedule

	if (pageval == 'mu'):
		import user_maintenance

	if (pageval == 'updts'):
		import updates

	if (pageval == 'st'):
		import scheduled_tasks

	if (pageval == 'nd'):
		#import nas_disks_list 
		import nw_nas_disk_list

	if (pageval == 'all_disk_list'):
                #import nas_disks_list 
        	import all_disk_list


	if (pageval == 'bd'):
		#import iscsi_disks_list
		#import fio_disk_confi
		import create_container

	if (pageval == 'bckp'):
		import local_backup

	if (pageval == 'rs'):
		import raid_settings_new

	if (pageval == 'support'):
		import support_page

	if (pageval == 'crs'):
		import create_raid_set

	if (pageval == 'drs'):
		import delete_raidset

	if (pageval == 'ers'):
		import expand_raidset

	if (pageval == 'ors'):
		import offline_raidset

	if (pageval == 'ars'):
		import activate_raidset

	if (pageval == 'ch'):
		import create_hotspare

	if (pageval == 'dh'):
		import delete_hotspare

	if (pageval == 'cvs'):
		import create_volume_set

	if (pageval == 'dvs'):
		import delete_volumeset

	if (pageval == 'cpt'):
		import create_passthrough

	if (pageval =='log_info'):
                import log_info
	if (pageval == 'mail'):
		import mail_configuration
	
	if (pageval == 'dpt'):
		import delete_passthrough

	if (pageval == 'mpt'):
		import modify_passthrough

	if (pageval == 'id'):
		import identify_drive

	if (pageval == 'ri'):
		import raid_information

	if (pageval == 'hi'):
		import hdd_information

	if (pageval == 'share_det'):
		import share_details

	if (pageval == 'rr'):
		import draw_graph

	if (pageval == 'dg'):
		import disk_graph

	if (pageval == 'scan'):
		import scan_volume

	if (pageval == 're_mount'):
		import remount

	if (pageval == 'vtl'):
		import vtl_disk_list

	if (pageval == 'vtls'):
		import vtl_settings

	if (pageval == 'sr'):
		import start_services
	
	if (pageval == 'qo'):
		import user_quota
	
	if (pageval == 'fq'):
		import folder_quota

	if (pageval == 'sinfo'):
		import shares_info
	
	if (pageval == 'acl'):
		import set_acl_page
	
	if (pageval == 'afp'):
		import afp_settings
	
	if (pageval == 'es'):
		import edit_share
	
	if (pageval == 'append'):
		import append_mode
	
	if (pageval == 'smb_set'):
		import smb_settings
	
	if (pageval == 'nfs'):
		import nfs_settings_page
	
	if (pageval == 'ftp'):
		import ftp_settings
	
	if (pageval == 'sys_logs'):
		import system_logs
	
	if (pageval == 'change_pass'):
		import change_password_page
	
	if (pageval == 'san'):
		import san_disk_confi
	
	if (pageval == 'san_list'):
		import added_to_san
	
	if (pageval == 'sensor'):
		import sensor_info
	
	if (pageval == 'volume'):
		import volume_info
	
	if (pageval == 'info_disk'):
		import disk_info
	
	if(pageval == 'san_map'):
		import san_map

	
	if(pageval == 'fc_map'):
		import fc_map
else:
	common_methods.relogin();
