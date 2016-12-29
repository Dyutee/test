#!/usr/bin/python

import traceback, sys, system_info, include_files
sys.path.append('../modules/')
import disp_except;
try:
	#################################################
        ################ import modules #################
        #################################################
        import cgitb,  os, sys, commands, common_methods, traceback, cgi
        cgitb.enable()
	form = cgi.FieldStorage()
	sys.path.append('/var/nasexe/python/')
	import tools
	from tools import db
        sys.path.append('/var/nasexe/storage/')
        import storage_op
        from lvm_infos import *
        from functions import *
        sys.path.append('/var/nasexe/')
        import storage
	#--------------------- END --------------------#

	################################################
        ################ Check HA Status ###############
        ################################################	
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
	
	################################################
        ################# Increase Size ################
        ################################################	
	if(form.getvalue("submit_update")):
                update_disk = form.getvalue("update_disk")
                update_size = form.getvalue("update_size")
                size_info = form.getvalue("size_info")
                size_info = size_info.replace('GB', '')
                increase_size = float(size_info)+float(update_size)
                increase_size = str(increase_size)+"GB"

                update_lv = storage_op.lv_increase(update_disk,increase_size)
		if(update_lv == True):
                        print""" <div id = 'id_trace' >"""
                        print "You Increase <font color = 'darkred'><b>"+str(update_size)+'GB'+" </b></font> of Size! Your Size <font color = 'darkred'><b>"+str(size_info)+'GB'+"</b></font> is successfully Updated to <font color = 'darkred'><b>"+increase_size+"</b></font>!"
                        print "</div>"
                else:
                        print""" <div id = 'id_trace_err' >"""
                        print "You Can't decrease the Size!"
                        print "</div>"
	#--------------------- END --------------------#

	#--- Get VGS
	vg_info = get_vgs()
	
	type_list=['NAS','BIO','FIO','VTL']
	st=storage_op.list_all_disks()
	get_vol_name = "ALL"
	get_vol_type = "ALL"

	condition = st
	condition_len = st
	array_len = len(condition_len)
	if(form.getvalue("volume_sel")):
		get_vol_name = form.getvalue("volume_sel")
		get_vol_type = form.getvalue("disk_type")
		subarray = []

		if((get_vol_name == "ALL") and (get_vol_type == "ALL")):
			condition = st
		
		elif((get_vol_name == "ALL") or (get_vol_type == "ALL")):
			if(get_vol_name == "ALL"):
				for u in condition:
					if (u['type'] == get_vol_type):
						subarray.append(u)

			if(get_vol_type == "ALL"):
				for u in condition:
					if (u['vg_name'] == get_vol_name):
						subarray.append(u)

			condition = subarray

		else:
			for u in condition:
				if (u['vg_name'] == get_vol_name):
					if (u['type'] == get_vol_type):
						subarray.append(u)

			condition = subarray

		array_len = len(condition)

        image_icon = common_methods.getimageicon();

        log_array = [];
        log_file = common_methods.log_file;
        logstring = '';
        vg = '';

        nas_info = get_lvs()

        ss = nas_info
        logstring = str(common_methods.now) + '<<>>From: ' + common_methods.remote_ip + '<<>>' + str(ss) + str("Retrieve lv info");
        log_array.append(logstring);
        common_methods.append_file(log_file, log_array);
	
	################################################
        ################# Delete Volume ################
        ################################################	
	if(form.getvalue("delete_but")):
                get_lv = form.getvalue("delete_option[]")
                check_get_lv =isinstance(get_lv, str)

                if(check_get_lv ==True):
                        remove_lv = storage_op.lvremove(get_lv)

                else:
                        get_lv = set(get_lv)
                        for value in get_lv:
                                remove_lv = storage_op.lvremove(value)

                ss = remove_lv
                logstring = str(common_methods.now) + '<<>>From: ' + common_methods.remote_ip + '<<>>' + str(ss) + str(" Deleting Volume");
                log_array.append(logstring);
                common_methods.append_file(log_file, log_array);

                if(remove_lv == True):
                        print"""<div id = 'id_trace'>"""
                        print " Disk <font color='darkred'><b>"+str(get_lv)+"</b></font> Successfully Deleted!"
                        print "</div>"
                else:
                        print"""<div id = 'id_trace_err'>"""
                        print "Error occured while deleting Disk <font color = 'darkred'><b>"+str(get_lv)+"</b></font> !"
                        print "</div>"
	#--------------------- END --------------------#

	#--- Get VGS	
	vg_info = get_vgs()
	#--- Get LVS
        nas_info = get_lvs()

	for free_vg in vg_info["vgs"]:
        	if(free_vg != {}):
                	free_vg = free_vg["free_size"]

	print
	print """

		<head>

		<!--<script src="new-tooltip/jquery.js"></script>
                        <script src="new-tooltip/lptooltip.js"></script>
                        <link rel='stylesheet' type='text/css' href='new-tooltip/lptooltip.css' />-->
                        <link rel="stylesheet" href="../fancyBox/source/jquery.fancybox.css" type="text/css" media="screen" />
                        <script type="text/javascript" src="../fancyBox/source/jquery.fancybox.pack.js"></script>
                        <script type="text/javascript">
        $(document).ready(function() {
        $(".various").fancybox({
                maxWidth        : 800,
                maxHeight       : 600,
                fitToView       : false,
                width           : '60%',
                height          : '68%',
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

<!--<meta http-equiv="Content-Type" content="text/html; charset=utf-8">-->
        <!--<link rel="stylesheet" href="style.css" type="text/css">-->
        <script src="../js/amcharts.js" type="text/javascript"></script>
        <script src="../js/pie.js" type="text/javascript"></script>
		
		</head>


		<div id="loader-div" style="text-align:center; display:none;" ><img style="margin-top:20%;" src="../images/ajax-loader.gif" /><br/> Loading...</div>		
	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer" style="width:740px;" id="body-div">
		<!--tab srt-->
		<div class="searchresult-container">
		 <div style="margin:0 0 0px 0;" class="topinputwrap-heading"><a class="demo" href ="#"><img src ="../images/help_icon1.png" style = "width:13px;"><span class="tooltip" >
                 <table border="0">
        <tr>
        <td class="text_css">This page shows the available volumes and used/free spaces on those volumes. It also allows users to create new NAS, VTL, BIO and FIO disks on those volumes.</td>
        </tr>
        </table>"""
	if(check_ha == True):
		print"""</span></a><span class = "gap_text" style="color:#fff;margin-left:7px;">Volume Information ("""+show_tn+""")</span>
                <span style="float:right; margin:0 0px 0 0;"><a onclick="return onclick_loader();" class="resource_links" href="https://"""+other_node_ip+"""/fs4/py/iframe_nw_nas_disk_list.py">"""+show_on+"""</a></span>

                </div>"""
	else:
		print"""</span></a>Volume Information</div>"""
	print"""
			<form name="volume_conf" action="iframe_nw_nas_disk_list#tabs-1" method="post">
		  <div class="infoheader">
		    <!--<div id="tabs">
		      <ul>
			<li><a href="#tabs-1">Volume Configuration</a></li>
		      </ul>-->
		      <div id="tabs-1">

			</form>
		<!--form container starts here-->
		<div class="form-container">
		  <div class="inputwrap">
		    <div class="formleftside-content"></div>
		    <div class="formrightside-content">
		<div style="float:right; margin-left:5%;">
		<!--<table style="margin-left: -39%;">-->

		 <!--<tr>

		<td style="font-family:icon;color:#EC1F27; border:#BDBDBD 1px solid;"><b>Volume</b></td>
		<td style="font-family:icon;color:#EC1F27;text-align:center; border:#BDBDBD 1px solid;"><b>Size</b></td>
		</tr>-->
	<form name = 'disk_form' method = 'POST' />"""


	if(vg_info["vgs"]!=[{}]):

                multi = 1;
		chart_var = 1

		vol_array_len = 2001
		j=2001
		k=2001

                for x in vg_info["vgs"]:
			volume_name= x["vg_name"];
			full_size= x['size']
			full_size = full_size.replace('g', '')
			full_size = float(full_size)
			free_get_size = new_free = x["free_size"]
			free_get_size = free_get_size.replace('g', '')
			free_get_size = float(free_get_size)
			
			get_used_size=full_size - free_get_size

                        new_free = x["free_size"]

                        if (new_free.find('g') > 0):
                                multi = 1;
                                new_free = new_free.replace('g', '');

                        if (new_free.find('t') > 0):
                                multi = 1024;
                                new_free = new_free.replace('t', '');

                        free_size = float(new_free) * multi;
			avail_free_size = free_size
                        free_size = str(free_size) + 'GB';

