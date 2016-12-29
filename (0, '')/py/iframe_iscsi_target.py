#!/usr/bin/python
import cgitb, sys,  common_methods, cgi, include_files
cgitb.enable()

sys.path.append('/var/nasexe/storage')
import storage_op
import sys,os
from lvm_infos import *
from functions import *
import san_disk_funs

form = cgi.FieldStorage()
iscsi_status = common_methods.get_iscsi_status();

display_create = ''
display_delete_target = ''

random_target=san_disk_funs.get_iscsi_target_name()
#print 'Content-Type: text/html'
remove_targets_list= san_disk_funs.iscsi_list_all_tgt()

target_del = ''
target_select_delete = ''
if(form.getvalue('action_butt')):
	iscsi_target= form.getvalue('iscsi_target')

	#print iscsi_target
	#print '<br/>'
	check_target =isinstance(iscsi_target, str)
	#print check_target

	if(check_target ==True):

	#print '<br/>'
		addtarget=san_disk_funs.iscsi_add_target(iscsi_target)
		#print addtarget
		if(addtarget == True):
			print"""<div id = 'id_trace'>"""
			print " <font color='darkred'></b></font> You have Successfully added the Target Name!"
			print "</div>"
			#print "<script>location.href = 'iscsi_target.py?act=create_target_done#tabs-1';</script>"
	 		#print "<script>location.href = 'main.py?page=target_iscsi#tabs-1';</script>";
	 		#print "<script>location.href = 'iframe_iscsi_target.py#tabs-1';</script>";
	 		print "<script>location.href = 'iscsi_new.py#tabs-1';</script>";
			display_create = 'block';
			display_delete_target = 'none'


		else:
			print"""<div id = 'id_trace_err'>"""
			print "Error occured while Adding the Target Name!"
			print "</div>"
			display_create = 'block';
			display_delete_target = 'none';
	 		print "<script>location.href = 'iframe_iscsi_target.py#tabs-1';</script>";


if(form.getvalue('del_target')):
	target_del = form.getvalue('target_to_delete')
	#print target_del
	xyz = []
	chk_used_disk = san_disk_funs.iscsi_used_disks_tgt(target_del)

	check_ini_list =san_disk_funs.iscsi_ini_list(target_del)

	if(len(check_ini_list) > 0):
		print"""<div id = 'id_trace_err'>"""
		print "Error occured while Deleting! Target contains initiator(s)"
		print "</div>"

	elif(len(chk_used_disk) > 0):
		print"""<div id = 'id_trace_err'>"""
		print "Error occured while Deleting! Target contains disk(s)"
		print "</div>"
		print "<script>location.href = 'iframe_iscsi_target.py#tabs-2';</script>"

	else:

		target_delete_msg = san_disk_funs.iscsi_rem_target(target_del)
		print"""<div id = 'id_trace'>"""
		print "Successfully Deleted the Target!"
		print "</div>"
		#print "<script>location.href = 'main.py?page=iscsi&act=delete_target_done';</script>"
		#display_create = 'none';
                #display_delete_target = 'block'
		print "<script>location.href = 'iframe_iscsi_target.py#tabs-2';</script>";

sys.path.append("/var/nasexe/python/")
import tools
from tools import db

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
#import left_nav

if(iscsi_status > 0):
	print
	print """
		<div id="loader-div" style="text-align:center; display:none;" ><img style="margin-top:20%;" src="../images/ajax-loader.gif" /><br/> Loading...</div>
		<div class="view_option" style = 'border: 0px solid;margin-top:-5px;'><a href = 'iscsi_new.py'><img title = 'Back to Iscsi Target List' src = '../images/gobacktoshares.png' /></a></div>
	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer" id="body-div" style="margin-top: -2%;">
		<!--tab srt-->
		<div class="searchresult-container">
		 <div class="topinputwrap-heading"><a class="demo" href ="#"><img src ="../images/help_icon1.png" style="width: 13px;"><span class="tooltip" >


                 <table border="0">
        <tr>
        <td style="font-size: medium;text-align:start;">Iscsi Create:</td>
        </tr>

        <tr>     
        <td class="text_css">In this Page Create the Iscsi Target.</td>
        </tr>
        </table>"""

	if(check_ha == True):
	
		print"""
	</span></a>Create Target ("""+show_tn+""")
                <span style="float:right; margin:0 5px 0 0;"><a  onclick="return onclick_loader();" class="resource_links" href="https://"""+other_node_ip+"""/fs4/py/iframe_iscsi_target.py">"""+show_on+"""</a></span>
                </div>"""
	else:
		print """</span></a>Create Target</div>"""
	print"""
		  <div class="infoheader">
		    <!--<div id="tabs">
		      <ul>
			<li><a href="#tabs-1">Create Target</a></li>
			<li><a href="#tabs-2">Delete Target</a></li>
		      </ul>
		      <div id="tabs-1">-->

		<!--form container starts here-->
		<div class="form-container">
		  <div class="inputwrap">
		    <div class="formrightside-content">
		   <form name = 'add_disk' method = 'post'>
			
		<!--<table width = "200">
			<tr>
				 <td width = '19%' height = "35px" valign = "middle">
                   			Node1 
				</td>
				<td height = "35px" valign = "middle">
                                 <input type = 'radio' name = 'chk'>
                                </td>
			<td width = '19%' height = "35px" valign = "middle">
                                        Node2 
                                </td>
                                <td height = "35px" valign = "middle">
                                 <input type = 'radio' name = 'chk'>
                                </td></tr>
		</table>-->

		   <table width = "685" border = "0" cellspacing = "0" cellpadding = "0" style = 'display:"""+display_create+""" ;'>

							
	
										<tr>
										<td width = '19%' height = "35px" valign = "middle">
											Target name
										</td>
										<td height = "35px" valign = "middle">
											<input class = 'textbox' type = 'text' name = 'iscsi_target' value = '"""+random_target+"""' style = 'width:493px;'>
										</td>
									</tr>


				<tr><td>
				<!--<div><span id="button-one"><button type = 'submit'  name = 'action_butt' value = 'Create target' onclick = 'return validate_iscsi_target_form();'  style = ' background-color:#FFFFFF;border:none; float:right;  font-size: 86%; ' title="Create"><a style="font-size:85%; width:100%;"  >Create Target</a></button></span></div>-->
	<div>
	<td style="float: right;">
	<button class = 'buttonClass' type="submit" name = 'action_butt' value = 'Create target' onclick = 'return validate_iscsi_target_form();'>Create</button></td>

	</div>

	</td>
				</tr>
				</table>
				</form>
		   </div>"""


	print"""
		  </div>
		</div>
		<!--form container ends here-->
		<p>&nbsp;</p>
	</div>"""
else:
	print "<div style = 'margin-top: 10%; margin-bottom: 10%; margin-left: auto; margin-right: auto; text-align: center; vertical-align: center; color: darkred; font: 16px Arial;'>Check the 'Enable/Disable i-SCSI' option in Maintenance -><a href ='#'style ='text-decoration:underline;'>Services</a>.</div>"

print"""
"""
