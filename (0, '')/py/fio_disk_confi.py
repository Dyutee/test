#!/usr/bin/python
import cgitb, header, header, os, sys, commands, common_methods, traceback, string, system_info
cgitb.enable()


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

checked_bio_rm = ''
checked_fio_rm = ''
checked_bio = ''
checked_fio = ''
get_radio = ''
get_radio_rm = ''
get_vol_chk_2 = ''
get_vol_chk = ''
selected_con = ''
display_bio = 'block'
display_fio = 'none'
display_cr_con = 'none'
display_cr_img = 'none'
display_rm_con = 'none'
display_rm_img = 'none'
display_add_san = 'none'
display_remove_san = 'none'
display_details = 'none'

san_list = san_disk_funs.list_all_disk_att()
targets_list= san_disk_funs.iscsi_list_all_tgt()

if(header.form.getvalue("delete_san_but")):
	san_val = header.form.getvalue("delete_option_san[]")
	print san_val
	check_san = isinstance(san_val, str)
	if(check_san == True):
		remove_san =san_disk_funs.remove_disk_san(san_val)
		print remove_san
	else:
		san_val = set(san_val)
		for san in san_val:
			remove_san = san_disk_funs.remove_disk_san(san)

	if(remove_san== True):
		print"""<div id = 'id_trace'>"""
		print " Disk <font color='darkred'><b>"+str(san_val)+"</b></font> Successfully Deleted!"
		print "</div>"
	else:
		print"""<div id = 'id_trace_err'>"""
		print "Error occured while deleting Disk <font color = 'darkred'><b>"+str(san_val)+"</b></font> !"
		print "</div>"


if(header.form.getvalue("delete_but")):
	get_lv = header.form.getvalue("delete_option[]")
	check_get_lv =isinstance(get_lv, str)

	if(check_get_lv ==True):
		remove_lv = storage_op.lvremove(get_lv, type1='BIO')

	else:
		get_lv = set(get_lv)
		for value in get_lv:
			remove_lv = storage_op.lvremove(value, type1='BIO')


	if(remove_lv == True):
		print"""<div id = 'id_trace'>"""
		print " Disk <font color='darkred'><b>"+str(get_lv)+"</b></font> Successfully Deleted!"
		print "</div>"
	else:
		print"""<div id = 'id_trace_err'>"""
		print "Error occured while deleting Disk <font color = 'darkred'><b>"+str(get_lv)+"</b></font> !"
		print "</div>"


if(header.form.getvalue("create_container")):
	get_volume = header.form.getvalue("volume")
	get_con_name = header.form.getvalue("container_name")
	get_con_size = header.form.getvalue("container_size")
	get_f_op = header.form.getvalue("adv1")
	get_m_op = header.form.getvalue("adv2")

	get_con_size = get_con_size+'GB'

	if(get_f_op==None):
		get_f_op = ''

	if(get_m_op==None):
		get_m_op = ''

	call_create_con = storage_op.lvcreate(get_volume, get_con_name, get_con_size, get_f_op, get_m_op, type1='FIO')


	display_bio = 'none'
	display_fio = 'block'
	display_cr_con = 'none'
	display_cr_img = 'none'
	display_rm_con = 'none'
	display_rm_img = 'none'
	display_add_san = 'none'
	display_remove_san = 'none'

	if(call_create_con == True):
		print"""<div id = 'id_trace'>"""
		print """Container '"""+get_con_name+"""' created Successfully!"""
		print "</div>"
	else:
		print"""<div id = 'id_trace_err' >"""
		print """Error Creating Container '"""+get_con_name+"""' !"""
		print "</div>"



if(header.form.getvalue("remove_container")):
	get_volume = header.form.getvalue("volume")
	call_remov_con = storage_op.lvremove(get_volume,type1='FIO')
	if(call_remov_con == True):
		print "<div id='id_trace'>"
		print "Container deleted successfully!"
		print "</div>"
	else:
		print "<div id='id_trace_err'>"
		print "Error deleting Container!"
		print "</div>"

	display_bio = 'none'
	display_fio = 'block'
	display_cr_con = 'none'
	display_cr_img = 'none'
	display_rm_con = 'none'
	display_rm_img = 'none'
	display_add_san = 'none'
	display_remove_san = 'none'



