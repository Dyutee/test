#!/usr/bin/python
import cgitb, common_methods, commands, share_details, share_smb_settings
cgitb.enable();

# display style set for append mode form
append_mode_style = 'none';

# assign the path from share_details to path_for_append
path_for_append = share_details.path;

# getting the connection status from conn_status() method definedin common_methods.py
connstatus = common_methods.conn_status();

append_mode = '';

# remove the trailing slash at the end of the path
path_for_append = path_for_append + '###';
path_for_append = path_for_append.replace('/###', '');
path_for_append = path_for_append.replace('###', '');

if (path_for_append.find('/storage/') < 0):
	path_for_append = '/storage/' + path_for_append;

# call the method to get the append mode settings
append_mode = common_methods.get_appendmode(path_for_append);

appmessage = '';

# when log path is enabled for a share, append mode can't be enabled for this share. so the enable append mode option is disabled when
# lo path is enabled for that particular share
if (share_smb_settings.smbdisabled == 'disabled'):
	appmessage = '<font color = \'red\'>(You can\'t enable append mode since this share is set as log path!)</font>';

# if append mode is 'a' then append mode option should be checked state, else blank
if (append_mode == 'a'):
	append_checked = 'checked';

else:
	append_checked = '';

# this is a div which shows the 'processing...' image
print common_methods.wait_for_response;

print """
	<form name = 'share_append' method = 'POST' action = 'enable_append_mode.py'>
        <table width = "685" border = "0" cellspacing = "0" cellpadding = "0" name = 'disp_tables' id = 'id_append_mode' style = 'display: """ + share_details.append_mode_style + """; """ + share_details.stylestring + """;' class = 'outer_border'>
                <tr>
                        <td height = "33px" width = "8" align = "left">
                                <img src = "../images/rightside_left.jpg" width = "8" height = "33" />
                        </td>
                        <td width = "669" height = "33px" align = "left" valign = "middle" class = "right_bg rightsidemenuheading">
                                <a class = 'link' href = 'append_mode_settings_help.php' onclick = "window.open('append_mode_settings_help.php', 'help', 'location = no, height = 500, width = 600, scrollbars = 1'); return false;"><?= $image_icon ?></a>
                                Append mode
                        </td>
                        <td height = "33px" width = "8" align = "right">
                                <img src = "../images/rightside_right.jpg" />
                        </td>
                </tr>
                <tr>
                        <td colspan = "3" align = "left" valign = "top">
                        <table width = "685" border = "0" cellspacing = "0" cellpadding = "0" class = "border">
                        <tr>
                                <td width = "1%" class = "table_heading" height = "70px" valign = "middle">"""
if (connstatus == 'Join is OK'):
	# append mode doesn't work in ads or nis connection
	# if authentication is set to nis or ads, the error message is displayed.
	# append mode works only in local authentication mode
        print common_methods.append_mode_error;

else:
	print """<input type = 'checkbox' name = 'use_append_mode' onclick = 'return enable_append_mode();' %s %s %s>Enable append mode %s""" % (share_details.alldisabled, append_checked, share_smb_settings.smbdisabled, appmessage);

share   = share_details.share.strip();
path    = share_details.path.replace('/storage/', '');
comment = share_details.comment.strip();

print """                                </td>
                        </tr>
                        </table>
                        </td>
                </tr>
        </table>
        <input type = 'hidden' name = 'hid_share' value = '%s'>
        <input type = 'hidden' name = 'hid_comment' value = '%s'>
        <input type = 'hidden' name = 'hid_path' value = '%s'>
        </form>""" % (share, comment, path);

