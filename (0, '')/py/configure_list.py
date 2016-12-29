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

check_ha = tools.check_ha()
#print 'Content-Type: text/html'

#-------------------------------------- Change SMB Perm Start -------------------------------------------#
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

#-------------------------------------- Change SMB Perm End -------------------------------------------#

#-------------------------------------- Change AFP Perm Start -------------------------------------------#
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

#-------------------------------------- Change AFP Perm End -------------------------------------------#

#-------------------------------------- Delete Share Start -----------------------------------------#
#if(header.form.getvalue("delete_share")):
#        get_share_to_delete = header.form.getvalue("hid_share_name_to_del")
#        delete_share_cmd = tools.remove_share(get_share_to_delete)
#        if(delete_share_cmd["id"] == 0):
#                print "<div id='id_trace'>"
#                print delete_share_cmd["desc"]
#                print "</div>"
#        else:
#                print "<div id='id_trace_err'"
#                print delete_share_cmd["desc"]
#                print "</div>"
#-------------------------------------- Delete Share End -----------------------------------------#

#-------------------------------------- Delete Share Start -----------------------------------------#
if(header.form.getvalue("delete_share")):
        get_share_to_delete = header.form.getvalue("hid_share_name_to_del")
        get_share_path = header.form.getvalue("hid_share_path_to_del")
        delete_share_cmd = tools.remove_share(get_share_to_delete)
        if(delete_share_cmd["id"] == 0):
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

                tools.delete_entry_from_file('^' + get_share_to_delete + ':', 'shares_global_file', '/var/www/global_files/');
                print "<div id='id_trace'>"
                print delete_share_cmd["desc"]
                print "</div>"
        else:
                print "<div id='id_trace_err'>"
                print delete_share_cmd["desc"]
                print "</div>"
#-------------------------------------- Delete Share End -----------------------------------------#



get_all_shares = common_methods.get_share_names()
array_len = len(get_all_shares)

get_shares = tools.get_all_shares(debug=True)
if(get_shares["id"] == 0):
	get_all_shares = tools.get_share_date_size_info(get_shares['shares'])
	array_len = len(get_all_shares["shares"])

#conn = common_methods.conn_status()
conn = authentication.get_auth_type()

import left_nav
print
print """

      <!--Right side body content starts from here-->
      <div class="rightsidecontainer">
	<div style="margin-left:5px;" class="iframe-insidepage-heading">
	<a class="demo" href ="#"><img style="border:#000 1px solid; margin:-5px 2px;" src ="../images/help_icon1.png">
        <span class="tooltip" >
        <table border="0">
        <tr>
        <td style="font-size: medium;text-align:start;">Share Information:</td>
        </tr>
        <tr>     
        <td class="text_css">This page Display the Share of both nodes .Color code to distribute the node name.If you Click on any Share then you can get few option which you can use for share properties .likeEdit share ,SMB settings,AFP,NFS etc.You have three Icons on top Right hand side first option to create share second is grid view option and third is list view option..</td>
        </tr>
        </table></span></a>
	<a class="iframe_bc" href="main.py?page=csl">Nas</a> >> <span class="content">Shares</span></div>
	<!--tab srt-->
	<div class="searchresult-container">
	  <div class="infoheader">
	    <div id="tabs">
	      <ul style="display:none;">
		<li><a href="#tabs-1">Configure Share</a></li>
	      </ul>
	      <div id="tabs-1">

	<!--form container starts here-->
	<div class="form-container" style="border:0px;">
	<div class="view_option"><a href = 'main.py?page=nas'><img title = 'Create Share' src = '../images/new-folder-9.png' /></a><a href="main.py?page=cs"><img src="../images/grid-view.png" height="30px" width="30px" title="Grid View" /></a> <a href="main.py?page=csl"><img src="../images/list-view.png" height="30px" width="30px" title="List View" /></a></div>
	  <div class="inputwrap">
	    <div class="formrightside-content">"""
if(get_all_shares["shares"] != []):
	print """<table style="border:#D1D1D1 1px solid; width:700px; margin:0 0 0 10px;">
		<tr style="border-bottom:#D1D1D1 1px solid;">
			<th align="left" style="border-bottom:#D1D1D1 1px solid;">Name</th>
			<th align="left" style="border-bottom:#D1D1D1 1px solid;">Size</th>
			<th align="left" style="border-bottom:#D1D1D1 1px solid;">Date Modified</th>
			<th align="left" style="border-bottom:#D1D1D1 1px solid;">Protocols</th>
			<th align="left" style="border-bottom:#D1D1D1 1px solid;">Disk Name</th>
			<th align="left" style="border-bottom:#D1D1D1 1px solid;">Node</th>
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

	fade = ""
        func = "folder_click"
        if((check_ha != True) and (x["node"].strip() == "node2")):
                fade = "opacity:0.5;"
                func = ""

	print """<tr>
	<td>
	<nav id="menulist">
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
        <h5>Delete """+x['name']+"""<span onclick="popup('proppopUpDiv2"""+str(i)+"""')" style="cursor:pointer;">X</span></h5>
        <div style="border:#D1D1D1 1px solid; text-align:center; height:70px; margin:20px 0 20px 0;">
        Are you sure you want to delete """+x['name']+""" ?<br/><br/>
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

<table style="padding:20px 0 0 20px;">
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
        <button class="button_example" type = 'submit'  name="change_perm_but" value="change_perm_but" onclick = "return validate_dns_conf();" style="float:right; margin:0 10px 10px 0;">Change Permission</button>

<br/>
<br/>

                </form>"""
        else:
                print """<p style='text-align:center; margin:20px 0 20px 0;'>SMB not configured for """+x['name']+""". <a href='smb_settings.py?share_name="""+x['name']+"""&view=list'>Configure SMB</a></p>"""

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


	<li style='"""+fade+"""' onclick="return """+func+"""("""+str(i)+""", """+str(array_len)+""", """+str(s)+""");"><a>"""+x['name']+"""</a>

        <div id='"""+str(i)+"""' style="display:none;">
        <ul>

        <li><a href="main.py?page=es&share_name="""+x['name']+"""&view=list">Edit this Share</a></li>
        <li><a href="main.py?page=smb_set&share_name="""+x['name']+"""&view=list">SMB Settings</a></li>
        <li><a href="main.py?page=append&share_name="""+x['name']+"""&view=list">Append Mode</a></li>
        <li><a href="main.py?page=afp&share_name="""+x['name']+"""&view=list">AFP Settings</a></li>
        <li><a href="main.py?page=nfs&share_name="""+x['name']+"""&view=list">NFS Settings</a></li>
        <li><a href="main.py?page=ftp&share_name="""+x['name']+"""&view=list">FTP Settings</a></li>
	<!--<li><a href="set_acl_page.py?share_name="""+x['name']+"""">ACL Settings</a></li>-->
	<li><a href="main.py?page=acl&share_name="""+x['name']+"""&view=list">ACL Settings</a></li>"""
        if(test_mount == True):
                print """<li><a href="main.py?page=fq&share_name="""+x['name']+"""">Folder Quota</a></li>"""

        print """

	<li><a onclick="popup('proppopUpDiv"""+str(i)+"""')" href="#">Properties</a></li>
	<li><a onclick="popup('proppopUpDiv2"""+str(i)+"""')" href="#">Delete</a></li>

        </ul>
        </div>

        </li>
			
	</ul>
	</nav>


	</td>
	<td>"""+x['size']+"""</td>
	<td>"""+x['date']+"""</td>
	<td>"""+get_all_protocols+"""</td>
	<td>"""+disk_name+"""</td>
	<td>"""+x['node']+"""</td>
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
