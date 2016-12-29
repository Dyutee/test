#!/usr/bin/python
import cgitb, header,commands, os, sys, cgi, common_methods, string
cgitb.enable()

sys.path.append('/var/nasexe/')
import net_manage as net_manage_bond

log_array = [];
log_file = common_methods.log_file;
logstring = '';

if(header.form.getvalue("submit_hostname")):
	get_hostname = header.form.getvalue("hostname")
	get_ip_address = header.form.getvalue("select_primary_ip")
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

gethostname = net_manage_bond.get_hostname()
#print gethostname

ss = gethostname
logstring = str(common_methods.now) + '<<>>From: ' + common_methods.remote_ip + '<<>>' + str(ss);
log_array.append(logstring);
#print gethostname
#print gethostname["hostname"]

getall_ifaces=net_manage_bond.get_all_ifaces_config()
get_all_ip = getall_ifaces["all_conf"]
#print get_all_ip

ss = getall_ifaces
logstring = str(common_methods.now) + '<<>>From: ' + common_methods.remote_ip + '<<>>' + str(ss);
log_array.append(logstring);
common_methods.append_file(log_file, log_array);

#------------------ Network Settings Start -------------------#
get_all_iface = net_manage_bond.get_all_ifaces_config()

if(get_all_iface["id"]==0):
	iface_info = get_all_iface["all_conf"]
	#print iface_info

elif(get_all_iface["id"]==2):
	iface_info = [{'status': '', 'iface': '', 'netmask': '', 'address': '', 'model': '', 'gateway': ''}]
#------------------ Network Settings End -------------------#

#------------------ DNS Configuration Start --------------------#
image_icon = common_methods.getimageicon();
dns_conf_file="/etc/resolv.conf"

#Entering values into resolv.conf file "START"

if(header.form.getvalue("submit")):
	new_primary_dns = header.form.getvalue("pdns")
	new_secondary_dns = header.form.getvalue("sdns")

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
	#print split_new_string1
	#exit;
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
		split_dns_lines = string.split(line)
		new_string = new_string + split_dns_lines[1]+" "

	split_new_string = string.split(new_string)
	split_new_string1 = split_new_string[0]
	#print split_new_string1
	#exit;
	split_new_string2 = split_new_string[1]

dns_file.close()
#------------------ DNS Configuration End --------------------#

#------------------ Ethernet Teaming Start --------------------#
# Get all bond ifaces   
bond_created=net_manage_bond.get_all_bond_ifaces()

# Get free bond ifaces
free_bond=net_manage_bond.get_free_bond_ifaces()

# Get all configurable ifaces
all_confi_ifaces=net_manage_bond.get_all_configurable_ifaces(exclude_bond="yes")

#------------------ Ethernet Teaming End --------------------#

