#!/usr/bin/python
import cgitb, sys,  common_methods, include_files, cgi 
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


iscsi_status = common_methods.get_iscsi_status();

display_create = ''
display_delete_target = ''

iscsi_enable_cmd = san_disk_funs.iscsi_enable(act='ENABLE')
random_target=san_disk_funs.get_iscsi_target_name()
#print 'Content-Type: text/html'
display_targets_list= san_disk_funs.iscsi_list_all_tgt()
#print display_targets_list
array_len = len(display_targets_list)

target_del = ''
target_select_delete = ''
check_but = ''
check_but_val = ''

#array_len = len(get_all_target)

if(form.getvalue("chk")):
	check_but = form.getvalue("chk")
	#print check_but
	iscsi_enable_cmd1 = san_disk_funs.iscsi_enable(act='ENABLE')
	#print iscsi_enable_cmd1
	if(check_but == "on"):
		check_but_val = 'checked'
	else:
		check_but_val = ""
#-------------------------iSCSI delete Target------------------ 
#--------------Get a button name "delete_target" and target name "hid_target_name_del" from form and the pass the target name "hid_target_name_del" in backend function for delete the target.
if(form.getvalue('delete_target')):
        target_del = form.getvalue('hid_target_name_del')
        xyz = []
        chk_used_disk = san_disk_funs.iscsi_used_disks_tgt(target_del)

        check_ini_list =san_disk_funs.iscsi_ini_list(target_del)
	
        if(len(check_ini_list) > 0):
                print"""<div id = 'id_trace_err'>"""
                print "Error occured while Deleting! Target contains initiator(s)"
                print "</div>"

        elif(len(chk_used_disk) > 0):
                print"""<div id = 'id_trace_err'>"""
                print "Error occured while Deleting! Target contains disk(s)"
                print "</div>"
                print "<script>location.href = 'iscsi_new.py';</script>"

        else:

                target_delete_msg = san_disk_funs.iscsi_rem_target(target_del)
                print"""<div id = 'id_trace'>"""
                print "Successfully Deleted the Target!"
                print "</div>"
                #print "<script>location.href = 'main.py?page=iscsi&act=delete_target_done';</script>"
                #display_create = 'none';
                #display_delete_target = 'block'
                print "<script>location.href = 'iscsi_new.py';</script>";
