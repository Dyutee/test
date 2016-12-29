#!/usr/bin/python

import cgitb, sys, cgi, include_files, os
cgitb.enable()
sys.path.append('../modules/')
import disp_except;
try:

	import os, commands, cgi, common_methods

	sys.path.append('/var/nasexe/python/')
	import tools
	from tools import shutdown
	from tools import db
	
	check_ha = tools.check_ha()

	form = cgi.FieldStorage()

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
	#-----------------------------Shutdown Code start ---------------------------
	querystring=form.getvalue('querystring')
	#print querystring
	# ---------------Get the button name "shutdown" and called the backend shutdown()---------------------------------- 
	if(form.getvalue('shutdown')):
		#status = shutdown.shutdown()
		print """<script>parent.location.href = 'login.py?sd=yes';</script>"""
		if(status == 0):
			print""" <div id = 'id_trace' >"""
			print "Shutdown Successfull !"
			print "</div>"
			logstatus = common_methods.sendtologs('Success', 'Successfully Shutdown', 'shutdown.py', str(status));
			#print "<script>location.href = 'iframe_shutdown.py#tabs-1';</script>"
			print """<script>location.href = 'main.py?page=sd&"""+querystring+"""#tabs-1';</script>"""
			#print """<script>location.href = 'shutdown.py';</script>"""
		else:
			print """<div id = 'id_trace_err'>"""
			print "Error ocured!"
			print "</div>"
			logstatus = common_methods.sendtologs('Error', 'Shutdown Failed', 'shutdown.py', str(status));
			#print "<script>location.href = 'iframe_shutdown.py#tabs-1';</script>"
			print """<script>location.href = 'main.py?page=sd&"""+querystring+"""#tabs-1';</script>"""
			#print """<script>location.href = 'shutdown.py';</script>"""
	#---------------------End-----------------------------------------
	#------------------Reboot code Start -------------------------------------
	# ---------------Get the button name "reboot_but" and called the backend reboot()----------------------------------
	if(form.getvalue('reboot_but')):
		status = shutdown.reboot()
		if(status == 0):
			print""" <div id = 'id_trace' >"""
			print "Reboot Successfull !"
			print "</div>"
			logstatus = common_methods.sendtologs('Success', 'Successfully Reboot', 'shutdown.py', str(status));
			#print "<script>location.href = 'iframe_shutdown.py#tabs-1';</script>"
			print """<script>location.href = 'main.py?page=sd&"""+querystring+"""#tabs-1';</script>"""
		else:
			print """<div id = 'id_trace_err'>"""
			print "Error ocured!"
			print "</div>"
			logstatus = common_methods.sendtologs('Error', 'Error Occurred while Rebooting', 'shutdown.py', str(status));
			#print "<script>location.href = 'iframe_shutdown.py#tabs-1';</script>"
			print """<script>location.href = 'main.py?page=sd&"""+querystring+"""#tabs-1';</script>"""
	#--------------------------End----------------------------------

	#print 'Content-Type: text/html'


	#----------------------Schedule shutdown Remove-----------------------------
	#----------------Get the button name from form "remove_sched" and get a time from form name "hid_time" ,then call a function for scheduled shutdown and pass a argument of "hid_time in function.After calling this function Scheduled Shutdown Information is removed."
	sys.path.append('/var/nasexe/python/tools/')
	import schedule_shutdown
	if(form.getvalue("remove_sched")):
		get_time = form.getvalue("hid_time")
		remove_status = schedule_shutdown.remove_schecule_shutdown_script(get_time, debug=False)

		if(remove_status == True):
			print "<div id='id_trace'>"
                        print "successfully remove the Scheduled shutdown!"
                	print "</div>"
			#print "<script>location.href = 'iframe_shutdown.py#tabs-2';</script>"
		else:
			print "<div id='id_trace_err'>"
                        print "Error Occurred while deleting Shutdown Scheduled!"
                	print "</div>"
			#print "<script>location.href = 'iframe_shutdown.py#tabs-2';</script>"
		print "<script>location.href = 'iframe_shutdown.py#tabs-2';</script>"

	#------------------------------End-----------------------------------------
	#----------------------Schedule Reboot Remove-----------------------------
	#----------------Get the button name from form "remove_sched_reboot" and get a time from form name "hid_time" ,then call a function for scheduled Reboot pass a argument of "hid_time in function.After calling this function Scheduled Reboot Information is removed."
	sys.path.append('/var/nasexe/python/tools/')
	import schedule_reboot
	if(form.getvalue("remove_sched_reboot")):
		get_time = form.getvalue("hid_time")
		#print get_time
		remove_status = schedule_reboot.remove_schecule_reboot_script(get_time, debug=False)

		if(remove_status == True):
			print "<div id='id_trace'>"
                        print "successfully remove the Reboot Scheduled !"
                	print "</div>"
			#print "<script>location.href = 'iframe_shutdown.py#tabs-2';</script>"
		else:
			print "<div id='id_trace_err'>"
                        print "Error Occurred while deleting Reboot Scheduled!"
                	print "</div>"
			#print "<script>location.href = 'iframe_shutdown.py#tabs-2';</script>"
		print "<script>location.href = 'iframe_shutdown.py#tabs-3';</script>"

	#------------------------------End-----------------------------------------

	#----------------------Schedule Shutdown and Reboot List Information-------------------------
	
	get_value=schedule_shutdown.get_all(debug=False)
	#print  get_value
	#exit()
	get_value_reboot=schedule_reboot.get_all(debug=False)
	#print get_value

	#--------------------------End-----------------------------------------------
	#import left_nav
	print
	print """
		<head>
                <script type="text/javascript">
                $(document).ready(function() {
                $(".various").fancybox({
                        maxWidth        : 800,
                        maxHeight       : 600,
                        fitToView       : false,
                        width           : '100%',
                        height          : '98%',
                        autoSize        : false,
                        closeClick      : false,
                        openEffect      : 'none',
                        closeEffect     : 'none',
                        'afterClose':function () {
                          window.location.reload();
                         },
                        helpers   : { 
                        overlay  :       {closeClick: false} // prevents closing when clicking OUTSIDE fancybox 
                                     }
                        
               });

                });
                </script>
		
		</head>
		<div id="loader-div" style="text-align:center; display:none;" ><img style="margin-top:20%;" src="../images/ajax-loader.gif" /><br/> Loading...</div>
	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer" id="body-div">
		<!--tab srt-->
		<div class="searchresult-container">
		<div style="margin:0 0 0px 0;" class="topinputwrap-heading"><a class="demo" href ="#"><img src ="../images/help_icon1.png" style="width:13px;"><span class="tooltip" >
                 <table border="0">
        <tr>     
        <td class="text_css">This page allows you to shutdown or reboot your FS2 system. It also lets you schedule shutdowns or reboots at specific intervals.</td>
        </tr>
        </table>"""
	if(check_ha == True):
		print"""
	</span></a><p class = "gap_text">Shutdown Information ("""+show_tn+""")</p>
                <span style="float:right; margin:-15px 0px 0 0;"><a onclick="return onclick_loader();" class="resource_links" href="https://"""+other_node_ip+"""/fs4/py/iframe_shutdown.py">"""+show_on+"""</a></span>
                </div>"""
	else:
		print"""</span></a><p class = "gap_text">Shutdown Information</p> </div>"""
	print"""

		  <div class="infoheader">
		    <div id="tabs">
		      <ul>
			<li><a href="#tabs-1">Shutdown/Reboot</a></li>
			<li><a href="#tabs-2">Schedule Shutdown Information</a></li>
			<li><a href="#tabs-3">Schedule Reboot Information</a></li>
			<!--<li><a href="#tabs-4">Disk Information</a></li>-->
		      </ul>
		      <div id="tabs-1">

		<!--form container starts here-->
		<div class="form-container">
		  <div class="inputwrap">
		   <div class="formleftside-content">

	<style>
	#proppopUpDiv2 {position: fixed; background-color: #fff; width: 500px; z-index: 9002; padding: 5px;}
        #proppopUpDiv2 h5{width:100%; font-size:15px; color:#0070bd; text-align:center; font-weight:bold;}
        #proppopUpDiv2 span{ color:#FFFFFF; background-color:#0070bd; padding:1px 3px 0 3px; float:right;}
        #proppopUpDiv2 ul.idTabs{list-style:none; border:none; width:400px; margin:5px 0 0 0;}
        #proppopUpDiv2 ul.idTabs li{display:inline;}
        #proppopUpDiv2 ul.idTabs li a.link_tabs{display:inline; border:none; background-color:#D1D1D1; padding:10px;}
        #proppopUpDiv2 ul.idTabs li a.link_tabs:hover{background-color:#cfbdbd;}

	#proppopUpDiv3 {position: fixed; background-color: #fff; width: 500px; z-index: 9002; padding: 5px;}
        #proppopUpDiv3 h5{width:100%; font-size:15px; color:#0070bd; text-align:center; font-weight:bold;}
        #proppopUpDiv3 span{ color:#FFFFFF; background-color:#0070bd; padding:1px 3px 0 3px; float:right;}
        #proppopUpDiv3 ul.idTabs{list-style:none; border:none; width:400px; margin:5px 0 0 0;}
        #proppopUpDiv3 ul.idTabs li{display:inline;}
        #proppopUpDiv3 ul.idTabs li a.link_tabs{display:inline; border:none; background-color:#D1D1D1; padding:10px;}
        #proppopUpDiv3 ul.idTabs li a.link_tabs:hover{background-color:#cfbdbd;}

	</style>

	<div style="display: none;" id="blanket"></div>
        <form name="delete_share_form" method="post" target="_parent" action="system-down.py">
        <div style="display: none;" id='proppopUpDiv2'>
        <h5>Confirm Box<span onclick="popup('proppopUpDiv2')" style="cursor:pointer;">X</span></h5>
        <div style="text-align:center; height:70px; margin:20px 0 20px 0;">
        Are you sure you want to shutdown ?<br/><br/>
	<input type="hidden" name="hid_top_val" value="syes" />
        <button class="button_example" type="button" name = 'local_action_but'  id = 'local_action_but' value = 'Update' style="float:right; margin:0px 200px 0 0; " onclick="popup('proppopUpDiv2')" >No</button>
        <button class="button_example" type="submit" name = 'shutdown'  id = 'shutdown' value = 'shutdown' style="float:right; " >Yes</button>
        </div>
        </form>

        </div>

        <form name="restart_share_form" method="post" action="">
        <div style="display: none;" id='proppopUpDiv3'>
        <h5>Confirm Box<span onclick="popup('proppopUpDiv3')" style="cursor:pointer;">X</span></h5>
        <div style="text-align:center; height:70px; margin:20px 0 20px 0;">
        Are you sure you want to restart ?<br/><br/>
        <button class="button_example" type="button" name = 'local_action_but'  id = 'local_action_but' value = 'Update' style="float:right; margin:0px 200px 0 0; " onclick="popup('proppopUpDiv3')" >No</button>
        <button class="button_example" type="submit" name = 'reboot_but'  id = 'reboot_but' value = 'reboot_but' style="float:right; " >Yes</button>
        </div>
        </form>
        </div>


<form name='form_nm' method='post' action='shutdown.py'>
	<table width = "685" border = "0" cellspacing = "0" cellpadding = "0" name = 'disp_tables'>
		<tr>
			<td height = "70px" valign = "middle"  align = 'center'>

		<a onclick="popup('proppopUpDiv2')" href="#"><img src="../images/remote_shutdown.png" alt="Shutdown" height="60" width="60" title="Shutdown"><br/>Shutdown</a>
	<br/>
							</td>
			<td width = "311"  height = "70px" valign = "middle" align = 'center'>
										<!--<button type="submit" id="submit" name="reboot_but" value = 'reboot' style = 'background: #fff; border: 0px;cursor:pointer;margin-left:-47%;' title="reboot" onclick ="return confirm('Do you want to Reboot the System')";><img src="../images/remote_reboot.png" alt="reboot" height="60" width="60" title="Reboot"><br>Reboot</button>-->
		
		<a onclick="popup('proppopUpDiv3')" href="#"><img src="../images/remote_reboot.png" alt="reboot" height="60" width="60" title="Reboot"><br/>Reboot</a>
										<!--<input class = 'input1' type = 'image' src = '../images/remote_reboot.png' height = '60' width = '60' style = 'background: #fff; border: 0px;' name = 'reboot_but' value = 'Restart'>--><BR>
			</td>

		<td>
			<a class="various" data-fancybox-type="iframe" style="color:#666666;text-decoration:none;" href="schedule_shudown.py"><img src = "../images/scheduler.jpg" height = '60' width = '60' style = 'background: #fff; border: 0px;margin-left:-51%;' name = 'action_but' "Schedule Shutdown", "dialogWidth: 750px; dialogHeight: 300px; resizable:0;" title="Schedule Shutdown");'><sup><img src = '../images/remote_shutdown.png' height = '30' width = '30'/></sup></a><br/><p style="text-indent:-63px;">Schedule shutdown</p>

		</td>

		<td width = "311"  height = "70px" valign = "middle"  align = 'center'>

			<a class="various" data-fancybox-type="iframe" style="color:#666666;text-decoration:none;" href="schedule_restart.py"><img src = "../images/scheduler.jpg" height = '60' width = '60' title="Schedule Reboot"><sup><img src = '../images/remote_reboot.png' height = '30' width = '30'/></sup></a><br/><p>Schedule Restart</p>

			</td>
		</tr>
	</table>
</form>

		</div>
		  </div>
		</div>
		<!--form container ends here-->
		<p>&nbsp;</p>
		      </div>

<div id="tabs-2">

                <!--form container starts here-->
                <div class="form-container">
                  <div class="inputwrap">
                   <div class="formleftside-content">
		<form name = "remove_form" action="" method ="post">
        <table width = "680" style="margin-top: 13%;">
                <tr>
                <th style="border:#D1D1D1 1px solid;width:22%;">Type</th>
                <th style="border:#D1D1D1 1px solid;">Schedule</th>
                <th style="border:#D1D1D1 1px solid;">Time</th>
                <th style="border:#D1D1D1 1px solid;">Delete</th>
                </tr>"""
	if(get_value !=[]):
                for sched_shut_info in get_value:
			#print '<br/>'
			tr = sched_shut_info.has_key('trigger')
			if(tr == False):
				type_info = ''
			else:
				type_info = sched_shut_info['trigger']
			type_info = type_info.replace("'", "")
			type_info = type_info.replace("SCHEDULE", "")
			sch_time = sched_shut_info['scheduler_time']
			#print sch_time
			time_info = sched_shut_info['time']
			#print time_info
			decode_sch = tools.decode_schedule(sched_shut_info['scheduler_time'])
			#decode_sch = tools.decode_schedule(sched_shut_info['scheduler_time'])
			#print '<br/>'
			#decode_sch = decode_sch.replace("'", "")
			#print type_info
			print"""
			<form name="remove_shut" method="post" action="" />
                        <tr>
			<input type = "hidden" name = "hid_time" value ='"""+time_info+"""'>
			<td style = "text-align:center;border:#D1D1D1 1px solid;"><img src="../images/sched_snap_img2.gif" style="margin-top: 15%;"><br/>"""+type_info+"""</td>
                        <td style = "text-align:center;border:#D1D1D1 1px solid;">"""+decode_sch+"""</td>
                        <td style = "text-align:center;border:#D1D1D1 1px solid;">"""+time_info+"""</td>
			<td style="float:right;width:98%;height:88px;margin-top:-3%;text-align:center;border:#D1D1D1 1px solid;"><button type="image" value = "remove" name='remove_sched' style="background: #fff; border: 0px;cursor:pointer;margin-top:28%;" ><img src="../images/snap_del_but.jpg" style="margin-top: 15%;"></button></td> 
			</tr>
			</form>"""
	else:
       		print"""<tr>
                <td style="border:#D1D1D1 1px solid;padding-top: 3%; text-align: center;" colspan = "7"><span>No Schedule Information is Available</span></td>
                </tr>"""
	
	

	print"""</table></form>
			
	
</div>
   </div>
                </div>
                <!--form container ends here-->
                <p>&nbsp;</p>
                      </div>
<div id="tabs-3">

                <!--form container starts here-->
                <div class="form-container">
                  <div class="inputwrap">
                   <div class="formleftside-content">
		<form name = "remove_form1" action="" method ="post">
        <table width = "680" style="margin-top: 13%;">
                <tr>
                <th style="border:#D1D1D1 1px solid;width:22%;">Type</th>
                <th style="border:#D1D1D1 1px solid;">Schedule</th>
                <th style="border:#D1D1D1 1px solid;">Time</th>
                <th style="border:#D1D1D1 1px solid;">Delete</th>
                </tr>"""
	if(get_value_reboot !=[]):
                for sched_shut_info in get_value_reboot:
			#print sched_shut_info
			#type_info = sched_shut_info['trigger']
			tr = sched_shut_info.has_key('trigger')
                        if(tr == False):
                                type_info = ''
                        else:
                                type_info = sched_shut_info['trigger']
			type_info = type_info.replace("'", "")
			type_info = type_info.replace("SCHEDULE", "")
			sch_time = sched_shut_info['scheduler_time']
			#print sch_time
			time_info = sched_shut_info['time']
			#print time_info
			decode_sch = tools.decode_schedule(sched_shut_info['scheduler_time'])
			#decode_sch = tools.decode_schedule(sched_shut_info['scheduler_time'])
			#print '<br/>'
			#decode_sch = decode_sch.replace("'", "")
			#print type_info
			print"""
			<form name="remove_shut" method="post" action="" />
                        <tr>
			<input type = "hidden" name = "hid_time" value ='"""+time_info+"""'>
			<td style = "text-align:center;border:#D1D1D1 1px solid;"><img src="../images/sched_snap_img2.gif" style="margin-top: 15%;"><br/>"""+type_info+"""</td>
                        <td style = "text-align:center;border:#D1D1D1 1px solid;">"""+decode_sch+"""</td>
                        <td style = "text-align:center;border:#D1D1D1 1px solid;">"""+time_info+"""</td>
			<td style="float:right;width:98%;height:88px;margin-top:-3%;text-align:center;border:#D1D1D1 1px solid;"><button type="image" value = "remove" name='remove_sched_reboot' style="background: #fff; border: 0px;cursor:pointer;margin-top:28%;" ><img src="../images/snap_del_but.jpg" style="margin-top: 15%;"></button></td> 
			</tr>
			</form>"""
	else:
       		print"""<tr>
                <td style="border:#D1D1D1 1px solid;padding-top: 3%; text-align: center;" colspan = "7"><span>No Schedule Information is Available</span></td>
                </tr>"""
	
	

	print"""</table></form>
			
	
</div>
   </div>
                </div>
                <!--form container ends here-->
                <p>&nbsp;</p>
                      </div>	
	"""
except Exception as e:
	disp_except.display_exception(e);
