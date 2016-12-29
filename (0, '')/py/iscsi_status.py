#!/usr/bin/python
import cgitb, sys, header, common_methods
cgitb.enable()

sys.path.append('/var/nasexe/storage')
import storage_op
import sys,os
from lvm_infos import *
from functions import *
import san_disk_funs

iscsi_status = common_methods.get_iscsi_status();

start_iscsi_chk = ''
stop_iscsi_chk = ''

if (iscsi_status > 0):
	start_iscsi_chk = 'checked';

if(header.form.getvalue('start_iscsi')):
	checkstatus = header.form.getvalue('start_iscsi');
	#print 'checked:'+str(checkstatus);

	if(checkstatus=='on'):

		start = san_disk_funs.iscsi_enable(act='ENABLE')
		#print start
		if(start == True):
			print"""<div id = 'id_trace'>"""
			print " <font color='darkred'></b></font> Successfully started I-scsi!"
			print "</div>"
			print "<script>location.href = 'main.py?page=iscsi&act=delete_target_done';</script>"
			display_enable = 'block'
			display_create = 'none'
			display_delete_target = 'none';
			display_assign_disk = 'none';
			display_delete_disk = 'none';
			display_add_initiator = 'none'
			display_delete_initiator = 'none';
			display_authentication_initiator = 'none';
			display_list_info = 'none';
			display_target_properties = 'none';


		start_iscsi_chk ='checked'

#print 'Content-Type: text/html'
import left_nav
if (iscsi_status > 0):
	print
	print """
	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer">
		<div class="insidepage-heading">I-Scsi >> <span class="content">I-Scsi Information</span></div>
		<!--tab srt-->
		<div class="searchresult-container">
		  <div class="infoheader">
		    <div id="tabs">
		      <ul>
			<li><a href="#tabs-1">I-scsi</a></li>
		      </ul>
		      <div id="tabs-1">

		<!--form container starts here-->
		<div class="form-container">
		  <div class="topinputwrap-heading">Iscsi Service Status </div>
		  <div class="inputwrap">
		    <div class="formrightside-content">
		    <input type = 'checkbox' name = 'start_iscsi' onclick='this.form.submit()' """+start_iscsi_chk+""" disabled><font color="darkgreen" size="2px"><b>I-SCSI Active</></font> <?= $message ?>


		</div>"""

else:


	print "<div style = 'margin-top: 10%; margin-bottom: 10%; margin-left: auto; margin-right: auto; text-align: center; vertical-align: center; color: darkred; width: 65%; font: 16px Arial;'>Check the 'Enable/Disable i-SCSI' option in Maintenance -> Services.</div>"
print"""          </div>
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
</div>
<!--body wrapper end-->
</body>
</html>
"""
