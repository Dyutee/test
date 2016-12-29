#!/usr/bin/python
import cgitb, os, sys, commands, common_methods, traceback, string, include_files, cgi
cgitb.enable()

form = cgi.FieldStorage()

#################################################
################ import modules #################
#################################################
sys.path.append('/var/nasexe/storage/');
import storage_op
import sys,os
from lvm_infos import *
from functions import *
import san_disk_funs
sys.path.append('/var/nasexe/python/');
import nfs
import tools
from tools import db
from tools import raid_controller
sys.path.append('../modules/');
import disp_except;
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

################################################
################ Default Values ################
################################################
enable_iscsi_checked = '';
enable_fc_checked    = '';
enable_srp_checked   = '';
enable_nfs_checked   = '';
enable_san_checked   = '';

iscsimessage = '';
fcmessage    = '';
srpmessage   = '';
nfsmessage   = '';
sanmessage   = '';
#--------------------- END --------------------#

#--- Get NFS Service Status
check_nfs_service = nfs.get_nfs_service_status();

if (check_nfs_service == True):
	enable_nfs_checked = 'checked';
	nfsmessage = '&nbsp;&nbsp;&nbsp;<B><font color = "darkgreen">(CURRENTLY ENABLED)</font></B>';

else:
	nfsmessage = '&nbsp;&nbsp;&nbsp;<B><font color = "#EC1F27">(CURRENTLY DISABLED)</font></B>';

#--- Get iSCSI Status
check_iscsi_status = common_methods.get_iscsi_status();
if (check_iscsi_status > 0):
        enable_iscsi_checked = 'checked';
        iscsimessage = '&nbsp;&nbsp;&nbsp;<B><font color = "darkgreen">(CURRENTLY ENABLED)</font></B>';
else:
	iscsimessage = '&nbsp;&nbsp;&nbsp;<B><font color = "#EC1F27">(CURRENTLY DISABLED)</font></B>';

#--- Get FC Status
check_fc = san_disk_funs.fc_target_status();
if (check_fc !=[]):
        enable_fc_checked = 'checked';
        fcmessage         = '&nbsp;&nbsp;&nbsp;<B><font color = "darkgreen">(CURRENTLY ENABLED)</font></B>';
else:
	
        fcmessage         = '&nbsp;&nbsp;&nbsp;<B><font color = "#EC1F27">(CURRENTLY DISABLED)</font></B>';

#--- Get SRP Status
check_srp = san_disk_funs.ib_target_status();

if (check_srp !=[]):
        enable_srp_checked = 'checked';
        srpmessage         = '&nbsp;&nbsp;&nbsp;<B><font color = "darkgreen">(CURRENTLY ENABLED)</font></B>';
	
else:
	
        srpmessage         = '&nbsp;&nbsp;&nbsp;<B><font color = "#EC1F27">(CURRENTLY DISABLED)</font></B>';

################################################
############# Restart NFS Service ##############
################################################
if(form.getvalue("restart-nfs")):
	nfs_restart_cmd = tools.restart_service("NFS")
	if(nfs_restart_cmd == True):
		print "<div id='id_trace'>"
		print "NFS service restarted!"
		print "</div>"
	else:
		print "<div id='id_trace_err'>"
		print "Error restarting NFS!"
		print "</div>"
#--------------------- END --------------------#

################################################
############# Restart SMB Service ##############
################################################
if(form.getvalue("restart-smb")):
	smb_stop_cmd = tools.smb_service("stop")
	if(smb_stop_cmd == True):
		smb_start_cmd = tools.smb_service("start")
		if(smb_start_cmd == True):
			print "<div id='id_trace'>"
			print "SMB service restarted!"
			print "</div>"
		else:
			print "<div id='id_trace_err'>"
			print "Error restarting SMB!"
			print "</div>"
	else:
		print "<div id='id_trace_err'>"
		print "Error restarting SMB!"
		print "</div>"
#--------------------- END --------------------#

################################################
############# Restart AFP Service ##############
################################################
if(form.getvalue("restart-afp")):
	afp_restart_cmd = tools.restart_service("AFP")
	if(afp_restart_cmd == True):
                print "<div id='id_trace'>"
                print "AFP service restarted!"
                print "</div>"
        else:
                print "<div id='id_trace_err'>"
                print "Error restarting AFP!"
                print "</div>"
#--------------------- END --------------------#

################################################
############# Restart FTP Service ##############
################################################
if(form.getvalue("restart-ftp")):
	ftp_restart_cmd = tools.restart_service("FTP")
	if(ftp_restart_cmd == True):
                print "<div id='id_trace'>"
                print "FTP service restarted!"
                print "</div>"
        else:
                print "<div id='id_trace_err'>"
                print "Error restarting FTP!"
                print "</div>"
#--------------------- END --------------------#

################################################
########### Restart RAID Controller ############
################################################
if(form.getvalue("restart-raid")):
	restart_raid = raid_controller.start_webui()
	if(restart_raid == True):
                print "<div id='id_trace'>"
                print "RAID Controller restarted!"
                print "</div>"
        else:
                print "<div id='id_trace_err'>"
                print "Error restarting RAID Controller!"
                print "</div>"
