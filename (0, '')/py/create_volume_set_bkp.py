#!/usr/bin/python

import cgitb, sys, header, common_methods, os, commands, string
cgitb.enable()
sys.path.append('../modules/');
import disp_except

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
<div style="margin-left:35px;" class="iframe-insidepage-heading"><a class="iframe_bc" href="#">Raid Configuration</a> <span style="color:#000; "> >> </span>Create/Delete Volume Set</div>
"""
print """<iframe src='iframe_create_volume_set.py' style="width:795px; border:none; min-height: 500px; height:auto !important; height: 500px;" ></iframe>"""
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