if(header.form.getvalue("delete_container")):
	get_vol_array = header.form.getvalue("delete_option_img[]")
	if(get_vol_array != None):
		check_vol = isinstance(get_vol_array, str)
		if(check_vol == True):
			call_remov_con = storage_op.lvremove(get_vol_array,type1='FIO')
			if(call_remov_con == True):
				print "<div id='id_trace'>"
				print "Container deleted successfully!"
				print "</div>"
			else:
				print "<div id='id_trace_err'>"
                                print "Error deleting Container!"
                                print "</div>"

			display_bio = 'none'
			display_fio = 'block'
			display_cr_con = 'none'
			display_cr_img = 'none'
			display_rm_con = 'none'
			display_rm_img = 'none'
			display_add_san = 'none'
			display_remove_san = 'none'
		else:
			for x in get_vol_array:
				call_remov_con = storage_op.lvremove(x,type1='FIO')
	else:
		print"""<div id = 'id_trace_err' >"""
		print """Please Select a container to Delete!"""
		print "</div>"


if(header.form.getvalue("volume_con")):
	get_vol_chk = header.form.getvalue("volume_con")
	size_lv = storage.get_size_lv(get_vol_chk,type2='FIO')

	images=storage_op.list_size_images(get_vol_chk)
	tot_vir_size=0.0
	tot_disk_size=0.0
	if len(images) ==0:
		re={'lvsize':size_lv,'vmsize':tot_vir_size,'dsize':tot_disk_size}

	for vm in images:
		siz_t=vm['size']
		t_v=storage_op.convert_size(siz_t)
		tot_vir_size+=t_v
		siz_d=vm['used']
		t_d=storage_op.convert_size(siz_d)
		tot_disk_size+=t_d

	re={'lvsize':size_lv,'vmsize':tot_vir_size,'dsize':tot_disk_size}

	u_siz = re['vmsize']
	lv_siz1 = re['lvsize']
	un_use = lv_siz1 - u_siz

	selected_con = 'selected'
	display_bio = 'none'
	display_fio = 'none'
	display_cr_con = 'none'
	display_cr_img = 'block'
	display_rm_con = 'none'
	display_rm_img = 'none'
	display_add_san = 'none'
	display_remove_san = 'none'


else:
	un_use = ''
	selected_con = 'selected'



if(header.form.getvalue("create_image")):
	get_vol_chk = header.form.getvalue("volume_con")
	get_img_name = header.form.getvalue("img_name")
	get_img_size = header.form.getvalue("img_size")
	get_img_size = get_img_size+'GB'
	mod_img_name = "TYRFS-"+str(get_img_name)

	test_img_name = storage.storage_op.test_image(mod_img_name)
	if test_img_name  == True:
		call_cr_img = storage.storage_op.fio_image_create(get_img_name,get_vol_chk,get_img_size)

		display_bio = 'none'
		display_fio = 'block'
		display_cr_con = 'none'
		display_cr_img = 'none'
		display_rm_con = 'none'
		display_rm_img = 'none'
		display_add_san = 'none'
		display_remove_san = 'none'

		if(call_cr_img == True):
			print"""<div id = 'id_trace'>"""
			print """Image '"""+get_img_name+"""' created Successfully!"""
			print "</div>"
		else:
			print"""<div id = 'id_trace_err' >"""
			print """Error Creating Image '"""+get_img_name+"""' !"""
			print "</div>"

	else:
		print"""<div id = 'id_trace_err' >"""
		print """Image '"""+get_img_name+"""' already Exists !"""
		print "</div>"

	get_vol_chk = ''
	un_use = ''


if(header.form.getvalue("volume_con_rm")):
	get_vol_chk_2 = header.form.getvalue("volume_con_rm")

	display_bio = 'none'
	display_fio = 'none'
	display_cr_con = 'none'
	display_cr_img = 'none'
	display_rm_con = 'none'
	display_rm_img = 'block'
	display_add_san = 'none'
	display_remove_san = 'none'


