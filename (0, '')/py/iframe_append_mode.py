#!/usr/bin/python
import cgitb, sys, include_files, cgi
cgitb.enable()

sys.path.append('../modules/')
import disp_except
form = cgi.FieldStorage()

try:
	#################################################
	################ import modules #################
	#################################################
	sys.path.append('/var/nasexe/python/')
	import tools
	from fs2global import *
	from tools import acl
	#--------------------- END --------------------#

	#################################################
	################ Get all shares #################
	#################################################
	get_share = form.getvalue("share_name")
	get_sharess = tools.get_all_shares(debug=True)
	for x in get_sharess["shares"]:
		if x["name"] == get_share:
			selected_share =  x["name"]
			selected_share_path = x["path"]
	#--------------------- END --------------------#

	#################################################
	############## Enable Append Mode ###############
	#################################################
	if(form.getvalue("enable_append")):
		set_append_mode_cmd = acl.attr(selected_share_path, op='set')
		if(set_append_mode_cmd == True):
			print "<div id='id_trace'>"
			print "Successfully Enabled append mode for "+selected_share
			print "</div>"
		else:
			print "<div id='id_trace_err'>"
			print "Error enabling append mode for "+selected_share
			print "</div>"
	#--------------------- END --------------------#
			
	#################################################
	############# Disable Append Mode ###############
	#################################################
	if(form.getvalue("disable_append")):
		disable_append_mode_cmd = acl.attr(selected_share_path, op='rem')
		if(disable_append_mode_cmd == True):
			print "<div id='id_trace'>"
			print "Successfully disabled append mode for "+selected_share
			print "</div>"
		else:
			print "<div id='id_trace_err'>"
			print "Error disabling append mode for "+selected_share
			print "</div>"
	#--------------------- END --------------------#

	#--- Get Append Mode Status
	get_append_status = acl.attr(selected_share_path, op='get')

	print
	print """

	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer">
		<!--<div class="insidepage-heading">NAS >> <span class="content">Configure Information</span></div>-->
		<!--tab srt-->
		<div class="searchresult-container">
		  <div class="infoheader">
		    <div id="tabs">
		      <!--<ul>
			<li><a href="#tabs-1">Append Mode</a></li>
		      </ul>-->
		      <div id="tabs-1">

		<!--form container starts here-->
		<!--<div class="form-container">-->
		<div style="padding:10px; background-color:#e9e5e5; border-bottom:#D1D1D1 1px solid; font-weight:bold;">Append Mode for '"""+get_share+"""' 
<!--<a href = 'main.py?page=cs'><img style="float:right; padding:0;" title = 'Back to shares' src = '../images/gobacktoshares.png' /></a>-->
</div>


		  <div class="inputwrap">
		<form name = 'share_append' method = 'POST' action = ''>
		<table width = "685" border = "0" cellspacing = "0" cellpadding = "0" name = 'disp_tables' id = 'id_append_mode' style = 'display:block; margin:0 0 0 10px;' class = 'outer_border'>
			<tr>
				<td colspan = "3" align = "left" valign = "top">
				<table width = "685" border = "0" cellspacing = "0" cellpadding = "0" class = "border">
				<tr>
					<td width = "1%" class = "table_heading" height = "70px" valign = "middle">
	<!--<input type = 'checkbox' name = 'use_append_mode' onclick = 'return enable_append_mode();'/> <b style="color:#999999;"> Enable Append Mode</b>-->"""

	if(get_append_status == False):
		print """<button class="buttonClass" type = "submit"  name="enable_append" value="enable_append" style="float:left;" >Enable</button>"""
	else:
		print """<button class="buttonClass" type = "submit"  name="disable_append" value="disable_append" style="float:left;" >Disable</button>"""

	print """

					</td>
				</tr>
				</table>
				</td>
			</tr>
		</table>
		</form>





		  </div>
	</div>
	<!--form container ends here-->
	<p>&nbsp;</p>
	      <!--</div>-->

	</div>
	  </div>
	</div>
	</div>
	"""
except Exception as e:
        disp_except.display_exception(e);
