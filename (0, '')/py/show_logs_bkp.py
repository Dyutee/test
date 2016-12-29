#!/usr/bin/python

import cgitb, sys, common_methods, os, commands, string, include_files
cgitb.enable()
sys.path.append('../modules/');
import disp_except;

try:
	sys.path.append('/var/nasexe/python/');
	import tools
	from tools import acl
	from tools import share_permissions
	from tools import log_backup_schedule
	from tools import smb_logpath
	import schedulelogs;
	import schedulelogs as slogs

	def write_file(file_to_write, params_array, append):
		if (file_to_write != ''):
			chown_file = commands.getoutput('sudo chown www-data:www-data ' + file_to_write);


			status, output=commands.getstatusoutput("/usr/bin/sudo /usr/bin/touch "+file_to_write)
			commands.getoutput('sudo chmod 777 ' + file_to_write);

			if(append=="yes"):
				file_handle = open(file_to_write, 'a');
				for i in params_array:
					status = file_handle.write(i);

			else:
				file_handle = open(file_to_write, 'w');
				for i in params_array:
					status = file_handle.write(i + "\n");

			commands.getoutput('sudo chmod 755 ' + file_to_write);
			file_handle.close()

	


	get_logs_file1 = ''
	querystring = os.environ['QUERY_STRING'];

	response = '';

	if (querystring.find('&act=') > 0):
		response = querystring[querystring.find('&act=') + len('&act='):];

	sun_checked = '';
	mon_checked = '';
	tue_checked = '';
	wed_checked = '';
	thu_checked = '';
	fri_checked = '';
	sat_checked = '';

	sys.path.append('/var/nasexe/python/')
	import logrotate

	log_array = [];
	log_file = common_methods.log_file;
	logstring = '';


	querystring    = os.environ['QUERY_STRING'];

	old_val = '';

	checkdownloads = commands.getstatusoutput('sudo ls /var/www/fs4/downloads');

	frompage       = '';
	checkforfile   = [];
	filetodownload = '';

	if (querystring.find('frompage=') > 0):
		frompage = common_methods.substr(querystring, 'frompage=', '', '&');

	if (frompage == 'getlogs'):
		logfileline = commands.getoutput('ls /var/www/fs4/downloads/fs2_logs*');
		logfileline = logfileline.strip();

		filetodownload = logfileline[logfileline.rfind('/') + 1:];

	if (frompage == 'sysinfo'):
		checkforfile = commands.getstatusoutput('sudo ls /var/www/fs4/downloads/sysinfo*');

		if (checkforfile[0] == 0):
			checkfile = str(checkforfile[1]).strip();
			filetodownload = checkfile[checkfile.rfind('/') + 1:];


	#######################################

	#LOG ROTATE CODE START HERE#

	#######################################

	avail_user = ''

	#------------------Log Rotate End----------------------------------------
	if (response == 'sched_logs_done'):
		display_auto_logs = 'table';
		display_get_logs  = 'none';

		
	
	show_status=log_backup_schedule.show()
	#print show_status
	#print '<br/>'
	#print show_status["date_freq"]
		#print status

	#-----------------------------End---------------------------------
	#------------------SMB Log Path Code-----------------------------------

	sys.path.append('/var/nasexe/python/');
	import smb

	 #----------------Restart Samba----------------#
		#restart_samba  = commands.getstatusoutput('sudo /etc/init.d/samba restart')
		#restart_syslog = commands.getstatusoutput('sudo /etc/init.d/rsyslog restart');

		#if (restart_syslog[0] > 0):
		#	print 'Failed to start rsyslog!<BR />';

		#if(restart_samba[0] != 0):
		#	print "Failed to restart Samba!"

		#d.msgbox("Log Path Set Successfully!")
		#maintenance_option.config()




	#get_shares = common_methods.get_shares_array()
	#print get_shares
	#print '<br/>'
	get_shares1 = tools.get_all_shares(debug=True)
	#shr = get_shares1['name']
	share_infos = get_shares1["shares"]
	
	#share_names = ''

	#for i in get_shares:
	#	split_line = string.split(i, ":")
	#	share_names += split_line[0]+" "

	#print share_names
	#split_line = string.split(share_names)
	#print split_line


	messageID = 0
	message = ''

	smb_log_file = '/var/nasconf/smb-log.conf'
	read_smb_log_file = common_methods.read_file(smb_log_file)
	active_smb_log_share = ''
	length_of_list = ''
	if(len(read_smb_log_file) == 1):
		#print read_smb_log_file
		for z in read_smb_log_file:
			find_slash = z.find("/")
			if(find_slash != -1):
				split_log_line = string.split(z, "/")
				length_of_list = len(split_log_line)
				#print length_of_list
				#print "<br/>"
				active_smb_log_share = split_log_line[length_of_list - 1].strip()


				#if(len(split_log_line) == 4):
					#active_smb_log_share = split_log_line[3].strip()
					#print active_smb_log_share
				#else:
					#messageID = 1
					#message =  "Something is Wrong with SMB File! Share path is missing."
					#print message
	else:
		messageID = 1
		message = "Something is wrong with smb File! There cannot be more than one Entry."

	retrieve_log_path = ''
	log_path_status = smb_logpath.is_set()
	if(log_path_status == True):
		get_log_path_cmd = smb_logpath.get()
		retrieve_log_path = get_log_path_cmd["share_path"]


	print
	print """

		<script type="text/javascript">
        $(document).ready(function() {
        $(".various").fancybox({
                maxWidth        : 1000,
                maxHeight       : 600,
                fitToView       : false,
                width           : '100%',
                height          : '90%',
                autoSize        : false,
                closeClick      : false,
                openEffect      : 'none',
                closeEffect     : 'none',
                /*'afterClose':function () {
                 window.location.reload();
                 },*/
                helpers   : { 
                overlay  :       {closeClick: false} // prevents closing when clicking OUTSIDE fancybox 
                             }
                
       });

        });
        </script>



	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer">
		<div class="insidepage-heading">Maintenance >> <span class="content">Logs Information</span></div>
		<!--tab srt-->"""
	print common_methods.wait_for_response;
	print"""<div class="searchresult-container">
		  <div class="infoheader">
		    <div id="tabs">
		      <ul>
			<li><a href="#tabs-1">Get Logs</a></li>
			<li><a href="#tabs-2">Auto Schedule Logs</a></li>
			<li><a href="#tabs-3">Log Rotate</a></li>
			<li><a href="#tabs-4">SMB Log Path</a></li>
		      </ul>
		      <div id="tabs-1">

		<!--form container starts here-->
		<div class="form-container">
		  <div class="inputwrap">
		    <div class="formrightside-content">"""

	print"""<form name = 'show_logs' method = 'post'>
		     <table width = "685" border = "0" cellspacing = "0" cellpadding = "0" class="outer_border"  bgcolor = "#f5f5f5" style="padding-left: 9%; margin:10px 0 0 0; text-align:center;">
									 <tr>
				<td> 
	 <div style="margin-left: -5%;">

	<a class='various logs_page_class' data-fancybox-type='iframe' href='view_logs_pag.py'>View Logs</a>

	<a class='logs_page_class' href='#' onclick="return fetch_logs();">System Logs</a>

	<a class='logs_page_class' href='main.py?page=logs&act=clear_logs' >Clear Logs</a>

	<!--<button type="submit" class='logs_page_class' name="clear_logs" value="clear_logs">Clear Logs</button>-->


	</div>
	</td>
	</tr>
	<tr><td  align = 'left' style = 'font:12px Arial; font-style: italic; color: darkred;'>"""
	if (checkdownloads[0] == 0 and checkdownloads[1] != ''):

		print """
			 <BR><BR><!--Files can be downloaded from 'Help -> Support' menu-->"""

	print """                                       </td>
					       </tr>


	</table>
	</form>	


		   </div>"""


	print"""
		  </div>
		</div>
		<!--form container ends here-->
		<p>&nbsp;</p>
		      </div>
		      <div id="tabs-2">
		<!--form container starts here-->
		<div class="form-container">
		  <div class="topinputwrap-heading">Auto Log Information</div>
		  <div class="inputwrap">
		<div class="formrightside-content">"""



	frequency = '';

	freq_array = [];

	freq_array.append(5);
	freq_array.append(10);
	freq_array.append(15);
	freq_array.append(30);

	backups = 1;
	backupval = '';

	schedlogstatus = log_backup_schedule.show();

	if (schedlogstatus['id'] == 0):
		frequency = schedlogstatus['date_freq'];
		backups   = schedlogstatus['no_of_files'];
		backupval = backups;


	print"""	  

	<form name = 'autoschedulelogs' method = 'POST'>

	<table width = "685" border = "0" cellspacing = "0" cellpadding = "0" class="outer_border"  bgcolor = "#f5f5f5">

	<!--<tr>
							<td class = 'table_heading' colspan = '2'>
								<font color = 'darkred'>** Older Backups will be deleted. If the total backups size Exceeds 500Mb</font><BR>
							</td>
						</tr>-->


	<tr>
							 <td class = "table_heading">
								<BR>Frequency of backups:<BR><BR>
								<div class="styled-select2" style="width:85px;">
								<select class = 'textbox' name = 'freq' style = 'width:100px;'>
									<option value = 'sel_day'>select</option>"""
	for i in freq_array:
		if (str(i) == str(frequency)):
			print "<option value = '""" + str(i) + """' selected>""" + str(i) + """</option>"""
		
		else:
			print "<option value = '""" + str(i) + """'>""" + str(i) + """</option>"""

	print """                                               </select></div><p style="margin-top: -8%; margin-left: 36%;">Days(s)</p>
		
					</td>

	<td class = 'table_heading'>
							<!--<BR>No. of copies to keep:<BR><BR>-->
							<BR>Number of Files:<BR><BR>
							<input class = 'textbox' type = 'text' name = 'noofcops' value = '""" + str(backups) + """' style = 'width: 5%;' readonly />
							<input type = 'image' src = '../images/plus1.jpg' style = 'width: 20px; height: 20px;' onclick = 'if (document.autoschedulelogs.noofcops.value < 10){document.autoschedulelogs.noofcops.value++;} return false;' />
							<input type = 'image' src = '../images/minus2.jpg' iname = 'reduce' style = 'width: 20px; height: 20px;' onclick = 'if (document.autoschedulelogs.noofcops.value > 1){document.autoschedulelogs.noofcops.value--;} return false;' />
						</td>
					</tr>




	</table>
	<div>
	<!--<button class = 'button_example' type="button" name = 'del_sched_log' value = 'Remove Scheduled log' onclick = 'return remove_schedule_log(\"""" + backupval + """");' style="float: right; margin-right: -46%;">Remove Logs</button>-->
	<!--<button class = 'button_example' type="button" name = 'sched_log' value = 'Scheduled log' onclick = 'return do_schedule_log(\"""" + str(backupval) + """", document.autoschedulelogs.freq.value, document.autoschedulelogs.noofcops.value);' style="float: right; margin-right: -20%;">Schedule Logs</button>-->

<button class = 'buttonClass' type="submit" name = 'del_sched_log' value = 'Remove Scheduled log' onclick = 'return validate_schedule_log();'style="float: right; margin-right: -46%;width:120px;">Remove</button>
<button class = 'buttonClass' type="submit" name = 'sched_log' value = 'Scheduled log' onclick = 'return validate_schedule_log();' style="float: right; margin-right: -20%;width:120px;">Schedule Log</button></div>


	</form>"""
	print"""
	</div>
	</div>
	</div>
	<!--form container ends here-->
	<p>&nbsp;</p>
	      </div>

	<div id="tabs-3">
			<!--form container starts here-->
			<div class="form-container">
			  <div class="topinputwrap-heading">Log Rotation</div>
			  <div class="inputwrap">
			<div class="formrightside-content">

			<form name = 'rotate_log' method = 'POST' action = ''>

			<table name = 'disp_tables' width = "100%" border = "0" cellspacing = "0" cellpadding = "0" id = 'id_rotate_log'>

			<tr>
	<td  class = 'table_heading' width = '25%'><input type="checkbox"  name="chck" id="chk" onclick = 'return create_text();'><span style="position:absolute;overflow:hidden;color:#666666;"><b>Create New Configuration</b>:</span></td><!--<td class = 'table_heading' width = '25%'   style="text-indent: -73%;">Create Configuration:</td>-->

	<td class = 'table_heading' width = '25%'  style=" text-align:center;  padding-left:14%;"><b>Frequency</b>:</td>
	<td class = 'table_heading' width = '25%' ><span style="text-align: right;margin-left:67%;color:#666666;" id = "conf_name_hide" ><b>ConfigurationFile</b>:</span></td>
	</tr>
	<tr>
	<td colspan="0" style=" padding-right: 13%;">
	<div style="position:absolute; display: none;  padding-top: 1%;color:#666666;" id ="txt"><b>Create</b>:</div><br/><br/><input type="text" class = "textbox" name="create_val" id ="inpt" size="10" onclick="enable()" style = 'display: none;'/>
	<div style="position:absolute; padding-top: 1%; display: none;" id ="txt1"><b>Configuration Path</b>:</div><br/><br/><input type="text" class = "textbox"  name="create_path" id ="inpt1" size="10" onclick="enable()"  style = 'display: none;'/>
	<br/>
	<div>
	<button class = 'buttonClass' type="submit" name = 'create_value' value = 'Create' onclick = 'return validate_create_rotate_configuration();' style = 'float: left;display: none;' title="Rotate Logs">Create</button>
	</div>
	</td>
	<td style="padding-bottom: 26%; padding-left:8%; align:center;">
	
	<div class="styled-select2" style="width:138px;">
	<select name ='set_freq' value = '' style="text-align: center;width:152px;">
		<option value = '' >Frequency</option>
		<option"""


	if (fetch_freq == "daily"):
		print "selected = selected"

	print """>daily</option>
		<option"""

	if (fetch_freq == "weekly"):
		print "selected = selected"

	print """>weekly</option>
		<option"""

	if (fetch_freq == "monthly"):
		print "selected = selected"

	print """>monthly</option>
		<option"""

	if (fetch_freq == "yearly"):
		print "selected = selected"

	print """>yearly</option>


	</select></div>
	</td>
	<td colspan="0" style="width: 33%; float:right;margin-right:14%;" id= "conf_dis" class = 'table_heading'>
	<br/>
	<select onclick="return move_users(this.form.available, this.form.granted, '1');" multiple="" name="avail_users" value = "avail_select"id="available" onclick='#'style="width: 200px; height: 150px;" class="input" >"""
	for x in logs["conf_files"]:
		print"""<option value='"""+x+"""'"""

		#if(get_logs_file1 !=''):
		#	if(get_logs_file1 == x):
		if(avail_user == x):
			print """selected = 'selected'""" 
		print""">"""+x+"""</option>"""
	print"""</select><BR>
	<input id = 'conf_file_dis'type ="checkbox" onclick="rotate_log_disable()" value="allfiles" name="check" >All
	<!--<input id = 'conf_file_dis'type ="checkbox"onclick="rotate_log_disable()"value="allfiles" name="check" ><td class = 'table_heading' style="padding-top: 24%; text-align: right; padding-left: 3%;" id ="hid_allfile" >AllFiles</td>-->
	</td>
	</tr>                             
	</div>

	<tr>
						<div>
						<td height = '35px'>"""

	print """Log rotate frequency:<input lass = 'input' class = 'textbox' readonly name = 'freq_rotate' style="margin-left:145px; width:35px;margin-top: -13%;" value ="""+fetch_rotate_name+""">

						</td>
						<td>
							<div style="margin-left:14%;">
								<input type = "button" name = 'increase' value = "&#9650;"  onclick = "this.form.freq_rotate.value++; if (parseInt(this.form.freq_rotate.value) >= 1){this.form.reduce.disabled=false;} if (this.form.freq_rotate.value == 4){this.form.increase.disabled=true;}" style = "font-size:8px; margin:0; padding:0; width:28px;  height:21px;" >
								<input type = "button" value = "&#9660;" name = 'reduce' onclick = "this.form.freq_rotate.value--; if (this.form.freq_rotate.value <= 1){this.form.reduce.disabled=true;} if (this.form.freq_rotate.value < 7){this.form.increase.disabled=false;}" style = "font-size:8px; margin:0; padding:0; width:28px; height:21px;" disabled>
							</div>

	</td>

						<td>
							<p style="margin-left:-12%;color:#666666;">Log size(MB):</p><input lass = 'input' class = 'textbox' readonly name = 'size' style="width:35px;margin-left:35%;margin-top:-10.5%;" value ="""+str(fetch_size)+""">
						</td>
						<td>
							<div style="margin-left:-61px;">
								<input type = "button" name = 'increase1' value = "&#9650;" onclick = "this.form.size.value++; if (parseInt(this.form.size.value) >= 1){this.form.reduce1.disabled=false;} if (this.form.size.value == 15){this.form.increase1.disabled=true;}" style = "font-size:8px; margin:0; padding:0; width:28px;  height:21px;" >
								<input type = "button" value = "&#9660;" name = 'reduce1' onclick = "this.form.size.value--; if (this.form.size.value <= 1){this.form.reduce1.disabled=true;} if (this.form.size.value < 5){this.form.increase1.disabled=false;}" style = "font-size:8px; margin:0; padding:0; width:28px; height:21px;" disabled>
							</div>
	</td>
	</div>
				     </tr>

	</table>
	
	<div>
	<button class = 'buttonClass' type="submit" name = 'submit_rotate_log' value = 'Rotate log' onclick = 'return do_rotate_log(document.rotate_log.freq_rotate.value, document.rotate_log.size.value);' style="float: right; margin-right: -46%;">Rotate Log</button>
	<button class = 'buttonClass' type="submit" name = 'fetch_info' value = 'Fetch' onclick = 'return fetch_log();' style="float: right; margin-right: -24%;">Fetch Log</button>
	</div>

	 </form>"""


	print"""</div>
	</div>
	</div>
	<!--form container ends here-->
	<p>&nbsp;</p>
	      </div>"""
	print"""

	<div id="tabs-4">
			<!--form container starts here-->
			<div class="form-container">
			  <div class="topinputwrap-heading">SMB Log Information</div>
			 <div class="inputwrap">
			<div class="formrightside-content">
			 <form name = 'smb_log_path' method = 'POST' action="main.py?page=logs#tabs-4">
					<table width = '100%' border = "0" cellspacing = "0" cellpadding = "0" class = "outer_border">
						<tr>
							<td width = '25%' class = "table_heading" height = "35px" valign = "middle">
								<B>Choose log path:</B>
							</td>
							<td width = '75%' class = "table_content" height = "35px" valign = "middle" bgcolor = "#f5f5f5">
									<div class="styled-select2" style="width:335px;">
									<select class = 'textbox' name = 'audit_path' style = 'width:349px;'>
	<option value='select' selected>Select a Share</option>"""

	#for i in split_line:

	for share_name_info in share_infos:
		share_nm = share_name_info['name']
		if(share_name_info["path"] == retrieve_log_path):
			selected = "selected"
		else:
			selected = ""
		print """<option """+selected+"""  value = """+share_nm+""">"""+share_nm+"""</option>"""


	print """
	</select></div><BR>
							</td>
						</tr>


	<tr>
							<td colspan = '0' align = 'right'>
								<BR><!--<input class = 'input1' type = 'button' name = 'apply' value = 'Set Log Path' onclick = 'return enable_smb_log_path(document.smb_log_path.audit_path.value);' >-->
	<div>

	<!--<span id="button-one"><button type = 'submit' name = 'set_log_path' value = 'set_log_path' onclick = 'return validate_set_log_path();' style = 'background-color:#ffffff; border:none;float:none;font-size: 82%;' title="Set Logs"><a style="font-size:90%;  width: 100%;">Set Log Path</a></button></span>-->

	<button class = 'buttonClass' type="submit" name = 'set_log_path' value = 'set_log_path' onclick = 'return validate_set_log_path();'>Set Log</button>


	<button class = 'buttonClass' type="submit" name = 'reset_log_path' value = 'Reset Logs' onclick = 'return confirm("Audit Log for all SMB shares will be disabled and All SMB Connection will be Restarted.Do you still to Continue?");' style ="margin-right:-240px;">Reset Log</button>


	</div>
								<!--<input class = 'input1' type = 'button' name = 'unset' value = 'Reset to default' onclick = 'return enable_smb_log_path("unset");' <?= $smb_log_disabled ?>><BR><?= $message ?>-->
							</td>
						</tr>
					<input type = 'hidden' name = 'hid_share' value = ''>
					<input type = 'hidden' name = 'hid_path' value = '>'>
				</table>
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

	print"""
	<!--body wrapper end-->
	</body>
	</html>
	"""
except Exception as e:
	disp_except.display_exception(e);
