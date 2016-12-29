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
        ipmi_cpu_info =ipmi.cpu_temp()

        ipmi_fan_info = ipmi.fan_speed()
	print ipmi_fan_info
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
	      <!--Right side body content starts from here-->
		
		<!--<script src="new-tooltip/jquery.js"></script>
                        <script src="new-tooltip/lptooltip.js"></script>
                        <link rel='stylesheet' type='text/css' href='new-tooltip/lptooltip.css' />-->
		<script src="new-tooltip/jquery.js"></script>
        <script src="new-tooltip/lptooltip.js"></script>
        <link rel='stylesheet' type='text/css' href='new-tooltip/lptooltip.css' />
		
		<head>
	    <title>Set tooltip HTML content</title>
	    <script src="tooltip/themes/1/tooltip.js" type="text/javascript"></script>
	    <link href="tooltip/themes/1/tooltip.css" rel="stylesheet" type="text/css" />
	    <style type="text/css">
		h3 { font: normal 24px/36px Arial;}
		h4 { font-family: "Trebuchet MS", Verdana; }
		#span4 img {cursor:pointer;margin:20px;}
	    </style>
	    <script type="text/javascript">
		//for tooltip.ajax demo
		var myAjaxSetting = {
		    context: { index: -1 },
		    success: myCallback,
		    responseType: "xml"
		};
		function myCallback(response, context) {
		    var x = response.documentElement.getElementsByTagName("cd")[context.index];
		    var title = x.getElementsByTagName("title")[0].childNodes[0].nodeValue;
		    var image = "<img src='#" + context.index + "' style='float:right;margin-left:12px;width:75px;height:75px;' />";
		    var image1  = "<img src = '#'" + content.index + "' style = 'float:right;margin-left:12px;widh:75px;height:75px;' />";
		    return "<div style='width:220px;'>" + image + "<b>" + title + "</b></div>";
		}        
	    </script>
	</head>

	      <div class="rightsidecontainer">
		<!--tab srt-->
		<div class="searchresult-container">
		  <div class="infoheader">
		<div class="topinputwrap-heading">Sensor Information of """+show_tn+"""
                <span style="float:right; margin:0 0px 0 0;"><a class="resource_links" href="https://"""+other_node_ip+"""/fs4/py/iframe_sensor_info.py">"""+show_on+"""</a></span>
                </div>
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
                        print"""<div class="formleftside-content"><img src='../images/cpu_img1.png'>:<b>&nbsp;-</b></span></div><br/><br/><br/><br/>"""
		else:

                	print"""<div class="formleftside-content"><img src='../images/cpu_img1.png'>:<b style = "text-decoration:blink;color:green;">"""+ cpu_info_value + """<sup>o</sup>C</b></div><br/><br/><br/>"""
	print"""</div>

		<div class="inputwrap">
                    <div class="formleftside-content">Fan Speed(RPM):</div>
                    <div class="formrightside-content"style="margin-left:-6%;">"""
	i =1
	for keys in ipmi_fan_info:
                ipmi_fan_val = str(ipmi_fan_info[keys]);
                fan_icon = "<img src='../images/cpu_fan_nw.gif' >"
                fan1_icon = "<img src='../images/cpu_fan6.jpeg'>"
                fan_speed = ipmi_fan_val;
                if(fan_speed == '0'):
			#print""" """+fan1_icon+"""<span>"""+fan_speed+"""</span>"""
			#print"""<span class="tooltip" onmouseover="tooltip.pop(this, '#demo2_tip"""+str(i)+"""')">"""+fan1_icon+"""</span>
			 #<div style="display:none;">
            		#<div id='demo2_tip"""+str(i)+"""'>
                 	#<strong>"""+keys+""":"""+fan_speed+"""</strong>     
        		#</div>
    			#</div>"""
			print """<span style = "color:green;" class="btn btnPluginDownload lpTooltip lpRight" data-tooltip-text="""+keys+""":"""+fan_speed+""">"""+fan1_icon+"""</span>"""

                else:
                        #print""" """+fan_icon+"""<span style="color:green;">"""+fan_speed+"""</span>"""
			#print """'demo2_tip"""+str(i)+"""'"""
			#print"""<span class="tooltip" onmouseover="tooltip.pop(this, '#demo2_tip"""+str(i)+"""')">"""+fan_icon+"""&nbsp;&nbsp;</span>
			 #<div style="display:none;">
            		#<div id='demo2_tip"""+str(i)+"""'>
                 	#<strong>"""+keys+""":"""+fan_speed+"""</strong>     
        		#</div>
    			#</div>"""
			print fan_speed
			
			print """<span style = "color:green;" class="btn btnPluginDownload lpTooltip lpRight" data-tooltip-text="""+keys+""": """+fan_speed+""">"""+fan_icon+"""</span>"""
		i = i+1
			
	print"""</div>
                  </div>
		 <div class="inputwrap">
                    <div class="formleftside-content">RAID CPU:</div>"""
        if(raid_cpu_temp == ''):
                    print"""<div class="formrightside-content" style="margin-left:-12%;">-</div>"""
        else:
                print"""<div class="formrightside-content" style="margin-left:-12%;"><b style = "text-decoration:blink;color:green;">"""+raid_cpu_temp+"""<sup>o</sup>C</b></div>"""
        print"""                </div>

                <div class="inputwrap">
                    <div class="formleftside-content">RAID Controller:</div>"""
        if(raid_controller_temp == ''):
                print"""<div class="formrightside-content" style="margin-left:-7%;">-</div>"""
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
