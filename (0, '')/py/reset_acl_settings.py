#!/usr/bin/python
#_*_ coding: UTF-8 _*_                                          

#enable debugging                                       
import cgitb, header, os, common_methods, set_acl, commands
cgitb.enable()

image_icon = common_methods.getimageicon();
share_path = set_acl.path_acl;

disp_path = share_path.replace('/storage/', '');

sharesarray = [];
sharesarray = common_methods.get_shares_array();

sharename     = '';
aclsharearray = [];

connstatus = common_methods.conn_status();

if (connstatus == 'local connection'):
	if (len(sharesarray) > 0):
		for share in sharesarray:
			sharename = share[:share.find(':')];
			sharepath = share[share.find(':') + 1:share.rfind(':')];

			checkacl  = commands.getstatusoutput('sudo getfacl "%s"|grep "mask"' % sharepath);

			if (checkacl[0] == 0):
				aclsharearray.append(sharename + '-' + sharepath);

	print """
		<form name = 'reset_acl_settings' method = 'POST'>
			<table name = 'disp_tables' width = "685" border = "0"  cellspacing = "0" cellpadding = "0" id = 'id_reset_acl' style = 'display:none;' class = 'outer_border'>
				<tr>
					<td height = "33px" width = "8" align = "left">
						<img src = "../images/rightside_left.jpg" width = "8" height = "33" />
					</td>
					<td width = "669" height = "33px" align = "left" valign = "middle" class = "right_bg rightsidemenuheading">
						<!--<a class = 'link' href = 'reset_acl_help.php' onclick = "window.open('#', 'help', 'location = no, height = 500, width = 600, scrollbars = 1'); return false;"></a>-->
		<div id="item_2" class="item">         
		"""+image_icon+""" Reset ACL Settings
		<div class="tooltip_description" style="display:none" title="Reset ACL">
			<span>This gives information about the resources that are being used by the system.</span><br/><br/>
			<table border="0">
			<tr class="spaceUnder">
			<td valign="top" align="left"><strong style="color:#b2b2b2; padding:0px 2px 0px 2px;">Reset Acl:</strong></td>
			<td>This option is used to reset the already set ACL for a share. This can be applicable to the sub folders inside</td>
			</tr>
			</table>
			</div></div>
					</td>
					<td height = "33px" width = "8" align = "right">
						 <img src = "../images/rightside_right.jpg" />
					</td>
				</tr>
				<tr>
					<td colspan = "3" align = "left" valign = "top">
					<table width = "685" border = "0"  cellspacing = "0" cellpadding = "0">
					<tr>
						<td class = "table_heading" height = "70px" valign = "middle">
							Share path
						</td>
						<td class = "table_content" height = "70px" valign = "middle" bgcolor = "#f5f5f5">
							<select class = 'textbox' name = 'share_path' style = 'width: 99%;'>"""
	for share in aclsharearray:
		sharename = share[:share.find('-')];
		sharename = sharename.strip();

		sharepath = common_methods.get_share_path(sharename);
		
		if (sharepath != 1):
			disppath = sharepath.replace('/storage/', '');

			print "<option value = '" + disppath + "'>" + sharename + " - " + disppath + "</option>";

	print """</select>
							<!--<input class = 'input' type = 'text' readonly name = 'share_path' value = '""" + disp_path + """' style = 'width: 99%;'>-->					</td>
					</tr>
					<tr>
						<td colspan = '2'>
							<input type = 'checkbox' name = 'acl_recur' checked disabled><B>Reset ACLs for sub-folders also</B>
						</td>
					</tr>
					<tr>
						<td align = 'right' colspan = '2'>
							<span style='margin-left: 54%;' ><span id='button-one'><button type = 'button' name='reset_acl' value='Reset ACL settings' style = 'width:67px; background-color:#E8E8E8; border:none; float: right;font-size: 98%;' title='Reset' onclick = 'return reset_acl_params(document.reset_acl_settings.share_path.value, "");' ><a style='font-size:85%;'>Reset ACL settings</a></button></span></span>


					</td>
					</tr>
					</table>
					</td>
				</tr>
			</table>
			<input type = 'hidden' name = 'hid_share' value = '""" + sharename + """'>
			<input type = 'hidden' name = 'hid_comment' value = ''>
			<input type = 'hidden' name = 'hid_path' value = ''>
			</form>
			<!--<table name = 'disp_tables' width = "685" border = "0"  cellspacing = "0" cellpadding = "0" id = 'id_reset_acl' style = 'display:none;' class = 'outer_border'>
				<tr>
					<td height = "33px" width = "8" align = "left">
						<img src = "../images/rightside_left.jpg" width = "8" height = "33" />
					</td>
					<td width = "669" height = "33px" align = "left" valign = "middle" class = "right_bg rightsidemenuheading">
						<a class = 'link' href = 'append_mode_settings_help.php' onclick = "window.open('append_mode_settings_help.php', 'help', 'location = no, height = 500, width = 600, scrollbars = 1'); return false;"></a>
						Reset ACL settings
					</td>
					<td height = "33px" width = "8" align = "right">
						 <img src = "../images/rightside_right.jpg" />
					</td>
				</tr>
				<tr>
					<td colspan = '3' align = 'center'>
					</td>
				</tr>
			</table>-->
				 """

else:
	print """
	<table width = "685" cellspacing = "0" cellpadding = "0" name = 'disp_tables' id = 'id_reset_acl' style = 'display: none; border-collapse: collapse;' class = 'outer_border' border = '0'>
		<tr>
			<td align = 'center'>"""
	print common_methods.acl_message;
	print """	</td>
		</tr>
	</table>"""



