#!/usr/bin/python
import cgitb, sys, common_methods, include_files
cgitb.enable()
sys.path.append('../modules/')
import disp_except;
try:
	import cgitb, os, cgi, sys, commands, system_info
        cgitb.enable()
	#-------------------------------Import backend Modules----------------------------
        sys.path.append('/var/nasexe/storage/')

        import storage_op
        from lvm_infos import *
        from functions import *
	#-----------------------------------End--------------------------------------------
	#-------------------Call the backend function for volume and Disk----------------------
        vg_info  = get_vgs()
        nas_info = get_lvs()
        free_d   = free_disks()
	#-------------------End---------------------------------------------------------------
	sys.path.append("/var/nasexe/python/")
        import tools
        from tools import db
	#----------------------Check HA status----------------------
	check_ha = tools.check_ha()
	#-------------------------End------------------------------
	#-------------------This function show the Current Node-----------------------------------
        sys_node_name = tools.get_ha_nodename()
	#--------------------------------End------------------------------------------------------
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

	print
	print """
		<div id="loader-div" style="text-align:center; display:none;" ><img style="margin-top:20%;" src="../images/ajax-loader.gif" /><br/> Loading...</div>
	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer" id="body-div">
		<!--tab srt-->
		<div class="searchresult-container">
		  <div class="infoheader">
		<div class="topinputwrap-heading"><a class="demo" href ="#"><img src ="../images/help_icon1.png" style="width:13px;"><span class="tooltip" >
        <div style="font-size: medium;text-align:start;margin-left:8px;">Disk Information:</div>
        

        <div class="text_css">In this Page display the Information of Disk and Protocol.In Disk Information like Disk Name, Total Space and used(%) and in Protocol like Smb,Ftp,Afp,Nfs,Audit and Smb log Path.</div>
        """
	if(check_ha == True):
		print"""</span></a>Disk Information ("""+show_tn+""")
                <span style="float:right; margin:5px 0px 0 0;"><a onclick="return onclick_loader();" class="resource_links" href="https://"""+other_node_ip+"""/fs4/py/iframe_disk_info.py">"""+show_on+"""</a></span>
                </div>"""
	else:
		print"""</span></a>Disk Information</div>"""
	print"""
		    <!--<div id="tabs">
		      <ul>
			<li><a href="#tabs-1">Disk Info</a></li>
		      </ul>-->
		      <div id="tabs-1">

		<!--form container starts here-->
		<div class="iframe-form-container">
		<div class="formrightside-content">"""
	if(nas_info["lvs"] != [{}]):
        	print"""
		<style>
		table { margin: 1em; border-collapse: collapse; }
		td, th { padding: .3em; border: 1px #ccc solid; }
		td { text-align:center;}
		</style>
                <table style="width:730px;">
                <tr>
                <th>Disk Name</th>
                <th>Total Space</th>
                <th>Used(%)</th>
                <th>SMB</th>
                <th>NFS</th>
                <th>FTP</th>
                <th>AFP</th>
                <th>SMB Log Path</th>
                <th>Audit</th> 
                </tr>"""
		#-----------------------------Get the nas Disk----------------------------------------------
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
					use_per = "Disk not Mounted"


				get_protocols = system_info.check_protocols(x["lv_name"])
				#print get_protocols
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
					if(check_AUDIT < 0):
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

		#-----------------------------------------------End-------------------------------------------------------------
		print"""</table>"""
	else:
        	print "<div style = 'padding:20px 0 0 300px;color:#2C2222;font-size:12px;'><b>No Disk is Created</b>!</div>"
	print"""
		
		</div></div></div>
</div>
                <p>&nbsp;</p>
                      </div>
                        
                  </div>
                </div>
	"""
except Exception as e:
        disp_except.display_exception(e);
