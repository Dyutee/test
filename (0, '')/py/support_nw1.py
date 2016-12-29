#!/usr/bin/python
import cgitb,  os, sys, include_files, cgi
cgitb.enable()
sys.path.append('/var/nasexe/python/');
import tools
from tools import db
from tools import nas_disks

#################################################
############### Check HA Status #################
#################################################
check_ha = tools.check_ha()
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
#--------------------- END --------------------#

#--- Get all Stats
st = nas_disks.get_all_stats()

sys.path.append('/var/nasexe/')
import net_manage_newkernel as net_manage_bond
getall_ifaces=net_manage_bond.get_all_ifaces_config()
get_all_ip = getall_ifaces["all_conf"]

form = cgi.FieldStorage()
if(form.getvalue("down_pdf")):
	print "Content-Type: application/pdf"
	print "Content-Disposition: attachment; Tyronemanual.pdf"
int_type =''
g_type =''
from_val = ''
to_val = ''
search_from = ''
search_to = ''
on_page_show_graph = 'no'
graph_type = ''
execute = {'output':'no'}

#################################################
############### Get Graph type ##################
#################################################
if(form.getvalue("g_type")):
	g_type = form.getvalue("g_type")
#--------------------- END --------------------#
	
if(form.getvalue("show_graph")):
	from_val = form.getvalue("from")
	to_val = form.getvalue("to")
	g_type = form.getvalue("g_type")
	if(from_val != None or to_val != None):
		search_from = from_val.replace("-","")+str("000000")
		search_to = to_val.replace("-","")+str("235959")
		on_page_show_graph = "yes"
		if(g_type == "interface"):
			int_type = form.getvalue("int_type")
			query = 'select * from eth_traffic where interface="'+int_type+'" and timestamp between '+search_from+' and '+search_to+';'
			execute=db.sql_execute(query,data=1)
		if(g_type == "temperature"):
			query = 'select * from temperature where timestamp between '+search_from+' and '+search_to+';'
			execute=db.sql_execute(query,data=1)
		if(g_type == "memory"):
			query = 'select * from memory_data where timestamp between '+search_from+' and '+search_to+';'
			execute=db.sql_execute(query,data=1)
		if(g_type == "diskio"):
			int_type = form.getvalue("int_type")
			query = 'select * from disk_usage where disk_name="'+int_type+'" and timestamp between '+search_from+' and '+search_to+';'
			execute=db.sql_execute(query,data=1)
		

print
print """

<link rel="stylesheet" href="datepicker/jquery-ui.css">
<script src="datepicker/jquery-ui.js"></script>
<script>
$(function() {
$( "#from" ).datepicker({
defaultDate: "+1w",
changeMonth: true,
numberOfMonths: 2,
onClose: function( selectedDate ) {
$( "#to" ).datepicker( "option", "minDate", selectedDate );
$( "#to" ).datepicker( "option", "dateFormat", "yy-mm-dd" );
}
});
$( "#to" ).datepicker({
defaultDate: "+1w",
changeMonth: true,
numberOfMonths: 2,
onClose: function( selectedDate ) {
$( "#from" ).datepicker( "option", "maxDate", selectedDate );
$( "#from" ).datepicker( "option", "dateFormat", "yy-mm-dd" );
}
});
});
</script>

      <!--Right side body content starts from here-->
      <div class="rightsidecontainer">
        <!--<div class="insidepage-heading"><a class="iframe_bc" href="main.py?page=report">MONITORING</a> >> <span class="content">Reports</span></div>-->
        <!--tab srt-->
        <div class="searchresult-container">
 <div style="margin:0 0 0px 0;" class="topinputwrap-heading"><a class="demo" href ="#"><img src ="../images/help_icon1.png" style="width:13px;"><span class="tooltip" style="height:100px;" >
        <div class="text_css">On this page, you can view the historical monitoring data for a specified date range.</div>"""
if(check_ha == True):
        print"""
</span></a><p class = "gap_text">Report Information of """+show_tn+"""</p>
        <span style="float:right; margin:-15px 0px 0 0;"><a onclick="return onclick_loader();" class="resource_links" href="https://"""+other_node_ip+"""/fs4/py/support_nw1.py">"""+show_on+"""</a></span>

        </div>"""
