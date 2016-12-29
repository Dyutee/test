#!/usr/bin/python
import cgitb, sys,  common_methods, cgi, include_files, os
cgitb.enable()

sys.path.append('/var/nasexe/python/')
import tools
from tools import db

sys.path.append('/var/nasexe/storage')
import storage_op
import sys,os
from lvm_infos import *
from functions import *
import san_disk_funs

form = cgi.FieldStorage()

iscsi_status = common_methods.get_iscsi_status();
get_target = ''
finaldisk = ''
rm_target = ''
luns_array=[];
free_opt = range(0, 16)
lun_ar = []
db_lun_ar = []

for k in free_opt:
	#print k
	#l = str(k)
	lun_ar.append(k)
lun_array = [];
	


#for i in range(0, 16):
#       lun_array.append(i);

random_target=san_disk_funs.get_iscsi_target_name()
#print random_target
#print '<br/>'
disk=san_disk_funs.list_all_disk()
#for i in disk.keys():
#       print str(disk[i])
	#print str(i)
#print 'Disk:'+str(disk)

querystring = os.environ['QUERY_STRING'];
target_name = form.getvalue("target")
tar_arr_n =[]
list_target_name = [target_name]

#for h in get_all_lun:
#	lun_db_from = h['lun']
#	db_lun_ar.append(lun_db_from)
#-------------End---------------------
biodisk = disk['BIO'];
fiodisk = disk['FIO'];

#luns =['free_luns']
#print luns
alldisk = [];


for i in biodisk:
	alldisk.append(i);

for j in fiodisk:
	alldisk.append(j);

display_optn_one = 'none'
display_optn_two = 'none'
display_del_optn = 'none'
display_del_optn1= 'none'
free_luns = [];
avail_luns = [];




used_disk_list = san_disk_funs.iscsi_used_disks()
#print used_disk_list
random_target=san_disk_funs.get_iscsi_target_name()
#print 'Content-Type: text/html'
remove_targets_list= san_disk_funs.iscsi_list_all_tgt()


select_targets=san_disk_funs.iscsi_list_all_tgt_att()

#----------------Add Disk--------------------------
#new_targt_new = form.getvalue("target")
#rint new_targt_new
if(form.getvalue('target_for_disk')):
	get_target = form.getvalue('target_for_disk')
	target_name = get_target.strip()
	print "<script>location.href = 'iframe_iscsi_disk_target.py?target="+target_name+"#tabs-1';</script>"
	#print "<script>location.href = 'main.py?page=iscsi&act=assign_target_done';</script>"
	display_optn_one = 'block'
	display_optn_two = 'block'
	get_luns_name   = form.getvalue('select_lun')
	used_disks_array = [];
	used_disks_name = san_disk_funs.iscsi_used_disks_tgt(target_name);
	finaldisk = list(set(alldisk) - set(used_disks_name));
	free_luns = san_disk_funs.iscsi_luns(get_target)
	free_luns = map(int, free_luns)
	avail_luns = list(set(lun_ar) - set(free_luns));


if(form.getvalue('add_disk')):
	get_target_name= form.getvalue('target_for_disk')
	target_name = get_target_name.strip()

	display_assign_disk = 'block';
	#print 'TNAMe:'+str(get_target_name)
	#print '<br/>'
	get_disk_name = form.getvalue('select_disk')
	#print 'DISK:'+str(get_disk_name)
	#print '<br/>'
	get_lun_name = form.getvalue('select_lun')

	used_disks_array = [];
	used_disks_name = san_disk_funs.iscsi_used_disks_tgt(get_target_name);

	if (len(used_disks_name) == 0):
		print "<script>jAlert('This is the first disk... So assigning lun 0!');</script>"
		#print "<script>jAlert('<img src='../images/info.gif'><div style='float: right; margin-right: 12%; padding-top: 4%; font-family: status-bar;'>This is the first disk.so your lun number start with 0 !</div>, 'Alert Dialog');</script>"
		get_lun_name = 0;

	target_assign=san_disk_funs.iscsi_add_disks_tgt(get_target_name,get_lun_name,get_disk_name)
	#print target_assign

	if(target_assign == True):
		print"""<div id = 'id_trace'>"""
		print "Target <font color='darkred'><b>"+str(get_target_name)+"</b></font> Successfully Assign !"
		print "</div>"
		#print "<script>location.href = 'iframe_iscsi_disk_target.py#tabs-1';</script>"
		#print "<script>location.href = 'main.py?page=iscsi&act=assign_target_done';</script>"
	else:
		print"""<div id = 'id_trace_err'>"""
		print "Error occured while Creating Target <font color = 'darkred'><b>"+str(get_target_name)+"</b></font> !"
		print "</div>"
		#print "<script>location.href = 'iframe_iscsi_disk_target.py#tabs-1';</script>"

#--------------------Delete Disk------------------------------
#--------------Get a target name "target_remove"  and disk name "select_disk_remove" from the form and pass the target and disk name  in backend  function for remove the disk  

if(form.getvalue('target_remove')):

	rm_target = (form.getvalue('target_remove'))
	target_name = rm_target.strip()

	#print "<script>location.href = 'main.py?page=iscsi&act=delete_disk_done';</script>"
	print "<script>location.href = 'iframe_iscsi_disk_target.py?target="+target_name+"#tabs-2';</script>"
	display_del_optn = 'block'
	display_del_optn1= 'block'

used_disk_list = san_disk_funs.iscsi_used_disks_tgt(target_name)