if(header.form.getvalue("remove_image")):
	get_con_rm = header.form.getvalue("volume_con_rm")
	get_img_rm = header.form.getvalue("volume_img_rm")


	check_file = os.path.isfile('/storage/FIO/'+get_con_rm+'/'+get_img_rm)

	if(check_file==True):
		rm_image = commands.getstatusoutput('sudo rm -rf /storage/FIO/'+get_con_rm+'/'+get_img_rm)

		display_bio = 'none'
		display_fio = 'block'
		display_cr_con = 'none'
		display_cr_img = 'none'
		display_rm_con = 'none'
		display_rm_img = 'none'
		display_add_san = 'none'
		display_remove_san = 'none'

		if(rm_image[0]==0):
			print"""<div id = 'id_trace'>"""
			print """Image '"""+get_img_rm+"""' removed Successfully!"""
			print "</div>"
		else:
			print"""<div id = 'id_trace_err' >"""
			print """Error Deleting Image '"""+get_img_rm+"""'!"""
			print "</div>"

	else:
		print"""<div id = 'id_trace_err' >"""
		print """Image not Found!"""
		print "</div>"

	get_vol_chk_2 = ''


if(header.form.getvalue("select_disk")):
	get_radio = header.form.getvalue("select_disk")
	if(get_radio != ''):
		if(get_radio == 'bio'):
			call_func = storage.get_lvs(type1='BIO')
			checked_bio = 'checked'
			checked_fio = ''
		else:
			call_func = storage.get_lvs(type1='FIO')
			checked_bio = ''
			checked_fio = 'checked'

	display_bio = 'none'
	display_fio = 'none'
	display_cr_con = 'none'
	display_cr_img = 'none'
	display_rm_con = 'none'
	display_rm_img = 'none'
	display_add_san = 'block'
	display_remove_san = 'none'

#########Add to San################################



if(header.form.getvalue("add_to_san")):
	get_radio = header.form.getvalue("select_disk")
	get_lv_name = header.form.getvalue("select_lv")
	get_san_name = header.form.getvalue("san_name")
	get_san_blocksize = header.form.getvalue("select_block")
	if(get_radio == 'bio'):
		get_path = '/dev/peg/BIO-'+str(get_lv_name)
		disk_type = 'BIO'
	if(get_radio == 'fio'):
		split_gln = string.split(get_lv_name, ':')
		get_path = '/storage/'+split_gln[1]+'/'+split_gln[0]
		disk_type = 'FIO'
	call_add_func = san_disk_funs.add_disk_san(get_path,get_san_name,get_san_blocksize,type=disk_type)
	#print call_add_func
	display_bio = 'none'
	display_fio = 'none'
	display_cr_con = 'none'
	display_cr_img = 'none'
	display_rm_con = 'none'
	display_rm_img = 'none'
	display_add_san = 'none'
	display_remove_san = 'none'
	display_details = 'block'

	if(call_add_func == True):
		print"""<div id = 'id_trace'>"""
		print """Successfully added '"""+get_lv_name+"""' to SAN!"""
		print "</div>"
	else:
		print"""<div id = 'id_trace_err' >"""
		print """Error adding '"""+get_lv_name+"""' to SAN!"""
		print "</div>"


	get_radio = ''
	checked_bio = ''
        checked_fio = ''


############## Select Disk to remove##########

if(header.form.getvalue("select_disk_rm")):
	get_radio_rm = header.form.getvalue("select_disk_rm")
	if(get_radio_rm != ''):
		disks = san_disk_funs.list_all_disk()
		if(get_radio_rm == 'bio'):
			call_func = disks['BIO']
			checked_bio_rm = 'checked'
			checked_fio_rm = ''
		else:
			call_func = disks['FIO']
			checked_bio_rm = ''
			checked_fio_rm = 'checked'

	display_bio = 'none'
	display_fio = 'none'
	display_cr_con = 'none'
	display_cr_img = 'none'
	display_rm_con = 'none'
	display_rm_img = 'none'
	display_add_san = 'none'
	display_remove_san = 'block'

