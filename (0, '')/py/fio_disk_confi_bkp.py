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


	check_file = os.path.isfile('/storage/'+get_con_rm+'/'+get_img_rm)

	if(check_file==True):
		rm_image = commands.getstatusoutput('sudo rm -rf /storage/'+get_con_rm+'/'+get_img_rm)

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
        <div class="insidepage-heading">Volume Configuration >> <span class="content">Block Disk Information</span></div>
        <!--tab srt-->
        <div class="searchresult-container">
          <div class="infoheader">
            <div id="tabs">
              <ul>
                <li><a href="#tabs-1">Block Disk</a></li>
                <li><a href="#tabs-2">Fio Disk</a></li>
                <li><a href="#tabs-3">San Disk</a></li>
              </ul>
	      <div id="tabs-1">
        <!--form container starts here-->
        <div class="form-container">
          <div class="topinputwrap-heading">Bio Disk Information </div>
          <div class="inputwrap">
	 <div class="formleftside-content">
	<form name = 'disk_to_delete' method = 'POST' action = ''>
	
	<table  width = "150" border = "1"  cellspacing = "1" cellpadding = "1" style="border-style: ridge;">
                <tr>
                        <th class="border"><font color="#7F0101" style="font-family: sans-serif;">Volume</font></th>
                        <th class="border"><font color="#7F0101" style="font-family: sans-serif;">Size</font></th>
                </tr>"""

if(vg_info["pvs"]!=[{}]):

	for x in vg_info["pvs"]:
		#print x
		free_size = x["free_size"]
		free_size = free_size.replace("g", "GB")

		print """<tr>
                        <td align= "center">
                        <a class="various" data-fancybox-type="iframe" style="color:#666666;text-decoration:none;font-weight:bold;" href="block_configuration.py?volume="""+x["vg_name"]+"""&free_size="""+free_size+"""">"""+x["vg_name"]+"""</a></td>
                        <td class="border" align='center' style="font-weight:bold;">"""+free_size+"""</td>
                        </tr>"""	



print"""</table>"""
print"""<table width = "455" border = "1"  align="center" cellspacing = "1" cellpadding = "1" style="margin-left: 91%;border-style: ridge;">"""
get_bio_lvs = storage.get_lvs(type1='BIO')
		#print get_bio_lvs
if(get_bio_lvs["lvs"]!=[]):

	print"""<tr><th class="border" align='center'><input type = 'checkbox' id = 'id_select_all' name = 'select_all' onclick = 'return select_iscsi_disks_all();'></th>"""
else:
	print"""<th class="border" align='center'><input type = 'checkbox' id = 'id_select_all' name = 'select_all' disabled onclick = 'return select_iscsi_disks_all();'></th>"""
print"""<th class="border" align='center'><font color="#7F0101">Volume</font></th>
		<th class="border" align='center'><font color="#7F0101">Disk</font></th>
		<th class="border" align='center'><font color="#7F0101">Size</font></th>
	</tr>"""