if(form.getvalue('del_from_target')):
	remove_target_name= form.getvalue('target_remove')
	#print remove_target_name
	target_name = remove_target_name.strip()
	#print 'AC:'+str(target_name)
	check_init_list =san_disk_funs.iscsi_ini_list(remove_target_name)
	if(len(check_init_list) > 0):
                print"""<div id = 'id_trace_err'>"""
                print "First Remove the Initiators From the Target"
                print "</div>"
                #print "<script>location.href = 'main.py?page=srp&act=delete_target_done';</script>"
                print "<script>location.href = 'iframe_iscsi_disk_target.py?target="+target_name+"#tabs-2';</script>"
	else:
		
		remove_disk_name = form.getvalue('select_disk_remove')
		#print 'Target: ' + remove_target_name;
		#print '<BR>DISK:'+str(remove_disk_name)
		get_nw_lun = common_methods.get_lun_number(remove_target_name, remove_disk_name)
		#print 'GET NEW LUN:'+str(get_nw_lun)
		#get_lun = []
		#get_free_luns = san_disk_funs.iscsi_luns(remove_target_name)
		#for freeluns in get_free_luns:
			#get_free_luns = map(int, freeluns)
		#print'<br/>'
		#target_remove_function = ''
		#print 'GET FREE LUNS: ' + str(get_free_luns);
		target_remove_function=san_disk_funs.iscsi_rem_disks_tgt(remove_target_name, get_nw_lun)
		#print 'rm res:'+str(target_remove_function)

		if(target_remove_function == True):
			print"""<div id = 'id_trace'>"""
			print "Disk Remove Successfully  !"
			print "</div>"
			print "<script>location.href = 'iframe_iscsi_disk_target.py?target="+target_name+"#tabs-2';</script>"
		else:
			print"""<div id = 'id_trace_err'>"""
			print "Error occured while Deleating the disk!"
			print "</div>"
			print "<script>location.href = 'iframe_iscsi_disk_target.py?target="+target_name+"#tabs-2';</script>"

#import left_nav
if (iscsi_status > 0):

	print
	print """
	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer"  style="margin:0;width:716px;padding-left:0px;">
		<!--<div class="insidepage-heading">I-Scsi >> <span class="content">I-Scsi Configuration</span></div>-->
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
		 <!-- <div class="topinputwrap-heading">Add Disk To Target</div>-->
		  <div class="inputwrap">
		<div class="formrightside-content">
		   <form name = 'add_disk_to_target' method = 'POST' >"""

	print"""<table width = "685" border = "0" cellspacing = "0" cellpadding = "0">
										<tr>
										<td width = '23%' height = "35px" valign = "middle">
											Select target
										</td>
										<td height = "35px" valign = "middle">
			<div class="styled-select2" style="width:518px;">
			<select name = 'target_for_disk' onchange='this.form.submit()' style="width: 104%;">
			<option value='assign_tar'>Select Target</option>
			"""


	if (list_target_name != []):
		for x in list_target_name:
			print """<option value = '"""+str(x)+"""'"""
			if(get_target !=''):
				if(get_target == str(x)):
					print """selected = 'selected'"""
			print """>"""+str(x)+"""</option>"""

	print"""</select></div>"""
	print"""</td>
	</tr>"""

	print"""


		<tr id = 'optn_one' style = 'display:"""+display_optn_one+""";'>
					<td width = "158" height = "40px" valign = "middle" style="float: left;">
					<B>Select Disk:</B>
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
					<B>Select Lun:</B>
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
	<button class = 'buttonClass' type="submit" name = 'add_disk' value = 'Apply' onclick ='return validate_assign_target();'>Add Disk</button>
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
		    <form name = 'del_disk_from_target' method = 'POST'>
			<table width = "685" border = "0" cellspacing = "0" cellpadding = "0">

			 <tr>
											<td width = '23%' class = "table_heading" height = "35px" valign = "middle">
												Select target
											</td>
											<td class = "table_content" height = "35px" valign = "middle">
			<div class="styled-select2" style="width:518px;">
			<select class = 'input' name = 'target_remove' onchange='this.form.submit()' style="width:534px;">
			<option value = 'del_assign_tar'>Select Target</option>
			"""
	for y in list_target_name:
		print """<option value = '"""+y+"""'"""
		if(rm_target !=''):
			if(rm_target == y):
				print """selected = 'selected'"""
		print """>"""+y+"""</option>"""


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
		
		#for used_disks in used_disk_list:
		for used_disks in used_disk_list:
			#used_disks = used_disks['disk']

			print"""<option value = '"""+str(used_disks)+"""'>"""+str(used_disks)+"""</option>"""

		print"""</select></div>
		</td></tr>"""


			
	print"""	
	<tr>
	<td>
	<Div>
	<td style= "float:right;">

	<button class = 'buttonClass' type="submit" name = 'del_from_target' value = 'Remove selected disk' onclick ='return validate_del_assign_target();'>Delete Disk</button>
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
		      </div>

		  <!--</div>
		</div>-->
		<!--form container ends here-->
		<!--form container starts here-->
		<!--form container ends here-->
	      <!--</div>-->
	      <!--Right side body content ends here-->
	    <!--</div>-->
	    <!--Footer starts from here-->
	    <!--<div class="insidefooter footer_content">&copy; 2013 Opslag FS2</div>-->
	    <!-- Footer ends here-->
	  <!--</div>-->
	  <!--inside body wrapper end-->
	<!--</div>-->"""

else:
	print "<div style = 'margin-top: 10%; margin-bottom: 10%; margin-left: auto; margin-right: auto; text-align: center; vertical-align: center; color: darkred; width: 65%; font: 16px Arial;'>Check the 'Enable/Disable i-SCSI' option in Maintenance -><a href ='main.py?page=sr'style ='text-decoration:underline;'>Services</a>.</div>"
print"""
<!--body wrapper end-->
<!--</body>
</html>-->
"""
