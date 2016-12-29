#!/usr/bin/python
import cgitb, include_files, os, sys, cgi
cgitb.enable()

sys.path.append('/var/nasexe/python/')
import infiniband

form = cgi.FieldStorage()

#-------------Check HA---------------
sys.path.append('/var/nasexe/python/')
import tools
from tools import scan_remount
from tools import db
import nfs
import infiniband
#from python import infiniband
#from tools import 

nfs_status = nfs.get_nfs_service_status()
#print nfs_status
#nfs_status =False
#print nfs_status
get_shares1 = tools.get_all_shares(debug=True)
#shr = get_shares1['name']
share_infos = get_shares1["shares"]
#print share_infos

sys_node_name = tools.get_ha_nodename()
for x in share_infos:
	path = x['path']
	node = x['node']
	#print path
	#print '<br/>'
	#print node
	if(sys_node_name == "node1"):
		node = sys_node_name
		nfs_status_line = nfs.getstatus(path,node)
		nfs_get= nfs_status_line['exports']
		check_nfs= nfs_get['use_nfs']
	else:
		other_node = "node2"
		node = other_node
                nfs_status_line = nfs.getstatus(path,node)
                nfs_get= nfs_status_line['exports']
                check_nfs= nfs_get['use_nfs']
check_ha = tools.check_ha()

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

#----------------End---------------------
#--------------------_Enable Ip Over IB-------------------------------------------------
status_chk = ''
display_color = ''
status_chk1 = ''
display_color1 = ''
if(form.getvalue("ip_start")):
	ip_name = form.getvalue("ip_start")
	enable_status=infiniband.enable_ipoib()
	
	if(enable_status == True):
		print"""<div id = 'id_trace'>"""
		print "Successfully enabled IP over IB!"
		print "</div>"
	else:
		print"""<div id = 'id_trace_err'>"""
		print "Error occured while enabling!"
		print "</div>"
	print "<script>location.href = 'new_iframe_infiniband.py#tabs-1';</script>"
#----------------------End---------------------------------------------------------------

#--------------------Disable Ip Over IB------------------------------------------------
if(form.getvalue("ip_stop")):
        ip_name = form.getvalue("ip_stop")
        disable_status=infiniband.disable_ipoib()

        if(disable_status == True):
                print"""<div id = 'id_trace'>"""
                print "Successfully disabled IP over IB!"
                print "</div>"
        else:
                print"""<div id = 'id_trace_err'>"""
                print "Error occured while disabling!"
                print "</div>"
	print "<script>location.href = 'new_iframe_infiniband.py#tabs-1';</script>"
#-------------------------------------End------------------------------------------------------

#---------------------Status Ip Over IB---------------------------------------------------------
status=infiniband.status_ipoib()
if(status == True):
	status_chk = 'Enabled'
	display_color = 'green'
	display_img ='block'
	display_img1 ='none'
else:
	status_chk = 'Disabled'
	display_color = 'red'
	display_img ='none'
	display_img1 ='block'

#----------------------------------------End------------------------------------------
#--------------------_Enable Nfs Over Rdma -------------------------------------------------

status_ipoib=infiniband.status_ipoib()
#print status_ipoib
st = infiniband.status_nfsordma()
on_var = ''
check_nfs_array = []
if(form.getvalue("nfs_start")):
	nfs_name = form.getvalue("nfs_start")
	if(status_ipoib ==False):
		print"""<div id = 'id_trace_err'>"""
                print "First enable IP over IB Service!"
                print "</div>"
		print "<script>location.href = 'new_iframe_infiniband.py#tabs-2';</script>"
	elif(nfs_status == False):
		print"""<div id = 'id_trace_err'>"""
                print "First Start the NFS service! Go to Services option and start the NFS Service!"
                print "</div>"
                print "<script>location.href = 'new_iframe_infiniband.py#tabs-2';</script>"

	else:
	
		for x in share_infos:
			
			path = x['path']
			node = x['node']
			nfs_status_line = nfs.getstatus(path,sys_node_name)
			nfs_get= nfs_status_line['exports']
			check_nfs= nfs_get['use_nfs']
			check_nfs_array.append(check_nfs)
			if(check_nfs =='on'):
				on_var += "yes"
				enable_status_nfs=infiniband.enable_nfsordma()
				#print enable_status_nfs
				if(enable_status_nfs == True):
					print"""<div id = 'id_trace'>"""
					print "Successfully enabled NFS over RDMA!"
					print "</div>"
					print "<script>location.href = 'new_iframe_infiniband.py#tabs-2';</script>"
				else:
					print"""<div id = 'id_trace_err'>"""
					print "Error occured while enabling!"
					print "</div>"
					print "<script>location.href = 'new_iframe_infiniband.py#tabs-2';</script>"
		if "yes" not in on_var:
		#if 'on' not in check_nfs_array:
			print"""<div id = 'id_trace_err'>"""
			print "Please enable at least one NFS share!"
			print "</div>"
			print "<script>location.href = 'new_iframe_infiniband.py#tabs-2';</script>"
		#print 'Array:'+str(check_nfs_array)
		#print on_var