#-------------------------------End--------------------------------------------
#import left_nav
print
if(iscsi_status > 0):
	print """
		<div id="loader-div" style="text-align:center; display:none;" ><img style="margin-top:20%;" src="../images/ajax-loader.gif" /><br/> Loading...</div>
		 <link rel="stylesheet" href="../fancyBox/source/jquery.fancybox.css" type="text/css" media="screen" />
				<script type="text/javascript" src="../fancyBox/source/jquery.fancybox.pack.js"></script>
				<script type="text/javascript">
		$(document).ready(function() {
		$(".various").fancybox({
			maxWidth        : 800,
			maxHeight       : 600,
			fitToView       : false,
			width           : '102%',
			height          : '98%',
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


	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer" id="body-div">
		<!--<div class="insidepage-heading">San >> <span class="content">Configure Information</span></div>-->

		<div class="searchresult-container">
                        <div style="margin:0 0 0px 0;" class="topinputwrap-heading"><a class="demo" href ="#"><img src ="../images/help_icon1.png" style="width:13px;"><span class="tooltip" >

		<table border="0">
        <tr>
        <td class="text_css">This page allows you to create, view, configure and delete iSCSI targets.</td>
        </tr>
        </table>
		<!--tab srt-->"""
	if(check_ha == True):
		print""" </span></a><span class = "gap_text" style="color:#fff;margin-left:7px;">Target Information ("""+show_tn+""")</span>
			<span style="float:right; margin:0 0px 0 0;"><a  onclick="return onclick_loader();" class="resource_links" href="https://"""+other_node_ip+"""/fs4/py/iscsi_new.py">"""+show_on+"""</a></span>
			</div>"""
	else:
		print"""
			</span></a>Target Information
			</div>"""
	print"""
		  <div class="infoheader">
		    <div id="tabs">
		      <ul style="display:none;">
			<li><a href="#tabs-1">Shares</a></li>
		      </ul>
		      <div id="tabs-1">

		<!--form container starts here-->
		<div class="iframe-form-container">
		<div class="view_option"><a href = 'iframe_iscsi_target.py'><img title = 'Create Target' src = '../images/new-folder-9.png' /></a>

		<!--<a href="main.py?page=iscsi"><img src="../images/grid-view.png" height="30px" width="30px" title="Grid View"></a> <a href="iscsi_configure_list.py"><img src="../images/list-view.png" height="30px" width="30px" title="List View"></a>-->
	</div>
		<!--<div style="width:100px; float:left; text-align:right; margin:0 0 10px 0;">
		<hr style="width:50px; float:left; display:block; border:#2E64FE 1px solid; margin:10px 0 0 5px;"></hr>Node1<br/>
		<hr style="width:50px; float:left; display:block; border:#DF0174 1px solid; margin:10px 0 0 5px;"></hr>Node2<br/><br/>
		</div>-->

		  <div class="inputwrap">
		    <div class="formrightside-content">

	<nav id="menu1">

	<ul>"""

	i=1
	s=1

	if (display_targets_list !=[]):
		for x in display_targets_list:
			#print x
			target_name = x
			alias_name = target_name[target_name.rfind(':')+1:]
			#target_alias_name = x['name']
			#target_node_name = x['node']
			
			if("node1"):
				border_bottom = 'style="border-bottom:#2E64FE 2px solid;"'
			#elif(x["node"].strip() == "node2"):
			#	border_bottom = 'style="border-bottom:#DF0174 1px solid;"'
			#else:
			#	border_bottom = ''
			#exit();
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
			
			</style>

			<div style="display: none;" id="blanket"></div>
			<form name="delete_share_form" method="post" action="">
			<div style="display: none;" id='proppopUpDiv2"""+str(i)+"""'>
			<h5>Delete """+alias_name+""" <span onclick="popup('proppopUpDiv2"""+str(i)+"""')" style="cursor:pointer;">X</span></h5>
			<div style="border:#D1D1D1 1px solid; text-align:center; height:70px; margin:20px 0 20px 0;">
			Are you sure you want to delete """+alias_name+""" ?<br/><br/>
			<button class="button_example" type="button" name = 'local_action_but'  id = 'local_action_but' value = 'Update' style="float:right; margin:0px 200px 0 0; " onclick="popup('proppopUpDiv2"""+str(i)+"""')" >No</button>
			<button class="button_example" type="submit" name = 'delete_target'  id = 'delete_share' value = 'Update' style="float:right; " >Yes</button>
			<input type='hidden' name='hid_target_name_del' value='"""+x+"""' />
			</div>
			</form>

			</div>

			<div style="display: none;" id='proppopUpDiv3"""+str(i)+"""'>
			<h5>Alert Box<span onclick="popup('proppopUpDiv3"""+str(i)+"""')" style="cursor:pointer;">X</span></h5>
			<div style="text-align:center; height:30px; margin:20px 0 20px 0;">
			No User present! <a href="main.py?page=mu">Add User</a><br/><br/>
			</div>

			</div>"""


			
			#print """<li """+border_bottom+""" onclick="return folder_click("""+str(i)+""", """+str(array_len)+""", """+str(s)+""");"><a>"""+x['name']+"""</a>
			print """<li """+border_bottom+""" onclick="return folder_click("""+str(i)+""", """+str(array_len)+""", """+str(s)+""");"><a>"""+alias_name+"""</a>"""
			print"""
			<div id='"""+str(i)+"""' style="display:none;">
			<ul>"""
			#print """<li><a href="main.py?page=disk_iscsi&target="""+x+"""">Disk To Target</a></li>"""
			print"""<li><a class="various" data-fancybox-type="iframe" href="iframe_iscsi_disk_target.py?target="""+x+""""">Disk To Target</a></li>"""
			#print """<li><a href="main.py?page=prop_iscsi&target="""+x+"""">properties</a></li>"""
			print"""<li><a class="various" data-fancybox-type="iframe" href="iframe_initiator.py?target="""+x+"""">Initiator</a></li>"""
			print"""<li><a class="various" data-fancybox-type="iframe" href="iframe_iscsi_authentication.py?target="""+x+"""">Authentication</a></li>"""
			#print"""<li><a class="various" data-fancybox-type="iframe" href="iframe_iscsi_properties.py?target="""+x+"""">Properties</a></li>"""
			print"""<li><a class="various" data-fancybox-type="iframe" href="iframe_iscsi_properties_new.py?target="""+x+"""">Properties</a></li>"""
			#print"""<li><a class="various" data-fancybox-type="iframe" href="#?target="""+x+"""">Properties</a></li>"""
			#print"""<li><a href="main.py?page=det_iscsi&detail="target_name">Target Information</a></li>"""
			print"""<li><a class="various" data-fancybox-type="iframe" href="iscsi_list.py?target="""+x+"""">Target Information</a></li>"""
			print"""<li><a class="various" data-fancybox-type="iframe" href="iscsi_session.py?target="""+x+"""">Session Information</a></li>"""
			#print"""<li><a href="main.py?page=ses_iscsi&session="target_name">Session Information</a></li>"""
			print"""<li><a onclick="popup('proppopUpDiv2"""+str(i)+"""')" href="#">Delete</a></li>"""
			print"""
			</ul>
			</div>

			</li>"""
			i=i+1
	else:
		print"""<div style="text-align:center; height:30px; margin:20px 0 20px 0;">No-Target Found !<a href="iframe_iscsi_target.py" style="text-decoration:underline;">Create Target</a></div>"""
		
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
	print"""
<form name = "nm" method="post" action = '' />
<table width="685" style="border:#D1D1D1 1px solid;margin-left:1%;" align ="center">
<tr>
<td>
<div style="height:30px; margin:20px 0 20px 0;width:625px;font-size:15px;"><input type="checkbox" name="chk"  """+check_but_val+""" onchange='this.form.submit()' />Enable</div>
</td>
</tr>
</table>
</form>
"""
	#print"""<form name = "frm" ><div style="text-align:center; height:30px; margin:20px 0 20px 0;width:625px;font-size:20px;"><button type="submit" name="san_start" value="restart-nfs" style="border:none; background-color:#FFF; cursor:pointer;text-align:center;margin-left:220px;"><img src="../images/restart-services-fs4.png" alt="start SAN" /></button><br/><p style="margin-left:234px;"></p></button></div></form>"""