#--------------------- END --------------------#

################################################
################# Restart SAN ##################
################################################
if(form.getvalue("san_start")):
	start_san = tools.restart_service("SAN")
	if(start_san == True):
                print "<div id='id_trace'>"
                print "SAN service restarted!"
                print "</div>"
        else:
                print "<div id='id_trace_err'>"
                print "Error restarting SAN!"
                print "</div>"
#--------------------- END --------------------#

#--- Get RAID Controller
controllers = raid_controller.raid_c()


print
print """
	<div id="loader-div" style="text-align:center; display:none;" ><img style="margin-top:20%;" src="../images/ajax-loader.gif" /><br/> Loading...</div>
      <!--Right side body content starts from here-->
      <div class="rightsidecontainer" id="body-div">
        <!--tab srt-->
        <div class="searchresult-container">
	<div style="margin:0 0 0px 0;" class="topinputwrap-heading"><a class="demo" href ="#"><img src ="../images/help_icon1.png" style="width:13px;"><span class="tooltip" >
                 <table border="0">
        <tr>     
        <td class="text_css">This page lets you restart a number of different services, such as SAN, NFS, SMB, AFP, FTP and the RAID controller service.
</td>
        </tr>
        </table>"""
if(check_ha == True):
	print"""</span></a> Services ("""+show_tn+""")
                <span style="float:right; margin:0;"><a onclick="return onclick_loader();" class="resource_links" href="https://"""+other_node_ip+"""/fs4/py/iframe_start_services.py">"""+show_on+"""</a></span>
                </div>"""
else:
	print """</span></a><p class = "gap_text">Services</p></div>"""
print"""
          <div class="infoheader">
            <div id="tabs">
              <ul>
                <li><a href="#tabs-1">SAN</a></li>
                <!--<li><a href="#tabs-2">FC</a></li>
                <li><a href="#tabs-3">SRP</a></li>-->
                <li><a href="#tabs-4">NFS</a></li>
                <li><a href="#tabs-5">SMB</a></li>
                <li><a href="#tabs-6">AFP</a></li>
                <li><a href="#tabs-7">FTP</a></li>
                <li><a href="#tabs-8">RAID Controller</a></li>
              </ul>"""
print common_methods.wait_for_response;
		
