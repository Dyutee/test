#!/usr/bin/python
import cgitb, commands, common_methods, os, share_details, sys;
cgitb.enable();

sys.path.append('/var/nasexe/python/');
from fs2global import *;
from tools import *;

querystring = os.environ['QUERY_STRING'];

if (querystring.find('share_name') >= 0):
	get_share = querystring[querystring.find('share_name=') + len('share_name='):];

image_icon = common_methods.getimageicon();

print """<form id = 'id_edit_share' name = 'edit_this_share' method = 'POST'>
	<table width = "685" border = "0" cellspacing = "0" cellpadding = "0" name = 'disp_tables' id = 'id_edit_this_share' style = 'display: """ + share_details.edit_share_style + """; """ + share_details.stylestring + """' class = 'outer_border'>
		<tr>
                	<td height = "33px" width = "8" align = "left">
                        	<img src = "../images/rightside_left.jpg" width = "8" height = "33" />
                        </td>
                        <td width = "669" height = "33px" align = "left" valign = "middle" class = "right_bg rightsidemenuheading">
				<!--<a class = 'link' href = 'edit_shares_help.php' onclick = "window.open('edit_shares_help.php', 'help', 'location = no, height = 500, width = 600'); return false;"><?= $image_icon ?></a>-->
				<div id="item_2" class="item" style="width: 17%;">         
                        """+image_icon+""" Edit this Share
                        <div class="tooltip_description" style="display:none" title="Edit Share">
                                <span>This gives information about the resources that are being used by the system.</span><br/><br/>
                                <table border="0">
                                <tr class="spaceUnder">
                                <td valign="top" align="left"><strong style="color:#b2b2b2; padding:0px 2px 0px 2px;">Edit Share:</strong></td>
                                <td>Once the Share is created, you cannot change its location or share name. But you can change its comment from here. Provide a meaningful comment which describes this share.</td>
                                </tr>

                                </table>
                                </div></div>

			</td>
			<td height = "33px" width = "8" align = "right">
				<img src = "../images/rightside_right.jpg" />
			</td>
		</tr>"""

readonly_text = '';
edit_message = '';

comment = share_details.comment;

if (comment == ''):
	commentline = commands.getoutput('grep "sharecomm=" /tmp/details_of_share');

	comment = commentline[commentline.find('=') + 1:];

check_path = smb_share_conf_dir + '/' + share_details.share;

test_share = check_file_exits(check_path);

if (test_share == 'exists'):
	readonly_text = 'readonly';
	edit_message  = 'Can\'t edit since SMB is active!';

print """		<tr>
			<td colspan = "3" align = "left" valign = "top">
			<table width = "685" border = "0" cellspacing = "0" cellpadding = "0">
			<tr>
				<td width = "72" class = "table_heading" height = "35px" valign = "middle">
					Share name
				</td>
				<td width = "172" class = "table_content" height = "35px" valign = "middle" bgcolor = "#f5f5f5">
					<input class = 'input' type = 'text' name = 'share' value = '""" + share_details.share + """' readonly style = 'width: 90%;'>
				</td>
		</tr>
		<tr>
			<td width = "72" class = "table_heading" height = "35px" valign = "middle">
				Comment
			</td>
			<td width = "172" class = "table_content" height = "35px" valign = "middle" bgcolor = "#f5f5f5">
				<input class = 'input' type = 'text' name = 'comment' value = '""" + comment + """' style = 'width: 90%;' """ + share_details.alldisabled + """>
			</td>
		</tr>
		<tr>
			<td width = "72" class = "table_heading" height = "35px" valign = "middle">
				Share Path
			</td>
			<td width = "172" class = "table_content" height = "35px" valign = "middle" bgcolor = "#f5f5f5">"""
path    = common_methods.get_share_path(get_share);
comment = common_methods.get_share_comment(get_share);
common_methods.alert(path);

disppath = path.replace('/storage/', '');
common_methods.alert(dsippath);

print """				<input class = 'input' type = 'text' readonly name = 'share_path' value = '""" + disppath + """' style = 'width: 90%;'>
			</td>
			</tr>
			<tr>
				<td colspan = '2'>"""
#print edit_message
print """				</td>
			</tr>
			<tr>
				<td colspan = '2' align = 'right'>
				<!--<input class = 'input1' type = 'button' name = 'action_but' value = 'Apply' onclick = 'return submit_edit_share_form();'>-->
				     <div><span id="button-one"><button type = 'button'  onclick = 'return submit_edit_share_form();' style = ' background-color:#FFFFFF;border:none; float:right;  font-size: 86%; ' title="Apply\" """ + share_details.alldisabled + """><a style="font-size:85%;"  >Apply</a></button></span></div>
        </div>

					<input type = 'hidden' name = 'hidshare' value = '""" + share_details.share + """'>
				</td>
			</tr>
			</table>
			</td>
		</tr>
	</table>
	</form>"""
