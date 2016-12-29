#!/usr/bin/python
#import cgitb, header
#cgitb.enable()

import traceback, sys, system_info
sys.path.append('/var/www/fs4/modules')
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


	vtl_info = storage.get_lvs(type1='VTL')

        sys.path.append('/var/nasexe/python/')
        import mhvtl
        get_all_vtls = mhvtl.get_all_vtls()
#-------------------------------------VTL DISK DELETE------------------------------

        if(header.form.getvalue("delete_but")):
                get_lv = header.form.getvalue("delete_option[]")
                check_get_lv =isinstance(get_lv, str)

                if(check_get_lv ==True):
                        remove_lv = storage_op.lvremove(get_lv,type1='VTL')

                else:
                        get_lv = set(get_lv)
                        for value in get_lv:
                                remove_lv = storage_op.lvremove(value,type1='VTL')

		if(remove_lv == True):
                        print"""<div id = 'id_trace'>"""
                        print " Disk <font color='darkred'><b>"+str(get_lv)+"</b></font> Successfully Deleted!"
                        print "</div>"
			logstatus = common_methods.sendtologs('Success', 'Successfully deleted Vtl', 'vtl_disk_list.py', str(remove_lv));
                else:
                        print"""<div id = 'id_trace_err'>"""
                        print "Error occured while deleting Disk <font color = 'darkred'><b>"+str(get_lv)+"</b></font> !"	
			print "</div>"
			logstatus = common_methods.sendtologs('Error', 'Error Occurred while Deleting Disk', 'vtl_disk_list.py', str(remove_lv));
#---------------------------------------End-------------------------------------------------------
	vg_info = get_vgs()

        vtl_info = storage.get_lvs(type1='VTL')
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



		
		</head>


		
	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer">
		<div class="insidepage-heading">Volume Configuration >> <span class="content">VTl Disk Configuration</span></div>
		<!--tab srt-->
		<div class="searchresult-container">
		  <div class="infoheader">
		    <div id="tabs">
		      <ul>
			<li><a href="#tabs-1">VTL</a></li>
		      </ul>
		      <div id="tabs-1">

		<!--form container starts here-->
		<div class="form-container">
		  <div class="topinputwrap-heading">Nas Disk Configuration </div>
		  <div class="inputwrap">
		    <div class="formleftside-content"></div>
		    <div class="formrightside-content">
		<div style="float: none; margin-left: 5%;">
		<table style="margin-left: -39%; border:#BDBDBD 1px solid;"> 

		 <tr>

		<td style="font-family:icon;color:#EC1F27; border:#BDBDBD 1px solid;"><b>Volume</b></td>
		<td style="font-family:icon;color:#EC1F27;text-align:center; border:#BDBDBD 1px solid;"><b>Size</b></td>
		</tr>"""


	if(vg_info["vgs"]!=[{}]):

                multi = 1;

                for x in vg_info["vgs"]:
                        #print x
                        new_free = x["free_size"]
                        #print new_free

                        if (new_free.find('g') > 0):
                                multi = 1;
                                new_free = new_free.replace('g', '');

                        if (new_free.find('t') > 0):
                                multi = 1024;
                                new_free = new_free.replace('t', '');

                        free_size = float(new_free) * multi;
			avail_free_size = free_size
                        free_size = str(free_size) + 'GB';

                        #free_size = new_free.replace("g", "GB")
                        #free_size = new_free.replace("t", "TB")
			print"""

			<form name = 'disk_form' method = 'POST'>
			<tr>
			
                        <td style="border:#BDBDBD 1px solid; text-align: center;">
