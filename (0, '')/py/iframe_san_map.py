#!/usr/bin/python
import cgitb, sys, common_methods, include_files, cgi
cgitb.enable()
sys.path.append('../modules/')
import disp_except;
try:
	
	
	sys.path.append('/var/nasexe/python/')
	import tools
	from tools import scan_remount
	from tools import db
	#from tools import 
	form = cgi.FieldStorage()

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
	print
	print """
		<div id="loader-div" style="text-align:center; display:none;" ><img style="margin-top:20%;" src="../images/ajax-loader.gif" /><br/> Loading...</div>
	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer" id="body-div">
		<!--tab srt-->
		<div class="searchresult-container">
		 <div style="margin:0 0 0px 0;" class="topinputwrap-heading"><a class="demo" href ="#"><img src ="../images/help_icon1.png" style="width:13px;"> <span class="tooltip" >
                 <table border="0">
        <tr>
        <td style="font-size: medium;text-align:start;">Srp Map  Information:</td>
        </tr>
        <tr>     
        <td class="text_css">In this Page Discussed about the Srp mapping.In the first tab select the source target, destination Target and node name, when apply on the button then the mapping is done.In the Second tab listing of srp mapping </td>
        </tr>
        </table>"""
	if(check_ha == True):
		print"""
	</span></a>

San Advance Information ("""+show_tn+""")
                <span style="float:right; margin:0 0px 0 0;"><a onclick="return onclick_loader();" class="resource_links" href="https://"""+other_node_ip+"""/fs4/py/iframe_san_map.py">"""+show_on+"""</a></span>

                </div>"""
	else:
		print"""</span></a>San Advance Information </div>"""
	print"""
		  <div class="infoheader">
		    <div id="tabs">
		      <ul>
			<li><a href="#tabs-1">San</a></li>
		      </ul>
		      <div id="tabs-1">

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

		<!--<table  width = "685" bgcolor="#f5f5f5" border = "0"  cellspacing = "0" cellpadding = "0" class = 'outer_border'>
									<tr>


		<td width = "311" class = "table_content" height = "70px" valign = "middle" bgcolor = "#f5f5f5" align = 'center'>

	<form name='form1' method='post' action=''>

	<a onclick="popup('proppopUpDiv4')" href="#"><img src="../images/scan.png"  height="60" width="60" title="Scan"></a>
	</form>
								      </td>
								    </tr>
							      </table>-->

		</div>
		  </div>
		</div>
		<!--form container ends here-->
		<p>&nbsp;</p>
		      </div>
	"""
except Exception as e:
        disp_except.display_exception(e);
