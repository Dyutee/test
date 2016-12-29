#!/usr/bin/python
import cgitb, header, os, sys, commands, opslag_info
cgitb.enable()

sys.path.append('../modules/')
import disp_except;
try:
	sys.path.append("/var/nasexe/python/")
	import tools
	date_cmd=commands.getoutput('sudo date +"%Y"')
	os_name= opslag_info.getos('oss')

	#change_pass_cmd = tools.change_password("Full Access","netweb","opslag")
	#print change_pass_cmd

	if(header.form.getvalue("change_password")):
		get_old_pass = header.form.getvalue("old_password")
		get_new_pass = header.form.getvalue("new_password")
		get_re_new_pass = header.form.getvalue("re_new_password")
		if((get_old_pass != None) and (get_new_pass != None)):
			if(get_new_pass == get_re_new_pass):
				change_pass_cmd = tools.change_password("Full Access",get_old_pass,get_new_pass)
				if(change_pass_cmd["id"] == 0):
					print "<div id='id_trace'>"
					print change_pass_cmd["desc"]
					print "</div>"
				else:
					print "<div id='id_trace_err'>"
                                        print change_pass_cmd["desc"]
                                        print "</div>"

	import left_nav
	print
	print """

	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer">
		<div class="insidepage-heading">Maintenace >> <span class="content">Change Password</span></div>
		<!--tab srt-->
		<div class="searchresult-container">
		  <div class="infoheader">
		    <div id="tabs">
		      <ul>
			<li><a href="#tabs-1">Change Password</a></li>
		      </ul>

		<div id="tabs-1">
		<!--form container starts here-->
		<form name="change_password_form" method="post" action="" />
		<div class="form-container">
		<div class="inputwrap">
		<div class="formleftside-content">

		<table style="width:500px;">
		<tr>
		<td>Enter Old Password</td>
		<td>
		<input type="password" name="old_password" class = 'textbox' style="width:188px;" /></td>
		</tr>

		<tr>
		<td>Enter New Password</td>
		<td><input type="password" name="new_password" class = 'textbox' style="width:188px;" /></td>
		</tr>

		<tr>
		<td>Re-enter New Password</td>
		<td><input type="password" name="re_new_password" class = 'textbox' style="width:188px;" /></td>
		</tr>

		<tr>
		<td></td>
		<td>
		<button class = 'buttonClass' type="submit" name = 'change_password' value = 'change_password' style = 'float:right;width:133px;' onclick="return validate_change_password();">Change Password</button>
		</td>
		</tr>

		</table>

		</div>
		</div>
		</div>
		<!--form container ends here-->
		<p>&nbsp;</p>
		</form>
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
	    <div class="insidefooter footer_content">&copy """+date_cmd+""" """+os_name+""" FS2</div>
	    <!-- Footer ends here-->
	  </div>
	  <!--inside body wrapper end-->
	</div>
	<!--body wrapper end-->
	</body>
	</html>

	<!-- ####### Sub Tabs Start ####### -->

	<script>
	$("#tabs, #subtabs").tabs();
	$("#tabs, #subsubtabs").tabs();
	</script>

	<!-- ####### Sub Tabs End ####### -->

	"""
except Exception as e:
        disp_except.display_exception(e);
