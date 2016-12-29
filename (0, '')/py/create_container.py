#!/usr/bin/python
import cgitb, os, sys, commands, common_methods, traceback, string, system_info, cgi
cgitb.enable()

form = cgi.FieldStorage()

sys.path.append('/var/nasexe/storage')
import storage_op
import lvm_infos
import san_disk_funs
from lvm_infos import *
bl_info = get_vgs()
sys.path.append('/var/nasexe/')
import storage

select_targets=san_disk_funs.iscsi_list_all_tgt_att()
srp_target=san_disk_funs.ib_list_targets()
fc_targets= san_disk_funs.fc_list_targets()

#get_all_used_disk_block = ''
proto_disk = san_disk_funs.get_all_used_disk_block()
#print proto_disk
proto1_disk = san_disk_funs.get_all_used_disk_block(detail='yes')
#print proto1_disk

san_list = san_disk_funs.list_all_disk_att()
targets_list= san_disk_funs.iscsi_list_all_tgt()

if(form.getvalue("create_container")):
	get_volume = form.getvalue("hid_volume")
	get_con_name = form.getvalue("container_name")
	get_con_size = form.getvalue("container_size")
	get_f_op = form.getvalue("adv1")
	get_m_op = form.getvalue("adv2")
	
	if(get_con_name != None and get_con_size!= None):
		get_con_size = get_con_size+'GB'

		if(get_f_op==None):
			get_f_op = ''

		if(get_m_op==None):
			get_m_op = ''

		call_create_con = storage_op.lvcreate(get_volume, get_con_name, get_con_size, get_f_op, get_m_op, type1='FIO')

		if(call_create_con == True):
			print"""<div id = 'id_trace_small'>"""
			print """Container '"""+get_con_name+"""' created Successfully!"""
			print "</div><br/>"
		else:
			print"""<div id = 'id_trace_err_small' >"""
			print """Error Creating Container '"""+get_con_name+"""' !"""
			print "</div><br/>"
	else:
		print "<div id = 'id_trace_err_small' >"
		print "Enter both Container Name & Size!"
		print "</div><br/>"




vg_info = storage.get_pvs()
get_con = storage.get_lvs(type1='FIO')
san_list = san_disk_funs.list_all_disk_att()

get_vol_name = form.getvalue("volume")
get_free_size = form.getvalue("free_size")

print
print """

<head>
<link rel='stylesheet' type='text/css' href='new-tooltip/lptooltip.css' />
<link href="../css/style_new.css" rel="stylesheet" type="text/css"/>
<link rel="stylesheet" href="../fancyBox/source/jquery.fancybox.css" type="text/css" media="screen" />
<script type="text/javascript" src="../fancyBox/source/jquery.fancybox.pack.js"></script>
<script type="text/javascript">
$(document).ready(function() {
$(".various").fancybox({
	maxWidth        : 800,
	maxHeight       : 600,
	fitToView       : false,
	width           : '40%',
	height          : '50%',
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

<SCRIPT language=Javascript>

function isNumberKey(evt)
{
 var charCode = (evt.which) ? evt.which : event.keyCode
 if (charCode > 31 && (charCode < 46 || charCode > 57 || charCode == 190))
    return false;

    return true;

}

</SCRIPT>
<script src="../js/commons.js" type="text/javascript"></script>
<link href="../css/style.css" rel="stylesheet" type="text/css"/>
 <script src="../js/jquery1.7.js"></script>
<script type="text/javascript" src="../js/jquery.alerts.js"></script>
<script type="text/javascript">
        var helperPopup = new Popup('helper'); // Pass an ID to link with an existing DIV in page
        helperPopup.autoHide = false;
        helperPopup.position = "below right";
        helperPopup.constrainToScreen = false;
        </script>
<link href = "../css/jquery.alerts.css" rel = "stylesheet" type = "text/css" />
</head>

<form name = 'create_container' method = 'POST' action = ''>

<table width="90%" style="margin:20px 0 0 20px; text-align:center; border:#D1D1D1 1px solid;"">
<tr>
<td style=" background-color:#D1D1D1; padding:5px;">Create FIO Container</td>
</tr>
</table>

<table width="90%" style="margin:0px 0 0 20px; border-top:#D1D1D1 1px solid; border-right:#D1D1D1 1px solid; border-left:#D1D1D1 1px solid; font-size:12px;">
<tr>
<th align="left" style="padding:5px;">Selected Volume</th>
<td>"""+get_vol_name+"""</td>
<input type="hidden" name="hid_volume" value='"""+get_vol_name+"""' />
<input type ="hidden" name="free_size2" value="""+str(get_free_size)+""">
</tr>

<tr>
<th align="left" style="padding:5px;">Available size in Volume</th>
<td>"""+get_free_size+"""</td>
</tr>

<tr>
<th align="left" style="padding:5px;">Enter Container Name</th>
<td><input class = 'textbox' type = 'text' name = 'container_name' id = 'container_name' style="width:187px;"></td>    
</tr>

<tr>
<th align="left" style="padding:5px;">Enter Container Size (GB)</th>
<td><input class = 'textbox' type = 'text' name = 'container_size' onkeypress="return isNumberKey(event)" id = 'container_size' style="width:187px;"></td>    
</tr>

<tr>
<td><input type="checkbox" name="advance_option" id="adv_chk" onclick = 'return nas_advance_config2() ' /> Advance Options</td>
<td></td>    
</tr>

</table>

<table id="adv_txt1"  width="90%" style="margin:0px 0 0 20px; padding:0 0 0 20px; border-left:#D1D1D1 1px solid; border-right:#D1D1D1 1px solid; font-size:12px; display:none;">

<tr>
<th align="right">Format Option</th>
<td><input type= "text" class="textbox" name = "adv1" id = "inpt1_adv1" onclick="enable()" style="width:187px;"/></td>
</tr>

<tr>
<th align="right">Mount Option</th>
<td><input type= "text" class="textbox" name= "adv2" id = "inpt2_adv2" onclick="enable()" style="width:187px;"/></td>
</tr>

</table>

<table width="90%" style="margin:0px 0 0 20px; border-left:#D1D1D1 1px solid; border-right:#D1D1D1 1px solid; border-bottom:#D1D1D1 1px solid; font-size:12px;">
<tr>
<td>
<button class="buttonClass" style="float:right; margin:0 30px 20px 0; font-size:12px;" type="submit" name = 'create_container'  id = 'create_container' value = 'create_container'  onclick = 'return validate_create_container();'>Create</button>
</td>
</tr>


</table>
</form>

</body>
</html>


"""
