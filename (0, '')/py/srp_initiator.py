#!/usr/bin/python
import cgitb, sys, header, common_methods
cgitb.enable()

sys.path.append('/var/nasexe/storage')
import storage_op
import sys,os
from lvm_infos import *
from functions import *
import san_disk_funs

check_srp = san_disk_funs.ib_target_status();
srp_target=san_disk_funs.ib_list_targets()

assign_disk_name = ''
get_target = ''
finaldisk = ''
rm_target = ''
initiator_name = ''
initiator_del_name = ''
initiator_list = ''
delete_assign_disk_name = ''


###############Add Initiator###########################
if(header.form.getvalue('srp_ini_but')):
	initiator_name = header.form.getvalue('list_targets')
	#print initiator_name
	add_ini = header.form.getvalue('all_portal')
	#print add_ini
	get_ini_array = [];
	gets_initiator_list = san_disk_funs.ib_ini_list(initiator_name)
	#print gets_initiator_list
	for l in gets_initiator_list:
		#print 'L'+str(l)
		get_ini1 = str(l)

		get_ini2 = get_ini1.replace('\'', '')
		get_ini3 =get_ini2.replace('[', '')
		get_ini4 =get_ini3.replace(']', '')
		get_ini_array.append(get_ini4+initiator_name);
		#print get_ini_array
		#print '<br/>'
	test_ini = add_ini + initiator_name;
	test_ini = test_ini.strip();
	#print test_ini
	if(test_ini in get_ini_array):
		#print 'True'
		#print 'Error'

		print"""<div id = 'id_trace_err'>"""
		print "Duplicate Entry not be allowed!"
		print "</div>"

	else:

		initiator_status=san_disk_funs.ib_ini_add(initiator_name,add_ini)
	#print initiator_status
		if(initiator_status == True):
			print"""<div id = 'id_trace'>"""
			print "Successfully Added the Initiator!"
			print "</div>"
			print "<script>location.href = 'main.py?page=ini_srp#tabs-1';</script>"


			#print "<script>location.href = 'main.py?page=srp&act=add_ini_done';</script>"
		else:
			print"""<div id = 'id_trace_err'>"""
			print "Error occured while Adding !"
			print "</div>"
			print "<script>location.href = 'main.py?page=ini_srp#tabs-1';</script>"



###### Srp DELETE Initiator #################
if(header.form.getvalue('choose_list')):
	initiator_del_name = header.form.getvalue('choose_list')
	print "<script>location.href = 'main.py?page=ini_srp#tabs-2';</script>"
	#print "<script>location.href = 'main.py?page=srp&act=del_ini_done';</script>"
	initiator_list = san_disk_funs.ib_ini_list(initiator_del_name)

	#print initiator_list
	#for i in initiator_list:
	#       print i
if(header.form.getvalue('delete_initiator')):
	show_target_ini = header.form.getvalue('choose_list')
	#print 'Targ:'+str(show_target_ini)
	#print '<br/>`'
	initiator_name = header.form.getvalue('initr_list')
	#print initiator_name
	#print initiator_del_status
	#check_used_disk = san_disk_funs.srp_used_disks_tgt(show_target_ini)    
	session_check=san_disk_funs.ib_session(show_target_ini)
	if(len(session_check) > 0):
		initiator_del_status=san_disk_funs.ib_ini_del(show_target_ini,initiator_name)

		print"""<div id = 'id_trace'>"""
		print "Successfully Deleted the Initiator!"
		print "</div>"

		print "<script>jAlert('Initiator is Deleted But the Session is Active.After reboot the Fs2 or client machine then it is deactivated');</script>"

	else:
                #print"""<div id = 'id_trace_err'>"""
                #print "Disks exist in this target. Could not delete initiator !"
                #print "</div>"
                #else:

		initiator_del_status=san_disk_funs.ib_ini_del(show_target_ini,initiator_name)
		if(initiator_del_status == True):

			print"""<div id = 'id_trace'>"""
			print "Successfully Deleted the Initiator!"
			print "</div>"
			print "<script>location.href = 'main.py?page=ini_srp#tabs-2';</script>"
		else:
			print"""<div id = 'id_trace_err'>"""
			print "Error occured while Deleting !"
			print "</div>"
			print "<script>location.href = 'main.py?page=ini_srp#tabs-2';</script>"

import left_nav