else:
        print""" </span></a><p class = "gap_text">Report Information</p></div>"""
print"""
          <div class="infoheader">
            <div id="tabs">
              <!--<ul>
                <li><a href="#tabs-1">Reports</a></li>
              </ul>-->
	      <div id="tabs-1">
        <!--form container starts here-->
        <div class="form-container" style="border:none;">
          <!--<div class="topinputwrap-heading">Reports</div>-->
          <div class="inputwrap">
	 <div class="formleftside-content">
<form name="graph" action="" method="post" >
<table width="750px">
<tr>
<th>Select Graph</th>
<td>
<div class="styled-select2">
<select name="g_type" onchange="this.form.submit();">
<option value='temperature'"""
if(g_type == "temperature"):
	print "selected"
print """>CPU Temperature</option>
<option value='memory'"""
if(g_type == "memory"):
	print "selected"
print """>Memory Usage</option>"""
if(st != []):
	print """<option value='diskio'"""
	if(g_type == "diskio"):
	        print "selected"
	print """>Disk I/O</option>"""
print """
<option value='interface'"""
if(g_type == "interface"):
        print "selected"
print """>Network I/O</option>
</select>
</div>
</td>
</tr>"""

if(g_type == "interface"):
	print """<tr>
	<th>Select Interface</th>
	<td>
	<div class="styled-select2">
	<select name="int_type">"""
	for iface in get_all_ip:
		print """<option value='"""+str(iface['iface'])+"""'>"""+str(iface['iface'])+"""</option>"""
	print """
	</select>
	</div>
	</td>
	</tr>"""

if(g_type == "diskio"):
	print """<tr>
	<th>Select Disk</th>
	<td>
	<div class="styled-select2">
	<select name="int_type">"""
	for i in st:
		if 'used' in i.keys() and i["type"] == "NAS":
			print """<option value='"""+str(i['name'])+"""'>"""+str(i['name'])+"""</option>"""
	print """
	</select>
	</div>
	</td>
	</tr>"""

print """
<tr>
<th>From Date</th>
<td><input class='textbox' readonly type="text" name="from" id="from" style="width:187px;"></td>
</tr>

<tr>
<th>To Date</th>
<td><input class='textbox' readonly type="text" name="to" id="to" style="width:187px;" /></td>
</tr>

</table>

<table width="750px;">
<tr>
<td>
<button class="buttonClass" type="submit" name = 'show_graph' value ='show_graph'  style=" width:110px; margin:10px 335px 20px 0; float:right;">Show Graph</button>
</td>
</tr>
</table>
</form>
"""
if(execute["output"] != ()):
	if (on_page_show_graph == "yes"):
		if(g_type == "temperature"):
			print """<iframe src='canvas_temp_static2.py?from="""+str(search_from)+"""&to="""+str(search_to)+"""' style="width:650px; border:none; min-height: 500px; height:auto !important; height: 500px;" ></iframe>"""
		if(g_type == "memory"):
			print """<iframe src='canvas_mem_static.py?from="""+str(search_from)+"""&to="""+str(search_to)+"""' style="width:650px; border:none; min-height: 500px; height:auto !important; height: 500px;" ></iframe>"""
		if(g_type == "interface"):
			print """<iframe src='canvas_interface_static.py?int_type="""+int_type+"""&from="""+str(search_from)+"""&to="""+str(search_to)+"""' style="width:650px; border:none; min-height: 500px; height:auto !important; height: 500px;" ></iframe>"""
		if(g_type == "diskio"):
			print """<iframe src='canvas_disk_static.py?int_type="""+int_type+"""&from="""+str(search_from)+"""&to="""+str(search_to)+"""' style="width:650px; border:none; min-height: 500px; height:auto !important; height: 500px;" ></iframe>"""
		
else:
	print """<div style="width:600px; text-align:center; color:red;">No Records Found!</div>"""
print """

	</div>
          </div>
        </div>
        <!--form container ends here-->
	<p>&nbsp;</p>
              </div>
</div>
</div>
<!-- ####### Sub Tabs Start ####### -->

<script>
$("#tabs, #subtabs").tabs();
$("#tabs, #subsubtabs").tabs();
</script>

<!-- ####### Sub Tabs End ####### -->

"""
