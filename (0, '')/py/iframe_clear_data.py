#!/usr/bin/python
import cgitb,  os, sys, include_files, cgi, commands, string
cgitb.enable()
sys.path.append('/var/nasexe/python/');
import db_logs
import tools
from tools import db
from tools import nas_disks

check_ha = tools.check_ha()

#form = cgi.FieldStorage()
sys_node_name = tools.get_ha_nodename()
if(sys_node_name == "node1"):
        other_node = "node2"
        show_tn = "Node1"
        show_on = "Node2"
else:
        other_node = "node1"
        show_tn = "Node2"
        show_on = "Node1"

query="select * from network_ifaces where (name='eth1' and node='"+other_node+"')"
status=db.sql_execute(query)
for x in status["output"]:
        other_node_ip = x["ip"]

sys.path.append('/var/nasexe/')
import net_manage_newkernel as net_manage_bond
getall_ifaces=net_manage_bond.get_all_ifaces_config()
get_all_ip = getall_ifaces["all_conf"]

#import left_nav
form = cgi.FieldStorage()

if(form.getvalue("clr")):
	strvar = ''
	cmd = commands.getstatusoutput("sudo mysql -u root -pnetweb -Nse 'show tables' fs2data")
	if(cmd[0] == 0):
		split = cmd[1].split("\n")
		for x in split:
			query = 'TRUNCATE table '+x+';'
			execute = db.sql_execute(query,data=1)
			if(execute["id"] == 0):
				strvar += "yes"
			else:
				strvar += "no"
	if "no" in strvar:
		print"<div id = 'id_trace_err'>"
		print "Error clearing data!"
		print "</div>"
	else:
		log_msg={'type':'INFO','log_src':'SCRIPT','msg':'INFO: Successfully cleared data.'}
        	log_msg['more_info']='clear data script from UI'
	        db_logs.write_log(log_msg)
		print"<div id = 'id_trace'>"
		print "Successfully cleared data!"
		print "</div>"
	

print
print """


      <!--Right side body content starts from here-->
      <div class="rightsidecontainer">
        <!--<div class="insidepage-heading"><a class="iframe_bc" href="main.py?page=report">MONITORING</a> >> <span class="content">Reports</span></div>-->
        <!--tab srt-->
        <div class="searchresult-container">
 <div style="margin:0 0 0px 0;" class="topinputwrap-heading"><a class="demo" href ="#"><img src ="../images/help_icon1.png" style="width:13px;"><span class="tooltip" style="height:100px;" >
        <div class="text_css">Using this page you can clear the recorded monitoring data.</div>"""
if(check_ha == True):
        print"""
</span></a><p class = "gap_text">Clear Data of """+show_tn+"""</p>
        <span style="float:right; margin:-15px 0px 0 0;"><a onclick="return onclick_loader();" class="resource_links" href="https://"""+other_node_ip+"""/fs4/py/iframe_clear_data.py">"""+show_on+"""</a></span>

        </div>"""
else:
        print""" </span></a><p class = "gap_text">Clear Data</p></div>"""
print"""
          <div class="infoheader">
            <div id="tabs">
              <!--<ul>
                <li><a href="#tabs-1">Reports</a></li>
              </ul>-->
	      <div id="tabs-1">
        <!--form container starts here-->
        <div class="form-container" style="border:none;">
          <div class="inputwrap">
	 <div class="formleftside-content">
	<form name="clear" method="post" action="">
	<button class="buttonClass" type = 'submit'  name="clr" onclick="return confirm('Are you sure you want to clear data?');" value="down_pdf" style="width:100px; margin:0 0 0 0;">Clear Data</button>
	</form>

	</div>
          </div>
        </div>
        <!--form container ends here-->
	<p>&nbsp;</p>
              </div>
</div>
</div>

"""