#-------------------------------------End----------------------------------------------

#--------------------Disable Nfs Over Rdma--------------------------------------------
if(form.getvalue("nfs_stop")):
        nfs_name = form.getvalue("nfs_stop")
        disable_status=infiniband.disable_nfsordma()

        if(disable_status == True):
                print"""<div id = 'id_trace'>"""
                print "Successfully disabled NFS over RDMA!"
                print "</div>"
                print "<script>location.href = 'new_iframe_infiniband.py#tabs-2';</script>"
        else:
                print"""<div id = 'id_trace_err'>"""
                print "Error occured while disabling!"
                print "</div>"
                print "<script>location.href = 'new_iframe_infiniband.py#tabs-2';</script>"

#-------------------------------------End------------------------------------------------

#--------------------------Status Nfs Over Rdma-------------------------------------------
#status1=infiniband.status_nfsordma()
status1 = infiniband.status_nfsordma()
if(status1 == True):
	status_chk1 = 'Enabled'
	display_color1 = 'green'
	display_img3 ='block'
	display_img2 ='none'
else:
	status_chk1 = 'Disabled'
	display_color1 = 'red'
	display_img3 ='none'
	display_img2 ='block'

#----------------------------------------End------------------------------------------

#import left_nav
print
print """

      <!--Right side body content starts from here-->
      <div class="rightsidecontainer">
        <!--<div class="insidepage-heading">Maintenance >> <span class="content">Infiniband</span></div>-->
        <!--tab srt-->
        <div class="searchresult-container">
	<div style="margin:0 0 0px 0;" class="topinputwrap-heading"><a class="demo" href ="#"><img src ="../images/help_icon1.png" style="width:13px;"><span class="tooltip" >
                 <table border="0">
        <tr>     
        <td class="text_css">This page lets you manage the "IP over IB" and the "NFS over RDMA" services.</td>
        </tr>
        </table>"""
if(check_ha == True):
	print"""
</span></a><p class = "gap_text">InfiniBand Information ("""+show_tn+""")</p>
	<span style="float:right; margin:-15.5px 0px 0 0;"><a onclick="return onclick_loader();" class="resource_links" href="https://"""+other_node_ip+"""/fs4/py/new_iframe_infiniband.py">"""+show_on+"""</a></span>

	</div>"""
else:
	print""" </span></a><p class = "gap_text">InfiniBand Information</p></div>"""
