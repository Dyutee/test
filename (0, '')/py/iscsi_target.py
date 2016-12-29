#!/usr/bin/python
#_*_ coding: UTF-8 _*_                                          
"""
	this page is for creating share, modifying a share, user quota and showing share information. to create a share, it is required that we
	should have atleast one nas disk created.
"""
#enable debugging                                       
import cgitb, header, os, common_methods, commands, sys

cgitb.enable()          

sys.path.append('/var/nasexe/storage/');
sys.path.append('../modules/');
import disp_except;

import storage_op
from lvm_infos import *
from functions import *

sys.path.append('/var/nasexe/python/');
import cli_utils;

get_all_disk = storage_op.list_all_disks()

import left_nav
print """
<style>
::-webkit-scrollbar { 
    display: none; 
}
::-moz-scrollbar { 
    display: none; 
}

a.iframe_bc{color:#000; text-decoration:underline; }
a.iframe_bc:hover{text-decoration:overline;}
</style>
<div style="margin-left:35px;" class="iframe-insidepage-heading">I-Scsi <span style="color:#000; "> >> </span> <span><a class="iframe_bc" href="main.py?page=iscsi">Iscsi Target</a></span> <span style="color:#000; "> >> </span> I-Scsi Configuration</div>
"""
print """<iframe src='iframe_iscsi_target.py' style="width:795px; border:none; min-height: 500px; height:auto !important; height: 500px;" ></iframe>"""
print """
<!--form container ends here-->
<!--form container starts here-->
<!--form container ends here-->
</div>
<!--Right side body content ends here-->
</div>
<!--Footer starts from here-->
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


