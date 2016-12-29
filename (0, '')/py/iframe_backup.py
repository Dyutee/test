#!/usr/bin/python
#_*_ coding: UTF-8 _*_

#enable debugging
import traceback
try:
	import cgitb, os, sys, commands, common_methods, traceback, string, backup_include_files, cgi
	cgitb.enable()
	form = cgi.FieldStorage()
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
	#------------------Opslag Fs2 backup create----------------
	if(form.getvalue("fs2_backup_but")):
		create_backup = br.backup(for_web="yes") 
		if (create_backup["id"]==0):
			print"""<div id = 'id_trace'>"""
			print create_backup["desc"]
			print "</div>"
			logstatus = common_methods.sendtologs('Success', 'Backup Succefully Created', 'UI','backup.py'+ str(create_backup));
		else:
			print"""<div id = 'id_trace_err'>"""
			print create_backup["desc"]
			print "</div>"
			logstatus = common_methods.sendtologs('Error', 'Error Occured while Creating backup', 'UI','backup.py'+ str(create_backup));
	#-----------------------------End---------------------------
		
		#createcli_backup = br.backup() 
		
		#if (createcli_backup['id'] > 0):
		#	print createcli_backup['desc'];

	
		display_take_backup = 'none'
		display_restore_backup = 'block'

	if(form.getvalue("restore_backup")):
		get_backup_id = form.getvalue("backup_id")
		split_gbi = string.split(get_backup_id, "/")
		filename = split_gbi[6]

		#copy_to_tmp = commands.getstatusoutput('sudo cp "'+get_backup_id+'" /tmp/')
		#if(copy_to_tmp[0]==0):
		restore_backup = br.restore("yes",filename)
		if(restore_backup["id"]==0):	
			print"""<div id = 'id_trace'>"""
			print restore_backup["desc"]
			print "</div>"
		else:
			print"""<div id = 'id_trace_err'>"""
			print restore_backup["desc"]
			print "</div>"

			
		#else:
		#	print"""<div id = 'id_trace_err'>"""
		#	print "Error Copying to tmp!"
		#	print "</div>"


		display_take_backup = 'none'
		display_restore_backup = 'block'

	if(form.getvalue("restore_clibackup")):
		get_backup_id = form.getvalue("cli_backup_id")
		split_gbi = string.split(get_backup_id, "/")
		filename = split_gbi[6]

		copy_to_tmp = commands.getstatusoutput('sudo cp "'+get_backup_id+'" /tmp/')
		#if(copy_to_tmp[0]==0):
		restore_cli_backup = br.restore("yes", filename)
		if(restore_cli_backup["id"] == 0):	
			print"""<div id = 'id_trace'>"""
			print restore_cli_backup["desc"]
			print "</div>"
			ss = 'Restore Successful'

		else:
			print"""<div id = 'id_trace_err'>"""
			print "Restore failed!"
			print "</div>"
			ss = 'Restore Failed'

			
		#else:
		#	print"""<div id = 'id_trace_err'>"""
		#	print "Error Copying to tmp!"
		#	print "</div>"


		display_take_backup    = 'none'
		display_cli_backup     = 'none';
		display_restore_backup = 'none';
		display_cli_restore    = 'block';

	if(form.getvalue("delete_backup")):
		get_backup_id = form.getvalue("backup_id")
		delete_backup = commands.getstatusoutput("sudo rm -rf "+get_backup_id)
		if(delete_backup[0]==0):
			print"""<div id = 'id_trace'>"""
			print "Backup Deleted Successfully."
			print "</div>"


		else:
			print"""<div id = 'id_trace_err'>"""
			print "Error Deleting Backup!"
			print "</div>"

		display_take_backup = 'none'
		display_restore_backup = 'block'

	if(form.getvalue("delete_clibackup")):
		get_backup_id = form.getvalue("cli_backup_id")
		delete_backup = commands.getstatusoutput("sudo rm -rf "+str(get_backup_id))
		if(delete_backup[0]==0):
			print"""<div id = 'id_trace'>"""
			print "Backup Deleted Successfully."
			print "</div>"


		else:
			print"""<div id = 'id_trace_err'>"""
			print "Error Deleting Backup!"
			print "</div>"


		display_take_backup    = 'none'
		display_restore_backup = 'none'
		display_cli_restore    = 'none';
		display_cli_backup     = 'block';

	if(form.getvalue("download_backup")):
		get_backup_id = form.getvalue("backup_id")
		display_take_backup = 'none'
		display_restore_backup = 'block'

		
		check_file_existance = os.path.isfile(get_backup_id)
		#print check_file_existance
	        if(check_file_existance == True):
        	        download_file = "yes"
		else:	
			download_file = "no"
			print"""<div id = 'id_trace_err'>"""
			print "Unable to Download. Backup not found!"
			print "</div>"

	if(form.getvalue("download_clibackup")):
		get_backup_id = form.getvalue("cli_backup_id")
		display_take_backup = 'none';
		display_cli_backup  = 'none'
		display_cli_restore = 'block'

		
		check_file_existance = os.path.isfile(get_backup_id)
		#print check_file_existance
	        if(check_file_existance == True):
        	        download_file = "yes"
		else:	
			download_file = "no"
			print"""<div id = 'id_trace_err'>"""
			print "Unable to Download. Backup not found!"
			print "</div>"

	if (form.getvalue("cli_backup_but")):
		status = savecliconf.take();

		if (status == 'success'):
			print "<script>alert('RAID configuration saved!');</script>";

		else:
			print "<script>alert('Could not save RAID cofiguration!');</script>";

		print "<script>location.href = 'iframe_backup.py';</script>";

	
	common_methods.append_file(log_file, log_array)

	get_backup_files = br.get_backup_files_for_web_ui()
	#print get_backup_files
	fileline = ''

	sys.path.append("/var/nasexe/python/")
	import tools
	from tools import db

	check_ha = tools.check_ha()

	sys_node_name = tools.get_ha_nodename()
	if(sys_node_name == "node1"):
		other_node = "node2"
		show_tn = "Node1"
		show_on = "Node2"
	else:
		other_node = "node1"
		show_tn = "Node2"
		show_on = "Node1"

	query="select * from network_ifaces where (name='eth1' and node='"+other_node+"')"
	status=db.sql_execute(query)
	for x in status["output"]:
		other_node_ip = x["ip"]

	#print common_methods.wait_for_response;
	print """
	<script>
	function processForm()
	{
		$("#bkp_form").submit(function(e) {
    		e.preventDefault();
		});
	}


		
	</script>
		<div id="loader-div" style="text-align:center; display:none;" ><img style="margin-top:20%;" src="../images/ajax-loader.gif" /><br/> Loading...</div>
		 <!--Right side body content starts from here-->
              <div class="rightsidecontainer" id="body-div">
                <!--tab srt-->
                <div class="searchresult-container">
		<div style="margin:0 0 0px 0;" class="topinputwrap-heading"><a class="demo" href ="#"><img src ="../images/help_icon1.png" style = "width:13px;"><span class="tooltip" >
                 <table border="0">
        <tr>     
        <td class="text_css">This page allows you to backup FS2's configuration and maintain multiple copies of those backups.</td>
        </tr>
        </table>"""
	if(check_ha == True):
		print"""
			</span></a> Backup ("""+show_tn+""")
                <span style="float:right; margin:0;"><a onclick="return onclick_loader();" class="resource_links" href="https://"""+other_node_ip+"""/fs4/py/iframe_backup.py">"""+show_on+"""</a></span>
                </div>"""
	else:
		print"""</span></a><p class = "gap_text">Backup</p> </div>"""
	print"""
                  <div class="infoheader">
                    <div id="tabs">
                      <ul>
                        <li><a href="#tabs-1">Backup Information</a></li>
                        <li><a href="#tabs-2">Take FluidOS Backup</a></li>
                      </ul>
                      
	<div id="tabs-1">
	<!--form container starts here-->
	<div class="form-container">
	<div class="inputwrap">
	<div class="formleftside-content">

	<table width="600px">
	<tr>
	<th style="border:#D1D1D1 1px solid; padding:5px;">Backup</th>
	<th style="border:#D1D1D1 1px solid; padding:5px;">Restore</th>
	<th style="border:#D1D1D1 1px solid; padding:5px;">Download</th>
	<th style="border:#D1D1D1 1px solid; padding:5px;">Delete</th>
	</tr>"""

	if get_backup_files['id'] == 0:
		for file_tuple in get_backup_files['filelist']:
			fileline = file_tuple[0]
                        backupfile = fileline[fileline.rfind('/') + 1:]
			print """
			<form name="backup" method="post" action="" id = 'bkp_form'>	
			<tr>
			<td align = "center" style="border:#D1D1D1 1px solid;">"""+backupfile+"""</td>
			<input name='cli_backup_id' type='hidden' value='"""+file_tuple[0]+"""' />
			<td align = "center" style="border:#D1D1D1 1px solid;">
			<button type="image" value="restore_clibackup" name="restore_clibackup" style = "background-color:#ffffff; border:none; margin:0 0 0 12px; cursor:pointer;" title=" Click to Restore Backup"><img src="images/my_icons/restore3.png" alt="restore" title="Restore Backup" /></button>
			</td>
			<td align = "center" style="border:#D1D1D1 1px solid;">
			<button type="image" value="download_clibackup" name="download_clibackup" style = "background-color:#ffffff; border:none; margin:0 0 0 12px; cursor:pointer;" title=" Click to Download CLI Backup"><img src="images/my_icons/download.png" align="center" alt="download" title="Download Backup"  onclick="return processForm()";/></button>
			</td>
			<td align = "center" style="border:#D1D1D1 1px solid;">
			<button type="image" value="detele_clibackup" name="delete_clibackup" style = "background-color:#ffffff; border:none; margin:0 0 0 12px; cursor:pointer;" title=" Click to Delete Backup" onclick="return confirm('Are you sure you want to Delete this Backup?');"><img src="images/my_icons/delete.png" align="center" alt="delete" title="Delete Backup" /></button>
			</td>
			</tr>
			</form>"""
	else:
		
        	print """<tr><td colspan = "4" style="text-align:center; width:600px;border:#D1D1D1 1px solid;"><span>No Information is Available</span>!</td></tr>"""
	print"""
			"""

	print """</table>

	</div>
        </div>
        </div>
	<!--form container ends here-->
        <p>&nbsp;</p>
        </div>
	<div id="tabs-2">
	<!--form container starts here-->
	<div class="form-container">
	<div class="inputwrap">
	<div class="formleftside-content">
	<form name="fs2_backup_form" method="post" action="">
	<button class="buttonClass" type = 'submit' name = 'fs2_backup_but' value = 'fs2_backup_but' style="width:150px; margin:0 0 10px 250px;" >Take Backup</button>
	</form>
	</div>
        </div>
        </div>
	<!--form container ends here-->
        <p>&nbsp;</p>
        </div>


	

	</div>
                  </div>
                </div>
		</div>

	"""
	#import footer

	#if(header.form.getvalue("bckup")):
	#	print "<script>location.href = 'Backupfs2.tar.gz'</script>"


	if(form.getvalue("download_backup")):
		get_backup_id = form.getvalue("backup_id")
		split_gbi = string.split(get_backup_id, "/")
                filename = split_gbi[6]
		url = get_backup_id

		if(download_file == "yes"):
			print "<script>location.href='../downloads/settings/"+filename+"'</script>"

	if(form.getvalue("download_clibackup")):
		get_backup_id = form.getvalue("cli_backup_id")
		split_gbi = string.split(get_backup_id, "/")
                filename = split_gbi[6]
		url = get_backup_id

		if(download_file == "yes"):
			print "<script>location.href='../../fs2/downloads/settings/"+filename+"'</script>"
			

except Exception as e:
        fh = open('/var/www/fs4/py/temp', 'w');
        traceback.print_exc(file = fh);
        fh.write("<BR>");
        fh.write('<BR><input type = "button" value = "Back" onclick = "location.href = \'/fs4/py/iframe_backup.py\'">');
        print "<script>location.href = './error.py';</script>";


