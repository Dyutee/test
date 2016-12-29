#!/usr/bin/python
import cgitb, sys, header, common_methods, opslag_info, commands
cgitb.enable()

#################################################
################ import modules #################
#################################################
sys.path.append('/var/nasexe/python/')
import smb
import afp
import nfs 
import ftp_auth
import anon_ftp
import tools
import manage_users
import commons
import cli_utils
from tools import acl
from tools import share_permissions
from tools import prjquota
from tools import smb_logpath
#-------------------- End ----------------------#

date_cmd=commands.getoutput('sudo date +"%Y"')
os_name= opslag_info.getos('oss')
check_ha = tools.check_ha()

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

#################################################
########## Change SMB Permission ################
#################################################
if(header.form.getvalue("change_perm_but")):
	get_hid_share_name = header.form.getvalue("hid_share_name")
	get_hid_share_path = header.form.getvalue("hid_share_path")
	get_directory_mask = header.form.getvalue("smb_directory_mask")
	get_create_mask = header.form.getvalue("smb_create_mask")

	set_smb_perms = share_permissions.set_smb_perms(get_hid_share_name,get_directory_mask,get_create_mask)
	if(set_smb_perms["id"] == 0):
		print "<div id='id_trace'>"
		print set_smb_perms["desc"]
		print "</div>"
	else:
		print "<div id='id_trace_err'>"
                print set_smb_perms["desc"]
                print "</div>"
#-------------------- End ----------------------#

#################################################
########## Change AFP Permission ################
#################################################
if(header.form.getvalue("change_perm_but_afp")):
	get_hid_share_name = header.form.getvalue("hid_share_name")
	get_hid_share_path = header.form.getvalue("hid_share_path")
	get_file_perm = header.form.getvalue("afp_file_permission")
	get_dir_perm = header.form.getvalue("afp_directory_permission")

	set_afp_perms = share_permissions.set_afp_perms(get_hid_share_name,get_dir_perm,get_file_perm)
	if(set_afp_perms["id"] == 0):
		print "<div id='id_trace'>"
		print set_afp_perms["desc"]
		print "</div>"
	else:
		print "<div id='id_trace_err'>"
                print set_afp_perms["desc"]
                print "</div>"
#-------------------- End ----------------------#

#################################################
############## Change Ownership #################
#################################################
if(header.form.getvalue("re_assign_ownership")):
	get_assign_user = header.form.getvalue("ass_user")
	get_assign_group = header.form.getvalue("ass_group")
	get_s_name = header.form.getvalue("hid_s_name")
	get_s_path = header.form.getvalue("hid_s_path")
	get_inherit_ownership = header.form.getvalue("inherit_ownership")
	
	if(get_inherit_ownership == "on"):
		get_inherit_ownership = "yes"
	else:
		get_inherit_ownership = "no"

	set_ownership_cmd = acl.set_ownership(get_s_path,user=get_assign_user,group=get_assign_group,recur=get_inherit_ownership)
	if(set_ownership_cmd == True):
		print "<div id='id_trace'>"
		print "Successfully set ownership!"
		print "</div>"
	else:
		print "<div id='id_trace'>"
                print "Error setting ownership!"
                print "</div>"
#-------------------- End ----------------------#

#################################################
############### Reset Ownership #################
#################################################
if(header.form.getvalue("reset_ownership")):
	get_s_path = header.form.getvalue("hid_s_path")
	reset_ownership_cmd = acl.set_ownership(get_s_path,user='root',group='root',recur='yes')
	if(reset_ownership_cmd == True):
		print "<div id='id_trace'>"
		print "Successfully reset ownership!"
		print "</div>"
	else:
		print "<div id='id_trace_err'"
		print "Error resetting ownership!"
		print "</div>"
#-------------------- End ----------------------#