###########Remove from San#################



if(header.form.getvalue("remove_from_san")):
	get_radio_rm = header.form.getvalue("select_disk_rm")
	get_lv_name_rm = header.form.getvalue("select_lv_rm")

	if(get_radio_rm == 'bio'):
		disk_type = 'BIO'
	if(get_radio_rm == 'fio'):
		disk_type = 'FIO'
	xyz = []
	for remove in targets_list:
		used_disk = san_disk_funs.iscsi_used_disks_tgt(remove)
		if(len(used_disk) > 0):
			xyz.append(used_disk[0])

	if(get_lv_name_rm not in xyz):
		call_remove_func = san_disk_funs.remove_disk_san(get_lv_name_rm,disk_type)
		print"""<div id = 'id_trace'>"""
		print """Successfully removed  from SAN!"""
		print """</div>"""
	else:
		print"""<div id = 'id_trace_err'>"""
		print 'This disk is used in Iscsi!'
		print '</div>'


	get_radio_rm = ''
	checked_bio_rm = ''
	checked_fio_rm = ''

	display_bio = 'none'
	display_fio = 'none'
	display_cr_con = 'none'
	display_cr_img = 'none'
	display_rm_con = 'none'
	display_rm_img = 'none'
	display_add_san = 'none'
	display_remove_san = 'none'
	display_details = 'block'

vg_info = storage.get_pvs()
get_con = storage.get_lvs(type1='FIO')
san_list = san_disk_funs.list_all_disk_att()

import left_nav
print
print """

 <head>
                <link rel='stylesheet' type='text/css' href='new-tooltip/lptooltip.css' />
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
        </head>


      <!--Right side body content starts from here-->
      <div class="rightsidecontainer">
        <div class="insidepage-heading">Volume Configuration >> <span class="content">FIO Disk Information</span></div>
        <!--tab srt-->
        <div class="searchresult-container">
          <div class="infoheader">
            <div id="tabs">
              <ul>
                <li><a href="#tabs-1">FIO Details</a></li>
                <li><a href="#tabs-2">Create Container</a></li>
                <li><a href="#tabs-3">Create Image</a></li>
                <li><a href="#tabs-4">Remove Container</a></li>
                <li><a href="#tabs-5">Remove Image</a></li>
              </ul>





<div id="tabs-1">
<div class="topinputwrap">"""

if(get_con['lvs']!=[]):
	print """
	<form name = 'disk_to_delete' method = 'POST' action = ''>
	<table width="100%" style="margin:10px 0 0 0; border:#D1D1D1 1px solid;">
	<tr>
	<th style="border:#D1D1D1 1px solid; padding:5px;"><input type = 'checkbox' id = 'id_select_all_img' name = 'select_all_img' onclick = 'return select_iscsi_disks_all_img2();'></th>"""


	print"""<th style="border:#D1D1D1 1px solid; padding:5px;">Volume</th>
	<th style="border:#D1D1D1 1px solid; padding:5px;">Container</th>
	<th style="border:#D1D1D1 1px solid; padding:5px;">Container Size</th>
	<th style="border:#D1D1D1 1px solid; padding:5px;">FIO Image</th>
	</tr>"""
	for i in get_con['lvs']:
		get_images = storage_op.list_size_images(i['lv_name'])
		if(get_images!=[]):
			disabled = 'disabled'
		else:
			disabled = ''

		print """<tr>
		<td align="center" style="padding:5px;"><input id = 'id_disk_array_img' type = 'checkbox' name = 'delete_option_img[]' value = '"""+i['lv_name']+"""' """+disabled+""" /></td>
		<td align="center" style="padding:5px;">"""+i['vg_name']+"""</td>
		
		<td align="center" style="padding:5px;"><a class="various" data-fancybox-type="iframe" style="color:green; font-weight: bold; width:100%;float:right; text-decoration:none; "  href="fio_disk_increase.py?volume="""+i["vg_name"]+"""&disk_name="""+i['lv_name']+"""&size_name="""+i['size']+"""&available_size="""+i["size"]+"""">"""+i["lv_name"]+"""</td>
	 
		<td align="center" style="padding:5px;">"""+i['size'].replace('g', ' GB')+"""</td>
		<td align="center" style="padding:5px;">"""
		if len(get_images) != 0:
			for j in get_images:
				print j['name']+' [ '+j['size'].replace('G', 'GB')+' ]'
				print "<br/>"

		print """</td></tr>"""

	print """</table>"""

	print """<table width="100%" style="margin:20px 0 0 0;"><tr>
	<td>"""


	print """<button class="buttonClass" style="float:right;" type="submit" name = 'delete_container'  id = 'delete_container' value = 'delete_container'  onclick = 'return fio_disk_delete();'>Delete</button>"""

	print"""
	</td>
	</tr>
	</table>
	</form>
	"""

