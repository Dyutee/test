#!/usr/bin/python
import cgitb, sys, header, common_methods
cgitb.enable()

sys.path.append('/var/nasexe/storage')
import storage_op
import sys,os
from lvm_infos import *
from functions import *
import san_disk_funs

start_fc_chk = ''
check_fc = '0'

check_fc = san_disk_funs.fc_target_status();

#if (str(check_fc).find("'1'") > 0):
if (check_fc !=[]):
        start_fc_chk = 'checked'

########## FC CHECKED ###########
if(header.form.getvalue('start_fc')):
        checkstatus = header.form.getvalue('start_fc');
        #print 'checked:'+str(checkstatus);

        if(checkstatus=='on'):

                start =san_disk_funs.fc_enable_disable(opp='ENABLE')

                start_fc_chk ='checked'

import left_nav

if (check_fc !=[]):
	print
	print """
	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer">
		<div class="insidepage-heading">Fc >> <span class="content">Fc Information</span></div>
		<!--tab srt-->
		<div class="searchresult-container">
		  <div class="infoheader">
		    <div id="tabs">
		      <ul>
			<li><a href="#tabs-1">Fc</a></li>
		      </ul>
		      <div id="tabs-1">

		<!--form container starts here-->
		<div class="form-container">
		  <div class="topinputwrap-heading">Fc Service Status </div>
		  <div class="inputwrap">
		    <div class="formrightside-content">
		    <input type = 'checkbox' name = 'start_fc' onclick='this.form.submit()' """+start_fc_chk+""" disabled><font color="darkgreen" size="2px"><b>Fc Active</></font> <?= $message ?>


		</div>"""
else:
	print "<div style = 'margin-left: auto; margin-right: auto; text-align: center; vertical-align: center; color: darkred; width: 65%; font: 16px Arial;'><br/><br/><br/><b>Check the 'Enable/Disable Fc' option in Maintenance -> Services.</div>"

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
