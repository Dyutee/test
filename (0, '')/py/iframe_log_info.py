#!/usr/bin/python
import cgitb, sys, common_methods, include_files, cgi
cgitb.enable()
sys.path.append('../modules/')
import disp_except;
try:
	
	select_user = ''
	get_value = ''
	action1 = ''
	trigger = ''
	time = ''
	sched_time = ''
	#get_value['launcher_scripts'] = ''
	#-----------------Import backend modules------------------------------------
	sys.path.append('/var/nasexe/python/')
	import tools
	import launcher
	from tools import scan_remount
	from tools import db
	#--------------------------End------------------------------------------------
	#from tools import 
	
	#--------------------------------Chceck ha status-----------------------------
	check_ha = tools.check_ha()
	#---------------------------------------End-----------------------------------
	form = cgi.FieldStorage()
	#--------------------------------Get node name--------------------------------
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
	#----------------------------End------------------------------------------------

	#-------------Script-----------------------------

	
	
	#---------------------End-------------------
	#-----------------Get the user Information--------------------
	arr_info = []
	if(form.getvalue("user_name")):
		select_user = form.getvalue("user_name")
		select_user = select_user.strip()
		get_value = launcher.get(user=select_user)

		if(get_value['id'] == 0):
			print"""<div id = 'id_trace'>"""
                        print "Successfully get the "+select_user+" Information!"
                        print "</div>"

		else:
			print"""<div id = 'id_trace_err'>"""
                        print "Error occured while getting the "+select_user+" Information!"
                        print "</div>"

		for script_st  in get_value['launcher_scripts']:
			script_n =  script_st['script_name']
			arr_info.append(script_st)
	#print 'Value:'+str(arr_info)

	#exit();
	#--------------------End---------------------
	#print get_info1
	#exit()
	
	#import left_nav
	print
	print """
		<!-- <style>
                table { margin: 1em; border-collapse: collapse; }
                td, th { padding: .3em; border: 1px #ccc solid; }
                td { text-align:center;}
                </style>-->

		<div id="loader-div" style="text-align:center; display:none;" ><img style="margin-top:20%;" src="../images/ajax-loader.gif" /><br/> Loading...</div>
	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer" id="body-div">
		<!--tab srt-->
		<div class="searchresult-container">
		 <div style="margin:0 0 0px 0;" class="topinputwrap-heading"><a class="demo" href ="#"><img src ="../images/help_icon1.png" style="width:13px;"><span class="tooltip" >
                 <table border="0">
        <tr>     
        <td class="text_css">The page lets you view the different tasks performed by FS2 in the background, and the triggers for those tasks.</td>
        </tr>
        </table>"""
	if(check_ha == True):
		print"""
	</span></a><span style="margin-left:5px;color:#fff;">Tasks ("""+show_tn+""")</span>
                <span style="float:right; margin:0 0px 0 0;"><a onclick="return onclick_loader();" class="resource_links" href="https://"""+other_node_ip+"""/fs4/py/iframe_log_info.py">"""+show_on+"""</a></span>

                </div>"""
	else:
		print""" </span></a>Log Information </div>"""
	print"""
		  <div class="infoheader">
		    <!--<div id="tabs">
		      <ul>
			<li><a href="#tabs-1">Log </a></li>
		      </ul>
		      <div id="tabs-1">-->

		<!--form container starts here-->
		<div class="form-container">
		  <div class="inputwrap">
		    <div class="formleftside-content">
	<style>
        #proppopUpDiv4 {position: fixed; background-color: #fff; width: 500px; z-index: 9002; padding: 5px;}
        #proppopUpDiv4 h5{width:100%; font-size:15px; color:#0070bd; text-align:center; font-weight:bold;}
        #proppopUpDiv4 span{ color:#FFFFFF; background-color:#0070bd; padding:1px 3px 0 3px; float:right;}
        #proppopUpDiv4 ul.idTabs{list-style:none; border:none; width:400px; margin:5px 0 0 0;}
        #proppopUpDiv4 ul.idTabs li{display:inline;}
        #proppopUpDiv4 ul.idTabs li a.link_tabs{display:inline; border:none; background-color:#D1D1D1; padding:10px;}

        </style>
	
	<div style="display: none;" id="blanket"></div>
        <form name="delete_share_form" method="post" action="">
        <div style="display: none;" id='proppopUpDiv4'>
        <h5>Confirm Box<span onclick="popup('proppopUpDiv4')" style="cursor:pointer;">X</span></h5>
        <div style="text-align:center; height:70px; margin:20px 0 20px 0;">
        Are you sure you want to scan Volume?<br/><br/>
        <button class="button_example" type="button" name = 'local_action_but'  id = 'local_action_but' value = 'Update' style="float:right; margin:0px 200px 0 0; " onclick="popup('proppopUpDiv4')" >No</button>
        <button class="button_example" type="submit" name = 'scan_volume'  id = 'scan' value = 'scanvolume' style="float:right; " >Yes</button>
        </div>
        </form>

        </div>


	<form name='form1' method='post' action=''>
		
	<table style="width:500px;">
                <tr>
                <td>Select User:</td>
                <td>
                <div class="styled-select2">
                <select name="user_name" onchange='this.form.submit()' >
                <option >Select User</option>
		
        <option value='user' """
	if (select_user == "user"):
                print "selected = selected"
	
	print""">User</option>
                <option value='sys' """
	if (select_user == "sys"):
                print "selected = selected"

	print""">Sys</option>"""


        print """</select></div>
                </tr>
		</table>

		<table width = "698" >
		<th  style="padding: .3em; border: 1px #ccc solid;">Action</th>
		<th  style="padding: .3em; border: 1px #ccc solid;">Trigger</th>
		<th  style="padding: .3em; border: 1px #ccc solid;">Time</th>
		<th  style="padding: .3em; border: 1px #ccc solid;">scheduler Time</th>"""
	#if(get_value !=[]):
	#	print get_value
	#	for z in get_value['launcher_scripts'][0]:
	#		print z
	#		action = z['script']
	#		print action
	#		
	#		exit();
			#trigger_n = z['trigger']
			#time_n = z['time']
			#sched_time = z['scheduler_time']
			#print"""
	#--------------------------display the log information value --------------------------------
	for z in arr_info:
		if(z["db_entry"] == True):
			act = z.has_key('action1')
			if(act == False):
				action= ''
			else:
				action =  z['action1']
				action = action.replace("'", "")
			
			tme = z.has_key('time')
			if(tme == False):
				time = ''
			else:
				time =  z['time']
			
			trg = z.has_key('trigger')
			if(trg == False):
				trigger = ''
			else:
				trigger=  z['trigger']
				trigger = trigger.replace("'", "")
			sch = z.has_key('scheduler_time')
			if(sch == False):
				sched_time = ''
			else:
				sched_time =  z['scheduler_time']
			decode_sched = tools.decode_schedule(sched_time)
	#--------------------------------------------End------------------------------------------------
			print"""<tr>

				<td style = "text-align:center;border:#D1D1D1 1px solid;">"""+action+"""</td>
				<td style = "text-align:center;border:#D1D1D1 1px solid;">"""+trigger+"""</td>
				<td style = "text-align:center;border:#D1D1D1 1px solid;">"""+time+"""</td>
				<td style = "text-align:center;border:#D1D1D1 1px solid;">"""+decode_sched+"""</tad>



				</tr>"""


	print"""
		
		</table>
		<input type = "hidden" name="user_name" />
	   <!--<button type="image" value = "scan_volume" name="scan_volume" style="background: #fff; border: 0px;cursor:pointer;" onclick ="return confirm('Do you want to Scan Volume')"; ><img src="../images/scan.png" height = '60' width = '60'></button><br/>-->
	<!--<a onclick="popup('proppopUpDiv4')" href="#"><img src="../images/scan.png"  height="60" width="60" title="Scan"></a>-->
	</form>

		</div>
		  </div>
		</div>
		<!--form container ends here-->
		<p>&nbsp;</p>
		      </div>
	"""
except Exception as e:
        disp_except.display_exception(e);
