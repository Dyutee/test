#!/usr/bin/python
#_*_ coding: UTF-8 _*_

#enable debugging
import traceback
try:
	import cgitb, header, os, sys, commands, common_methods, traceback, string
	cgitb.enable()
	image_icon = common_methods.getimageicon();

	sys.path.append('/var/nasexe/python/')
        import backuprestore as br
	import savecliconf

	import urllib

	log_array = []
        log_file = common_methods.log_file
        logstring = ''

	display_take_backup    = 'block'
	display_restore_backup = 'none'
	display_cli_backup     = 'none';
	display_cli_restore    = 'none';

	if(header.form.getvalue("fs2_backup_but")):
		create_backup = br.backup(for_web="yes") 
		if (create_backup["id"]==0):
			print"""<div id = 'id_trace'>"""
			print create_backup["desc"]
			print "</div>"
		else:
			print"""<div id = 'id_trace_err'>"""
			print create_backup["desc"]
			print "</div>"

		#createcli_backup = br.backup() 
		
		#if (createcli_backup['id'] > 0):
		#	print createcli_backup['desc'];

		ss = str(create_backup["desc"])
                logstring = str(common_methods.now) + '<<>>From: ' + common_methods.remote_ip + '<<>>' + str(ss);
                log_array.append(logstring);

		display_take_backup = 'none'
		display_restore_backup = 'block'

	if(header.form.getvalue("restore_backup")):
		get_backup_id = header.form.getvalue("backup_id")
		split_gbi = string.split(get_backup_id, "/")
		filename = split_gbi[6]

		copy_to_tmp = commands.getstatusoutput('sudo cp "'+get_backup_id+'" /tmp/')
		if(copy_to_tmp[0]==0):
			restore_backup = br.restore("yes",filename)
			if(restore_backup["id"]==0):	
				print"""<div id = 'id_trace'>"""
				print restore_backup["desc"]
				print "</div>"
			else:
				print"""<div id = 'id_trace_err'>"""
				print restore_backup["desc"]
				print "</div>"

			
		else:
			print"""<div id = 'id_trace_err'>"""
			print "Error Copying to tmp!"
			print "</div>"

		ss = str(restore_backup["desc"])
                logstring = str(common_methods.now) + '<<>>From: ' + common_methods.remote_ip + '<<>>' + str(ss);
                log_array.append(logstring);	

		display_take_backup = 'none'
		display_restore_backup = 'block'

	if(header.form.getvalue("restore_clibackup")):
		get_backup_id = header.form.getvalue("cli_backup_id")
		split_gbi = string.split(get_backup_id, "/")
		filename = split_gbi[5]

		copy_to_tmp = commands.getstatusoutput('sudo cp "'+get_backup_id+'" /tmp/')
		if(copy_to_tmp[0]==0):
			restore_cli_backup = savecliconf.restore(filename)

			if(restore_cli_backup == "success"):	
				print"""<div id = 'id_trace'>"""
				print "Restore successful";
				print "</div>"
				ss = 'Restore Successful'

			else:
				print"""<div id = 'id_trace_err'>"""
				print "Restore failed!"
				print "</div>"
				ss = 'Restore Failed'

			
		else:
			print"""<div id = 'id_trace_err'>"""
			print "Error Copying to tmp!"
			print "</div>"

                logstring = str(common_methods.now) + '<<>>From: ' + common_methods.remote_ip + '<<>>' + str(ss);
                log_array.append(logstring);	

		display_take_backup    = 'none'
		display_cli_backup     = 'none';
		display_restore_backup = 'none';
		display_cli_restore    = 'block';

	if(header.form.getvalue("delete_backup")):
		get_backup_id = header.form.getvalue("backup_id")
		delete_backup = commands.getstatusoutput("sudo rm -rf "+get_backup_id)
		if(delete_backup[0]==0):
			print"""<div id = 'id_trace'>"""
			print "Backup Deleted Successfully."
			print "</div>"

			ss = str("Backup Deleted Successfully.")
			logstring = str(common_methods.now) + '<<>>From: ' + common_methods.remote_ip + '<<>>' + str(ss);
			log_array.append(logstring);

		else:
			print"""<div id = 'id_trace_err'>"""
			print "Error Deleting Backup!"
			print "</div>"

			ss = str("Error Deleting Backup!")
                        logstring = str(common_methods.now) + '<<>>From: ' + common_methods.remote_ip + '<<>>' + str(ss);
                        log_array.append(logstring);

		display_take_backup = 'none'
		display_restore_backup = 'block'

	if(header.form.getvalue("delete_clibackup")):
		get_backup_id = header.form.getvalue("cli_backup_id")
		delete_backup = commands.getstatusoutput("sudo rm -rf "+get_backup_id)
		if(delete_backup[0]==0):
			print"""<div id = 'id_trace'>"""
			print "Backup Deleted Successfully."
			print "</div>"

			ss = str("Backup Deleted Successfully.")
			logstring = str(common_methods.now) + '<<>>From: ' + common_methods.remote_ip + '<<>>' + str(ss);
			log_array.append(logstring);

		else:
			print"""<div id = 'id_trace_err'>"""
			print "Error Deleting Backup!"
			print "</div>"

			ss = str("Error Deleting Backup!")
                        logstring = str(common_methods.now) + '<<>>From: ' + common_methods.remote_ip + '<<>>' + str(ss);
                        log_array.append(logstring);

		display_take_backup    = 'none'
		display_restore_backup = 'none'
		display_cli_restore    = 'none';
		display_cli_backup     = 'block';

	if(header.form.getvalue("download_backup")):
		get_backup_id = header.form.getvalue("backup_id")
		display_take_backup = 'none'
		display_restore_backup = 'block'

		ss = str("Successfully Downloaded Backup!")
		logstring = str(common_methods.now) + '<<>>From: ' + common_methods.remote_ip + '<<>>' + str(ss);
		log_array.append(logstring);
		
		check_file_existance = os.path.isfile(get_backup_id)
		#print check_file_existance
	        if(check_file_existance == True):
        	        download_file = "yes"
		else:	
			download_file = "no"
			print"""<div id = 'id_trace_err'>"""
			print "Unable to Download. Backup not found!"
			print "</div>"

	if(header.form.getvalue("download_clibackup")):
		get_backup_id = header.form.getvalue("cli_backup_id")
		display_take_backup = 'none';
		display_cli_backup  = 'none'
		display_cli_restore = 'block'

		ss = str("Successfully Downloaded Backup!")
		logstring = str(common_methods.now) + '<<>>From: ' + common_methods.remote_ip + '<<>>' + str(ss);
		log_array.append(logstring);
		
		check_file_existance = os.path.isfile(get_backup_id)
		#print check_file_existance
	        if(check_file_existance == True):
        	        download_file = "yes"
		else:	
			download_file = "no"
			print"""<div id = 'id_trace_err'>"""
			print "Unable to Download. Backup not found!"
			print "</div>"

	if (header.form.getvalue("cli_backup_but")):
		status = savecliconf.take();

		if (status == 'success'):
			print "<script>alert('RAID configuration saved!');</script>";

		else:
			print "<script>alert('Could not save RAID cofiguration!');</script>";

		print "<script>location.href = 'main.py?page=fs2';</script>";

	status=br.get_backup_files_for_web_ui()

	common_methods.append_file(log_file, log_array)

	print common_methods.wait_for_response;
	print """
						<table width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#f9f9f9">
							<tr>
								<td height="450px" valign="top" align="center">

<table width = "1000" border = "0" cellspacing = "0" cellpadding = "0" bgcolor = "#f9f9f9">
        <tr>
                <td valign = "top" align = "right" width = "275px">
                        <table width = "265" border = "0" cellspacing = "0" cellpadding = "0">
                                <tr>
                                        <td height = "33px" width = "8px" align = "left">
                                        <img src = "../images/rightside_left.jpg" />
                                        </td>
                                        <td height = "33px" class = "right_bg rightsidemenuheading" valign = "middle" width = "249">
			
                                                <!--<a class = 'sidenav' href = 'main.py?page=fs2'>FS2 Backup/Restore</a>-->
			<div id="item_2" class="item" style="width:66%;">         
                        """+image_icon+""" FS2 Backup/Restore
                        <div class="tooltip_description" style="display:none" title="FS2 Backup/Restore">
                                <span>This gives information about the resources that are being used by the system.</span><br/><br/>
                                <table border="0">
                                <tr class="spaceUnder">
                                <td valign="top" align="left"><strong style="color:#b2b2b2; padding:0px 2px 0px 2px;">Take Backup:</strong></td>
                                <td>Click on the button to take a Fs2 backup</td>
                                </tr>
                                <tr class="spaceUnder">
                                <td valign="top" align="left"><strong style="color:#cccccc; padding:0px 2px 0px 2px;">Restore backup:</strong></td>
                                <td>Click on the button to restore the Fs2 backup.</td>
                             </tr>
				 <tr class="spaceUnder">
                                <td valign="top" align="left"><strong style="color:#cccccc; padding:0px 2px 0px 2px;">Backup Raid Settings:</strong></td>
                                <td>Click on the button to take raid setting backup.</td>
                             </tr>
				 <tr class="spaceUnder">
                                <td valign="top" align="left"><strong style="color:#cccccc; padding:0px 2px 0px 2px;">Restore Raid settings:</strong></td>
                                <td>Click on the button to take raid setting restore.</td>
                             </tr>


                                </table>
                                </div></div>

                                        </td>
                                        <td height = "33px" width = "8px" align = "right">
                                                <img src = "../images/rightside_right.jpg" />
                                        </td>
                                </tr>
                                <tr>
                                        <td colspan = "3" valign = "top" align = "left">
                                                <table width = "265" border = "0" cellspacing = "0" cellpadding = "0" class="outer_border">
                                                        <tr>
                                                                <td width = "2px" class = "plusmark" align = "right">
                                                                </td>
                                                                <td width = "263px" height = "30px" valign = "middle">
                                                                        <a href = "#" class = "sidenav" onclick = 'return show_table("id_take_backup");'>Take FS2 Backup</a>
                                                                </td>
                                                        </tr>

<tr>
                                                                <td width = "2px" class = "plusmark" align = "right">
                                                                </td>
                                                                <td width = "263px" height = "30px" valign = "middle">
                                                                        <a href = "#" class = "sidenav" onclick = 'return show_table("id_restore_backup");'>Restore FS2 Backup</a>
                                                                </td>
                                                        </tr>"""
	checkareca = commands.getstatusoutput('lspci | grep -i "areca"');

	if (checkareca[0] == 0):
		print """				                                                        <tr>
                                                                <td width = "2px" class = "plusmark" align = "right">
                                                                </td>
                                                                <td width = "263px" height = "30px" valign = "middle">
                                                                        <a href = "#" class = "sidenav" onclick = 'return show_table("id_savecli_conf");'>Backup RAID Settings</a>
                                                                </td>
                                                        </tr>
                                                        <tr>
                                                                <td width = "2px" class = "plusmark" align = "right">
                                                                </td>
                                                                <td width = "263px" height = "30px" valign = "middle">
                                                                        <a href = "#" class = "sidenav" onclick = 'return show_table("id_restore_cliconf");'>Restore RAID Settings</a>
                                                                </td>
                                                        </tr>"""
        print """                                 </table>
                                        </td>
                                </tr>
                        </table>
                </td>
                <td valign = "top" align = "left" width = "30px"></td>
                <td valign = "top" align = "left" width = "695px">
	<form name = 'fs2_backup' action = '' method = 'post'>
        <table width = "550" border = "0" cellspacing = "0" cellpadding = "0" name = 'disp_tables' id = 'id_take_backup' style = 'display: """+display_take_backup+"""'>
                        <tr>
                                <td height = "33px" width = "8" align = "left">
                                        <img src = "../images/rightside_left.jpg" width = "8" height = "33" />
                                </td>
                                <td width = "550" height = "33px" align = "left" valign = "middle" class = "right_bg rightsidemenuheading">
                                <!--<a class = 'link' href = 'fs2_backup_help.php' onclick = "window.open('fs2_backup_help.php', 'help', 'location = no, height = 500, width = 600, scrollbars = 1'); return false;"><?= $image_icon ?></a>-->
				<div id="item_2" class="item" style="width:27%;">         
                        """+image_icon+""" Take FS2 Backup
                        <div class="tooltip_description" style="display:none" title="Take FS2 Backup">
                                <span>This gives information about the resources that are being used by the system.</span><br/><br/>
                                <table border="0">
                                <tr class="spaceUnder">
                                <td valign="top" align="left"><strong style="color:#b2b2b2; padding:0px 2px 0px 2px;">Take Backup:</strong></td>
                                <td>Click on the button to take a Fs2 backup</td>
                                </tr>
                                </table>
                                </div></div>

                                 </td>
                                <td height = "33px" width = "8" align = "right">
                                        <img src = "../images/rightside_right.jpg" />
                                </td>
                        </tr>
	<tr>
                                <td colspan = "3" height="33px" bgcolor="#f5f5f5" align = "center" class="table_content" valign = "top">
                          </td></tr>
                         <tr><td colspan = "3" height="33px" bgcolor="#f5f5f5" align = "right" valign = "top">   
                        <!--<input class = 'input1' type = 'submit' name = 'fs2_backup_but' value = 'Take FS2 Backup' onclick='return submit_fs2backup_form();'>-->
			    <div style="margin-right: 2%;"><span id="button-one"><button type = 'submit' value = 'fs_backup_but' name = 'fs2_backup_but' style = 'background-color:#ffffff; border:none; float: right;' title="Fs2 Backup"><a style="font-size:80%;  width: 100%;">Take FS2 Backup</a></button></span></div>
                                        </td>
                         </tr>
	</table></form>



			<table width = "685" border = "0" cellspacing = "0" cellpadding = "0" name = 'disp_tables' id = 'id_restore_backup' style = 'display: """+display_restore_backup+""";'>
                                        <tr>


        <td height = "33px" width = "8" align = "left">
                                                        <img src = "../images/rightside_left.jpg" width = "8" height = "33" />
                                                </td>
                                                <td width = "669" height = "33px" align = "left" valign = "middle" class = "right_bg rightsidemenuheading">
                                                        <!--<a class = 'link' href = 'sys_information_help3.php' onclick = "window.open('sys_information_help3.php', 'help', 'location = no, height = 500, width = 600'); return false;"></a>-->
			<div id="item_2" class="item" style="width:27%;">         
                        """+image_icon+""" Restore FS2 Backup
                        <div class="tooltip_description" style="display:none" title="Restore FS2 Backup">
                                <span>This gives information about the resources that are being used by the system.</span><br/><br/>
                                <table border="0">
                                <tr class="spaceUnder">
                                <td valign="top" align="left"><strong style="color:#b2b2b2; padding:0px 2px 0px 2px;">Restore Backup:</strong></td>
                                <td>Click on the button to Restore a Fs2 backup</td>
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
                                                        <table width = "685" border = "0" cellspacing = "0" cellpadding = "0" class = "border">
                                                                <tr>
                                                                        <td width = "288" class = "table_heading" height = "35px" valign = "middle">
                                                                                Backup
                                                                        </td>
                                                                        <td width = "172" class = "table_heading" height = "35px" align = "middle">
                                                                                Restore
                                                                        </td>
                                                                        <td width = "1" class = "table_heading" height = "35px" align = "middle">
                                                                                Download
</td>
                                                                                                     

        <td width = "172" class = "table_heading" height = "35px" align = "middle">
                                                                                Delete
                                                                        </td>
                                                               </tr>"""

	fileline = '';
	if status['id'] != 0:
		print """<tr>
		<td colspan = '4' align = 'center' width = "100%" class = "table_content" height = "35px" valign = "middle" bgcolor = "#f5f5f5">
                <font color="RED">Unable to find any webbackup files to restore</font>
                </td>

		</tr>"""
	else:
		#print status['filelist']
   		for file_tuple in status['filelist']:
			#print file_tuple[1]

                        print"""<form enctype="multipart/form-data" name = 'upload_file' action = "" method = "POST">
        		<tr>
			<td width = "55%" class = "table_content" height = "35px" valign = "middle" bgcolor = "#f5f5f5">"""
			fileline = file_tuple[0]
			backupfile = fileline[fileline.rfind('/') + 1:];
			print backupfile;
			print"""</td>

			<input name='backup_id' type='hidden' value='"""+file_tuple[0]+"""' />

                        <td width = "15%" class = "table_content" height = "35px" valign = "middle" bgcolor = "#f5f5f5">
                        <button type="image" value="restore_backup" name="restore_backup" style = "background-color:#ffffff; border:none; margin:0 0 0 12px;" title=" Click to Restore Backup"><img src="images/my_icons/restore3.png" alt="restore" height="30px" width="30px" title="Restore Backup" /></button>
                        </td>
                        <td width = "15%" class = "table_content" height = "35px" valign = "middle" bgcolor = "#f5f5f5">
                               <button type="image" value="download_backup" name="download_backup" style = "background-color:#ffffff; border:none; margin:0 0 0 12px;" title=" Click to Download Backup"><img src="images/my_icons/download.png" align="center" alt="restore" height="30px" width="30px" title="Download Backup" /></button>
                        </td>
                        <td width = "15%" class = "table_content" height = "35px" valign = "middle" bgcolor = "#f5f5f5">
                               <button type="image" value="detele_backup" name="delete_backup" style = "background-color:#ffffff; border:none; margin:0 0 0 12px;" title=" Click to Delete Backup" onclick="return confirm('Are you sure you want to Delete this Backup?');"><img src="images/my_icons/delete.png" align="center" alt="restore" height="30px" width="30px" title="Delete Backup" /></button>
                        </td>
                        </tr>
			</form>"""

        print """</table><br /><br /><br />
        </td>
        </tr>
        </table>
	<form name = 'take_clibackup' action = '' method = 'post'>
        <table width = "550" border = "0" cellspacing = "0" cellpadding = "0" name = 'disp_tables' id = 'id_savecli_conf' style = 'display: """+display_cli_backup+""";'>
                        <tr>
                                <td height = "33px" width = "8" align = "left">
                                        <img src = "../images/rightside_left.jpg" width = "8" height = "33" />
                                </td>
                                <td width = "550" height = "33px" align = "left" valign = "middle" class = "right_bg rightsidemenuheading">
                                <!--<a class = 'link' href = 'fs2_backup_help.php' onclick = "window.open('fs2_backup_help.php', 'help', 'location = no, height = 500, width = 600, scrollbars = 1'); return false;"><?= $image_icon ?></a>-->
			<div id="item_2" class="item" style="width:30%;">         
                        """+image_icon+""" Backup RAID Settings
                        <div class="tooltip_description" style="display:none" title="RAID Settings backup">
                                <span>This gives information about the resources that are being used by the system.</span><br/><br/>
                                <table border="0">
                                <tr class="spaceUnder">
                                <td valign="top" align="left"><strong style="color:#b2b2b2; padding:0px 2px 0px 2px;">Raid setting backup:</strong></td>
                                <td>Click on the button to take backup for raid setting</td>
                                </tr>
                                </table>
                                </div></div>
                                 </td>
                                <td height = "33px" width = "8" align = "right">
                                        <img src = "../images/rightside_right.jpg" />
                                </td>
                        </tr>
	<tr>
                                <td colspan = "3" height="33px" bgcolor="#f5f5f5" align = "center" class="table_content" valign = "top">
                          </td></tr>
                         <tr><td colspan = "3" height="33px" bgcolor="#f5f5f5" align = "right" valign = "top">   
                        <!--<input class = 'input1' type = 'submit' name = 'fs2_backup_but' value = 'Take FS2 Backup' onclick='return submit_fs2backup_form();'>-->
			    <div style="margin-right: 2%;"><span id="button-one"><button type = 'image' name = 'cli_backup_but' value = 'Take CLI Backup'  style = 'background-color:#ffffff; border:none; float: right;' title="CLI Backup"><a style="font-size:80%;  width: 100%;">Take RAID Settings Backup</a></button></span></div>
                                        </td>
                         </tr>
	</table></form>
	<form name = 'upload_cliconf' enctype="multipart/form-data" action = '' method = 'post'>
        <table width = "550" border = "0" cellspacing = "0" cellpadding = "0" name = 'disp_tables' id = 'id_restore_cliconf' style = 'display: """+display_cli_restore+"""'>
                        <tr>
                                <td height = "33px" width = "8" align = "left">
                                        <img src = "../images/rightside_left.jpg" width = "8" height = "33" />
                                </td>
                                <td width = "550" height = "33px" align = "left" valign = "middle" class = "right_bg rightsidemenuheading">
                                <!--<a class = 'link' href = 'fs2_backup_help.php' onclick = "window.open('fs2_backup_help.php', 'help', 'location = no, height = 500, width = 600, scrollbars = 1'); return false;"><?= $image_icon ?></a>-->
			<div id="item_2" class="item" style="width:24%;">         
                        """+image_icon+""" Restore RAID Settings
                        <div class="tooltip_description" style="display:none" title="Restore RAID Settings">
                                <span>This gives information about the resources that are being used by the system.</span><br/><br/>
                                <table border="0">
                                <tr class="spaceUnder">
                                <td valign="top" align="left"><strong style="color:#b2b2b2; padding:0px 2px 0px 2px;">Restore Raid setting:</strong></td>
                                <td>Click on the button to restore for raid setting backup</td>
                                </tr>
                                </table>
                                </div></div>
                                 </td>
                                <td height = "33px" width = "8" align = "right">
                                        <img src = "../images/rightside_right.jpg" />
                                </td>
                        </tr>
	<tr>
                                <td colspan = "3" height="33px" bgcolor="#f5f5f5" align = "center" class="table_content" valign = "top">
 <table width = "685" border = "0" cellspacing = "0" cellpadding = "0" class = "border">
                                                                <tr>
                                                                        <td width = "288" class = "table_heading" height = "35px" valign = "middle">
                                                                                Backup
                                                                        </td>
                                                                        <td width = "172" class = "table_heading" height = "35px" align = "middle">
                                                                                Restore
                                                                        </td>
                                                                        <td width = "1" class = "table_heading" height = "35px" align = "middle">
                                                                                Download
</td>
                                                                                                     

        <td width = "172" class = "table_heading" height = "35px" align = "middle">
                                                                                Delete
                                                                        </td>
                                                               </tr>"""

	getclibackup = commands.getstatusoutput('ls /var/www/fs2/downloads/RAIDSETTINGS.tar.bz2');

	if (getclibackup[0] == 0):
		print"""<form enctype="multipart/form-data" name = 'upload_cli_file' action = "" method = "POST">
		<tr>
		<td width = "55%" class = "table_content" height = "35px" valign = "middle" bgcolor = "#f5f5f5">"""
		showfileline = getclibackup[1];

		dispfile = showfileline[showfileline.rfind('/') + 1:];

		print dispfile;
		print"""</td>

		<input name='cli_backup_id' type='hidden' value='"""+getclibackup[1]+"""' />

		<td width = "15%" class = "table_content" height = "35px" valign = "middle" bgcolor = "#f5f5f5">
		<button type="image" value="restore_clibackup" name="restore_clibackup" style = "background-color:#ffffff; border:none; margin:0 0 0 12px;" title=" Click to Restore Backup"><img src="images/my_icons/restore3.png" alt="restore" height="30px" width="30px" title="Restore Backup" /></button>
		</td>
		<td width = "15%" class = "table_content" height = "35px" valign = "middle" bgcolor = "#f5f5f5">
		       <button type="image" value="download_clibackup" name="download_clibackup" style = "background-color:#ffffff; border:none; margin:0 0 0 12px;" title=" Click to Download CLI Backup"><img src="images/my_icons/download.png" align="center" alt="restore" height="30px" width="30px" title="Download Backup" /></button>
		</td>
		<td width = "15%" class = "table_content" height = "35px" valign = "middle" bgcolor = "#f5f5f5">
		       <button type="image" value="detele_clibackup" name="delete_clibackup" style = "background-color:#ffffff; border:none; margin:0 0 0 12px;" title=" Click to Delete Backup" onclick="return confirm('Are you sure you want to Delete this Backup?');"><img src="images/my_icons/delete.png" align="center" alt="restore" height="30px" width="30px" title="Delete Backup" /></button>
		</td>
		</tr>
		</form>"""

	else:
		print """<tr>
		<td colspan = '4' align = 'center' width = "100%" class = "table_content" height = "35px" valign = "middle" bgcolor = "#f5f5f5">
                <font color="RED">Unable to find RAID configuration files to restore</font>
                </td>

		</tr>"""

        print """</table><br /><br /><br />

                          </td></tr>
                         <tr><td colspan = "3" height="33px" bgcolor="#f5f5f5" align = "right" valign = "top">   
                        <!--<input class = 'input1' type = 'submit' name = 'fs2_backup_but' value = 'Take FS2 Backup' onclick='return submit_fs2backup_form();'>-->
                                        </td>
                         </tr>
	</table></form>



        </td>
        </tr>
        </table>
        

                        </td>
                        </tr>
                        </table>

 

	"""
	import footer

	#if(header.form.getvalue("bckup")):
	#	print "<script>location.href = 'Backupfs2.tar.gz'</script>"


	if(header.form.getvalue("download_backup")):
		get_backup_id = header.form.getvalue("backup_id")
		split_gbi = string.split(get_backup_id, "/")
                filename = split_gbi[6]
		url = get_backup_id

		if(download_file == "yes"):
			print "<script>location.href='../downloads/settings/"+filename+"'</script>"

	if(header.form.getvalue("download_clibackup")):
		get_backup_id = header.form.getvalue("cli_backup_id")
		split_gbi = string.split(get_backup_id, "/")
                filename = split_gbi[5]
		url = get_backup_id

		if(download_file == "yes"):
			print "<script>location.href='../downloads/"+filename+"'</script>"


except Exception as e:
        fh = open('/var/www/fs2/py/temp', 'w');
        traceback.print_exc(file = fh);
        fh.write("<BR>");
        fh.write('<BR><input type = "button" value = "Back" onclick = "location.href = \'/fs2/py/backup.py\'">');
        print "<script>location.href = './error.py';</script>";


