#!/usr/bin/python
import cgitb, sys,  common_methods, cgi, include_files
cgitb.enable()

form = cgi.FieldStorage()
sys.path.append('/var/nasexe/python/')
import tools
from tools import db

sys.path.append('/var/nasexe/storage')
import storage_op
import sys,os
from lvm_infos import *
from functions import *
import san_disk_funs

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

random_target=san_disk_funs.get_iscsi_target_name()
#print 'Content-Type: text/html'
display_targets_list= san_disk_funs.iscsi_list_all_tgt()
array_len = len(display_targets_list)

target_del = ''
target_select_delete = ''

#print 'Content-Type: text/html'



#get_all_shares = common_methods.get_share_names()
get_all_shares = {'id': 0, 'shares': [{'comment': '', 'node': 'node1', 'name': 'sunny', 'ftp': 1, 'tstamp':'', 'nfs': 0, 'date': '', 'path': '/storage/lotus_n1/sunny', 'afp': 0, 'smb': 0, 'size': '0'}, {'comment': '', 'node': 'node2', 'name': 'rahul', 'ftp': 0, 'tstamp':'', 'nfs': 0, 'date': '', 'path': '/storage/lotus_n2/rahul', 'afp': 0, 'smb': 0, 'size': ''}]}
array_len = len(get_all_shares)

#conn = common_methods.conn_status()
#conn = authentication.get_auth_type()

#import left_nav
print
print """

      <!--Right side body content starts from here-->
      <div class="rightsidecontainer">
	<!--tab srt-->
	<div class="searchresult-container">
	 <div style="margin:0 0 0px 0;" class="topinputwrap-heading">Target Information of """+show_tn+"""
                <span style="float:right; margin:0 0px 0 0;"><a class="resource_links" href="https://"""+other_node_ip+"""/fs4/py/iscsi_new.py">"""+show_on+"""</a></span>
        </div>
	  <div class="infoheader">
	    <div id="tabs">
	      <ul>
		<li><a href="#tabs-1">Configure List</a></li>
	      </ul>
	      <div id="tabs-1">

	<!--form container starts here-->
	<div class="form-container">
	<div class="view_option"><a href = 'iframe_iscsi_target.py'><img title = 'Create Target' src = '../images/new-folder-9.png' /></a><a href="iscsi_new.py"><img src="../images/grid-view.png" height="30px" width="30px" title="Grid View" /></a> <a href="iscsi_configure_list.py"><img src="../images/list-view.png" height="30px" width="30px" title="List View" /></a></div>
	  <div class="inputwrap">
	    <div class="formrightside-content">"""
if(get_all_shares["shares"] != []):
	print """<table style="border:#D1D1D1 1px solid; width:700px; margin:0 0 0 10px;">
		<tr style="border-bottom:#D1D1D1 1px solid;">
			<th align="left" style="border-bottom:#D1D1D1 1px solid;">Name</th>
			<th align="left" style="border-bottom:#D1D1D1 1px solid;">Size</th>
			<th align="left" style="border-bottom:#D1D1D1 1px solid;">Date Modified</th>
			<!--<th align="left" style="border-bottom:#D1D1D1 1px solid;">Protocols</th>-->
			<th align="left" style="border-bottom:#D1D1D1 1px solid;">Disk Name</th>
	</tr>"""
	


