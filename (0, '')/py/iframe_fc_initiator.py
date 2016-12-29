#!/usr/bin/python
import cgitb, sys,  common_methods, include_files, cgi
cgitb.enable()

sys.path.append('/var/nasexe/storage')
import storage_op
import sys,os
from lvm_infos import *
from functions import *
import san_disk_funs

form = cgi.FieldStorage()

target_name = form.getvalue("target")
list_fc_target = [target_name]

check_fc = san_disk_funs.fc_target_status();
fc_target=san_disk_funs.fc_list_targets()

assign_disk_name = ''
get_target = ''
finaldisk = ''
rm_target = ''
initiator_name = ''
initiator_del_name = ''
initiator_list = ''
delete_assign_disk_name = ''
session_check = ''
show_target_ini = ''
#------------Add Initiator---------------------------
if(form.getvalue('fc_ini_but')):
	initiator_name = form.getvalue('list_targets')
	target_name =initiator_name.strip() 
	#print initiator_name
	add_ini = form.getvalue('all_portal')
	#print add_ini
	get_ini_array = [];
	gets_initiator_list = san_disk_funs.fc_ini_list(initiator_name)
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

		initiator_status=san_disk_funs.fc_ini_add(initiator_name,add_ini)
	#print initiator_status
		if(initiator_status == True):
			print"""<div id = 'id_trace'>"""
			print "Successfully Added the Initiator!"
			print "</div>"
			print "<script>location.href = 'iframe_fc_initiator.py?target="+target_name+"#tabs-1';</script>"


			#print "<script>location.href = 'main.py?page=fc&act=add_ini_done';</script>"
		else:
			print"""<div id = 'id_trace_err'>"""
			print "Error occured while Adding !"
			print "</div>"
			print "<script>location.href = 'iframe_fc_initiator.py?target="+target_name+"#tabs-1';</script>"



#---------------------------FC DELETE Initiator-------------------------------
'''
if(form.getvalue('choose_list')):
	initiator_del_name = form.getvalue('choose_list')
	#print "<script>location.href = 'main.py?page=fc_ini#tabs-2';</script>"
#print "<script>location.href = 'main.py?page=fc&act=del_ini_done';</script>"
	initiator_list = san_disk_funs.fc_ini_list(initiator_del_name)

#print initiator_list
#for i in initiator_list:
#       print i
if(form.getvalue('delete_initiator')):
	show_target_ini = form.getvalue('choose_list')
#print 'Targ:'+str(show_target_ini)
#print '<br/>`'
	initiator_name = form.getvalue('initr_list')
#print initiator_name
#print initiator_del_status
#check_used_disk = san_disk_funs.fc_used_disks_tgt(show_target_ini)    
	session_check=san_disk_funs.fc_session(show_target_ini)
if(len(session_check) > 0):
	initiator_del_status=san_disk_funs.fc_ini_del(show_target_ini,initiator_name)

	print"""<div id = 'id_trace'>"""
	print "Successfully Deleted the Initiator!"
	print "</div>"

	print "<script>jAlert('Initiator is Deleted But the Session is Active.After reboot the Fs2 or client machine then it is deactivated');</script>"

else:
	#print"""<div id = 'id_trace_err'>"""
	#print "Disks exist in this target. Could not delete initiator !"
	#print "</div>"
	#else:

	initiator_del_status=san_disk_funs.fc_ini_del(show_target_ini,initiator_name)
	if(initiator_del_status == True):

		print"""<div id = 'id_trace'>"""
		print "Successfully Deleted the Initiator!"
		print "</div>"
		#print "<script>location.href = 'main.py?page=fc_ini#tabs-2';</script>"
	else:
		print"""<div id = 'id_trace_err'>"""
		print "Error occured while Deleting !"
		print "</div>"
		#print "<script>location.href = 'main.py?page=fc_ini#tabs-2';</script>"

'''


if(form.getvalue('choose_list')):
	initiator_del_name = form.getvalue('choose_list')
	target_name = initiator_del_name.strip()
	#print "<script>location.href = 'main.py?page=fc&act=del_ini_done';</script>"
	print "<script>location.href = 'iframe_fc_initiator.py?target="+target_name+"#tabs-2';</script>"
	initiator_list = san_disk_funs.fc_ini_list(initiator_del_name)
	

	#print initiator_list
	#for i in initiator_list:
	#       print i
