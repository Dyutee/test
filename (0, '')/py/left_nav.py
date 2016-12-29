#!/usr/bin/python
import cgitb, sys, traceback
cgitb.enable()

sys.path.append('../modules/')
import disp_except;

try:

	sys.path.append('/var/nasexe/')
	import net_manage_newkernel as net_manage_bond

	getall_ifaces=net_manage_bond.get_all_ifaces_config()
	get_all_ip = getall_ifaces["all_conf"]

	sys.path.append('/var/nasexe/storage/')
	import storage_op
	from lvm_infos import *
	from functions import *
	import storage
	#-----Nas Disk only
	nas_info = get_lvs()
	# -----End-----	
	alldisk = storage_op.list_all_disks()
	querystring = os.environ['QUERY_STRING'];
	#print querystring
	#for z in alldisk:
	#	print z['lv_name']

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
			width           : '100%',
			height          : '58%',
			autoSize        : false,
			closeClick      : false,
			openEffect      : 'none',
			closeEffect     : 'none',
			/*'afterClose':function () {
			  window.location.reload();
			 },*/
			helpers   : { 
			overlay  :       {closeClick: false} // prevents closing when clicking OUTSIDE fancybox 
				     }
			
	       });

		});
		</script>



			
			</head>
	<!-- Left Nav Start -->
