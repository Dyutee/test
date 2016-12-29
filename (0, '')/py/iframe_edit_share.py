#!/usr/bin/python
import cgitb, sys, common_methods, string, include_files, cgi
cgitb.enable()
form = cgi.FieldStorage()
sys.path.append('../modules/');
import disp_except;

#print 'Content-Type: text/html'

try:
	get_share_name = form.getvalue("share_name")

	sys.path.append("/var/nasexe/python/")
	import tools


	#------------------------------ Edit Share Start --------------------------------#
	if(form.getvalue("update_share")):
		get_share = form.getvalue("share")
		get_comment = form.getvalue("comment")
		get_path = form.getvalue("path")
		if(get_comment == None):
			get_comment = ''		

		if((get_share != None) and (get_share != '')):
			update_share = tools.edit_share(share_name=get_share,comment=get_comment,debug=False)
			if(update_share["id"] == 0):
				print "<div id='id_trace'>"
				print update_share["desc"]
				print "</div>"
			else:
				print "<div id='id_trace_err'>"
                                print update_share["desc"]
                                print "</div>"
		else:
			print "<div id='id_trace'>"
			print "Error: Cannot fetch share name!"
			print "</div>"
	#------------------------------ Edit Share End --------------------------------#



	#share_path    = common_methods.get_share_path(get_share);
	#disppath      = share_path.replace('/storage/', '');
	#share_comment = common_methods.get_share_comment(get_share);

	
	status = tools.get_share(get_share_name,debug=False)
	share_details = status["share"]
	mod_share_path = str(share_details["path"]).replace("/storage","")

	print
	print """

	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer">
		<!--tab srt-->
		<div class="searchresult-container">
		  <div class="infoheader">
		    <div id="tabs">
		      <ul>
			<li><a href="#tabs-1">Edit Share</a></li>
		      </ul>
		      <div id="tabs-1">

		<!--form container starts here-->
		<form name = 'edit_this_share' method = 'POST' >
		<div class="form-container">

		<!--<div class="topinputwrap-heading">Edit Share '"""+get_share_name+"""'</div>-->
		  <div class="inputwrap">
		<table width="100%" style="padding:0 0 0 10px;">
			<tr>
			<td width="30%">Share Name</td>
			<td><input class = 'textbox' type = 'text' readonly name = 'share' value = '""" + str(get_share_name) + """'></td>
			</tr>
			<tr>
			<td>Comment</td>
			<td><input class = 'textbox' type = 'text' name = 'comment' value = '""" + str(share_details["comment"]) + """'></td>
			</tr>
			<tr>
			<td>Share Path</td>
			<td><input class = 'textbox' type = 'text' readonly name = 'path' value = '""" + str(mod_share_path) + """'></td>
			</tr>

			<tr>
			<td></td>
			<td>

			<button class="buttonClass" type = 'submit'  name="update_share" value="update_share" style="float:right; margin:20px 338px 20px 0;">Update</button>
			</td>
			</tr>
			</table>
		  </div>
	</div>
	</form>
	<!--form container ends here-->
	<p>&nbsp;</p>
	      </div>

	  </div>
	</div>
	</div>
	"""

except Exception as e:
	disp_except.display_exception(e);
