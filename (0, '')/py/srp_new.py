#!/usr/bin/python
import cgitb, sys, common_methods, include_files, cgi
cgitb.enable()

sys.path.append('/var/nasexe/python/')
import tools
from tools import db

sys.path.append('/var/nasexe/storage')
import storage_op
import sys,os
from lvm_infos import *
from functions import *
import san_disk_funs

check_ha = tools.check_ha()

form = cgi.FieldStorage()

srp_target=san_disk_funs.ib_list_targets()



check_srp =''
target_del = ''

#----------------------Check the Srp Status------------------------
check_srp = san_disk_funs.ib_target_status();
#-------------------------End---------------------------------
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

display_srp_target=san_disk_funs.ib_list_targets()
array_len = len(display_srp_target)

conn = common_methods.conn_status()

#------------------------- Enable Srp Target-------------------------
if(form.getvalue('action_butt')):
        srp_target_name= form.getvalue('hid_target_enable')
        if(srp_target_name == None):
                print
        else:

                enable_status=san_disk_funs.ib_enable_disable(targets=srp_target_name, opp='ENABLE')
                #print 'Single:'+str(enable_status)
                if(enable_status == True):
                        print"""<div id = 'id_trace'>"""
                        print " <font color='darkred'></b></font> You have Successfully Enabled the Target!"
                        print "</div>"
                        print "<script>location.href = 'srp_new.py';</script>";
                else:
                        print"""<div id = 'id_trace_err'>"""

                        print "Error occured while enable the Target!"
                        print "</div>"
                        print "<script>location.href = 'srp_new.py';</script>";

#-------------------------------------End------------------------------------------------------------

#---------------------------------- Disable Srp-----------------------   
if(form.getvalue('action_disable_butt')):
        srp_disable_name = form.getvalue('hid_target_disable')
        chk_used_disk = san_disk_funs.ib_used_disks_tgt(srp_disable_name)

        check_ini_list =san_disk_funs.ib_ini_list(srp_disable_name)

        if(len(check_ini_list) > 0):
                print"""<div id = 'id_trace_err'>"""
                print "Error occured while Disable! Target contains initiator(s)"
                print "</div>"
                print "<script>location.href = 'srp_new.py';</script>";

        elif(len(chk_used_disk) > 0):
                print"""<div id = 'id_trace_err'>"""
                print "Error occured while Disable! Target contains disk(s)"
                print "</div>"
                print "<script>location.href = 'srp_new.py';</script>";
        else:
                if(srp_disable_name == None):
                        print

                else:
                        disable_status = san_disk_funs.ib_enable_disable(srp_disable_name,opp='DISABLE')
                        if(disable_status == True):
                                print"""<div id = 'id_trace'>"""
                                print " <font color='darkred'></b></font> You have Successfully Disabled the Target!"
                                print "</div>"
                                print "<script>location.href = 'srp_new.py';</script>";

                        else:
                                print"""<div id = 'id_trace_err'>"""
                                print "Error occured while Disabled the Target!"
                                print "</div>"
                                print "<script>location.href = 'srp_new.py';</script>";



#------------------------------------------------------End--------------------------------------------------

