#!/usr/bin/python
import cgitb, header, sys
cgitb.enable()
sys.path.append('../modules/')
import disp_except;
import left_nav

sys.path.append("/var/nasexe/python/")
import tools
from tools import db

target_name = header.form.getvalue("target")
node_name = header.form.getvalue("node")
#print target_name

#query = "select * from iscsi_tgt"
#status=db.sql_execute(query)
#for z in status['output']:
#	target_alias_name = z['name']
#	target_node_name = z['node']
#share_det = tools.get_share(share_name,debug=False)
#share_node_name = share_det["share"]["node"]

#print '<br/>'
#print node_name	
#print '<br/>'
sys_node_name = tools.get_ha_nodename()
#print 'NODE:'+str(sys_node_name)
#exit()
if(sys_node_name == "node1"):
        other_node = "node2"
else:
        other_node = "node1"

query="select * from network_ifaces where (name='eth1' and node='"+other_node+"')"
status=db.sql_execute(query)
for x in status["output"]:
        other_node_ip = x["ip"]
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
<div style="margin:0 0 0 40px;" class="insidepage-heading">San >> <span><a class="iframe_bc" href="main.py?page=iscsi">I-scsi Target</a></span> >>Iscsi</div>
"""
#if(share_node_name == "node1"):
if(node_name == sys_node_name):
	print """<iframe src='iframe_iscsi_disk_target.py?target_name="""+target_name+"""' style="width:795px; border:none; min-height: 500px; height:auto !important; height: 500px;" ></iframe>"""
else:
	print """<iframe src='https://"""+other_node_ip+"""/fs4/py/iframe_iscsi_disk_target.py?target_name="""+target_name+"""' style="width:795px; border:none; min-height: 500px; height:auto !important; height: 500px;" ></iframe>"""

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
