#!/usr/bin/python
import cgitb, sys, common_methods, include_files
cgitb.enable()
#form = cgi.FieldStorage()
sys.path.append('/var/nasexe/python/')
import smb
import afp
import nfs 
import ftp_auth
import anon_ftp
import tools
import manage_users
import commons
from tools import acl
from tools import share_permissions
from tools import prjquota
from tools import db
#status = prjquota.used_prjs()
#print status

#sys.path.append('/var/nasexe/python/tools/')
#import acl

#print 'Content-Type: text/html'

o_read_val = 0
o_write_val = 0
o_execute_val = 0
g_read_val = 0
g_write_val = 0
g_execute_val = 0
ot_read_val = 0
ot_write_val = 0
ot_execute_val = 0
get_sub_inherit = "no"

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

#-------------------------------------- Delete Share End -----------------------------------------#



#get_all_shares = common_methods.get_share_names()
#array_len = len(get_all_shares)

#get_shares = tools.get_all_shares(debug=True)
#if(get_shares["id"] == 0):
        #get_all_shares = tools.get_share_date_size_info(get_shares['shares'])
	#array_len = len(get_all_shares["shares"])
	#print array_len

#get_all_shares = {'id': 0, 'shares': [{'comment': 'apple share from FS2', 'node': 'node1', 'name': 'apple', 'ftp': 1, 'tstamp': '', 'nfs': 0, 'date': 'Jun 6', 'path': '/storage/lotus_n1/apple', 'afp': 1, 'smb': 1, 'size': '68K'}, {'comment': 'orange share from FS2', 'node': 'node2', 'name': 'orange', 'ftp': 0, 'tstamp': '', 'nfs': 0, 'date': '', 'path': '/storage/lotus_n2/orange', 'afp': 0, 'smb': 0, 'size': ''}]}

get_all_shares = {'id': 0, 'shares': [{'comment': '', 'node': 'node1', 'name': 'sunny', 'ftp': 1, 'tstamp':'', 'nfs': 0, 'date': '', 'path': '/storage/lotus_n1/sunny', 'afp': 0, 'smb': 0, 'size': '0'}, {'comment': '', 'node': 'node2', 'name': 'rahul', 'ftp': 0, 'tstamp':'', 'nfs': 0, 'date': '', 'path': '/storage/lotus_n2/rahul', 'afp': 0, 'smb': 0, 'size': ''}]}
get_all_users = manage_users.get_smb_users()
array_len = len(get_all_shares["shares"])

#get_all_groups = manage_users.get_sys_groups()

#conn = common_methods.conn_status()

#import left_nav
print

print """
	 <link rel="stylesheet" href="../fancyBox/source/jquery.fancybox.css" type="text/css" media="screen" />
                        <script type="text/javascript" src="../fancyBox/source/jquery.fancybox.pack.js"></script>
                        <script type="text/javascript">
        $(document).ready(function() {
        $(".various").fancybox({
                maxWidth        : 800,
                maxHeight       : 600,
                fitToView       : false,
                width           : '100%',
                height          : '100%',
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
      <div class="rightsidecontainer">
	<!--<div class="insidepage-heading">San >> <span class="content">Configure Information</span></div>-->
	<div style="margin-left:5px;" class="iframe-insidepage-heading">San<span style="color:#000; "> >> Iscsi >> </span> Target >> """+show_tn+"""  <span style="float:right; margin:0 0px 0 0;width:150px;margin-right:-99%;"><a class="resource_links" href="https://"""+other_node_ip+"""/fs4/py/iframe_iscsi_new.py">"""+show_on+"""</a></span>
</div>
	<!--tab srt-->
	<div class="searchresult-container">
	  <div class="infoheader">
	    <div id="tabs">
	      <ul style="display:none;">
		<li><a href="#tabs-1">Shares</a></li>
	      </ul>
	      <div id="tabs-1">

	<!--form container starts here-->
	<div class="iframe-form-container">
	<div class="view_option"><a href = 'main.py?page=target_iscsi'><img title = 'Create Target' src = '../images/new-folder-9.png' /></a>

	<a href="main.py?page=iscsi"><img src="../images/grid-view.png" height="30px" width="30px" title="Grid View"></a> <a href="main.py?page=lst_iscsi"><img src="../images/list-view.png" height="30px" width="30px" title="List View"></a>
</div>
	<div style="width:100px; float:left; text-align:right; margin:0 0 10px 0;">
	<hr style="width:50px; float:left; display:block; border:#2E64FE 1px solid; margin:10px 0 0 5px;"></hr>Node1<br/>
	<hr style="width:50px; float:left; display:block; border:#DF0174 1px solid; margin:10px 0 0 5px;"></hr>Node2<br/><br/>
	</div>

	  <div class="inputwrap">
	    <div class="formrightside-content">

<nav id="menu1">

<ul>"""

