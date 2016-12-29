#!/usr/bin/python
import cgitb, sys,  common_methods, cgi, include_files
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
#print list_srp_target
#---------------Check Srp status-------------------
check_srp = san_disk_funs.ib_target_status();

srp_target=san_disk_funs.ib_list_targets()
#---------------End-------------------------------

#import left_nav

if (check_srp !=[]):
	print
	print """
	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer" style="margin:0;width:716px;padding-left:0px;">
		<!--tab srt-->
		<div class="searchresult-container">
		  <div class="infoheader">
		    <!--<div id="tabs">
		      <ul>
			<li><a href="#tabs-1">Srp Information</a></li>
		      </ul>
		      <div id="tabs-1">-->

		<!--form container starts here-->
		<div class="form-container" style="width: 97%;">
		  <div class="topinputwrap-heading">Srp Target Information </div>
		  <div class="inputwrap">
		    <div class="formrightside-content">
		  <form name = 'list_initr_from_target' method = 'POST'>
		
		  <table width = "685" cellspacing = "1" cellpadding = "0" border = "1" id = 'id_list_info' style="border-style: inset;">
							<tr style = 'background-color:#999999;font-weight: bold;'>
							<td height = "35px" valign = "middle" style = 'color: #FFF;'>Target</td>
							<td height = "35px" valign = "middle" style = 'color: #FFF;'>Disks</td>
							<td height = "35px" valign = "middle" style = 'color: #FFF;'>Initiators</td>
						</tr>"""
	#-------------------display the Srp target, Disk and Initiator------------------------------ 
	if(list_srp_target !=[]):
		#for tar_list_info in remove_targets_list:
		for tar_list_info in list_srp_target:

			#print tar_list_info
			print"""<tr>
			<td height = "35px" valign = "middle" style="font-family: Times New Roman;">
									 

			 """+tar_list_info+"""
			</td>&nbsp;&nbsp;"""

			print"""<td height = "35px" valign = "middle" style="text-align:center;">"""

			used_disks_info = san_disk_funs.ib_used_disks_tgt(tar_list_info)

			replace_disk0 = str(used_disks_info).replace('[]', '')
			replace_disk1 = str(replace_disk0).replace('[', '')
			replace_disk2 = str(replace_disk1).replace(']', '')
			used_disk_info = str(replace_disk2).replace("'", '')
			print used_disk_info
			#for disks_ini_list in alldisk:
				#print disks_ini_list
			#       print""" """+disks_ini_list+"""<br>"""
			print"""</td>"""

			getinilist = san_disk_funs.ib_ini_list(tar_list_info)
			#print getinilist
			replace_get_ini = str(getinilist).replace('[]', '')
			#print 'rep1:'+replace_get_ini
			#print '<br/>'
			get_initiator = str(replace_get_ini).replace('[', '')
			get_initiator1 = str(get_initiator).replace(']', '')
			get_initiator2 = str(get_initiator1).replace("'", '')
			#print 'GET I:'+ get_initiator2
			get_initiator3 = str(get_initiator2).replace('*', 'Access for all ip(*)' )


			get_initiator3 = get_initiator3.replace(',', '<BR>');
			get_initiator4= get_initiator3.replace('#', ' through ')
			print"""
			<td>"""
			print""" """+str(get_initiator4)+"""
			</td>"""
		#---------------------------------------End---------------------------------------
			print"""</tr>"""
	else:
		print"""<tr>
		<td colspan = '3' align = 'center' height="50px;">
		<marquee behavior="alternate" direction= "right"><b><font size="5">No Information is available</font></b></marquee>
		</td>
		</tr>"""

	print"""</table></form>"""
	print"""
		</div>
		  </div>
		</div>
		<!--form container ends here-->
	</div>"""
else:
	print "<div style = 'margin-left: auto; margin-right: auto; text-align: center; vertical-align: center; color: darkred; width: 65%; font: 16px Arial;'><br/><br/><br/><b>Check the 'Enable/Disable Srp' option in Maintenance -></b><a href= 'main.py?page=sr'><span style='text-decoration:underline;'>Services</span></a>.</div>"

print"""
"""
