#!/usr/bin/python
import cgitb, sys, commands, common_methods, share_details

cgitb.enable();

nfs = '';

sys.path.append('/var/nasexe/python/');
import nfs;

# prefix the path with '/storage' so that it forms a complete path
if (share_details.path.find('/storage/') < 0):
	inputparam = '/storage/' + share_details.path;

else:
	inputparam = share_details.path;

# get the current settings for nfs
nfs_status = nfs.getstatus(inputparam);

# initializing all the options for nfs
smbdisabled = '';
insecure_disabled = '';

readonly_string = '';
writable_string = '';

nfs_checked      = '';
nfs_style        = 'none';
insecure_checked = '';
synch_checked    = '';
ins_checked      = '';
all_sq_checked   = '';
no_root_checked  = '';

# nfs settings retreived from the nfs.getstatus() method
if (nfs_status['use_nfs'] == 'on'):
	nfs_style = 'table';
	nfs_checked = 'checked';
else:
	insecure_checked = 'checked'

if (nfs_status['insecure'] == 'on'):
	insecure_checked = 'checked';

if (nfs_status['sync'] == 'on'):
	synch_checked = 'checked';

if (nfs_status['insecure_locks'] == 'on'):
	ins_checked = 'checked';

if (nfs_status['no_root_squash'] != 'on'):
	all_sq_checked = 'checked';

if (nfs_status['no_root_squash'] == 'on'):
	no_root_checked = 'checked';
	
if (all_sq_checked == ''):
	no_root_checked = 'checked';

allow_ip_val = nfs_status['read_ips'];
write_ip_val = nfs_status['write_ips'];

# check for nfs over rdma
check_for_nfs_over_rdma_command = 'sudo /var/nasexe/nfs_rdma_active check';
nfs_over_rdma                   = commands.getoutput(check_for_nfs_over_rdma_command);

if (nfs_over_rdma == 'active'):
	insecure_checked = 'checked';
	insecure_disabled = 'disabled';

print common_methods.share_nfs_wait;

print """
<table width = "100%" border = "0" cellspacing = "0" cellpadding = "0" name = 'disp_tables' id = 'id_nfs_settings' style = 'display: """ + share_details.share_nfs_style + """; """ + share_details.stylestring + """;'>
<form name = 'nfs_setup' method = 'POST' action = 'nfs_settings.py'>
		<tr>
			<td height = "33px" width = "8" align = "left">
				<img src = "../images/rightside_left.jpg" width = "8" height = "33" />
			</td>
			<td width = "669" height = "33px" align = "left" valign = "middle" class = "right_bg rightsidemenuheading">			
				<a class = 'link' href = 'nfs_share_access_help.php' onclick = "window.open('nfs_share_access_help.php', 'help', 'location = no, height = 500, width = 600'); return false;">""" + common_methods.getimageicon() + """</a>
				NFS settings
			</td>
			<td height = "33px" width = "8" align = "right">
				<img src = "../images/rightside_right.jpg" />
			</td>
		</tr>
		<tr>
			<td colspan = "3" align = "left" valign = "top">
			<table width = "100%" border = "0" cellspacing = "0" cellpadding = "0" class = "outer_border">
			<tr>
			<td class = "table_heading" height = "70px" valign = "middle">
				<input type = 'checkbox' name = 'use_nfs' """ + nfs_checked + " " + smbdisabled +  """ """ + share_details.alldisabled + """ onclick = 'return show_frame();'>&nbsp;<B>Use NFS</B><BR><BR>
			</td>
		</tr>
		<tr>
			<td>
				<div  id = 'nfs_param' name = 'nfs_params' style = 'display: """ + nfs_style + """; font-weight: bold;'>
				<table align = 'center' style = 'font-weight: bold; width: 100%;'>
					<tr>
						<td width = '40%'>
							Allow access IP
						</td>
						<td>
							<input class = 'input' type = 'text' name = 'access_ip' value = '""" + allow_ip_val + """' style = 'width: 100%;' """ + smbdisabled + """ """ + share_details.alldisabled + """> <I>(Use comma separator if IPs more than one.)</I>
						</td>
					</tr>
					<tr>
						<td>
							Allow write IP
						</td>
						<td>
							<input class = 'input' type = 'text' name = 'write_ip' value = '""" + write_ip_val + """' style = 'width: 100%;' """ + smbdisabled + """ """ + share_details.alldisabled + """><BR><BR>
						</td>
					</tr>
					<tr>
						<td valign = 'middle'  align = 'left' colspan = '2'>
							<input type = 'checkbox' name = 'insecure' """ + insecure_checked + " " + insecure_disabled+ " " + smbdisabled + """ """ + share_details.alldisabled + """>&nbsp;Insecure<BR>
							<input type = 'checkbox' name = 'synchronous' """ + synch_checked + " " + smbdisabled + """ """ + share_details.alldisabled + """>&nbsp;Synchronous<BR>
							<input type = 'checkbox' name = 'ins_locks' """ + ins_checked + " " + smbdisabled + """ """ + share_details.alldisabled + """>&nbsp;Insecure locks<BR><BR>
							<input type = 'radio' name = 'no_root' value = 'no_root' """ + no_root_checked + " " + smbdisabled + """ """ + share_details.alldisabled + """>&nbsp;No root squash<BR>
							<input type = 'radio' name = 'no_root' value = 'all_squash' """ + all_sq_checked + " " + smbdisabled + """ """ + share_details.alldisabled + """>&nbsp;All squash<BR><BR>
							Optional parameters:<BR>
							<input class = 'textbox' type = 'text' name = 'optional' """ + share_details.alldisabled + """>
						</td>
					</tr>
				</table>
				</div>
			</td>
		</tr>
		<tr>
			<td align = 'right'>
				<!--<BR><input class = 'input1' type = 'button' name = 'action_but' value = 'Apply' onclick = 'return validate_nfs_form();' """ + smbdisabled + """>-->

				  <span style="margin-left: 54%;" ><span id="button-one"><button type = 'button' name="action_but" value="Apply" onclick = 'return validate_nfs_form();' style = 'width:65px; background-color:#E8E8E8; border:none; float:none;font-size: 86%; ' title="Apply\" """ + share_details.alldisabled + """><a style="font-size:85%;">Apply</a></button></span></span>
				<input type = 'hidden' name = 'hid_share' value = '""" + share_details.share + """'>
				<input type = 'hidden' name = 'hid_path' value = '""" + share_details.path + """'>
				<input type = 'hidden' name = 'hid_comment' value = '""" + share_details.comment + """'>
				<input type = 'hidden' name = 'hid_nfs' value = 'nfs'>
				<input type = 'hidden' name = 'hid_guest'>
				<input type = 'hidden' name = 'hidpage_from' value = 'checked'>
			</td>
			</td></tr></table>
		</tr>
	</form>
	</table>"""
#""" % (share_details.share, share_details.path, share_details.comment);