#import left_nav
print
if(check_srp !=[]):
	print """
		 <link rel="stylesheet" href="../fancyBox/source/jquery.fancybox.css" type="text/css" media="screen" />
				<script type="text/javascript" src="../fancyBox/source/jquery.fancybox.pack.js"></script>
				<script type="text/javascript">
		$(document).ready(function() {
		$(".various").fancybox({
			maxWidth        : 800,
			maxHeight       : 600,
			fitToView       : false,
			width           : '720px',
			height          : '420px',
			autoSize        : false,
			closeClick      : false,
			openEffect      : 'none',
			closeEffect     : 'none',
			'afterClose':function () {
			 // window.location.reload();
			 },
			helpers   : { 
			overlay  :       {closeClick: false} // prevents closing when clicking OUTSIDE fancybox 
				     }
			
	       });

		});
		</script>

		<div id="loader-div" style="text-align:center; display:none;" ><img style="margin-top:20%;" src="../images/ajax-loader.gif" /><br/> Loading...</div>
	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer" id="body-div">
		<!--<div class="insidepage-heading">San >> <span class="content">Configure Information</span></div>-->
		<!--tab srt-->
		<div class="searchresult-container">
		<div style="margin:0 0 0px 0;" class="topinputwrap-heading"><a class="demo" href ="#"><img src ="../images/help_icon1.png" style="width:13px;"><span class="tooltip" >
		<table border="0">

		<tr>
        <td style="font-size: medium;text-align:start;">Srp Information:</td>
        </tr>
        <tr>
        <td class="text_css">In this Page Information about the Srp.when Click bootom of Srp icon then some option is popup like Disk to target,Initiators,Target Information and Session Information.Choose the given option to Start work with.</td>
        </tr>

        </table>

		"""
	if(check_ha == True):
		print"""</span></a><span class = "gap_text" style="color:#fff;margin-left:7px;">Target Information ("""+show_tn+""")</span>
			<span style="float:right; margin:0 0px 0 0;"><a  onclick="return onclick_loader();" class="resource_links" href="https://"""+other_node_ip+"""/fs4/py/srp_new.py">"""+show_on+"""</a></span>
		</div>"""
	else:
		
		print"""</span></a>Target Information</div>"""
	print"""
		  <div class="infoheader">
		    <div id="tabs">
		      <ul style="display:none;">
			<li><a href="#tabs-1">Shares</a></li>
		      </ul>
		      <div id="tabs-1">

		<!--form container starts here-->
		<div class="iframe-form-container">
		<div class="view_option"><!--<a href = 'iframe_srp_target.py'><img title = 'Create Target' src = '../images/new-folder-9.png' /></a>

		<a href="main.py?page=stat_srp"><img src="../images/grid-view.png" height="30px" width="30px" title="Grid View"></a> <a href="main.py?page=list_srp"><img src="../images/list-view.png" height="30px" width="30px" title="List View"></a>-->
	</div>"""
	if(check_srp !=[]):
		disable_check = 'block'
	else:
		disable_check = 'none'
	print"""
		 <div style="width:100px; float:left; text-align:right; margin:0 0 10px 0;display:"""+disable_check+""" ">
		<hr style="width:50px; float:left; display:block; border:green 1px solid; margin:5% 0 0 5px;"></hr>Enable<br/>
		<hr style="width:50px; float:left; display:block; border:#AC000E 1px solid; margin:5% 0 0 5px;"></hr>Disable<br/><br/>
		</div>

		  <div class="inputwrap">
		    <div class="formrightside-content">

	<nav id="menu2">

	<ul>"""

	i=1
	s=1
	if(check_srp !=[]):
		for x in check_srp:
			keys_val = x.keys()
			keys_val = str(keys_val).replace('[', '')
			keys_val = str(keys_val).replace(']', '')
			keys_val = str(keys_val).replace("'", "")
			#print keys_val
			value_check = x.values()
			#print value_check
			if("node1") :
				border_bottom = 'style="border-bottom:#AC000E 2px solid;"'
				#border_bottom = 'style="border-bottom:#2E64FE 1px solid;"'
			#else:
				
				border_bottom1 = 'style="border-bottom:green 2px solid;"'
			print """
			<style>
			#proppopUpDiv"""+str(i)+""" {position: fixed; background-color: #fff; width: 500px; z-index: 9002; padding: 5px;}
			#proppopUpDiv"""+str(i)+""" h5{width:100%; font-size:15px; color:#0070bd; text-align:center; font-weight:bold;}
			#proppopUpDiv"""+str(i)+""" span{ color:#FFFFFF; background-color:#0070bd; padding:1px 3px 0 3px; float:right;}
			#proppopUpDiv"""+str(i)+""" ul.idTabs{list-style:none; border:none; width:400px; margin:5px 0 0 0;}
			#proppopUpDiv"""+str(i)+""" ul.idTabs li{display:inline;}
			#proppopUpDiv"""+str(i)+""" ul.idTabs li a.link_tabs{display:inline; border:none; background-color:#D1D1D1; padding:10px;}
			#proppopUpDiv"""+str(i)+""" ul.idTabs li a.link_tabs:hover{background-color:#cfbdbd;}
			
			#proppopUpDiv2"""+str(i)+""" {position: fixed; background-color: #fff; width: 500px; z-index: 9002; padding: 5px;}
			#proppopUpDiv2"""+str(i)+""" h5{width:100%; font-size:15px; color:#0070bd; text-align:center; font-weight:bold;}
			#proppopUpDiv2"""+str(i)+""" span{ color:#FFFFFF; background-color:#0070bd; padding:1px 3px 0 3px; float:right;}
			#proppopUpDiv2"""+str(i)+""" ul.idTabs{list-style:none; border:none; width:400px; margin:5px 0 0 0;}
			#proppopUpDiv2"""+str(i)+""" ul.idTabs li{display:inline;}
			#proppopUpDiv2"""+str(i)+""" ul.idTabs li a.link_tabs{display:inline; border:none; background-color:#D1D1D1; padding:10px;}
			#proppopUpDiv2"""+str(i)+""" ul.idTabs li a.link_tabs:hover{background-color:#cfbdbd;}
			
			#proppopUpDiv3"""+str(i)+""" {position: fixed; background-color: #fff; width: 500px; z-index: 9002; padding: 5px;}
			#proppopUpDiv3"""+str(i)+""" h5{width:100%; font-size:15px; color:#0070bd; text-align:center; font-weight:bold;}
			#proppopUpDiv3"""+str(i)+""" span{ color:#FFFFFF; background-color:#0070bd; padding:1px 3px 0 3px; float:right;}
			#proppopUpDiv3"""+str(i)+""" ul.idTabs{list-style:none; border:none; width:400px; margin:5px 0 0 0;}
			#proppopUpDiv3"""+str(i)+""" ul.idTabs li{display:inline;}
			#proppopUpDiv3"""+str(i)+""" ul.idTabs li a.link_tabs{display:inline; border:none; background-color:#D1D1D1; padding:10px;}
			#proppopUpDiv3"""+str(i)+""" ul.idTabs li a.link_tabs:hover{background-color:#cfbdbd;}
			
			#proppopUpDiv4"""+str(i)+""" {position: fixed; background-color: #fff; width: 500px; z-index: 9002; padding: 5px;}
			#proppopUpDiv4"""+str(i)+""" h5{width:100%; font-size:15px; color:#0070bd; text-align:center; font-weight:bold;}
			#proppopUpDiv4"""+str(i)+""" span{ color:#FFFFFF; background-color:#0070bd; padding:1px 3px 0 3px; float:right;}
			#proppopUpDiv4"""+str(i)+""" ul.idTabs{list-style:none; border:none; width:400px; margin:5px 0 0 0;}
			#proppopUpDiv4"""+str(i)+""" ul.idTabs li{display:inline;}
			#proppopUpDiv4"""+str(i)+""" ul.idTabs li a.link_tabs{display:inline; border:none; background-color:#D1D1D1; padding:10px;}
			#proppopUpDiv4"""+str(i)+""" ul.idTabs li a.link_tabs:hover{background-color:#cfbdbd;}
			
			</style>

			<div style="display: none;" id="blanket"></div>
			<form name="enable_srp" method="post" action="">
			<div style="display: none;" id='proppopUpDiv2"""+str(i)+"""'>
			<h5>Enable """+str(keys_val)+"""<span onclick="popup('proppopUpDiv2"""+str(i)+"""')" style="cursor:pointer;">X</span></h5>
			<div style="border:#D1D1D1 1px solid; text-align:center; height:70px; margin:20px 0 20px 0;">
			Are you sure you want to Enable """+str(keys_val)+""" ?<br/><br/>
			<button class="button_example" type="button" name = 'local_action_but'  id = 'local_action_but' value = 'Update' style="float:right; margin:0px 200px 0 0; " onclick="popup('proppopUpDiv2"""+str(i)+"""')" >No</button>
			<button class="button_example" type="submit" name = 'action_butt'  id = 'action_butt' value = 'Update' style="float:right; " >Yes</button>
			<input type='hidden' name='hid_target_enable' value='"""+str(keys_val)+"""' />
			</div>
			</form>

			</div>

			<form name="disable_srp" method="post" action="">
			<div style="display: none;" id='proppopUpDiv3"""+str(i)+"""'>
			<h5>Disable """+str(keys_val)+"""<span onclick="popup('proppopUpDiv3"""+str(i)+"""')" style="cursor:pointer;">X</span></h5>
			<div style="border:#D1D1D1 1px solid; text-align:center; height:70px; margin:20px 0 20px 0;">
			Are you sure you want to Disable """+str(keys_val)+""" ?<br/><br/>
			<button class="button_example" type="button" name = 'local_action_but'  id = 'local_action_but' value = 'Update' style="float:right; margin:0px 200px 0 0; " onclick="popup('proppopUpDiv3"""+str(i)+"""')" >No</button>
			<button class="button_example" type="submit" name = 'action_disable_butt'  id = 'action_disable_butt' value = 'Update' style="float:right; " >Yes</button>
			<input type='hidden' name='hid_target_disable' value='"""+str(keys_val)+"""' />
			</div>
			</form>

			</div>"""
			if(value_check == ['0']):
				print """<li """+border_bottom+""" onclick="return folder_click("""+str(i)+""", """+str(array_len)+""", """+str(s)+""");"><a></a>"""
			else:
				
				print """<li """+border_bottom1+""" onclick="return folder_click("""+str(i)+""", """+str(array_len)+""", """+str(s)+""");"><a></a>"""
			print"""
			<div id='"""+str(i)+"""' style="display:none;">
			<ul style="margin-left:-1px; margin-top: 0.5px;">"""
			print"""<li><a class="various" data-fancybox-type="iframe" href="iframe_srp_disk_target.py?target="""+str(keys_val)+""""">Disk To Target</a></li>"""
			print"""<li><a class="various" data-fancybox-type="iframe" href="iframe_srp_initiator.py?target="""+str(keys_val)+""""">Initiator</a></li>"""
			print"""<li><a class="various" data-fancybox-type="iframe" href="iframe_srp_list.py?target="""+str(keys_val)+""""">Target Information</a></li>"""
			print"""<li><a class="various" data-fancybox-type="iframe" href="iframe_srp_session.py?target="""+str(keys_val)+""""">Session Information</a></li>"""
			if(value_check == ['0']):
				print"""<li><a onclick="popup('proppopUpDiv2"""+str(i)+"""')" href="#">Enable</a></li>"""
			else:
				print"""<li><a onclick="popup('proppopUpDiv3"""+str(i)+"""')" href="#">Disable</a></li>"""
					
			print"""
			</ul>
			</div>

			</li>"""
			i=i+1
	else:
		print "<div style='text-align:center;'>No-Target Found</div>"
		
	print """


	</ul>

	</nav>

		</div>"""



	print"""          </div>
	</div>
	<!--form container ends here-->
	<p>&nbsp;</p>
	      </div>
	"""
else:
	print"""<div style="text-align:center; height:30px; margin:139px 0 20px 0;width:787px;font-size:20px;">No-Target Found!</div>"""
	#print """<div style="text-align:center; margin:10px 0 10px 0; width:600px;">No Target is available!</div>"""
	#print"<div style = 'padding:20px 0 0 267px; font-size:12px;text-decoration:underline;'>There in No Target!</div>"
        #print"""<div style="text-align:center; height:30px; margin:20px 0 20px 0;width:625px;font-size:20px;">Srp not Started !<a href="iframe_start_services.py" style="text-decoration:underline;color:#89A6C4;">Start SAN Services</a></div>"""
