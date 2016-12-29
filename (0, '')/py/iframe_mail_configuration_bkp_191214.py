#!/usr/bin/python
import cgitb, sys, common_methods, include_files, cgi
cgitb.enable()
sys.path.append('../modules/')
import disp_except;
try:
	#---------------------Import backend modules---------------------------------------
	sys.path.append('/var/nasexe/python/')
	import tools
	from tools import send_mail
	from tools import db
	from tools import scan_remount
	from tools import shutdown
	#--------------------------------End--------------------------------------------------
	
	form = cgi.FieldStorage()
	#--------------------------Check ha status--------------------------------------------
	check_ha = tools.check_ha()
	#------------------------------------End---------------------------------------------
	#--------------------------------------Get node name--------------------------------
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
	#------------------------------------------End---------------------------------------
	#--------------------------------call backend function for get the mail information value------------------------
        mail_val_func =scan_remount.mail_val()
	#-----------------------------------------------End--------------------------------------------------------------
        #mail_val_func =shutdown.mail_val()
	#print 'Test:'+str(mail_val_func)
	#-----------------------------------------Assigned a empty value for variable--------------------------------------
	dic={}
	get_server_name = ''
	get_port = ''
	get_auth =''
	get_tsl = ''
	get_from_mail = ''
	get_username = ''
	get_to = ''
	get_password = ''
	get_message = ''
	display_optn_one = 'none'
	display_optn_two = 'none'
	display_del_optn = 'none'
	display_del_optn1= 'none'
	#------------------------------------------------End---------------------------------------------------------------
	#----------------------------Set value----------------------------#
	if(form.getvalue("select_auth")):
		get_auth = form.getvalue("select_auth")
		get_server_name = form.getvalue("server_name")
		if(get_auth == "on"):
			display_optn_one = 'block'
			display_optn_two = 'block'
		else:
			display_optn_one = 'none'
			display_optn_two = 'none'

	if(form.getvalue("send_mail")):
		get_server_name = form.getvalue("server_name")
		get_auth =form.getvalue("select_auth")
		get_port = form.getvalue("port_name")
		get_tsl = form.getvalue("select_tsl")
		get_from_mail = form.getvalue("from_email")
		get_username = form.getvalue("user_name")
		get_password = form.getvalue("user_pass")
		get_to = form.getvalue("to_mail")
		get_message = form.getvalue("message_text")
		dic={'server':get_server_name,'auth':get_auth,'port':get_port,'from':get_from_mail,'user':get_username,'pass':get_password,'tsl':get_tsl,'to':get_to}
		#print 'DICTIONARY:'+str(dic)
		#print '<br/>'
		set_smtp_status = send_mail.set_smtp(dic)

		if(set_smtp_status == True):
                	print"""<div id = 'id_trace'>"""
                	print "Successfully Configure the Mail!"
                	print "</div>"
                	#print "<script>location.href = 'main.py?page=mail#tabs-1';</script>"
        	else:
                	print"""<div id = 'id_trace_err'>"""
                	print "Error occured while Configuring the mail!"
			print "</div>"
                	#print "<script>location.href = 'main.py?page=mail#tabs-1';</script>"
		#print 'SET SMTP:'+str(set_smtp_status)
		#print '<br/>'
		#print '<br/>'
		#send_mail_status = send_mail.send_mail(get_message= '')
		#print send_mail_status

	#---------------------End------------------------------------
	#--------------------Get Values------------------------------
	if(form.getvalue("mail_values")):
		mail_val_func =scan_remount.mail_val()
		#print mail_val_func
		get_server_name = mail_val_func[2]
        	get_server_name = get_server_name.replace("host", "")
		get_server_name = get_server_name.strip()
		get_from_mail = mail_val_func[3]
        	get_from_mail = get_from_mail.replace("from", "")
		get_from_mail = get_from_mail.strip()
        	get_auth = mail_val_func[4]
		get_auth = get_auth.replace("auth", "")
		get_auth = get_auth.strip()
		get_username = mail_val_func[5]
		get_username = get_username.replace("user", "")
		get_username = get_username.strip()
		#print get_auth
		get_to = mail_val_func[11]
		get_to = get_to.replace("TO", "")
		get_to = get_to.replace("=", "")
		get_to = get_to.replace('"', '')
		get_to = get_to.strip()
		get_port = mail_val_func[7]
		get_port = get_port.replace("port", "")
		get_port = get_port.strip()
		get_tsl ='off' 
		if(get_auth == 'on'):
		
			display_optn_one = 'block'
                	display_optn_two = 'block'
		else:
			display_optn_one = 'none'
                        display_optn_two = 'none'

		if(mail_val_func == []):
			mail_val_func  = False
		else:
			mail_val_func = True

		if(mail_val_func == True):
                        print"""<div id = 'id_trace'>"""
                        print "Successfully get the Mail Information"
                        print "</div>"
                        #print "<script>location.href = 'main.py?page=mail#tabs-1';</script>"
                else:
                        print"""<div id = 'id_trace_err'>"""
                        print "Error occured while getting the Mail Information!"
			print"</div>"
                        #print "<script>location.href = 'main.py?page=mail#tabs-1';</script>"
		
		#print '<br/>'
		#print mail_val_func
		
	#---------------------End-----------------------------------

	print """
		<div id="loader-div" style="text-align:center; display:none;" ><img style="margin-top:20%;" src="../images/ajax-loader.gif" /><br/> Loading...</div>
	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer" id="body-div">
		<!--tab srt-->
		<div class="searchresult-container">
		<div style="margin:0 0 0px 0;" class="topinputwrap-heading"><a class="demo" href ="#"><img src ="../images/help_icon1.png" style="width:13px;"><span class="tooltip" >
                 <table border="0">
        <tr>     
        <td class="text_css">This page lets you configure the mail settings for your FS2 system.</td>
        </tr>
        </table>"""
	if(check_ha == True):
		print"""
	</span></a><span style="color:#fff;margin-left:7px;">Mail Configuration of """+show_tn+"""</span>
                <span style="float:right; margin:0 0px 0 0;"><a onclick="return onclick_loader();" class="resource_links" href="https://"""+other_node_ip+"""/fs4/py/iframe_mail_configuration.py">"""+show_on+"""</a></span>
                </div>"""
	else:
		print """</span></a>Mail Configuration </div>"""
	print"""
		  <div class="infoheader">
		   <!-- <div id="tabs">
		      <ul>
			<li><a href="#tabs-1">Mail Configuration</a></li>
		      </ul>-->
		      <div id="tabs-1">
		<!--form container starts here-->
		<div class="form-container">
		  <div class="inputwrap">
		    <div class="formleftside-content">
	<form name='mail_form' method='post'>
		<table  width = "480" border = "0"  cellspacing = "0" cellpadding = "0">
		<tr>
 <td valign="top">
  <label>Server Name:<font color ="#EC1F27"></font></label>
 </td>
 <td valign="top">
  <input  type="text" class = 'textbox' name="server_name" maxlength="100" size="25" value = '"""+get_server_name+"""' style="width: 218px;">
 </td>
</tr>
 
<tr>
 <td valign="top"">
  <label>Authentication:<font color ="#EC1F27"></font></label>
 </td>
 <td valign="top">
 <div class="styled-select2" style="width:218px;">"""
	if(get_server_name !=''):
	
		print"""<select name = 'select_auth'style="width:230px;" onchange='this.form.submit()' value = '"""+get_auth+"""'>"""

	else:
		print"""<select name = 'select_auth'style="width:230px;" onchange='this.form.submit()' value = '"""+get_auth+"""' onclick = 'return validate_chk_server_nm();'>"""

	print"""
                        <option value = 'select_auth_val'>Select Authentication</option>"""

	print"""
                        <option value = 'on'"""
        if(get_auth !=''):
                if(get_auth == "on"):
                        print """selected = 'selected'"""

        print""">Yes</option>"""
	print"""
			<option value = 'off'"""
	if(get_auth !=''):
		if(get_auth == "off"):
			print """selected = 'selected'"""
	print""">No</option>"""
	print"""			</select>
</div>
 </td>
</tr>
<tr>
 <td valign="top">
  <label>Port:<font color ="#EC1F27"></font></label>
 </td>
<td valign="top">"""
	if(get_port !=''):
		print"""<input  type="text" class = 'textbox' name="port_name" value = '"""+get_port+"""' maxlength="80" size="25" style="width: 218px;">"""
	else:
		print"""<input  type="text" class = 'textbox' name="port_name" value = "587" maxlength="80" size="25" style="width: 218px;">"""
	print"""</td>
 
</tr>
<tr>
 <td valign="top"">
  <label>TLS:<font color ="#EC1F27"></font></label>
 </td>
 <td valign="top">
 <div class="styled-select2" style="width:218px;">
                        <select name = 'select_tsl'style="width:230px;">
                        <option value = 'select_tsl_val'>Select TLS</option>"""
	print"""
                        <option value = 'on'"""
	if(get_tsl !=''):
		if(get_tsl == 'on'):
			print """selected = 'selected'"""
	print""">Yes</option>"""

	print"""
	                <option value = 'off'"""
	if(get_tsl !=''):
		if(get_tsl == 'off'):
			print """selected = 'selected'"""
	print""">No</option>"""
        print"""                </select>
</div>
 </td>
</tr>
<tr>
 <td valign="top">
  <label>From:<font color ="#EC1F27"></font></label>
 </td>
 <td valign="top">
  <input  type="text" class = 'textbox' name="from_email" maxlength="100" size="25" value = '"""+get_from_mail+"""' style="width: 218px;">
 </td>
</tr>
<tr id = 'optn_one' style = 'display:"""+display_optn_one+""";'>
 <td valign="top">
  <label>Username:<font color ="#EC1F27"></font></label>
 </td>
 <td valign="top">
  <input type name="user_name" class = 'textbox' value = '"""+get_username+"""'maxlength="100" size="25" style="margin-left: 100%;width:218px;">
 </td>
 
</tr>

<tr id = 'optn_two' style = 'display:"""+display_optn_two+""";'>
 <td valign="top">
  <label>Password:<font color ="#EC1F27"></font></label>
 </td>
 <td valign="top">
  <input type = "password" class = 'textbox' name="user_pass" maxlength="100" size="25" style="margin-left: 100%;width:218px;">
 </td>
 
</tr>

<tr>
 <td valign="top">
  <label>To:<font color ="#EC1F27"></font></label>
 </td>
 <td valign="top">
  <input type name="to_mail" class = 'textbox' maxlength="100" size="25" value = '"""+get_to+"""' style="width: 218px;">
 </td>
 
</tr>

<!--<tr>
 <td valign="top">
  <label>Message:<font color ="#EC1F27"></font></label>
 </td>
 <td valign="top">
  <textarea  name="message_text" maxlength="1000" cols="25" rows="6"></textarea>
 </td>
 
</tr>-->

	<tr>
	<td>
                <div>
                <td style= "float:right;">
        <button class = 'buttonClass' type="submit" name = 'send_mail' value = 'send' onclick ='return validate_mail_configuration();'>Set</button>
        </td>

        </div>
        </td>

	 <td>
                <div>
                <td style= "float:right;">
        <button class = 'buttonClass' type="submit" name = 'mail_values' value = 'get_values' onclick =''>Get</button>
        </td>

        </div>
        </td>
								    </tr>
<tr>
	<td colspan = "2" style="font-family: georgia;">All fields are mandatory</td>
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