#print 'Content-Type: text/html'
import left_nav
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


      <!--Right side body content starts from here-->
      <div class="rightsidecontainer">
        <div class="insidepage-heading"> RESOURCES >> <span class="content">Network Settings</span></div>
        <!--tab srt-->
        <div class="searchresult-container">
          <div class="infoheader">
            <div id="tabs">
              <ul>
                <li><a href="#tabs-1">Host Name</a></li>
                <li><a href="#tabs-2">Network</a></li>
                <li><a href="#tabs-3">DNS</a></li>
                <li><a href="#tabs-4">Ethernet Teaming</a></li>
                <li><a href="#tabs-5">Activate Ethernet Teaming</a></li>
                <li><a href="#tabs-6">Remove Ethernet Teaming</a></li>
              </ul>
              <div id="tabs-1">

	<!--form container starts here-->
        <div class="form-container">
	<form name = 'server_change' method = 'POST'>
          <div class="topinputwrap-heading"> Change Host Name </div>
          <div class="topinputwrap">
		<table width="100%" style="padding:0 0 0 10px;">
		<tr>
		<td>HostName</td>
		<td><input class = 'textbox' type = 'text' name = 'hostname' value =""" + gethostname["hostname"] + """></td>
		</tr>
		<tr>
		<td>Select Primary IP</td>
		<td>
		<select name="select_primary_ip">
                <option value="""+gethostname["primary_ip"]+""" selected="selected">"""+gethostname["primary_ip"]+"""</option>"""
for ip in get_all_ip:
	if(ip["address"]!=''):
		print """<option value="""+ip["address"]+""" >"""+ip["address"]+"""</option>"""

print """</select>

		</td>
		</tr>

		<tr>
		<td></td>
		<td>

		<button class="button_example" type = 'submit'  name="submit_hostname" value="Apply" onclick = "return validate_form();" style="float:left; margin:0 0 0 200px;">Apply</button>
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
	<div class="topinputwrap-heading">Network Information</div>
          <div class="topinputwrap">
	
	<table width="100%" style="border:#BDBDBD 1px solid;">
	<tr>
	<th style="border:#BDBDBD 1px solid;">Interface</th>
	<th style="border:#BDBDBD 1px solid;">Model</th>
	<th style="border:#BDBDBD 1px solid;">Status</th>
	<th style="border:#BDBDBD 1px solid;">IP Address</th>
	<th style="border:#BDBDBD 1px solid;">Mask</th>
	<th style="border:#BDBDBD 1px solid;">Identify</th>
	</tr>"""

for x in iface_info:
	print """<tr>
	<td  style="border:#BDBDBD 1px solid; height:70px; min-width:50px; ">
	<!--<font color = 'darkred' size = '4'> *</font>-->
	<a class="various" data-fancybox-type="iframe"  style="text-decoration:none;" href="ethernet_details.py?device=%s"><img src='../images/ethernet-icon.png' style='margin:0 0 0 18px;' /><br/><span style='float:right; color:#000; padding: 0 20px 0 0;'>"""% x["iface"]

	print x["iface"]
	print """</span></a> <input type = 'hidden' name = 'hid_network' value = ''>
	</td>

	<td style="border:#BDBDBD 1px solid;">"""
	print x["model"]
	print """</td>

	<td style="border:#BDBDBD 1px solid;">"""
	print x["status"]
	print "<br/>"
	count = 0
	for y in x["slave_ifaces_status"]:
		print x["slave_ifaces"][count]+"-"+y+"<br/>"
		count =count + 1
	print """</td>

	<td style="border:#BDBDBD 1px solid;">"""
	print x["address"]
	print """</td>

	<td style="border:#BDBDBD 1px solid;">"""
	print x["netmask"]
	print """</td>"""


	print """<td style="border:#BDBDBD 1px solid;">
	<input id = 'id_activate_button' class="button_example" type = 'button' name = 'eth_button' value = 'Blink' onclick='return blink_interface_alert(\"""" + x["iface"] + """");' >
	<input type='hidden' name = 'hid_activate' id = 'hid_activate' value='"""+x["iface"]+"""'>
	</td>

	</tr>"""


print """	
<tr>
                                        <td colspan = '6' class = "table_content" height = "35px" valign = "middle" bgcolor = "#f5f5f5">
                                                <font color = 'darkred' size = '4'><B>*</B></font> - <B>Device is used for replication</B><BR>
                                                <B>Status 'UNKNOWN'</B> indicates that the port of that specific interface is free.
                                        </td>
                                </tr>
