#!/usr/bin/python
import common_methods, os, commands, sys

from fs2global import *

image_icon = common_methods.getimageicon();
shares_array = [];

shares_file  = '/var/www/global_files/shares_global_file';
shares_array = common_methods.read_file(shares_file);

check_log_path_command = 'sudo grep "SMBLOGPATH=" /var/nasconf/smb-log.conf';
check_log              = commands.getoutput(check_log_path_command);

#list(d1, lpath) = explode('=', check_log);
lpath = check_log[check_log.find('=') + 1:];

del_shares_style = 'none';

querystring = os.environ['QUERY_STRING'];

response = common_methods.getsubstr(querystring, '&act=', '&');

if (response == 'del_share_done'):
	del_shares_style = 'block';
	
#print common_methods.wait_for_delete;
print """			<form name = 'share_maintenance' action = 'delete_share.py'>
				<table width = "685" border = "0" cellspacing = "0" cellpadding = "0" bgcolor="#f9f9f9" style='display: """ + del_shares_style + """' id='id_share_info' name='disp_tables'>
					<tr>
						<td height = "33px" width = "8" align = "left">
							<img src = "../images/rightside_left.jpg" width = "8" height = "33" />
						</td>
						<td width = "669" height = "33px" align = "left" valign = "middle" class = "right_bg rightsidemenuheading">
							<!--<a class = 'link' href = 'share_maintenance_help.php' onclick = "window.open('share_maintenance_help.php', 'help', 'location = no, height = 500, width = 600, scrollbars = 1'); return false;">""" + common_methods.getimageicon() + """ </a>-->
							<div id="item_2" class="item" style="width:35%;">         
                        """+image_icon+""" Shares Information/Delete Shares
                        <div class="tooltip_description" style="display:none" title="Share Information">
                                <span>This gives information about the resources that are being used by the system.</span><br/><br/>
                                <table border="0">
                                <tr class="spaceUnder">
                                <td valign="top" align="left"><strong style="color:#b2b2b2; padding:0px 2px 0px 2px;">Share Info:</strong></td>
                                <td>Display All the share Information which one is used.if any share is in used ,then it is a tick mark of that share</td>
                                </tr>
                                <tr class="spaceUnder">
                                <td valign="top" align="left"><strong style="color:#cccccc; padding:0px 2px 0px 2px;">Delete Share:</strong></td>
                                <td>Select the Share to Delete.</td>
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
						<font color = 'darkred'><B>* You can't delete the shares which are set as SMB log path</B></font>
                                                <table width = "685" border = "0" cellspacing = "0" cellpadding = "0" class = 'border'>
						<tr bgcolor = "#f5f5f5">
							<td width = "1%" class = "table_heading" height = "35px" valign = "middle" align = 'center'>
								<input type = 'checkbox' name = 'delete_all' id = 'id_select_all' title = 'Check this to select all' onclick = 'return select_all_shares();'>
							</td>
							<td width = "172" class = "table_heading" height = "35px" valign = "middle">
								Share
							</td>
							<td width = "172" class = "table_heading" height = "35px" valign = "middle">
								Path
							</td>
							<td width = "172" class = "table_heading" height = "35px" valign = "middle" align = 'center'>
								Audit
							</td>
							<td width = "172" class = "table_heading" height = "35px" valign = "middle" align = 'center'>
								SMB Log Path
							</td>
							<td width = "172" class = "table_heading" height = "35px" valign = "middle" align = 'center'>
								SMB
							</td>
							<td width = "172" class = "table_heading" height = "35px" valign = "middle" align = 'center'>
								NFS
							</td>
							<td width = "172" class = "table_heading" height = "35px" valign = "middle" align = 'center'>
								FTP
							</td>
							<td width = "172" class = "table_heading" height = "35px" valign = "middle" align = 'center'>
								AFP
							</td>
						</tr>"""
	
