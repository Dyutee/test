#!/usr/bin/python
#import cgitb, header
#cgitb.enable()

import traceback, sys, system_info
sys.path.append('../modules/')
import disp_except;
try:
        import cgitb, header, os, sys, commands, common_methods, traceback
        cgitb.enable()
        image_icon = common_methods.getimageicon();

        sys.path.append('/var/nasexe/storage/')
        import storage_op
        from lvm_infos import *
        from functions import *

        sys.path.append('/var/nasexe/')
        import storage
        log_array = [];
        log_file = common_methods.log_file;
        logstring = '';
        #lv_name = '';
        vg = '';

        nas_info = get_lvs()
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
		  <div class="infoheader">
		    <div id="tabs">
		      <ul>
			<li><a href="#tabs-1">Volume Configuration</a></li>
			<li><a href="#tabs-2">Nas Disk List </a></li>
			<li><a href="#tabs-3">Vtl Disk List </a></li>
		      </ul>
		      <div id="tabs-1">

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

                <!--form container starts here-->
                <div class="form-container">
                  <div class="inputwrap">
                    <div class="formleftside-content"></div>
                    <div class="formrightside-content">


				
				<form name = 'disk_to_delete' method = 'POST'>
				

                                                <table width ="600" align="center" style="float: right;"> 
                                                <tr style = 'font-weight: bold;'>
                                                        <td align = 'center' width = '1%' height = '35px' style="font-family:icon;color:#EC1F27; border:#BDBDBD 1px solid;">
                                                                <input type = 'checkbox' id = 'id_select_all' name = 'select_all' onclick = 'return select_nas_disks_all();'>
                                                        </td>
                                                    <td align = 'center' style="font-family:icon;color:#EC1F27; border:#BDBDBD 1px solid;">
                                                                Volume
                                                        </td>
                                                        <td align = 'center' style="font-family:icon;color:#EC1F27; border:#BDBDBD 1px solid;">
                                                                Disk
                                                        </td>
                                                        <td  align = 'center' style="font-family:icon;color:#EC1F27; border:#BDBDBD 1px solid;">
                                                                Size
                                                        </td>


                                                </tr>
						<!--</table>-->
						<!--<table style =" border:#BDBDBD 1px solid;" width = '100%' cellspacing ="1" align = 'center'>-->

<input id="free_vg_val" name="free_vg_val" type='hidden' value='"""+free_vg+"""' />
"""

	str_var = ''
	if(nas_info["lvs"]!=[{}]):

                i = 1
                multi = 1;

		f=1

                for y in nas_info["lvs"]:
                #       print y

                        new = y["size"]

                        #print 'NEw:'+str(new)
                        if (new.find('g') > 0):
                                size = new.replace("g", "");

                        if (new.find('t') > 0):
                                multi = 1024;
                                size = new.replace("t", "")

                        size = float(size) * multi;
                        size_for_graph = float(size) * multi;
                        size = str(size) + 'GB';

                        checkforshares = commands.getoutput('sudo grep "/%s/" /var/www/global_files/shares_global_file' % y['lv_name']);
                #       print checkforshares

                        if (checkforshares != ''):
                                disabled = 'disabled';
                                star_icon = "<font color = '#EC1F27' size = '3' style='font-family: Georgia;'>*</font>"

                        else:
                                disabled = '';
                                star_icon = ''
			
                        if (y['lv_name'] == 'rrd_data'):
                                disabled = 'disabled';

			print """
			
                        <tr>
			
			<input id="disk_size_val" name="disk_size_val" type='hidden' value='"""+str(size_for_graph)+"""' />


                        <td style="font-family:icon; border:#BDBDBD 1px solid;">
                        <input id = 'id_disk_array' type = 'checkbox' name = 'delete_option[]' value = '"""+y["lv_name"]+"""'""" + disabled + """ >
                        </td>
                        <td title="Nas volume name" style="font-family:icon;border:#BDBDBD 1px solid;text-align:center"><b><i>""" +y["vg_name"] + """</i></b></td>
			
<input name='free_disk_val"""+str(f)+"""' type='hidden' value='"""+str(size_for_graph)+"""' />

                        <td style="font-family:icon;border:#BDBDBD 1px solid;"> 

                        <a class="various" data-fancybox-type="iframe" style="color:SaddleBrown; font-weight: bold; width:100%;float:right;text-align:center; text-decoration:none; "  href="setup_diskmgr_add_disk.py?volume="""+y["vg_name"]+"""&disk_name="""+y['lv_name']+"""&size_name="""+size+"""&available_size="""+x["free_size"]+"""">"""

			
			str_var2 = "{volume:"+str(f)+", area:"+str(size_for_graph)+" }"
			str_var = str_var+str_var2+','
			f=f+1


			#if(y["vg_name"]==x["vg_name"]):
			disk_name = y["lv_name"];
			get_protocols = system_info.check_protocols(disk_name)
			print_protocols = ''
			if(get_protocols == "No Protocols"):
				print_protocols = "No-Protocols"
			else:
				proto = ''
				for a in get_protocols:
					proto = proto+str(a)+'&nbsp;'

				print_protocols = proto


			print """
				<img src="../images/lv_img.jpg"><br/>
				<span style ="text-align:center;color:seaGreen;" class="btn btnPluginDownload lpTooltip lpRight" data-tooltip-text="""+str(print_protocols)+""">"""+y["lv_name"]+star_icon+"""</span>
	<input id="free_lv_nm" name="free_lv_nm" type='hidden' value='"""+y["lv_name"]+"""' />"""

			print"""</td>"""
		

			print """<td align = 'right' title="Nas volume size" style="font-family:icon;text-align:center;border:#BDBDBD 1px solid;"><b><i>"""+size+"""</i></b></td>
			<input id="use_sz" name="use_sz" type='hidden' value='"""+size+"""' />

	</tr>"""

	else:
		 print """
                <tr>
                <td colspan = '6' align = 'center' height="50px;">
                <marquee behavior="alternate" direction= "right"><b><font size="5">No disks is available</font></b></marquee>
                </td>
                </tr></table>"""
		

	str_var = str_var[:str_var.rfind(',')]
	str_var = str_var.replace("'","\'")
	#print str_var
	print """<input type='hidden' name='str_var' value='"""+str_var+"""' />"""
	print"""<table style="float: right;">
		<tr>
			<td>
		<button class="button_example" type="submit" name = 'delete_but' value = 'Delete' onclick = 'return nas_disk_delete();'>Delete</button>
		</td></tr>


		</table></form>

		<!--<div class="topinputwrap-heading" style="width:23%;margin-left:-40%;">Nas Disk Creation </div>-->



		  </div>
		  </div>
		</div>

		<input type='hidden' name='value_of_f' value='"""+str(f)+"""' />
		</form>
		<!--form container ends here-->
		<p>&nbsp;</p>
		      </div>

			 <div id="tabs-3">

                <!--form container starts here-->
                <div class="form-container">
                  <div class="inputwrap">
                    <div class="formleftside-content">Vtl Disk List</div>
                    <div class="formrightside-content">


		</div>
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
        disp_except.display_exception(e);