</table>
	</div>
        </div>
        <!--form container ends here-->
	<p>&nbsp;</p>
              </div>
              <div id="tabs-3">
		<div class="form-container">
		<form name = 'dns_form' method = 'POST'>
		 <div class="topinputwrap-heading">DNS Configuration</div>
          <div class="topinputwrap">
	<table width="100%" style="padding:0 0 0 10px;">
                <tr>
                <td>Primary DNS IP</td>
                <td><input class="textbox" type="text" name="pdns" id = "pdns" value='"""+split_new_string1+"""' /></td>
                </tr>

                <tr>
                <td>Secondary DNS IP</td>
                <td><input class="textbox" type="text" name="sdns" id = "sdnd"  value='"""+split_new_string2+"""' /></td>
                </tr>

		<tr>
                <td></td>
                <td>
		<button class="button_example" type = 'submit'  name="submit" value="Apply" onclick = "return validate_dns_conf();" style="float:left; margin:0 0 0 200px;">Apply</button>
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
	<form name = 'plan_eth' action = 'submit_ethernet_teaming.py' method = 'POST'>
        <div class="topinputwrap-heading">Create Ethernet Teaming/Aggregation</div>
         <div class="topinputwrap">"""
if(bond_created["stdout"]!=[]):
	print """<span style="font-weight:bold; padding:10px 0 0 150px; color:#B40404; text-align:center;">Please remove existing bonds to activate this option!</B>"""
else:
	print """
	<table width="100%" style="padding:0 0 0 10px;">
                <tr>
                <td>Select the number of Bonds</td>
                <td>

		<input class = 'textbox' name = 'bond_count' value = '1' style='width:30px;' readonly>
		<input type = "button" name = 'increase' value = "&#9650;" onclick = "this.form.bond_count.value++; if (parseInt(this.form.bond_count.value) >= 1){this.form.reduce.disabled=false;} if (this.form.bond_count.value == 16){this.form.increase.disabled=true;}" style = "font-size:8px; margin:0; padding:0; width:20px;  height:13px;" ><BR>
                <input type = "button" value = "&#9660;" name = 'reduce' onclick = "this.form.bond_count.value--; if (this.form.bond_count.value <= 1){this.form.reduce.disabled=true;} if (this.form.bond_count.value < 16){this.form.increase.disabled=false;}" style = "font-size:8px; margin:0 488px 0 0; padding:0; width:20px; height:12px; float:right;" disabled>

		</td>
                </tr>

                <tr>
                <td>Choose the type of Bond</td>
                <td>
		<input type = 'radio' name = 'bond_type' value = '802.3ad' >802.3ad
		<input type = 'radio' name = 'bond_type' value = 'balance-alb' >ALB
		</td>
                </tr>

                <tr>
                <td></td>
                <td>
		<button class="button_example" type = 'submit'   name="submit_ethernet_bond" value="Create New Team"  onclick = "return validate_plan_team();" style="float:left; margin:0 0 0 200px;">Create new Team</button>
                </td>
                </tr>

        </table>"""

print """</div>
	</div>
	<p>&nbsp;</p>
	</form>
              </div>


              <div id="tabs-5">
	<div class="form-container">
	<form name = 'assign_eth' action = 'submit_ethernet_teaming.py' method = 'POST'>
        <div class="topinputwrap-heading">Activate Ethernet Teaming/Aggregation</div>
         <div class="topinputwrap">"""
if(bond_created["stdout"]==[]):
	print """<span style="font-weight:bold; padding:10px 0 0 150px; color:#B40404; text-align:center;">No bonds created! Please create a bond.</B>"""
else:
	print """
	<table width="100%" style="padding:0 0 0 10px;">
                <tr>
                <td>Choose a Bond to Activate</td>
                <td>
		<select class = 'input' name = 'bond_list' style = 'width: 100%;'>
                <option value = ''>--</option>"""
	for z in free_bond["stdout"]:
		print """<option value = '"""+z+"""'>"""+z+"""</option>"""
	print """</select>

		</td>
                </tr>

                <tr>
                <td>Choose eth Devices for teaming</td>
                <td>
	<select class = 'input' name = 'eth_list[]' multiple style = 'width: 99%; height: 130px;'>"""
	for w in all_confi_ifaces["stdout"]:
		print """<option value = '"""+w+"""'>"""+w+"""</option>"""

	print """
	</select><BR>
	(Use 'Ctrl' key for multiple selection.)
		</td>
                </tr>

                <tr>
                <td></td>
                <td>
		<button class="button_example" type = 'submit' name="submit_slave" value="Assign eth to bond" onclick ="return validate_teaming_form();" style="float:right; margin:0 0 0 0;">Assign eth to bond</button>
                </td>
                </tr>

        </table>"""

print """</div>
	</div>
	<p>&nbsp;</p>
	</form>
              </div>


              <div id="tabs-6">
	<div class="form-container">
	<form name = 'rem_bond_list' method = 'POST' action='submit_ethernet_teaming.py'>
        <div class="topinputwrap-heading">Remove Ethernet Teaming/Aggregation</div>
         <div class="topinputwrap">"""
if(bond_created["stdout"]==[]):
	print """<span style="font-weight:bold; padding:10px 0 0 150px; color:#B40404; text-align:center;">No bonds created! Please create a bond.</B>"""
else:
	print """
	<table width="100%" style="padding:0; border:#BDBDBD 1px solid;">
                <tr>
                <th style="border:#BDBDBD 1px solid;">Team</th>
                <th style="border:#BDBDBD 1px solid;">Bonding Mode</th>
		<th style="border:#BDBDBD 1px solid;">Teamed Devices</th>
                </tr>"""

	nol=0
	for value in bond_created["stdout"]:
		print """<tr>
		<td style="border:#BDBDBD 1px solid; text-align:center;">"""+str(value)+"""</td>
		<td style="border:#BDBDBD 1px solid; text-align:center;">"""+str(bond_created["bond_type"])+"""</td>
		<td style="border:#BDBDBD 1px solid; text-align:center;">"""
		if(bond_created["slave_ifaces"][nol]==[]):
			print "None"
		else:
			for x in bond_created["slave_ifaces"][nol]:
				print x+" "
		nol = nol+1
		print """</td>
		</tr>"""

	print """<tr>
                <td></td>
                <td></td>
                <td>
		<button class="button_example" type = 'submit' name="submit_remove" value="Remove" style="float:right; margin:0 0 0 0;">Remove</button>
                </td>
                </tr>

        </table>"""

print """</div>
	</div>
	<p>&nbsp;</p>
	</form>
              </div>




            </div>
          </div>
        </div>
        <!--form container ends here-->
        <!--form container starts here-->
        <!--form container ends here-->
      </div>
      <!--Right side body content ends here-->
    </div>
    <!--Footer starts from here-->
    <div class="insidefooter footer_content">&copy; 2013 Opslag FS2</div>
    <!-- Footer ends here-->
  </div>
  <!--inside body wrapper end-->
</div>
<!--body wrapper end-->
</body>
</html>
"""