<a class="various" data-fancybox-type="iframe" style="color:#666666;text-decoration:none;" href="nas_configuration.py?volume="""+x["vg_name"]+"""&free_size="""+free_size+"""">"""+x["vg_name"]+"""</a></td>
                        <td title=' Available volume size' style="border:#BDBDBD 1px solid;">"""+free_size+"""</td>
                        </tr></form>"""

		print"""</table></div>
		<span style="margin-left: -32%;"><font color = '#EC1F27' size = '5'>*</font> - <I style="color:#666666;">Disk is shared</I></span>
				
                                <div id="chartContainer" style="width: 50%; height:200px;float: left; margin-left: -48%;"></div>

						<td width = '70%'>
						<div style="margin-left: -6.5%; margin-top: -10%;">
                                                <table border = "1" style =" border-style:ridge;" cellspacing ="1" align = 'center'>
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
						<form name = 'disk_to_delete' method = 'POST'>

"""
	if(vtl_info["lvs"]!=[{}]):

		i = 1
		multi = 1;

		for y in vtl_info["lvs"]:

			new = y["size"]

			#print 'NEw:'+str(new)
			if (new.find('g') > 0):
				size = new.replace("g", "");

			if (new.find('t') > 0):
				multi = 1024;
				size = new.replace("t", "")

			size = float(size) * multi;
			size = str(size) + 'GB';

			checkforshares = commands.getoutput('sudo grep "/%s/" /var/www/global_files/shares_global_file' % y['lv_name']);
		#       print checkforshares

			if (checkforshares != ''):
				disabled = 'disabled';
				star_icon = "<font color = 'darkred' size = '3' style='font-family: Georgia;'>*</font>"

			else:
				disabled = '';
				star_icon = ''


			
			lib_path = '/storage/VTL/'+y['lv_name']
                        disable_chk = ""
                        star_icon = ""
                        for k in get_all_vtls['vtl_libs']:
                                lib_home_dir = k['lib_home_dir'].strip()
                                lib_home_dir = lib_home_dir[:lib_home_dir.rfind('/')]
                                if(lib_home_dir == lib_path.strip()):
                                        disable_chk = "disabled"
                                        star_icon = "<font color = 'darkred' size = '3' style='font-family: Georgia;'>*</font>"

			print """


				 <tr>
                        <td height = '35px'>
                        <input id = 'id_disk_array' type = 'checkbox' """+disable_chk+""" name = 'delete_option[]' value = '"""+y["lv_name"]+"""'""" + disabled + """ >
                        </td>
                        <td title="VTL volume name" style = "text-align:center;"><b><i>""" +y["vg_name"] + """</i></b></td>
                        <td name" style = "text-align:center;"> 
                        <!--<a class = 'share_link1' href = '#' onclick = 'window.showModalDialog("setup_diskmgr_add_disk.py?volume="""+y['vg_name']+"""&disk_name="""+y['lv_name']+"""&size_name="""+size+"""&available_size="""+x["free_size"]+"""", "Expand Disk", "dialogWidth: 550px; dialogHeight: 350px;");' style="color: green;"> """ +y["lv_name"]+ """ </a>-->

                        <a class="various" data-fancybox-type="iframe" style="color:green; font-weight: bold; width:100%;float:right; text-decoration:none; "  href="vtl_increase.py?volume="""+y["vg_name"]+"""&disk_name="""+y['lv_name']+"""&size_name="""+size+"""&available_size="""+x["free_size"]+"""">"""


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

			
			print """<span style = "color:green; margin:0;" >"""+y["lv_name"]+star_icon+"""</span>"""			
			print"""</td>"""

                        print """<td align = 'right' title="VTL volume size" style = "text-align:center;" ><b><i>"""+size+"""</i></b></td>

	</tr>"""

	else:
		 print """
                <tr>
                <td colspan = '6' align = 'center' height="50px;">
                <marquee behavior="alternate" direction= "right"><b><font size="5">No disks is available</font></b></marquee>
                </td>
                </tr></table></div>"""
		

	print"""<table style="float: right;">
		<tr>
			<td>
		<button class="button_example" type="submit" name = 'delete_but' value = 'Delete selected' onclick = 'return nas_disk_delete();'>Delete</button>
		</td></tr>


		</table>

		<!--<div class="topinputwrap-heading" style="width:23%;margin-left:-40%;">Nas Disk Creation </div>-->



		  </div>
		  </div>
		</div>

		</form>
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
