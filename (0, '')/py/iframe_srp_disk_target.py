#!/usr/bin/python
import cgitb, sys, include_files, common_methods, cgi
cgitb.enable()

form = cgi.FieldStorage()
sys.path.append('/var/nasexe/storage')
import storage_op
import sys,os
from lvm_infos import *
from functions import *
import san_disk_funs

target_name = form.getvalue("target")
list_srp_target = [target_name]
srp_target=san_disk_funs.ib_list_targets()

check_srp = san_disk_funs.ib_target_status();

assign_disk_name = ''
get_target = ''
finaldisk = ''
rm_target = ''

delete_assign_disk_name = ''
luns_array=[];
free_opt = range(0, 16)
lun_ar = []

for k in free_opt:
	#print k
	#l = str(k)
	lun_ar.append(k)
lun_array = [];
	


#for i in range(0, 16):
#       lun_array.append(i);

#print random_target
#print '<br/>'
disk=san_disk_funs.list_all_disk()
#for i in disk.keys():
#       print str(disk[i])
	#print str(i)
#print 'Disk:'+str(disk)

biodisk = disk['BIO'];
fiodisk = disk['FIO'];

#luns =['free_luns']
#print luns
alldisk = [];


for i in biodisk:
	alldisk.append(i);

for j in fiodisk:
	alldisk.append(j);

display_optn_one = ''
display_optn_two = ''
display_del_optn= ''
display_optn_one = 'none'
display_optn_two = 'none'
display_del_optn = 'none'
display_del_optn1= 'none'
free_luns = [];
avail_luns = [];

iscsi_status = ''


used_disk_list = san_disk_funs.ib_used_disks()



#----------------------Add Disk-------------------------------------------------

#---------------ASSIGN Srp DISK--------------------------------------------------
if(form.getvalue('assign_disk_nm')):
	assign_disk_name = form.getvalue('assign_disk_nm')
	target_name = assign_disk_name.strip()
	print "<script>location.href = 'iframe_srp_disk_target.py?target="+target_name+"#tabs-1';</script>"
	#print assign_disk_name
	display_optn_one = 'block'
	display_optn_two = 'block'
	#used_disks_array = [];
	used_disks_name = san_disk_funs.ib_used_disks_tgt(assign_disk_name)
	finaldisk = list(set(alldisk) - set(used_disks_name));
	free_luns = san_disk_funs.ib_luns(assign_disk_name)
	free_luns = map(int, free_luns)
	avail_luns = list(set(lun_ar) - set(free_luns));
if(form.getvalue('add_disk_action')):
	assign_disk_names = form.getvalue('assign_disk_nm')
	target_name = assign_disk_names.strip()
	#print assign_disk_names
	disk_assign = form.getvalue('select_disk')
	#print disk_assign
	#print '<br>'
	lun_assign = form.getvalue('select_lun')
	#print lun_assign
	used_disks_array = [];
	used_disks_name = san_disk_funs.ib_used_disks_tgt(assign_disk_names)
	if(len(used_disks_name) == 0):

		print """<script>jAlert('This is the first disk... So assigning lun 0!');</script>"""
		lun_assign = 0

	target_assign_to_disk = san_disk_funs.ib_add_disks_tgt(assign_disk_names,lun_assign,disk_assign)
	#san_disk_funs.srp_add_disks_tgt(t_name,disk_lun,disk)
	#print target_assign_to_disk
	if((target_assign_to_disk) == True):

		print"""<div id = 'id_trace'>"""
		print "Disk Assigned!"
		print "</div>"
		print "<script>location.href = 'iframe_srp_disk_target.py?target="+target_name+"#tabs-1';</script>"
		#print "<script>location.href = 'main.py?page=p&act=assign_target_done';</script>"
	else:
		print"""<div id = 'id_trace_err'>"""
		print "Error occured while  assigned to disk!"
		print "</div>"
		print "<script>location.href = 'iframe_srp_disk_target.py?target="+target_name+"#tabs-1';</script>"

