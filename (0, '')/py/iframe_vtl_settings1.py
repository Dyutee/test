#!/usr/bin/python
import cgitb, sys, include_files, cgi
cgitb.enable()
form = cgi.FieldStorage()
sys.path.append('../modules/')
import disp_except;
try:
	import os, commands, common_methods, string, time
	#cgitb.enable()

	sys.path.append('/var/nasexe/storage')
	import storage_op
	import lvm_infos
	import san_disk_funs
	from lvm_infos import *

	sys.path.append('/var/nasexe/')
	import storage

	sys.path.append('/var/nasexe/python/')
	import mhvtl
	import tools

	check_ha = tools.check_ha()

	sys.path.append('/var/nasexe/')
	import net_manage_newkernel as net_manage_bond

	image_icon = common_methods.getimageicon()

	get_all_iface = net_manage_bond.get_all_ifaces_config()

	get_all_targets = san_disk_funs.iscsi_list_all_tgt()

	target_plus = "+"
	iscsi_plus = "+"
	g_library_name = ''
	display_iscsi_show_target = 'none'
	display_fc_show = 'none'
	display_src_show = 'none'
	display_iscsi_session_form = 'none'
	display_iscsi = 'none'
	display_iscsi_add = 'none'
	display_iscsi_del = 'none'
	display_iscsi_show = 'none'
	display_iscsi_session = 'none'

	display_fc = 'none'
	display_fc_add = 'none'
	display_fc_del = 'none'
	display_fc_show = 'none'
	display_src_show = 'none'

	display_src = 'none'
	display_src_add = 'none'
	display_src_del = 'none'
	display_src_show = 'none'

	auto_tape_size = ''
	readonly_tape_size = ''
	get_t_t = ''
	get_t_d = ''
	get_lib_id_new = ''
	tape_exist = True
	get_comp_factor = 'enabled'
	get_tape_drive = ''
	get_vendor = ''
	get_brand = ''
	get_vtl_vol = ''
	get_code = 256
	display_cr_con = 'block'
	display_rm_vtl = 'none'
	display_add_tape = 'none'
	display_add_to_target = 'none'

	if(form.getvalue("vtl_volume")):
		gcv = form.getvalue("create_vtl_exist")
		get_vtl_vol = form.getvalue("vtl_volume")
		cmd = commands.getstatusoutput("sudo mount | grep "+get_vtl_vol)
		get_code = cmd[0]
		if(get_code != 0):
			print """<script>alert("The Disk is not ready to use! Please select another Disk.");</script>"""

		tape_home_dir = '/storage/VTL/'+get_vtl_vol
		tape_exist = mhvtl.is_tape_exist(tape_home_dir)
		if((tape_exist == True) and (gcv == None)):
			print """<script>alert("Tapes already available. Use existing Tapes to create Library!");</script>"""

	if(form.getvalue("brand_name")):
		get_brand = form.getvalue("brand_name")

	if(form.getvalue("vendor_name")):
		get_vendor = form.getvalue("vendor_name")

	if(form.getvalue("tape_drive")):
		get_tape_drive = form.getvalue("tape_drive")

	if(form.getvalue("comp_factor")):
		get_comp_factor = form.getvalue("comp_factor")

	if(form.getvalue("create_vtl")):
		get_vtl_disk = form.getvalue("vtl_volume")
		get_brand_name = form.getvalue("brand_name")
		get_vendor_name = form.getvalue("vendor_name")
		get_tape_drive_name = form.getvalue("tape_drive")
		get_no_of_tape_drive = form.getvalue("no_of_tape")
		get_im_ex = form.getvalue("im_ex")
		get_backoff = form.getvalue("backoff")
		get_tape_size = form.getvalue("tape_size")
		get_no_of_slots = form.getvalue("no_of_slots")
		get_no_of_empty_slots = form.getvalue("no_of_empty_slots")
		get_comp_factor_name = form.getvalue("comp_factor")
		get_tape_comp_factor = form.getvalue("tape_comp_factor")
		get_comp_type = form.getvalue("comp_type")

		split_str = string.split(get_tape_drive_name,":")
		tape_drive_vendor_name = split_str[0]
		tape_drive_name = split_str[1]
		tape_dr_no = int(split_str[2])

		media_density = mhvtl.vtl_tlibs_drives[get_brand_name][int(tape_dr_no)-1]['media_density']
		tape_suffix = mhvtl.vtl_tlibs_drives[get_brand_name][int(tape_dr_no)-1]['tape_suffix']
		tape_prefix = mhvtl.vtl_vendor_tape_prefix[get_brand_name]
		total_tape_drives = get_no_of_tape_drive.strip()
		total_tape_drive_maps = get_im_ex.strip()
		tape_home_dir = '/storage/VTL/'+get_vtl_disk
		lib_backoff = get_backoff.strip()
		tape_size = get_tape_size.strip()
		full_slots = get_no_of_slots.strip()
		empty_slots = get_no_of_empty_slots.strip()

		if(get_comp_factor_name == 'enabled'):
			compression_factor_state = '1'
		else:
			compression_factor_state = '0'

		tape_compression_factor = get_tape_comp_factor.strip()
		compression_type = get_comp_type

		lib_defn = {}
		lib_defn['vendor_name'] = get_brand_name
		lib_defn['tape_lib_name'] = get_vendor_name
		lib_defn['tape_drive_vendor_name'] = tape_drive_vendor_name
		lib_defn['tape_drive_name'] = tape_drive_name
		lib_defn['media_density'] = media_density
		lib_defn['tape_prefix'] = tape_prefix
		lib_defn['tape_suffix'] = tape_suffix
		lib_defn['total_tape_drives'] = total_tape_drives
		lib_defn['total_tape_drive_maps'] = total_tape_drive_maps
		lib_defn['tape_home_dir'] = tape_home_dir
		lib_defn['lib_backoff'] = lib_backoff
		lib_defn['tape_size'] = tape_size
		lib_defn['total_full_slots'] = full_slots
		lib_defn['empty_slots'] = empty_slots
		lib_defn['compression_factor_state'] = compression_factor_state
		lib_defn['tape_compression_factor'] = tape_compression_factor
		lib_defn['compression_type'] = compression_type

		status = mhvtl.make_vtl_library(lib_defn)
		if(status['id'] == 0):
			print"""<div id = 'id_trace'>"""
			print status['desc']
			print "</div>"
		else:
			print"""<div id = 'id_trace_err' >"""
			print status['desc']
			print "</div>"

		get_comp_factor = 'enabled'
		get_tape_drive = ''
		get_vendor = ''
		get_brand = ''
		get_vtl_vol = ''
		get_code = 256
		display_cr_con = 'none'
		display_rm_vtl = 'block'
		display_add_tape = 'none'
		display_add_to_target = 'none'

	if(form.getvalue("create_vtl_exist")):
		get_vtl_disk = form.getvalue("vtl_volume")
		total_tape_drives = form.getvalue("no_of_tape").strip()
		total_tape_drive_maps = form.getvalue("im_ex").strip()
		empty_slots = form.getvalue("no_of_empty_slots").strip()

		tape_home_dir = '/storage/VTL/'+get_vtl_disk
		status = mhvtl.get_all_tapes(tape_home_dir)

		vtl_tapes=status['vtl_tapes']
		media_density=status['density'].strip()
		tape_suffix=mhvtl.vtl_tape_density_suffix[media_density].strip()
		tape_drive_vendor_name=status['tape_vendor_name'].strip()
		vendor_name=status['vendor_name'].strip()
		tape_library_name=status['vtl_lib_name'].strip()
		tape_drive_name=status['tape_drive_name'].strip()
		lib_backoff=status['lib_backoff'].strip()
		compression_factor_state=status['compression_factor_state'].strip()
		tape_compression_factor=status['tape_compression_factor'].strip()
		compression_type=status['compression_type'].strip()
		slot_maps=status['slot_maps']
		tape_prefix=mhvtl.vtl_vendor_tape_prefix[vendor_name]

		lib_defn={}
		lib_defn['vendor_name']=vendor_name
		lib_defn['tape_lib_name']=tape_library_name
		lib_defn['tape_drive_vendor_name']=tape_drive_vendor_name
		lib_defn['tape_drive_name']=tape_drive_name
		lib_defn['media_density']=media_density
		lib_defn['tape_prefix']=tape_prefix
		lib_defn['tape_suffix']=tape_suffix
		lib_defn['total_tape_drives']=total_tape_drives
		lib_defn['total_tape_drive_maps']=total_tape_drive_maps
		lib_defn['tape_home_dir']=tape_home_dir
		lib_defn['lib_backoff']=lib_backoff
		lib_defn['vtl_tapes']=vtl_tapes
		lib_defn['slot_maps']=slot_maps
		lib_defn['empty_slots']=empty_slots
		lib_defn['compression_factor_state']=compression_factor_state
		lib_defn['tape_compression_factor']=tape_compression_factor
		lib_defn['compression_type']=compression_type

		make_vtl = mhvtl.make_vtl_library_from_existing_tapes(lib_defn)
		if(make_vtl['id'] == 0):
			print"""<div id = 'id_trace'>"""
			print make_vtl['desc']
			print "</div>"
		else:
			print"""<div id = 'id_trace_err' >"""
			print make_vtl['desc']
			print "</div>"

		get_comp_factor = 'enabled'
		get_tape_drive = ''
		get_vendor = ''
		get_brand = ''
		get_vtl_vol = ''
		get_code = 256
		display_cr_con = 'none'
		display_rm_vtl = 'block'
		display_add_tape = 'none'
		display_add_to_target = 'none'

	if(form.getvalue("delete_library")):
		get_del_arr = form.getvalue("delete_option_san[]")
		get_yes_no = form.getvalue("yes_no")
		get_force = form.getvalue("force_yes_no")

		if(get_yes_no.strip()=='yes'):
			k_data = True
		else:
			k_data = False

		if(get_force == 'yes'):
			force = True
		else:
			force = False

		check = isinstance(get_del_arr,str)
		if(check == False):
			for x in get_del_arr:
				split_str = string.split(x,":")
				lib_defn = {}
				lib_defn['lib_id']=split_str[0]
				lib_defn['lib_home_dir']=split_str[1]
				lib_defn['keep_data']=k_data
				lib_defn['force']=force
				status = mhvtl.delete_vtl_lib(lib_defn)
		else:
			split_str = string.split(get_del_arr,":")
			lib_defn = {}
			lib_defn['lib_id']=split_str[0]
			lib_defn['lib_home_dir']=split_str[1]
			lib_defn['keep_data']=k_data
			lib_defn['force']=force
			status = mhvtl.delete_vtl_lib(lib_defn)

		if(status['id'] == 0):
			print"""<div id = 'id_trace'>"""
			print status['desc']
			print "</div>"
		else:
			print"""<div id = 'id_trace_err' >"""
			print status['desc']
			print "</div>"

		display_cr_con = 'none'
		display_rm_vtl = 'block'
		display_add_tape = 'none'
		display_add_to_target = 'none'

	if(form.getvalue("on_but")):
		get_on_val = form.getvalue("on_but")
		get_on_val = get_on_val.strip()
		make_offline = mhvtl.offline_vtl(get_on_val)
		if(make_offline['id'] == 0):
			print"""<div id = 'id_trace'>"""
			print make_offline['desc']
			print "</div>"
		else:
			print"""<div id = 'id_trace_err' >"""
			print make_offline['desc']
			print "</div>"

		display_cr_con = 'none'
		display_rm_vtl = 'block'
		display_add_tape = 'none'
		display_add_to_target = 'none'

	if(form.getvalue("off_but")):
		get_off_val = form.getvalue("off_but")
		get_off_val = get_off_val.strip()
		make_online = mhvtl.online_vtl(get_off_val)
		if(make_online['id'] == 0):
			print"""<div id = 'id_trace'>"""
			print make_online['desc']
			print "</div>"
		else:
			print"""<div id = 'id_trace_err' >"""
			print make_online['desc']
			print "</div>"

		display_cr_con = 'none'
		display_rm_vtl = 'block'
		display_add_tape = 'none'
		display_add_to_target = 'none'

	if(form.getvalue("add_tape_form")):
		get_lib_id_new = form.getvalue("add_tape_form")

		####### Check Free Slots #######
		status = mhvtl.get_vtl(get_lib_id_new)
		status = status['vtl_lib']
		lib_status = status['lib_status']

		if(lib_status == 'online'):
			lib_sg_dev = status['lib_sg_dev']
			slot_status = mhvtl.get_vtl_lib_status_os(get_lib_id_new,lib_sg_dev)
			slot_status = slot_status['vtl_status']
			slot_status = slot_status['free_slots']
		else:
			lib_sg_dev = ''
			slot_status = mhvtl.get_vtl_lib_status_conf(get_lib_id_new)
			slot_status = slot_status['slots_status']
			slot_status = 'OK'
		####### End #######
		if((slot_status == 'OK') or (slot_status != [])):
			check_cleaning_tape = mhvtl.is_cleaning_tape_exist(get_lib_id_new)
			if(check_cleaning_tape == True):
				print """<script>alert("Cleaning Tape exists!");</script>"""
				display_cr_con = 'none'
				display_rm_vtl = 'block'
				display_add_tape = 'none'
				display_add_to_target = 'none'
			else:
				display_cr_con = 'none'
				display_rm_vtl = 'none'
				display_add_tape = 'block'
				display_add_to_target = 'none'

		else:
			print """<script>alert("No Free Slots Available!");</script>"""
			print """<script>location.href="iframe_vtl_settings.py";</script>"""
			display_cr_con = 'none'
			display_rm_vtl = 'block'
			display_add_tape = 'none'
			display_add_to_target = 'none'

	if(form.getvalue("tape_type")):
		get_t_t = form.getvalue("tape_type")
		get_t_d = form.getvalue("tape_density")
		get_lib_id_new = form.getvalue("tape_lib_id")
		if(get_t_t == 'clean'):
			auto_tape_size = 1
			readonly_tape_size = 'readonly = "readonly"'
		else:
			auto_tape_size = ''
			readonly_tape_size = ''

		display_cr_con = 'none'
		display_rm_vtl = 'none'
		display_add_tape = 'block'
		display_add_to_target = 'none'

	if(form.getvalue("submit_add_tape")):
		get_tape_density = form.getvalue("tape_density")
		get_tape_type = form.getvalue("tape_type")
		get_tape_size = form.getvalue("tape_size")
		get_tape_lib_id = form.getvalue("tape_lib_id")

		status = mhvtl.get_vtl(get_tape_lib_id)
		status = status['vtl_lib']
		vtl_home_dir = status['lib_home_dir']
		lib_status = status['lib_status']

		if(lib_status == 'online'):
			lib_sg_dev = status['lib_sg_dev']
		else:
			lib_sg_dev = ''


		create_tape_cmd = mhvtl.create_tape(get_tape_lib_id,lib_sg_dev,lib_status,get_tape_density,get_tape_size,get_tape_type,vtl_home_dir)
		if(create_tape_cmd['id'] == 0):
			print"""<div id = 'id_trace'>"""
			print create_tape_cmd['desc']
			print "</div>"
		else:
			print"""<div id = 'id_trace_err' >"""
			print create_tape_cmd['desc']
			print "</div>"

		display_cr_con = 'none'
		display_rm_vtl = 'block'
		display_add_tape = 'none'
		display_add_to_target = 'none'

	if(form.getvalue("remove_tape_form")):
		get_ct_lib_id = form.getvalue("remove_tape_form")
		split_get_ct_lib_id = string.split(get_ct_lib_id,":")
		re_get_ct_lib_id = split_get_ct_lib_id[0]
		get_ct_lib_status = split_get_ct_lib_id[1]
		if(get_ct_lib_status == 'online'):
			print """<script>alert("For Removing Cleaning Tape Library has to be offline!");</script>"""
		else:
			rm_tape_cmd = mhvtl.remove_clean_tape(re_get_ct_lib_id)
			if(rm_tape_cmd['id'] == 0):
				print"""<div id = 'id_trace'>"""
				print rm_tape_cmd['desc']
				print "</div>"
			else:
				print"""<div id = 'id_trace_err' >"""
				print rm_tape_cmd['desc']
				print "</div>"

		display_cr_con = 'none'
		display_rm_vtl = 'block'
		display_add_tape = 'none'
		display_add_to_target = 'none'

	if(form.getvalue("select_add_target")):
		get_add_to_tar = form.getvalue("select_add_target")
		display_cr_con = 'none'
		display_rm_vtl = 'none'
		display_add_tape = 'none'
		display_add_to_target = 'block'

	if(form.getvalue("library_name")):
		g_library_name = form.getvalue("library_name")
		if(g_library_name != 'select-vtl-library'):
			split_g_l_n = string.split(g_library_name,":")
			g_library_name = split_g_l_n[0]

			g_target_name = san_disk_funs.vtl_iscsi_target(g_library_name)

		else:
			g_library_name = ''

		display_cr_con = 'none'
		display_rm_vtl = 'none'
		display_add_tape = 'none'
		display_add_to_target = 'block'
		display_iscsi_show_target = 'none'
		display_fc_show = 'none'
		display_src_show = 'none'
		display_iscsi_session_form = 'none'

		display_iscsi = 'block'
		display_iscsi_add = 'block'
		display_iscsi_del = 'none'
		display_iscsi_show = 'block'
		display_iscsi_session = 'block'

		display_fc = 'block'
		display_src = 'block'

		target_plus = "-"
		iscsi_plus = "-"

	if(form.getvalue("submit_add_target")):
		get_library_name = form.getvalue("library_name")
		get_target_name = form.getvalue("target_name")
		get_initiator_name = form.getvalue("initiator_name")
		get_portals_array = form.getvalue("portals_array[]")
		get_total_interfaces = form.getvalue("total_interfaces")

		split_gln = string.split(get_library_name,":")
		func_library_name = split_gln[0]
		get_lib_id = split_gln[1]
		get_vtl_details = mhvtl.get_vtl(str(get_lib_id))
		dict_details = get_vtl_details['vtl_lib']
		remove_l_brac = dict_details['lib_scsi_id'].replace("[","")
		remove_r_brac = remove_l_brac.replace("]","")
		library_value = remove_r_brac.split()

		drives_lib = []
		for e in dict_details['drives']:
			rm_l_brac = e['drive_scsi_id'].replace("[","")
			rm_r_brac = rm_l_brac.replace("]","")
			drives_lib.append(rm_r_brac)

		length_portals = len(get_portals_array)
		chk_str = isinstance(get_portals_array,str)
		if(chk_str == True):
			ips = get_portals_array
		if(chk_str == False):
			if(int(get_total_interfaces) == int(length_portals)):
				ips = "*"
			else:
				ips_pre = ''
				for x in get_portals_array:
					ips_pre = x+','+ips_pre
				ips = ips_pre
				ips = ips[:-1]

		if((get_initiator_name == "*") and (ips == "*")):
			ini_name = "*"
		else:
			ini_name = get_initiator_name+"#"+ips

		type_name = 'ISCSI'

		target_name = san_disk_funs.vtl_iscsi_target(func_library_name)

		add_to_target_func = san_disk_funs.vtl_add_to_target(library_value,drives_lib,func_library_name,get_lib_id,type_name,target_name,ini_name)
		if(add_to_target_func == True):
			print"""<div id = 'id_trace'>"""
			print """Successfully added to target!"""
			print "</div>"
		else:
			print"""<div id = 'id_trace_err' >"""
			print """Error adding to target!"""
			print """</div>"""

		display_cr_con = 'none'
		display_rm_vtl = 'none'
		display_add_tape = 'none'
		display_add_to_target = 'none'
		display_iscsi_show_target = 'block'
		display_fc_show = 'none'
		display_src_show = 'none'
		display_iscsi_session_form = 'none'

		display_iscsi = 'block'
		display_iscsi_add = 'block'
		display_iscsi_del = 'none'
		display_iscsi_show = 'block'
		display_iscsi_session = 'block'

		display_fc = 'block'
		display_src = 'block'
		target_plus = "-"
		iscsi_plus = "-"
		g_library_name = ''

	if(form.getvalue("delete_target")):
		get_hid_lib_id = form.getvalue("delete_target")
		get_lib_dict = mhvtl.get_vtl(get_hid_lib_id)

		get_lib_dict_vtl = get_lib_dict['vtl_lib']

		l_h_d = get_lib_dict_vtl['lib_home_dir']
		split_lhd = string.split(l_h_d,"/")
		if(len(split_lhd) > 4):
			post_lib_name = split_lhd[3]
		else:
			post_lib_name = ''

		dict_details2 = get_lib_dict['vtl_lib']
		remove_l_brac2 = dict_details2['lib_scsi_id'].replace("[","")
		remove_r_brac2 = remove_l_brac2.replace("]","")
		library_value2 = remove_r_brac2.split()

		drives_lib2 = []
		for e in dict_details2['drives']:
			rm_l_brac2 = e['drive_scsi_id'].replace("[","")
			rm_r_brac2 = rm_l_brac2.replace("]","")
			drives_lib2.append(rm_r_brac2)

		iscsi_tar_func = san_disk_funs.list_vtl_iscsi_target(str(get_lib_dict_vtl['lib_name'].replace(' ', '')+'VTL'+post_lib_name))
		tgt = iscsi_tar_func['target']

		LIBRARY = library_value2
		DRIVES = drives_lib2
		NAME = str(get_lib_dict_vtl['lib_name'].replace(' ', '')+'VTL'+post_lib_name)
		TYPE = 'ISCSI'
		tgt = str(tgt)
	
		#print LIBRARY
		#print "<br/>"
		#print DRIVES
		#print "<br/>"
		#print NAME
		#print "<br/>"
		#print TYPE
		#print "<br/>"
		#print tgt
		#print "<br/>"

		remove_vtl_target = san_disk_funs.vtl_del_from_target(LIBRARY,DRIVES,NAME,TYPE,tgt)
		if(remove_vtl_target == True):
			print"""<div id = 'id_trace'>"""
			print """Successfully removed from target!"""
			print "</div>"
		else:
			print"""<div id = 'id_trace_err' >"""
			print """Error removing from target!"""
			print """</div>"""

		display_cr_con = 'none'
		display_rm_vtl = 'none'
		display_add_tape = 'none'
		display_add_to_target = 'none'
		display_iscsi_show_target = 'block'
		display_fc_show = 'none'
		display_src_show = 'none'
		display_iscsi_session_form = 'none'

		display_iscsi = 'block'
		display_iscsi_add = 'block'
		display_iscsi_del = 'none'
		display_iscsi_show = 'block'
		display_iscsi_session = 'block'

		display_fc = 'block'
		display_src = 'block'
		target_plus = "-"
		iscsi_plus = "-"

	get_vtl = storage.get_lvs(type1='VTL')
	get_all_vtls = mhvtl.get_all_vtls()


	sys.path.append("/var/nasexe/python/")
        import tools
        from tools import db
        sys_node_name = tools.get_ha_nodename()
        if(sys_node_name == "node1"):
                other_node = "node2"
                show_tn = "Node1"
                show_on = "Node2"
        else:
                other_node = "node1"
                show_tn = "Node2"
                show_on = "Node1"

        query="select * from network_ifaces where (name='eth1' and node='"+other_node+"')"
        status=db.sql_execute(query)
        for x in status["output"]:
                other_node_ip = x["ip"]

	#print 'Content-Type: text/html'
	print
	print """
		<script language = 'javascript' src = '../js/jquery1.8.js'></script>
		<link rel="stylesheet" href="../fancyBox/source/jquery.fancybox.css" type="text/css" media="screen" />
		<script type="text/javascript" src="../fancyBox/source/jquery.fancybox.pack.js"></script>
		<script type="text/javascript">
		$(document).ready(function() {
		$(".various").fancybox({
			maxWidth        : 800,
			maxHeight       : 600,
			fitToView       : false,
			width           : '60%',
			height          : '68%',
			autoSize        : false,
			closeClick      : false,
			openEffect      : 'none',
			closeEffect     : 'none',
			'afterClose':function () {
			 // window.location.reload();
			 },
			helpers   : { 
			overlay  :       {closeClick: false} // prevents closing when clicking OUTSIDE fancybox 
				     }
			
	       });

		});
		</script>

		<div id="loader-div" style="text-align:center; display:none;" ><img style="margin-top:20%;" src="../images/ajax-loader.gif" /><br/> Loading...</div>
	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer" id="body-div">
		<!--tab srt-->
		<div class="searchresult-container">
		<div style="margin:0 0 0px 0;" class="topinputwrap-heading"><a class="demo" href ="#"><img src ="../images/help_icon1.png" style="width:13px;"><span class="tooltip" >
                 <table border="0">
        <tr>
        <td style="font-size: medium;text-align:start;">Vtl Settings:</td>
        </tr>
        <tr>
        <td class="text_css">In this Page discussed the Vtl Settings.In the First tab select the vtl Disk to create vtl Library.In the Second tab show the Vtl created Vtl libraries Information.In the Third tab add the Vtl Traget library with a IScsi,Fc and Srp.</td>
</tr>
        </table>
	</div>
	</div>
		  <div class="infoheader">
		    <div id="tabs">
		      <ul>
			<li><a href="#tabs-1">Create VTL Library</a></li>
			<li><a href="#tabs-2">Show VTL Libraries</a></li>
			<li><a href="#tabs-3">Add Target</a></li>
			<li style="display:none;"><a href="#tabs-5">Add Tape</a></li>
		      </ul>
		      <div id="tabs-1">

		<!--form container starts here-->
		<form name = 'create_container' method = 'POST' action = 'iframe_vtl_settings.py#tabs-1'>
		<div class="form-container">
		  <div class="topinputwrap-heading"> Create VTL Library </div>
		<div class="form-container">
		<table width="100%" style="padding:0 0 0 10px; border:none;">
		<tr>
		<td>Select VTL Disk</td>
		<td>
	<div class="styled-select2">
	<select name='vtl_volume' onchange="this.form.submit();">
	<option value=''>Select VTL Disk</option>"""
	if(get_vtl['lvs'] != [{}]):
		for x in get_vtl['lvs']:
			vtl_disk_size = x['size']
			vtl_disk_size = vtl_disk_size.replace("g"," ")
			vtl_disk_size = vtl_disk_size.strip()
			vtl_disk_size_new = float(vtl_disk_size)*1024

			lib_path = '/storage/VTL/'+x['lv_name']
			print """<option value = '"""+x['lv_name']+"""'"""
			if(get_vtl_vol != ''):
				if(get_vtl_vol == x['lv_name']):
					print """selected = 'selected'"""

			for k in get_all_vtls['vtl_libs']:
				lib_home_dir = k['lib_home_dir'].strip()
				lib_home_dir = lib_home_dir[:lib_home_dir.rfind('/')]
				if(lib_home_dir == lib_path.strip()):
					print """disabled"""
			print """>"""+x['lv_name']+" ["+str(vtl_disk_size_new)+""" MB]</option>"""

	print """</select></div>"""
	if(tape_exist == False):
		if(get_code == 0):
			print """<tr>
			<td>
			Select Vendor
			</td>
			<td>"""
			if(get_vtl_vol != ''):
				for x in get_vtl['lvs']:
					if(x['lv_name'] == get_vtl_vol):
						v_d_size = x['size']
						v_d_size = v_d_size.replace("g"," ")
						v_d_size = v_d_size.strip()
						v_d_size_new = float(v_d_size)*1024
						print """<input type='hidden' name='hid_vtl_size' id='hid_vtl_size' value='"""+str(v_d_size_new)+"""' />"""

			print """<div class="styled-select2">
			<select name = 'brand_name' onchange="this.form.submit();">
			<option value = ''>Select Vendor</option>"""
			for vendor in mhvtl.vtl_library_vendors:
				print """<option value = '"""+vendor+"""'"""
				if(get_brand != ''):
					if(get_brand == vendor):
						print """selected = selected"""

				print""">"""+vendor+"""</option>"""

			print """</select>
			</div>
			</td>    
			</tr>

			<tr>
			<td>
			Select Library
			</td>
			<td>"""
			if(get_brand != ''):
				print """<div class="styled-select2">
				<select name = 'vendor_name' onchange="this.form.submit();">
				<option value = ''>Select Library</option>"""
				for tape_library in mhvtl.vtl_vendors_tlibs[get_brand]:
					print """<option value = '"""+tape_library+"""'"""
					if(get_vendor != ''):
						if(get_vendor == tape_library):
							print """selected = selected"""

					print """>"""+tape_library+"""</option>"""

				print """</select></div>"""
			else:
				print """<input type='text' class='textbox' value='Select a Vendor to enable this option' disabled=disabled size='30' />"""

			print """</td>    
			</tr>

			<tr>
			<td>
			Select Tape Drive
			</td>
			<td>"""
			if((get_vendor != '') and (get_brand != '')):
				print """<div class="styled-select2">
				<select name = 'tape_drive'  onchange="this.form.submit();">
				<option value = ''>Select Tape Drive</option>"""
				i=1
				for tape_drives in mhvtl.vtl_tlibs_drives[get_brand]:
					print """<option value = '"""+tape_drives['vendor_name']+':'+tape_drives['tape_model']+':'+str(i)+"""'"""
					if(get_tape_drive != ''):
						if(get_tape_drive == tape_drives['vendor_name']+':'+tape_drives['tape_model']+':'+str(i)):
							print """selected = selected"""

					print """>"""+tape_drives['vendor_name']+' '+tape_drives['tape_model']+"""</option>"""
					i+=1

				print """</select></div>"""
			else:
				print """<input type='text' class='textbox' value='Select a Library to enable this option' disabled=disabled size='30' />"""

			print """</td>    
			</tr>"""
			if((get_tape_drive != '') and (get_vendor != '') and (get_brand != '')):
				print """<tr>
				<td>
				Select No. of Tape Drive
				</td>
				<td>"""
				if((get_tape_drive != '') and (get_vendor != '') and (get_brand != '')):
					print """<div class="styled-select2">
					<select name = 'no_of_tape'>"""
					z=1
					while (z<=16):
						print """<option value = '"""
						print z
						print """'>"""
						print z
						print """</option>"""
						z = z+1

					print """</select></div>"""
				else:
					print """<input type='text' value='Select a Tape Drive to enable this option' disabled=disabled size='30' />"""

				print """</td>    
				</tr>

				<tr>
				<td>
				Select Import/Export Slots
				</td>
				<td>"""
				if((get_tape_drive != '') and (get_vendor != '') and (get_brand != '')):
					print """<div class="styled-select2">
					<select name = 'im_ex'>"""
					z=1
					while (z<=4):
						print """<option value = '"""
						print z
						print """'>"""
						print z
						print """</option>"""
						z = z+1

					print """</select></div>"""
				else:
					print """<input type='text' value='Select a Tape Drive to enable this option' disabled=disabled size='30' />"""

				print """</td>    
				</tr>

				<tr>
				<td>
				Select Library Backoff Value
				</td>
				<td>"""
				if((get_tape_drive != '') and (get_vendor != '') and (get_brand != '')):
					print """<div class="styled-select2"><select name = 'backoff'>
					<option value = '400'>400</option>
					</select>"""
				else:
					print """<input type='text' value='Select a Tape Drive to enable this option' disabled=disabled size='30' />"""

				print """</td>    
				</tr>

				<tr>
				<td>
				Enter Tape Size (MB)
				</td>
				<td>"""
				if((get_tape_drive != '') and (get_vendor != '') and (get_brand != '')):
					print """<input class = 'textbox' type = '' name = 'tape_size' id = 'tape_size'>"""
				else:
					print """<input type='text' class='textbox' value='Select a Tape Drive to enable this option' disabled=disabled size='30' />"""

				print """</td>    
				</tr>

				<tr>
				<td>
				Select No of Slots full with Tape in Library
				</td>
				<td>"""
				if((get_tape_drive != '') and (get_vendor != '') and (get_brand != '')):
					print """<div class="styled-select2">
					<select name = 'no_of_slots'>"""
					z=1
					while (z<=99):
						print """<option value = '"""
						print z
						print """'>"""
						print z
						print """</option>"""
						z = z+1

					print """</select></div>"""
				else:
					print """<input type='text' class='textbox' value='Select a Tape Drive to enable this option' disabled=disabled size='30' />"""

				print """</td>    
				</tr>

				<tr>
				<td>
				Select No of empty Slots in Library
				</td>
				<td width = "311" class = "table_content" height = "40px" valign = "middle" bgcolor = "#f5f5f5">"""
				if((get_tape_drive != '') and (get_vendor != '') and (get_brand != '')):
					print """<div class="styled-select2">
					<select name = 'no_of_empty_slots'>"""
					z=1
					while (z<=4):
						print """<option value = '"""
						print z
						print """'>"""
						print z
						print """</option>"""
						z = z+1

					print """</select></div>"""
				else:
					print """<input type='text' class='textbox' value='Select a Tape Drive to enable this option' disabled=disabled size='30' />"""

				print """</td>    
				</tr>

				<tr>
				<td>
				Choose Compression Factor
				</td>
				<td>"""
				if((get_tape_drive != '') and (get_vendor != '') and (get_brand != '')):
					print """<div class="styled-select2">
					<select name = 'comp_factor'  onchange="this.form.submit();">
					<option value = 'enabled'"""
					if(get_comp_factor != ''):
						if(get_comp_factor == 'enabled'):
							print """selected = selected"""
					print """>Enabled</option>
					<option value = 'disabled'"""
					if(get_comp_factor != ''):
						if(get_comp_factor == 'disabled'):
							print """selected = selected"""
					print """>Disabled</option>
					</select></div>"""
				else:
					print """<input type='text' class='textbox'  value='Select a Tape Drive to enable this option' disabled=disabled size='30' />"""

				print """</td>    
				</tr>

				<tr>
				<td>
				Select Tape Compression Factor
				</td>
				<td>"""
				if((get_tape_drive != '') and (get_vendor != '') and (get_brand != '')):
					print """<div class="styled-select2">
					<select name = 'tape_comp_factor'>"""
					if(get_comp_factor != 'disabled'):
						z=1
						while (z<=9):
							print """<option value = '"""
							print z
							print """'>"""
							print z
							print """</option>"""
							z = z+1
					else:
						print """<option value = '0'>0</option>"""

					print """</select></div>"""
				else:
					print """<input type='text' class='textbox' value='Select a Tape Drive to enable this option' disabled=disabled size='30' />"""

				print """</td>    
				</tr>

				<tr>
				<td>
				Choose Compression Type
				</td>
				<td>"""
				if((get_tape_drive != '') and (get_vendor != '') and (get_brand != '')):
					print """<div class="styled-select2">
					<select name = 'comp_type'>
					<option value = 'zlib'>zlib</option>
					</select></div>"""
				else:
					print """<input type='text' value='Select a Tape Drive to enable this option' disabled=disabled size='30' />"""

				print """</td>    



				<tr>
				<td align = 'right' colspan = '2'>



				<button class="buttonClass" type="submit" name = 'create_vtl' value ='create_vtl'  onclick = 'return create_vtl_disk();' style="margin:10px 120px 20px 0;">Create</button>
				</td>
				</tr>"""
	elif((get_code == 0) and (tape_exist == True)):
		print """<tr>
		<td>
		<b>select no. of tape drive</b>
		</td>
		<td>"""
		print """<select name = 'no_of_tape'>"""
		z=1
		while (z<=16):
			print """<option value = '"""
			print z
			print """'>"""
			print z
			print """</option>"""
			z = z+1

		print """</select>"""

		print """</td>    
		</tr>

		<tr>
		<td>
		Select Import/Export Slots
		</td>
		<td>"""
		print """<select name = 'im_ex'>"""
		z=1
		while (z<=4):
			print """<option value = '"""
			print z
			print """'>"""
			print z
			print """</option>"""
			z = z+1

		print """</select>"""

		print """</td>    
		</tr>

		<tr>
		<td>
		Select No of empty Slots in Library
		</td>
		<td>"""
		print """<select name = 'no_of_empty_slots'>"""
		z=1
		while (z<=4):
			print """<option value = '"""
			print z
			print """'>"""
			print z
			print """</option>"""
			z = z+1

		print """</select>"""

		print """</td>    
		</tr>"""





	print """	</td>
		</tr>
		</table>

		</div>
		</div>
		</form>
		<!--form container ends here-->
		<p>&nbsp;</p>
		      </div>
		      <div id="tabs-2">
		<!--form container starts here-->
		<form name = 'san_det_list' method = 'POST' action = ''>
		<div class="form-container">
		 <div class="topinputwrap-heading"> Show VTL Libraries </div>
		 <div class="inputwrap">"""
	if len(get_all_vtls['vtl_libs']) != 0:
		print """<table width="100%" >
		<tr>
		<th style="border:#BDBDBD 1px solid; padding:5px;"><input type = 'checkbox' id = 'id_select_all_san' name = 'select_all' onclick = 'return select_san_disks_all();'></th>
		<th style="border:#BDBDBD 1px solid;">Library ID</th>
		<th style="border:#BDBDBD 1px solid;">Library Name</th>
		<th style="border:#BDBDBD 1px solid;">Library Status</th>
		<th style="border:#BDBDBD 1px solid;">Library Drive(s)</th>
		<th style="border:#BDBDBD 1px solid;">Add/Remove Tape</th>
		<th style="border:#BDBDBD 1px solid;">Exported to</th>
		</tr>"""

		if get_all_vtls['id']== 0:
			if len(get_all_vtls['vtl_libs']) != 0:
				for lib in get_all_vtls['vtl_libs']:
					if lib.has_key('lib_sg_dev'):
						lib_sg_dev = lib['lib_sg_dev']
					else:
						lib_sg_dev = ''

					if(lib['lib_status'] == 'online'):
						checkbox_disabled = 'disabled'
					else:
						checkbox_disabled = ''

					l_h_d = lib['lib_home_dir']
					split_lhd = string.split(l_h_d,"/")
					if(len(split_lhd) > 4):
						post_lib_name = split_lhd[3]
					else:
						post_lib_name = ''

					print """<tr> 
					<td style="border:#BDBDBD 1px solid;" align='center'><input id = 'id_disk_array_san' """+checkbox_disabled+""" type = 'checkbox' name = 'delete_option_san[]' value = '"""+str(lib['lib_id'])+':'+lib['lib_home_dir']+"""' ></td>
					<td style="border:#BDBDBD 1px solid;" align='center'>"""+str(lib['lib_id'])+"""</td>
					<td style="border:#BDBDBD 1px solid;" align='center'><a style="color:#610B0B; text-decoration:none; font-weight:bold;" class="various" data-fancybox-type="iframe" style="color:#292915;text-decoration:none;" href="library_info.py?st="""+lib['lib_status']+"""&lib_id="""+str(lib['lib_id'])+"""&lib_sg_dev="""+lib_sg_dev+"""" >"""+lib['lib_name'].replace(' ', '')+'VTL'+post_lib_name+"""</a></td>
					<td style="border:#BDBDBD 1px solid;" align='center'>"""
					if(lib['lib_status'] == 'online'):
						print """ <button type='submit' name='on_but' value='"""+str(lib['lib_id'])+"""' style='background-color:#FFF; border:none; cursor:pointer;' onclick='return make_offline();' title='Click to make Offline.'><img src = '../images/active.png' alt='online' /></botton>"""
					else:
						print """ <button type='submit' name='off_but' value='"""+str(lib['lib_id'])+"""' style='background-color:#FFF; border:none; cursor:pointer;' onclick='return make_online();' title='Click to make Online.'><img src = '../images/inactive.png' alt='offline' /></button>"""

					print """</td>
					<td style="border:#BDBDBD 1px solid;" align='center'>"""

					i=1
					for drive in lib['drives']:
						print str(i)+'. '+drive['drive_name']+'<br/>'
						i=i+1

					print """</td>
					<td style="border:#BDBDBD 1px solid;" align='center'>
		<button class='add_tape_but' type = 'submit'  name = 'add_tape_form' value ='"""+str(lib['lib_id'])+"""' title="Add Tape" style="background-color:#FFF; border:none; cursor:pointer;" onclick="return form_action('add_tape_to_library');"><img src='../images/add_tape_library.png' /></button>

		<!--<a href='main.py?page=vtls&add_tape_form="""+str(lib['lib_id'])+"""#tabs-5'><img src='../images/add_tape_library.png' /></a>-->

		"""
					check_cleaning_tape_exist = mhvtl.is_cleaning_tape_exist(lib['lib_id'])
					if(check_cleaning_tape_exist == True):
						print """

						<button class='add_tape_but' type = 'submit'  name = 'remove_tape_form' value ='"""+lib['lib_id']+':'+lib['lib_status']+"""' title="Remove Cleaning Tape" style="bacground-color:#FFF; border:none; cursor:pointer;" onclick="return form_action('remove_cleaning_tape');"><img src='../images/remove_tape.png' /></button>
		"""

					print """
					</td>
					<td style="border:#BDBDBD 1px solid;" align='center'></td>
					</tr>"""

		print """	



		</table>


			<div style='float:right;' id='second_butt'>

			<button class='buttonClass' type = 'button' title ="Delete" onclick = 'return vtl_disk_delete("no");' style='margin:10px;width:125px;' >Delete Library</button>
			
			</div>

		<div id = 'keep' style = 'display:none; height:60px;' class="border" align='left'>Do you want to keep the tapes? <input type='radio' name='yes_no' value='yes' >YES <input type='radio' name='yes_no' value='no' checked>NO <br/>

		Do you want to force delete? <input type='radio' name='force_yes_no' value='yes' checked >YES <input type='radio' name='force_yes_no' value='no' >NO 
		<button class='buttonClass' type = 'button' name = 'cancel_library' value = 'cancel_library' title ="Cancel" onclick = 'return cancel_disk_delete();' style = ' float:right; margin:0 70px 0 0; background-color:#ffffff; border:none; font-size: 100%;' title="signin">Cancel</button>

		<button class='buttonClass' type = 'submit' name = 'delete_library' value = 'delete_library' title ="Delete" onclick = 'return vtl_disk_delete("yes");' style = 'float:right; margin:0 10px 0 0; background-color:#ffffff; border:none; font-size: 100%;' title="signin">Delete</button>

		</div>
		</form>"""

	else:
		print """<div style="text-align:center; padding:5px;">No Information found!</div>"""

	print """
			</div>
			</div>
		<p>&nbsp;</p>
		      </div>
		      <div id="tabs-3">
			<div id="subtabs">

			  <ul>

			    <li><a href="#subtabs-1">ISCSI</a></li>

			    <li><a href="#subtabs-2">FC</a></li>

			    <li><a href="#subtabs-3">SRP</a></li>

			  </ul>

			  <div id="subtabs-1">

			<div id="subsubtabs">

			  <ul>

			    <li><a href="#subsubtabs-1">Add to Target</a></li>

			    <li><a href="#subsubtabs-2">Show Details</a></li>

			    <li><a href="#subsubtabs-3">Session Details</a></li>

			  </ul>

			  <div id="subsubtabs-1">
	<form name = 'add_target_form' method = 'POST' action = 'iframe_vtl_settings.py#tabs-3'>
	<table width="100%">
	<tr>
	<td>Select VTL Library</td>
	<td>
	<div class="styled-select2">
	<select name='library_name' id='id_library_name' onchange="this.form.submit();">
	<option value='select-vtl-library'>Select VTL Library</option>"""
	if get_all_vtls['id']== 0:
		if len(get_all_vtls['vtl_libs']) != 0:
			for lib in get_all_vtls['vtl_libs']:
				l_h_d = lib['lib_home_dir']
				split_lhd = string.split(l_h_d,"/")
				if(len(split_lhd) > 4):
					post_lib_name = split_lhd[3]
				else:
					post_lib_name = ''

				chk_already_added = san_disk_funs.list_vtl_iscsi_target(str(lib['lib_name'].replace(' ', '')+'VTL'+post_lib_name))

				if(lib['lib_status'] == 'offline'):
					disabled_q = 'disabled'
				else:
					disabled_q = ''

				if(chk_already_added != {}):
					disabled_q = 'disabled'

				print """<option """+disabled_q+""" value='"""+lib['lib_name'].replace(' ','')+'VTL'+post_lib_name+':'+lib['lib_id']+"""'"""
				if(g_library_name != ''):
					if(g_library_name == lib['lib_name'].replace(' ','')+'VTL'+post_lib_name):
						print """selected = 'selected'"""
				print """>"""+lib['lib_name'].replace(' ','')+'VTL'+post_lib_name+"""</option>"""

	print """</select></div>
	</td>
	</tr>

	<tr>
	<td>Target Name</td>
	<td>"""
	if(g_library_name != ''):
        	print """<input class = 'textbox' type = 'text' name = 'target_name' id = 'target_name' value = '"""+g_target_name+"""' readonly />"""
	else:
        	print """<input class = 'textbox' type = 'text' name = 'target_name' id = 'target_name' disabled value = 'Select VTL Library' />"""

	print """</td>    
	</tr>


	<tr>
	<td>Enter Initiator Name</td>
	<td>
	<input class = 'textbox' type = 'text' name = 'initiator_name' id = 'id_initiator_name' >
	</td>    
	</tr>

	<tr>
	<td width = "200" class = "table_heading" height = "40px" valign = "top" bgcolor = "#f5f5f5">
	Check the Portal(s) to Add
	</td>

	<td>

	<table width="90%" style="border:#D1D1D1 1px solid;">
	<tr style = 'background-color: #D1D1D1; font-weight: bold;'>
	<td class = "table_heading" height = "30px" align = "middle">
	<input type = 'checkbox' id = 'id_select_all_portals' name = 'select_all_portals' onclick='return select_all_portals_to_add();' />
	</td> 
	<td class = "table_heading" height = "30px" align = "middle" >
	Device
	</td>
	<td class = "table_heading" height = "30px" align = "middle" >
	IP
	</td>
	</tr>"""
	if(get_all_iface['id'] == 0):
        	i=1
        	for x in get_all_iface['all_conf']:
                	print """<tr>
			<td align="middle"><input id = 'id_portals_array' type = 'checkbox' name = 'portals_array[]' value = '"""+x['address']+"""'></td>
			<td align="middle">"""+x['iface']+"""</td>
			<td align="middle">"""+x['address']+"""</td>
			</tr>"""
			i=i+1

	print """
	</table>    
	</td>
	</tr>

	<tr>
	<td align = 'right' colspan = '2'>
	<br/>
	<br/><input type='hidden' name='total_interfaces' value='"""+str(i-1)+"""' />
	<button class="buttonClass" type="submit" name = 'submit_add_target'  id = 'submit_add_target' value = 'submit_add_target'  onclick="return validate_add_to_target();" style="margin:0 50px 0 0a;width:120px;">Add to Target</button>

	</td>
	</tr>



	</table>
	</form>

			  <p>&nbsp;</p>
			  </div>

			  <div id="subsubtabs-2">

	<form name = 'show_iscsi_target_list' method = 'POST' action = 'iframe_vtl_settings.py#tabs-3'>
	<table width='100%' >
		<tr>
			<th style='background-color:#D1D1D1; color:#000; padding:5px;'>Library Name</th>
			<th style='background-color:#D1D1D1; color:#000;'>VTL ISCSI Target Details</th>
			<th style='background-color:#D1D1D1; color:#000;'>Delete Target</th>
		</tr>"""

	if get_all_vtls['id']== 0:
		if len(get_all_vtls['vtl_libs']) != 0:
			for lib in get_all_vtls['vtl_libs']:

				l_h_d = lib['lib_home_dir']
				split_lhd = string.split(l_h_d,"/")
				if(len(split_lhd) > 4):
					post_lib_name = split_lhd[3]
				else:
					post_lib_name = ''

				list_iscsi_tar = san_disk_funs.list_vtl_iscsi_target(str(lib['lib_name'].replace(' ', '')+'VTL'+post_lib_name))
				print """<tr> 
				<td class='border' align='center'>"""+lib['lib_name'].replace(' ', '')+'VTL'+post_lib_name+"""</td>
				<td class="border" align='left'>"""
				if(list_iscsi_tar != {}):
					print "<b>luns : </b>"+str(list_iscsi_tar['luns'])
					print "<br/>"
					print "<b>target : </b>"+str(list_iscsi_tar['target'])
					print "<br/>"
					print "<b>initiator : </b>"+str(list_iscsi_tar['ini'])
					print "<br/>"
				else:
					print "Not Found"
				print """</td>
				<td class="border" align='center'>"""
				if(list_iscsi_tar != {}):
					sess = san_disk_funs.iscsi_session(str(list_iscsi_tar['target']))
                                        if(sess == []):
						print """<button class="buttonClass" type="submit" name = 'delete_target'  id = 'delete_target' value = '"""+str(lib['lib_id'])+"""'  onclick="return confirm('Are you sure you want to delete?');">Delete</button>"""
					else:
						print """<button class="buttonClass" type="button" name = 'd_t'  id = 'd_t' value = ''  onclick="alert('Cannot delete Target since there are active sessions!');">Delete</button>"""
								

				print """</td>
				</tr>"""

	print """</table></form>



				<p>&nbsp;</p>
			  </div>

			  <div id="subsubtabs-3">

	<table width='100%' >
		<tr>
			<th style='background-color:#D1D1D1; color:#000; padding:5px;'>Library Name</th>
			<th style='background-color:#D1D1D1; color:#000; padding:5px;'>Target Details</th>
			<th style='background-color:#D1D1D1; color:#000; padding:5px;'>Client IP Info</th>
		</tr>"""

	if get_all_vtls['id']== 0:
		if len(get_all_vtls['vtl_libs']) != 0:
			for lib in get_all_vtls['vtl_libs']:

				l_h_d = lib['lib_home_dir']
				split_lhd = string.split(l_h_d,"/")
				if(len(split_lhd) > 4):
					post_lib_name = split_lhd[3]
				else:
					post_lib_name = ''

				list_iscsi_tar = san_disk_funs.list_vtl_iscsi_target(str(lib['lib_name'].replace(' ', '')+'VTL'+post_lib_name))
				print """<tr> 
				<td class='border' align='center'>"""+lib['lib_name'].replace(' ', '')+'VTL'+post_lib_name+"""</td>
				<td class="border" align='left'>"""
				if(list_iscsi_tar != {}):
					sess = san_disk_funs.iscsi_session(str(list_iscsi_tar['target']))
					if(sess != []):
						font_color = "#298A08"
					else:
						font_color = "#DF0101"

					print """<span style='color:"""+font_color+""";'>"""+str(list_iscsi_tar['target'])+"""</span>"""
				else:
					print "<span style='color:#DF0101;'>Not Found!</span>"
				print """</td>
				<td class="border" align='center'>"""
				if(list_iscsi_tar != {}):
					if(sess != []):
						for j in sess:
							sess_f = san_disk_funs.iscsi_session_info(str(list_iscsi_tar['target']),j)
							if(sess != []):
								print"""<a class="various" data-fancybox-type="iframe" style="color:#292915;text-decoration:none;" href="iscsi_ip_info.py?ip="""+sess_f["ips"]+"""&data_dig="""+sess_f["DataDigest"]+"""&fbl="""+sess_f["FirstBurstLength"]+"""&maxxmit="""+sess_f["MaxXmitDataSegmentLength"]+"""&maxburst_len="""+sess_f["MaxBurstLength"]+"""&none_cmd_out="""+sess_f["none_cmd_count"]+"""&ini_r2t="""+sess_f['InitialR2T']+"""&max_ini_r2t="""+sess_f["MaxOutstandingR2T"]+"""&active_cmd="""+sess_f["active_commands"]+"""&hd="""+sess_f["HeaderDigest"]+"""&imd="""+sess_f["ImmediateData"]+"""&write_cmd="""+sess_f["write_cmd_count"]+"""&read_cmd="""+sess_f["read_cmd_count"]+"""&sid="""+sess_f["sid"]+"""&read_kb="""+sess_f["read_io_count_kb"]+"""&write_kb="""+sess_f["write_io_count_kb"]+"""&ini_name="""+sess_f["initiator_name"]+""""><b><font color="green">"""+sess_f["ips"]+"""</font></b></a>"""+ "<br/>"
							else:
								print "No client Connected!"
					else:
						print "<span style='color:#DF0101;'>No client Connected!</span>"
				else:
					print "<span style='color:#DF0101;'>Not Found!</span>"
				print """</td>
				</tr>"""

	print """</table>





			<p>&nbsp;</p>
			  </div>

			</div>
			
			  </div>

			  <div id="subtabs-2">
				<div align='center' style='background-color:#585858; color:#FFF; height:70px; -moz-border-radius: 10px; -webkit-border-radius: 7px; border-radius: 7px; -khtml-border-radius: 7px; '><img src="../images/information4.png" height="30px" width="30px" alt='info'style="float:left; padding:20px 0 0 150px;"/> <span style="float:left; padding:25px 0 0 10px; font-size:14px; color:#FFF;">This Section is currently Under Development!</span></div>
			  </div>

			  <div id="subtabs-3">
				<div align='center' style='background-color:#585858; color:#FFF; height:70px; -moz-border-radius: 10px; -webkit-border-radius: 7px; border-radius: 7px; -khtml-border-radius: 7px; '><img src="../images/information4.png" height="30px" width="30px" alt='info'style="float:left; padding:20px 0 0 150px;"/> <span style="float:left; padding:25px 0 0 10px; font-size:14px; color:#FFF;">This Section is currently Under Development!</span></div>
			  </div>

			</div>
		      </div>

		      <div id="tabs-5">

		<!--form container starts here-->
		<form name = 'add_tape_form' method = 'POST' action = 'iframe_vtl_settings.py#tabs-5'>
		<div class="form-container">
		<div class="topinputwrap-heading"> Add Tape </div>
		<div class="topinputwrap">
		<table width="100%" style="border:#BDBDBD 1px solid;">
		<tr>
		<td>Select Tape Density</td>
		<td>
	<div class="styled-select2">
	<select class = 'input' name='tape_density' id='tape_density'>
	<option value=''>Select Tape Density</option>"""
	for index, density in enumerate(mhvtl.vtl_tape_density):
		print """<option value = '"""+density+"""'"""
		if(get_t_d != ''):
			if(get_t_d == density):
				print """selected = selected"""

		print """>"""+density+"""</option>"""

	print """</select></div>
		</td>
		</tr>

		<tr>
		<td>Select Tape Type</td>
		<td>
	<div class="styled-select2">
	<select class = 'input' name='tape_type' id='tape_type' onchange="this.form.submit();">
	<option value=''>Select Tape Type</option>"""
	for index, tape_type in enumerate(mhvtl.vtl_tape_types):
		print """<option value = '"""+tape_type+"""'"""
		if(get_t_t != ''):
			if(get_t_t == tape_type):
				print """selected = selected"""

		print """>"""+tape_type+"""</option>"""

	print """</select></div>
		</td>
		</tr>

		<tr>
		<td>Enter Tape Size (MB)</td>
		<td>
		<input class = 'textbox' type = 'text' name = 'tape_size' id = 'tape_size' value = '"""+str(auto_tape_size)+"""' """+readonly_tape_size+""">
	 <input class = 'textbox' type = 'hidden' name = 'tape_lib_id' id = 'tape_lib_id' value = '"""+str(get_lib_id_new)+"""' />
		</td>
		</tr>

		</table>
		<div style="float:right; margin:10px;">
		<button class="buttonClass" type = 'submit'  name = 'submit_add_tape' value ='submit_add_tape' onclick = 'return add_tape_to_library();' >Add Tape</button>
		</div>
		</div>
		</div>
		</form>

		<p>&nbsp;</p>
		      </div>

		</div>
		    </div>
		  </div>
		</div>
	<!-- ####### Sub Tabs Start ####### -->

	<script>
	$("#tabs, #subtabs").tabs();
	$("#tabs, #subsubtabs").tabs();
	</script>

	<!-- ####### Sub Tabs End ####### -->
	"""
except Exception as e:
	disp_except.display_exception(e);
