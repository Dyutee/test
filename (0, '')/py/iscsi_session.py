#!/usr/bin/python
import cgitb, sys,  common_methods, cgi, include_files
cgitb.enable()

sys.path.append('/var/nasexe/storage')
import storage_op
import sys,os
from lvm_infos import *
from functions import *
import san_disk_funs

form = cgi.FieldStorage()
querystring = os.environ['QUERY_STRING'];
target_name = form.getvalue("target")
db_list_target = [target_name]
iscsi_status = common_methods.get_iscsi_status();

ses_ip = ''
remove_targets_list= san_disk_funs.iscsi_list_all_tgt()
#print remove_targets_list
###########Session ##########################

#for ses_tar in remove_targets_list:
for ses_tar in db_list_target:
	sesion_tar =san_disk_funs.iscsi_session(ses_tar)
	for ses_info in sesion_tar:
		sesi_get = san_disk_funs.iscsi_session_info(ses_tar, ses_info)
		ses_ip = sesi_get['ips']


#if(form.getvalue('sess_target_name')):
#	session_target_select = form.getvalue('sess_target_name')
#import left_nav
if (iscsi_status > 0):

	print
	print """	
	<head>
                <link rel="stylesheet" href="../fancyBox/source/jquery.fancybox.css" type="text/css" media="screen" />
                <script type="text/javascript" src="../fancyBox/source/jquery.fancybox.pack.js"></script>
                <script type="text/javascript">
                $(document).ready(function() {
                $(".various").fancybox({
                        maxWidth        : 800,
                        maxHeight       : 600,
                        fitToView       : false,
                        width           : '98%',
                        height          : '98%',
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
	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer" style="margin:0;width:716px;padding-left:0px;">
		<!--tab srt-->
		<div class="searchresult-container">
		  <div class="infoheader">
		   <!-- <div id="tabs">
		      <ul>
			<li><a href="#tabs-1">iSCSI Session</a></li>
		      </ul>
		      <div id="tabs-1">-->

		<!--form container starts here-->
		<div class="form-container" style="width: 96.9%;">
		<div class="topinputwrap-heading">iSCSI Session Information</div>
		  <div class="inputwrap">
		    <div class="formrightside-content">

		<form name = 'add_info' method = 'POST'>
					<table width = "685" border = "1" cellspacing = "0" cellpadding = "0" name = 'disp_tables' id = 'id_target_info'style ="border-style:ridge;">


		 <tr style = 'background-color:#999999; font-weight: bold;'>
							<!--<td height = "35px" valign = "middle">Action</td>-->
							<td height = "35px" valign = "middle" style = 'color: #FFF;'>Target</td>
							<td height = "35px" valign = "middle" style = 'color: #FFF;text-align:center;'>Disks</td>
							<td height = "35px" valign = "middle" style = 'color: #FFF;text-align:center;'>Initiators</td>
							<td height = "35px" valign = "middle" style = 'color: #FFF;text-align:center;'>Client IP Info</td>
						</tr>"""

	#--------------------------Initialise session ip is empty-------------------------
	if(ses_ip!= ''):
		#for tar_info in remove_targets_list:
		for tar_info in db_list_target:
			#print 'Tar:'+str(tar_info)
		#if(tar_info == target_name):
			sesion_tar =san_disk_funs.iscsi_session(tar_info)
	#-----------------------------------End------------------------------------------
			if (sesion_tar != []):
				print"""<tr>
									<!--<td class = "table_content" height = "35px" valign = "middle">
			<a href = 'main.php?page=iscsi&act=add_disk_tgt_done&target=<?= $show_targets ?>'><img border = '0' style = 'margin-top: 2px;' src = '../images/add.png' title = 'Add disk to target' /></a>&nbsp;<a href = 'main.php?page=iscsi&act=del_disk_tgt_done&t=<?= $show_targets ?>'><img border = '0' src = '../images/fileclose.png' title = 'Remove disk from target' /></a>&nbsp;<a href = 'get_properties.php?target=<?= $show_targets ?>'><img border = '0' src = '../images/properties.png' title = 'Target properties' /></a> </td>-->


				<td height = "35px" valign = "middle" style= "text-decoration:blink;">"""
				#-------------------------pass the target name in backend Function to get session is active or not for that target----------------------------
				#print 'SESI:'+ses_ip
				for ses_info in sesion_tar:
				#print ses_info
				#print tar_info
					ses_get = san_disk_funs.iscsi_session_info(tar_info, ses_info)
				#print ses_get['ips']
				if (ses_get['ips'] != ''):
					print""" <font color = 'darkgreen'>"""+tar_info+"""</font>"""
				print """</td>"""

				print"""<td height = "35px" valign = "middle" >"""

				used_disks_nm = san_disk_funs.iscsi_used_disks_tgt(tar_info)
				replace_disk_nm = str(used_disks_nm).replace('[]', '')
				replace_disk_nm1 = str(replace_disk_nm).replace('[', '')
				replace_disk_nm2 = str(replace_disk_nm1).replace(']', '')
				replace_used_disk = str(replace_disk_nm2).replace("'", '')
				print replace_used_disk
				#for disk_info_lst in alldisk:
				#       if len(ses_get['ips']) != 0:
				#               print disk_info_lst 
				#       else:
				#               print disk_info_list

				print"""</td>"""
				print"""
									<td height = "35px" valign = "middle">"""

			#for target_pass in remove_targets_list:
				sess_show=san_disk_funs.iscsi_session(tar_info)
				sess_ini_list =san_disk_funs.iscsi_ini_list(tar_info)
				#print 'SES LIST:'+str(sess_ini_list)
				replace_ses_ini = str(sess_ini_list).replace('[]', '')
				#print 'rep1:'+replace_get_ini
				#print '<br/>'
				ses_initiator = str(replace_ses_ini).replace('[', '')
				ses_initiator1 = str(ses_initiator).replace(']', '')
				ses_initiator2 = str(ses_initiator1).replace("'", '')
				#print 'GET I:'+ get_initiator2
				ses_initiator3 = str(ses_initiator2).replace('*', 'Access for all ip(*)' )
				ses_initiator3 = ses_initiator3.replace(',', '<BR>');
				ses_initiator4 = ses_initiator3.replace('#', ' through ')
				print ses_initiator4


				#for sess_val in sess_show:
					#print sess_val
				#       sess_f=san_disk_funs.iscsi_session_info(tar_info,sess_val)
					#print sess_f
					#print sess_f['initiator_name']+"<br/>"
				#----------------------------------End-----------------------------------------------
				print """</td>
									<td height = "35px" valign = "middle">"""

				for sess_val in sess_show:
					#print sess_val
					sess_f=san_disk_funs.iscsi_session_info(tar_info,sess_val)
					#print sess_f
					print"""<a class="various" data-fancybox-type="iframe" style="color:#292915;text-decoration:none;" href="iscsi_ip_info.py?ip="""+sess_f["ips"]+"""&data_dig="""+sess_f["DataDigest"]+"""&fbl="""+sess_f["FirstBurstLength"]+"""&maxxmit="""+sess_f["MaxXmitDataSegmentLength"]+"""&maxburst_len="""+sess_f["MaxBurstLength"]+"""&none_cmd_out="""+sess_f["none_cmd_count"]+"""&ini_r2t="""+sess_f['InitialR2T']+"""&max_ini_r2t="""+sess_f["MaxOutstandingR2T"]+"""&active_cmd="""+sess_f["active_commands"]+"""&hd="""+sess_f["HeaderDigest"]+"""&imd="""+sess_f["ImmediateData"]+"""&write_cmd="""+sess_f["write_cmd_count"]+"""&read_cmd="""+sess_f["read_cmd_count"]+"""&sid="""+sess_f["sid"]+"""&read_kb="""+sess_f["read_io_count_kb"]+"""&write_kb="""+sess_f["write_io_count_kb"]+"""&ini_name="""+sess_f["initiator_name"]+""""><b><font color="green">"""+sess_f["ips"]+"""</font></b></a>"""+ "<br/>"
				print """</td>

								</tr>"""

	else:
		print """
		<tr>
		<td align = 'center' height="50px;" colspan="4">
		<font>No-Client is Connected</font>
		</td>
		</tr>"""



	print"""	
	</table>
	</form>"""
	print"""</div>
		  </div>
		</div>
		<!--form container ends here-->
		      </div>
	"""
else:
	print "<div style = 'margin-top: 10%; margin-bottom: 10%; margin-left: auto; margin-right: auto; text-align: center; vertical-align: center; color: darkred; width: 65%; font: 16px Arial;'>Check the 'Enable/Disable i-SCSI' option in Maintenance -><a href ='main.py?page=sr'style ='text-decoration:underline;'>Services</a>.</div>"
print"""
"""
