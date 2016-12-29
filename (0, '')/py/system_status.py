#!/usr/bin/python

import traceback, sys, header
sys.path.append('../modules/')
import disp_except;

try:
	import cgitb, os, cgi, sys, commands, opslag_info, system_info, memory_information
	cgitb.enable()

	sys.path.append('/var/nasexe/storage/')

        import storage_op
        from lvm_infos import *
        from functions import *

        sys.path.append('/var/nasexe/storage/')
        import storage_op

        from lvm_infos import *;
        from functions import *

        vg_info  = get_vgs()
        nas_info = get_lvs()
        free_d   = free_disks()

	memory_info = memory_information.mem_information()
	
	#-----------------------All Information Getting from Tools -----------------------
        sys.path.append('/var/nasexe/python/')
	from tools import ipmi
        from tools import scan_remount
	ipmi_cpu_info =ipmi.cpu_temp()

        ipmi_fan_info = ipmi.fan_speed()

        ipmi_power_info = ipmi.power_supply()

        cpu_new_model = scan_remount.cpu_model()

        cpu_new_intrusion = scan_remount.intrusion()

	intrusion = cpu_new_intrusion

        server_ip_cmd = scan_remount.server_ip()

        remote_ip_cmd = scan_remount.remote_ip()

	server_cmd = scan_remount.server_name()

	uptime_cmd = scan_remount.up_time()

	cpu_use_cmd = scan_remount.cpu_use()

	raid_temp_cmd = scan_remount.raid_temp()
	raid_cpu_temp =raid_temp_cmd[0]
	raid_controller_temp =raid_temp_cmd[1]

	last_login_cmd = scan_remount.last_login()

	current_login_cmd = scan_remount.current_login()
	status_dump= shutdown.dump_configuration_module()
	print status_dump
	#--------------------------------End----------------------------------------

	#----------Log Size Comment------------------ 
	#log_size = common_methods.get_log_size();

        #log_size = str(log_size).replace('G', '');
        #log_size = str(log_size).replace('M', '');
        #log_size = str(log_size).replace('K', '');

        #log_size = log_size.strip();

	#if (float(log_size) > 200):
        #        print "<script>alert('Log files reached the size limit. Clearing them! For logs you can download the [fs2_logs.tar] from [Support] page.');</script>";
        #        print "<script>location.href = 'clear_logs.py';</script>";
	#-------------End-----------------------------
        #print server 

        #for last login command


        #print last_time


	import left_nav
	print"""
	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer">
		<div class="insidepage-heading"> RESOURCES >> <span class="content">Resources Information</span></div>
		<!--tab srt-->
		<div class="searchresult-container">
		  <div class="infoheader">
		    <div id="tabs">
		      <ul>
			<li><a href="#tabs-1">System Information</a></li>
			<li><a href="#tabs-2">Sensor Information</a></li>
			<li><a href="#tabs-3">Volume Group Information</a></li>
			<li><a href="#tabs-4">Disk Information</a></li>
		      </ul>
			
			<div id="tabs-1">
			<div class="form-container">
			<div class="inputwrap">
                    <div class="formleftside-content">CPU:</div>
                    <div class="formrightside-content"><img src='../images/cpu_img1.png'>"""+cpu_new_model+"""</div>
                  </div>
                  <div class="topinputwrap">
                    <div class="formleftside-content">Server IP:</div>
                    <div class="formrightside-content">""" +server_ip_cmd+ """</div>
                 </div>
		 <div class="inputwrap">
                    <div class="formleftside-content">Remote IP:</div>
                    <div class="formrightside-content"> """ +remote_ip_cmd+ """</div>
                  </div>
                  <div class="altinputwrap">
                    <div class="formleftside-content">HostName:</div>
                    <div class="formrightside-content">""" + server_cmd + """</div>
                  </div>
                  <div class="inputwrap">
                    <div class="formleftside-content">Uptime:</div>
                    <div class="formrightside-content">""" + uptime_cmd + """</div>
                  </div>
                  <div class="altinputwrap">
                    <div class="formleftside-content">Current Login:</div>
                    <div class="formrightside-content" style="margin-top: -2%;">""" +current_login_cmd+ """</div>
                  </div>
                 <div class="inputwrap">
                    <div class="formleftside-content">Last Login:</div>
                    <div class="formrightside-content" style="margin-top: -2%;">""" +last_login_cmd+ """</div>
                  </div>
                 <div class="altinputwrap">
                    <div class="formleftside-content">Memory(MB):</div>
                    <div class="formrightside-content">""" +memory_info["total"]+ """</div>
                  </div>
                
                <div class="inputwrap">
                    <div class="formleftside-content">Used Memory(MB):</div>
                    <div class="formrightside-content">""" +memory_info["used"]+ """</div>
                  </div>

		  <div class="altinputwrap">
                    <div class="formleftside-content">Free Memory(MB):</div>
                    <div class="formrightside-content">""" +memory_info["free"]+ """</div>
                  </div>
                 <div class="inputwrap">
                    <div class="formleftside-content">Cpu usage:</div>
                    <div class="formrightside-content">""" +cpu_use_cmd+ """</div>
                  </div>
		<div class="altinputwrap">
                    <div class="formleftside-content">OS:</div>
                    <div class="formrightside-content">""" + opslag_info.getos('oss') + """</div>
                  </div>
                 <div class="inputwrap">
                    <div class="formleftside-content">Version:</div>
                    <div class="formrightside-content">""" + opslag_info.getos('version') + """</div>
                  </div>
		<div class="altinputwrap">
                    <div class="formleftside-content">Build:</div>
                    <div class="formrightside-content">""" + opslag_info.getos('build') + """</div>
                  </div>
                 <div class="inputwrap">
                    <div class="formleftside-content">Model:</div>
                    <div class="formrightside-content">""" + opslag_info.getos('model') +"""</div>
                  </div>

		  <div class="altinputwrap">
                    <div class="formleftside-content">Serial:</div>
                    <div class="formrightside-content">""" + opslag_info.getos('serial') + """</div>
                  </div>
                 <div class="inputwrap">
                    <div class="formleftside-content">Dispatch Date:</div>
                    <div class="formrightside-content">""" + opslag_info.getos('disp_date') +"""</div>
                  </div>
		</div>
		<p>&nbsp;</p>
		      </div>
			
		      <div id="tabs-2">
		  
		      <div class="form-container">
                	<div class="inputwrap">"""
	for cpu_info_value in ipmi_cpu_info.values():
		cpu_info_value = str(cpu_info_value);
		if(cpu_info_value == '0'):
			print"""<div class="formleftside-content"><img src='../images/cpu_img1.png'>:<span>Not-Connected</span></div><br/><br/><br/><br/>"""
		else:

			print"""<div class="formleftside-content"><img src='../images/cpu_img1.png'>:<b style = "text-decoration:blink;color:green;">"""+ cpu_info_value + """<sup>o</sup>C</b></div><br/><br/><br/>"""
	print"""</div>
                <div class="inputwrap">
                    <div class="formleftside-content">Fan Speed(RPM):</div>
                    <div class="formrightside-content"style="margin-left:-6%;">"""
	for keys in ipmi_fan_info:
        	ipmi_fan_val = str(ipmi_fan_info[keys]);
		fan_icon = "<img src='../images/cpu_fan_nw.gif'>"
		fan1_icon = "<img src='../images/cpu_fan6.jpeg'>"
                fan_speed = ipmi_fan_val;
		if(fan_speed == '0'):
			print""" """+fan1_icon+"""<span>"""+fan_speed+"""</span>"""
		else:			
			print""" """+fan_icon+"""<span style="color:green;">"""+fan_speed+"""</span>"""


	print"""</div>
                  </div>

		 <div class="inputwrap">
                    <div class="formleftside-content">RAID CPU:</div>"""
	if(raid_cpu_temp == 'Raid not detected!'):
                    print"""<div class="formrightside-content" style="margin-left:-12%;"><span>"""+raid_cpu_temp+"""</span></div>"""
	else:
		print"""<div class="formrightside-content" style="margin-left:-12%;"><b style = "text-decoration:blink;color:green;">"""+raid_cpu_temp+"""<sup>o</sup>C</b></div>"""
	print"""                </div>

		<div class="inputwrap">
                    <div class="formleftside-content">RAID Controller:</div>"""
	if(raid_controller_temp == 'Raid not detected!'):
        	print"""<div class="formrightside-content" style="margin-left:-7%;"><span>"""+raid_controller_temp+"""</span></div>"""
	else:
		print"""<div class="formrightside-content" style="margin-left:-7%;"><b style = "text-decoration:blink;color:green;">"""+raid_controller_temp+"""<sup>o</sup>C</b></div>"""
	print"""                        </div>"""

	print"""                <div class="inputwrap">"""
	for keys in ipmi_power_info:
        	#print keys + ':' + str(ipmi_power_info[keys]);
                print"""<div class="formleftside-content">"""+keys+""":"""+ipmi_power_info[keys]+"""</div><br/><br/>"""
	print"""
                  </div>

		  <div class="inputwrap">
                    <div class="formleftside-content">Intrusion:</div>
                    <div class="formrightside-content" style="margin-left:-12%;">""" +intrusion+ """</div>
			</div>

			</div>
		      </div><p>&nbsp;</p>"""
	print"""<div id="tabs-3">


		<div class="form-container">"""

	multi = 1;

        if(vg_info["vgs"]!=[{}]):

		print"""
			
                	<div class="inputwrap">
                    	<div class="formleftside-content" style ="color:DarkOliveGreen;font-family: menu;"><b>Volume Name</b></div>
			<div class="formleftside-content" style ="color:DarkOliveGreen;font-family: menu;"><b>Total Space</b></div>
			<div class="formleftside-content" style ="color:DarkOliveGreen;font-family: menu;"><b>Free Space</b></div></div>"""
                for x in vg_info["vgs"]:
                        new_free   = x["free_size"]
                        total_size = x["size"]

                        if (total_size.find('g') > 0):
                                size = total_size.replace("g", "");

                        if (total_size.find('t') > 0):
                                multi = 1024;
                                size = total_size.replace("t", "")

                        size = float(size) * multi;
                        size = str(size) + 'GB';

                        if (new_free.find('g') > 0):
                                free_size = new_free.replace("g", "");
                                free_size = new_free.replace("g", "")

                        if (new_free.find('t') > 0):
                                multi = 1024;
                                free_size = new_free.replace("t", "")

                        free_size = float(free_size) * multi;
                        free_size = str(free_size) + 'GB';

			print"""<div class="inputwrap">
                    	<div class="formrightside-content" style ="margin-left:7%;margin-top:1%;">"""+x["vg_name"]+"""</div>
                  	</div>
                	<div class="inputwrap">
                    	<div class="formrightside-content" style ="margin-left:3%;margin-top:-3%;text-align:center;">"""+size+"""</div>
                  	</div>
                	<div class="inputwrap">
                    	<div class="formrightside-content" style ="margin-top:-4%;text-align:right;margin-left:1%;">"""+free_size+"""</div>
                  	</div>"""

	else:
        	print "<div style = 'padding:20px 0 0 267px; font-size:12px;text-decoration:underline;'><a href ='main.py?page=rs'>No Volume is Created</a> !</div>"
	print"""</div><p>&nbsp;</div></p>
		
			<div id="tabs-4">	
			<div class="form-container">
                    <div class="formrightside-content">"""
	if(nas_info["lvs"] != [{}]):

		print"""<div class="inputwrap">
		<table style="width: 149%;">
		<tr>
		<td class="formleftside-content" style="width:77px;color:DarkOliveGreen;font-family: menu;margin-left:7%;"><b>Disk Name</b></td>
		<td class="formleftside-content" style="width:82px;color:DarkOliveGreen;font-family: menu;"><b>Total Space</b></td>
		<td class="formleftside-content" style="width:28px;color:DarkOliveGreen;font-family: menu;"><b>Used(%)</b></td>
		<!--<td class="formleftside-content" style="width:44px;color:DarkOliveGreen;font-family: menu;"><b>Snapshot</b></td>-->
		<td class="formleftside-content" style="width:0px;color:DarkOliveGreen;font-family: menu;"><b>SMB</b></td>
		<td class="formleftside-content" style="width:0px;color:DarkOliveGreen;font-family: menu;"><b>NFS</b></td>
		<td class="formleftside-content" style="width:0px;color:DarkOliveGreen;font-family: menu;"><b>FTP</b></td>
		<td class="formleftside-content" style="width:0px;color:DarkOliveGreen;font-family: menu;"><b>AFP</b></td>
		<td class="formleftside-content" style="width:96px;color:DarkOliveGreen;font-family: menu;"><b>SMB Log Path</b></td>
		<td class="formleftside-content" style="width:0px; margin-left:2%;color:DarkOliveGreen;font-family: menu;"><b>Audit</b></td> 
		</tr>
		"""

		for x in nas_info["lvs"]:
                        #z = x["size"]
                        #print z
                        total_size=x["size"]
                        size=total_size.replace("g", "GB")
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
                                        use_per = "Unable to Get Information"
                        else:
                                use_per = "Unable to Get Information"


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
				<td class="formleftside-content" style="width:82px;margin-top:2%;margin-left:8%;">"""+x['lv_name']+""" </td>
				<td class="formleftside-content" style="width:72px;margin-top:2%;">"""+size+""" </td>
				<td class="formleftside-content" style="width:24px;margin-left:7%;margin-top:2%;">"""+use_per+""" </td>
				<!--<td class="formleftside-content" style="width:44px;margin-top:2%;">"""""" </td>-->
				<td class="formleftside-content" style="width:0px;margin-top:2%;">"""+smb_active_png+"""</td>
				<td class="formleftside-content" style="width:0px;margin-top:2%;">"""+nfs_active_png+""" </td>
				<td class="formleftside-content" style="width:0px;margin-top:2%;">"""+ftp_active_png+""" </td>
				<td class="formleftside-content" style="width:0px;margin-top:2%;">"""+afp_active_png+""" </td>
				<td class="formleftside-content" style="width:84px; padding-left: 33px;margin-top:2%;">"""+smbl_active_png+""" </td>
				<td class="formleftside-content" style="width:0px; margin-left:-1%;margin-top:2%;">"""+audit_active_png+""" </td>
				</tr>"""


        	print"""</table>"""

	
	else:
		
                print "<div style = 'padding:20px 0 0 300px;color:#2C2222;font-size:12px;'><b>No Disk is Created</b>!</div>"
	print"""</div>
        </div>

                      </div>
        <p>&nbsp;</p>
                    </div>
                  </div>
                </div>
                <!--form container ends here-->
                <!--form container starts here-->
                <!--form container ends here-->
              </div>
              <!--Right side body content ends here-->
            </div>
                </div>
            <!--Footer starts from here-->
            <div class="insidefooter footer_content"><a href= "http://tyronesystems.com" style= "text-decoration:none;color:#666666;">&copy; 2013 Opslag FS2</a></div>

                <!-- Footer ends here-->
          </div>
          <!--inside body wrapper end-->
        </div>
	<!--body wrapper end-->
	</body>
	</html>"""

except Exception as e:
        disp_except.display_exception(e);