i=1
s=1
for x in get_all_shares["shares"]:
	#get_share_perm = share_permissions.get_smb_perms(x["name"])
	#get_afp_perm = share_permissions.get_afp_perms(x["name"])

	#get_mount_point = prjquota.get_mountpoint(x["path"])
	#get_mount_point = ''
	#test_mount = ''
	#test_mount = prjquota.test_mount(get_mount_point)
	
	if(x["node"].strip() == "node1"):
		border_bottom = 'style="border-bottom:#2E64FE 1px solid;"'
	elif(x["node"].strip() == "node2"):
		border_bottom = 'style="border-bottom:#DF0174 1px solid;"'
	else:
		border_bottom = ''

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
	<h5>Delete "TargetNAME"<span onclick="popup('proppopUpDiv2"""+str(i)+"""')" style="cursor:pointer;">X</span></h5>
	<div style="border:#D1D1D1 1px solid; text-align:center; height:70px; margin:20px 0 20px 0;">
        Are you sure you want to delete "Target Name" ?<br/><br/>
	<button class="button_example" type="button" name = 'local_action_but'  id = 'local_action_but' value = 'Update' style="float:right; margin:0px 200px 0 0; " onclick="popup('proppopUpDiv2"""+str(i)+"""')" >No</button>
        <button class="button_example" type="submit" name = 'delete_share'  id = 'delete_share' value = 'Update' style="float:right; " >Yes</button>
	<input type='hidden' name='hid_share_name_to_del' value='"""+x["name"]+"""' />
	<input type='hidden' name='hid_share_path_to_del' value='"""+x["path"]+"""' />
        </div>
	</form>

	</div>

	<div style="display: none;" id='proppopUpDiv3"""+str(i)+"""'>
	<h5>Alert Box<span onclick="popup('proppopUpDiv3"""+str(i)+"""')" style="cursor:pointer;">X</span></h5>
	<div style="text-align:center; height:30px; margin:20px 0 20px 0;">
        No User present! <a href="main.py?page=mu">Add User</a><br/><br/>
        </div>

	</div>"""

	smb_status = smb.is_configured(x["name"],debug=False)
	afp_status = afp.is_configured(x["name"])

	print """

	<div style="display: none;" id='proppopUpDiv"""+str(i)+"""'>
	<h5><span onclick="popup('proppopUpDiv"""+str(i)+"""')" style="cursor:pointer;">X</span></h5>

	<script type="text/javascript" src="popup/jquery-tabs.js"></script>
	<ul class="idTabs">"""
	print """<li><a href='#jquery"""+str(i)+"""' class="link_tabs">SMB Permissions</a></li> """

	print """<li><a href='#official"""+str(i)+"""' class="link_tabs">AFP Permissions</a></li>"""


	print """</ul> """
	
	print """</div>"""

	
	#print """<li """+border_bottom+""" onclick="return folder_click("""+str(i)+""", """+str(array_len)+""", """+str(s)+""");"><a>"""+x['name']+"""</a>
	print """<li """+border_bottom+""" onclick="return folder_click("""+str(i)+""", """+str(array_len)+""", """+str(s)+""");"><a>Iscsi</a>"""
	print"""
	<div id='"""+str(i)+"""' style="display:none;">
	<ul>"""
	print"""<li><a class="various" data-fancybox-type="iframe" href="iscsi_disk_target.py?target="target_n"">Disk To Target</a></li>"""
        #print """<li><a href="main.py?page=prop_iscsi&sprop="target_name">properties</a></li>"""
        print"""<li><a class="various" data-fancybox-type="iframe" href="iscsi_properties.py?target="target_n"">Properties</a></li>"""
        #print"""<li><a href="main.py?page=det_iscsi&detail="target_name">Target Information</a></li>"""
        print"""<li><a class="various" data-fancybox-type="iframe" href="iscsi_list.py?target="target_n"">Target Information</a></li>"""
        print"""<li><a class="various" data-fancybox-type="iframe" href="iscsi_session.py?target="target_n"">Session Information</a></li>"""
        #print"""<li><a href="main.py?page=ses_iscsi&session="target_name">Session Information</a></li>"""
        print"""<li><a onclick="popup('proppopUpDiv2"""+str(i)+"""')" href="#">Delete</a></li>"""
	print"""
	</ul>
	</div>

	</li>"""
	i=i+1
	
print """


</ul>

</nav>

	</div>"""



print"""          </div>
</div>
<!--form container ends here-->
<p>&nbsp;</p>
      </div>
</div>
  </div>
"""