#--------------------------- Display Pie Chart for all volumes start------------------------------#

			print"""
			<!--<div class="topinputwrap-heading">Volume"""+str(chart_var)+"""</div>-->
			<div style ="text-align:left; padding:5px; color:#365371; width:190px;"><b>Volume"""+str(chart_var)+"""</b></div>

			<div id='chartdiv"""+str(chart_var)+"""' style="width: 100%; height: 200px;float:right;"></div>"""

			print """
			<nav id="menu_vol">

			<ul>"""


			print """<li onclick="return folder_click("""+str(j)+""", """+str(vol_array_len)+""", """+str(k)+""");"><a>"""+volume_name+"""</a>

			<div id='"""+str(j)+"""' style="display:none;">
			<ul>

			<li><a class="various" data-fancybox-type="iframe" href="nas_configuration.py?volume="""+x["vg_name"]+"""&free_size="""+free_size+"""">NAS Disk</a></li>
			<li><a class="various" data-fancybox-type="iframe" href="vtl_configuration.py?volume="""+x["vg_name"]+"""&free_size="""+free_size+"""">VTL Disk</a></li>
			<li><a class="various" data-fancybox-type="iframe" href="bio_configuration.py?volume="""+x["vg_name"]+"""&free_size="""+free_size+"""">BIO Disk</a></li>
			<li><a class="various" data-fancybox-type="iframe" href="create_container.py?volume="""+x["vg_name"]+"""&free_size="""+free_size+"""">FIO Disk</a></li>

			</ul>
			</div>

			</li>"""

			print """

			</ul>

			</nav>"""
			
			print """	
			<script type="text/javascript">

			var chart"""+str(chart_var)+""";

			var chartData"""+str(chart_var)+""" = [
			{
				"Volume": "Free (GB)",
				"value":"""+str(avail_free_size)+"""
			},

			{
			"Volume": "Used (GB)",
			"value":"""+str(get_used_size)+""" 
			},
			    ];

			AmCharts.ready(function () {
				// PIE CHART
				chart"""+str(chart_var)+""" = new AmCharts.AmPieChart();
				chart"""+str(chart_var)+""".dataProvider = chartData"""+str(chart_var)+""";
				chart"""+str(chart_var)+""".titleField = "Volume";
				chart"""+str(chart_var)+""".valueField = "value";
				chart"""+str(chart_var)+""".outlineColor = "#FFFFFF";
				chart"""+str(chart_var)+""".outlineAlpha = 0.8;
				chart"""+str(chart_var)+""".outlineThickness = 2;
				chart"""+str(chart_var)+""".balloonText = "[[title]]<br><span style='font-size:14px'><b>[[value]]</b> ([[percents]]%)</span>";
				// this makes the chart 3D
				chart"""+str(chart_var)+""".depth3D = 15;
				chart"""+str(chart_var)+""".angle = 30;

				// WRITE
				chart"""+str(chart_var)+""".write("chartdiv"""+str(chart_var)+"""");


				});
			</script>"""
			chart_var = chart_var+1
			j = j+1