#---------------------------------End------------------------------------------
#----------------------------Delete Disk-----------------------------------------

#---------------------------------- SRP Delete disk from Target ----------------------------------
if(form.getvalue('delete_target_name')):
	delete_assign_disk_name = form.getvalue('delete_target_name')
	#print delete_assign_disk_name
	print "<script>location.href = 'iframe_srp_disk_target.py?target="+target_name+"#tabs-2';</script>"
	target_name = delete_assign_disk_name.strip()
	display_del_optn = 'block'
	display_del_optn1= 'block'

	used_disk_list = san_disk_funs.ib_used_disks_tgt(delete_assign_disk_name)
	#print used_disk_list
if(form.getvalue('remove_disk')):
	delete_assign_target = form.getvalue('delete_target_name')
	target_name = delete_assign_target.strip()
	#print delete_assign_target
	disk_name_rm  = form.getvalue('select_disk_remove')

	check_init_list =san_disk_funs.ib_ini_list(delete_assign_target)
	#print 'Get INI:'+str(check_init_list)
	#exit();

	if(len(check_init_list) > 0):
		print"""<div id = 'id_trace_err'>"""
		print "First Remove the Initiators From the Target"
		print "</div>"
		#print "<script>location.href = 'main.py?page=srp&act=delete_target_done';</script>"
		print "<script>location.href = 'iframe_srp_disk_target.py?target="+target_name+"#tabs-2';</script>"

	else:
		get_nw_lun = common_methods.get_lun_number(delete_assign_target, disk_name_rm)
		#print get_nw_lun
		delete_disk_status = san_disk_funs.ib_rem_disks_tgt(delete_assign_target,get_nw_lun)
		if(delete_disk_status == True):
			print"""<div id = 'id_trace'>"""
			print "Disk Remove Successfully  !"
			print "</div>"
			print "<script>location.href = 'iframe_srp_disk_target.py?target="+target_name+"#tabs-2';</script>"
			#print "<script>location.href = 'main.py?page=srp&act=delete_disk_done';</script>"
		else:
			print"""<div id = 'id_trace_err'>"""
			print "Error occured while Deleating the disk!"
			print "</div>"
			print "<script>location.href = 'iframe_srp_disk_target.py?target="+target_name+"#tabs-2';</script>"