<div class="menuNavWrap" style="margin-top: 40px;"> 

  <!--Level 1 Menu starts from here-->

  <div class="firstLevelItemWrap">

    <div class="firstLevelItemImageWrap"><img src="../images/resources_icon.png" width="24" height="23" /></div>

    <!--<h3>RESOURCES</h3>-->"""
	if("page=sys" in querystring):
        	print"""
                <a href="main.py?page=sys">
                <h3 class="MenuActiveClass">DASHBOARD</h3>
                </a>"""
        else:
                print"""<a href="main.py?page=sys">

                        <h3>DASHBOARD</h3>
                        </a>"""


        print"""</div>  

  <div class="2ndLevel" style="display:none; width:200px; float:left;">

  <!--Level 2.1 Menu starts from here-->"""
	#if("page=sys" in querystring):
		
		
  	#	print"""<a href="main.py?page=sys"><div class="ThirdLevelItemWrap ">

    	#		<h2 class="MenuActiveClass">OS Information</h2>
  	#		</div></a>"""
	#else:
		
  	#	print"""<a href="main.py?page=sys"><div class="ThirdLevelItemWrap ">

    	#		<h2 >OS Information</h2>
  	#		</div></a>"""
	
	#if("page=sensor" in querystring):
   	#	print"""<a href="main.py?page=sensor"><div class="ThirdLevelItemWrap">
   	#	 <h2 class="MenuActiveClass">Sensor Information</h2>
  	#	</div></a>"""
	#else:
	#	print"""<a href="main.py?page=sensor"><div class="ThirdLevelItemWrap">
        #         <h2>Sensor Information</h2>
        #        </div></a>"""
	#if("page=volume" in querystring):
	#	print"""<a href="main.py?page=volume"><div class="ThirdLevelItemWrap">
	#		<h2 class="MenuActiveClass">Volume Information</h2>
  	#		</div></a>"""
	#else: 
		
	#	print"""<a href="main.py?page=volume"><div class="ThirdLevelItemWrap">
	#		<h2>Volume Information</h2>
  	#		</div></a>"""
	#if("page=info_disk" in querystring):
	#	print"""<a href="main.py?page=info_disk"><div class="ThirdLevelItemWrap">
        #                <h2 class="MenuActiveClass">Disk Information</h2>
        #                </div></a>"""
        #else: 
	
	#	print"""
  	#		<a href="main.py?page=info_disk"><div class="ThirdLevelItemWrap">

    	#		<h2>Disk Information</h2>

  	#		</div></a>"""
	print"""
  <!--Level 2.1 Menu ends here --> 

	</div>
	<div class="firstLevelItemWrap">

            <div class="firstLevelItemImageWrap"><img src="../images/resources_icon.png" width="24" height="23" /></div>

            <!--<h3>RESOURCES</h3>-->
            <h3>SYSTEM</h3>

            <div class="firstLevelRightarrow"> <img src="../images/firstrightArrow.png"/></div>

          </div>

          <!--Level 2 Menu starts from here-->

          <div class="2ndLevel" style="display:none;width:200px; float:left;">"""
	if("page=date" in querystring):
  		print"""<a href="main.py?page=date"><div class="SecondLevelItemWrap">
    		<h2 class="MenuActiveClass">Date/Time</h2>
  		</div></a>"""
	else:
		 print"""<a href="main.py?page=date"><div class="SecondLevelItemWrap">
    		<h2>Date/Time</h2>
  		</div></a>"""
	if("page=network"in querystring):
	
		print"""
   			<a href="main.py?page=network"><div class="SecondLevelItemWrap">
    			<h2 class="MenuActiveClass">Network Settings</h2>
  			</div></a>"""
	else:
		print"""
                        <a href="main.py?page=network"><div class="SecondLevelItemWrap">
                        <h2>Network Settings</h2>
                        </div></a>"""
	if("page=auth" in querystring):
	
		print"""
  		<a href="main.py?page=auth"> <div class="SecondLevelItemWrap">
   		 <h2 class="MenuActiveClass">Authentication</h2>
		</div></a>"""
	else:
		print"""<a href="main.py?page=auth"> <div class="SecondLevelItemWrap">
                 <h2>Authentication</h2>
                </div></a>"""
	if("page=mu" in querystring):

                print"""
                <a href="main.py?page=mu"> <div class="SecondLevelItemWrap">
                 <h2 class="MenuActiveClass">Users/Groups</h2>
                </div></a>"""
        else:
                print"""<a href="main.py?page=mu"> <div class="SecondLevelItemWrap">
                 <h2>Users/Groups</h2>
                </div></a>"""

	if("page=fs2" in querystring):

                print"""
                        <a href="main.py?page=fs2"><div class="SecondLevelItemWrap">
                        <h2 class="MenuActiveClass">Save/Restore Config</h2>
                        </div></a>"""
        else:
                print"""
                        <a href="main.py?page=fs2"><div class="SecondLevelItemWrap">
                        <h2>Save/Restore Config</h2>
                        </div></a>"""
	
	if("page=sd" in querystring):
                print"""
                        <a href="main.py?page=sd"><div class="SecondLevelItemWrap">
                        <h2 class="MenuActiveClass">Shutdown</h2>
                        </div> </a>"""
        else:
                print"""<a href="main.py?page=sd"><div class="SecondLevelItemWrap">
                        <h2>Shutdown</h2>
                        </div> </a>"""
	print"""
</div>
  <!--Level 2 Menu ends here --> 
  <!--Level 1 Menu ends here--> 
  <!--Level 1 Menu starts from here-->

  <div class="firstLevelItemWrap">

    <div class="firstLevelItemImageWrap"><img src="../images/NAS_icon.png" width="24" height="23" /></div>

    <h3>NAS</h3>

    <div class="firstLevelRightarrow"> <img src="../images/firstrightArrow.png"/></div>

  </div>

  <div class="2ndLevel" style="display:none;width:200px; float:left;">"""
        if("page=nas" in querystring):
                print"""<a href="main.py?page=nas"><div class="SecondLevelItemWrap">
                        <h2 class="MenuActiveClass">Create</h2>
                        </div></a>"""
        else:
                print"""<a href="main.py?page=nas"><div class="SecondLevelItemWrap">
                        <h2>Create</h2>
                        </div></a>"""
	if("page=cs" in querystring or "page=smb_set" in querystring or "page=afp" in querystring or "page=nfs" in querystring or "page=ftp" in querystring or "page=acl" in querystring or "page=fq" in querystring or "page=es" in querystring or "page=append" in querystring):
	
  		print"""<a href="main.py?page=cs"><div class="SecondLevelItemWrap">
    			<h2 class="MenuActiveClass">Manage Shares</h2>
  			</div></a>"""
	else:
  		print"""<a href="main.py?page=cs"><div class="SecondLevelItemWrap">
    			<h2>Manage Shares</h2>
  			</div></a>"""
	if("page=qo" in querystring):
		
		print"""		
   			<a href="main.py?page=qo"><div class="SecondLevelItemWrap">
    			<h2 class="MenuActiveClass">User/Group Quotas</h2></div></a>"""
	else:
		print"""<a href="main.py?page=qo"><div class="SecondLevelItemWrap">
                        <h2>User/Group Quotas</h2>
  			</div></a> """
	print"""
  <!--Level 2 Menu ends here --> 
  </div>
  <!--Level 1 Menu ends here--> 

  <!--Level 1 Menu starts from here-->

 <div class="firstLevelItemWrap">

    <div class="firstLevelItemImageWrap"><img src="../images/san.png" width="24" height="23" /></div>

    <h3>iSCSI/SRP/FC</h3>

    <div class="firstLevelRightarrow"> <img src="../images/firstrightArrow.png"/></div>

  </div>

  <div class="2ndLevel" style="display:none;width:200px; float:left;">"""
	if("page=san_list" in querystring):
		print"""
			<a href="main.py?page=san_list"><div class="SecondLevelItemWrap">
			<h2 class="MenuActiveClass">Volumes</h2>
			</div></a>"""
	else:
		print"""
                        <a href="main.py?page=san_list"><div class="SecondLevelItemWrap">
                        <h2>Volumes</h2>
                        </div></a>"""
	if("page=target_iscsi" in querystring or "page=iscsi" in querystring or "page=disk_iscsi" in querystring or "page=prop_iscsi" in querystring or "page=det_iscsi" in querystring or "page=ses_iscsi" in querystring or "page=ses_iscsi" in querystring or "page=lst_iscsi" in querystring):
		print"""
			<a href="main.py?page=iscsi"><div class="SecondLevelItemWrap">
			<!--<a href="#"><div class="SecondLevelItemWrap">-->
			<h2 class="MenuActiveClass">iSCSI</h2>
			</div></a>"""
	else:
		print"""
                        <a href="main.py?page=iscsi"><div class="SecondLevelItemWrap">
			<!--<a href="#"><div class="SecondLevelItemWrap">-->
                        <h2>iSCSI</h2>
                        </div></a>"""
	if("page=stat_srp" in querystring or "page=tar_srp" in querystring or "page=disk_srp" in querystring or "page=ini_srp" in querystring or "page=inf_srp" in querystring or "page=sess_srp" in querystring or "page=l_srp"in querystring):
		print"""
			<a href="main.py?page=stat_srp"><div class="SecondLevelItemWrap">
			<!--<a href="#"><div class="SecondLevelItemWrap">-->
			<h2 class="MenuActiveClass">SRP </h2>
			</div></a>"""
	else:
		print"""
                        <a href="main.py?page=stat_srp"><div class="SecondLevelItemWrap">
			<!--<a href="#"><div class="SecondLevelItemWrap">-->
                        <h2>SRP</h2>
                        </div></a>"""
	if("page=status_fc" in querystring or "page=tar_fc" in querystring or "page=disk_fc" in querystring or "page=fc_ini" in querystring or "page=inf_fc" in querystring or "page=sess_fc" in querystring or "page=list_fc" in querystring):
		print"""
			<a href="main.py?page=status_fc"><div class="SecondLevelItemWrap">
			<!--<a href="#"><div class="SecondLevelItemWrap">-->
			<h2 class="MenuActiveClass">FC</h2>
			</div></a>"""
	else:
		print"""
                        <a href="main.py?page=status_fc"><div class="SecondLevelItemWrap">
			<!--<a href="#"><div class="SecondLevelItemWrap">-->
                        <h2>FC</h2>
                        </div></a>"""
	print"""

  </div>

  <!--Level 1 Menu ends here--> 

  <!--Level 1 Menu starts from here-->

  <div class="firstLevelItemWrap">

    <div class="firstLevelItemImageWrap"><img src="../images/vtl_tape.png" width="24" height="23" /></div>

    <h3>VTL</h3>

    <div class="firstLevelRightarrow"> <img src="../images/firstrightArrow.png"/></div>

  </div>

  <div class="2ndLevel" style="display:none;width:200px; float:left;">

  <!--Level 2 Menu starts from here-->"""
	if("page=vtls" in querystring):
	
  		print"""<a href="main.py?page=vtls"><div class="SecondLevelItemWrap">
    			<h2 class="MenuActiveClass">VTL Settings</h2>
  			</div></a>"""
	else:
		print"""<a href="main.py?page=vtls"><div class="SecondLevelItemWrap">
                        <h2>VTL Settings</h2>
                        </div></a>"""
	print"""

  <!--Level 2 Menu ends here --> 

  </div>

  <!--Level 1 Menu ends here--> 

  <!--Level 1 Menu starts from here-->
 <div class="firstLevelItemWrap">

    <div class="firstLevelItemImageWrap"><img src="../images/raid.png" width="24" height="23" /></div>

    <h3>DISK/RAID</h3>

    <div class="firstLevelRightarrow"> <img src="../images/firstrightArrow.png"/></div>

  </div>

  <div class="2ndLevel" style="display:none;width:200px; float:left;">

  <!--Level 2.1 Menu starts from here-->"""
	if("page=crs" in querystring):
                print"""
                        <a href="main.py?page=crs"><div class="SecondLevelItemWrap">
                        <h2 class="MenuActiveClass">RAID Set Functions</h2>
                        </div> </a>"""
        else:
                print"""
                        <a href="main.py?page=crs"><div class="SecondLevelItemWrap">
                        <h2>RAID Set Functions</h2>
                        </div> </a>"""
        if("page=cvs" in querystring):
                print"""
                        <a href="main.py?page=cvs"><div class="SecondLevelItemWrap">
                        <h2 class="MenuActiveClass">Volume Set Functions</h2>
                        </div> </a>"""
        else:
                print"""
                        <a href="main.py?page=cvs"><div class="SecondLevelItemWrap">
                        <h2>Volume Set Functions</h2>
                        </div> </a>"""
        if("page=rs" in querystring):
                print """
                <a href="main.py?page=rs"><div class="SecondLevelItemWrap">
                <h2 class="MenuActiveClass">RAID Setup</h2>
                </div></a>"""
        else:
                print """
                <a href="main.py?page=rs"><div class="SecondLevelItemWrap">
                <h2>RAID Setup</h2>
                </div></a>"""
        print """
	<!--Level 2 Menu starts from here-->

  <div class="SecondLevelItemWrap">

    <div class="secondLevelRightarrow"> <img src="../images/secondrightArrow.png"/></div>

    <h3>Volume Configuration</h3>

  </div>
<div class="3rdLevel" style="display:none;width:200px; float:left;">
  <!--Level 2.1 Menu starts from here-->"""
        if("page=nd" in querystring):

                print"""<a href="main.py?page=nd"><div class="ThirdLevelItemWrap ">
                <h2 class="MenuActiveClass">Disk Configuration</h2>
                </div></a>"""
        else:

                print"""<a href="main.py?page=nd"><div class="ThirdLevelItemWrap ">
                <h2>Disk Configuration</h2>
                </div></a>"""
        if("page=all_disk_list" in querystring):
                print"""
                        <a href="main.py?page=all_disk_list"><div class="ThirdLevelItemWrap">
                        <h2 class="MenuActiveClass">Disk List</h2>
                        </div></a>"""
        else:

                print"""
                        <a href="main.py?page=all_disk_list"><div class="ThirdLevelItemWrap">
                        <h2>Disk List</h2>
                        </div></a>"""
        print"""
</div>"""

        if("page=volume_disk" in querystring):
                print"""
                        <a href="main.py?page=volume_disk"><div class="SecondLevelItemWrap">
                        <h2 class="MenuActiveClass">Volume/Disk Information</h2>
                        </div> </a>"""
        else:
                print"""
                        <a href="main.py?page=volume_disk"><div class="SecondLevelItemWrap">
                        <h2>Volume/Disk Information </h2>
                        </div> </a>"""
	print"""

  </div>

  <!--Level 1 Menu ends here--> 

  <!--Level 1 Menu starts from here-->

 <div class="firstLevelItemWrap">

    <div class="firstLevelItemImageWrap"><img src="../images/maintenance.png" width="24" height="23" /></div>

    <h3>TOOLS</h3>

    <div class="firstLevelRightarrow"> <img src="../images/firstrightArrow.png"/></div>

  </div>

  <div class="2ndLevel" style="display:none;width:200px; float:left;">

  <!--Level 2 Menu starts from here-->"""
	if("page=infini" in querystring):
	
  		print"""<a href="main.py?page=infini"><div class="SecondLevelItemWrap">
    			<h2 class="MenuActiveClass">Infiniband</h2>
  			</div></a>"""
	else:
		print"""<a href="main.py?page=infini"><div class="SecondLevelItemWrap">
                        <h2>Infiniband</h2>
                        </div></a>"""
	if("page=sr" in querystring):
		print"""<a href="main.py?page=sr"><div class="SecondLevelItemWrap">
                        <h2 class="MenuActiveClass">Services</h2>
                        </div></a>"""
	else:
		print"""<a href="main.py?page=sr"><div class="SecondLevelItemWrap">
                        <h2>Services</h2>
                        </div></a>"""
	if("page=logs" in querystring):
	
		print"""
  			<a href="main.py?page=logs"><div class="SecondLevelItemWrap">
			<h2 class="MenuActiveClass">Logs</h2>
  			</div> </a>"""
	else:
		print""" <a href="main.py?page=logs"><div class="SecondLevelItemWrap">
                        <h2>Logs</h2>
                        </div> </a>"""
	if("page=scan" in querystring):
	
		print"""
  			<a href="main.py?page=scan"><div class="SecondLevelItemWrap">
    			<h2 class="MenuActiveClass">Scan Volume</h2>
  			</div> </a>"""
	else:
		print"""
                        <a href="main.py?page=scan"><div class="SecondLevelItemWrap">
                        <h2>Scan Volume</h2>
                        </div> </a>"""
	if("page=re_mount" in querystring):
	
		print"""
  			<a href="main.py?page=re_mount"><div class="SecondLevelItemWrap">
    			<h2 class="MenuActiveClass">Remount</h2>
  			</div></a>"""
	else:
		print"""
                        <a href="main.py?page=re_mount"><div class="SecondLevelItemWrap">
                        <h2>Remount</h2>
                        </div></a>"""
	if("page=ss" in querystring):
		print"""
  		<a href="main.py?page=ss"><div class="SecondLevelItemWrap">
    		<h2 class="MenuActiveClass">Snapshot</h2>
  		</div> </a>"""
	else:
		print"""
                <a href="main.py?page=ss"><div class="SecondLevelItemWrap">
                <h2 >Snapshot</h2>
                </div> </a>"""
	if("page=updts" in querystring):

		print"""
  			<a href="main.py?page=updts"><div class="SecondLevelItemWrap">
    			<h2 class="MenuActiveClass">Updates</h2>
  			</div></a>"""
	else:
		print"""
                        <a href="main.py?page=updts"><div class="SecondLevelItemWrap">
                        <h2>Updates</h2>
                        </div></a>"""

	if("page=log_info" in querystring):
                print"""
                <a href="main.py?page=log_info"><div class="SecondLevelItemWrap">
                <h2 class="MenuActiveClass">Tasks</h2>
                </div> </a>"""
        else:
                print"""
                <a href="main.py?page=log_info"><div class="SecondLevelItemWrap">
                <h2 >Tasks</h2>
                </div> </a>"""
	if("page=mail" in querystring):
		print"""
  			<a href="main.py?page=mail"><div class="SecondLevelItemWrap">
    			<h2 class="MenuActiveClass">Mail Configuration</h2>
  			</div> </a>"""
	else:
		print"""
                        <a href="main.py?page=mail"><div class="SecondLevelItemWrap">
                        <h2>Mail Configuration</h2>
                        </div> </a>"""
	print"""
	<div class="SecondLevelItemWrap">

    <div class="secondLevelRightarrow"> <img src="../images/secondrightArrow.png"/></div>

    <h3>SAN Advanced Settings</h3>
  </div>
<div class="3rdLevel" style="display:none;width:200px; float:left;">
"""
	
	if("san_map" in querystring):
			print"""
			<a href="main.py?page=san_map"><div class="ThirdLevelItemWrap ">
                        <h2 class="MenuActiveClass">SRP Map Settings</h2>
                        </div> </a>"""
	else:
		print"""
			 <a href="main.py?page=san_map"><div class="ThirdLevelItemWrap ">
                        <h2>SRP Map Settings</h2>
                        </div> </a>"""

	if("fc_map" in querystring):
			print"""
			<a href="main.py?page=fc_map"><div class="ThirdLevelItemWrap ">
                        <h2 class="MenuActiveClass">FC Map Settings</h2>
                        </div> </a>"""
	else:
		print"""
			 <a href="main.py?page=fc_map"><div class="ThirdLevelItemWrap ">
                        <h2>FC Map Settings</h2>
                        </div> </a>"""

	print"""

  <!--Level 2 Menu ends here -->

  </div>
</div>
  <!--Level 1 Menu ends here--> 

  <!--Level 1 Menu starts from here-->

  <div class="firstLevelItemWrap">

    <div class="firstLevelItemImageWrap"><img src="../images/graph3 .png" width="24" height="23" /></div>

    <h3>MONITORING</h3>

    <div class="firstLevelRightarrow"> <img src="../images/firstrightArrow.png"/></div>

  </div>
 <div class="2ndLevel" style="display:none;width:200px; float:left;">
  <!--Level 2 Menu starts from here-->
<a href="#"><div class="SecondLevelItemWrap ">
    <h2><a class='various' data-fancybox-type='iframe' style='color:#666666;text-decoration:none;' href='canvas_cpu.py'>CPU Temperature</a></h2>
  </div></a>

<a href="#"><div class="SecondLevelItemWrap ">
    <h2><a class='various' data-fancybox-type='iframe' style='color:#666666;text-decoration:none;' href='canvas_mem_graph.py'>Memory Usage</a></h2>
  </div></a>

  <!--<div class="SecondLevelItemWrap">
    <div class="secondLevelRightarrow"> <img src="../images/secondrightArrow.png"/></div>
    <h3>System Temperature</h3>
  </div>
<div class="3rdLevel" style="display:none;width:200px; float:left;">
  <a href="#"><div class="ThirdLevelItemWrap ">
    <h2><a class='various' data-fancybox-type='iframe' style='color:#666666;text-decoration:none;' href='canvas_temperature_graph.py'>CPU Temperature</a></h2>
  </div></a>
</div>-->

 <!--Level 2 Menu starts from here-->
  <div class="SecondLevelItemWrap">
    <div class="secondLevelRightarrow"> <img src="../images/secondrightArrow.png"/></div>
    <h3>Disk I/O</h3>
  </div>
<div class="3rdLevel" style="display:none;width:200px; float:left;">
  <!--Level 2.1 Menu starts from here-->"""
	if(nas_info["lvs"]!=[{}]):
                for disk_detail in nas_info["lvs"]:
                        disk_info = disk_detail['lv_name']
                        print"""
                                <a href="#"><div class="ThirdLevelItemWrap ">
                                <h2><a class='various' data-fancybox-type='iframe' style='color:#666666;text-decoration:none;' href='canvas_disk_usage.py?disk_name="""+disk_info+"""'>"""+disk_info+"""</a></h2>
                                </div></a>"""

	print"""
</div>
<!--Level 2 Menu starts from here-->
  <div class="SecondLevelItemWrap">
    <div class="secondLevelRightarrow"> <img src="../images/secondrightArrow.png"/></div>
    <h3>Network I/O</h3>
  </div>
<div class="3rdLevel" style="display:none;width:200px; float:left;">
  <!--Level 2.1 Menu starts from here-->"""
	for iface in get_all_ip:
                iface_info =  iface['iface']

                print"""<a href="#"><div class="ThirdLevelItemWrap ">
                        <h2><a class='various' data-fancybox-type='iframe' style='color:#666666;text-decoration:none;' href='canvas_traffic.py?ethernet="""+iface_info+"""'>"""+iface_info+"""</a></h2>
                        </div></a>"""
        print"""
</div>
"""
        if("report" in querystring):
                print """<a href="main.py?page=report"><div class="SecondLevelItemWrap ">
                <h2 class="MenuActiveClass">Reports</h2>
                </div></a>"""
        else:
                print """<a href="main.py?page=report"><div class="SecondLevelItemWrap ">
                <h2>Reports</h2>
                </div></a>"""

        if("cleardata" in querystring):
                print """<a href="main.py?page=cleardata"><div class="SecondLevelItemWrap ">
                <h2 class="MenuActiveClass">Clear Data</h2>
                </div></a>"""
        else:
                print """<a href="main.py?page=cleardata"><div class="SecondLevelItemWrap ">
                <h2>Clear Data</h2>
                </div></a>"""
	print"""
</div>



  <!--Level 1 Menu ends here--> 

  <!--Level 1 Menu starts from here-->

  <div class="firstLevelItemWrap">

    <div class="firstLevelItemImageWrap"><img src="../images/help.png" width="24" height="23" /></div>

    <h3>HELP</h3>

    <div class="firstLevelRightarrow"> <img src="../images/firstrightArrow.png"/></div>

  </div>
<div class="2ndLevel" style="display:none; width:200px; float:left;">

  <!--Level 2 Menu starts from here-->

    """
	if("support" in querystring):
                        print"""
                        <a href="main.py?page=support"><div class="SecondLevelItemWrap">
                        <h2 class="MenuActiveClass">Support</h2>
                        </div> </a>"""
        else:
                print"""
                         <a href="main.py?page=support"><div class="SecondLevelItemWrap">
                        <h2>Support</h2>
                        </div> </a>"""

	if("first" in querystring):
                        print"""
                        <a href="main.py?page=first"><div class="SecondLevelItemWrap">
                        <h2 class="MenuActiveClass">Welcome</h2>
                        </div> </a>"""
        else:
                print"""
                         <a href="main.py?page=first"><div class="SecondLevelItemWrap">
                        <h2>Welcome</h2>
                        </div> </a>"""

  	print"""</div>
  </div>


  <!--Level 1 Menu ends here--> 

</div>
	      <!--Left side navigation ends here-->
	"""

except Exception as e:
        disp_except.display_exception(e);