if(form.getvalue('delete_initiator')):
	show_target_ini = form.getvalue('choose_list')
	target_name = show_target_ini.strip()
	#print 'Targ:'+str(show_target_ini)
	#print '<br/>`'
	initiator_name = form.getvalue('initr_list')
	#print initiator_name
	#print initiator_del_status
	#check_used_disk = san_disk_funs.fc_used_disks_tgt(show_target_ini)     
	session_check=san_disk_funs.fc_session(show_target_ini)
	if(len(session_check) > 0):
		initiator_del_status=san_disk_funs.fc_ini_del(show_target_ini,initiator_name)

		print"""<div id = 'id_trace'>"""
		print "Successfully Deleted the Initiator!"
		print "</div>"
		

		print "<script>jAlert('Initiator is Deleted But the Session is Active.After reboot the Fs2 or client machine then it is deactivated');</script>"
	else:
		initiator_del_status=san_disk_funs.fc_ini_del(show_target_ini,initiator_name)
		if(initiator_del_status == True):

			print"""<div id = 'id_trace'>"""
			print "Successfully Deleted the Initiator!"
			print "</div>"
			print "<script>location.href = 'iframe_fc_initiator.py?target="+target_name+"#tabs-2';</script>"
		else:
			print"""<div id = 'id_trace_err'>"""
			print "Error occured while Deleting !"
			print "</div>"
			print "<script>location.href = 'iframe_fc_initiator.py?target="+target_name+"#tabs-2';</script>"

#import left_nav

#if (str(check_srp).find("'1'") > 0):
if (check_fc !=[]):
	print
	print """
	<!--Right side body content starts from here-->
	<div class="rightsidecontainer" style="margin:0;width:716px;padding-left:0px;">
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
	  <div class="inputwrap">
	<div class="formrightside-content">
	   <form name = 'add_fc_ini' method = 'POST'>"""

	print"""<table width = "685" border = "0" cellspacing = "0" cellpadding = "0">
										<tr>
										<td width = '23%' height = "35px" valign = "middle">
											Select target
										</td>
										<td height = "35px" valign = "middle">
			<div class="styled-select2" style="width:207px;">
			<select name = 'list_targets'>
			<option value='list_ini_val'>Select Target</option>"""
	if (list_fc_target!= []):
		for initiator_target in list_fc_target:
			#print x
			print """<option value = '"""+str(initiator_target)+"""'"""
			if(initiator_name!=''):
				if(initiator_name == initiator_target):
					print """ selected"""
			print """>"""+str(initiator_target)+"""</option>"""

	print"""</select></div>
	</td>
	</tr>"""

	print"""
		 <tr>
						<td width = '30%' class = "table_heading" height = "35px" valign = "middle">
							Enter initiator name
						</td>
						<td class = "table_content" height = "35px" valign = "middle">
							<input id = 'id_add_props' class = 'textbox' type = 'text' name = 'all_portal'  style="width: 207px;">
						</td>
					</tr>

					</td>
					</tr>


		"""
	print"""	<tr>
		<td>
		<div>
		<td style= "float:right;">
	<button class = 'buttonClass' type="submit" name = 'fc_ini_but' value = 'Apply' onclick ='return validate_fc_add_initiator();'>Apply</button>


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
		  <div class="inputwrap">
		    <div class="formrightside-content">
		    <form name = 'fc_ini_delete' method = 'POST'>
			<table width = "685" border = "0" cellspacing = "0" cellpadding = "0">

			 <tr>
											<td width = '23%' class = "table_heading" height = "35px" valign = "middle">
												Select target
											</td>
											<td class = "table_content" height = "35px" valign = "middle">
			<div class="styled-select2" style="width:210px;">
			<select class = 'input' name = 'choose_list' onchange='this.form.submit()'>
			<option value = 'choose_list_val'>Select Target</option>"""
	if (list_fc_target != []):
		for initiator_del_target in list_fc_target:
			#print x
			print """<option value = '"""+str(initiator_del_target)+"""'"""
			if(initiator_del_name!=''):
				if(initiator_del_name == initiator_del_target):
					print """ selected"""
			print """>"""+str(initiator_del_target)+"""</option>"""
	print"""</select></div>
		</td>
		</tr>"""


	print"""
									<tr>
										<td width = '23%' class = "table_heading" height = "35px" valign = "middle">
											Choose initiator
										</td>"""

	print"""                                                                        <td class = "table_content" height = "35px" valign = "middle">
		<div class="styled-select2" style="width:208px;">
		<select class = 'input' name = 'initr_list' style = 'width:106%;'>
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

	<button class = 'buttonClass' type="submit" name = 'delete_initiator' value = 'Remove initiator' onclick ='return validate_fc_remove_ini();'>Remove</button>

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
	</div>"""

else:
	print "<div style = 'margin-left: auto; margin-right: auto; text-align: center; vertical-align: center; color: darkred; width: 65%; font: 16px Arial;'><br/><br/><br/><b>Check the 'Enable/Disable FC' option in Maintenance -></b><a href= 'main.py?page=sr'><span style='text-decoration:underline;'>Services</span></a>.</div>"
print"""
"""
