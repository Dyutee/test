#!/usr/bin/python

import cgitb, sys, os, common_methods, include_files, cgi
cgitb.enable()

sys.path.append('../modules/')
import disp_except;

try:
	#-------------------Import backend modules----------------------------
	sys.path.append('/var/nasexe/python/')
	import tools
	from tools import scan_remount
	from tools import db
	#----------------------------------End--------------------------------
	form = cgi.FieldStorage()
	#----------------Check ha----------------------------------------------
	check_ha = tools.check_ha()
	#-----------------------End--------------------------------------------
	#-------------------------Get Node name--------------------------------
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
	#--------------------------------End--------------------------------------
	#-------------------------------Remount code start here-----------------------------------------------------
	#---------------------------Get a button name from form and call the backend function onclick of button--------------------------
	if(form.getvalue("remount")):
		remount_status = scan_remount.remount()

		if(remount_status == 0):
			print""" <div id = 'id_trace' >"""
			print "Remount Successfull !"
			print "</div>"
			logstatus = common_methods.sendtologs('Success', 'volume Successfully Remount', 'remount.py', str(remount_status));
		else:
			print """<div id = 'id_trace_err'>"""
			print "Error ocured during Remount!"
			print "</div>"
			logstatus = common_methods.sendtologs('Error', 'Error Occurred while Remount the Volume', 'remount.py', str(remount_status));
	#----------------------------------------------------------End------------------------------------------------------------------------

	#import left_nav
	print
	print """
		<div id="loader-div" style="text-align:center; display:none;" ><img style="margin-top:20%;" src="../images/ajax-loader.gif" /><br/> Loading...</div>
	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer" id="body-div">
		<!--tab srt-->
		<div class="searchresult-container">
		<div style="margin:0 0 0px 0;" class="topinputwrap-heading"><a class="demo" href ="#"><img src ="../images/help_icon1.png" style="width:13px;"><span class="tooltip" >
                 <table border="0">
        <tr>     
        <td class="text_css">This page helps you remount the volumes retrieved using the "Scan Volume" option.</td>
        </tr>
        </table>"""
	if(check_ha == True):
		print"""
	</span></a><span  style="color:#fff;margin-left:7px;">Remount Information ("""+show_tn+""")</span>
                <span style="float:right; margin:0 0px 0 0;"><a onclick="return onclick_loader();" class="resource_links" href="https://"""+other_node_ip+"""/fs4/py/iframe_remount.py">"""+show_on+"""</a></span>
                </div>"""
	else:
		print"""</span></a>Remount Information </div>"""
	print"""
		  <div class="infoheader">
		    <div id="tabs">
		      <!--<ul>
			<li><a href="#tabs-1">Remount</a></li>
		      </ul>-->
		      <div id="tabs-1">

		<!--form container starts here-->
		<!--<div class="form-container">-->
		  <div class="inputwrap">
		    <div class="formleftside-content">
		<style>
        #proppopUpDiv5 {position: fixed; background-color: #fff; width: 500px; z-index: 9002; padding: 5px;}
        #proppopUpDiv5 h5{width:100%; font-size:15px; color:#0070bd; text-align:center; font-weight:bold;}
        #proppopUpDiv5 span{ color:#FFFFFF; background-color:#0070bd; padding:1px 3px 0 3px; float:right;}
        #proppopUpDiv5 ul.idTabs{list-style:none; border:none; width:400px; margin:5px 0 0 0;}
        #proppopUpDiv5 ul.idTabs li{display:inline;}
        #proppopUpDiv5 ul.idTabs li a.link_tabs{display:inline; border:none; background-color:#D1D1D1; padding:10px;}

        </style>

	<div style="display: none;" id="blanket"></div>
        <form name="delete_share_form" method="post" action="">
        <div style="display: none;" id='proppopUpDiv5'>
        <h5>Confirm Box<span onclick="popup('proppopUpDiv5')" style="cursor:pointer;">X</span></h5>
        <div style="text-align:center; height:70px; margin:20px 0 20px 0;">
        Are you sure you want to Remount Volume?<br/><br/>
        <button class="button_example" type="button" name = 'local_action_but'  id = 'local_action_but' value = 'Update' style="float:right; margin:0px 200px 0 0; " onclick="popup('proppopUpDiv5')" >No</button>
        <button class="button_example" type="submit" name = 'remount'  id = 'remount' value = 'remount' style="float:right; " >Yes</button>
        </div>
        </form>

        </div>

		<table  width = "685" border = "0"  cellspacing = "0" cellpadding = "0" class = 'outer_border'>
									<tr>


		<td width = "311" class = "table_content" height = "70px" valign = "middle" align = 'center'>

	<form name='form1' method='post' action=''>
	
	<a onclick="popup('proppopUpDiv5')" href="#"><img src="../images/remount.png"  height="60" width="60" title="Remount"></a>

	   <!--<button type="image" value = "remount" name="remount" style="background: #fff; border: 0px;cursor:pointer;" ><img src="../images/remount.png" height = '60' width = '60' onclick ="return confirm('Do you want to Remount Volume')";></button><br/>-->
	</form>
								      </td>
								    </tr>
							      </table>

		</div>
		  </div>
		</div>
		<!--form container ends here-->
		<p>&nbsp;</p>	
			</div>
	"""

except Exception as e:
	disp_except.display_exception(e);
