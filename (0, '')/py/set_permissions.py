#!/usr/bin/python
import cgitb, sys, header, common_methods, string, commands, share_details
cgitb.enable()


#print 'Content-Type: text/html'
import left_nav

get_share = header.form.getvalue("share_name")


sys.path.append('/var/nasexe/python/');
from fs2global import *;

cgitb.enable();

session_user = common_methods.get_session_user();

commands.getoutput('sudo sed -i "/^$/d" /var/www/global_files/share_perms_global_file');

if (session_user != ''):
        path    = share_details.path.replace('/storage/', '');
        share   = share_details.share;
        comment = share_details.comment;

        allselected   = 'selected';
        afpselected   = '';
        smbselected   = '';
        localselected = '';

        querystring = os.environ['QUERY_STRING'];

        if (comment != ''):
                comment.strip();

        restrict_checked = '';
        inherit_checked  = '';

        # retrieve the permissions set for the share path
        find_share_perms_command = 'sudo /var/nasexe/permission_of "/storage/' + path + '"';
        find_share_perms         = commands.getoutput(find_share_perms_command);

        # get the properties of 'restrict' and 'recursive' from share_perms_global_file
        share_details_command1 = 'sudo grep "' + share + ':" /var/www/global_files/share_perms_global_file';
        share_details1         = commands.getoutput(share_details_command1);
        #print share_details1
        #print'<br>'

        if (share_details1 != ''):
                temp = [];
                temp = share_details1.split(':');

                restrict  = temp[1];
                recursive = temp[2];

                if (restrict == 'true'):
                        restrict_checked = 'checked';

                if (recursive == 'true'):
                        inherit_checked = 'checked';

                # when restrict is set to true, the permissions can be retreived only from the command getfacl
                if (restrict == 'true'):
                        other_perm = 'sudo getfacl /storage/' + path + '|grep "other"';
                        result_oth = commands.getoutput(other_perm);
                        #print result_oth

                        # get the permission string from result_oth (sample output: other::r-x)
                        allperms = result_oth[result_oth.find('::') + 2:];

                        allperms = allperms.strip();

                        if (allperms == '---'):
                                o_perm = '__';

                        if (allperms == 'r--'):
                                o_perm = 'r__';

                        if (allperms == '-w-'):
                                o_perm = '_w_';

                        if (allperms == '--x'):
                                o_perm = '__x';

                        if (allperms == 'rw-'):
                                o_perm = 'r_w_';

                        if (allperms == 'rwx'):
                                o_perm = 'r_w_x';

                        if (allperms == 'r-x'):
                                o_perm = 'r__x';

                        if (allperms == '-wx'):
                                o_perm = '_w_x';

        # extract the individual permissions from the result string of find_share_perms(r_w_x:r_w_x:r_w_x)
        u_perm = find_share_perms[:find_share_perms.find(':')];
        #print 'Uperm:'+ u_perm
        #print '<br/>'
        g_perm = find_share_perms[find_share_perms.find(':') + 1:find_share_perms.rfind(':')];
        o_perm = find_share_perms[find_share_perms.rfind(':') + 1:];

        # trim the permission values
        u_perm = u_perm.strip();
        g_perm = g_perm.strip();
        o_perm = o_perm.strip();

        # initialise the checked status for the user permissions
        o_read_checked  = '';
        o_write_checked = '';
        o_exec_checked  = '';

        # initialise the checked status for the group permissions
        g_read_checked  = '';
        g_write_checked = '';
        g_exec_checked  = '';

        # initialise the checked status for the other permissions
        oth_read_checked  = '';
        oth_write_checked = '';
        oth_exec_checked  = '';

        o_perm = o_perm.strip();

        # extract individual owner permissions 'r', 'w', 'x' from the string r_w_x:r_w_x:r_w_x
        u_read  = u_perm[:u_perm.find('_')];
        #print 'Uread' ' ' + u_read
        #print '<br/>'
        u_write = u_perm[u_perm.find('_') + 1:u_perm.rfind('_')];
        u_exec  = u_perm[u_perm.rfind('_') + 1:];

        # extract individual group permissions 'r', 'w', 'x' from the string r_w_x:r_w_x:r_w_x
        g_read  = g_perm[:g_perm.find('_')];
        g_write = g_perm[g_perm.find('_') + 1:g_perm.rfind('_')];
        #print g_write
        g_exec  = g_perm[g_perm.rfind('_') + 1:];

        # extract individual other permissions 'r', 'w', 'x' from the string r_w_x:r_w_x:r_w_x
        ot_read  = o_perm[:o_perm.find('_')];
        ot_write = o_perm[o_perm.find('_') + 1:o_perm.rfind('_')];
        ot_exec  = o_perm[o_perm.rfind('_') + 1:];

        # convert owner permissions to its corresponding numerical value, ex: read(r) - 4, write(w) - 2, execute(x) - 1
        if (u_read == 'r'):
                o_read = 4;
                o_read_checked = 'checked';

        if (u_write == 'w'):
                o_write = 2;
                o_write_checked = 'checked';

        if (u_exec == 'x'):
                o_exec = 1;
                o_exec_checked = 'checked';

        # convert group permissions to its corresponding numerical value, ex: read(r) - 4, write(w) - 2, execute(x) - 1
        if (g_read == 'r'):
                g_read = 4;
                g_read_checked = 'checked';

        if (g_write == 'w'):
                g_write = 2;
                g_write_checked = 'checked';

                #print g_write_checked
        if (g_exec == 'x'):
                g_exec = 1;
                g_exec_checked = 'checked';

        # convert other permissions to its corresponding numerical value, ex: read(r) - 4, write(w) - 2, execute(x) - 1
        if (ot_read == 'r'):
                oth_read = 4;
                oth_read_checked = 'checked';

        if (ot_write == 'w'):
                oth_write = 2;
                oth_write_checked = 'checked';

        if (ot_exec == 'x'):
                oth_exec = 1;
                oth_exec_checked = 'checked';

        if (ot_exec == 'x'):
                oth_exec = 1;
                oth_exec_checked = 'checked';

        sharepath = share_details.path;

        shareval = sharepath[sharepath.rfind('/') + 1:];

        checksmbpath = smb_share_conf_dir + shareval;
        checkafppath = afp_share_conf_dir + shareval;

        checksmbshare = commands.getstatusoutput('ls "%s"' % checksmbpath);
        checkafpshare = commands.getstatusoutput('ls "%s"' % checkafppath);



                                               


