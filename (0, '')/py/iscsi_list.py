#!/usr/bin/python
import cgitb, sys, include_files, common_methods, cgi, os
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

#---------------New Getting all Information From db----------
display_ini = ''
display_disk = ''
display_target = ''
display_node = ''
form = cgi.FieldStorage()
querystring = os.environ['QUERY_STRING'];
target_name = form.getvalue("target")
list_target_name = [target_name]

#---------------End------------------------------------------
#----------------------This function to show status of the iscsi---------------
iscsi_status = common_methods.get_iscsi_status();

#----------------------------End------------------------------
#---------------------This function display all the Target Information---------------------------
remove_targets_list= san_disk_funs.iscsi_list_all_tgt()
#---------------------------------End------------------------------------------------------------
#print 'Content-Type: text/html'
#import left_nav

if (iscsi_status > 0):
	print
	print """
	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer" style="margin:0;width:716px;padding-left:0px;">
		<!--tab srt-->
		<div class="searchresult-container">
		      <div id="tabs-1">

		<!--form container starts here-->
		<div class="form-container"  style="width: 96.9%;">
		  <div class="topinputwrap-heading">iSCSI Target Information </div>
		  <div class="inputwrap">
		    <div class="formrightside-content">
		  <form name = 'list_list_from_target' method = 'POST'>
		
		  <table width = "685" cellspacing = "1" cellpadding = "0" border = "1" id = 'id_list_info' style="border-style: inset;">
							<tr style = 'background-color:#999999;font-weight: bold;'>
							<td height = "35px" valign = "middle" style = 'color: #FFF;'>Target</td>
							<td height = "35px" valign = "middle" style = 'color: #FFF;'>Disks</td>
							<td height = "35px" valign = "middle" style = 'color: #FFF;'>Initiators</td>
						</tr>"""


	#if(remove_targets_list!=[]):
	#-------------------Display the target disk and Initiator from this Code------------------------------------
	if(list_target_name !=[]):
                for tar_list_info in list_target_name:

                        #print tar_list_info
                        print"""<tr>
                        <td height = "35px" valign = "middle" style="font-family: Times New Roman;">
                                                                         

                         """+tar_list_info+"""
                        </td>&nbsp;&nbsp;"""

                        print"""<td height = "35px" valign = "middle" style="text-align:center;">"""

                        used_disks_info = san_disk_funs.iscsi_used_disks_tgt(tar_list_info)

                        replace_disk0 = str(used_disks_info).replace('[]', '')
                        replace_disk1 = str(replace_disk0).replace('[', '')
                        replace_disk2 = str(replace_disk1).replace(']', '')
                        used_disk_info = str(replace_disk2).replace("'", '')
                        print used_disk_info
                        #for disks_ini_list in alldisk:
                                #print disks_ini_list
                        #       print""" """+disks_ini_list+"""<br>"""
                        print"""</td>"""

                        getinilist = san_disk_funs.iscsi_ini_list(tar_list_info)
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
                        <td height = "35px" valign = "middle" style="width:25%;">"""
                        print""" """+str(get_initiator4)+"""
                        </td>"""
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
	  <!--inside body wrapper end-->
	</div>"""
else:
	print "<div style = 'margin-top: 10%; margin-bottom: 10%; margin-left: auto; margin-right: auto; text-align: center; vertical-align: center; color: darkred; width: 65%; font: 16px Arial;'>Check the 'Enable/Disable i-SCSI' option in Maintenance -><a href ='main.py?page=sr'style ='text-decoration:underline;'>Services</a>.</div>"

print"""
"""