print"""
          <div class="infoheader">
            <div id="tabs">
              <ul>
                <li><a href="#tabs-1">Enable IP Over IB</a></li>
		<li><a href="#tabs-2">Enable NFS Over RDMA</a></li>
              </ul>
              <div id="tabs-1">
	<div class="form-container">
	      <!--<div class="topinputwrap-heading">Enable Ip Information </div>-->
          <div class="inputwrap">
         <div class="formleftside-content">
	
	<form name = "ip_over" method="post" action = "">
	<table>
	<tr>
	<td>
	<button onclick="return onclick_loader_button('ip_stat');" type="submit" name="ip_start" value = "ip_start"style="border:none; background-color:#FFF; cursor:pointer;">
	<img id="sync-static" src="../images/enable_ip.gif" style="width: 62px;display:"""+display_img1+""";" title="Enable"/>
	 <img id="sync-loading" style="display:none;" src="../images/sync-loading.GIF" alt="sync users" /></button><br/>
	<p id="sync-content" style="padding:10px 0 0 0;"></p>
	
	<button onclick="return onclick_loader_button('ip_st');" type="submit" name="ip_stop" value = "ip_stop"style="border:none; background-color:#FFF; cursor:pointer;">
<img id="sync-static1" src="../images/disable_ip.gif" style="width:54px;display:"""+display_img+""";" title="Disable" />
         <img id="sync-loading1" style="display:none;" src="../images/sync-loading.GIF" alt="sync users" /></button><br/>
	<p id="sync-content1" style="padding:10px 0 0 0;"></p>
	</td>
	<td style="float:right;margin-top:11px;">STATUS</td>
	</tr>
	<tr>
	<td><p style="margin-left: 540px; margin-top: -33px; width: 0px;color:"""+display_color+""";">"""+status_chk+"""</p></td>
	</tr>
	</table>
	</form>

        </div>
          </div>



</div>

	<p>&nbsp;</p>
              </div>
		<div id="tabs-2">
		<!--<div align='center' style='background-color:#585858; color:#FFF; height:70px; -moz-border-radius: 10px; -webkit-border-radius: 7px; border-radius: 7px; -khtml-border-radius: 7px; '><img src="../images/information4.png" height="30px" width="30px" alt='info'style="float:left; padding:20px 0 0 150px;"/> <span style="float:left; padding:25px 0 0 10px; font-size:14px; color:#FFF;">This Section is currently Under Development!</span></div>-->
		<div class="form-container">

          <div class="inputwrap">
         <div class="formleftside-content">

	 <style>
        #proppopUpDiv19 {position: fixed; background-color: #fff; width: 500px; z-index: 9002; padding: 5px;}
        #proppopUpDiv19 h5{width:100%; font-size:15px; color:#0070bd; text-align:center; font-weight:bold;}
        #proppopUpDiv19 span{ color:#FFFFFF; background-color:#0070bd; padding:1px 3px 0 3px; float:right;}
        #proppopUpDiv19 ul.idTabs{list-style:none; border:none; width:400px; margin:5px 0 0 0;}
        #proppopUpDiv19 ul.idTabs li{display:inline;}
        #proppopUpDiv19 ul.idTabs li a.link_tabs{display:inline; border:none; background-color:#D1D1D1; padding:10px;}

        </style>
        
        <div style="display: none;" id="blanket"></div>
        <form name="delete_share_form" method="post" action="">
        <div style="display: none;" id='proppopUpDiv19'>
        <h5>Confirm Box<span onclick="popup('proppopUpDiv19')" style="cursor:pointer;">X</span></h5>
        <div style="text-align:center; height:70px; margin:20px 0 20px 0;">
        This will reset all your NFS connections. Do you want to continue?<br/><br/>
        <button class="button_example" type="button" name = 'local_action_but'  id = 'local_action_but' value = 'Update' style="float:right; margin:0px 200px 0 0; " onclick="popup('proppopUpDiv19')" >No</button>
        <button class="button_example" type="submit" name = 'nfs_stop'  id = 'scan' value = 'ip_stop' style="float:right; " >Yes</button>
        </div>
        </form>

        </div>
	
	 <form name = "nfs_over" method="post" action = "">
        <table>
        <tr>
        <td>
        <button onclick="return onclick_loader_button('nfs_stat');" type="submit" name="nfs_start" value = "nfs_start"style="border:none; background-color:#FFF; cursor:pointer;">
        <img id="sync-static2" src="../images/enable_ip.gif" style="width: 62px;display:"""+display_img2+""";" title="Enable"/>
         <img id="sync-loading2" style="display:none;" src="../images/sync-loading.GIF" alt="sync users" /></button><br/>
        <p id="sync-content2" style="padding:10px 0 0 0;"></p>
        
        <!--<button onclick="return onclick_loader_button('nfs_st');" type="submit" name="nfs_stop" value = "ip_stop"style="border:none; background-color:#FFF; cursor:pointer;">-->
	<a onclick="popup('proppopUpDiv19')" href="#"><img src="../images/disable_ip.gif" style="width:54px;display:"""+display_img3+""";" title="Disable" title="NFS">
<!--<img id="sync-static1" src="../images/disable_ip.gif" style="width:54px;display:"""+display_img3+""";" title="Disable" />-->
         <img id="sync-loading3" style="display:none;" src="../images/sync-loading.GIF" alt="sync users" /></a>
        <p id="sync-content3" style="padding:10px 0 0 0;"></p>
        </td>
        <td style="float:right;margin-top:11px;">STATUS</td>
        </tr>
        <tr>
        <td><p style="margin-left: 540px; margin-top: -33px; width: 0px;color:"""+display_color1+""";">"""+status_chk1+"""</p></td>
        </tr>
        </table>
        </form>


        </div>
          </div>


                </div>
         <!--form container ends here-->
        <p>&nbsp;</p>

              </div>

<!-- ####### Sub Tabs Start ####### -->

<script>
$("#tabs, #subtabs").tabs();
$("#tabs, #subsubtabs").tabs();
</script>

<!-- ####### Sub Tabs End ####### -->

"""