#--------------------------- Display Pie Chart for all volumes end------------------------------#


		print """ <nav id="menu_vol">

                <ul>"""


		'''<div id='"""+str(j)+"""' style="display:none;">
		<ul>


		</ul>
		</div>

		</li>"""
		j=j+1'''
		
                print """

                </ul>

                </nav>

			<tr>
			
			<input id="disk_used_size_val" name="disk_used_size_val" type='hidden' value='"""+str(get_used_size)+"""' />
			<input id="free_vg_val1" name="free_vg_val1" type='hidden' value='"""+str(avail_free_size)+"""' />

			<input id="free_vg_nm" name="free_vg_nm" type='hidden' value='"""+x["vg_name"]+"""' />

                        <!--<td style="border:#BDBDBD 1px solid; text-align: center;">
<a class="various" data-fancybox-type="iframe" style="color:#666666;text-decoration:none;" href="nas_configuration.py?volume="""+x["vg_name"]+"""&free_size="""+free_size+"""">"""+x["vg_name"]+"""</a></td>
                        <td title=' Available volume size' style="border:#BDBDBD 1px solid;">"""+free_size+"""</td>-->
			<input id="free_vg_sz" name="free_vg_sz" type='hidden' value='"""+free_size+"""' />
                        </tr>"""

		print"""</form></table></div>

			 </div>
                  </div>
                <!--form container ends here-->
                <p>&nbsp;</p>
                      </div>"""

	else:
		print """<div style="margin:10px 250px 0 0;">No Volume Found! <a href="iframe_raid_settings_new.py" style="text-decoration:underline;">Create Volume</a></div>"""


	print """</div>
		  </div>
		</div>

		<!--form container ends here-->
		<p>&nbsp;</p>
		      </div>

	"""
except Exception as e:
        print e