i=1
s=1
if (display_targets_list !=[]):
	for x in display_targets_list:
		target_name = x
		alias_name = target_name[target_name.rfind(':')+1:]
		#get_share_perm = share_permissions.get_smb_perms(x["name"])
		#get_afp_perm = share_permissions.get_afp_perms(x["name"])

		#get_all_protocols = tools.get_all_protocols(x["name"], x["path"])

		#get_mount_point = prjquota.get_mountpoint(x["path"])
		#test_mount = prjquota.test_mount(get_mount_point)

		#split_path = x["path"].split("/")
		#disk_name = x["path"][:x["path"].rfind('/')]
		#disk_name = disk_name[disk_name.rfind('/')+1:]
		#disk_name = split_path[2]

		print """<tr>
		<td>
		<nav id="menulist1">
		<ul>

		<style>
		#proppopUpDiv"""+str(i)+""" {position: fixed; background-color: #fff; width: 500px; z-index: 9002; padding: 5px; top:100px !important;}
		#proppopUpDiv"""+str(i)+""" h5{width:100%; font-size:15px; color:#0070bd; text-align:center; font-weight:bold;}
		#proppopUpDiv"""+str(i)+""" span{ color:#FFFFFF; background-color:#0070bd; padding:1px 3px 0 3px; float:right;}
		#proppopUpDiv"""+str(i)+""" ul.idTabs{list-style:none; border:none; width:400px; margin:5px 0 0 0;}
		#proppopUpDiv"""+str(i)+""" ul.idTabs li{display:inline;}
		#proppopUpDiv"""+str(i)+""" ul.idTabs li a.link_tabs{display:inline; border:none; background-color:#D1D1D1; padding:10px;}
		#proppopUpDiv"""+str(i)+""" ul.idTabs li a.link_tabs:hover{background-color:#cfbdbd;}

		#proppopUpDiv2"""+str(i)+""" {position: fixed; background-color: #fff; width: 500px; z-index: 9002; padding: 5px; margin-top:30px !important;}
		#proppopUpDiv2"""+str(i)+""" h5{width:100%; font-size:15px; color:#0070bd; text-align:center; font-weight:bold;}
		#proppopUpDiv2"""+str(i)+""" span{ color:#FFFFFF; background-color:#0070bd; padding:1px 3px 0 3px; float:right;}
		#proppopUpDiv2"""+str(i)+""" ul.idTabs{list-style:none; border:none; width:400px; margin:5px 0 0 0;}
		#proppopUpDiv2"""+str(i)+""" ul.idTabs li{display:inline;}
		#proppopUpDiv2"""+str(i)+""" ul.idTabs li a.link_tabs{display:inline; border:none; background-color:#D1D1D1; padding:10px;}
		#proppopUpDiv2"""+str(i)+""" ul.idTabs li a.link_tabs:hover{background-color:#cfbdbd;}

		
		</style>

		<div style="display: none;" id="blanket"></div>

		<form name="delete_share_form" method="post" action="">
		<div style="display: none; " id='proppopUpDiv2"""+str(i)+"""'>
		<h5>Delete "Target Name"<span onclick="popup('proppopUpDiv2"""+str(i)+"""')" style="cursor:pointer;">X</span></h5>
		<div style="border:#D1D1D1 1px solid; text-align:center; height:70px; margin:20px 0 20px 0;">
		Are you sure you want to delete "Target NAME" ?<br/><br/>
		<button class="button_example" type="button" name = 'local_action_but'  id = 'local_action_but' value = 'Update' style="float:right; margin:0px 200px 0 0; " onclick="popup('proppopUpDiv2"""+str(i)+"""')" >No</button>
		<button class="button_example" type="submit" name = 'delete_share'  id = 'delete_share' value = 'Update' style="float:right; " >Yes</button>
		<input type='hidden' name='hid_share_name_to_del' value='"""+x["name"]+"""' />
		<input type='hidden' name='hid_share_path_to_del' value='"""+x["path"]+"""' />
		</div>
		</form>

		</div>"""

		

		print """</div>


		<li onclick="return folder_click("""+str(i)+""", """+str(array_len)+""", """+str(s)+""");"><a>Targetname</a>

		<div id='"""+str(i)+"""' style="display:none;">
		<ul>"""
		print """<li><a href="main.py?page=disk_iscsi&disk="target_name">Disk To Target</a></li>"""
		print """<li><a href="main.py?page=prop_iscsi&sprop="target_name">properties</a></li>"""
		#print"""<li><a href="main.py?page=det_iscsi&detail="target_name">Target Information</a></li>"""
		print"""<li><a class="various" data-fancybox-type="iframe" href="iscsi_list.py?target="target_n"">Target Information</a></li>"""
		print"""<li><a class="various" data-fancybox-type="iframe" href="iscsi_session.py?target="target_n"">Session Information</a></li>"""
		#print"""<li><a href="main.py?page=ses_iscsi&session="target_name">Session Information</a></li>"""

		print """
		</ul>
		</div>

		</li>
				
		</ul>
		</nav>


		</td>
		<td>test</td>
		<td>date</td>
		<td>diskname</td>
		</tr>"""
		i=i+1

print """
		</table>


	</div>"""



print"""          </div>
</div>
<!--form container ends here-->
<p>&nbsp;</p>
      </div>
"""
