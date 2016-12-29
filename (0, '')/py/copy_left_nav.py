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

	    <div class="insidepagebodycontainer">
	      <!--left side navigation starts from here-->
	      <div class="leftsidenav" style="position:relative;">
		<div id="hmn0">
		  <nav>
		    <div id="acdnmenu" style="width:200px;">
		      <ul>"""
	if(querystring =="page=sys" or "page=sensor" in querystring or "page=volume" in querystring or"page=disk" in querystring or "page=date" in querystring or querystring =="page=network" or "page=auth" in querystring ):
	
		print"""
			<li><a href="#" style ="color:#333333;">RESOURCES</a>"""
	else:
		print"""<li>RESOURCES"""
	print"""
			  <ul>"""
	if("page=sys" in querystring or "page=sensor" in querystring or "page=volume" in querystring or "page=disk" in querystring):
	#if("page=sys" in querystring):
		print"""
			    <li><a href="#">Resources Information</a>"""
	else:
		print"""
			    <li>Resources Information"""
	print"""<ul>"""
	if("page=sys" in querystring):
		print"""<li><a href="main.py?page=sys" style ="color:#EC1F27;font-weight:bold;">OS Information</a></li>"""
	else:
		
		print"""<li><a href="main.py?page=sys">OS Information</a></li>"""
	if("page=sensor" in querystring):
		
		print"""<li><a href="main.py?page=sensor" style ="color:#EC1F27;font-weight:bold;">Sensor Information</a></li>"""
	else:
		
		print"""<li><a href="main.py?page=sensor">Sensor Information</a></li>"""
	if("page=volume" in querystring):
		
		print"""<li><a href="main.py?page=volume" style ="color:#EC1F27;font-weight:bold;">Volume Information</a></li>"""
	else:
		
		print"""<li><a href="main.py?page=volume">volume Information</a></li>"""
	if("page=disk" in querystring):
		
		print"""<li><a href="main.py?page=disk" style ="color:#EC1F27;font-weight:bold;">Disk Information</a></li>"""
	else:
		
		print"""<li><a href="main.py?page=disk">Disk Information</a></li>"""
	print"""</ul>"""
	print"""</li>"""
	if("page=date" in querystring):
		
		print"""
			    <li><a href="main.py?page=date" style ="color:#EC1F27;font-weight:bold;">Date/Time Settings</a> </li>"""
	else:
		print""" <li><a href="main.py?page=date">Date/Time Settings</a> </li>"""
	
	if(querystring =="page=network"):
		
		print"""<li><a href="main.py?page=network" style ="color:#EC1F27;font-weight:bold;">Network Settings</a> </li>"""
	else:
		print"""<li><a href="main.py?page=network">Network Settings</a> </li>"""

	if("page=auth" in querystring):
	
		print"""
			    <li><a href="main.py?page=auth" style ="color:#EC1F27;font-weight:bold;">Authentication</a></li>"""
	else:
		print"""<li><a href="main.py?page=auth">Authentication</a></li>"""

	print"""
			  </ul>

			</li>"""
	if(querystring =="page=cs" or querystring =="page=nas" or querystring =="page=csl" or "page=qo" in querystring or "page=es" in querystring or "page=smb_set" in querystring or "page=append" in querystring or "page=afp" in querystring or "page=nfs" in querystring or "page=ftp" in querystring or "page=acl" in querystring or "page=fq" in querystring):

		print"""
			<li><a href="main.py?page=cs" style ="color:#333333;">NAS</a>"""
	else:
		print"""<li>NAS"""
	print"""
			  <ul>"""

	if(querystring =="page=cs" or querystring =="page=nas" or querystring =="page=csl" or "page=es" in querystring or "page=smb_set" in querystring or "page=append" in querystring or "page=afp" in querystring or "page=nfs" in querystring or "page=ftp" in querystring or "page=acl" in querystring or "page=fq" in querystring):
		print"""
			    <li><a href="main.py?page=cs" style ="color:#EC1F27;font-weight:bold;">Shares</a></li>"""
	else:
		print"""<li><a href="main.py?page=cs">Shares</a></li>"""

	if("page=qo" in querystring):
		
		print"""
			    <li><a href="main.py?page=qo" style ="color:#EC1F27;font-weight:bold;">Quota</a></li>"""
	else:

		print"""<li><a href="main.py?page=qo">Quota</a></li>"""

	print"""
			    <!--<li><a href="main.py?page=sinfo">Share Info</a></li>
			    <li><a href="main.py?page=acl">Set/Reset Acl</a></li>-->
			  </ul>

			</li>"""

	if(querystring =="page=iscsi" or querystring =="page=iscsi_tar" or querystring =="page=iscsi_disk" or querystring =="page=iscsi_prop" or querystring =="page=iscsi_det" or querystring =="page=iscsi_ses" or querystring =="page=srp" or querystring =="page=srp_tar" or querystring =="page=srp_disk" or querystring =="page=srp_ini" or querystring =="page=srp_det" or querystring =="page=srp_ses" or querystring =="page=fc" or querystring =="page=fc_tar" or querystring =="page=fc_disk" or querystring =="page=fc_ini" or querystring =="page=fc_det" or querystring =="page=fc_ses"):
	
		print"""
			<li><a href="main.py?page=iscsi" style ="color:#333333;">SAN</a>"""
	else:
		print"""<li>SAN"""

	print"""
			  <ul>"""

	if(querystring =="page=iscsi" or querystring =="page=iscsi_tar" or querystring =="page=iscsi_disk" or querystring =="page=iscsi_prop" or querystring =="page=iscsi_det" or querystring =="page=iscsi_ses"):

		print"""
			    <li><a href="main.py?page=iscsi" style ="color:#333333;">I-SCSI</a>"""
	else:
		print"""<li>I-SCSI"""

	print"""
			      <ul>"""

	if(querystring =="page=iscsi"):
		
		print"""
				<li><a href="main.py?page=iscsi" style ="color:#EC1F27;font-weight:bold;">I-SCSI Status</a></li>"""

	else:
		print"""<li><a href="main.py?page=iscsi">I-SCSI Status</a></li>"""

	if(querystring =="page=iscsi_tar"):
	
		print"""
			    <li><a href="main.py?page=iscsi_tar" style ="color:#EC1F27;font-weight:bold;">I-SCSI Target</a></li>"""
	else:
		print"""
			<li><a href="main.py?page=iscsi_tar">I-SCSI Target</a></li>"""

	if(querystring =="page=iscsi_disk"):
		
		print"""
			   <li><a href="main.py?page=iscsi_disk" style ="color:#EC1F27;font-weight:bold;">Disk To Target</a></li>"""

	else:
		print"""

			<li><a href="main.py?page=iscsi_disk">Disk To Target</a></li>"""

	if(querystring =="page=iscsi_prop"):
	
		print"""
			    <li><a href="main.py?page=iscsi_prop" style ="color:#EC1F27;font-weight:bold;">Properties</a></li>"""
	else:
		print"""<li><a href="main.py?page=iscsi_prop">Properties</a></li>"""

	if(querystring =="page=iscsi_det"):

		print"""
			    <li><a href="main.py?page=iscsi_det" style ="color:#EC1F27;font-weight:bold;">Target Information</a></li>"""
	else:
		print"""<li><a href="main.py?page=iscsi_det">Target Information</a></li>"""

	if(querystring == "page=iscsi_ses"):
		
		print"""
			    <li><a href="main.py?page=iscsi_ses" style ="color:#EC1F27;font-weight:bold;">Session Information</a></li>"""
	else:
		print"""<li><a href="main.py?page=iscsi_ses">Session Information</a></li>"""

	print"""
			      </ul>

			    </li>"""

	if(querystring =="page=srp" or querystring =="page=srp_tar" or querystring =="page=srp_disk" or querystring =="page=srp_ini" or querystring =="page=srp_det" or querystring =="page=srp_ses"):
	
		print"""
			    <li><a href="main.py?page=srp" style ="color:#333333;">SRP</a>"""
	else:
		print"""<li>SRP"""

	print"""
			      <ul>"""

	if(querystring =="page=srp"):
	
		print"""<li><a href="main.py?page=srp" style ="color:#EC1F27;font-weight:bold;">SRP Status</a></li>"""
	else:
		print"""<li><a href="main.py?page=srp">SRP Status</a></li>"""

	if(querystring =="page=srp_tar"):
	
		print"""<li><a href="main.py?page=srp_tar" style ="color:#EC1F27;font-weight:bold;">SRP Target</a></li>"""
	else:
		print"""<li><a href="main.py?page=srp_tar">SRP Target</a></li>"""

	if(querystring =="page=srp_disk"):
	
		print"""<li><a href="main.py?page=srp_disk" style ="color:#EC1F27;font-weight:bold;">Disk To Target</a></li>"""

	else:
		print"""<li><a href="main.py?page=srp_disk">Disk To Target</a></li>"""

	if(querystring =="page=srp_ini"):
		
		print"""<li><a href="main.py?page=srp_ini" style ="color:#EC1F27;font-weight:bold;">SRP Initiator</a></li>"""

	else:
		print"""<li><a href="main.py?page=srp_ini">SRP Initiator</a></li>"""

	if(querystring =="page=srp_det"):
		
		print"""<li><a href="main.py?page=srp_det" style ="color:#EC1F27;font-weight:bold;">Target Information</a></li>"""

	else:
		print"""<li><a href="main.py?page=srp_det">Target Information</a></li>"""

	if(querystring =="page=srp_ses"):

		print"""<li><a href="main.py?page=srp_ses" style ="color:#EC1F27;font-weight:bold;">Session Information</a></li>"""

	else:
		print"""<li><a href="main.py?page=srp_ses">Session Information</a></li>"""

	print"""
			      </ul>

			    </li>"""

	if(querystring =="page=fc" or querystring =="page=fc_tar" or querystring =="page=fc_disk" or querystring =="page=fc_ini" or querystring =="page=fc_det" or querystring =="page=fc_ses"):

		print"""
			   <li><a href="main.py?page=fc" style ="color:#333333;">FC</a>"""
	else:
		print"""<li>FC"""

	print"""
			      <ul>"""

	if(querystring =="page=fc"):

		print"""<li><a href="main.py?page=fc" style ="color:#EC1F27;font-weight:bold;">Fc Status</a></li>"""
	else:
		print"""<li><a href="main.py?page=fc">Fc Status</a></li>"""

	if(querystring =="page=fc_tar"):
	
		print"""<li><a href="main.py?page=fc_tar" style ="color:#EC1F27;font-weight:bold;">Fc Target</a></li>"""
	else:	
		print"""<li><a href="main.py?page=fc_tar">Fc Target</a></li>"""

	if(querystring =="page=fc_disk"):
	
		print"""<li><a href="main.py?page=fc_disk" style ="color:#EC1F27;font-weight:bold;">Disk To Target</a></li>"""
	else:
		print"""<li><a href="main.py?page=fc_disk">Disk To Target</a></li>"""

	if(querystring =="page=fc_ini"):
	
		print"""<li><a href="main.py?page=fc_ini" style ="color:#EC1F27;font-weight:bold;">Fc Initiator</a></li>"""
	else:
		print"""<li><a href="main.py?page=fc_ini">Fc Initiator</a></li>"""

	if(querystring =="page=fc_det"):
	
		print"""<li><a href="main.py?page=fc_det" style ="color:#EC1F27;font-weight:bold;">Target Information</a></li>"""

	else:
		
		print"""<li><a href="main.py?page=fc_det">Target Information</a></li>"""

	if(querystring =="page=fc_ses"):
	
		print"""<li><a href="main.py?page=fc_ses" style ="color:#EC1F27;font-weight:bold;">Session Information</a></li>"""

	else:
		
		print"""<li><a href="main.py?page=fc_ses">Session Information</a></li>"""

	print"""

			      </ul>

			    </li>
			

			 <!--<li><a href="../i-scsi/disk-configuration.html"  style ="text-decoration:none;font-weight: bold; font-size: 12px;"></a></li>
			<li><a href="../i-scsi/disk-configuration.html"  style ="text-decoration:none;font-weight: bold; font-size: 12px;"></a></li>-->

			  </ul>
			
			</li>"""

	if(querystring =='page=vtls'):

		print"""<li><a href="main.py?page=vtls" style ="color:#333333;"> VTL</a>"""
	else:
		print"""<li>VTL"""	

	print"""
			  <ul>"""

	if(querystring =='page=vtls'):

		print"""<li><a href="main.py?page=vtls"  style ="color:#EC1F27;font-weight:bold;">VTL Settings</a></li>"""
	else:
		print"""<li><a href="main.py?page=vtls">VTL Settings</a></li>"""
	print"""
			  </ul>
			</li>"""
	if(querystring == 'page=nd' or querystring == 'page=disk_list' or querystring == 'page=rs' or querystring =='page=crs' or querystring =='page=cvs'):
	
		print"""
			<li><a href="main.py?page=nd" style ="color:#333333;">RAID</a>"""
	else:
		print"""<li>RAID"""
	print"""
			  <ul>"""
	if(querystring == 'page=nd' or querystring == 'page=disk_list'):
		print"""<li><a href="main.py?page=nd" style ="color:#333333;">Volume Configuration</a>"""
	else:
		print"""<li>Volume Configuration"""
	print"""
			      <ul>"""
	if(querystring == 'page=nd'):
		print"""<li><a href="main.py?page=nd" style ="color:#EC1F27;font-weight:bold;">Disk Configuration</a></li>"""
	else:
		print"""
			<li><a href="main.py?page=nd">Disk Configuration</a></li>"""
	if(querystring == 'page=disk_list'):
	
		print"""<li><a href="main.py?page=disk_list" style ="color:#EC1F27;font-weight:bold;">Disk List</a></li>"""
	else:
		
		print"""<li><a href="main.py?page=disk_list">Disk List</a></li>"""
	print"""
			      </ul>
			    </li>"""
	if(querystring == 'page=rs'):
		print"""<li><a href="main.py?page=rs" style ="color:#EC1F27;font-weight:bold;">Raid Setup</a></li>"""
	else:
		
		print"""<li><a href="main.py?page=rs">Raid Setup</a></li>"""

	if(querystring == 'page=crs'):
		print"""<li><a href="main.py?page=crs" style ="color:#EC1F27;font-weight:bold;">Raid Set Functions</a></li>"""
	else:
		print"""<li><a href="main.py?page=crs">Raid Set Functions</a></li>"""

	if(querystring == 'page=cvs'):
		print"""<li><a href="main.py?page=cvs" style ="color:#EC1F27;font-weight:bold;">Volume Set Functions</a></li>"""
	else:
		print"""<li><a href="main.py?page=cvs">Volume Set Functions</a></li>"""

	print """
		
			  </ul>
			</li>"""
	if(querystring == 'page=scan' or querystring == 'page=logs' or querystring == 'page=infini' or querystring == 'page=sr' or querystring == 'page=re_mount' or querystring == 'page=sd' or 'page=ss' in querystring or querystring == 'page=mail' or 'page=mu' in querystring or querystring == 'page=updts' or querystring == 'page=gr' or querystring == 'page=fs2'):

		print"""
			<li><a href="main.py?page=infini" style ="color:#333333;">MAINTENANCE</a>"""
	else:
		print """<li>MAINTENANCE"""
	print"""
			  <ul>"""
	if(querystring == 'page=infini'):
	
		print"""<li><a href="main.py?page=infini" style ="color:#EC1F27;font-weight:bold;">Infiniband</a></li>"""
	else:
		
		print"""<li><a href="main.py?page=infini">Infiniband</a></li>"""
	if(querystring == 'page=sr'):
	
		print"""<li><a href="main.py?page=sr" style ="color:#EC1F27;font-weight:bold;">Services</a></li>"""
	else:
		
		print"""<li><a href="main.py?page=sr">Services</a></li>"""
	if(querystring == 'page=logs'):
	
		print"""<li><a href="main.py?page=logs" style ="color:#EC1F27;font-weight:bold;">Logs</a></li>"""
	else:
		
		print"""<li><a href="main.py?page=logs">Logs</a></li>"""

	if(querystring == 'page=fs2'):

                print"""<li><a href="main.py?page=fs2" style ="color:#EC1F27;font-weight:bold;">Backup</a></li>"""
		#print
        else:

                print"""<li><a href="main.py?page=fs2">Backup</a></li>"""
		#print
	if(querystring == 'page=sd'):
	
		print"""<li><a href="main.py?page=sd" style ="color:#EC1F27;font-weight:bold;">Shutdown</a></li>"""
	else:
		
		print"""<li><a href="main.py?page=sd">Shutdown</a></li>"""
	if(querystring == 'page=scan'):
	
		print"""<li><a href="main.py?page=scan" style ="color:#EC1F27;font-weight:bold;">Scan Volume</a></li>"""
	else:
		
		print"""<li><a href="main.py?page=scan">Scan Volume</a></li>"""
	if(querystring == 'page=re_mount'):
		
		print"""<li><a href="main.py?page=re_mount" style ="color:#EC1F27;font-weight:bold;">Remount</a></li>"""
	else:
		
		print"""<li><a href="main.py?page=re_mount">Remount</a></li>"""
	if('page=ss' in querystring):
		
		print"""<li><a href="main.py?page=ss" style ="color:#EC1F27;font-weight:bold;">Snapshot</a></li>"""
	else:
		
		print"""<li><a href="main.py?page=ss">Snapshot</a></li>"""
	if('page=mu' in querystring):
		print"""<li><a href="main.py?page=mu" style ="color:#EC1F27;font-weight:bold;">Manage users</a></li>"""
	else:
		
		print"""<li><a href="main.py?page=mu">Manage users</a></li>"""
	if(querystring == 'page=updts'):
	
		print"""<li><a href="main.py?page=updts" style ="color:#EC1F27;font-weight:bold;">Updates</a></li>"""
	else:
		
		print"""<li><a href="main.py?page=updts">Updates</a></li>"""
	if(querystring == 'page=mail'):

		print"""<li><a href="main.py?page=mail" style ="color:#EC1F27;font-weight:bold;">Mail Configuration</a></li>"""
	else:
		
		print"""<li><a href="main.py?page=mail">Mail Configuration</a></li>"""
	print"""
			    <!--<li><a href="main.py?page=rr">FS4 Data Analysis(rrd)</a></li>
			    <li><a href="main.py?page=gr">FS4 Data Analysis</a></li>-->
			  </ul>
			</li>
			<li>Fs2 Data Analysis
			  <ul>
			  <li>System Temperature
			  <ul>
			   
			<li><a class='various' data-fancybox-type='iframe' style='color:#666666;text-decoration:none;' href='canvas_temperature_graph.py'>Temperature</a></li>
			<!--<li><a class='various' data-fancybox-type='iframe' style='color:#666666;text-decoration:none;' href='draw_graph.py'>Temperature2</a></li>-->
			</ul>
				</li>

			<li>Memory
			  <ul>
			   
			<!--<li><a class='various' data-fancybox-type='iframe' style='color:#666666;text-decoration:none;' href='draw_mem.py'>Memory1</a></li>-->
			<li><a class='various' data-fancybox-type='iframe' style='color:#666666;text-decoration:none;' href='canvas_mem_graph.py'>Memory </a></li>
			</ul>
				</li>
			   <li><!--<a href="resources.py" style ="text-decoration:none;font-weight: bold; font-size: 12px;">I-SCSI Status</a>-->
			    <li>Disk Graph
			      <ul>"""

	#if (alldisk != [{'type': 'NAS'}, {'type': 'BIO'}, {'type': 'FIO'}, {'type': 'SNP'}, {'type': 'VTL'}]):
	if(nas_info["lvs"]!=[{}]):
		for disk_detail in nas_info["lvs"]:
			disk_info = disk_detail['lv_name']
			#print"""<li><a href="main.py?page=dg">"""+disk_detail+"""</a></li>"""
			#print """<li><a class='various' data-fancybox-type='iframe' style='color:green; font-weight: bold; width:100%; float:right; text-decoration:none;' href='disk_graph?lv_name="""+disk_detail+"""'>"""+disk_detail+"""</a></li>"""
			print"""<li><a class='various' data-fancybox-type='iframe' style='color:#666666;text-decoration:none;' href='canvas_disk_usage.py?disk_name="""+disk_info+"""'>"""+disk_info+"""</a></li>"""


	print"""
			      </ul>
			    </li>
			   <li>Interface
			   <ul>"""

	for iface in get_all_ip:
		iface_info =  iface['iface']

		print"""<li><a class='various' data-fancybox-type='iframe' style='color:#666666;text-decoration:none;' href='canvas_traffic.py?ethernet="""+iface_info+"""'>"""+iface_info+"""</a></li>"""


	print"""			</ul>
				</li>
				</ul>
				</li>"""
	if(querystring == "page=support"):
		print"""<li><a href="main.py?page=support" style ="color:#333333;">HELP</a>"""
	else:
		
		print"""<li>HELP"""
	print"""
			  <ul>"""
	if(querystring == "page=support"):
		print"""<li><a href="main.py?page=support" style ="color:#EC1F27;font-weight:bold;">Support</a></li>"""
	else:
		print"""<li><a href="main.py?page=support">Support</a></li>"""
	print"""
			  </ul>
			</li>
			
		      </ul>
		    </div>
		  </nav>
		</div>
	      </div>
	      <!--Left side navigation ends here-->
	"""

except Exception as e:
        disp_except.display_exception(e);
