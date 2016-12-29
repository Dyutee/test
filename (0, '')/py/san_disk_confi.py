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
	check_san = isinstance(san_val, str)
	if(check_san == True):
		split_san = string.split(san_val,":")
		remove_san =san_disk_funs.remove_disk_san(split_san[0],split_san[1])
	else:
		san_val = set(san_val)
		for san in san_val:
			split_san = string.split(san,":")
			remove_san = san_disk_funs.remove_disk_san(split_san[0],split_san[1])

	if(remove_san== True):
		print"""<div id = 'id_trace'>"""
		print " Disk <font color='darkred'><b>"+str(san_val)+"</b></font> Successfully Deleted!"
		print "</div>"
	else:
		print"""<div id = 'id_trace_err'>"""
		print "Error occured while deleting Disk <font color = 'darkred'><b>"+str(san_val)+"</b></font> !"
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
	get_hid_vg_name = header.form.getvalue("hid_vg_name")

	if(get_radio == 'bio'):
		get_path = '/dev/'+get_hid_vg_name+'/BIO-'+str(get_lv_name)
		disk_type = 'BIO'
	if(get_radio == 'fio'):
		split_gln = string.split(get_lv_name, ':')
		get_path = '/storage/FIO/'+split_gln[1]+'/'+split_gln[0]
		disk_type = 'FIO'

	call_add_func = san_disk_funs.add_disk_san(get_path,get_san_name,get_san_blocksize,type=disk_type)

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
                        /*'afterClose':function () {
                          window.location.reload();
                         },*/
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
                <li><a href="#tabs-1">SAN Configuration</a></li>
                <li><a href="#tabs-2">Add to SAN</a></li>
              </ul>





<div id="tabs-1">
<div class="topinputwrap">
<form name = 'san_det_list' method = 'POST' action = ''>

"""
if(san_list != []):
	if 'blocksize' in san_list[0].keys():
		print"""
		<table width="100%" style="margin:10px 0 0 0; border:#D1D1D1 1px solid;">
		<tr>
		<th style="border:#D1D1D1 1px solid; padding:5px;"><input type = 'checkbox' id = 'id_select_all_san' name = 'select_all' onclick = 'return select_san_disks_all();'></th>"""

		print"""<th style="border:#D1D1D1 1px solid; padding:5px;">San Name</th>
		<th style="border:#D1D1D1 1px solid; padding:5px;">Disk name</th>
		<th style="border:#D1D1D1 1px solid; padding:5px;">Disk Size (MB)</th>
		<th style="border:#D1D1D1 1px solid; padding:5px;">Block Size (MB)</th>
		</tr>"""

		iscsi_disks_array = [];
		srp_disks_array   = [];
		fc_disks_array    = [];
		if(select_targets!=[{}]):
			for x in select_targets:
				get_target= x['target']
				iscsi_used_disks_list = san_disk_funs.iscsi_used_disks_tgt(get_target)

				if (len(iscsi_used_disks_list) > 0):
					for iscsidisk in iscsi_used_disks_list:
						iscsi_disks_array.append(iscsidisk);

		for y in srp_target:
			get_target= y
			srp_used_disks_list = san_disk_funs.ib_used_disks_tgt(get_target)

			if (len(srp_used_disks_list) > 0):
				for srpdisk in srp_used_disks_list:
					srp_disks_array.append(srpdisk);

		for z in fc_targets:
			get_target= z
			fc_used_disks_list = san_disk_funs.fc_used_disks_tgt(get_target)

			if (len(fc_used_disks_list) > 0):
				for fcdisk in fc_used_disks_list:
					fc_disks_array.append(fcdisk);

		if(san_list!=[]):
			for i in san_list:
				iscsi_disk = i['name'];

				for keys in i:
					if (str(keys) == 'filename'):
						filename = i['filename']

						filename= filename[filename.rfind('-')+1:];
						disable_chk = ""
						star_icon = ""
						used_disks_name = ""

						iscsi_active = '';
						srp_active = '';
						fc_active = '';

						if (iscsi_disk in iscsi_disks_array):
							iscsi_active = 'ISCSI';

						if (iscsi_disk in srp_disks_array):
							srp_active = 'SRP';

						if (iscsi_disk in fc_disks_array):
							fc_active = 'FC';

						string = iscsi_active + '&nbsp;' + srp_active + '&nbsp;' + fc_active;
						string = string.strip();

						if (string == '&nbsp;&nbsp;'):
							string = 'No-Protocols';

						if (iscsi_disk in iscsi_disks_array or iscsi_disk in srp_disks_array or iscsi_disk in fc_disks_array):
							disable_chk = "disabled"
							star_icon = "<font color = 'darkred' size = '3' style='font-family: Georgia;'>*</font>"
						print""" <tr> 
						<td align="center" style="padding:5px;"><input id = 'id_disk_array_san' """+disable_chk+""" type = 'checkbox' name = 'delete_option_san[]' value = '"""+i['name']+':'+i['type']+"""' ></td>

						<td align="center"><a style="margin:0; font-weight:bold; color:#B45F04;" class="various" data-fancybox-type="iframe" style="color:green; font-weight: bold; width:150%;float:right; text-decoration:none; "  href="san_properties.py?thread="""+i['threads_pool_type']+"""&dev_id="""+i['t10_dev_id']+"""&type="""+i['type']+"""&threads="""+i['threads_num']+"""&usn="""+i['usn']+"""&cache= """+i['nv_cache']+"""&thin="""+i['thin_provisioned']+"""">"""+i['name']+''+star_icon+''"""</span></a></td>
						<td align="center">"""+filename+"""</td>
						<td align="center">"""+i['size_mb']+"""</td>
						<td align="center">"""+i['blocksize']+"""</td>
						</tr>"""


		

		print """</table>

		<table width="100%">
		<tr>
		<td>
		<button class="button_example" style="float:right; margin:10px 0 10px 0;" type="submit" name = 'delete_san_but'  id = 'delete_san_but' value = 'delete_san_but'  onclick = 'return san_disk_delete();'>Delete Selected</button>
		</td>
		</tr>


		</table>
		"""

	else:
		print """<div style="text-align:center; margin:20px 0 20px 0;">No Information available!</div>"""

