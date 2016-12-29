#!/usr/bin/python
import cgitb, sys, header, common_methods
cgitb.enable()

sys.path.append('/var/nasexe/python/')
import authentication
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


#print 'Content-Type: text/html'

#-------------------------------------- Delete Share End -----------------------------------------#



#get_all_shares = common_methods.get_share_names()
get_all_shares = {'id': 0, 'shares': [{'comment': '', 'node': 'node1', 'name': 'sunny', 'ftp': 1, 'tstamp':'', 'nfs': 0, 'date': '', 'path': '/storage/lotus_n1/sunny', 'afp': 0, 'smb': 0, 'size': '0'}, {'comment': '', 'node': 'node2', 'name': 'rahul', 'ftp': 0, 'tstamp':'', 'nfs': 0, 'date': '', 'path': '/storage/lotus_n2/rahul', 'afp': 0, 'smb': 0, 'size': ''}]}
array_len = len(get_all_shares)
get_shares = tools.get_all_shares(debug=True)
if(get_shares["id"] == 0):
	get_all_shares = {'id': 0, 'shares': [{'comment': '', 'node': 'node1', 'name': 'sunny', 'ftp': 1, 'tstamp':'', 'nfs': 0, 'date': '', 'path': '/storage/lotus_n1/sunny', 'afp': 0, 'smb': 0, 'size': '0'}, {'comment': '', 'node': 'node2', 'name': 'rahul', 'ftp':'', 'tstamp':'', 'nfs': 0, 'date': '', 'path': '/storage/lotus_n2/rahul', 'afp': 0, 'smb': 0, 'size': ''}]}
	#get_all_shares = tools.get_share_date_size_info(get_shares['shares'])
	array_len = len(get_all_shares["shares"])

#conn = common_methods.conn_status()
conn = authentication.get_auth_type()

import left_nav
print
print """

      <!--Right side body content starts from here-->
      <div class="rightsidecontainer">
	<div class="insidepage-heading">San >> Fc >><span class="content">Configure Information</span></div>
	<!--tab srt-->
	<div class="searchresult-container">
	  <div class="infoheader">
	    <div id="tabs">
	      <ul>
		<li><a href="#tabs-1">Configure List</a></li>
	      </ul>
	      <div id="tabs-1">

	<!--form container starts here-->
	<div class="form-container">
	<div class="view_option"><a href = 'main.py?page=tar_fc'><img title = 'Create Target' src = '../images/new-folder-9.png' /></a><a href="main.py?page=status_fc"><img src="../images/grid-view.png" height="30px" width="30px" title="Grid View" /></a> <a href="main.py?page=list_fc"><img src="../images/list-view.png" height="30px" width="30px" title="List View" /></a></div>
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
for x in get_all_shares["shares"]:
	get_share_perm = share_permissions.get_smb_perms(x["name"])
        get_afp_perm = share_permissions.get_afp_perms(x["name"])

	get_all_protocols = tools.get_all_protocols(x["name"], x["path"])

	get_mount_point = prjquota.get_mountpoint(x["path"])
        test_mount = prjquota.test_mount(get_mount_point)

	split_path = x["path"].split("/")
	#disk_name = x["path"][:x["path"].rfind('/')]
	#disk_name = disk_name[disk_name.rfind('/')+1:]
	disk_name = split_path[2]

	print """<tr>
	<td>
	<nav id="menulist3">
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

	smb_status = smb.is_configured(x["name"],debug=False)
        afp_status = afp.is_configured(x["name"])


        print """<div style="display: none;" id='proppopUpDiv"""+str(i)+"""'>
        <h5><span onclick="popup('proppopUpDiv"""+str(i)+"""')" style="cursor:pointer;">X</span></h5>

        <script type="text/javascript" src="popup/jquery-tabs.js"></script>
        <ul class="idTabs"> 
        <li><a href='#jquery"""+str(i)+"""' class="link_tabs">SMB Permissions</a></li> 
        <li><a href='#official"""+str(i)+"""' class="link_tabs">AFP Permissions</a></li> 
        </ul>
 
        <div id='jquery"""+str(i)+"""' style="margin:32px 0 0 0; font-size:12px; font-weight:bold; border:#cfbdbd 1px solid;">"""

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
                print """<p style='text-align:center; margin:20px 0 20px 0;'>SMB not configured for """+x['name']+""". <a href='smb_settings.py?share_name="""+x['name']+"""'>Configure SMB</a></p>"""

        print """</div>"""


        print """<div id='official"""+str(i)+"""' style="margin:32px 0 0 0; font-size:12px; font-weight:bold; border:#cfbdbd 1px solid;">"""
       
	if((conn["type"] == "nis") or (conn["type"] == "ads")):
		if(conn["type"] == "nis"): 
			print """<p style='text-align:center; margin:20px 0 20px 0;'>System is connected to NIS server!</p>"""
		if(conn["type"] == "ads"): 
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


        print """</div>


	<li onclick="return folder_click("""+str(i)+""", """+str(array_len)+""", """+str(s)+""");"><a>Targetname</a>

        <div id='"""+str(i)+"""' style="display:none;">
        <ul>"""
	print """<li><a href="main.py?page=disk_fc&disk="target_name">Disk To Target</a></li>"""
        print """<li><a href="main.py?page=fc_ini&sprop="target_name">Initiator</a></li>"""
        #print"""<li><a href="main.py?page=det_iscsi&detail="target_name">Target Information</a></li>"""
        print"""<li><a class="various" data-fancybox-type="iframe" href="fc_list.py?target="target_n"">Target Information</a></li>"""
        print"""<li><a class="various" data-fancybox-type="iframe" href="fc_session.py?target="target_n"">Session Information</a></li>"""
        #print"""<li><a href="main.py?page=ses_iscsi&session="target_name">Session Information</a></li>"""
        print """<li><a onclick="popup('proppopUpDiv2"""+str(i)+"""')" href="#">Delete</a></li>

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