else:
	print"""<div style="text-align:center; margin:20px 0 20px 0;">No Information available!</div>"""



print """</form>


</div>
<p>&nbsp;</p>
</div>



<div id="tabs-2">
<div class="topinputwrap">

<form name = 'create_container' method = 'POST' action = ''>
<table width="80%" style="margin:10px 0 0 100px;">

<tr>
<td>Select Volume</td>
<td>
<div class="styled-select2">
<select class = 'input' name='volume'>
<option value='select-volume'>Select Volume</option>"""
if(vg_info["pvs"]!=[{}]):
	for x in vg_info["pvs"]:
		free_size = x["free_size"]
		free_size = free_size.replace("g", "GB")
		print """<option value='"""+x['vg_name']+"""'>"""+x['vg_name']+' ('+free_size+')'"""</option>"""

print """</select></div>
</td>
</tr>

<tr>
<td>
Enter Container Name</td>
<td><input class = 'textbox' type = 'text' name = 'container_name' id = 'container_name' style="width:187px;"></td>    
</tr>

<tr>
<td>Enter Container Size (GB)</td>
<td><input class = 'textbox' type = 'text' name = 'container_size' onkeypress="return isNumberKey(event)" id = 'container_size' style="width:187px;"></td>    
</tr>

<tr>
<td><input type="checkbox" name="advance_option" id="adv_chk" onclick = 'return nas_advance_config2() ' /> Advance Options</td>
<td></td>    
</tr>

</table>

<table width:100% id="adv_txt1" style="display:none; margin:10px 0 0 100px;">

<tr>
<td>Format Option</td>
<td><input type= "text" class="textbox" name = "adv1" id = "inpt1_adv1" onclick="enable()"/></td>
</tr>

<tr>
<td>Format Option</td>
<td><input type= "text" class="textbox" name= "adv2" id = "inpt2_adv2" onclick="enable()"/></td>
</tr>

</table>

<table width="100%">
<tr>
<td>
<button class="buttonClass" style="float:right; margin:0 200px 20px 0;" type="submit" name = 'create_container'  id = 'create_container' value = 'create_container'  onclick = 'return validate_fio_container();'>Create Container</button>	
</td>
</tr>


</table>
</form>

</div>
<p>&nbsp;</p>
</div>



<div id="tabs-3">
<div class="topinputwrap">

<form name = 'create_image' action = 'main.py?page=bd#tabs-3' method = 'POST'>
<table width="80%" style="margin:10px 0 0 100px;">

<tr>
<td>Select Container</td>
<td>
<div class="styled-select2">
<select name='volume_con' onchange="this.form.submit();">
<option value='select-container'>Select Container</option>"""
for i in get_con['lvs']:
	print """<option value='"""+i['lv_name']+"""'"""
	if(get_vol_chk != ''):
		if(get_vol_chk == i['lv_name']):
			print """selected = selected"""

	print """>"""+i['lv_name']+' ('+i['size'].replace('g', ' GB')+')'"""</option>"""

print """</select></div>
</td>    
</tr>

<tr>
<td>Enter Image Name</td>
<td><input class = 'textbox' type = '' name = 'img_name' id = 'group' style="float:left; width:187px;"></td>    
</tr>

<tr>
<td>Enter Image Size <br/>"""
if(un_use != ''):
	print """<font style="color:#B45F04;">(MAX """+str(un_use)+"""GB available)</font>"""