#################################################
################# Delete Share ##################
#################################################
if(header.form.getvalue("delete_share")):
	get_share_to_delete = header.form.getvalue("hid_share_name_to_del")
	get_share_path = header.form.getvalue("hid_share_path_to_del")
	retrieve_log_path = ''
        log_path_status = smb_logpath.is_set()
        if(log_path_status == True):
                get_log_path_cmd = smb_logpath.get()
                retrieve_log_path = get_log_path_cmd["share_path"]

	if (get_share_path == retrieve_log_path):
		print "<div id='id_trace_err'>"
                print "Share cannot be deleted since it is set as SMB LOG PATH."
                print "</div>"
	else:
		get_smb_status = smb.is_configured(get_share_to_delete,debug=False)
		get_afp_status = afp.is_configured(get_share_to_delete)
		get_ftp_status = ftp_auth.is_configured(get_share_to_delete)
		get_nfs_status = nfs.is_configured(get_share_path)
		if(get_smb_status == True):
			unconf_smb_cmd = smb.unconfigure(get_share_to_delete,debug=False)
		if(get_afp_status == True):
			unconf_afp_cmd = afp.unconfigure(get_share_to_delete)
		if(get_ftp_status == True):
			call_unmount = commons.unmount_ftp(get_share_to_delete)
			unconf_ftp_cmd = ftp_auth.unconfigure(get_share_to_delete)
			unconf_ftp_anon = anon_ftp.anonymous_unconfigure(get_share_to_delete)
		if(get_nfs_status == True):
			unconf_nfs_cmd = nfs.unconfigure(get_share_path)

		delete_share_cmd = tools.remove_share(get_share_to_delete)
		tools.delete_entry_from_file('^' + get_share_to_delete + ':', 'shares_global_file', '/var/www/global_files/');
		if(delete_share_cmd["id"] == 0):
			print "<div id='id_trace'>"
			print delete_share_cmd["desc"]
			print "</div>"
		else:
			print "<div id='id_trace_err'>"
			print delete_share_cmd["desc"]
			print "</div>"
#-------------------- End ----------------------#

#################################################
################ Get all shares #################
#################################################
get_all_shares = common_methods.get_share_names()
array_len = len(get_all_shares)

get_shares = tools.get_all_shares(debug=True)
if(get_shares["id"] == 0):
        get_all_shares = tools.get_share_date_size_info(get_shares['shares'])
	array_len = len(get_all_shares["shares"])
#-------------------- End ----------------------#

#--- Get all Users
get_all_users = manage_users.get_smb_users()

#--- Get all Groups
get_all_groups = manage_users.get_sys_groups()

#--- Connection Status
conn = common_methods.conn_status()

import left_nav
print
print """


      <!--Right side body content starts from here-->
      <div class="rightsidecontainer">
	<!--<div class="insidepage-heading">Nas >> <span class="content">Configure Information</span></div>-->
	<div style="margin-left:5px;" class="iframe-insidepage-heading"><a class="demo" href ="#"><img style="border:#000 1px solid; margin:-5px 2px;" src ="../images/help_icon1.png">
	<span class="tooltip" >
                 <table border="0">
        <tr>     
        <td class="text_css">On this page, you can create, view, edit and delete NAS shares. You can also configure various protocols and set up ACL on those shares.</td>
        </tr>
        </table></span></a> <a class="iframe_bc" href="main.py?page=cs">NAS</a> <span style="color:#000; "> >> </span> Manage Shares</div>
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
	<div class="view_option"><a href = 'main.py?page=nas'><img title = 'Create Share' src = '../images/new-folder-9.png' /></a><a href="main.py?page=cs"><img src="../images/grid-view.png" height="30px" width="30px" title="Grid View"></a> <a href="main.py?page=csl"><img src="../images/list-view.png" height="30px" width="30px" title="List View"></a></div>
	<div style="width:100px; float:left; text-align:right; margin:0 0 10px 0;">
	<hr style="width:50px; float:left; display:block; border:#2E64FE 1px solid; margin:10px 0 0 5px;"></hr>Node1<br/>
	<hr style="width:50px; float:left; display:block; border:#DF0174 1px solid; margin:10px 0 0 5px;"></hr>Node2<br/><br/>
	</div>

	  <div class="inputwrap">
	    <div class="formrightside-content">

<nav id="menu">

<ul>"""

i=1
s=1
if(get_all_shares["shares"] == []):
        print "<div style='text-align:center;'>No Shares Created! <a href='main.py?page=nas'>Create a Share</a></div>"
