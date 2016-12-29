#!/usr/bin/python
import cgitb, sys, common_methods, include_files
cgitb.enable()
sys.path.append('../modules/')
import disp_except;
try:
	import cgitb, os, cgi, sys, commands, opslag_info, system_info, memory_information
        cgitb.enable()

        memory_info = memory_information.mem_information()

        #-----------------------All Information Getting from Tools -----------------------
        sys.path.append('/var/nasexe/python/')
	import tools
        from tools import ipmi
        from tools import scan_remount
	from tools import db

	check_ha = tools.check_ha()
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

	print
	print """
		<div id="loader-div" style="text-align:center; display:none;" ><img style="margin-top:20%;" src="../images/ajax-loader.gif" /><br/> Loading...</div>
	      <!--Right side body content starts from here-->
		
		<!--<script src="new-tooltip/jquery.js"></script>
                        <script src="new-tooltip/lptooltip.js"></script>
                        <link rel='stylesheet' type='text/css' href='new-tooltip/lptooltip.css' />-->
        <script src="new-tooltip/lptooltip.js"></script>
        <link rel='stylesheet' type='text/css' href='new-tooltip/lptooltip.css' />
		
		
	      <div class="rightsidecontainer" id="body-div">
		<!--tab srt-->
		<div class="searchresult-container">
		  <div class="infoheader">
		<div class="topinputwrap-heading"><a class="demo" href ="#"><img src ="../images/help_icon1.png" style="width: 13px;"><span class="tooltip" >


		 <table border="0">
        <tr>
        <td style="font-size: medium;text-align:start;">Sensor Information:</td>
        
        </tr>

        <tr>     
        <td class="text_css">In this Page Displays the information of Cpu temperature , Fan Information,Raid Information,Power supply and Intrusion Information.</td>
        </tr>
        </table>"""
	if(check_ha == True):

		print"""</span></a>
	Sensor Information of """+show_tn+"""
                <span style="float:right; margin:5px 0px 0 0;"><a onclick="return onclick_loader();" class="resource_links" href="https://"""+other_node_ip+"""/fs4/py/iframe_sensor_info.py">"""+show_on+"""</a></span>
                </div>"""
	else:
		print"""</span></a>Sensor Information </div>"""
	print """
		    <!--<div id="tabs">-->
		      <!--<ul>
			<li><a href="#tabs-1">Sensor Info</a></li>
		      </ul>-->
		      <div id="tabs-1">

		<!--form container starts here-->
		<div class="iframe-form-container">
		  <div class="inputwrap">"""
	for cpu_info_value in ipmi_cpu_info.values():
                cpu_info_value = str(cpu_info_value);
                if(cpu_info_value == '0'):
                        print"""<div class="formleftside-content"><img src='../images/cpu_img1.png'>:<b>&nbsp;&nbsp;-</b></span></div><br/><br/><br/><br/>"""
		else:

                	print"""<div class="formleftside-content"><img src='../images/cpu_img1.png'>:<b style = "text-decoration:blink;color:green;">&nbsp;&nbsp;"""+ cpu_info_value + """<sup>o</sup>C</b></div><br/><br/><br/>"""
	print"""</div>

		<div class="inputwrap">
                    <div class="formleftside-content" style="margin-top:10px;">Fan Speed (RPM):</div>
                    <div class="formrightside-content" >
			<div class="examples_wrapper">
			<table>
		
			"""
	i = 1
	j = 1
	for keys in ipmi_fan_info:
                ipmi_fan_val = str(ipmi_fan_info[keys]);
                fan_icon = "<img src='../images/cpu_fan_nw.gif' >"
                fan1_icon = "<img src='../images/cpu_fan6.jpeg'>"
                fan_speed = ipmi_fan_val;
                if(fan_speed == '0'):
			print"""
			
            		<span  style = "color:green;cursor:pointer;" class="btn btnPluginDownload lpTooltip lpRight example bg" data-tooltip-text='"""+keys+""":"""+fan_speed+"""'>
			
           		<img class="turbine" width="54" height="auto" id="""+str(i)+""" src="../images/fan.png"></span>
			<script>
                        $('#"""+str(j)+"""').propeller({inertia: 1, speed:"""+fan_speed+"""}); 
                        </script>
		""" 
		#	print """<span style = "color:green;cursor:pointer;" class="btn btnPluginDownload lpTooltip lpRight" data-tooltip-text='"""+keys+""":"""+fan_speed+"""'>"""+fan1_icon+"""</span>"""

                else:
			print"""
			
            		<span  style = "color:green;cursor:pointer;" class="btn btnPluginDownload lpTooltip lpRight example bg" data-tooltip-text='"""+keys+""":"""+fan_speed+"""'>
                        <img class="turbine" width="54" height="auto"  id="""+str(i)+""" src="../images/fan.png"></span>

			<script>
    			$('#"""+str(j)+"""').propeller({inertia: 1, speed:"""+fan_speed+"""}); 
			</script>
			"""
			#print """<span style = "color:green;cursor:pointer;" class="btn btnPluginDownload lpTooltip lpRight" data-tooltip-text='"""+keys+""": """+str(fan_speed)+"""'>"""+fan_icon+"""</span>"""
		i = i+1		
		j = j+1
	print"""</table></div></div>
                  </div>
		 <div class="inputwrap">
                    <div class="formleftside-content">RAID CPU Temperature:</div>"""
        if(raid_cpu_temp == ''):
        	print"""<div class="formrightside-content" style="margin-left:0%;">-</div>"""
        else:
                print"""<div class="formrightside-content" style="margin-left:0%;"><b style = "text-decoration:blink;color:green;">"""+raid_cpu_temp+"""<sup>o</sup>C</b></div>"""
        print"""                </div>

                <div class="inputwrap">
                    <div class="formleftside-content" style="width:190px;">RAID Controller Temperature:</div>"""
        if(raid_controller_temp == ''):
                print"""<div class="formrightside-content" style="margin-left:-0%;">-</div>"""
        else:
                print"""<div class="formrightside-content" style="margin-left:0%;"><b style = "text-decoration:blink;color:green;">"""+raid_controller_temp+"""<sup>o</sup>C</b></div>"""
        print"""                        </div>"""

        print"""                <div class="inputwrap">"""
        for keys in ipmi_power_info:
                #print keys + ':' + str(ipmi_power_info[keys]);
                print"""<div class="formleftside-content">"""+keys+""":"""+ipmi_power_info[keys]+"""</div><br/><br/>"""
	print"""
                  </div>

                  <div class="inputwrap">
                    <div class="formleftside-content">Intrusion:</div>
                    <div class="formrightside-content" style="margin-top: 4px; margin-left: -99px;">""" +intrusion+ """</div>
                        </div>

		  </div>
		</div>
		<!--form container ends here-->
		<p>&nbsp;</p>
		      </div>
		    </div>
		  </div>
		</div>
	"""
except Exception as e:
        disp_except.display_exception(e);
