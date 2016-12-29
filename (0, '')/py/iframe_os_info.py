#!/usr/bin/python

import traceback, sys, include_files
sys.path.append('../modules/')
import disp_except;

try:
	import cgitb, os, cgi, sys,opslag_info, memory_information
	cgitb.enable()

	memory_info = memory_information.mem_information()
	
	#-----------------------All Information Getting from Tools -----------------------
        sys.path.append('/var/nasexe/python/')
	import tools
        from tools import scan_remount
        from tools import shutdown
	from tools import db

	check_ha = tools.check_ha()
	#print check_ha

        cpu_new_model = scan_remount.cpu_model()

        server_ip_cmd = scan_remount.server_ip()

        remote_ip_cmd = scan_remount.remote_ip()

	server_cmd = scan_remount.server_name()

	uptime_cmd = scan_remount.up_time()

	cpu_use_cmd = scan_remount.cpu_use()


	last_login_cmd = scan_remount.last_login()

	current_login_cmd = scan_remount.current_login()
	#status_dump= shutdown.dump_configuration_module()
        #print status_dump
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

	print"""
		<div id="loader-div" style="text-align:center; display:none;" ><img style="margin-top:20%;" src="../images/ajax-loader.gif" /><br/> Loading...</div>

	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer" style="width:730px;" id="body-div">
		<!--tab srt-->
		<div class="searchresult-container">
		  <div class="infoheader">
		    <!--<div id="tabs">-->
		<div class="topinputwrap-heading"><a class="demo" href ="#"><img src ="../images/help_icon1.png" style="width: 13px;"><span class="tooltip" >

		<table border="0">
        <tr>
        <td style="font-size: medium;text-align:start;">OS Information:<!--<p class= "text_css">Display the Information Heloo sanjeev sunny rahul</p>--></td>
	
        <!--<td>Displays the information related to host IP and host name and system up time.</td>-->
        </tr>
	<tr>
	
        <!--<td class="text_css">Displays the information related to host IP and host name and system up time.Displays the information about the CPU, like CPU temperature and CPU usage.Shows the disk related information like, used space on the disk and available space.</td>-->
	
        <td class="text_css">In this Page Displays the information of Cpu model number,Server Ip, Remote Ip,Hostname,System Up and down time,Current and Last Login time.Memory Information of this system.Cpu usage by the System.Os Information of the system.system version, Model and serial Number.</td>
	</tr>
	</table>"""
	if(check_ha == True):
		
		print""" </span></a>OS Information of """+show_tn+"""
		<span style="float:right; margin:5px 0px 0 0;"><a onclick="return onclick_loader();" class="resource_links" href="https://"""+other_node_ip+"""/fs4/py/iframe_os_info.py">"""+show_on+"""</a></span>
		</div>"""
	else:
		 print""" </span></a>OS Information</div>"""
	print"""
		      <!--<ul>
			<li><a href="#tabs-1">OS Information</a></li>
		      </ul>-->
			
			<div id="tabs-1">
			<!--<div class="form-container">-->
			<div class="inputwrap">
                    <div class="formleftside-content">CPU:</div>
                    <div class="formrightside-content"><img src='../images/cpu_img1.png'></div><div class="formrightside-content" style="margin-top: -4%; margin-left: 34%;">"""+cpu_new_model+"""</div>
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
                    <div class="formleftside-content">Hostname:</div>
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
                    <div class="formleftside-content">Memory (MB):</div>
                    <div class="formrightside-content">""" +memory_info["total"]+ """</div>
                  </div>
                
                <div class="inputwrap">
                    <div class="formleftside-content">Used Memory (MB):</div>
                    <div class="formrightside-content">""" +memory_info["used"]+ """</div>
                  </div>

		  <div class="altinputwrap">
                    <div class="formleftside-content">Free Memory (MB):</div>
                    <div class="formrightside-content">""" +memory_info["free"]+ """</div>
                  </div>
                 <div class="inputwrap">
                    <div class="formleftside-content">CPU usage:</div>
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
			
                  </div>
                </div>
	"""

except Exception as e:
        disp_except.display_exception(e);