print """
</td>
<td><input class = 'textbox' type = 'text' name = 'img_size' onkeypress="return isNumberKey(event)" id = 'group' style="float:left; width:187px;"></td>    
</tr>

</table>

<table width="90%">
<tr>
<td>

<button class="buttonClass" style="float:right; margin:10px 165px 0 0;" type="submit" name = 'create_image'  id = 'create_image' value = 'Apply'  onclick = 'return validate_fio_image();'>Create FIO Image</button>

</td>
</tr>

</table>
</form>


</div>
<p>&nbsp;</p>
</div>




<div id="tabs-4">
<div class="topinputwrap">

<form name = 'remove_container' action = 'main.py?page=bd#tabs-4' method = 'POST'>
<table width="100%" style="margin:10px 0 0 20px; text-align:center;">

<tr>
<td>Select Container</td>
<td>
<div class="styled-select2">
<select name='volume'>
<option value='select-volume'>Select Container</option>"""
for i in get_con['lvs']:
	get_images = storage_op.list_size_images(i['lv_name'])
	if(get_images!=[]):
		disabled = 'disabled'
	else:
		disabled = ''

	print """<option value='"""+i['lv_name']+"""' """+disabled+""">"""+i['lv_name']+' ['+i['size'].replace('g', ' GB')+']'""" </option>"""

print """</select></div>
</td>    
</tr>

</table>

<table width="90%">
<tr>
<td>

<button class="buttonClass" type="submit" name = 'remove_container'  id = 'remove_container' value = 'remove_container'  onclick = 'return validate_remove_container();' style="float:right; margin:10px 220px 0 0;">Remove</button>

</td>
</tr>
</table>

</form>

</div>
<p>&nbsp;</p>
</div>



<div id="tabs-5">
<div class="topinputwrap">

<form name = 'remove_image' action = 'main.py?page=bd#tabs-5' method = 'POST'>
<table width="100%" style="margin:10px 0 0 20px; text-align:center;">

<tr>
<td>Select Container</td>
<td>
<div class="styled-select2">
<select name='volume_con_rm' onchange="this.form.submit();">
<option value='select-container'>Select Container</option>"""
for i in get_con['lvs']:
	print """<option value='"""+i['lv_name']+"""'"""
	if(get_vol_chk_2 != ''):
		if(get_vol_chk_2 == i['lv_name']):
			print """selected = selected"""

	print """>"""+i['lv_name']+' ('+i['size'].replace('g', ' GB')+')'"""</option>"""

print """</select></div>
</td>    
</tr>

<tr>
<td>Select FIO Image</td>
<td>"""
if(get_vol_chk_2 != ''):
	get_images2 = storage_op.list_size_images(get_vol_chk_2)
	if len(get_images2) != 0:
		print """<div class="styled-select2"><select name='volume_img_rm'>"""
		for j in get_images2:
			print """<option value='"""+j['name']+"""'>"""+j['name']+' ['+j['size'].replace('G', 'GB')+' ]'"""</option>"""
		print """</select></div>"""

	else:
		print """<input class="textbox" type='text' value='No image found!' disabled=disabled style="float:left; width:187px;" />"""

else:
	print """<input class="textbox" type='text' value='Select container' disabled=disabled style="float:left; width:187px;"/>"""

print """
</td>    
</tr>
</table>

<table width="90%">
<tr>
<td>

<button class="buttonClass" type="submit" name = 'remove_image'  id = 'remove_image' value = 'remove_image'  onclick = 'return validate_remove_image();' style="float:right; margin:10px 210px 0 0;">Remove Image</button>

</td>
</tr>



</table>

</div>
<p>&nbsp;</p>
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

<!-- ####### Sub Tabs Start ####### -->

<script>
$("#tabs, #subtabs").tabs();
$("#tabs, #subsubtabs").tabs();
</script>

<!-- ####### Sub Tabs End ####### -->

"""
