#!/usr/bin/python
import cgitb, sys, header, common_methods
cgitb.enable()

sys.path.append('/var/nasexe/storage')
import storage_op
import sys,os
from lvm_infos import *
from functions import *
import san_disk_funs


check_fc =''
target_del = ''

start_fc_chk = ''

check_fc = san_disk_funs.fc_target_status();

#------------------------- Enable Fc Target-------------------------
if(header.form.getvalue('enable_butt')):
        fc_target_name= header.form.getvalue('enable_tar_name')
        if(fc_target_name == None):
                print
        else:

                enable_status=san_disk_funs.fc_enable_disable(targets=fc_target_name, opp='ENABLE')
                #print 'Single:'+str(enable_status)
                if(enable_status == True):
                        print"""<div id = 'id_trace'>"""
                        print " <font color='darkred'></b></font> You have Successfully Enabled the Target!"
                        print "</div>"
                        #print "<script>location.href = 'main.py?page=fc&act=create_target_done';</script>"
                        print "<script>location.href = 'main.py?page=fc_tar#tabs-1';</script>";
                else:
			print"""<div id = 'id_trace_err'>"""

                        print "Error occured while enable the Target!"
                        print "</div>"
                        print "<script>location.href = 'main.py?page=fc_tar#tabs-1';</script>";
                        #print "<script>location.href = 'main.py?page=fc&act=create_target_done';</script>"

#-------------------------------------End------------------------------------------------------------

#---------------------------------- Disable FC-----------------------   
if(header.form.getvalue('disable_target')):
        fc_disable_name = header.form.getvalue('disable_target_name')
        chk_used_disk = san_disk_funs.fc_used_disks_tgt(fc_disable_name)

        check_ini_list =san_disk_funs.fc_ini_list(fc_disable_name)

        if(len(check_ini_list) > 0):
                print"""<div id = 'id_trace_err'>"""
                print "Error occured while Disable! Target contains initiator(s)"
                print "</div>"
                #print "<script>location.href = 'main.py?page=fc&act=disable_target_done';</script>"
                print "<script>location.href = 'main.py?page=fc_tar#tabs-2';</script>";

        elif(len(chk_used_disk) > 0):
                print"""<div id = 'id_trace_err'>"""
                print "Error occured while Disable! Target contains disk(s)"
                print "</div>"
                print "<script>location.href = 'main.py?page=fc_tar#tabs-2';</script>";
        else:
        #print fc_disable_name
                if(fc_disable_name == None):
                        print

                else:
                        disable_status = san_disk_funs.fc_enable_disable(fc_disable_name,opp='DISABLE')
                        if(disable_status == True):
                                print"""<div id = 'id_trace'>"""
                                print " <font color='darkred'></b></font> You have Successfully Disabled the Target!"
                                print "</div>"
                                #print "<script>location.href = 'main.py?page=fc&act=disable_target_done';</script>"
                                print "<script>location.href = 'main.py?page=fc_tar#tabs-2';</script>";

                        else:
                                print"""<div id = 'id_trace_err'>"""
                                print "Error occured while Disabled the Target!"
                                print "</div>"
                                #print "<script>location.href = 'main.py?page=fc&act=disable_target_done';</script>"
                                print "<script>location.href = 'main.py?page=fc_tar#tabs-2';</script>";



#------------------------------------------------------End--------------------------------------------------

import left_nav
if (check_fc !=[]):
	print
	print """
	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer">
		<div class="insidepage-heading">Fc >> <span class="content">Fc Configuration</span></div>
		<!--tab srt-->
		<div class="searchresult-container">
		  <div class="infoheader">
		    <div id="tabs">
		      <ul>
			<li><a href="#tabs-1">Enable Target</a></li>
			<li><a href="#tabs-2">Disable Target</a></li>
		      </ul>
		      <div id="tabs-1">

		<!--form container starts here-->
		<div class="form-container">
		  <div class="topinputwrap-heading">Enable </div>
		  <div class="inputwrap">
		    <div class="formrightside-content">
		   <form name = 'enable_fc' method = 'post'>
		   <table width = "685" border = "0" cellspacing = "0" cellpadding = "0">
			 <tr>
									<td width = '19%' class = "table_heading" height = "35px" valign = "middle">
										Select Target
									</td>"""
	print"""
							<td class = "table_content" height = "35px" valign = "middle">
	<div class="styled-select2" style="width:332px;">
	<select class = 'input' name = 'enable_tar_name' style="width:104%;">
	<option value = ''>Select target</option>"""
	if (check_fc != [{}]):
		for x in check_fc:
			if (str(x).find("'0'") > 0):
				x = str(x).replace('{', '');
				x = str(x).replace('}', '');
				x = str(x).replace('\'', '');
				x = x[:x.rfind(':')];
				print """<option value = '"""+str(x)+"""'>"""+str(x)+"""</option>"""
	print"""</select></div></td></tr>"""


	print"""				<tr><td>

	<div>
	<td style="float: right;">
	<button class = 'buttonClass' type="submit" name = 'enable_butt' value = 'Create target' onclick = 'return validate_enable_fc();'>Enable Target</button></td>
	</div>
	</td>

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
		  <div class="topinputwrap-heading">Select Target to Delete</div>
		  <div class="inputwrap">
		<div class="formrightside-content">
		   <form name = 'disable_fc' method = 'POST'>"""

	print"""<table width = "685" border = "0" cellspacing = "0" cellpadding = "0">

										<tr>
										<td width = '23%' class = "table_heading" height = "35px" valign = "middle">
											Select target
										</td>
										<td class = "table_content" height = "35px" valign = "middle">
		<div class="styled-select2" style="width:279px;">
		<select class = 'input' name = 'disable_target_name' style = 'width: 104%;'>
		<option value=''>Select Target</option>"""

	#-------------------FC disabale-------------------
	if (check_fc != [{}]):
		for x in check_fc:
			if (str(x).find("'1'") > 0):
				x = str(x).replace('{', '');
				x = str(x).replace('}', '');
				x = str(x).replace('\'', '');
				x = x[:x.rfind(':')];
				print """<option value = '"""+str(x)+"""'>"""+str(x)+"""</option>"""
	
	print"""</select></div></td></tr>"""


	print"""
		<tr>
		<td>
		<div>
		<td style= "float:right;">
	<button class = 'buttonClass' type="submit" name = 'disable_target' value = 'Delete Selected' onclick = 'return validate_disable_fc();'>Disable Target</button>
	</td>
	</div>
	</td>
	</tr>
	</table></form>

		  </div>
	</div>
	</div></div>
	<!--form container ends here-->
	<p>&nbsp;</p>
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
else:
	print "<div style = 'margin-left: auto; margin-right: auto; text-align: center; vertical-align: center; color: darkred; width: 65%; font: 16px Arial;'><br/><br/><br/><b>Check the 'Enable/Disable FC' option in Maintenance -></b><a href= 'main.py?page=sr'><span style='text-decoration:underline;'>Services</span></a>.</div>"

print"""
<!--body wrapper end-->
</body>
</html>
"""