print
print """

      <!--Right side body content starts from here-->
      <div class="rightsidecontainer">
	<div class="insidepage-heading">Nas >> <span class="content">Configure Information</span></div>
	<!--tab srt-->
	<div class="searchresult-container">
	  <div class="infoheader">
	    <div id="tabs">
	      <ul>
		<li><a href="#tabs-1">Share Permissions</a></li>
	      </ul>
	      <div id="tabs-1">

	<!--form container starts here-->
	<div class="form-container">
	<div class="topinputwrap-heading">Share Permissions for '"""+get_share+"""'</div>
	  <div class="topinputwrap">




                        <table width = "685" name = 'disp_tables' id = 'id_share_permissions' style = 'display: block; padding:0 0 0 10px;' class = 'outer_border'>
                        <form name = 'share_permissions' method = 'POST' action = 'share_permissions.py'>"""

        # check if append mode is enabled or not.
        # if append mode is enabled, then share permissions and ownership can not be set ('a' is the output for append mode)
if (share_details.append_mode == 'a'):
	print """<tr><td><div style = 'display: block; margin-top: 2%; margin-left: auto; margin-right: auto; text-align: center; border: 0px solid #736f6e; vertical-align: center; color: darkred; font: 16px Arial;'>You can't set permissions since 'Append mode' is enabled for this path!</div></td></tr>""";

