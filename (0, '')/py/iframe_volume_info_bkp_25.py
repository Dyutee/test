#!/usr/bin/python
import cgitb, sys, common_methods, include_files
cgitb.enable()
sys.path.append('../modules/')
import disp_except;
try:
	import cgitb, os, cgi, sys, commands, opslag_info, system_info
        cgitb.enable()

        sys.path.append('/var/nasexe/storage/')

        import storage_op
        from lvm_infos import *
        from functions import *

        sys.path.append('/var/nasexe/storage/')
        import storage_op

        from lvm_infos import *;
        from functions import *

        vg_info  = get_vgs()
        nas_info = get_lvs()
        free_d   = free_disks()

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


	print
	print """
		<div id="loader-div" style="text-align:center; display:none;" ><img style="margin-top:20%;" src="../images/ajax-loader.gif" /><br/> Loading...</div>
	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer" id="body-div">
		<!--tab srt-->
		<div class="searchresult-container">
		  <div class="infoheader">
		<div class="topinputwrap-heading">

		<a class="demo" href ="#"><img src ="../images/help_icon1.png" style="width:13px;"><span class="tooltip" >
                 <table border="0">
        <tr>
        <td style="font-size: medium;text-align:start;">Volume Information:</td>
        
        </tr>

        <tr>     
        <td class="text_css">In this Page Displays the information of Volume Like ,Volume Name ,Total Space and Free Space.</td>
        </tr>
        </table>"""
	if(check_ha == True):
		print"""</span></a>
	Volume Information of """+show_tn+"""
                <span style="float:right; margin:5px 0px 0 0;"><a onclick="return onclick_loader();" class="resource_links" href="https://"""+other_node_ip+"""/fs4/py/iframe_volume_info.py">"""+show_on+"""</a></span></div>"""
	else:
		 print"""</span></a>Volume Information of """+show_tn+"""
                </div>"""
	print """
		    <!--<div id="tabs">
		      <ul>
			<li><a href="#tabs-1">Volume Info</a></li>
		      </ul>-->
		      <div id="tabs-1">

		<!--form container starts here-->
		<div class="iframe-form-container">"""
	multi = 1;

        if(vg_info["vgs"]!=[{}]):

                print"""
                        
                        <div class="inputwrap">
                        <div class="formleftside-content" style ="color:DarkOliveGreen;font-family: menu;"><b>Volume Name</b></div>
                        <div class="formleftside-content" style ="color:DarkOliveGreen;font-family: menu;"><b>Total Space</b></div>
                        <div class="formleftside-content" style ="color:DarkOliveGreen;font-family: menu;"><b>Free Space</b></div></div>"""
                for x in vg_info["vgs"]:
                        new_free   = x["free_size"]
                        total_size = x["size"]

                        if (total_size.find('g') > 0):
                                size = total_size.replace("g", "");

                        if (total_size.find('t') > 0):
                                multi = 1024;
                                size = total_size.replace("t", "")

                        size = float(size) * multi;
                        size = str(size) + 'GB';
			if (new_free.find('g') > 0):
                        	free_size = new_free.replace("g", "");
                                free_size = new_free.replace("g", "")

                        if (new_free.find('t') > 0):
                                multi = 1024;
                                free_size = new_free.replace("t", "")

                        free_size = float(free_size) * multi;
                        free_size = str(free_size) + 'GB';

                        print"""<div class="inputwrap">
                        <div class="formrightside-content" style ="margin-left:7%;margin-top:1%;">"""+x["vg_name"]+"""</div>
                        </div>
                        <div class="inputwrap">
                        <div class="formrightside-content" style ="margin-left:3%;margin-top:-3%;text-align:center;">"""+size+"""</div>
                        </div>
                        <div class="inputwrap">
                        <div class="formrightside-content" style ="margin-top:-4%;text-align:right;margin-left:1%;">"""+free_size+"""</div>
                        </div>"""
	else:
        	print "<div style = 'padding:20px 0 0 267px; font-size:12px;text-decoration:underline;'><a href ='main.py?page=rs'>No Volume is Created</a> !</div>"
	print"""
</div>
	</div>
		</div>
			</div>
	
         <p>&nbsp;</p>
         	</div>
                        
                  	</div>
                		</div>
	"""
except Exception as e:
        disp_except.display_exception(e);
