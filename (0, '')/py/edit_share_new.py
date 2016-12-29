#!/usr/bin/python
import cgitb, sys, header, common_methods
cgitb.enable()

sys.path.append('../modules/');
import disp_except;

#print 'Content-Type: text/html'
import left_nav

try:
	get_share = header.form.getvalue("share_name")

	share_path    = common_methods.get_share_path(get_share);
	disppath      = share_path.replace('/storage/', '');
	share_comment = common_methods.get_share_comment(get_share);

	print
	print """

	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer">
		<div class="insidepage-heading">NAS >> <span class="content">Configure Information</span></div>
		<!--tab srt-->
		<div class="searchresult-container">
		  <div class="infoheader">
		    <div id="tabs">
		      <ul>
			<li><a href="#tabs-1">Edit Share</a></li>
		      </ul>
		      <div id="tabs-1">

		<!--form container starts here-->
		<form name = 'edit_this_share' method = 'POST'>
		<div class="form-container">
		<div class="view_option" style = 'border: 0px solid;'><a href = 'main.py?page=cs'><img title = 'Back to shares' src = '../images/gobacktoshares.png' /></a></div>

		<!--<div class="topinputwrap-heading">Edit Share '"""+get_share+"""'</div>-->
		  <div class="inputwrap">
		<table width="100%" style="padding:0 0 0 10px;">
			<tr>
			<td>Share Name</td>
			<td><input class = 'textbox' type = 'text' readonly name = 'share_name' value = '""" + get_share + """'></td>
			</tr>
			<tr>
			<td>Comment</td>
			<td><input class = 'textbox' type = 'text' name = 'comment' value = '""" + share_comment + """'></td>
			</tr>
			<tr>
			<td>Share Path</td>
			<td><input class = 'textbox' type = 'text' readonly name = 'share_path' value = '""" + disppath + """'></td>
			</tr>

			<tr>
			<td></td>
			<td>

			<button class="button_example" type = 'button'  name="cancelbutt" value="Cancel" onclick = "location.href = 'main.py?page=cs';" style="float:right;">Back</button>
			<button class="button_example" type = 'submit'  name="submit_hostname" value="Apply" onclick = "return validate_form();" style="float:right;">Apply</button>
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
