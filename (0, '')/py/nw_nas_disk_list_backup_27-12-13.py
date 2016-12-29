#!/usr/bin/python
#import cgitb, header
#cgitb.enable()

import traceback, sys, system_info
sys.path.append('../modules/')
import disp_except;
try:
        import cgitb, header, os, sys, commands, common_methods, traceback
        cgitb.enable()

        sys.path.append('/var/nasexe/storage/')
        import storage_op
        from lvm_infos import *
        from functions import *

        sys.path.append('/var/nasexe/')
        import storage

	if(header.form.getvalue("submit_update")):
                #update_volume = form.getvalue("update_volume")
                update_disk = header.form.getvalue("update_disk")
                update_size = header.form.getvalue("update_size")
                size_info = header.form.getvalue("size_info")
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




	vg_info = get_vgs()
	#print vg_info
	
	type_list=['NAS','BIO','FIO','VTL']
	st=storage_op.list_all_disks()
	#print st
	get_vol_name = "ALL"
	get_vol_type = "ALL"
	#dict_val = get_lvs()
	#condition = dict_val
	#condition_len = dict_val["lvs"]
	condition = st
	condition_len = st
	array_len = len(condition_len)
	if(header.form.getvalue("volume_sel")):
		get_vol_name = header.form.getvalue("volume_sel")
		get_vol_type = header.form.getvalue("disk_type")
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

	#print array_len

	#if(header.form.getvalue("disk_type")):
	#	get_vol_type = header.form.getvalue("disk_type")
	#	if(get_vol_type == "ALL"):
	#		condition = st
	#	else:
	#		subarray2 = []
	#		for u in condition:
	#			if (u['type'] == get_vol_type):
	#				subarray2.append(u)

	#		condition = subarray2

	#	array_len2 = len(condition)


        image_icon = common_methods.getimageicon();

        log_array = [];
        log_file = common_methods.log_file;
        logstring = '';
        #lv_name = '';
        vg = '';

        nas_info = get_lvs()
        #nas_infonas = get_lvs("nas")
	#print nas_info

        ss = nas_info
        logstring = str(common_methods.now) + '<<>>From: ' + common_methods.remote_ip + '<<>>' + str(ss) + str("Retrieve lv info");
        log_array.append(logstring);
        common_methods.append_file(log_file, log_array);
	
	if(header.form.getvalue("delete_but")):
                get_lv = header.form.getvalue("delete_option[]")
                #print get_lv
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
	
	vg_info = get_vgs()

        nas_info = get_lvs()
	#print 'Content-Type: text/html'
	for free_vg in vg_info["vgs"]:
		#print free_vg

		free_vg = free_vg["free_size"]
		#print free_vg

	import left_nav
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


		
	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer">
		<div class="insidepage-heading"> Volume Configuration >> <span class="content">Nas Disk Configuration</span></div>
		<!--tab srt-->
		<div class="searchresult-container">
			<form name="volume_conf" action="main.py?page=nd#tabs-1" method="post">
		  <div class="infoheader">
		    <div id="tabs">
		      <ul>
			<li><a href="#tabs-1" onclick="return select_submit('volume_config');">Volume Configuration</a></li>
			<li><a href="#tabs-2">Disks </a></li>
		      </ul>
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
			<div class="topinputwrap-heading">Volume"""+str(chart_var)+"""</div>

			<div id='chartdiv"""+str(chart_var)+"""' style="width: 100%; height: 200px;float:right;"></div>"""

			print """
			<nav id="menu_vol">

			<ul>"""


			print """<li onclick="return folder_click("""+str(j)+""", """+str(vol_array_len)+""", """+str(k)+""");"><a>"""+volume_name+"""</a>

			<div id='"""+str(j)+"""' style="display:none;">
			<ul>

			<li><a class="various" data-fancybox-type="iframe" href="nas_configuration.py?volume="""+x["vg_name"]+"""&free_size="""+free_size+"""">Nas Disk</a></li>
			<li><a href="#">VTL Disk</a></li>

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
				"Volume": "Free",
				"value":"""+str(avail_free_size)+"""
			},

			{
			"Volume": "Used",
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
                </div>
                <!--form container ends here-->
                <p>&nbsp;</p>
                      </div>


		<div id="tabs-2">
		<form name="disk_list_form" action="" method="post">
                <!--form container starts here-->
                <div class="form-container">
                  <div class="inputwrap">
                    <div class="formrightside-content">


	<div id="filter_option">
		<table>
		<tr>
		<td>Filter by volume : </td>
		<td>	
			<div class="styled-select2"> 
			<select name="volume_sel" onchange="select_submit('select_volume');">
			<option>ALL</option>"""
	for x in vg_info["vgs"]:
		print """<option"""
		if(x["vg_name"] == get_vol_name):
			print "selected"

		print """>"""+x["vg_name"]+"""</option>"""
	
	print """
			</select>
			</div>
		</td>

		<td>Filter by Disk Type : </td>
		<td>
			<div class="styled-select2" onchange="select_submit('select_volume');"> 
			<select name="disk_type">
			<option>ALL</option>"""
	for t in type_list:
		print """<option"""
		if(t == get_vol_type):
			print "selected"

		print """>"""+t+"""</option>"""

	print """</select>
			</div>
		</td>
		</tr>
		</table>
		</form>

	</div>

	<nav id="menu_disk">

	<ul>"""

	if(array_len != 0):

		#array_len = 5
		i=1
		s=1
		for y in condition:
			new = y["size"]

                        if (new.find('g') > 0):
                                size = new.replace("g", "");

                        if (new.find('t') > 0):
                                multi = 1024;
                                size = new.replace("t", "")

                        size = float(size) * multi;
                        size = str(size) + ' GB';

			checkforshares = commands.getoutput('sudo grep "/%s/" /var/www/global_files/shares_global_file' % y['lv_name']);

			disk_name = y["lv_name"]
                        get_protocols = system_info.check_protocols(disk_name)
                        print_protocols = ''
                        if(get_protocols == "No Protocols"):
                                print_protocols = "No-Protocols"
                        else:
                                proto = ''
                                for a in get_protocols:
                                        proto = proto+str(a)+'&nbsp;'

                                print_protocols = proto

			if((print_protocols != "No-Protocols") or (checkforshares != '')):
				border_bottom = 'style="border-bottom:#DF0101 1px solid;"'
			else:
				border_bottom = ''
			
			print """<li """+border_bottom+""" onclick="return folder_click("""+str(i)+""", """+str(array_len)+""", """+str(s)+""");"><a>"""+y["lv_name"]+"""</a>

			<style>
			#popUpDiv1"""+str(i)+""" {position: fixed; background-color: #fff; min-width: 400px; z-index: 9002; padding: 5px;}
			#popUpDiv1"""+str(i)+""" h5{width:100%; font-size:15px; color:#0070bd; text-align:center; font-weight:bold;}
			#popUpDiv1"""+str(i)+""" span{ color:#FFFFFF; background-color:#0070bd; padding:1px 3px 0 3px; float:right;}

			#popUpDiv2"""+str(i)+""" {position: fixed; background-color: #fff; min-width: 400px; z-index: 9002; padding: 5px;}
			#popUpDiv2"""+str(i)+""" h5{width:100%; font-size:15px; color:#0070bd; text-align:center; font-weight:bold;}
			#popUpDiv2"""+str(i)+""" span{ color:#FFFFFF; background-color:#0070bd; padding:1px 3px 0 3px; float:right;}

			#popUpDiv3"""+str(i)+""" {position: fixed; background-color: #fff; min-width: 400px; z-index: 9002; padding: 5px;}
			#popUpDiv3"""+str(i)+""" h5{width:100%; font-size:15px; color:#0070bd; text-align:center; font-weight:bold;}
			#popUpDiv3"""+str(i)+""" span{ color:#FFFFFF; background-color:#0070bd; padding:1px 3px 0 3px; float:right;}

			#popUpDiv4"""+str(i)+""" {position: fixed; background-color: #fff; min-width: 400px; z-index: 9002; padding: 5px;}
			#popUpDiv4"""+str(i)+""" h5{width:100%; font-size:15px; color:#0070bd; text-align:center; font-weight:bold;}
			#popUpDiv4"""+str(i)+""" span{ color:#FFFFFF; background-color:#0070bd; padding:1px 3px 0 3px; float:right;}

			#popUpDiv5"""+str(i)+""" {position: fixed; background-color: #fff; min-width: 400px; z-index: 9002; padding: 5px;}
			#popUpDiv5"""+str(i)+""" h5{width:100%; font-size:15px; color:#0070bd; text-align:center; font-weight:bold;}
			#popUpDiv5"""+str(i)+""" span{ color:#FFFFFF; background-color:#0070bd; padding:1px 3px 0 3px; float:right;}

			</style>"""

			for b in vg_info["vgs"]:
				if(b["vg_name"] == y["vg_name"]):
					new_free = b["free_size"]

                        if (new_free.find('g') > 0):
                                multi = 1;
                                new_free = new_free.replace('g', '');

                        if (new_free.find('t') > 0):
                                multi = 1024;
                                new_free = new_free.replace('t', '');

                        free_size = float(new_free) * multi;
                        free_size = str(free_size) + ' GB';


			print """<div style="display: none;" id="blanket"></div>
			<div style="display: none;" id='popUpDiv1"""+str(i)+"""'>
			<h5>Increase Size of '"""+y['lv_name']+"""' <span onclick="popup('popUpDiv1"""+str(i)+"""')">X</span></h5>
			<form name="update_disk_size" action="main.py?page=nd#tabs-2" method="post" >
			<p class="popup">
			<span style="color:#424242; padding:0 0 10px 5px; background-color:#FFFFFF; font-size:12px; float:left;">Available Size in Volume '"""+y['vg_name']+"""' : """+free_size+"""</span>
			<table width="100%" style="text-align:center; padding:20px; border:#D1D1D1 1px solid;">

			<tr>
			<td align="left" width="45%">Previous Size</td>
			<td align="left">"""+size+"""</td>
			</tr>

			<tr>
			<td align="left">Volume</td>
			<td align="left">"""+y['vg_name']+"""</td>
			</tr>

			<tr>
			<td align="left">Disk</td>
			<td align="left">"""+y['lv_name']+"""</td>
			</tr>

			<tr>
			<td align="left">Increase Size</td>
			<td align="left"><input type="text" style = "text-align:center;" name="update_size" onkeypress="return isNumberKey(event)" size="5" > GB

			<input type="hidden" name="size_info" value='"""+size+"""' />
			<input type="hidden" name="update_disk" value='"""+y['lv_name']+"""' />
			</td>
			</tr>

			</table>
			
			<button class="button_example" type="submit" name="submit_update" id="id_create_but" value = "Update" onclick ="return select_submit('update_disk');" style="float:right; margin:10px 20px 10px 10px;" >Update</button>
			</p>
			</form>
			</div>

			<div style="display: none;" id='popUpDiv2"""+str(i)+"""'>
			<h5>Information of """+y['lv_name']+"""<span onclick="popup('popUpDiv2"""+str(i)+"""')">X</span></h5>
			<p class="popup">
			<table width="100%" style="text-align:center; padding:20px 20px 20px 80px; margin:0 0 20px 0; border:#D1D1D1 1px solid;">"""

                        print """<tr>
                        <td align="left" width="45%">Disk Name</td>
                        <td align="left">"""+y['lv_name']+"""</td>
                        </tr>

                        <tr>
                        <td align="left" width="45%">Disk Type</td>
                        <td align="left">"""+y['type']+"""</td>
                        </tr>

                        <tr>
                        <td align="left" width="45%">Volume Name</td>
                        <td align="left">"""+y['vg_name']+"""</td>
                        </tr>

                        <tr>
                        <td align="left" width="45%">Disk Size</td>
                        <td align="left">"""+size+"""</td>
                        </tr>

                        <tr>
                        <td align="left" width="45%">Protocols</td>
                        <td align="left">"""+print_protocols+"""</td>
                        </tr>

			</table>

			</p>
			</div>

			<div style="display: none;" id='popUpDiv3"""+str(i)+"""'>
			<h5>Delete """+y['lv_name']+"""<span onclick="popup('popUpDiv3"""+str(i)+"""')">X</span></h5>
			<p class="popup">
			<div style="border:#D1D1D1 1px solid; text-align:center; height:70px; margin-bottom:20px;">"""
			if((print_protocols != "No-Protocols") or (checkforshares != '')):
				print """You cannot delete this disk because either the Protocols<br/> has been enabled or the the disk is busy.<br/>
				<button class="button_example" type="button" name = 'local_action_but'  id = 'local_action_but' value = 'Update' style="float:right; margin:0px 150px 0 0; " onclick="popup('popUpDiv3"""+str(i)+"""')" >Go Back</button>"""
			else:
				print """Are you sure you want to delete """+y['lv_name']+"""?<br/><br/>
			<button class="button_example" type="button" name = 'local_action_but'  id = 'local_action_but' value = 'Update' style="float:right; margin:0px 150px 0 0; " onclick="popup('popUpDiv3"""+str(i)+"""')" >No</button>
			<button class="button_example" type="submit" name = 'local_action_but'  id = 'local_action_but' value = 'Update' style="float:right; " >Yes</button>"""
			
			print """</div>
			</p>
			</div>

			<div id='"""+str(i)+"""' style="display:none;">
			<ul>

			<li><a href="#" onclick="popup('popUpDiv1"""+str(i)+"""')">Increase Size</a></li>
			<li><a href="#" onclick="popup('popUpDiv2"""+str(i)+"""')">Information</a></li>
			<li><a href="#" onclick="popup('popUpDiv3"""+str(i)+"""')">Delete</a></li>

			</ul>
			</div>

			</li>"""
			i=i+1

		print """


		</ul>

		</nav>"""

	else:
		print """<div style="text-align:center; color:#FE2E2E;">No Disk Found !</div>"""



				




		print """</div>
		  </div>
		</div>

		<!--form container ends here-->
		<p>&nbsp;</p>
		      </div>


		
		      </div>
		    </div>
		  </div>
		</div>
		<!--form container ends here-->
		<!--form container starts here-->
		<!--form container ends here-->
	      </div>
	      <!--Right side body content ends here-->
	    </div>
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
except Exception as e:
        print e
