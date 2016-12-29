#!/usr/bin/python
import cgitb, sys, header, common_methods
cgitb.enable()

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


get_all_shares = {'id': 0, 'shares': [{'comment': '', 'node': 'node1', 'name': 'sunny', 'ftp': 1, 'tstamp':'', 'nfs': 0, 'date': '', 'path': '/storage/lotus_n1/sunny', 'afp': 0, 'smb': 0, 'size': '0'}, {'comment': '', 'node': 'node2', 'name': 'rahul', 'ftp': 0, 'tstamp':'', 'nfs': 0, 'date': '', 'path': '/storage/lotus_n2/rahul', 'afp': 0, 'smb': 0, 'size': ''}]}
array_len = len(get_all_shares["shares"])


conn = common_methods.conn_status()

import left_nav
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
                width           : '60%',
                height          : '68%',
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
	<div style="margin-left:5px;" class="iframe-insidepage-heading">San<span style="color:#000; "> >> Srp >></span> Target Information</div>
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
	<div class="view_option"><a href = 'main.py?page=tar_srp'><img title = 'Create Target' src = '../images/new-folder-9.png' /></a>

	<a href="main.py?page=stat_srp"><img src="../images/grid-view.png" height="30px" width="30px" title="Grid View"></a> <a href="main.py?page=l_srp"><img src="../images/list-view.png" height="30px" width="30px" title="List View"></a>
</div>
	<div style="width:100px; float:left; text-align:right; margin:0 0 10px 0;">
	<hr style="width:50px; float:left; display:block; border:#2E64FE 1px solid; margin:10px 0 0 5px;"></hr>Node1<br/>
	<hr style="width:50px; float:left; display:block; border:#DF0174 1px solid; margin:10px 0 0 5px;"></hr>Node2<br/><br/>
	</div>

	  <div class="inputwrap">
	    <div class="formrightside-content">

<nav id="menu2">

<ul>"""

i=1
s=1
for x in get_all_shares["shares"]:
	#test_mount = prjquota.test_mount(get_mount_point)
	
	if(x["node"].strip() == "node1"):
		border_bottom = 'style="border-bottom:#2E64FE 1px solid;"'
	elif(x["node"].strip() == "node2"):
		border_bottom = 'style="border-bottom:#2E64FE 1px solid;"'
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

	
	print """<div id='jquery"""+str(i)+"""' style="margin:32px 0 0 0; font-size:12px; font-weight:bold; border:#cfbdbd 1px solid;">
<br/>	"""
	if(smb_status == True):
		print """<form name='set_perm_form' method='post' action=''>


<br/>	
	<input type='hidden' name='hid_share_name' value='"""+x["name"]+"""' />
	<input type='hidden' name='hid_share_path' value='"""+x["path"]+"""' />
	<button class="button_example" type = 'submit'  name="change_perm_but" value="change_perm_but" onclick = "return validate_dns_conf();" style="float:right; margin:0 10px 10px 0;">Change Permission</button>

<br/>
<br/>

		</form>"""
	else:
		print """<p style='text-align:center; margin:0 0 20px 0;'>SMB not configured for """+x['name']+""". <a href='main.py?page=smb_set&share_name="""+x['name']+"""'>Configure SMB</a></p>"""

	print """</div>"""

	print """<div id='official"""+str(i)+"""' style="margin:32px 0 0 0; font-size:12px; font-weight:bold; border:#cfbdbd 1px solid;">"""

	if((conn == "nis is running") or (conn == "Join is OK")):
                if(conn == "nis is running"):
                        print """<p style='text-align:center; margin:20px 0 20px 0;'>System is connected to NIS server!</p>"""
                if(conn == "Join is OK"):
                        print """<p style='text-align:center; margin:20px 0 20px 0;'>System is connected to ADS server!</p>"""

	else:

		if(afp_status == True):	
			print """<form name="chang_owner_form" method="post" action="">
	<br/>	
	<table style="padding:0 0 0 20px;">
	<tr>
	<td>File Permission </td>
	<td><input type='text' name='afp_file_permission' value='"""+str(get_afp_perm['file_perm'])+"""' /></td>
	</tr>

	<tr>
	<td>Directory Permission</td>
	<td><input type='text' name='afp_directory_permission' value='"""+str(get_afp_perm['directory_perm'])+"""' /></td>
	</tr>
	</table>

	<br/>	
		<input type='hidden' name='hid_share_name' value='"""+x["name"]+"""' />
		<input type='hidden' name='hid_share_path' value='"""+x["path"]+"""' />
		<button class="button_example" type = 'submit'  name="change_perm_but_afp" value="change_perm_but_afp" onclick = "return validate_dns_conf();" style="float:right; margin:0 10px 10px 0;">Change Permission</button>

	<br/>
	<br/>
			</form>"""
		else:
			print """<p style='text-align:center; margin:20px 0 20px 0;'>AFP not configured for """+x['name']+""". <a href='main.py?page=afp&share_name="""+x['name']+"""'>Configure AFP</a></p>"""
		
	print """</div>"""

	print """</div>"""

	
	#print """<li """+border_bottom+""" onclick="return folder_click("""+str(i)+""", """+str(array_len)+""", """+str(s)+""");"><a>"""+x['name']+"""</a>
	print """<li """+border_bottom+""" onclick="return folder_click("""+str(i)+""", """+str(array_len)+""", """+str(s)+""");"><a>Srp</a>"""
	print"""
	<div id='"""+str(i)+"""' style="display:none;">
	<ul>"""
	print """<li><a href="main.py?page=disk_srp&disk="target_name">Disk To Target</a></li>"""
	print """<li><a href="main.py?page=ini_srp&sprop="target_name">Initiator</a></li>"""
	#print"""<li><a href="main.py?page=det_iscsi&detail="target_name">Target Information</a></li>"""
	print"""<li><a class="various" data-fancybox-type="iframe" href="srp_list.py?target="target_n"">Target Information</a></li>"""
	print"""<li><a class="various" data-fancybox-type="iframe" href="srp_session.py?target="target_n"">Session Information</a></li>"""
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