if (str(check_srp).find("'1'") > 0):
	print
	print """
	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer">
		<div class="insidepage-heading">Srp >> <span class="content">Srp Configuration</span></div>
		<!--tab srt-->
		<div class="searchresult-container">
		  <div class="infoheader">
		    <div id="tabs">
		      <ul>
			<li><a href="#tabs-1">Add Initiator</a></li>
			<li><a href="#tabs-2">Delete Initiator</a></li>
		      </ul>
		  <div id="tabs-1">
		<!--form container starts here-->
		<div class="form-container">
		  <div class="topinputwrap-heading">Add Disk To Target</div>
		  <div class="inputwrap">
		<div class="formrightside-content">
		   <form name = 'add_srp_ini' method = 'POST'>"""

	print"""<table width = "685" border = "0" cellspacing = "0" cellpadding = "0">
										<tr>
										<td width = '23%' height = "35px" valign = "middle">
											Select target
										</td>
										<td height = "35px" valign = "middle">
			<div class="styled-select2" style="width:332px;">
			<select name = 'list_targets' style="width: 346px;">
			<option value='list_ini_val'>Select Target</option>"""
	if (srp_target != [{}]):
		for initiator_target in srp_target:
			#print x
			print """<option value = '"""+initiator_target+"""'"""
			if(initiator_name!=''):
				if(initiator_name == initiator_target):
					print """ selected"""
			print """>"""+initiator_target+"""</option>"""


	print"""</select></div>
	</td>
	</tr>"""

	print"""
		 <tr>
                                                <td width = '30%' class = "table_heading" height = "35px" valign = "middle">
                                                        Enter initiator name
                                                </td>
                                                <td class = "table_content" height = "35px" valign = "middle">
                                                        <input id = 'id_add_props' class = 'input' type = 'text' name = 'all_portal'>
                                                </td>
                                        </tr>

                                        </td>
                                        </tr>


		"""
	print"""	<tr>
		<td>
		<div>
		<td style= "float:right;">
	<button class = 'buttonClass' type="submit" name = 'srp_ini_but' value = 'Apply' onclick ='return validate_srp_add_initiator();'>Apply</button>


	</td>
	</div>
	</td>
	</tr>
	</table></form>

		  </div>"""

	print """
		</div>
		</div>
		<!--form container ends here-->
		<p>&nbsp;</p>
		      </div>

		<div id="tabs-2">

		<!--form container starts here-->
		<div class="form-container">
		  <div class="topinputwrap-heading">Delete Disk To Target </div>
		  <div class="inputwrap">
		    <div class="formrightside-content">
		    <form name = 'srp_ini_delete' method = 'POST'>
			<table width = "685" border = "0" cellspacing = "0" cellpadding = "0">

			 <tr>
											<td width = '23%' class = "table_heading" height = "35px" valign = "middle">
												Select target
											</td>
											<td class = "table_content" height = "35px" valign = "middle">
			<div class="styled-select2" style="width:332px;">
			<select class = 'input' name = 'choose_list' onchange='this.form.submit()' style="width:448px;">
			<option value = 'choose_list_val'>Select Target</option>"""
	if (srp_target != [{}]):
		for initiator_del_target in srp_target:
			#print x
			print """<option value = '"""+initiator_del_target+"""'"""
			if(initiator_del_name!=''):
				if(initiator_del_name == initiator_del_target):
					print """ selected"""
			print """>"""+initiator_del_target+"""</option>"""

                print"""</select></div>
                </td>
                </tr>"""


	print"""
                                                                        <tr>
                                                                                <td width = '23%' class = "table_heading" height = "35px" valign = "middle">
                                                                                        Choose initiator
                                                                                </td>"""
	
	print"""                                                                        <td class = "table_content" height = "35px" valign = "middle">
		<div class="styled-select2" style="width:332px;">
                <select class = 'input' name = 'initr_list' style = 'width:348px;'>
                <option value = 'initr_list_val'>Select Initiator</option>"""
	
	for ini_list in initiator_list:
		print """<option value = '"""+ini_list+"""'>"""+ini_list+"""</option>"""                 



	print"""</select></div>
	</td>
	</tr>"""



	print"""</select>"""
	print"""</td>
	</tr>"""

	print"""	
	<tr>
	<td>
	<Div>
	<td style= "float:right;">

	<button class = 'buttonClass' type="submit" name = 'delete_initiator' value = 'Remove initiator' onclick ='return validate_srp_remove_ini();'>Remove Initiator</button>

	</td>
	</Div>
	</td>
	</tr>

			</table>
				</form>
		   </div>
		  </div>
		</div>
		<!--form container ends here-->
		<p>&nbsp;</p>
		      </div></div>

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
	print "<div style = 'margin-left: auto; margin-right: auto; text-align: center; vertical-align: center; color: darkred; width: 65%; font: 16px Arial;'><br/><br/><br/><b>Check the 'Enable/Disable SRP' option in Maintenance--></b><a href ='main.py?page=sr'style ='text-decoration:underline;'>Services</a>.</div>"
print"""
<!--body wrapper end-->
</body>
</html>
"""
