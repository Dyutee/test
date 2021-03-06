#!/usr/bin/python
import cgitb, sys, header, common_methods, string, commands, traceback, os, opslag_info
cgitb.enable()

sys.path.append('/var/nasexe/python/');
import nfs, tools
from tools import db

sys.path.append('../modules/');
import disp_except;

date_cmd=commands.getoutput('sudo date +"%Y"')
os_name= opslag_info.getos('oss')

share_name = header.form.getvalue("share_name")
share_det = tools.get_share(share_name,debug=False)
share_node_name = share_det["share"]["node"]
sys_node_name = tools.get_ha_nodename()
if(sys_node_name == "node1"):
        other_node = "node2"
else:
        other_node = "node1"

query="select * from network_ifaces where (name='eth1' and node='"+other_node+"')"
status=db.sql_execute(query)
for x in status["output"]:
        other_node_ip = x["ip"]

red_page = "cs"
if(header.form.getvalue("view")):
        view_val = header.form.getvalue("view")
        if(view_val == "list"):
                red_page = "csl"

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
<div id="iframe_flow_control" class="iframe-insidepage-heading"><a class="demo" href ="#"><img src ="../images/help_icon1.png" style="border:#000 1px solid; margin:-4px 2px;"><span class="tooltip" >
                 <table border="0">
        <tr>
        <td class="text_css">
	On this page, you can configure IP based access rights and configure mount options for NFS shares.</td>
        </tr>
        </table></span></a>NAS <span style="color:#000; "> >> </span> <span><a class="iframe_bc" href="main.py?page="""+red_page+"""">Shares</a></span> <span style="color:#000; "> >> </span> NFS Settings</div>
"""
if(share_node_name == sys_node_name):
        print """<iframe src='iframe_nfs_settings_page.py?share_name="""+share_name+"""' style="width:795px; border:none; min-height: 500px; height:auto !important; height: 500px;" ></iframe>"""
else:
        print """<iframe src='https://"""+other_node_ip+"""/fs4/py/iframe_nfs_settings_page.py?share_name="""+share_name+"""' style="width:795px; border:none; min-height: 500px; height:auto !important; height: 500px;" ></iframe>"""

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

