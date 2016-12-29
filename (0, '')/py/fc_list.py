#!/usr/bin/python
import cgitb, sys, header, common_methods
cgitb.enable()

sys.path.append('/var/nasexe/storage')
import storage_op
import sys,os
from lvm_infos import *
from functions import *
import san_disk_funs
check_fc = san_disk_funs.fc_target_status();

fc_target=san_disk_funs.fc_list_targets()

import left_nav

if (check_fc !=[]):
	print
	print """
	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer">
		<div class="insidepage-heading">Fc >> <span class="content">Fc Target Information</span></div>
		<!--tab srt-->
		<div class="searchresult-container">
		  <div class="infoheader">
		    <div id="tabs">
		      <ul>
			<li><a href="#tabs-1">Fc Information</a></li>
		      </ul>
		      <div id="tabs-1">

		<!--form container starts here-->
		<div class="form-container">
		  <div class="topinputwrap-heading">Fc Target Information </div>
		  <div class="inputwrap">
		    <div class="formrightside-content">
		  <form name = 'list_initr_from_target' method = 'POST'>
		
		  <table width = "685" cellspacing = "1" cellpadding = "0" border = "1" id = 'id_list_info' style="border-style: inset;">
							<tr style = 'background-color:#999999;font-weight: bold;'>
							<td height = "35px" valign = "middle" style = 'color: #FFF;'>Target</td>
							<td height = "35px" valign = "middle" style = 'color: #FFF;'>Disks</td>
							<td height = "35px" valign = "middle" style = 'color: #FFF;'>Initiators</td>
						</tr>"""

	if(fc_target!=[]):
		#for tar_list_info in remove_targets_list:
		for tar_list_info in fc_target:

			#print tar_list_info
			print"""<tr>
			<td height = "35px" valign = "middle" style="font-family: Times New Roman;">
									 

			 """+tar_list_info+"""
			</td>&nbsp;&nbsp;"""

			print"""<td height = "35px" valign = "middle" style="text-align:center;">"""

			used_disks_info = san_disk_funs.fc_used_disks_tgt(tar_list_info)

			replace_disk0 = str(used_disks_info).replace('[]', '')
			replace_disk1 = str(replace_disk0).replace('[', '')
			replace_disk2 = str(replace_disk1).replace(']', '')
			used_disk_info = str(replace_disk2).replace("'", '')
			print used_disk_info
			#for disks_ini_list in alldisk:
				#print disks_ini_list
			#       print""" """+disks_ini_list+"""<br>"""
			print"""</td>"""

			getinilist = san_disk_funs.fc_ini_list(tar_list_info)
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
	</div>"""
else:
	print "<div style = 'margin-left: auto; margin-right: auto; text-align: center; vertical-align: center; color: darkred; width: 65%; font: 16px Arial;'><br/><br/><br/><b>Check the 'Enable/Disable FC' option in Maintenance -></b><a href= 'main.py?page=sr'><span style='text-decoration:underline;'>Services</span></a>.</div>"

print"""
<!--body wrapper end-->
</body>
</html>
"""