else:
	print """<div style="text-align:center; margin:20px 0 20px 0;">No Information available!</div>"""


print """</form></div>
<p>&nbsp;</p>
</div>


<div id="tabs-2">
<div class="topinputwrap">

<form name = 'add_group' method = 'POST' action="main.py?page=san#tabs-2">
<table width="80%" style="margin:10px 0 0 100px;">

<tr>
<td>Select Disk</td>
<td>
<input type='radio' name='select_disk' id="bio_chk" value='bio' onclick='this.form.submit()' """+checked_bio+""">BIO 
<input type='radio' name='select_disk' id="fio_chk" value='fio' onclick='this.form.submit()' """+checked_fio+""">FIO
</td>    
</tr>

<tr>
<td>Select a volume to Add</td>
<td>"""
if(get_radio != ''):
	print """<div class="styled-select2"><select name='select_lv' >"""
	if(get_radio == 'bio'):
		for x in call_func['lvs']:
			print """<option value = '"""+x['lv_name']+"""'>"""+x['lv_name']+"""</option>"""
			print """<input type="hidden" name="hid_vg_name" value='"""+x['vg_name']+"""' />"""
	else:
		for x in call_func['lvs']:
				get_images = storage_op.list_size_images(x['lv_name'])
				for y in get_images:
					print """<option value = '"""+y['name']+':'+x['lv_name']+"""'>"""+y['name']+"""</option>"""
					print """<input type="hidden" name="hid_vg_name" value='"""+x['vg_name']+"""' />"""
	print """</select></div>"""
else:
	print """ <input type='text' class = 'textbox' value='Select a disk' disabled=disabled style="width:187px;">"""

print """
</td>    
</tr>

<tr>
<td>Enter Name</td>
<td><input class = 'textbox' type = 'text' name = 'san_name' id = 'san_name' style="width:187px;"></td>    
</tr>

<tr>
<td align = 'right' colspan = '2'>
<tr>
<td>Block Size</td>
<td>
<div class="styled-select2">
<select name='select_block'>
<option value='option_block'>Select Size</option>
<option>512</option>
<option>4096</option>
</select>
</div>
</td>    
</tr>


<tr>
<td align = 'right' colspan = '2'>

<button class="button_example" style="float:right; margin:20px 170px 20px 0;" type="submit" name = 'add_to_san'  id = 'add_to_san' value = 'add_to_san'  onclick = 'return validate_san_configuration();'>Add to SAN</button>
</td>
</tr>

</table>
</form>



</div>
<p>&nbsp;</p>
</div>


<div id="tabs-3">
<div class="topinputwrap">

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