get_bio_lvs = storage.get_lvs(type1='BIO')
#print get_bio_lvs
if(get_bio_lvs["lvs"]!=[]):

	i = 1
	for z in get_bio_lvs["lvs"]:
		lv= z["lv_name"]
		new_size= z["size"]
		size = new_size.replace("g", "GB")

		#############################################
		####### Check Block Disk is used or not #######      
		#############################################
		#lib_path = '/storage/VTL/'+y['lv_name']
		disable_chk = ""
		star_icon = ""
		filename = ""

		for i in san_list:
			for keys in i:
				if (str(keys) == 'filename'):
					filename = i['filename']
					filename = filename[filename.rfind('-')+1:];

			if(filename == z["lv_name"]):
				disable_chk = "disabled"
				star_icon = "<font color = 'darkred' size = '3' style='font-family: Georgia;'>*</font>"


		print"""
                        <tr> 
                        <th class="border" align='center'><input id = 'id_disk_array' """+disable_chk+""" type = 'checkbox' name = 'delete_option[]' value = '"""+z["lv_name"]+"""' ></th>
                        <th class="border" align='center'>"""+z["vg_name"]+""" </th>
                        <!--<th class="border" align='center'></th>
                        <th class="border" align='center'><img src = '../images/active.png' /></th>-->
                        <th class="border" align='center'><a class="various" data-fancybox-type="iframe" style="color:green; font-weight: bold; width:100%;float:right; text-decoration:none; "  href="block_disk_increase.py?volume="""+z["vg_name"]+"""&disk_name="""+z['lv_name']+"""&size_name="""+size+"""&available_size="""+x["free_size"]+"""">"""
		if(z["vg_name"]==x["vg_name"]):
			disk_name = z["lv_name"];
			print z["lv_name"]+star_icon
		print"""</th>
		<th class="border" align='center'>"""+size+"""</th>
                        </tr>"""
else:
	print"""
	<tr>
	<td colspan = '4' align = 'center' height="50px;">
	<marquee behavior="alternate" direction= "right"><b><font size="5">No Information is available</font></b></marquee>
	</td>
	</tr>"""
print"""</table>"""

if(get_bio_lvs["lvs"]!=[]):
	print"""<div style="margin-left: 331%;">

<button class="button_example" type="submit" name = 'delete_but' value = 'Delete selected' onclick = 'return bio_disk_delete();'>Delete</button>
</div>"""

else:
	print"""<div style="margin-left: 331%;">
<!--<span id="button-one"><button type = 'submit' name = 'delete_but' disabled title ="Delete Nas"value = 'Delete selected' onclick = 'return bio_disk_delete();' style = 'background-color:#ffffff; border:none; float: right;font-size: 100%;' title="signin"><a style="font-size:85%;  width: 100%;">Delete seleted</a></button></span>-->
<button class="button_example" type="submit" disabled name = 'delete_but' value = 'Delete selected' onclick = 'return bio_disk_delete();'>Delete</button>

</div>"""



print"""</form>"""


print"""

	</div>
          </div>
        </div>
        <!--form container ends here-->
	<p>&nbsp;</p>
              </div>

              <div id="tabs-2">


		 <div id="subtabs">

                  <ul>

                    <li><a href="#subtabs-1">Create Fio</a></li>

                    <li><a href="#subtabs-2">Fio Image</a></li>

                    <li><a href="#subtabs-3">Remove Fio</a></li>
                    <li><a href="#subtabs-4">Remove Image</a></li>
                    <li><a href="#subtabs-5">Fio Details</a></li>

                  </ul>
		 <div id="subtabs-1">
                        <div>

		Create Fio

			</div>

	</div>
		 <div id="subtabs-2">
                        <div>

                Create Fio Image

                        </div>
                  </div>


  <div id="subtabs-3">
                        <div>

                Remove Fio 

                        </div>
                  </div>

  <div id="subtabs-4">
                        <div>

                Remove Image

                        </div>
                  </div>

  <div id="subtabs-5">
                        <div>

                 Fio Details

                        </div>
                  </div>
	

</div>

	<!--form container starts here-->
        <!--form container ends here-->
	<p>&nbsp;</p>
              </div>
                      <div id="tabs-3">
		<div id="subtabs">

                  <ul>

                    <li><a href="#subtabs-1">Add San</a></li>

                    <li><a href="#subtabs-2">Remove San</a></li>
                    <li><a href="#subtabs-3">San Details</a></li>

                  </ul>
		<div id="subtabs-1">
                        <div>

                San create

                        </div>

        </div>

	<div id="subtabs-2">
                        <div>

                San Remove

                        </div>

        </div>

<div id="subtabs-3">
                        <div>

                San Details

                        </div>

        </div>

        	</div>
	 <!--form container ends here-->
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
