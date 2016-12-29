#!/usr/bin/python
import cgitb, sys, common_methods, include_files
cgitb.enable()
sys.path.append('../modules/')
import disp_except;
try:
	#################################################
        ################ import modules #################
        #################################################
	import cgitb, os, cgi, sys, commands, opslag_info, system_info
        cgitb.enable()
        sys.path.append('/var/nasexe/storage/')
        import storage_op
        from lvm_infos import *
        from functions import *
        sys.path.append('/var/nasexe/storage/')
        import storage_op
        from lvm_infos import *;
        from functions import *
	
	#--- Get VGS
        vg_info  = get_vgs()

	#--- Get LVS
        nas_info = get_lvs()

	#--- Get free disks
        free_d   = free_disks()

	sys.path.append("/var/nasexe/python/")
	import tools
	from tools import db
	sys.path.append("/var/nasexe/python/")
        import tools
        from tools import db
        from tools import shutdown
	#--------------------- END --------------------#

	################################################
        ################ Check HA Status ###############
        ################################################
	check_ha = tools.check_ha() 
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
	#--------------------- END --------------------#


	print
	print """
		 <style>
                table { margin: 1em; border-collapse: collapse; }
                td, th { padding: .3em; border: 1px #ccc solid; }
                td { text-align:center;}
		.clr {clear: both; height: 0px; margin: 0px; padding: 0px;}
                </style>

		<div id="loader-div" style="text-align:center; display:none;" ><img style="margin-top:20%;" src="../images/ajax-loader.gif" /><br/> Loading...</div>
	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer" id="body-div">
		<!--tab srt-->
		<div class="searchresult-container">
		  <div class="infoheader" style= "border:none;">
		<div class="topinputwrap-heading" style="width:734px;">

		<a class="demo" href ="#"><img src ="../images/help_icon1.png" style="width:13px;"><span class="tooltip" >
        <div class="text_css">This page displays information about all the RAID volumes, NAS disks and iSCSI/FC/SRP disks present on your system.</div>
        """
	if(check_ha == True):
		print"""</span></a>
	<p class = "gap_text">Volume and Disk Information ("""+show_tn+""")</p>
                <span style="float:right; margin:-13px 0px 0 0;"><a onclick="return onclick_loader();" class="resource_links" href="https://"""+other_node_ip+"""/fs4/py/volume_disk_info.py">"""+show_on+"""</a></span></div>"""
	else:
		 print"""</span></a><span style="margin-left:5px;color:#FFFFFF;"><p class = "gap_text">Volume and Disk Information</p></span>
                </div>"""
	print """
		    <!--<div id="tabs">
		      <ul>
			<li><a href="#tabs-1">Volume Info</a></li>
		      </ul>-->
		      <div id="tabs-1">

		<!--form container starts here-->
		<div class="iframe-form-container">"""
	multi = 1;

        if(vg_info["vgs"]!=[{}]):

                print"""
<div style ="background:#ccc; text-align:center; padding:5px; color:#365371; margin:0 0 -12px 12px; width:185px;"><b>Volume Information</b></div>
			 <table style="width:730px; ">
                <tr>
                <th>Volume Name</th>
                <th>Total Space</th>
                <th>Free Space</th>
                </tr>
                        
                        """
                for x in vg_info["vgs"]:
                        new_free   = x["free_size"]
                        total_size = x["size"]

                        if (total_size.find('g') > 0):
                                size = total_size.replace("g", "");

                        if (total_size.find('t') > 0):
                                multi = 1024;
                                size = total_size.replace("t", "")

                        size = float(size) * multi;
                        size = str(size) + '&nbsp;GB';
			if (new_free.find('g') > 0):
                        	free_size = new_free.replace("g", "");
                                free_size = new_free.replace("g", "")

                        if (new_free.find('t') > 0):
                                multi = 1024;
                                free_size = new_free.replace("t", "")

                        free_size = float(free_size) * multi;
                        free_size = str(free_size) +  '&nbsp;GB';

                        print"""
			<tr>
                                        <td >"""+x['vg_name']+""" </td>
                                        <td >"""+size+""" </td>
                                        <td >"""+free_size+""" </td>
                                        </tr>

				"""

		print"</table>"
	else:
        	print """
<div class="clr"></div>
<div style ="background:#ccc; text-align:center; padding:5px; color:#365371; margin-left:8px; width:190px;"><b>Volume Information</b></div>
<table style="width:730px;margin-top: 0px;margin-left: 8px;">
<tr>
<td>No volume present!</td>
</tr>
</table>"""
	print"""
</div>
	</div>
		</div>
			</div>
	
         <p>&nbsp;</p>
         	</div>"""
        if(nas_info["lvs"] != [{}]):
                print"""
                <style>
                table { margin: 1em; border-collapse: collapse; }
                td, th { padding: .3em; border: 1px #ccc solid; }
                td { text-align:center;}
                </style>
		<div class="clr"></div>
                <div style ="background:#ccc; text-align:center; padding:5px; color:#365371; margin-left:38px; width:190px;"><b>NAS Disk Information</b></div>
                <table style="width:730px;margin-top: 0px;margin-left: 38px;">
                 <!--<div class="topinputwrap-heading" style="margin-left: 38px;">Nas Disk Information:</div>-->
                <tr>
                <th>Disk Name</th>
                <th>Total Space</th>
                <th>Used (%)</th>
                <th>SMB</th>
                <th>NFS</th>
                <th>FTP</th>
                <th>AFP</th>
                <th>SMB Log Path</th>
                <th>Audit</th> 
                </tr>"""
	 	for x in nas_info["lvs"]:
			#z = x["size"]
			#print z
			total_size=x["size"]
			size=total_size.replace("g", "&nbsp;GB")
			#print size
			if (total_size.find('t') > 0):
				multi = 1024;
				size = total_size.replace("t", "")

				size = float(size) * multi;
				size = str(size) + 'GB';

			grep_line = commands.getstatusoutput("sudo df -h|sed -n '/Use/, /^$/p'|grep '"+x["lv_name"]+"'  > /tmp/useperfile")
			#print grep_line
			if(grep_line[0] == 0):
				get_line = commands.getstatusoutput("cat /tmp/useperfile")
				get_per_str = get_line[1]
				if(get_line[0] == 0):
					split_gl = get_per_str.split()
					use_per = split_gl[4]
				else:
					#use_per = "Unable to Get Information"
					use_per = "Disk not mounted"
			else:
				#use_per = "Unable to Get Information"
				use_per = "Disk not mounted"


			get_protocols = system_info.check_protocols(x["lv_name"])
			check_str = isinstance(get_protocols, str)
			if(check_str != True):
				get_protocols = str(get_protocols)

				check_SMB = get_protocols.find("SMB")
				check_NFS = get_protocols.find("NFS")
				check_FTP = get_protocols.find("FTP")
				check_AFP = get_protocols.find("AFP")
				check_SMB_LOG_PATH = get_protocols.find("SMB_LOG_PATH")
				check_AUDIT = get_protocols.find("AUDIT")
				if(check_SMB > 0):
					smb_active_png = '<img src = \'../images/tick_active2.jpeg\' title = "SMB Enabled">'
				else:
					smb_active_png = '<img src = \'../images/ko_red1.ico\'>'
				if(check_NFS > 0):
					nfs_active_png = '<img src = \'../images/tick_active2.jpeg\' title = "NFS Enabled">'
				else:
					nfs_active_png = '<img src = \'../images/ko_red1.ico\'>'

				if(check_FTP > 0):
					ftp_active_png = '<img src = \'../images/tick_active2.jpeg\' title = "FTP Enabled">'
				else:
					ftp_active_png = '<img src = \'../images/ko_red1.ico\'>'


				if(check_AFP > 0):
					afp_active_png = '<img src = \'../images/tick_active2.jpeg\' title = "AFP Enabled">'
				else:
					afp_active_png = '<img src = \'../images/ko_red1.ico\'>'

				if(check_SMB_LOG_PATH > 0):
					smbl_active_png = '<img src = \'../images/tick_active2.jpeg\' title = "SMB LOG PATH Enabled">'
				else:
					smbl_active_png = '<img src = \'../images/ko_red1.ico\'>'
				if(check_AUDIT > 0):
					audit_active_png = '<img src = \'../images/tick_active2.jpeg\' title = "AUDIT Enabled">'
				else:
					audit_active_png = '<img src = \'../images/ko_red1.ico\'>'
			else:
				smb_active_png = '<img src = \'../images/ko_red1.ico\'>'
				nfs_active_png = '<img src = \'../images/ko_red1.ico\'>'
				ftp_active_png = '<img src = \'../images/ko_red1.ico\'>'
				afp_active_png = '<img src = \'../images/ko_red1.ico\'>'
				smbl_active_png = '<img src = \'../images/ko_red1.ico\'>'
				audit_active_png = '<img src = \'../images/ko_red1.ico\'>'
			print"""
				<tr>
				<td >"""+x['lv_name']+""" </td>
				<td >"""+size+""" </td>
				<td >"""+use_per+""" </td>
				<td >"""+smb_active_png+"""</td>
				<td >"""+nfs_active_png+""" </td>
				<td >"""+ftp_active_png+""" </td>
				<td >"""+afp_active_png+""" </td>
				<td >"""+smbl_active_png+""" </td>
				<td >"""+audit_active_png+""" </td>
				</tr>"""
		print"""</table>"""
	else:
		print """
<div class="clr"></div>
<div style ="background:#ccc; text-align:center; padding:5px; color:#365371; margin-left:38px; width:190px;"><b>NAS Disk Information</b></div>
<table style="width:730px;margin-top: 0px;margin-left: 38px;">
<tr>
<td>No NAS disk present!</td>
</tr>
</table>"""
	available_san_disk = shutdown.available_san_disk()
        iscsi_used_disk = shutdown.check_iscsi_disk()
        srp_used_disk = shutdown.check_srp_disk()
        fc_used_disk = shutdown.check_fc_disk()
	if(available_san_disk != []):	
		print"""
				
	<div style ="background:#ccc; text-align:center; padding:5px; color:#365371; margin-left:38px; width:190px;"><b>iSCSI/FC/SRP Disk Information</b></div>
	<table style="width:730px;margin-top: 0px;margin-left: 38px;">
			<tr>
			<th>Disk Name</th>
			<th>iSCSI</th>
			<th>SRP</th>
			<th>FC</th>
			</tr>"""
		for y in available_san_disk:
			print """<tr>
			<td>"""+y+"""</td>
			<td>"""
			iscsi_present = '<img src = \'../images/ko_red1.ico\' title = "iSCSI" style="cursor: pointer;">'
			#if any(d.get('0', None) == y for d in iscsi_disk):
			#       iscsi_present = '<img src = \'../images/tick_active2.jpeg\' title = "iSCSI" style="cursor: pointer;">'  
			search_list = tools.search_nested_list(iscsi_used_disk, y)
			if(search_list == "yes"):
				iscsi_present = '<img src = \'../images/tick_active2.jpeg\' title = "iSCSI" style="cursor: pointer;">'

			print iscsi_present

			print """</td>"""
			print"""<td>"""
			srp_present = '<img src = \'../images/ko_red1.ico\' title = "SRP" style="cursor: pointer;">'
			#if any(e.get('0', None) == y for e in srp_disk):
			#        srp_present = '<img src = \'../images/tick_active2.jpeg\' title = "SRP" style="cursor: pointer;">'
			search_list = tools.search_nested_list(srp_used_disk, y)
			if(search_list == "yes"):
				srp_present = '<img src = \'../images/tick_active2.jpeg\' title = "SRP" style="cursor: pointer;">'

			print srp_present

			print """
			</td>
				<td>"""
			fc_present = '<img src = \'../images/ko_red1.ico\' title = "Fc" style="cursor: pointer;">'
			#if any(f.get('0', None) == y for f in fc_disk):
			 #       fc_present = '<img src = \'../images/tick_active2.jpeg\' title = "Fc" style="cursor: pointer;">'
			search_list = tools.search_nested_list(fc_used_disk, y)
			if(search_list == "yes"):
				fc_present = '<img src = \'../images/tick_active2.jpeg\' title = "FC" style="cursor: pointer;">'
			print fc_present

			print"""
			</td>
			</tr>
				"""
		print"""</table>"""
	else:
		print """<div class="clr"></div>
<div style ="background:#ccc; text-align:center; padding:5px; color:#365371; margin-left:38px; width:190px;"><b>iSCSI/FC/SRP Disk Information</b></div>
<table style="width:730px;margin-top: 0px;margin-left: 38px;">
<tr>
<td>No iSCSI/FC/SRP disk present!</td>
</tr>
</table>"""



	print """
                      </div>
	</div>
                        
                  </div>
                </div>
	"""
except Exception as e:
        disp_except.display_exception(e);
