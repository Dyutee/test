#!/usr/bin/python
import traceback, sys,include_files
sys.path.append('../modules/')
import disp_except;
try:
	import traceback, sys,include_files
	import cgitb, os, cgi, sys,opslag_info, memory_information
        cgitb.enable()

        memory_info = memory_information.mem_information()

        #-----------------------All Information Getting from Tools -----------------------
        sys.path.append('/var/nasexe/python/')
        import tools
        from tools import ipmi
        from tools import scan_remount
        from tools import shutdown
        from tools import db

        check_ha = tools.check_ha()
        #print check_ha

        cpu_new_model = scan_remount.cpu_model()
        cpu_new_model = cpu_new_model.replace('CPU', '')
        cpu_new_model = cpu_new_model.replace('Intel(R) Xeon(R) ', '')
        #cpu_new_model = cpu_new_model.split()
        #cpu_new_model = cpu_new_model[0]

        server_ip_cmd = scan_remount.server_ip()

        remote_ip_cmd = scan_remount.remote_ip()

        server_cmd = scan_remount.server_name()

        uptime_cmd = scan_remount.up_time()

        #uptime_cmd1 = scan_remount.up_time_nw()
        #print uptime_cmd1

        cpu_use_cmd = scan_remount.cpu_use()


        last_login_cmd = scan_remount.last_login()

        current_login_cmd = scan_remount.current_login()

	#-----------------SENSOR-------------------------------
        ipmi_cpu_info =ipmi.cpu_temp()
	#ipmi_cpu_info = {'CPU1':'0','CPU2':'0'}
	cpu_ipmi_value = sorted(ipmi_cpu_info.values())
	cpu_info_value=cpu_ipmi_value[1]
        ipmi_fan_info = ipmi.fan_speed()
        ipmi_power_info = ipmi.power_supply()
	
        ipmi_intrusion_info =ipmi.intrusion()
	intrusion= ipmi_intrusion_info
	#------------------End----------------------------------
	#print intrusion
        sys_temp = ipmi.system_temp()
        sys_temp = sys_temp.replace('degrees C ', '')
        #intrusion = cpu_new_intrusion
        cpu_new_intrusion = scan_remount.intrusion()
	
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
        cpu_info_command = scan_remount.cpu_info_cmd()

        #------------------End---------------------------
	#status_dump= shutdown.dump_configuration_module()
        #print status_dump
        sys_node_name = tools.get_ha_nodename()
        if(sys_node_name.strip() == "node1"):
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

	print"""
	<script>
        setTimeout(function(){
         window.location.reload(1);
        }, 50000);

        </script>
	<script src="new-tooltip/lptooltip.js"></script>
                        <link rel='stylesheet' type='text/css' href='new-tooltip/lptooltip.css' />
        <script src="new-tooltip/lptooltip.js"></script>
        <link rel='stylesheet' type='text/css' href='new-tooltip/lptooltip.css' />

	 <style>
			<!--table { margin: 1em; border-collapse: collapse; }-->
			td, th { padding: .3em; border: 1px #ccc solid; }
			td, th{ text-align:left;}
			.clr {clear: both; height: 0px; margin: 0px; padding: 0px;}
			</style>
	<div id="loader-div" style="text-align:center; display:none;" ><img style="margin-top:20%;" src="../images/ajax-loader.gif" /><br/> Loading...</div>

              <!--Right side body content starts from here-->
              <div class="rightsidecontainer" id="body-div" style="margin-top:-13px;">
                <!--tab srt-->
                <div class="searchresult-container">
                  <div class="infoheader" style = "width:733px;border:none;">
		                <div class="topinputwrap-heading"><a class="demo" href ="#"><img src ="../images/help_icon1.png" style="width: 13px;"><span class="tooltip" style="margin-top: -19px;">
		<div class="text_css">This page displays information about your system's hardware and software along with sensor information for the important components of your system.</div>"""
	if(check_ha == True):
                print""" </span></a><p class = "gap_text">Dashboard Information ("""+show_tn+""")</p>
                <span style="float:right; margin:-12px 0px 0 0;"><a onclick="return onclick_loader();" class="resource_links" href="https://"""+other_node_ip+"""/fs4/py/iframe_dashboard1.py">"""+show_on+"""</a></span>
                </div>"""

	else:
		print""" </span></a><p class = "gap_text">Dashboard</p></div>"""
	print"""

	<table style="margin: 1em; border-collapse: collapse;margin-left:1px;width:734px;">
	<tr>
	<th style="width:100px;">CPU</th><td style="width:240px;">Intel&#174 Xeon&#174"""+""" """+cpu_new_model+"""</td> <th style="width:100px;">CPU Usage</th><td style="width:240px;">""" +cpu_use_cmd+ """</td>
	</tr>

	<tr>
	<th style="width:100px;">Total Memory</th><td style="width:240px;">""" +memory_info["total"]+ """ """+""" MB</td><th style="width:100px;">Used Memory</th><td style="width:240px;">""" +memory_info["used"]+ """ """+"""MB</td>
	</tr>

	<tr>
	<th style="width:100px;">Server IP</th><td style="width:240px;">""" +server_ip_cmd+ """</td><th style="width:100px;">Remote IP</th><td style="width:240px;">""" +remote_ip_cmd+ """</td>
	</tr>

	<tr>
	<th style="width:100px;">Hostname</th><td style="width:240px;">""" + server_cmd + """</td><th style="width:100px;">Uptime</th><td style="width:240px;">""" +uptime_cmd+ """</td>
	</tr>
	<tr>
	<th style="width:100px;"><p>Current Login</p></th><td style="width:240px;"><p style="margin-top: -18px;">""" +current_login_cmd+ """</p></td><th style="width:100px;"><p>Last Login</p></th><td style="width:240px;"><p style="margin-top: -18px;">"""+last_login_cmd+"""</p></td>
	</tr>
	<tr>
	<th style="width:100px;">OS</th><td style="width:240px;">""" +opslag_info.getos('oss')+ """</td><th style="width:100px;">Version</th><td style="width:240px;"> """ + opslag_info.getos('version') + """</td>
	</tr>
	</table>
	<table  style="margin-top: -13px;border-collapse: collapse;margin-left:1px;width:734px;">
	<tr>
	<th style="width:172px;">Model</th><td style="width:240px;">""" +opslag_info.getos('model').replace('"',"")+ """</td><th style="width:100px;">Serial</th><td style="width:240px;">""" + opslag_info.getos('serial') + """</td><th style="width:100px;">Build</th><td style="width:240px;">""" + opslag_info.getos('build') + """</td>
	<!--<th>Model</th><td>""" +opslag_info.getos('model')+ """</td><th>Serial</th><td>""" + opslag_info.getos('serial') + """<th>Build</th><td>value</td></td><th>Build</th><td>""" + opslag_info.getos('build') + """</td>-->
	</tr>
	</table>
	<table style="margin-top: -13px;border-collapse: collapse;margin-left:0px;width:734px;">
	<tr>"""

	if(ipmi_cpu_info['CPU1'] != '0'):
		print """<th style="width:96.5px;"><font color="#5555;">CPU1</font>
		<td style="width:74px;color:green;"><b>"""+ipmi_cpu_info['CPU1']+"""<sup>o</sup>C</p></b></td>"""
	else:
		print """<th style="width:96.5px;"><font color="#5555;">CPU1</font></th><td style="width:74px;color:darkred;">N.A.</td>"""
		
	if(ipmi_cpu_info['CPU2'] != '0'):
		print """<th style="width:77px;"><font color="#5555;">CPU2</font>
		</th>
		<td style="width:74px;color:green;"><b>"""+ipmi_cpu_info['CPU1']+"""<sup>o</sup>C</p></b></td>"""
	else:
		print """<th style="width:76px;"><font color="#5555;">CPU2</font></th><td style="width:74px;color:darkred;">N.A.</td>"""
	if(raid_cpu_temp == ""):	
		print"""<th style="width:76px;">RAID CPU</th><td style="width:74px;color:darkred;">N.A</td>"""
	else:
		print"""<th style="width:76px;">RAID CPU</th><td style="width:74px;"><b style = "text-decoration:blink;color:green;">"""+raid_cpu_temp+"""<sup>o</sup>C</b></td>"""
	if(sys_temp == ""):
		print"""<th style="width:78px;">System</th><td style="width:74pxcolor:darkred;">N.A</td>"""
	else:
		print"""<th style="width:78px;">System</th><td style="width:74px;"><b style = "text-decoration:blink;color:green;margin-left:-2px;">"""+sys_temp+"""<sup>o</sup>C</b></td>"""
	print"""
		
	
	</tr>
	</table>
	<table style="margin-top: -13px;margin-left:0px;width:734px">
	<tr>"""
	for keys in ipmi_power_info:
		pw_supply =ipmi_power_info[keys]
			
		print
	print"""
	<th style="width:100px;">PS1</th><td style="width:119px;">"""+ipmi_power_info[keys]+"""</td><th style="width:100.5px;">PS2</th><td style="width:121px;">"""+ipmi_power_info[keys]+"""</td><th style="width:100px;">Intrusion</th><td style="width:121px;">"""+intrusion+"""<button class="buttonClass" type="submit" style="margin-left:29px; width:45px; height: 27px;" name = 'set_p'  id = 'id_create_but'  value = 'set_p'>Clear</button></td>
	</tr>
	</table>
	<table style="margin-top: -13px;margin-left:0px;width:734px;">
	<tr>
	<th style="width:103.5px;">FAN (RPM)</th>
			<td>
	"""
	i = 1
        j =1
        for keys in ipmi_fan_info:
        	ipmi_fan_val = str(ipmi_fan_info[keys]);
                fan_icon = "<img src='../images/cpu_fan_nw.gif' >"
                fan1_icon = "<img src='../images/cpu_fan6.jpeg'>"
                fan_speed = ipmi_fan_val;
                if(fan_speed == '0'):
                        fan_speed = 'Not-detected'
		

			print"""
			<span style = "color:green;cursor:pointer;" class="btn btnPluginDownload lpTooltip lpRight example bg" data-tooltip-text='"""+keys+""":"""+fan_speed+"""'><img class="turbine" width="54" height="auto" id="""+str(i)+""" src="../images/fan.png"></span>

			<script>
                        $('#"""+str(j)+"""').propeller({inertia: 1, speed:"""+fan_speed+"""}); 
                        </script>"""

		else:
			print"""
			 <span style = "color:green;cursor:pointer;" class="btn btnPluginDownload lpTooltip lpRight example bg" data-tooltip-text='"""+keys+""":"""+fan_speed+"""'><img class="turbine" width="54" height="auto" id="""+str(i)+""" src="../images/fan.png"></span>

                        <script>
                        $('#"""+str(j)+"""').propeller({inertia: 1, speed:"""+fan_speed+"""}); 
                        </script>"""
		i = i+1
                j = j+1
	print"""
	</td>
	</tr>
	</table>
	</div>       
             </div>
                </div>
	"""
except Exception as e:
        disp_except.display_exception(e);