else:
	print """                               <tr>
                                        <td colspan = "3" align = "left" valign = "top">
                                        <table width = "685" border = "0"  cellspacing = "0" cellpadding = "0">
                                        <tr>
                                        <td width = '2%'>
                                        </td>
                                        <td width = "1%" class = "table_heading" height = "50px" valign = "middle">
                                                <B>Read</B><BR>
                                                                                                                             
                                        </td>
                                        <td width = "1%" class = "table_heading" height = "50px" valign = "middle">
                                                <B>Write</B><BR>
                                        </td>
                                        <td width = "1%" class = "table_heading" height = "50px" valign = "middle">
                                                <B>Execute</B><BR>
                                        </td>
                                </tr>
                                <tr>
                                        <td width = '2%'>
                                                <B>Owner</B>
                                        </td>
                                        <td width = "1%" class = "table_heading" height = "50px" valign = "middle">
                                                <input type = 'checkbox' name = 'o_read_perm' value = '4' """ + o_read_checked + """ """ + share_details.alldisabled + """>
                                        </td>
                                        <td width = "1%" class = "table_heading" height = "50px" valign = "middle">
                                                <input type = 'checkbox' name = 'o_write_perm' value = '2' """ + o_write_checked + """ """ + share_details.alldisabled + """>
                                        </td>
                                        <td width = "1%" class = "table_heading" height = "50px" valign = "middle">
                                                <input type = 'checkbox' name = 'o_exec_perm' value = '1' """ + o_exec_checked + """ """ + share_details.alldisabled + """>
                                        </td>
                                </tr>
                                <tr>
                                        <td>
                                                <B>Group</B>
                                        </td>
                                        <td width = "1%" class = "table_heading" height = "50px" valign = "middle">
                                                <input type = 'checkbox' name = 'g_read_perm' value = '4' """ + g_read_checked + """ """ + share_details.alldisabled + """>
                                        </td>
                                        <td width = "1%" class = "table_heading" height = "50px" valign = "middle">
                                                <input type = 'checkbox' name = 'g_exec_perm' value = '1' """ + g_exec_checked + """ """ + share_details.alldisabled + """>
                                        </td>
                                </tr>
                                <tr>
                                        <td>
                                                <B>Other</B>
                                        </td>
                                        <td width = "1%" class = "table_heading" height = "35px" valign = "middle">
                                                <input type = 'checkbox' name = 'oth_read_perm' value = '4' """ + oth_read_checked + """ """ + share_details.alldisabled + """>
                                        </td>
                                        <td width = "1%" class = "table_heading" height = "50px" valign = "middle">
                                                <input type = 'checkbox' name = 'oth_write_perm' value = '2' """ + oth_write_checked + """ """ + share_details.alldisabled + """>
                                        </td>
                                        <td width = "1%" class = "table_heading" height = "50px" valign = "middle">
                                                <input type = 'checkbox' name = 'oth_exec_perm' value = '1' """ + oth_exec_checked + """ """ + share_details.alldisabled + """>
                                        </td>
                                </tr>
                                <tr>
                                        <td></td>
                                        <td></td>
                                        <td></td>
                                        <td></td>
                                </tr>
                                <tr>
                                        <td></td>
                                        <td></td>
                                        <td></td>
                                        <td></td>
                                </tr>
                                <tr>
                                        <td colspan = '2' align = 'left'>
                                                <BR><input type = 'checkbox' name = 'restrict' """ + restrict_checked + """ """ + share_details.alldisabled + """><B>Others should not delete this share</B>
                                        </td>
                                        <td colspan = '2' align = 'left'>
                                                <BR><input type = 'checkbox' name = 'inherit' """ + inherit_checked + """ """ + share_details.alldisabled + """><B>Inherit premissions to sub-folders</B>
                                        </td>
                                </tr>
                                <tr>
                                        <td colspan = '4' class = 'table_heading'>
                                                <BR /><BR />Choose Operation:<BR />
                                                <select class = 'textbox' name = 'perm_type' """ + share_details.alldisabled + """>"""
        #if (checksmbshare[0] == 0 and checkafpshare[0] == 0):
	print """                               <option value = 'all' """ + allselected + """>All Operation</option>"""

	if (checkafpshare[0] == 0):
		print """                               <option value = 'afponly' """ + afpselected + """>AFP Only</option>"""

	if (checksmbshare[0] == 0):
		print """                               <option value = 'smbonly' """ + smbselected + """>SMB Only</option>"""

	print """                                       <option value = 'local'""" + localselected + """>Local Only</option>
                                                </select>
                                        </td>
                                </tr>
                                <tr>
                                        <td colspan = '4' align = 'right'>
                                                <BR><!--<input class = 'input1' type = 'button' name = 'assign_perms' value = 'pply' onclick = 'return permission_form();'  >-->

<button class="button_example" type="submit" name = 'local_action_but'  id = 'local_action_but' value = 'Apply'  onclick = 'validate_local_auth();' style="float:right; margin:0 0 10px 0;">Apply</button>


                                                <input type = 'hidden' name = 'hidpage_from' value = 'checked'>
                                        </td>
                                        </tr>
                                        </table>
                                        </td>
                                </tr>
                                <input type = 'hidden' name = 'hid_path' value = '""" + path + """'>
                                <input type = 'hidden' name = 'hid_share' value = '""" + share + """'>
                                <input type = 'hidden' name = 'hid_comment' value = '""" + comment + """'>
                               </form>
                        </table>
        
                                                                                                         




         </div>
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