if (isinstance(shares_array, (list, tuple))):
	if (len(shares_array) > 0):
		for share in shares_array:
			#list(share_name, share_path, comment) = explode(':', share);
			share_name = share[:share.find(':')];
			share_path = share[share.find(':') + 1:share.rfind(':')];
			comment    = share[share.rfind(':') + 1:];

			share_name = share_name.strip();
			share_path = share_path.strip();
			
			if (comment != None):
				comment = comment.strip();
							
			disp_share_path = share_path.replace('/storage/', '');
			disp_share_path = disp_share_path.strip();

			share_name = share_name.strip();
			share_path = share_path.strip();

			sharesconffile = smb_share_conf_dir + share_name;

			check_for_smb = commands.getstatusoutput('ls %s' % sharesconffile);

			check_for_nfs_command = 'sudo grep \"' + share_path + '\" /etc/exports';
			check_for_nfs = commands.getoutput(check_for_nfs_command);
			
			check_for_afp_command = 'sudo grep \"' + share_name + '\" /etc/netatalk/AppleVolumes.default';
			check_for_afp = os.path.isfile(afp_share_conf_dir+share_name) 

			check_for_ftp_auth = os.path.isfile(ftp_share_conf_dir+share_name+".auth")
			check_for_ftp_anon = os.path.isfile(ftp_share_conf_dir+share_name+".anon")
			#print check_for_ftp

			check_for_ftp_command1 = 'sudo grep "/' + share_name + '>" /var/nasconf/ftp_anonymous.conf';
			check_for_ftp1 = commands.getoutput(check_for_ftp_command1);

			check_for_ftp_command2 = 'sudo grep "/' + share_name + '>" /var/nasconf/ftp_users.conf';
			check_for_ftp2 = commands.getoutput(check_for_ftp_command2);

			check_for_audit_command = 'sudo grep -A10 "\\[' + share_name + '\\]" /var/nasconf/share_conf_file|tail -1';
			check_for_audit = commands.getoutput(check_for_audit_command);

			index_of_adt = check_for_audit.find('ull_audit:');

			check_audit = commands.getstatusoutput('sudo grep "full_audit:success" /var/nasconf/smbconf/"'+share_name+'"')
				
			#if (index_of_adt > 0):
			#	audit_active_png = '<img src = \'../images/tick_active.png\'>';

			#else:
			#	audit_active_png = '<font color = \'darkred\'>--</font>';

			if(check_audit[0] == 0):
				audit_active_png = '<img src = \'../images/tick_active.png\'>'
			else:
				audit_active_png = '<font color = \'darkred\'>--</font>'

			if (check_for_ftp1 != '' or check_for_ftp2 != ''):
				ftp_active_png = '<img src = \'../images/tick_active.png\'>';

			else:
				ftp_active_png = '<font color = \'darkred\'>--</font>';

			if (check_for_smb[0] == 0):
				smb_active_png = '<img src = \'../images/tick_active.png\'>';

			else:
				smb_active_png = '<font color = \'darkred\'>--</font>';

			if (check_for_nfs != ''):
				nfs_active_png = '<img src = \'../images/tick_active.png\'>';

			else:
				nfs_active_png = '<font color = \'darkred\'>--</font>';

			if (check_for_afp == True ):
				afp_active_png = '<img src = \'../images/tick_active.png\'>';

			else:
				afp_active_png = '<font color = \'darkred\'>--</font>';

			if ((check_for_ftp_auth == True) or (check_for_ftp_anon == True)):
				ftp_active_png = '<img src = \'../images/tick_active.png\'>';
			else:
				ftp_active_png = '<font color = \'darkred\'>--</font>';

			disabled = '';
			char = '';
			log_path_active = '<font color = \'darkred\'>--</font>';

			if (lpath == share_path):
				log_path_active = '<img src = \'../images/tick_active.png\'>';
				disabled = 'disabled';
		
			print """					<tr>
							<td bgcolor = "#f5f5f5" width = "172" class = "table_content" height = "35px" valign = "middle" align = 'center'>
								<input type = 'checkbox' name = 'delete_share[]' id = 'id_del_share' value = '%s:%s' %s >""" % (share_name, disp_share_path, disabled)
			print """			</td>
							<td bgcolor = "#f5f5f5" width = "172" class = "table_content" height = "35px" valign = "middle">
								<a class = 'sidenav' href = 'show_shares.py?s1=%s'>%s</a>""" % (share_name, share_name)
			print """			</td>
							<td width = "172" class = "table_content" height = "35px" valign = "middle">"""
			print						 disp_share_path
			print """				</td>
							<td width = "172" class = "table_content" height = "35px" valign = "middle" align = 'center'>"""
			print						 audit_active_png 
			print """				</td>
							<td width = "172" class = "table_content" height = "35px" valign = "middle" align = 'center'>"""
			print						 log_path_active 
			print """				</td>
							<td align = 'center'  width = "172" class = "table_content" height = "35px" valign = "middle" align = 'center'>"""
			print						 smb_active_png 
			print """				</td>
							<td align = 'center' width = "172" class = "table_content" height = "35px" valign = "middle" align = 'center'>"""
			print						 nfs_active_png 
			print """				</td>
							<td align = 'center'  width = "172" class = "table_content" height = "35px" valign = "middle" align = 'center'>"""
			print						 ftp_active_png 
			print """				</td>
							<td align = 'center'  width = "172" class = "table_content" height = "35px" valign = "middle" align = 'center'>"""
			print						 afp_active_png 
			print """				</td>
						</tr>"""
					
	else:
		print """	
						<tr>
							<td colspan = '9' align = 'center'>
								<B>No shares created!</B>
							</td>
						</tr>"""
		
	print """				</table>
					</td>
				</tr>
			       <td colspan = "3" align = "left" valign = "top">   """
				    
	if (len(shares_array) > 0):

		print """<BR>			<table align = 'center' width = '685'>
						<tr>
							<td align = 'right'>
							<span style="margin-left: 54%;" ><span id="button-one"><button type = 'button' name="delete" id="id_delshare" value="Delete Selected" onclick ="return validate_delete_share();" style = 'width:85px; background-color:#E8E8E8; border:none; float:none;font-size: 100%; ' title="Delete"><a style="font-size:70%;width:100%;">Delete Selected</a></button></span></span>
							<span style="margin-right:2%;"><span id="button-one"><button type = 'button'  name = 'cancel' value = 'Cancel' onclick = 'location.href = "main.py?page=nas";' style = 'width:63px; background-color:#E8E8E8; border:none; right: left;font-size: 94%; ' title="Cancel"><a style="font-size:75%;"  >Cancel</a></button></span></span>
								<!--<input id = 'id_delshare' class = 'input1' type = 'button' name = 'delete' value = 'Delete selected' onclick = 'return validate_delete_share();'>-->
								<!--<input class = 'input1' type = 'button' name = 'cancel' value = 'Cancel' onclick = 'location.href = "main.py?page=nas";'>-->
							</td>
						</tr>
					</table>"""
		
	print """                </td>
			     </tr>
			</table>
				</form>"""
