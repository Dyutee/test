#!/usr/bin/python
import cgitb, sys, common_methods, string, commands, traceback, os, include_files
cgitb.enable()

sys.path.append('/var/nasexe/python/');
import nfs, tools;

sys.path.append('../modules/');
import disp_except;

try:
	checkoptionalvalue = '';
	check_nfs_service = nfs.get_nfs_service_status();

	additional_options_array = [];
	additional_options_array.append('no_wdelay');
	additional_options_array.append('no_acl');
	

	get_share   = '';
	alldisabled = '';

	querystring = os.environ['QUERY_STRING'];

	if (querystring.find('share_name') >= 0):
		get_share = querystring[querystring.find('share_name=') + len('share_name='):];

	sharedetails = tools.get_share(get_share);
	#-----------------------------ha--------------------------------#
	par_share_det = tools.get_share(get_share,debug=False)
	share_ha_nodename = par_share_det["share"]["node"]
	#-----------------------------ha--------------------------------#

	if (sharedetails['id'] == 0):
		sharesinfo = sharedetails['share'];

		comment = sharesinfo['comment'];
		path    = sharesinfo['path'];

	# prefix the path with '/storage' so that it forms a complete path
	if (path.find('/storage/') < 0):
		inputparam = '/storage/' + path;

	else:
		inputparam = path;

	# get the current settings for nfs
	nfs_status_line = nfs.getstatus(inputparam,share_ha_nodename);

	# initializing all the options for nfs
	smbdisabled = '';
	insecure_disabled = '';

	readonly_string = '';
	writable_string = '';

	nfs_checked      = '';
	nfs_style        = '';
	insecure_checked = '';
	synch_checked    = '';
	ins_checked      = '';
	all_sq_checked   = '';
	no_root_checked  = '';
	optionalvalue    = '';

	opts_dropdown = '';

	if (nfs_status_line['id'] == 0):
		nfs_status = nfs_status_line['exports'];

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

		allow_ip_val  = nfs_status['read_ips'];
		write_ip_val  = nfs_status['write_ips'];

		if (write_ip_val == '*'):
			allow_ip_val = '*';

		if (nfs_status['use_nfs'] == 'on'):
			optionalvalue = nfs_status['additional_nfs_parameters'];

			if (optionalvalue != ''):
				checkoptionalvalue = ',' + optionalvalue + ',';

				if (optionalvalue.find(',') > 0):
					temp = [];
					temp = optionalvalue.split(',');

					if (len(temp) > 0):
						for opts in temp:
							if (opts != 'rw'):
								opts_dropdown += "<option value = '" + opts + "' selected>" + opts + "</option>";

			else:
				if (opts_dropdown != 'rw'):
					opts_dropdown = "<option value = '" + optionalvalue + "' selected>" + optionalvalue + "</option>";

	# check for nfs over rdma
	check_for_nfs_over_rdma_command = 'sudo /var/nasexe/nfs_rdma_active check';
	nfs_over_rdma                   = commands.getoutput(check_for_nfs_over_rdma_command);

	if (nfs_over_rdma == 'active'):
		insecure_checked = 'checked';

	print
	print """

	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer">
		<!--<div class="insidepage-heading">NAS >> <span class="content">NFS Settings</span></div>-->
		<!--tab srt-->
		<div class="searchresult-container">
		  <div class="infoheader">
		    <div id="tabs">
		      <!--<ul>
			<li><a href="#tabs-1">NFS Settings</a></li>
		      </ul>-->
		      <div id="tabs-1">

		<!--form container starts here-->
		<!--<div class="form-container">-->
		<div style="padding:10px; background-color:#e9e5e5; border-bottom:#D1D1D1 1px solid; font-weight:bold;">NFS Settings for '"""+get_share+"""' 
<!--<a href = 'main.py?page=cs'><img style="float:right; padding:0;" title = 'Back to shares' src = '../images/gobacktoshares.png' /></a>-->
</div>

		  <div class="inputwrap">"""
	if (check_nfs_service != True):
		print "<font color = 'darkred'></font>";
	print """<table align = 'center' width = "100%" border = "0" cellspacing = "0" cellpadding = "0" name = 'disp_tables' id = 'id_nfs_settings' style = 'display:block;'>
	<form name = 'nfs_setup' method = 'POST' action = 'nfs_settings.py'>
			<tr>
				<td align = "center" valign = "top">
				<table width = "100%" border = "0" cellspacing = "0" cellpadding = "0" class = "outer_border">
				<tr>
				<td class = "table_heading" height = "70px" valign = "middle">
					<!--<input type = 'checkbox' name = 'use_nfs' """ + nfs_checked + " " + smbdisabled +  """ """ + alldisabled + """ onclick = 'return show_frame();'>&nbsp;<B>Use NFS</B><BR><BR>-->
					<!--<input type = 'checkbox' name = 'use_nfs' "" onclick = 'return show_frame();'>&nbsp;<B style="color:darkred;">Use NFS</B><BR><BR>-->
				</td>
			</tr>
			<tr>
				<td>
					<div  id = 'nfs_param' name = 'nfs_params' style = 'display: """ + nfs_style + """; font-weight: bold;'>
					<table align = 'center' style = 'font-weight: bold; width: 100%;'>
						<tr>
							<td class="formleftside-content">
								Allow access IP:
							</td>
							<td Style="color:#999999;">
								<input class = 'textbox' style = 'width:55%;' type = 'text' name = 'access_ip' value = '""" + allow_ip_val + """' """ + smbdisabled + """ """ + alldisabled + """>
							</td>
						</tr>
						<tr>
							<td class="formleftside-content">
								Allow write IP:
							</td>
							<td>
								<input class = 'textbox' type = 'text' style = 'width:55%;' name = 'write_ip' value = '""" + write_ip_val + """' """ + smbdisabled + """ """ + alldisabled + """>
							</td>
						</tr>
						<tr>
							<td></td>
							<td>
								<i class="formrightside-content">(Use comma separator for multiple IPs)</i>
							</td>
						</tr>
						<tr>
							<td colspan = '2' align = 'center'>
								<table width = '90%' align = 'center' border = '0'>
								<tr><td>
								<BR><BR><input type = 'checkbox' name = 'insecure' """ + insecure_checked + " " + insecure_disabled+ " " + smbdisabled + """ """ + alldisabled + """>&nbsp;<span Style="color:#666666;">Insecure</span><BR><BR>
								<input type = 'checkbox' name = 'synchronous' """ + synch_checked + " " + smbdisabled + """ """ + alldisabled + """>&nbsp;<span Style="color:#666666;">Synchronous</span><BR><BR>
								<input type = 'checkbox' name = 'ins_locks' """ + ins_checked + " " + smbdisabled + """ """ + alldisabled + """>&nbsp;<span Style="color:#666666;">Insecure locks</span><BR><BR>
								</td><td>
								<BR><input type = 'radio' name = 'no_root' value = 'no_root' """ + no_root_checked + " " + smbdisabled + """ """ + alldisabled + """>&nbsp;<span Style="color:#666666;">No root squash</span><BR><BR>
								<input type = 'radio' name = 'no_root' value = 'all_squash' """ + all_sq_checked + " " + smbdisabled + """ """ + alldisabled + """>&nbsp;<span Style="color:#666666;">All squash</span><BR><BR>
								</td>
								</tr>
								<tr>
								<td>
								<span Style="color:darkred;">Optional parameters</span>:<BR>
								<select id = 'id_optional' name = 'optional[]' style = 'width: 60%; height: 150px;' multiple onclick = 'return move_users(this.form.id_optional, this.form.id_granted_optional, "1");'>"""
	for opts in additional_options_array:
		if (checkoptionalvalue.find(',' + opts + ',') < 0):
			print "<option value = '" + opts + "'>" + opts + "</option>";

	print """							</select></td>
									<td>
										<span Style="color:darkred;">Enabled Optional parameters</span>:<BR>
										<select id = 'id_granted_optional' name = 'granted_optional[]' style = 'width: 50%; height: 150px;' multiple onclick = 'return move_users(this.form.id_granted_optional, this.form.id_optional, "2");'>"""
	print opts_dropdown;
        print """                                                       </select>
								</td>
								<!--<td valign = 'top'>
									<B><font color = 'darkred'>Optional parameters set:</font></B><BR>
								</td> -->
								</tr></table>
							</td>
						</tr>
						<tr>
							<td colspan = '2' align = 'right'>"""
	if (nfs_status['use_nfs'] == 'on'):
		print """<button class="buttonClass" type="submit" name = 'conf' value = 'reconf' style="margin:20px 0 0 0;"  onclick = 'return validate_nfs_form();'>Update</button>"""
		print """<button class="buttonClass" type="submit" name = 'unconf' value = 'unconf'  onclick = 'return validate_nfs_form();'>Remove</button>"""
	else:
		print """<button class="buttonClass" type="submit" name = 'conf' value = 'configure'  onclick = 'return validate_nfs_form();' style="margin:20px 0 0 0;">Configure</button>"""
	
	print """						</td>
						</tr>
					</table>
					</div>
				</td>
			</tr>
			<tr>
				<td align = 'right'>
					<!--<BR><input class = 'input1' type = 'button' name = 'action_but' value = 'Apply' onclick = 'return validate_nfs_form();' """ + smbdisabled + """>-->

					  <!--<span style="margin-left: 54%;" ><span id="button-one"><button type = 'button' name="action_but" value="Apply" onclick = 'return validate_nfs_form();' style = 'width:65px; background-color:#E8E8E8; border:none; float:none;font-size: 86%; ' title="Apply\" """ + alldisabled + """><a style="font-size:85%;">Apply</a></button></span></span>-->


					<input type = 'hidden' name = 'hid_share' value = '""" + get_share + """'>
					<input type = 'hidden' name = 'hid_path' value = '""" + path + """'>
					<input type = 'hidden' name = 'hid_comment' value = '""" + comment + """'>
					<input type = 'hidden' name = 'hid_nfs' value = 'nfs'>
					<input type = 'hidden' name = 'hid_guest'>
					<input type = 'hidden' name = 'hidpage_from' value = 'checked'>
				</td>
				</td></tr></table>
			</tr>
		</form>
		</table>





		  </div>
	</div>
	<!--form container ends here-->
	<p>&nbsp;</p>
	      <!--</div>-->

	  </div>
	</div>
	</div>
	"""
except Exception as e:
	disp_except.display_exception(e);
