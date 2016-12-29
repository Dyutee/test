#!/usr/bin/python

import traceback, sys, header, commands, opslag_info
sys.path.append('../modules/')
import disp_except;

import left_nav
date_cmd=commands.getoutput('sudo date +"%Y"')

os_name= opslag_info.getos('oss')
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
<!--<div id="iframe_flow_control" class="iframe-insidepage-heading"><a class="iframe_bc" href="main.py?page=sys">Resources</a> <span style="color:#000; "> >> </span> <a class="iframe_bc" href="main.py?page=sys">Resources Information</a> <span style="color:#000; "> >> </span> OS Information</div>-->
<div id="iframe_flow_control" class="iframe-insidepage-heading" style="font-size:17px;font-family:message-box;"></div>
"""
print """<iframe src='iframe_dashboard1.py' style="width:795px; border:none; min-height: 500px; height:auto !important; height: 500px;" ></iframe>"""
print """
<!--form container ends here-->
<!--form container starts here-->
<!--form container ends here-->
</div>
<!--Right side body content ends here-->
</div>
<!--Footer starts from here-->
<!--Footer starts from here-->
<div class="insidefooter footer_content">&copy """+date_cmd+""" """+os_name+""" FS2</div>
<!-- Footer ends here-->
</div>
<!--inside body wrapper end-->
</div>
<!--body wrapper end-->
</body>
</html>
"""

