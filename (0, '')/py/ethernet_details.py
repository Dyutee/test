#!/usr/bin/python
#_*_ coding: UTF-8 _*_

#enable debugging
import cgitb, cgi, commands, sys 
cgitb.enable()
print "Content-Type: text/html\n"
try:
	sys.path.append('/var/nasexe/')
	import net_manage as net_manage_bond

	form = cgi.FieldStorage()
	iface_value = form.getvalue("device")

	####### on clicking apply button #######

	if(form.getvalue("submit")):
		getip=form.getvalue("ipaddress")
		#tracedebug.watch(getip);
		getmask=form.getvalue("netmask")
		#tracedebug.watch(getmask);
		getgateway=form.getvalue("gateway")
		#tracedebug.watch(getgateway);
		getdefault_gateway=form.getvalue("default_gateway")
		if(getdefault_gateway=="on"):
			def_gateway="yes"
		else:
			def_gateway="no"
	
		status=net_manage_bond.get_ifenslave_ifaces(iface_value)
		#print status
		if status['id'] == 0:
	        	slave_ifaces=status['slave_ifaces']
		else:
	        	slave_ifaces=[]

		if(getip==None):
	                getip=''

		if(getmask==None):
	                getmask=''
		
		if(getgateway==None):
			getgateway=''

		iface_inp={'iface':iface_value,'address':getip,'netmask':getmask,'gateway':getgateway,'debug':"no",'is_def_gateway':def_gateway,'slave_ifaces':slave_ifaces}

		#print iface_value
		#print "<br/>"
		#print getip
		#print "<br/>"
		#print getmask
		#print "<br/>"
		#print getgateway
		#print "<br/>"
		#print def_gateway
		#print "<br/>"
		#print slave_ifaces

		#print "<br/>"
		#exit()
		change_configuration = net_manage_bond.configure_iface(iface_inp)

		if(change_configuration["id"]==0):
			print"""<div id = 'id_trace'>"""
			print change_configuration["desc"]
			print "</div>"

		elif(change_configuration["id"]==2):
			print"""<div id = 'id_trace_err'>"""
	                print change_configuration["desc"]
	                print "</div>"


	####### end #######

	####### on clicking unconfigure button #######

	if(form.getvalue("unconfigure")):
		remove_configuration = net_manage_bond.unconfigure_iface(iface_value)

		if(remove_configuration["id"]==0):
        	        print"""<div id = 'id_trace'>"""
                	print remove_configuration["desc"]
	                print "</div>"

	        elif(remove_configuration["id"]==2):
	                print"""<div id = 'id_trace_err'>"""
	                print remove_configuration["desc"]
	                print "</div>"

	####### end #######

	####### show status #######

	#iface_info=net_manage.show_conf(iface_value)
	iface_primary_info = net_manage_bond.get_iface_config(iface_value)
	iface_info = iface_primary_info["conf"]

	####### end #######


	print """
	<html>
	<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <title>..::Tyrone Opslag FS2::..</title>

        <link href = "../css/style.css" rel = "stylesheet" type = "text/css" />
        <link href = "../css/jquery.alerts.css" rel = "stylesheet" type = "text/css" />
        <link rel = 'important.gif' href = '../images/important.gif  ' />

        <script language = 'javascript' src = 'js/commons.js'></script>
        <script type="text/javascript" src="js/jquery.min(1).js"></script>
        <script type="text/javascript" src="js/jquery.alerts.js"></script>
        <script language = 'javascript' src = 'js/jquery-latest-fade.js'></script>

       	<script type="text/javascript">
        var helperPopup = new Popup('helper'); // Pass an ID to link with an existing DIV in page
        helperPopup.autoHide = false;
        helperPopup.position = "below right";
        helperPopup.constrainToScreen = false;
        </script>

        <script type = "text/javascript">
        function hideMessage() {
        $(document).ready(
        function(){
                $("#id_trace_err").fadeOut(2000);
                $("#id_trace").fadeOut(2000);
                }
        );
        }
        var tim = window.setTimeout("hideMessage()", 10000);  // 10000 milliseconds = 10 seconds
        </script>



	
	</head>
	<body onload = 'document.change_network.action_but.disabled = "true";'>

	<form name = 'change_network' method = 'POST' action="" onsubmit="return validate_ethernet_details();">
        <table align = 'right' id = 'nis_auth_table' style = 'margin:70px 100px 20px 0; border:#BDBDBD 1px solid; font-size:10px; font-family: Arial, Helvetica, sans-serif; '>
        <tr>
        <td>

        <table width="500">
        <tr>
        <td style="background-color:#BDBDBD; height:30px; color:#000; padding:0 0 0 10px;">Device Details of <span style='color:#0B610B; font-weight:bold;'>"""+iface_value+"""</span></td>
        </tr>

        <tr>
        <td>

        <table width="500" style="padding:0 0 0 10px;">
        <tr>
        <td width="30%">IP</td>
        <td><input class = 'textbox' type = 'text' name = 'ipaddress' value = '"""+iface_info["address"]+"""' oninput = 'enable_apply_button();'></td>
        </tr>

        <tr>
        <td>Netmask</td>
        <td><input class = 'textbox' type = 'text' name = 'netmask' value = '"""+iface_info["netmask"]+"""' oninput = 'enable_apply_button();'></td>
        </tr>

        <tr>
        <td>Gateway</td>
        <td><input class = 'textbox' type = 'text' name = 'gateway' value = '"""+iface_info["gateway"]+"""' oninput = 'enable_apply_button();'></td>
        </tr>

        <tr>
        <td>Default Gateway</td>
        <td><input class = 'textbox' type = 'checkbox' name = 'default_gateway' ></td>
        </tr>

        <tr>
        <td></td>
        <td><button type = 'submit' class="button_example" name="submit" id="id_apply_but" value="Apply" onclick ="return enable_apply_button();" >Apply</button> 

        <button type = 'submit' class="button_example" name="Unconfigure" id="id_apply_but" value="Unconfigure" onclick ="return  confirm('Are you sure you want to unconfigure?');" >Unconfigure</button>
	</td>
        </tr>
        </table>

        </tr>
        </table>

        </td>
        </tr>
        </table>

	</form>
	</body>
	</html>"""

except Exception as e:
	print e
	fh = open('/var/www/fs4/py/temp', 'w');
        fh.write("<BR>");
        fh.write('<BR><input type = "button" value = "Back" onclick = "location.href = \'/fs4/py/network_settings_page.py\'">');
