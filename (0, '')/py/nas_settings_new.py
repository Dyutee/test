#!/usr/bin/python
#_*_ coding: UTF-8 _*_                                          
"""
	this page is for creating share, modifying a share, user quota and showing share information. to create a share, it is required that we
	should have atleast one nas disk created.
"""
#enable debugging                                       
import cgitb, header, os, common_methods, commands, sys

cgitb.enable()          

sys.path.append('/var/nasexe/storage/');
sys.path.append('../modules/');
import disp_except;

import storage_op
from lvm_infos import *
from functions import *

sys.path.append('/var/nasexe/python/');
import cli_utils;

try:
	image_icon = common_methods.getimageicon();
	log_array  = [];
        log_file   = common_methods.log_file;
        logstring  = '';
	use_manual = '';

	getdiskscommand = get_lv_infos();
	getdisksdictarray = getdiskscommand['lvs'];

	mounteddisksstring = ':';

	for lvdicts in getdisksdictarray:
		diskname = lvdicts['lv_name'];
		diskname = diskname[diskname.find('-') + 1:];
		diskname = diskname.strip();

		checkmount = cli_utils.is_disk_mounted(diskname);
		print checkmount
		

		if (checkmount['id'] == 0):
			mounteddisksstring = mounteddisksstring + diskname + ':';

	# get the session user here from get_session_user() method defined in common_methods.py
	session_user = common_methods.get_session_user();
	ss = session_user

	logstring = str(common_methods.now) + '<<>>From: ' + common_methods.remote_ip + '<<>>' + str(ss);
        log_array.append(logstring);
        common_methods.append_file(log_file, log_array);

	# define empty array for NAS disks
	nas_disks_array = [];
	shares_array    = [];
	nas_disk = 'Create a NAS disk';

	# get the shares from the shares global file
	shares_file  = '/var/www/global_files/shares_global_file';
	shares_array = common_methods.read_file(shares_file);
	
	ss = shares_array

	logstring = str(common_methods.now) + '<<>>From: ' + common_methods.remote_ip + '<<>>' + str(ss);
        log_array.append(logstring);
        common_methods.append_file(log_file, log_array);

	tempshares = [];
	message = 'Create a share!';

	groups_checked = '';

	if (isinstance(shares_array, (list, tuple))):
		if (len(shares_array) > 0):
			message = 'Choose a share';

	# get the nas disks from the get_nas_disks() method defined in common_methods.py
	nas_disks_array = common_methods.get_nas_disks();

	ss = nas_disks_array 
	
	logstring = str(common_methods.now) + '<<>>From: ' + common_methods.remote_ip + '<<>>' + str(ss);
        log_array.append(logstring);
        common_methods.append_file(log_file, log_array);

	create_share_style = '';
	create_share_link  = '';
	remove_blanklines = commands.getoutput('sudo /var/nasexe/delete_entry "^$" shares_global_file /var/www/global_files/');

	# check whether array has elements or not
	if (len(nas_disks_array) > 0):
		create_share_link = "<a class = 'sidenav' href = '#' onclick = 'return show_table(\"id_add_share\");' onmouseover = 'document.getElementById(\"id_shares_list\").style.display = \"none\";'>Create share</a>";

		nas_disk = nas_disks_array[0].strip();

	else:
		create_share_link = "<a class = 'sidenav' href = '#' onclick = 'window.alert(\"There should be atleast one NAS disk to create share\")' onmouseover = 'document.getElementById(\"id_shares_list\").style.display = \"none\";'>Create share</a>";
		create_share_style = 'none';
		
	if (len(nas_disks_array) == 0):
		print '<script>alert("Create atleast one NAS disk to create a share!");</script>';

	import left_nav
	print
	print """
	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer">
		<div class="insidepage-heading"> RESOURCES >> <span class="content">Resources Information</span></div>
		<!--tab srt-->
		<div class="searchresult-container">
		  <div class="infoheader">
		    <div id="tabs">
		      <ul>
			<li><a href="#tabs-1">Create Share</a></li>
			<!--<li><a href="#tabs-2">Configure Share</a></li>
			<li><a href="#tabs-3">Disk Quota</a></li>
			<li><a href="#tabs-4">ACL Settings</a></li>
			<li><a href="#tabs-5">Reset ACL</a></li>
			<li><a href="#tabs-6">Share Maintenance</a></li>-->
		      </ul>

              <div id="tabs-1">
        <!--form container starts here-->
        <div class="form-container">
	<div class="view_option" style = 'border: 0px solid;'><a href = 'main.py?page=cs'><img title = 'Back to shares' src = '../images/go-back-icon.png' /></a></div>
          <div class="topinputwrap-heading">Create New Share</div>
          <div class="topinputwrap">
            <table cellpadding="0" cellspacing="0" border="0" align="center">
              <tr>
                <td align="left" valign="top"><table width="100%" border="0" cellspacing="0" cellpadding="0" >
                    <tr>
                      <td width="100%" class="content" align="left" valign="top"><form name="user_share" method="post" action="add_share.py">
                          <div  align="left" style="height:20px; margin-top:0px;" class="menu_text_active"></div>
                          <table width="100%" border="0" cellspacing="0" cellpadding="0">
                            <tr>
                              <td colspan="3" height="5px"></td>
                            </tr>
                            <tr>
                              <td align="left" valign="top" height="20px" class="formleftside-content">Share name</td>
                              <td  align="left" valign="top" width="7"></td>
                              <td colspan = '4' align="left" valign="middle" height="20px">
				<input class = 'textbox' type = 'text' name = 'share' oninput = 'return update_path();' style = 'width: 100%;' id = 'id_create_share'></td>
                            </tr>
                            <tr>
                              <td colspan="3" height="5px"></td>
                            </tr>
                            <tr>
                              <td align="left" valign="top" height="20px" class="formleftside-content">Share path</td>
                              <td  align="left" valign="top" width="7"></td>
                              <td align="left" colspan = '4' valign="middle" height="20px">
				<input class = 'textbox' type = 'text' name = 'path' value = '""" + nas_disk + """' readonly style = 'width: 100%;'></td>
                            </tr>
                            <tr>
                              <td colspan="3" height="5px"></td>
                            </tr>
                            <tr>
                              <td class="formleftside-content" align="left" valign="top" width="101">Comment</td>
                              <td  align="left" valign="top" width="7"></td>
                              <td align="left" colspan="4">
				<input class = 'textbox' type = 'text' name = 'comment' style = 'width: 100%;'></td>
                            </tr>
                            <tr>
                              <td colspan="3" height="5px"></td>
                            </tr>
                            <tr>
                              <td width="210" align="left" valign="top" height="20px" class="content"></td>
                              <td  align="left" valign="top" width="7"></td>
                              <td width="84" align="left" valign="middle" height="20px">
                                </td>
                              <td align="left" valign="top" colspan="3">
			<table width="345" border="0" cellspacing="0" cellpadding="0">
                                  <tbody id="image" >
                                  </tbody>
                                </table></td>
                            </tr>
                            <tr>
                              <td colspan="3" height="5px"></td>
                            </tr>
                            <tr>
                              <td colspan="3" height="5px"></td>
                            </tr>
                            <tr>
                              <td colspan="3" height="5px"></td>
                            </tr>
                            <tr>
                               <td colspan = '4' class = 'formleftside-content'>
                               <input type = 'checkbox' name = 'use_manual' onclick = 'return show_hide_file_dir();'>&nbsp;Custom Location 
                            </td>
                            </tr>
                            <tr>
                               <td colspan = '6'align = 'right'>
                                    <!-- this iframe is to display the directories and files for navigation -->
                                    <iframe frameborder = 0 name = 'directories' id = 'dir_list' src = 'show_dir.py' style = 'display: none; float: right; font: 12px Arial white; border: 1px solid lightgrey; width: 99%; height: 100%; margin-bottom: 1%;'></iframe>
                               </td>

        		 </tr>

                            <tr>
                              <td>&nbsp;</td>
                              <td>&nbsp;</td>
                              <td colspan = '5'>
				<div align = 'center' id = 'response' style = 'color: darkred; font-style: italic; margin-right: auto; margin-left: auto;'><div align = 'center' id = 'wait' style = 'display: none;'><img src = '../images/arrows32.gif'> Processing...</div></div>
				<!--<input name="submit" value="Create" onclick="validate_add_share_form();" type="submit" />-->
				<button class = 'button_example' type="button" name = 'action_but' value = 'Cancel' onclick = "location.href = 'main.py?page=cs';" style = 'float: right;'>Back</button>
				<button class = 'button_example' type="submit" name = 'action_but'  id = 'local_action_but' value = 'Apply' onclick = 'return validate_add_share_form();' style = 'float:right;'>Create</button></td>

                                &nbsp;&nbsp;&nbsp;
				<input type = 'hidden' name = 'hid_manual' value = '""" + use_manual + """'>
                            </tr>
                            <tr>
                              <td height="10px"></td>
                            </tr>
                          </table>
                        </form></td>
                    </tr>
                  </table></td>
              </tr>
            </table>
            <br />
          </div>
        </div>
        <!--form container ends here-->
	<p>&nbsp;</p>
              </div>

		<!--form container ends here-->
		      <!--<div id="tabs-2">
			<div id = 'subtabs' style = 'display: block;'>
                  <ul>
                    <li><a href="#subtabs-1">Edit Share Info</a></li>
                    <li><a href="#subtabs-2">SMB</a></li>
                    <li><a href="#subtabs-3">AFP</a></li>
                    <li><a href="#subtabs-4">Share Permissions</a></li>
                    <li><a href="#subtabs-5">Share Ownership</a></li>
                    <li><a href="#subtabs-6">NFS</a></li>
                    <li><a href="#subtabs-7">FTP</a></li>
                    <li><a href="#subtabs-8">Append Mode</a></li>
                  </ul>
                  <div id="subtabs-1">
                    <p>Proin elit arcu, rutrum commodo, vehicula tempus, commodo a, risus. Curabitur nec arcu. Donec sollicitudin mi sit amet mauris. Nam elementum quam ullamcorper ante. Etiam aliquet massa et lorem. Mauris dapibus lacus auctor risus. Aenean tempor ullamcorper leo. Vivamus sed magna quis ligula eleifend adipiscing. Duis orci. Aliquam sodales tortor vitae ipsum. Aliquam nulla. Duis aliquam molestie erat. Ut et mauris vel pede varius sollicitudin. Sed ut dolor nec orci tincidunt interdum. Phasellus ipsum. Nunc tristique tempus lectus.</p>
			</div>	
		 <div id="subtabs-2">

                    <p>Morbi tincidunt, dui sit amet facilisis feugiat, odio metus gravida ante, ut pharetra massa metus id nunc. Duis scelerisque molestie turpis. Sed fringilla, massa eget luctus malesuada, metus eros molestie lectus, ut tempus eros massa ut dolor. Aenean aliquet fringilla sem. Suspendisse sed ligula in ligula suscipit aliquam. Praesent in eros vestibulum mi adipiscing adipiscing. Morbi facilisis. Curabitur ornare consequat nunc. Aenean vel metus. Ut posuere viverra nulla. Aliquam erat volutpat. Pellentesque convallis. Maecenas feugiat, tellus pellentesque pretium posuere, felis lorem euismod felis, eu ornare leo nisi vel felis. Mauris consectetur tortor et purus.</p>

                  </div>

                  <div id="subtabs-3">

                    <p>Mauris eleifend est et turpis. Duis id erat. Suspendisse potenti. Aliquam vulputate, pede vel vehicula accumsan, mi neque rutrum erat, eu congue orci lorem eget lorem. Vestibulum non ante. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Fusce sodales. Quisque eu urna vel enim commodo pellentesque. Praesent eu risus hendrerit ligula tempus pretium. Curabitur lorem enim, pretium nec, feugiat nec, luctus a, lacus.</p>

                    <p>Duis cursus. Maecenas ligula eros, blandit nec, pharetra at, semper at, magna. Nullam ac lacus. Nulla facilisi. Praesent viverra justo vitae neque. Praesent blandit adipiscing velit. Suspendisse potenti. Donec mattis, pede vel pharetra blandit, magna ligula faucibus eros, id euismod lacus dolor eget odio. Nam scelerisque. Donec non libero sed nulla mattis commodo. Ut sagittis. Donec nisi lectus, feugiat porttitor, tempor ac, tempor vitae, pede. Aenean vehicula velit eu tellus interdum rutrum. Maecenas commodo. Pellentesque nec elit. Fusce in lacus. Vivamus a libero vitae lectus hendrerit hendrerit.</p>

                  </div>
                  <div id="subtabs-4">
			Tab-4
                  </div>
                  <div id="subtabs-5">
			Tab-5
                  </div>
                  <div id="subtabs-6">
			Tab-6
                  </div>
                  <div id="subtabs-7">
			Tab-7
                  </div>
                  <div id="subtabs-8">
			Tab-8
                  </div>

			</div>-->
		<!--form container starts here-->
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
	</div>"""

	print """     
	</td>
	 <td valign = "top" align = "left" width = "30px"></td>

	<td valign = "top" align = "left" width = "695px">"""

	querystring = os.environ['QUERY_STRING'];

	response  = common_methods.getsubstr(querystring, '&act=', '&');
	from_page = common_methods.getsubstr(querystring, '&from_page=', '&');

	if (response == 'del_share_done' or from_page == 'add_quota_page' or response == 'search_quota_done'):
		create_share_style = 'none';

	#import share_maintenance                                                            
	#import user_quota
	#import set_acl
	#import reset_acl_settings
	print"""
	 </td>

			     </tr>
			<!-- </table>-->

<!-- ####### Sub Tabs Start ####### -->

<script>
$("#tabs, #subtabs").tabs();
$("#tabs, #subsubtabs").tabs();
</script>

<!-- ####### Sub Tabs End ####### -->

				     """
	if (session_user == 'Maintenance Access'):
		tracedebug.watch(create_share_link);

except Exception as e:
	disp_except.display_exception(e);

