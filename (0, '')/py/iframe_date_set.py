#!/usr/bin/python
import cgitb, sys, include_files, cgi
cgitb.enable()
form = cgi.FieldStorage()

sys.path.append('../modules/')
import disp_except
try:
	###########################################
	############# import modules ##############
	###########################################
	import os, commands, time, ntp_client_conf, common_methods, cgi, string
	sys.path.append('/var/nasexe/python/tools/')
	import ntp
	sys.path.append("/var/nasexe/python/")
        import tools
	check_ha = tools.check_ha()

	image_icon = common_methods.getimageicon();
	check_ntp = ntp_client_conf.server();

	###########################################
	############# default values ##############
	###########################################
	existing_ntp_server_input = '';
	message = '';
	ntpdisabled = '';
	disabled = '';
	manual_selected = '';
	manual_style = 'block';
	ntp_selected = '';
	ntp_style = 'none';
	sync_selected = '';
	pc_selected = '';
	mode_array = [];

	###########################################
	## check which mode is set Manual or NTP ##
	###########################################
	mode = commands.getoutput("sudo grep 'MODE=' /var/nasconf/set_date_global");
	mode = mode.strip();
	mode_array = mode.split('=');
	mode_val = mode_array[1].strip();

	###########################################################
	## Function to convert Date into Format MMDDHHmmYY Start ##
	###########################################################
	def format_date(get_date):
		split_gmd = string.split(get_date)
		date_str = split_gmd[0]
		time_str = split_gmd[1]

		split_ds = string.split(date_str,"-")
		DD_str = split_ds[0]
		if(len(DD_str) == 1):
			DD_str = "0"+DD_str

		MM_str = split_ds[1]
		if(len(MM_str) == 1):
			MM_str = "0"+MM_str
		YY_str = split_ds[2]
		
		if(MM_str == "Jan"):
			MM_str = "01"
		elif(MM_str == "Feb"):
			MM_str = "02"
		elif(MM_str == "Mar"):
			MM_str = "03"
		elif(MM_str == "Apr"):
			MM_str = "04"
		elif(MM_str == "May"):
			MM_str = "05"
		elif(MM_str == "Jun"):
			MM_str = "06"
		elif(MM_str == "Jul"):
			MM_str = "07"
		elif(MM_str == "Aug"):
			MM_str = "08"
		elif(MM_str == "Sep"):
			MM_str = "09"
		elif(MM_str == "Oct"):
			MM_str = "10"
		elif(MM_str == "Nov"):
			MM_str = "11"
		elif(MM_str == "Dec"):
			MM_str = "12"

		YY_str = YY_str[2:]

		split_ts = string.split(time_str,":")
		HH_str = split_ts[0]
		min_str = split_ts[1] 

		if(len(min_str) == 1):
			min_str = "0"+min_str


		full_date_str = MM_str+DD_str+HH_str+min_str+YY_str
		return full_date_str
	#########################################################
	## Function to convert Date into Format MMDDHHmmYY End ##
	#########################################################

	#########################################################
	################# Manual Date Start #####################
	#########################################################
	if(form.getvalue("action_but")):
		get_radio_val = form.getvalue("set_mode")
		get_manual_date = form.getvalue("setDate")
		format_date = format_date(get_manual_date)

		if(get_radio_val == "pc_time"):
			get_hid_pc_time =form.getvalue("hid_pc_time") 
			format_date = format_date(get_hid_pc_time)

		set_date_cmd = ntp.set_date(date=format_date)
		if(set_date_cmd == True):
			unconf_ntp = ntp.unconfigure()
			print """<script>location.href='iframe_date_set.py?valdate=success';</script>"""
			print"""<div id = 'id_trace' >"""
			print "Successfully set date!"
			print "</div>"
		else:	
			print"""<div id = 'id_trace_err' >"""
			print "Error setting Date!"
			print "</div>"
	#########################################################
	################### Manual Date End #####################
	#########################################################

	#########################################################
	##################### PC Time Start #####################
	#########################################################
	if(form.getvalue("use_pc_time")):
		get_hid_pc_time =form.getvalue("hid_pc_time")
		format_date = format_date(get_hid_pc_time)
		set_date_cmd = ntp.set_date(date=format_date)
		if(set_date_cmd == True):
			unconf_ntp = ntp.unconfigure()
			print"""<div id = 'id_trace' >"""
			print "Successfully set date!"
			print "</div>"
		else:
			print"""<div id = 'id_trace_err' >"""
			print "Error setting Date!"
			print "</div>"

	if(form.getvalue("valdate")):
		if(form.getvalue("valdate") == "success"):
			print"""<div id = 'id_trace' >"""
			print "Successfully set date!"
			print "</div>"
	#########################################################
	##################### PC Time End #######################
	#########################################################

	#########################################################
	################ NTP Synchronize Start ##################
	#########################################################
	if(form.getvalue("syncronize_ntp")):
		get_ntp_add = form.getvalue("ntp_server_add")
		synchronize_cmd = ntp.sync(get_ntp_add)
		if(synchronize_cmd == True):
			print"""<div id = 'id_trace' >"""
			print "Successfully Synchronized to "+get_ntp_add
			print "</div>"
		else:
			print"""<div id = 'id_trace_err' >"""
			print "Error synchronizing to "+get_ntp_add
			print "</div>"
	#########################################################
	################ NTP Synchronize End ####################
	#########################################################

	#########################################################
	################ NTP Configure Start ####################
	#########################################################
	if(form.getvalue("configure_ntp")):
		get_ntp_add = form.getvalue("ntp_server_add")
		configure_cmd = ntp.configure(get_ntp_add.strip())
		if(configure_cmd == True):
			print"""<div id = 'id_trace' >"""
			print "Successfully configured "+get_ntp_add
			print "</div>"
		else:
			print"""<div id = 'id_trace_err' >"""
			print "Error configuring "+get_ntp_add
			print "</div>"
	#########################################################
	################## NTP Configure End ####################
	#########################################################

	#########################################################
	################## NTP Status Start #####################
	#########################################################
	get_ntp_status = ntp.get_server()
	if(get_ntp_status != ''):
		print "<script>location.href = 'iframe_date_set.py#tabs-2';</script>"
		ntp_val = get_ntp_status
		ntp_val2 = get_ntp_status
	else:
		ntp_val = "Enter NTP Server Name" 
		ntp_val2 = ""
		manual_selected = 'checked'
		manual_style = 'block'
	#########################################################
	#################### NTP Status End #####################
	#########################################################

	if (mode_val == 'manual'):
		manual_selected = 'checked';
		manual_style = 'block';


	if (mode_val == 'pc_time'):
		pc_selected = 'checked';

	if (mode_val == 'ntp_time'):
		ntp_selected = 'checked';
		ntp_style = 'block';
		disabled = 'disabled';
		sync_selected = 'checked';
		existing_ntp_server_input = ntp_client_conf.server();

	if(form.getvalue("username")):
		if(username == "Maintenance"):
			getmanual=form.getvalue("manual")
			getserver=form.getvalue("server")
			print getmanual
			print getp

	sys.path.append("/var/nasexe/python/")
        import tools
        from tools import db
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

	print"""
		<div id="loader-div" style="text-align:center; display:none;" ><img style="margin-top:20%;" src="../images/ajax-loader.gif" /><br/> Loading...</div>
		 <!--Right side body content starts from here-->
		      <div class="rightsidecontainer" id="body-div">
			<!--tab srt-->
			<div class="searchresult-container">
			<div style="margin:0 0 0px 0;" class="topinputwrap-heading">
			<a class="demo" href ="#"><img src ="../images/help_icon1.png" style = "width:13px;"><span class="tooltip">
                 <table border="0">
        <tr>     
        <td class="text_css">This page allows you to set the date and time for your system, either manually or by specifying an NTP server.</td>
        </tr>
        </table>"""
	if(check_ha == True):
		print"""</span></a><p class = "gap_text">Date/Time Settings ("""+show_tn+""")</p>
                <span style="float:right; margin:-15px 0px 0 0;"><a onclick="return onclick_loader();" class="resource_links" href="https://"""+other_node_ip+"""/fs4/py/iframe_date_set.py">"""+show_on+"""</a></span>
               		</div>"""
	else:
		print"""</span></a><p class = "gap_text">Date/Time Settings</p></div>"""
	print"""
			  <div class="infoheader">
			    <div id="tabs">
			      <ul>
				<li><a href="#tabs-1">Manual/PC Time</a></li>
				<li><a href="#tabs-2">NTP Server Time</a></li>
			      </ul>
				
				<div id="tabs-1">
				<div class="form-container">
				<!--<div class="topinputwrap-heading">Set Date/Time</div>-->
				<div class="inputwrap">
				<center style="color:#365371;font-family:georgia;"><B>Current Date: """+time.strftime('%d-%h-%y')+"/"+time.strftime('%H:%M:%S')+"""</B></center>
			   <div class="formleftside-content" style = 'border: 0px solid;'>
			   <form name = 'set_time' action = 'iframe_date_set.py#tabs-1' method = 'POST'>
			   <table>
				   <!--<tr>
				      <td align="left"><input type="radio" name="set_mode" value="manual" """ + manual_selected + """ onclick = 'return show_date_time();'></td>
					
				      <td>Manual:</td>
				      </tr>-->

			<tr>
								<td>
								</td>
								<td>
									<div id = 'id_set_time' style = 'width: 90%; display: """ + manual_style + """;' border: 0px solid;'><BR>
									<table>
										<tr>
											<td>
											    Date:
											</td>
											<td>

			<input name="setDate" id="demo3" class = "textbox" type="text" readonly value ="">"""
	print"""
		<!--<a href="javascript:NewCal('demo3','ddmmmyyyy',true,24, 'datetime')"><img src="../images/cal.gif"  style="margin-top: -10%; margin-left: 174px;" border="0" alt="Pick a date"></a> -->
<a href="javascript:show_calendar('document.set_time.setDate', document.set_time.setDate.value);"><img src="../images/cal1.gif" style="margin-top: -10%; margin-left: 174px;" width="16" height="16" border="0" alt="Click Here to Pick up the timestamp"></a>

                                              </td>
									       </tr>


			<tr>
											<td style="text-indent: 141px;">
												<!--<BR><font color ="#EC1F27">Select a time zone</font>:-->
												<!--<BR>Select a time zone:-->
											</td>
											<td>
												<BR>
<div class="styled-select2" style = "width:277px;display:none;">
<select name="DropDownTimezone" id="DropDownTimezone" style = "width:290px;">
													<option value="IST">Mumbai, Kolkata, Chennai, New Delhi</option>
												</select></div>
											</td>
										</tr>
	</table>

	<!--<button class = 'button_example' style="margin:20px 0 0 0;" type="submit" name = 'action_but'  value = 'action_but' """ + disabled + """ onclick="return validate_date_time_form();">Apply New Date</button>-->
	<div class="buttonWrapper" style="width:110px;">
	<button class="buttonClass" type = "submit"  name="action_but" value="action_but" onclick="return validate_apply_new_date();" style="margin-bottom: -7px;margin-left:118px;">Set Date</button></div>
	
	<div class="buttonWrapper" style="width:110px;margin-left: 264px; width: 110px; margin-top: -34px;">
	<button class = 'buttonClass' type="submit" name = 'use_pc_time'  id = 'use_pc_time' value = 'Apply' onclick="return create_hid_date();" style="margin-bottom: 5px;">PC Time</button></div>



				<!-- <tr>
					<td>
					<input type="radio" name="set_mode" value="pc_time" onclick = 'return show_date_time();' """ + pc_selected + """>
					</td>
					
					<td>	
					Use this PC time:
					</td>
				    </tr>-->

				 <tr>
					<td>
					
					</td>
				      <td>
				       </td>
				    </tr>

					<tr>
								<td width = '10%'>
								</td>
								<td >
									<div id = 'id_ntp_time' style = 'width: 90%; display:""" + ntp_style + """;'>
									<table width="100%">
										<tr>

											<td>
												<font color ="#EC1F27">NTP Server</font>:
											</td>
											<td>
												<input type = 'text' name = 'ntp_server' value = '""" + existing_ntp_server_input + """' oninput = 'document.getElementById("id_sync_ntp").checked = false;'>
											</td>
										</tr>

	<tr>


											<td>
												<input id = 'id_sync_ntp' type = 'checkbox' name = 'synch_ntp' onclick = 'return run_ntp_sync(this.form.synch_ntp.checked);'""" + sync_selected + """>
											</td>

											<td><font color ="#EC1F27">Sync. now</font></td>
										</tr>
	</table>
	 <tr>
								<td colspan = '2' align = 'right'>


	<div><!--<span id="button-one"><button type = 'submit'  name = 'action_but' onclick = 'return validate_date_time_form();' style = ' background-color:#FFFFFF;border:none; float:right;  font-size: 86%; '""" + disabled + """ title="Apply"><a style="font-size:85%;"  >Apply</a></button></span>-->


	</div>

	<input type = 'hidden' name = 'hid_time' value = ''>
									<input type = 'hidden' name = 'set_date_page' value = 'proceed'>
									<input type = 'hidden' name = 'hid_curdate' value = ''>
		<input type = 'hidden' name = 'hid_curtime' value = ''>
									<input type = 'hidden' name = 'hid_session_user' value = ''>
									<input type = 'hidden' name = 'hid_pc_time' value = ''>

	</td>

		</tr>
				</table>
				</form>

			   </div>
				</div>
			    <div class="formrightside-content"></div>
			  </div>
				<p>&nbsp;</p>
					  </div>


	<div id="tabs-2">

		<!--form container starts here-->
		<div class="form-container">
		  <div class="inputwrap">
	<div class="formleftside-content">

	<form name="ntp_server_time" method="POST" action="iframe_date_set.py#tabs-2" >
	<table style="margin:20px 0 20px 100px; width:100%;">

	<tr>
	<td><input type="text" name="ntp_server_add" class="textbox" value='"""+ntp_val+"""' onfocus="if (this.value == '"""+ntp_val+"""') this.value = '"""+ntp_val2+"""';" onblur="if (this.value == '') this.value = '"""+ntp_val+"""';" />

	<button class = 'buttonClass' type="submit" name = 'syncronize_ntp'  id = 'syncronize_ntp' value = 'syncronize_ntp' style ="margin-left:-12px;margin-top:29px;" onclick = 'return sync_ntp_server(this.form.ntp_server_add.value);'>Synchronize</button>

	<button class = 'buttonClass' type="submit" name = 'configure_ntp'  id = 'configure_ntp' value = 'configure_ntp' style="float: right; margin-right: -27px; margin-top: 28px;" onclick = 'return sync_ntp_server(this.form.ntp_server_add.value);'>Configure</button>

	</td>
	</tr>

	<tr>
	<td></td>
	<td>

	</td>
	</tr>

	</table>

	</form>

		  </div>
	</div>
	</div>
	<!--form container ends here-->
	<p>&nbsp;</p>
			      </div>

	"""
except Exception as e:
	disp_except.display_exception(e);