print """              <div id="tabs-1">

	<!--form container starts here-->
        <div class="form-container">
          <div class="inputwrap">
            <div class="formleftside-content">
	 <form name = 'user_creation' method = 'POST' action = ''>
	<div id="restart-service-div" >
	 <button onclick="return onclick_loader_button('san');" type="submit" name="san_start" value="restart-nfs" style="border:none; background-color:#FFF; cursor:pointer;">
         <img id="sync-static" src="../images/restart-services-fs4.png" alt="start SAN" />
	 <img id="sync-loading" style="display:none;" src="../images/sync-loading.GIF" alt="sync users" /></button><br/>
	 <p id="sync-content" style="padding:10px 0 0 0;">Restart SAN</p>
                        <!--<p style="padding:10px 0 0 0;">start SAN</p>-->
        </div>
	</form>

	</div>
          </div>
        </div>
        <!--form container ends here-->
	<p>&nbsp;</p>
              </div>

              <!--<div id="tabs-2">
        <div class="form-container">
          <div class="inputwrap">
	<div class="formleftside-content">

	<form name = 'add_groups' method = 'POST' action = ''>

<table width ="685">
        <tr>
                <td><input type="checkbox" id = 'id_start_fc' name = 'fc' """+enable_fc_checked+""" onclick='return start_services("fc", document.getElementById("id_start_fc").checked);'> Enable/Disable FC """+fcmessage+"""
                </td>
        </tr>
        </table>
	</form>
	</div>
          </div>
        </div>
	<p>&nbsp;</p>
              </div>


              <div id="tabs-3">
	
        <div class="form-container">
          <div class="inputwrap">
        <div class="formleftside-content">
	<form name = 'add_iii' method = 'POST' action = ''>
	<table width ="685">
        <tr>
                <td><input type="checkbox" id = 'id_start_srp' name = 'srp' """+enable_srp_checked+""" onclick='return start_services("srp", document.getElementById("id_start_srp").checked);'> Enable/Disable SRP """+srpmessage+"""
                </td>
        </tr>
        </table>
        </form>
              </div>
            </div>
          </div>
	<p>&nbsp;</p>
        </div>-->


 <div id="tabs-4">
        
         <!--form container starts here-->
        <div class="form-container">
          <div class="inputwrap">
        <div class="formleftside-content">
        <form name = 'nfs_restart_form' method = 'post' action = 'iframe_start_services.py#tabs-4'>
	<div id="restart-service-div" >
		<button onclick="return onclick_loader_button('nfs');" type="submit" name="restart-nfs" value="restart-nfs" style="border:none; background-color:#FFF; cursor:pointer;">
		<img id="sync-static-nfs" src="../images/restart-services-fs4.png" alt="restart NFS" />
		<img id="sync-loading-nfs" style="display:none;" src="../images/sync-loading.GIF" alt="nfs restart" /></button><br/>
			<p id="sync-content-nfs" style="padding:10px 0 0 0;">Restart NFS</p>
	</div>

                <!--<td><input type="checkbox" id = 'id_start_nfs' name = 'nfs' """ + enable_nfs_checked + """ onclick='return start_services("nfs", document.getElementById("id_start_nfs").checked);'>Enable/Disable NFS """ + nfsmessage + """
                </td>-->
        </form>

              </div>
            </div>
          </div>
	<p>&nbsp;</p>
        </div>


 <div id="tabs-5">
        
         <!--form container starts here-->
        <div class="form-container">
          <div class="inputwrap">
        <div class="formleftside-content">
        <form name = 'smb_restart_form' method = 'post' action = 'iframe_start_services.py#tabs-5'>
	<div id="restart-service-div" >
		<button onclick="return onclick_loader_button('smb');" type="submit" name="restart-smb" value="restart-smb" style="border:none; background-color:#FFF; cursor:pointer;">
		<img id="sync-static-smb" src="../images/restart-services-fs4.png" alt="restart SMB" />
		<img id="sync-loading-smb" style="display:none;" src="../images/sync-loading.GIF" alt="smb restart" /></button><br/>
			<p id="sync-content-smb" style="padding:10px 0 0 0;">Restart SMB</p>
	</div>

        </form>

              </div>
            </div>
          </div>
	<p>&nbsp;</p>
        </div>

 <div id="tabs-6">
        
         <!--form container starts here-->
        <div class="form-container">
          <div class="inputwrap">
        <div class="formleftside-content">
        <form name = 'afp_restart_form' method = 'post' action = 'iframe_start_services.py#tabs-6'>
	<div id="restart-service-div" >
		<button onclick="return onclick_loader_button('afp');" type="submit" name="restart-afp" value="restart-afp" style="border:none; background-color:#FFF; cursor:pointer;">
		<img id="sync-static-afp" src="../images/restart-services-fs4.png" alt="restart AFP" />
		<img id="sync-loading-afp" style="display:none;" src="../images/sync-loading.GIF" alt="afp restart" /></button><br/>
			<p id="sync-content-afp" style="padding:10px 0 0 0;">Restart AFP</p>
	</div>

        </form>

              </div>
            </div>
          </div>
	<p>&nbsp;</p>
        </div>

 <div id="tabs-7">
        
         <!--form container starts here-->
        <div class="form-container">
          <div class="inputwrap">
        <div class="formleftside-content">
        <form name = 'ftp_restart_form' method = 'post' action = 'iframe_start_services.py#tabs-7'>
	<div id="restart-service-div" >
		<button onclick="return onclick_loader_button('ftp');" type="submit" name="restart-ftp" value="restart-ftp" style="border:none; background-color:#FFF; cursor:pointer;">
		<img id="sync-static-ftp" src="../images/restart-services-fs4.png" alt="restart FTP" />
		<img id="sync-loading-ftp" style="display:none;" src="../images/sync-loading.GIF" alt="ftp restart" /></button><br/>
			<p id="sync-content-ftp" style="padding:10px 0 0 0;">Restart FTP</p>
	</div>

        </form>

              </div>
            </div>
          </div>
	<p>&nbsp;</p>
        </div>

 <div id="tabs-8">
        
         <!--form container starts here-->
        <div class="form-container">
          <div class="inputwrap">
        <div class="formleftside-content">
        <form name = 'raid_en_form' method = 'post' action = 'iframe_start_services.py#tabs-8'>
	<table style="border:#D1D1D1 1px solid; width:400px; margin:0 0 20px 0; float:left;">
	<tr>
	<th style="border:#D1D1D1 1px solid; background-color:#D1D1D1; padding:5px;">RAID Controllers</th>
	</tr>

	<tr>
	<td style="padding:0 0 0 10px;">"""+controllers+"""</td>
	</tr>
	

	</table>

	<table style="border:#D1D1D1 1px solid; width:100px;">
	<tr>
        <th style="border:#D1D1D1 1px solid; background-color:#D1D1D1; padding:5px;">Restart RAID Controllers</th>
        </tr>

	<tr>
	<td>
	<div id="restart-service-div" style="width:100px;">
                <button onclick="return onclick_loader_button('raid');" type="submit" name="restart-raid" value="restart-raid" style="border:none; background-color:#FFF; cursor:pointer;">
                <img id="sync-static-raid" src="../images/restart-services-fs4.png" alt="restart RAID" />
		<img id="sync-loading-raid" style="display:none;" src="../images/sync-loading.GIF" alt="sync users" /></button><br/>
                        <!--<p style="padding:10px 0 0 0;">Restart RAID Controller</p>-->
        </div>
	</td>
	</tr>
	</table>

        </form>

              </div>
            </div>
          </div>
	<p>&nbsp;</p>
        </div>

</div>
</div/>
</div>
</div>
"""