#import left_nav
if (check_srp !=[]):
	print
	print """
	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer" style="margin:0;width:716px;padding-left:0px;">
		<!--tab srt-->
		<div class="searchresult-container">
		  <div class="infoheader">
		    <div id="tabs">
		      <ul>
			<li><a href="#tabs-1">Add Disk</a></li>
			<li><a href="#tabs-2">Delete Disk </a></li>
		      </ul>
		  <div id="tabs-1">
		<!--form container starts here-->
		<div class="form-container">
		  <!--<div class="topinputwrap-heading">Add Disk To Target</div>-->
		  <div class="inputwrap">
		<div class="formrightside-content">
		   <form name = 'add_disk_to_srp_target' method = 'POST'>"""

	print"""<table width = "685" border = "0" cellspacing = "0" cellpadding = "0">
										<tr>
										<td width = '23%' height = "35px" valign = "middle">
											Select target
										</td>
										<td height = "35px" valign = "middle">
			<div class="styled-select2" style="width:207px;">
			<select name = 'assign_disk_nm' onchange='this.form.submit()'>
			<option value='assign_tar'>Select Target</option>"""
	if (list_srp_target != []):
		for assign_disk in list_srp_target:
			#print x
			print """<option value = '"""+str(assign_disk)+"""'"""
			if(assign_disk_name!=''):
				if(assign_disk_name == assign_disk):
					print """ selected"""
			print """>"""+str(assign_disk)+"""</option>"""
			#print """>"""+x['target']+"""</option>"""
		#for x in select_targets:
			#print x
			#display_create = 'none'

	print"""</select></div>
	</td>
	</tr>"""

	print"""


		<tr id = 'optn_one' style = 'display:"""+display_optn_one+""";'>
					<td width = "158" height = "40px" valign = "middle" style="float: left;">
					Select Disk:
					</td>
					<td width = "311" height = "40px" valign = "middle">
			<div class="styled-select2" style="width:131px;">
			<select name = 'select_disk'>
			<option value = 'select_dis_val'>Select Disk</option>"""
	if(finaldisk != ''):
		for disk_info in finaldisk:
			print """<option value = '"""+disk_info+"""'>"""+disk_info+"""</option>"""
	print """</select></div>
			</td>
			</tr>"""
	print"""                <tr id = 'optn_two' style = 'display:"""+display_optn_two+""";'>
					<td width = "158" height = "40px" valign = "middle" style="float: left;">
					Select Lun:
					</td>
					<td width = "311" height = "40px" valign = "middle">
			<div class="styled-select2" style="width:131px;">
			<select name = 'select_lun'>
			<option value = 'select_lun_val'>Select Lun</option>"""

	for lun_value in avail_luns:
		print """<option value = '""" +str(lun_value) + """'>""" +str(lun_value) + """</option>"""

		#for luns in lun_array:

		#except Exception as e:
	print """                </select></div>
					</td>
			</tr>"""
	print"""	<tr>
		<td>
		<div>
		<td style= "float:right;">
	<button class = 'buttonClass' type="submit" name = 'add_disk_action' value = 'Apply' onclick ='return validate_srp_assign_target();'>Add Disk</button>


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
		  <!--<div class="topinputwrap-heading">Delete Disk To Target </div>-->
		  <div class="inputwrap">
		    <div class="formrightside-content">
		    <form name = 'del_disk_from_srp_target' method = 'POST'>
			<table width = "685" border = "0" cellspacing = "0" cellpadding = "0">

			 <tr>
											<td width = '23%' class = "table_heading" height = "35px" valign = "middle">
												Select target
											</td>
											<td class = "table_content" height = "35px" valign = "middle">
			 <div class="styled-select2" style="width:207px;">
			<select class = 'input' name = 'delete_target_name' onchange='this.form.submit()' style="width:448px;">
			<option value = 'del_assign_tar'>Select Target</option>"""
	if (list_srp_target != []):
		for delete_assign_disk in list_srp_target:
			#print x
			print """<option value = '"""+str(delete_assign_disk)+"""'"""
			if(delete_assign_disk_name!=''):
				if(delete_assign_disk_name == delete_assign_disk):
					print """ selected"""
			print """>"""+str(delete_assign_disk)+"""</option>"""

	print"""</select></div>"""
	print"""</td>
	</tr>"""


	print"""
			<tr id = 'optn_del_one' style = 'display:"""+display_del_optn+""";'>
			<td width = "200" class = "table_heading" height = "40px" valign = "middle" bgcolor = "#f5f5f5" style = 'float:left;'>
			<B>Select Disk:</B>
			</td>
			<td width = "311" class = "table_content" height = "40px" valign = "middle" bgcolor = "#f5f5f5" >
			 <div class="styled-select2" style="width:131px;">
			<select name = 'select_disk_remove'>
			<option value = 'disk_del_op'>Select Disk</option>"""
	if(used_disk_list!= ''):
		
		for used_disks in used_disk_list:


			print"""<option value = '"""+str(used_disks)+"""'>"""+str(used_disks)+"""</option>"""
	print"""</select></div>
		</td></tr>"""


			
	print"""	
	<tr>
	<td>
	<Div>
	<td style= "float:right;">

	<button class = 'buttonClass' type="submit" name = 'remove_disk' value = 'Remove selected disk' onclick ='return validate_del_srp_assign_target();'>Delete Disk</button>


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
	print "<div style = 'margin-left: auto; margin-right: auto; text-align: center; vertical-align: center; color: darkred; width: 65%; font: 16px Arial;'><br/><br/><br/><b>Check the 'Enable/Disable SRP' option in Maintenance -></b><a href= 'main.py?page=sr'><span style='text-decoration:underline;'>Services</span></a>.</div>"
print"""
"""
