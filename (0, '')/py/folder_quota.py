#!/usr/bin/python
import cgitb, sys, header
cgitb.enable()

sys.path.append('../modules/')
import disp_except;

try:
	#print 'Content-Type: text/html'

	sys.path.append('/var/nasexe/python/')
	import quota
	import tools
	from tools import prjquota


	get_share = header.form.getvalue("share_name")
	get_share_path = prjquota.get_sharepath(get_share)

	get_sharess = tools.get_all_shares(debug=True)
	for x in get_sharess["shares"]:
		if x["name"] == get_share:
			selected_share =  x["name"]
			selected_share_path = x["path"]

	if(header.form.getvalue("enable_fq")):
		get_size = header.form.getvalue("size")
		get_size = str(get_size).strip()+"G"

		folder_quota_cmd = prjquota.prj_q_create(get_share,spath=get_share_path,size=get_size)
		if(folder_quota_cmd == True):
			print "<div id='id_trace'>"
			print "Successfully enabled Folder Quota for "+get_share
			print "</div>"
		else:
			print "<div id='id_trace_err'>"
			print "Error enabling Folder Quota for "+get_share
			print "</div>"

	if(header.form.getvalue("disable_fq")):
		del_folder_qo_cmd = prjquota.prj_q_rem(get_share,spath=get_share_path)
		if(del_folder_qo_cmd == True):
			print "<div id='id_trace'>"
			print "Successfully deleted Folder Quota for "+get_share
			print "</div>"
		else:
			print "<div id='id_trace_err'>"
			print "Error deleting Folder Quota for "+get_share
			print "</div>"

	show_qo_cmd = quota.show(option='project',sharename=get_share)
	if(show_qo_cmd["id"] == 0):
		qo_enabled = "yes"
		quota_dict = show_qo_cmd["quota"]
		for x in quota_dict:
			size_var = x["limit"]
	else:
		qo_enabled = "no"
		size_var = ""

	


	import left_nav
	print
	print """

	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer">
		<div class="insidepage-heading">Nas >> <span class="content">Folder Quota</span></div>
		<!--tab srt-->
		<div class="searchresult-container">
		  <div class="infoheader">
		    <div id="tabs">
		      <ul>
			<li><a href="#tabs-1">Folder Quota</a></li>
		      </ul>
		      <div id="tabs-1">

		<!--form container starts here-->
		<div class="form-container">
		<div style="padding:10px; background-color:#e9e5e5; border-bottom:#D1D1D1 1px solid; font-weight:bold;">Folder Quota for '"""+get_share+"""' <a href = 'main.py?page=cs'><img style="float:right; padding:0;" title = 'Back to shares' src = '../images/gobacktoshares.png' /></a></div>


		  <div class="inputwrap">
	<form name="folder_quota_form" action="" method="post">
	<table width="100%" style="margin:0 0 20px 10px;">
	<tr>
	<td>Selected Share</td>
	<td><input class="textbox" type="textbox" readonly name="sharename" value='"""+str(get_share)+"""' /></td>
	</tr>
	<tr>
	<td>Enter Size (GB)</td>
	<td><input class="textbox" type="textbox" name="size" onkeypress="return isNumberKey(event)" value='"""+size_var.replace("G","").strip()+"""' /></td>
	</tr>
	</table>

	<table width="100%">
	<tr>
	<td>"""

	if(qo_enabled == "no"):
		print """<button class="button_example" type = "submit"  name="enable_fq" value="enable_fq" style="float:left; margin:0 0 20px 100px;" onclick="return validate_folder_quota_form();">Enable Folder Quota</button>"""

	if(qo_enabled == "yes"):
		print """<button class="button_example" type = "submit"  name="enable_fq" value="enable_fq" style="float:left; margin:0 0 20px 100px;" onclick="return validate_folder_quota_form();">Update Folder Quota</button>"""
		print """<button class="button_example" type = "submit"  name="disable_fq" value="disable_fq" style="float:left; margin:0 0 20px 20px;" onclick='return confirm("Are you sure you want to delete folder quota?");' >Delete Folder Quota</button>"""

	print """
	</td>
	</tr>
	</table>

	
		</form>





		  </div>
	</div>
	<!--form container ends here-->
	<p>&nbsp;</p>
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
	</div>
	<!--body wrapper end-->
	</body>
	</html>
	"""
except Exception as e:
        disp_except.display_exception(e);
