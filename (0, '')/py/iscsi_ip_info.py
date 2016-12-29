#!/usr/bin/python
#_*_ coding: UTF-8 _*_

#enable debugging
import traceback, sys
sys.path.append('../modules')
import disp_except;
try:
	import cgitb, os, sys, commands, common_methods, cgi, array, traceback
	cgitb.enable()
	sys.path.append('/var/nasexe/storage')
	import storage_op
	from lvm_infos import *
	from functions import *
	import san_disk_funs
	san_list = san_disk_funs.list_all_disk_att()
	#print san_list
	#sys.path.append('/var/nasexe/')
	#import storage
	
	form = cgi.FieldStorage()
	querystring = os.environ['QUERY_STRING'];
	#print querystring
	
	ini_name = form.getvalue('ini_name')
	ip = form.getvalue('ip')
	data_dig=form.getvalue('data_dig');	
	fbl = form.getvalue('fbl')
	#ips = form.getvalue('ip')
	maxxmit = form.getvalue('maxxmit')
	maxblen = form.getvalue('maxburst_len')
	ini_R2t = form.getvalue('ini_r2t')
	max_ini_R2t = form.getvalue('max_ini_r2t')
	none_cmd_out=form.getvalue('none_cmd_out')	
	active_cmd = form.getvalue('active_cmd')
	header_digest = form.getvalue('hd')
	imd_data = form.getvalue('imd')
	write_cmd = form.getvalue('write_cmd')
	read_cmd = form.getvalue('read_cmd')
	sid_cmd = form.getvalue('sid')
	write_io = form.getvalue("write_kb")
	#print write_io
	read_io = form.getvalue("read_kb")
	#print read_io
	
	#print """<script>javascript:parent.jQuery.fancybox.close();</script>""";

	

	print """
	<head>

	 <SCRIPT language=Javascript>
      
      function isNumberKey(evt)
      {
         var charCode = (evt.which) ? evt.which : event.keyCode
         if (charCode > 31 && (charCode < 46 || charCode > 57 || charCode == 190))
            return false;

            return true;

      }
     
        </SCRIPT>
 
	<script type = "text/javascript">
	function hideMessage() {
	$(document).ready(
	function(){
	          $("#id_trace_err").fadeOut(2000);
		  $("#id_trace").fadeOut(2000);
		  }
		  );
		 }
	var tim = window.setTimeout("hideMessage()", 10000);  // 10000 milliseconds = 10 seconds
	</script>	
	
	<h1 align="center"><u><font color ="silver">Iscsi Ip Info</font></u></h1>
	</head>
	<form method="POST" align ="center" action="" name="add_disk" >
</tr> </table><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
	<body align="center">
	<div style="margin-top:-33%;margin-left:8%;">
				<!--	<table width="120" align = "center" cellspacing="1" cellpadding="2" border="1" >

	<th>Device Id</th>	
	<th>Threads Pool</th>
	<th>Type</th>
        <th>USN</th>

						<tr>
							<td valign="top" align="left" colspan="4">
							<table width="400" align="center" cellspacing="1" cellpadding="2" border="1" class="uter_border">
	<tr>
	<th><font color="green">""""""</font></th>
	<th><font color="green">""""""</font></th>
	<th><font color="green">""""""</font></th>
	<th><font color="green">""""""</font></th>
	</tr>
	</table>--></div></form>
	</table>
	<br/>
	<br/>
	<table>	
	<tr>
        <th><font color = "#999999">Initiator Name:</font></th><td><font color="green">"""+ini_name+"""</font></td>
        </tr>

	<tr>
	<th><font color = "#999999">Client IP:</font></th><td><font color="green">"""+ip+"""</font></td>
	</tr>
	 <tr>
        <th><font color = "#999999">SID:</font></th><td><font color="green">"""+sid_cmd+"""</font></td>
        </tr>
	<tr>
	<th><font color = "#999999">Data-Digest:</font></th><td><font color="green">"""+data_dig+"""</font></td>
	</tr>
	<tr>
        <th><font color = "#999999">FirstBurstLength:</font></th><td><font color="green">"""+fbl+"""</font></td>
        </tr>
        <tr>
        <th><font color = "#999999">MaxXmitDataSegmentLength:</font></th><td><font color="green">"""+maxxmit+"""</font></td>
        </tr>
	<tr>
        <th><font color = "#999999">Max Burst Length:</font></th><td><font color="green">"""+maxblen+"""</font></td>
        </tr>

        <tr>

        <th><font color = "#999999">InitialR2T:</font></th><td><font color="green">"""+ini_R2t+"""</font></td>
        </tr>
	
        <tr>
        <th><font color = "#999999">MaxOutstandingR2T:</font></th><td><font color="green">"""+max_ini_R2t+"""</font></td>
        </tr>

	 <tr>

        <th><font color = "#999999">None Command Out:</font></th><td><font color="green">"""+none_cmd_out+"""</font></td>
        </tr>
        
        <tr>
        <th><font color = "#999999">Active Command:</font></th><td><font color="green">"""+active_cmd+"""</font></td>
        </tr>

	<tr>
        <th><font color = "#999999">Header Digest:</font></th><td><font color="green">"""+header_digest+"""</font></td>
        </tr>
        
        <tr>
        <th><font color = "#999999">Immediate Data:</font></th><td><font color="green">"""+imd_data+"""</font></td>
        </tr>

         <tr>

        <th><font color = "#999999">Write Command Out:</font></th><td><font color="green">"""+write_cmd+"""</font></td>
        </tr>
        
        <tr>
        <th><font color = "#999999">Read Command:</font></font><td><font color="green">"""+read_cmd+"""</font></td>
        </tr>

        <tr>
        <th><font color = "#999999">Write Io Kb:</font></th><td><font color="green">"""+write_io+"""</font></td>
        </tr>
	
        <tr>
        <th><font color = "#999999">Read Io Kb:</font></th><td><font color="green">"""+read_io+"""</font></td>
        </tr>
	</table>
	"""

except Exception as e:
	disp_except.display_exception(e);