for x in get_all_shares["shares"]:
	new_name = x["name"]
	#print new_name
	#print x
	new_path = x["path"]
        #print new_path
        disk_path =new_path[new_path.find('/')+1:new_path.rfind('/')]
        diskname=disk_path[disk_path.rfind('/')+1:]
        #print diskname
        #print '<br/>'
        #diskname = full_path[full_path.rfind('/')+1:]
        check_disk_mount = cli_utils.is_disk_mounted(diskname,debug="no")
        #print check_disk_mount
	get_share_perm = share_permissions.get_smb_perms(x["name"])
	get_afp_perm = share_permissions.get_afp_perms(x["name"])

	get_mount_point = prjquota.get_mountpoint(x["path"])
	test_mount = prjquota.test_mount(get_mount_point)

	fade = ""	
	func = "folder_click"	
	if((check_ha != True) and (x["node"].strip() == "node2")):
		fade = "opacity:0.5;" 
		func = ""	
	if(x["node"].strip() == "node1"):
		border_bottom = "border-bottom:#2E64FE 1px solid;"
	elif(x["node"].strip() == "node2"):
		border_bottom = "border-bottom:#DF0174 1px solid;"
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
	<h5>Delete """+x['name']+"""<span onclick="popup('proppopUpDiv2"""+str(i)+"""')" style="cursor:pointer;">X</span></h5>
	<div style="border:#D1D1D1 1px solid; text-align:center; height:70px; margin:20px 0 20px 0;">
        Are you sure you want to delete """+x['name']+""" ?<br/><br/>
	<button class="buttonClass" type="button" name = 'local_action_but'  id = 'local_action_but' value = 'Update' style="float:right; margin:0px 150px 0 0; " onclick="popup('proppopUpDiv2"""+str(i)+"""')" >No</button>
        <button class="buttonClass" type="submit" name = 'delete_share'  id = 'delete_share' value = 'Update' style="float:right; margin:0 10px 0 0;" >Yes</button>
	<input type='hidden' name='hid_share_name_to_del' value='"""+x["name"]+"""' />
	<input type='hidden' name='hid_share_path_to_del' value='"""+x["path"]+"""' />
        </div>
	</form>

	</div>

	<div style="display: none;" id='proppopUpDiv3"""+str(i)+"""'>
	<h5>Alert<span onclick="popup('proppopUpDiv3"""+str(i)+"""')" style="cursor:pointer;">X</span></h5>
	<div style="text-align:center; height:30px; margin:20px 0 20px 0;">
        Disk is Not Mounted For """+new_name+""" Share!<br/><br/>

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

<table style="padding:0 0 0 20px;">
<tr>
<td>Directory Mask</td>
<td><input type='text' name='smb_directory_mask' value='"""+str(get_share_perm['directory_mask'])+"""' /></td>
</tr>

<tr>
<td>Create Mask</td>
<td><input type='text' name='smb_create_mask' value='"""+str(get_share_perm['create_mask'])+"""' /></td>
</tr>
</table>

<br/>	
	<input type='hidden' name='hid_share_name' value='"""+x["name"]+"""' />
	<input type='hidden' name='hid_share_path' value='"""+x["path"]+"""' />
	<button class="buttonClass" type = 'submit'  name="change_perm_but" value="change_perm_but" onclick = "return validate_dns_conf();" style="float:right; margin:0 10px 10px 0; width:150px;">Change Permission</button>

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
		<button class="buttonClass" type = 'submit'  name="change_perm_but_afp" value="change_perm_but_afp" onclick = "return validate_dns_conf();" style="float:right; margin:0 10px 10px 0; width:150px;">Change Permission</button>

	<br/>
	<br/>
			</form>"""
		else:
			print """<p style='text-align:center; margin:20px 0 20px 0;'>AFP not configured for """+x['name']+""". <a href='main.py?page=afp&share_name="""+x['name']+"""'>Configure AFP</a></p>"""
		
	print """</div>"""

	print """</div>"""

	
	print """<li id="sharesid" style='"""+fade+""" """+border_bottom+"""' onclick="return """+func+"""("""+str(i)+""", """+str(array_len)+""", """+str(s)+""");"><a>"""+x['name']+"""</a>

	<div id='"""+str(i)+"""' style="display:none;">
	<ul>

	<li><a href="main.py?page=es&share_name="""+x['name']+"""">Edit this Share</a></li>"""
	print """<li><a href="main.py?page=smb_set&share_name="""+x['name']+"""">SMB Settings</a></li>"""
	print """<li><a href="main.py?page=append&share_name="""+x['name']+"""">Append Mode</a></li>"""
	print"""<li><a href="main.py?page=afp&share_name="""+x['name']+"""">AFP Settings</a></li>"""
	print"""<li><a href="main.py?page=nfs&share_name="""+x['name']+"""">NFS Settings</a></li>"""
	print"""<li><a href="main.py?page=ftp&share_name="""+x['name']+"""">FTP Settings</a></li>"""
	#if(check_disk_mount['id'] == 0):
	print"""<li><a href="main.py?page=acl&share_name="""+x['name']+"""">ACL Settings</a></li>"""
	#else:
	#	print """<li><a onclick="popup('proppopUpDiv3"""+str(i)+"""')" href="#">ACL Settings</a></li>"""
	if(test_mount == True):
		print """<li><a href="main.py?page=fq&share_name="""+x['name']+"""">Folder Quota</a></li>"""

	print """
	<!--<li><a href="perms_ownership.py?share_name="""+x['name']+"""">Permissions/Ownership</a></li>-->
	<li><a onclick="popup('proppopUpDiv"""+str(i)+"""')" href="#">Properties</a></li>
	<li><a onclick="popup('proppopUpDiv2"""+str(i)+"""')" href="#">Delete</a></li>

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
<div class="insidefooter footer_content">&copy """+date_cmd+""" """+os_name+""" FS2</div>
<!-- Footer ends here-->
</div>
<!--inside body wrapper end-->
</div>
<!--body wrapper end-->
</body>
</html>
"""
