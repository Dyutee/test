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
fc_ip = ''
ses = ''

########### FC  Session ##########################
for session_tar in fc_target:
	#print 'Session Target:'+str(session_tar)
	#print '<br/>'
	#print 'Sess Tar:'+str(session_tar)
	#print '<br/>'
	ses=san_disk_funs.fc_session(session_tar)

	#print 'FC SESSION Info:'+str(sess)
import left_nav

#if (str(check_fc).find("'1'") > 0):
if (check_fc !=[]):
	print
	print """
	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer">
		<div class="insidepage-heading">Fc >> <span class="content">Fc Session Information</span></div>
		<!--tab srt-->
		<div class="searchresult-container">
		  <div class="infoheader">
		    <div id="tabs">
		      <ul>
			<li><a href="#tabs-1">Fc Session</a></li>
		      </ul>
		      <div id="tabs-1">

		<!--form container starts here-->
		<div class="form-container">
		  <div class="topinputwrap-heading">Fc Session Information </div>
		  <div class="inputwrap">
		    <div class="formrightside-content">

		<form name = 'add_info' method = 'POST'>
					<table width = "680" border = "1" cellspacing = "0" cellpadding = "0" name = 'disp_tables' id = 'id_target_info' style ="border-style:ridge;">"""


	print"""<tr style = 'background-color:#999999; font-weight: bold;'>
			<td height = "35px" valign = "middle" style = 'color: #FFF;'>Fc Target</td>
			
			<td height = "35px" valign = "middle" style = 'color: #FFF;'>Connected Client</td>
			</tr>"""

		#print  fc_target
	
	if(ses !=''):
		for tar_info in fc_target:

			print"""<tr>
										<!--<td class = "table_content" height = "35px" valign = "middle">
				<a href = 'main.php?page=iscsi&act=add_disk_tgt_done&target=<?= $show_targets ?>'><img border = '0' style = 'margin-top: 2px;' src = '../images/add.png' title = 'Add disk to target' /></a>&nbsp;<a href = 'main.php?page=iscsi&act=del_disk_tgt_done&t=<?= $show_targets ?>'><img border = '0' src = '../images/fileclose.png' title = 'Remove disk from target' /></a>&nbsp;<a href = 'get_properties.php?target=<?= $show_targets ?>'><img border = '0' src = '../images/properties.png' title = 'Target properties' /></a> </td>-->


		<td class = "table_content" height = "35px" valign = "middle">"""
			print""" <font color ="darkred"><b>"""+tar_info+"""</b></font>"""
			print """</td>"""

			print"""<td class = "table_content" height = "35px" valign = "middle" style="font-family: Tahoma;text-decoration:blink;">"""

			sesion_tar =sess=san_disk_funs.fc_session(tar_info)
			replace_sess_nm = str(sesion_tar).replace('[]', '')
			replace_sess_nm1 = str(replace_sess_nm).replace('[', '')
			replace_sess_nm2 = str(replace_sess_nm1).replace(']', '')
			replace_session_name = str(replace_sess_nm2).replace("'", '')
			#print replace_session_name
			if(replace_session_name!=''):

				print"""<font color = 'darkgreen'><b>"""+replace_session_name+"""</b></font></td>"""
			else:
				print """
				<marquee behavior="alternate" direction ="right"><b><font size="3">There is no Session for this client</font></b></marquee>
				</td>
				"""
	else:
		print"""<tr>
                <td colspan = '3' align = 'center' height="50px;">
                <marquee behavior="alternate" direction= "right"><b><font size="5">No Information is available</font></b></marquee>
                </td>
                </tr>"""
		

	print"""	
	</table>
	</form>
	</div>"""
	print"""
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
