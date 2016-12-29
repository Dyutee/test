#!/usr/bin/python
import cgitb, sys, header, common_methods
cgitb.enable()

sys.path.append('/var/nasexe/storage')
import storage_op
import sys,os
from lvm_infos import *
from functions import *
import san_disk_funs

start_srp_chk = ''
check_srp = san_disk_funs.ib_target_status();

if (str(check_srp).find("'1'") > 0):
	start_srp_chk = 'checked'

########## SRP CHECKED ###########
if(header.form.getvalue('start_srp')):
	checkstatus = header.form.getvalue('start_srp');
	#print 'checked:'+str(checkstatus);
	
	if(checkstatus=='on'):

		start =san_disk_funs.ib_enable_disable(opp='ENABLE')

		start_srp_chk ='checked'

#print 'Content-Type: text/html'
import left_nav

if (str(check_srp).find("'1'") > 0):
	print
	print """
	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer">
		<div class="insidepage-heading">Srp >> <span class="content">Srp Information</span></div>
		<!--tab srt-->
		<div class="searchresult-container">
		  <div class="infoheader">
		    <div id="tabs">
		      <ul>
			<li><a href="#tabs-1">Srp</a></li>
		      </ul>
		      <div id="tabs-1">

		<!--form container starts here-->
		<div class="form-container">
		  <div class="topinputwrap-heading">Srp Service Status </div>
		  <div class="inputwrap">
		    <div class="formrightside-content">
		    <input type = 'checkbox' name = 'start_srp' onclick='this.form.submit()' """+start_srp_chk+""" disabled><font color="darkgreen" size="2px"><b>Srp Active</></font> <?= $message ?>


		</div>"""
else:
	print "<div style = 'margin-left: auto; margin-right: auto; text-align: center; vertical-align: center; color: darkred; width: 65%; font: 16px Arial;'><br/><br/><br/><b>Check the 'Enable/Disable SRP' option in Maintenance--></b><a href ='main.py?page=sr'style ='text-decoration:underline;'>Services</a>.</div>"

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
