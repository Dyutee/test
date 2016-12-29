#!/usr/bin/python

import cgitb, sys, include_files, cgi
cgitb.enable()
form = cgi.FieldStorage()
sys.path.append('../modules/')
import disp_except;

try:
	###########################################
        ############# import modules ##############
        ###########################################
	import commands, os, cgi, common_methods, string
	sys.path.append('/var/nasexe/')
	import net_manage_newkernel as net_manage_bond
	sys.path.append('/var/nasexe/python/')
	import net_manage_newkernel
	import tools
	from tools import db
	from tools import blink_interface

	###########################################
        ############## Check for HA ###############
        ###########################################
	check_ha = tools.check_ha()

	log_array = []
	log_file = common_methods.log_file
	logstring = ''

	status=net_manage_newkernel.get_iface_config('bond0',debug='no')
	##################################################
        ############# Blink Interface Start ##############
        ##################################################
	if(form.getvalue("blink_interface")):
		get_hid_eth_val = form.getvalue("hid_eth_val")
		blink_interface_cmd = blink_interface.blink(get_hid_eth_val)
	##################################################
        ############# Blink Interface End ################
        ##################################################

	###############################################
        ############# Set Hostname Start ##############
        ###############################################
	if(form.getvalue("submit_hostname")):
		get_hostname = form.getvalue("hostname")
		get_ip_address = form.getvalue("select_primary_ip")
		change_hostname = net_manage_bond.set_hostname(get_hostname, get_ip_address)
		if(change_hostname["id"]==0):
			print"<div id = 'id_trace'>"
			print change_hostname["desc"]
			print "</div>"
		else:
			print"""<div id = 'id_trace_err'>"""
			print change_hostname["desc"]
			print "</div>"

		ss = change_hostname
		logstring = str(common_methods.now) + '<<>>From: ' + common_methods.remote_ip + '<<>>' + str(ss);
		log_array.append(logstring);
		common_methods.append_file(log_file, log_array);
	###############################################
        ############## Set Hostname End ###############
        ###############################################

	gethostname = net_manage_bond.get_hostname()
	ss = gethostname
	logstring = str(common_methods.now) + '<<>>From: ' + common_methods.remote_ip + '<<>>' + str(ss);
	log_array.append(logstring);

	getall_ifaces=net_manage_bond.get_all_ifaces_config()
	get_all_ip = getall_ifaces["all_conf"]

	ss = getall_ifaces
	logstring = str(common_methods.now) + '<<>>From: ' + common_methods.remote_ip + '<<>>' + str(ss);
	log_array.append(logstring);
	common_methods.append_file(log_file, log_array);

	############################################
	########## Update ethernet Start ###########
	############################################
	if(form.getvalue("update_ethernet")):
		get_hid_iface_val = form.getvalue("hid_iface_val")
		get_up_ip = form.getvalue("ipaddress")
		get_up_netmask = form.getvalue("netmask")
		get_up_gateway = form.getvalue("gateway")
		get_up_default_gateway = form.getvalue("default_gateway")

		if(get_up_gateway == None):
			get_up_gateway =''

		if(get_up_default_gateway == "on"):
			get_up_default_gateway = "yes"
		else:
			get_up_default_gateway = "no"

		if((get_up_ip != None) and (get_up_ip != '') and (get_up_netmask != None) and (get_up_netmask != '')):
			slave_ifaces = net_manage_bond.get_slave_ifaces(get_hid_iface_val)
			slave_ifaces = slave_ifaces["slave_iface_list"]

			dict_inp={'iface':get_hid_iface_val,
			'address':get_up_ip,
			'netmask':get_up_netmask,
			'gateway':get_up_gateway,
			'debug':'no',
			'is_def_gateway':get_up_default_gateway,
			'slave_ifaces':slave_ifaces
			}

			configure_iface_cmd = net_manage_bond.configure_iface(dict_inp,want_to_set_hostname="no",validate_input="yes")
			if(configure_iface_cmd["id"] == 0):
				print "<div id = 'id_trace'>"
				print configure_iface_cmd["desc"]
				print "</div>"
			else:
				print "<div id = 'id_trace_err'>"
				print configure_iface_cmd["desc"]
				print "</div>"

		else:
			print"<div id = 'id_trace_err'>"
			print "Cannot modify interface. IP and Netmask are Mandatory!"
			print "</div>"
	############################################
	############ Update ethernet End ###########
	############################################
		
	############################################
	######## Unconfigure ethernet Start#########
	############################################
	if(form.getvalue("unconfigure_ethernet")):
		get_hid_iface_val = form.getvalue("hid_iface_val")
		unconfigure_iface_cmd = net_manage_bond.unconfigure_iface(get_hid_iface_val,debug="no",want_to_set_hostname="no",validate_input="yes")
		if(unconfigure_iface_cmd["id"] == 0):
			print"<div id = 'id_trace'>"
			print unconfigure_iface_cmd["desc"]
			print "</div>"
		else:
			print"<div id = 'id_trace_err'>"
			print unconfigure_iface_cmd["desc"]
			print "</div>"
	############################################
	######### Unconfigure ethernet End #########
	############################################

	############################################
	############ Delete Bond Start #############
	############################################
	if(form.getvalue("delete_bond_but")):
		bond_to_delete = form.getvalue("hid_bond_to_delete")
		delete_bond_cmd = net_manage_newkernel.delete_bond_iface(bond_to_delete)
		if(delete_bond_cmd["id"] == 0):
			print"<div id = 'id_trace'>"
			print delete_bond_cmd["desc"]
			print "</div>"
		else:
			print"<div id = 'id_trace_err'>"
			print delete_bond_cmd["desc"]
			print "</div>"
	############################################
	############# Delete Bond End ##############
	############################################

	############################################
	############ Update Bond Start #############
	############################################
	if(form.getvalue("update_bond_but")):
		hid_radio_no = form.getvalue("hid_radio_no")
		get_bond_name = form.getvalue("bond_name")
		get_ifaces = form.getvalue("ethernets")
		get_bond_type = form.getvalue("bond_type"+hid_radio_no)
		get_bond_ip = form.getvalue("bond_ip")
		get_bond_netmask = form.getvalue("bond_netmask")
		get_bond_gateway = form.getvalue("bond_gateway")
		get_bond_ip_hid = form.getvalue("bond_ip_hid")
		get_bond_netmask_hid = form.getvalue("bond_netmask_hid")
		get_bond_gateway_hid = form.getvalue("bond_gateway_hid")
		get_bond_is_default_gateway = form.getvalue("bond_is_default_gateway")

		if((get_ifaces != None) and (get_ifaces != '') and (get_bond_name != None) and (get_bond_name != '')):	
			if(isinstance(get_ifaces, str) == True):
				get_ifaces = [get_ifaces]

			get_iface_for_bond = net_manage_newkernel.get_iface_config(get_ifaces[0],debug="no")	
			get_conf_dict = get_iface_for_bond["conf"]

			if((get_bond_ip == None) or (get_bond_ip == '')):
				get_bond_ip = get_bond_ip_hid
				if((get_bond_ip == '') or (get_bond_ip == None)):
					get_bond_ip = "192.168."+str(get_ifaces[0])[3:]+".1"
			
			if((get_bond_netmask == None) or (get_bond_netmask == '')):
				get_bond_netmask = get_bond_netmask_hid
				if((get_bond_netmask == '') or (get_bond_netmask == None)):
					get_bond_netmask = "255.255.255.0"

			if((get_bond_gateway == None) or (get_bond_gateway == '')):
				get_bond_gateway = get_bond_gateway_hid
				if(get_bond_gateway == None):
					get_bond_gateway = ''

			if(get_bond_is_default_gateway == "on"):
				get_bond_is_default_gateway = "yes"
			else:
				get_bond_is_default_gateway = "no"


			bond_info={'name':get_bond_name,
			'type':get_bond_type,
			'slave_iface_list':get_ifaces,
			'address':get_bond_ip,
			'netmask':get_bond_netmask,
			'gateway':get_bond_gateway,
			'is_def_gateway':get_bond_is_default_gateway
			}

			modify_bond_cmd = net_manage_newkernel.modify_bond_iface(bond_info,debug="no")
			if(modify_bond_cmd["id"] == 0):
				print"<div id = 'id_trace'>"
				print modify_bond_cmd["desc"]
				print "</div>"
			else:
				print "<div id='id_trace_err'>"
				print modify_bond_cmd["desc"]
				print "</div>"

		else:
			print"<div id = 'id_trace_err'>"
			print "Bond cannot be created. Bond name and ethernet devices are mandatory!"
			print "</div>"
	############################################
	############# Update Bond End ##############
	############################################

	############################################
	############ Create Bond Start #############
	############################################
	if(form.getvalue("create_bond_but")):
		get_bond_name = form.getvalue("bond_name")
		get_ifaces = form.getvalue("ethernets")
		get_bond_type = form.getvalue("bond_type")
		get_bond_ip = form.getvalue("bond_ip")
		get_bond_netmask = form.getvalue("bond_netmask")
		get_bond_gateway = form.getvalue("bond_gateway")
		get_bond_is_default_gateway = form.getvalue("bond_is_default_gateway")

		if((get_ifaces != None) and (get_ifaces != '') and (get_bond_name != None) and (get_bond_name != '')):
			if(isinstance(get_ifaces, str) == True):
				get_ifaces = [get_ifaces]

			get_iface_for_bond = net_manage_newkernel.get_iface_config(get_ifaces[0],debug="no")	
			get_conf_dict = get_iface_for_bond["conf"]

			if((get_bond_ip == None) or (get_bond_ip == '')):
				get_bond_ip = get_conf_dict["address"]
				if(get_bond_ip == ''):
					get_bond_ip = "192.168."+str(get_ifaces[0])[3:]+".1"
			
			if((get_bond_netmask == None) or (get_bond_netmask == '')):
				get_bond_netmask = get_conf_dict["netmask"]
				if(get_bond_netmask == ''):
					get_bond_netmask = "255.255.255.0"

			if((get_bond_gateway == None) or (get_bond_gateway == '')):
				get_bond_gateway = ''

			if(get_bond_is_default_gateway == "on"):
				get_bond_is_default_gateway = "yes"
			else:
				get_bond_is_default_gateway = "no"


			bond_info={'name':get_bond_name,
			'type':get_bond_type,
			'slave_iface_list':get_ifaces,
			'address':get_bond_ip,
			'netmask':get_bond_netmask,
			'gateway':get_bond_gateway,
			'is_def_gateway':get_bond_is_default_gateway
			}

			create_bond_cmd = net_manage_newkernel.create_bond_iface(bond_info,debug="no")
			if(create_bond_cmd["id"] == 0):
				print"<div id = 'id_trace'>"
				print create_bond_cmd["desc"]
				print "</div>"
			else:
				print"<div id = 'id_trace_err'>"
				print create_bond_cmd["desc"]
				print "</div>"
				
		else:
			print"<div id = 'id_trace_err'>"
			print "Bond cannot be created. Bond name and ethernet devices are mandatory!"
			print "</div>"
	############################################
	############# Create Bond End ##############
	############################################


	get_all_bonds = net_manage_newkernel.get_all_bond_ifaces(debug='no')
	configurable_ifaces = net_manage_newkernel.get_all_configurable_ifaces(exclude_bond="yes")

	############################################
	######### Network Settings Start ###########
	############################################
	get_all_iface = net_manage_bond.get_all_ifaces_config()
	if(get_all_iface["id"]==0):
		iface_info = get_all_iface["all_conf"]
		array_len = len(iface_info)

	elif(get_all_iface["id"]==2):
		iface_info = [{'status': '', 'iface': '', 'netmask': '', 'address': '', 'model': '', 'gateway': ''}]
	############################################
	######### Network Settings Start ###########
	############################################

	############################################
	######### DNS Configuration Start ##########
	############################################
	image_icon = common_methods.getimageicon();
	dns_conf_file="/etc/resolv.conf"
	#Entering values into resolv.conf file "START"
	if(form.getvalue("submit")):
		new_primary_dns = form.getvalue("pdns")
		new_secondary_dns = form.getvalue("sdns")

		if((new_primary_dns==None) and (new_secondary_dns==None)):
			commands.getstatusoutput("sudo chmod 777 "+dns_conf_file)
			dns_file_submit = open(dns_conf_file, 'w')
			dns_file_submit.write('')
			dns_file_submit.close()
			commands.getstatusoutput("sudo chmod 755 "+dns_conf_file)

		elif((new_primary_dns!=None) and (new_secondary_dns==None)):
			primary_dns_string = "nameserver" + " " + new_primary_dns
			commands.getstatusoutput("sudo chmod 777 "+dns_conf_file)
			dns_file_submit = open(dns_conf_file, 'w')
			dns_file_submit.write(primary_dns_string+"\n")
			dns_file_submit.close()
			commands.getstatusoutput("sudo chmod 755 "+dns_conf_file)

		elif((new_primary_dns!=None) and (new_secondary_dns!=None)):
			primary_dns_string = "nameserver" + " " + new_primary_dns
			secondary_dns_string = "nameserver"+ " " + new_secondary_dns
			commands.getstatusoutput("sudo chmod 777 "+dns_conf_file)
			dns_file_submit = open(dns_conf_file, 'w')
			dns_file_submit.write(primary_dns_string+"\n")
			dns_file_submit.write(secondary_dns_string)
			dns_file_submit.close()
			commands.getstatusoutput("sudo chmod 755 "+dns_conf_file)

	#Entering values into resolv.conf file "END"

	#Fetch Primary and Secondary DNS values from resolv.conf file "START"

	dns_file = open('/etc/resolv.conf', 'r')
	lines = dns_file.readlines()
	count_lines=0
	for line in lines:
		count_lines += 1

	if(count_lines==2):
		new_string=''
		for line in lines:
			split_dns_lines = string.split(line)
			new_string = new_string + split_dns_lines[1]+" "

		split_new_string = string.split(new_string)
		split_new_string1 = split_new_string[0]
		split_new_string2 = split_new_string[1]

	elif(count_lines==1):
		for line in lines:
			split_dns_lines = string.split(line)

		split_new_string = split_dns_lines[1]
		split_new_string1 = split_new_string
		split_new_string2 = ''

	elif(count_lines==0):
		split_new_string1 = ''
		split_new_string2 = ''
	else:
		new_string=''
		for line in lines:
			if(line != "\n"):
				split_dns_lines = string.split(line)
				new_string = new_string + split_dns_lines[1]+" "

		split_new_string = string.split(new_string)
		split_new_string1 = split_new_string[0]
		split_new_string2 = split_new_string[1]

	dns_file.close()
	############################################
	########## DNS Configuration End ###########
	############################################

	############################################
	########## Ethernet Teaming Start ##########
	############################################
	# Get all bond ifaces   
	bond_created=net_manage_bond.get_all_bond_ifaces()
	# Get all configurable ifaces
	all_confi_ifaces=net_manage_bond.get_all_configurable_ifaces(exclude_bond="no")
	############################################
	########### Ethernet Teaming End ###########
	############################################
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
	<!-- ############## Fancybox CSS and JAVASCRIPT Start ############## -->

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
				window.location.reload();
			},
			helpers: { 
				overlay :{closeClick: false} // prevents closing when clicking OUTSIDE fancybox 
			}
			
		});

	});
	</script>

	<!-- ############## Fancybox CSS and JAVASCRIPT End ############## -->

		<div id="loader-div" style="text-align:center; display:none;" ><img style="margin-top:20%;" src="../images/ajax-loader.gif" /><br/> Loading...</div>
	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer" id="body-div">
		<!--tab srt-->
		<div class="searchresult-container">
		<div style="margin:0 0 0px 0;" class="topinputwrap-heading"><a class="demo" href ="#"><img src ="../images/help_icon1.png" style ="width:13px;"><span class="tooltip" >
                 <table border="0">
        <tr>     
        <td class="text_css">This page allows you to configure different network related settings of your system.</td>
        </tr>
        </table>"""
	if(check_ha == True):
		print"""
		</span></a> Network Settings ("""+show_tn+""")
                <span style="float:right; margin:0;"><a onclick="return onclick_loader();" class="resource_links" href="https://"""+other_node_ip+"""/fs4/py/iframe_network_settings_new.py">"""+show_on+"""</a></span>
                </div>"""
	else:
		print"""
                </span></a>Network Settings </div>"""
	print"""
		  <div class="infoheader">
		    <div id="tabs">
		      <ul>
			<li><a href="#tabs-1">Hostname</a></li>
			<li><a href="#tabs-2">Network</a></li>
			<li><a href="#tabs-3">DNS</a></li>
			<li><a href="#tabs-4">Aggregation</a></li>
		      </ul>
		      <div id="tabs-1">

		<!--form container starts here-->
		<div class="form-container">
		<form name = 'server_change' method = 'POST'>
		  <div class="topinputwrap-heading"> Change Hostname </div>
		  <div class="inputwrap">
			<table width="100%" style="padding:0 0 0 10px;">
			<tr>
			<td style=" color:#666666;">Hostname</td>
			<td><input class = 'textbox' type = 'text' name = 'hostname' value =""" + gethostname["hostname"] + """></td>
			</tr>
			<tr>
			<td style=" color:#666666;">Select Primary IP</td>
			<td>
			<div class="styled-select2" style="width:170px;">
			<select name="select_primary_ip" style="width:183px;">
			"""
	for ip in get_all_ip:
                if(ip["address"]!=''):
                        print """<option value="""+ip["address"]+""" """
                        if(gethostname["primary_ip"] == ip["address"]):
                                print "selected"
                        print """>"""+ip["address"]+"""</option>"""

	print """</select></div>

			</td>
			</tr>

			<tr>
			<td></td>
			<td>

			<button class="buttonClass" type = 'submit'  name="submit_hostname" value="Apply" onclick = "return validate_form();" style="float:left; margin:0 0 0 200px;">Apply</button>
			</td>
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
		<div class="form-container">
		  <div class="inputwrap">
		    <div class="formrightside-content">



	<nav id="menu_interface">

	<ul>"""

	i=1
	s=1
	for x in iface_info:

		print """<li onclick="return folder_click("""+str(i)+""", """+str(array_len)+""", """+str(s)+""");"><a>"""+x["iface"]+"""</a>

		<style>
		#popUpDiv1"""+str(i)+""" {position: fixed; background-color: #fff; min-width: 400px; z-index: 9002; padding: 5px;}
		#popUpDiv1"""+str(i)+""" h5{width:100%; font-size:15px; color:#0070bd; text-align:center; font-weight:bold;}
		#popUpDiv1"""+str(i)+""" span{ color:#FFFFFF; background-color:#0070bd; padding:1px 3px 0 3px; float:right;}

		#popUpDiv2"""+str(i)+""" {position: fixed; background-color: #fff; min-width: 400px; z-index: 9002; padding: 5px;}
		#popUpDiv2"""+str(i)+""" h5{width:100%; font-size:15px; color:#0070bd; text-align:center; font-weight:bold;}
		#popUpDiv2"""+str(i)+""" span{ color:#FFFFFF; background-color:#0070bd; padding:1px 3px 0 3px; float:right;}

		#popUpDiv3"""+str(i)+""" {position: fixed; background-color: #fff; min-width: 400px; z-index: 9002; padding: 5px;}
		#popUpDiv3"""+str(i)+""" h5{width:100%; font-size:15px; color:#0070bd; text-align:center; font-weight:bold;}
		#popUpDiv3"""+str(i)+""" span{ color:#FFFFFF; background-color:#0070bd; padding:1px 3px 0 3px; float:right;}

		#popUpDiv4"""+str(i)+""" {position: fixed; background-color: #fff; min-width: 400px; z-index: 9002; padding: 5px;}
		#popUpDiv4"""+str(i)+""" h5{width:100%; font-size:15px; color:#0070bd; text-align:center; font-weight:bold;}
		#popUpDiv4"""+str(i)+""" span{ color:#FFFFFF; background-color:#0070bd; padding:1px 3px 0 3px; float:right;}

		#popUpDiv5"""+str(i)+""" {position: fixed; background-color: #fff; min-width: 400px; z-index: 9002; padding: 5px;}
		#popUpDiv5"""+str(i)+""" h5{width:100%; font-size:15px; color:#0070bd; text-align:center; font-weight:bold;}
		#popUpDiv5"""+str(i)+""" span{ color:#FFFFFF; background-color:#0070bd; padding:1px 3px 0 3px; float:right;}

		#popUpDiv6"""+str(i)+""" {position: fixed; background-color: #fff; min-width: 400px; z-index: 9002; padding: 5px;}
		#popUpDiv6"""+str(i)+""" h5{width:100%; font-size:15px; color:#0070bd; text-align:center; font-weight:bold;}
		#popUpDiv6"""+str(i)+""" span{ color:#FFFFFF; background-color:#0070bd; padding:1px 3px 0 3px; float:right;}

		</style>

		<div style="display: none;" id="blanket"></div>
		<div style="display: none;" id='popUpDiv1"""+str(i)+"""'>
		<h5>Model of """+x["iface"]+""" <span onclick="popup('popUpDiv1"""+str(i)+"""')">X</span></h5>
		<p class="popup">"""+x["model"]+"""</p>
		</div>

		<div style="display: none;" id='popUpDiv2"""+str(i)+"""'>
		<h5>Status of """+x["iface"]+""" <span onclick="popup('popUpDiv2"""+str(i)+"""')">X</span></h5>
		<p class="popup">"""+x["status"]+"""</p>
		</div>

		<div style="display: none;" id='popUpDiv3"""+str(i)+"""'>
		<h5>IP address of """+x["iface"]+""" <span onclick="popup('popUpDiv3"""+str(i)+"""')">X</span></h5>
		<p class="popup">"""+x["address"]+"""</p>
		</div>

		<div style="display: none;" id='popUpDiv4"""+str(i)+"""'>
		<h5>Netmask of """+x["iface"]+""" <span onclick="popup('popUpDiv4"""+str(i)+"""')">X</span></h5>
		<p class="popup">"""+x["netmask"]+"""</p>
		</div>

		<form name="blink_interface_form" method="post" action="iframe_network_settings_new.py#tabs-2">
		<div style="display: none;" id='popUpDiv5"""+str(i)+"""'>
		<h5>Identify port """+x["iface"]+""" <span onclick="popup('popUpDiv5"""+str(i)+"""')">X</span></h5>
		<p class="popup">After clicking identify button the port """+x["iface"]+""" will blink for 10 seconds.<br/>
		<input type="hidden" name="hid_eth_val" value='"""+x["iface"]+"""' />
		<button class="buttonClass" type="submit" name = 'blink_interface'  id = 'blink_interface' value = 'Apply'  style="float:right; margin:10px 200px 10px 0; " >Identify</button>
		</p>
		</div>
		</form>

		<form name = 'change_network' method = 'POST' action="iframe_network_settings_new.py#tabs-2" onsubmit="return validate_ethernet_details();">
		<div style="display: none;" id='popUpDiv6"""+str(i)+"""'>
		<h5>Device details of """+x["iface"]+""" <span onclick="popup('popUpDiv6"""+str(i)+"""')">X</span></h5>
		<p class="popup">
		<table style="margin:0 20px 30px 20px; width:460px; padding:10px; border:#D1D1D1 1px solid;">
		<tr>
			<td valign="top"><strong>IP address</strong></td>
			<td><input class = 'textbox' type = 'text' name = 'ipaddress' value = '"""+x["address"]+"""'>
			</td>
		</tr>

		<tr>
			<td valign="top" width="40%"><strong>Netmask</strong></td>
			<td>
			<input class = 'textbox' type = 'text' name = 'netmask' value = '"""+x["netmask"]+"""'>
			<input class = 'textbox' type = 'hidden' name = 'hid_iface_val' value = '"""+x["iface"]+"""'>
			</td>
		</tr>

		<tr>
			<td><strong>Gateway</strong></td>
			<td><input class = 'textbox' type = 'text' name = 'gateway' value = '"""+x["gateway"]+"""'></td>
		</tr>

		<tr>
			<td><strong>Default Gateway</strong></td>
			<td><input class = 'textbox' type = 'checkbox' name = 'default_gateway'"""
		if(x["is_def_gateway"] == "yes"):
			print "checked"

		print """ ></td>
		</tr>

		<tr>
		<td></td>
		<td> <br/>
		<button class="buttonClass" type="submit" name = 'unconfigure_ethernet'  id = 'unconfigure_ethernet' value = 'Apply'  style="float:right; " onclick="return confirm('Are you sure you want to Unconfigure?');">Unconfigure</button>

		<button class="buttonClass" type="submit" name = 'update_ethernet'  id = 'update_ethernet' value = 'Apply'  style="float:right; ">Update</button>
		</td>
		</tr>

		</table>

		
		</p>
		</div>
		</form>

		<div id='"""+str(i)+"""' style="display:none;">
		<ul>

		<li><a href="#" onclick="popup('popUpDiv1"""+str(i)+"""')">Model</a></li>
		<li><a href="#" onclick="popup('popUpDiv2"""+str(i)+"""')">Status</a></li>
		<li><a href="#" onclick="popup('popUpDiv3"""+str(i)+"""')">IP Address</a></li>
		<li><a href="#" onclick="popup('popUpDiv4"""+str(i)+"""')">Mask</a></li>"""

		if 'bond_type' not in x.keys():
			print """<li><a href="#" onclick="popup('popUpDiv5"""+str(i)+"""')">Identify</a></li>"""

		print """<li><a href="#" onclick="popup('popUpDiv6"""+str(i)+"""')">Edit Network</a></li>

		</ul>
		</div>

		</li>"""
		i=i+1

	print """


	</ul>

	</nav>



	</div>	
		</div>
		</div>
		<!--form container ends here-->
		<p>&nbsp;</p>
		      </div>
		      <div id="tabs-3">
			<div class="form-container">
			<form name = 'dns_form' method = 'POST' action="iframe_network_settings_new.py#tabs-3">
			 <div class="topinputwrap-heading">DNS Configuration</div>
		  <div class="inputwrap">
		<table width="100%" style="padding:0 0 0 10px;">
			<tr>
			<td style=" color:#666666;">Primary DNS IP</td>
			<td><input class="textbox" type="text" name="pdns" id = "pdns" value='"""+split_new_string1+"""' /></td>
			</tr>

			<tr>
			<td style=" color:#666666;">Secondary DNS IP</td>
			<td><input class="textbox" type="text" name="sdns" id = "sdnd"  value='"""+split_new_string2+"""' /></td>
			</tr>

			<tr>
			<td></td>
			<td>
			<button class="buttonClass" type = 'submit'  name="submit" value="Apply" onclick = "return validate_dns_conf();" style="float:left; margin:0 0 0 200px;">Apply</button>
			</td>
			</tr>

		</table>
		</div>
		      </div>
		<p>&nbsp;</p>
			</form>
			</div>
		      <div id="tabs-4">
		<div class="form-container">
	<form name="create_bond_form" method="post" action="iframe_network_settings_new.py#tabs-4" >
		<div class="topinputwrap-heading">Available Bond</div>

	<div style="display: none;" id="blanket2"></div>
	<div style="display: none;" id="bondpopUpDiv">
	<h5><span onclick="popup2('bondpopUpDiv')" style="cursor:pointer;">X</span></h5>
	<p class="popup">

	<div id="popup_heading">Create Bond</div>

	<table style="margin:0 20px 30px 20px; width:460px; padding:10px; border:#D1D1D1 1px solid;">
	<tr>
		<td valign="top"><strong>Bond Name</strong></td>
		<td><input class="textbox" type="text" name="bond_name" />
		</td>
	</tr>

	<tr>
		<td valign="top" width="40%"><strong>Choose ethernet devices</strong></td>
		<td>
		<ul class="ethernet_bonding">"""
	for ifaces in configurable_ifaces["configurable_ifaces"]:
		print """<li><input type="checkbox" name="ethernets" value='"""+ifaces+"""' style="vertical-align:top;"/>"""+ifaces+"""</li>"""

	print """
		</ul>

		</td>
	</tr>

	<tr>
		<td><strong>IP address</strong></td>
		<td><input class="textbox" type="text" name="bond_ip" /></td>
	</tr>

	<tr>
		<td><strong>Netmask</strong></td>
		<td><input class="textbox" type="text" name="bond_netmask" /></td>
	</tr>

	<tr>
		<td><strong>Gateway</strong></td>
		<td><input class="textbox" type="text" name="bond_gateway" /></td>
	</tr>

	<tr>
		<td><strong>Default Gateway</strong></td>
		<td><input class="textbox" type="checkbox" name="bond_is_default_gateway" /></td>
	</tr>

	<tr>
		<td valign="top"><strong>Bond Type</strong></td>
		<td>

		<table>
		<tr>
		<td width="50%"><input type="radio" name="bond_type" value="balance-rr" /> balance-rr</td>
		<td><input type="radio" name="bond_type" value="active-backup" /> active-backup</td>
		</tr>

		<tr>
		<td><input type="radio" name="bond_type" value="balance-xor" /> balance-xor</td>
		<td><input type="radio" name="bond_type" value="broadcast" /> broadcast</td>
		</tr>

		<tr>
		<td><input type="radio" name="bond_type" value="802.3ad" /> 802.3ad</td>
		<td><input type="radio" name="bond_type" value="balance-tlb" /> balance-tlb</td>
		</tr>

		<tr>
		<td><input type="radio" name="bond_type" value="balance-alb" checked /> balance-alb</td>
		<td></td>
		</tr>

		</table>
		<br/>
		</td>
	</tr>

	<tr>
		<td></td>
		<td> <br/><button class="buttonClass" type="submit" name = 'create_bond_but'  id = 'local_action_but' value = 'Apply'  style="float:right; margin:0;">Create Bond</button></td>
	</tr>

	</table>
	</form>

	</p>
	</div>

			<div class="view_option"><a class="classname" onclick="popup2('bondpopUpDiv')" href="#">Create Bond</a> </div>


		  <div class="inputwrap">
		    <div class="formrightside-content">


	<nav id="menu_bond">

	<ul>"""

	if(get_all_bonds["bond_ifaces"] != []):
		bond_array_len = 7000+len(get_all_bonds["bond_ifaces"])
		j=7001
		k=7001
		#while(j<7006):
		for b in get_all_bonds["bond_ifaces"]:
			get_bond_details = net_manage_newkernel.get_iface_config(b["name"],debug='no')
			conf_key = get_bond_details["conf"]

			add_readonly = ""
			net_readonly = ""
			gat_readonly = ""

			if(conf_key["address"] != ''):
				add_readonly = "readonly"
			
			if(conf_key["netmask"] != ''):
				net_readonly = "readonly"
			
			if(conf_key["gateway"] != ''):
				gat_readonly = "readonly"
			

			print """<li onclick="return folder_click("""+str(j)+""", """+str(bond_array_len)+""", """+str(k)+""");"><a>"""+b["name"]+"""</a>

			<style>
			#popUpDiv7"""+str(j)+""" {position: fixed; background-color: #fff; min-width: 400px; z-index: 9002; padding: 5px; top:30px !important;}
			#popUpDiv7"""+str(j)+""" h5{width:100%; font-size:15px; color:#0070bd; text-align:center; font-weight:bold;}
			#popUpDiv7"""+str(j)+""" span{ color:#FFFFFF; background-color:#0070bd; padding:1px 3px 0 3px; float:right;}
			
			#popUpDiv8"""+str(j)+""" {position: fixed; background-color: #fff; min-width: 400px; z-index: 9002; padding: 5px;}
			#popUpDiv8"""+str(j)+""" h5{width:100%; font-size:15px; color:#0070bd; text-align:center; font-weight:bold;}
			#popUpDiv8"""+str(j)+""" span{ color:#FFFFFF; background-color:#0070bd; padding:1px 3px 0 3px; float:right;}
			
			</style>
			
			<div style="display: none;" id="blanket2"></div>
			<form name="delete_bond_form" method="post" action="iframe_network_settings_new.py#tabs-4">
			<div style="display: none;" id='popUpDiv8"""+str(j)+"""'>
			<h5>Delete """+b["name"]+"""<span onclick="popup2('popUpDiv8"""+str(j)+"""')">X</span></h5>
			<p class="popup">
			<div style="border:#D1D1D1 1px solid; text-align:center; height:70px; margin-bottom:20px;">
			<input type="hidden" name="hid_bond_to_delete" value='"""+b["name"]+"""' />
			Are you sure you want to delete """+b['name']+"""?<br/><br/>
				<button class="button_example" type="button" name = 'but_no'  id = 'but_no' value = '' style="float:right; margin:0px 150px 0 0; " onclick="popup2('popUpDiv8"""+str(j)+"""')" >No</button>
				<button class="button_example" type="submit" name = 'delete_bond_but'  id = 'delete_bond_but' value = 'Update' style="float:right; " >Yes</button>

				</div>
			</p>
			</div>
			</form>


			<form name="update_bond_form" method="post" action="iframe_network_settings_new.py#tabs-4" >
			<div style="display: none;" id='popUpDiv7"""+str(j)+"""'>
			<h5><span onclick="popup2('popUpDiv7"""+str(j)+"""')" style="cursor:pointer;">X</span></h5>
			<p class="popup">

			<div id="popup_heading">Modify Bond """+b["name"]+"""</div>

			<table style="margin:0 20px 30px 20px; width:460px; padding:10px; border:#D1D1D1 1px solid;">
			<tr>
				<td valign="top"><strong>Bond Name</strong></td>
				<td><input class="textbox" type="text" name="bond_name" value='"""+b["name"]+"""' readonly />
				</td>
			</tr>

			<tr>
				<td valign="top" width="40%"><strong>Choose ethernet devices</strong></td>
				<td>
				<div id="ethernet_bonding2"><ul>"""
			for ifaces in configurable_ifaces["configurable_ifaces"]:
				print """<li><input type="checkbox" name="ethernets" value='"""+ifaces+"""' style="vertical-align:top;"/>"""+ifaces+"""</li>"""

			if(b["slave_ifaces"] != []):
				for e in b["slave_ifaces"]:
					print """<li><input type="checkbox" name="ethernets" value='"""+e+"""' style="vertical-align:top;" checked/>"""+e+"""</li>"""

			print """
				</ul>

				</td>
			</tr>

			<tr>
				<td><strong>IP address</strong></td>
				<td><input class="textbox" type="text" """+add_readonly+""" name="bond_ip" value='"""+str(conf_key["address"])+"""' /></td>
				<input class="textbox" type="hidden" name="bond_ip_hid" value='"""+str(conf_key["address"])+"""' />
			</tr>

			<tr>
				<td><strong>Netmask</strong></td>
				<td><input class="textbox" type="text" """+net_readonly+""" name="bond_netmask" value='"""+str(conf_key["netmask"])+"""' /></td>
				<input class="textbox" type="hidden" name="bond_netmask_hid" value='"""+str(conf_key["netmask"])+"""' />
			</tr>

			<tr>
				<td><strong>Gateway</strong></td>
				<td><input class="textbox" type="text" """+gat_readonly+""" name="bond_gateway" value='"""+str(conf_key["gateway"])+"""'  /></td>
				<input class="textbox" type="hidden" name="bond_gateway_hid" value='"""+str(conf_key["gateway"])+"""' />
			</tr>

			<tr>
				<td><strong>Default Gateway</strong></td>
				<td><input class="textbox" type="checkbox" name='bond_is_default_gateway'"""
			if(str(conf_key["is_def_gateway"]) == "yes"):
				print "checked"

			print """ /></td>
			</tr>

			<tr>
				<td valign="top"><strong>Bond Type</strong></td>
				<td>

				<table>
				<tr>
				<td width="50%"><input type="radio" name='bond_type"""+str(j)+"""' value='balance-rr'"""
			if(b["type"] == "balance-rr"):
				print "checked"

			print """/> balance-rr</td>
				<td><input type="radio" name='bond_type"""+str(j)+"""' value='active-backup'"""
			if(b["type"] == "active-backup"):
				print "checked"

			print """/> active-backup</td>
				</tr>

				<tr>
				<td><input type="radio" name='bond_type"""+str(j)+"""' value='balance-xor'"""
			if(b["type"] == "balance-xor"):
				print "checked"

			print """ /> balance-xor</td>
				<td><input type="radio" name='bond_type"""+str(j)+"""' value='broadcast'"""
			if(b["type"] == "broadcast"):
				print "checked"

			print """ /> broadcast</td>
				</tr>

				<tr>
				<td><input type="radio" name='bond_type"""+str(j)+"""' value='802.3ad'"""
			if(b["type"] == "802.3ad"):
				print "checked"

			print """ /> 802.3ad</td>
				<td><input type="radio" name='bond_type"""+str(j)+"""' value='balance-tlb'"""
			if(b["type"] == "balance-tlb"):
				print "checked"

			print """ /> balance-tlb</td>
				</tr>

				<tr>
				<td><input type="radio" name='bond_type"""+str(j)+"""' value='balance-alb'"""
			if(b["type"] == "balance-alb"):
				print "checked"

			print """ /> balance-alb</td>
				<td></td>
				</tr>
				</table>
				<br/>
				</td>
			</tr>

			<tr>
				<td></td>
				<input type="hidden" name="hid_radio_no" value='"""+str(j)+"""' />
				<td> <br/><button class="buttonClass" type="submit" name = 'update_bond_but'  id = 'local_action_but' value = 'Apply'  style="float:right; margin:0;">Modify Bond</button></td>
			</tr>

			</table>
			</form>

			</p>


			</div>

			<div id='"""+str(j)+"""' style="display:none;">
			<ul>

			<li><a href="#" onclick="popup2('popUpDiv7"""+str(j)+"""')">Modify</a></li>
			<li><a href="#" onclick="popup2('popUpDiv8"""+str(j)+"""')">Delete</a></li>

			</ul>
			</div>

			</li>"""
			j=j+1
	else:
		print """<div style="margin:0 0 20px 0; text-align:center; color:#B40404;">There are no bonds available. Please <a onclick="popup2('bondpopUpDiv')" href="#" style="text-decoration:underline;">Create a Bond</a></div>"""

	print """

	<script src="new-tooltip/lptooltip.js"></script>
	<link rel = 'stylesheet' type = 'text/css' href = 'new-tooltip/lptooltip.css' />
	</ul>

	</nav>


	</div>
	</div>
		</div>
		<p>&nbsp;</p>
		      </div>







		    </div>
		  </div>
		</div>
	"""
except Exception as e:
	disp_except.display_exception(e);
