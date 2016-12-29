#!/usr/bin/python
import cgitb, sys, common_methods, os, commands, cgi, include_files
cgitb.enable()


#-------------Import modules name and Volume Size--------------------------------
sys.path.append('/var/nasexe/storage/')
import storage_op
from lvm_infos import *
from functions import *
vg_info = get_vgs()
form = cgi.FieldStorage()
free_vg = ''
if(vg_info["vgs"] != [{}]):
	for free_vg in vg_info["vgs"]:
		free_vg = free_vg["free_size"]
#-----------------------End--------------------------

select_opt_min_single = range(1, 60)
select_opt_min = range(1, 60)
select_opt_hour_single = range(1, 24)
select_opt_hour = range(1, 24)
select_opt_day = range(0, 7)
select_opt_day_month = range(1, 32)
select_opt_month = range(1, 13)

#--------------------------Empty value for a variable------------------
minute_chk_val = ''
hour_chk_val = ''
day_chk_val = ''
month_chk_val = ''
day_month_chk_val = ''

select_min_val = ''
select_hour_val = ''
select_day_val = ''
select_day_month_val = ''
select_month_val = ''

per_min_val = ''
per_hour_val = ''
per_day_val = ''
per_day_month_val = ''
per_month_val = ''
display_min = 'none'
display_hour = 'none'
display_day = 'none'
display_day_month = 'none'
display_month='none'
display_min1 = 'block'
display_hour1 = 'block'
display_day1 = 'block'
display_day_month1 = 'block'
display_month1='block'
get_file_name = ''
#--------------------------------------End------------------------------------
#---------------------------------import modules--------------------------------------
sys.path.append('/var/nasexe/python/tools/')
#import launcher
import snapshotschedule
#--------------------------------------End---------------------------------------------
#status=launcher.get(user='user')
#for script in status['launcher_scripts']:
#        print 

#---------------------------End-----------------------
#--------------- Get File Path------------------------------
files_path = '/var/nasexe/python/launcher_scripts/usr'

get_all_files_list = os.listdir(files_path)
#---------------------End------------------------------------
#print get_all_files_list

#---------------First Step------------------------------------ 

if(form.getvalue("submit_snap")):
	get_disk_name = form.getvalue("disk_name")
	get_snap_name = form.getvalue("snap_name")
	get_max_snap = form.getvalue("max_snap")
	get_snap_size = form.getvalue("snap_size")
	minute_chk = form.getvalue("min_check")
	hour_chk = form.getvalue("hour_check")
	day_month_chk = form.getvalue("day_month_check")
	month_chk = form.getvalue("month_check")
	day_chk = form.getvalue("day_check")

	if(minute_chk == 'on'):
		minute_chk_val = 'checked'
		select_min_val = form.getvalue("select_min1")
		minute_chk = "*"
	else:
		minute_chk = ""
		select_min_val= form.getvalue("select_min")


	if(hour_chk == 'on'):
		hour_chk_val = 'checked'
		select_hour_val = form.getvalue("select_hour1")
		hour_chk = "*"
	else:
		hour_chk = ""
		select_hour_val = form.getvalue("select_hour")

	if(day_month_chk == 'on'):
		day_month_chk_val = 'checked'
		select_day_month_val = form.getvalue("select_day_month1")
		day_month_chk = "*"
	else:
		day_month_chk =""
		select_day_month_val = form.getvalue("select_day_month")

	if(month_chk == 'on'):
		month_chk_val = 'checked'
		select_month_val = form.getvalue("select_month1")
		month_chk = "*"
	else:
		month_chk = ""
		select_month_val = form.getvalue("select_month")

	if(day_chk == 'on'):
		day_chk_val = 'checked'
		select_day_val = form.getvalue("select_day1")
		day_chk = "*"
	else:
		day_chk = ""
		select_day_val = form.getvalue("select_day")


#-----------------End----------------------------------------------------------
#--------------------------Second Step--------------------------------------------		
	if(minute_chk_val == 'checked' and select_min_val !=''):
		per_min_val ="*"+'/'+str(select_min_val)
		minute_chk = "checked"
		display_min = 'block'
		display_min1 = 'none'
		#print per_min_val
	else:
		minute_chk = ""
		per_min_val = select_min_val
		display_min = 'none'
		display_min1 = 'block'


	if(hour_chk_val == 'checked' and select_hour_val !=''):
		per_hour_val = "*"+'/'+str(select_hour_val)
		hour_chk = "checked"
		display_hour = 'block'
		display_hour1 = 'none'
		
	else:
		hour_chk = ""
		per_hour_val = select_hour_val
		display_hour = 'none'
		display_hour1 = 'block'

	if(day_chk_val == 'checked' and select_day_val !=''):
                per_day_val = "*"+'/'+str(select_day_val)
		day_chk = "checked"
		display_day = 'block'
		display_day1 = 'none'
        else:
		day_chk = ""
                per_day_val = select_day_val
		display_day = 'none'
		display_day1 = 'block'

	if(day_month_chk_val == 'checked' and select_day_month_val !=''):
                per_day_month_val = "*"+'/'+str(select_day_month_val)
		day_month_chk = "checked"
		display_day_month = 'block'
		display_day_month1 = 'none'
        else:
		day_month_chk = ""
                per_day_month_val = select_day_month_val
		display_day_month = 'none'
		display_day_month1 = 'block'

	if(month_chk_val == 'checked' and select_month_val !=''):
                per_month_val = "*"+'/'+str(select_month_val)
		month_chk = "checked"
		display_month='block'
		display_month1='none'
        else:
		month_chk =""
                per_month_val = select_month_val
		display_month1='block'
		display_month='none'
#---------------------------------------------End------------------------------------------------	
	
	#all_snap = str(minute_chk)+str(hour_chk)+str(day_chk)+str(day_month_chk)+str(month_chk)
	#print 'Checked_value:'+ all_snap
	#-------------------Replace all Value with [ and single quote("'")-------------------
	per_min_val = str(per_min_val).replace("[", '')
	per_min_val = str(per_min_val).replace("]", '')
	per_min_val = str(per_min_val).replace("'", '')
	per_min_val = str(per_min_val).replace(" ", "")

	per_hour_val = str(per_hour_val).replace("[", '')
	per_hour_val = str(per_hour_val).replace("]", '')
	per_hour_val = str(per_hour_val).replace("'", '')
	per_hour_val = str(per_hour_val).replace(" ", "")

	per_day_val = str(per_day_val).replace("[", '')
	per_day_val = str(per_day_val).replace("]", '')
	per_day_val = str(per_day_val).replace("'", '')
	per_day_val = str(per_day_val).replace(" ", "")

	per_day_month_val = str(per_day_month_val).replace("[", '')
	per_day_month_val = str(per_day_month_val).replace("]", '')
	per_day_month_val = str(per_day_month_val).replace("'", '')
	per_day_month_val = str(per_day_month_val).replace(" ", "")

	per_month_val = str(per_month_val).replace("[", '')
	per_month_val = str(per_month_val).replace("]", '')
	per_month_val = str(per_month_val).replace("'", '')
	per_month_val = str(per_month_val).replace(" ", "")
	
	#-------------------------------End--------------------------------------------------
	#-----------------------Both Checkbox and Select box blank------------------------------------------
	if(per_min_val == 'None'):
		per_min_val = "*"
		minute_chk_val = 'checked'


	if(per_hour_val == 'None'):
		per_hour_val = "*"
		hour_chk_val = 'checked'

	if(per_day_val == 'None'):
		per_day_val = "*"
		day_chk_val = 'checked'

	if(per_day_month_val == 'None'):
		per_day_month_val = "*"
		day_month_chk_val = 'checked'
		
		
	if(per_month_val == 'None'):
		per_month_val = "*"
		month_chk_val = 'checked'


	#-----------------------------End----------------------------------------------------
	#New_val = str(per_min_val)

	New_val = str(per_min_val)+' '+str(per_hour_val)+' '+str(per_day_month_val)+' '+str(per_month_val)+' '+str(per_day_val)
	
	if "/*" in str(New_val):
		New_val= New_val.replace("/*", '')
	
	#snapshot_status=launcher.ingest(get_file_name,New_val,'usr')
	#print 'STATUS:'+str(snapshot_status)
	#print '<br/>'
	snapshot_status = snapshotschedule.create_snap_rotate_script(get_disk_name,get_max_snap,get_snap_size,get_snap_name,New_val)
	if(snapshot_status == True):
		#print "<script>location.href = 'main.py?page=ss&action=snap_value#tabs-3';</script>"
		print "<script>location.href = 'iframe_snapshot_page.py?action=snap_value#tabs-3';</script>"
		#print


		
        	#print"""<div id = 'id_trace'>"""
                #print "Successfully Schedule the Snapshot!"
                #print "</div>"
       	#else:
        #       	print"""<div id = 'id_trace_err'>"""
        #        print "Error occured while Scheduling Snapshot!"
        #      	print "</div>"
#----------------------------------Remove Snapshot-----------------------------
#if(form.getvalue("remove_snap")):
#	get_disk_name = header.form.getvalue("disk_name")
#	get_time = header.form.getvalue("time_val")
#	print get_time
	
#	remove_status=snapshotschedule.remove_snap_rotate_script(get_disk_name,get_time,debug=True)
	
#	if(remove_status == True):
#		print "<script>location.href = 'main.py?page=ss&&rem_action=rem_value#tabs-3';</script>"
	
	

	#print get_file_name 

#-----------------------------------End-----------------------------
#----------------------------Set value----------------------------------
if(form.getvalue("disk_name")):
	set_disk_value = form.getvalue("disk_name")
	disk_set_value = snapshotschedule.get(set_disk_value,debug=True)
	#print disk_set_value
	

#----------------------------End---------------------------------------


sys.path.append("/var/nasexe/storage/")
import snapshot
import lvm_infos
get_snapshots = lvm_infos.get_lvs(type1='SNP')
get_nas_lvs = lvm_infos.get_lvs()
get_bio_lvs = lvm_infos.get_lvs(type1='BIO')
array_len = len(get_snapshots["lvs"])

#------------------Snapshot time Import-------------
sys.path.append('/var/nasexe/python/')
import smb, commons

from tools import sync
snap_time=sync.get_time()
#------------------------End------------------------


print
print """
		
 <form name='form1' method='post' action='snap_nw_page1.py'>
		
	<table style="width:500px;">

	
	 <tr>
	<td>Disk name</td>
	<td>
	<div class="styled-select2">
	<select name="disk_name">
	<option value = 'disk_val'>Select a disk name</option>"""
if(get_nas_lvs["lvs"] != [{}]):
	for n in get_nas_lvs["lvs"]:
		print """<option value='NAS-"""+n['lv_name']+"""'>NAS-"""+n['lv_name']+"""</option>"""

if(get_bio_lvs["lvs"] != [{}]):
	for b in get_bio_lvs["lvs"]:
		print """<option value='BIO"""+b['lv_name']+"""'>BIO"""+b['lv_name']+"""</option>"""

print """</select></div>
	</tr>

	 <tr>
	<td>Snapshot name</td>
	<td><input type="text" name="snap_name" class = 'textbox' value = "" style="width:188px;" /></td>
	</tr>

	<tr>
	<td>Max no. of snapshots</td>
	<td><input type="text" name="max_snap" onkeypress="return isNumberKey(event)" class = 'textbox' value = "" style="width:188px;" /></td>
	</tr>
	<tr>
	<td>Snapshot size (GB)</td>
	<td><input type="text" name="snap_size"  value = "" onkeypress="return isNumberKey(event)" class = 'textbox' style="width:188px;" /></td>
	 <input type ="hidden" name = "free_vol" value = '"""+free_vg+"""'>
	 <input type ="hidden" name = "time_val" value = '"""+snap_time+"""'>
	</tr>
	</table>
		<br/>
    	            <table  width = "600" bgcolor="#f5f5f5" border = "0"  cellspacing = "0" cellpadding = "0" class = 'outer_border'>
		<tr>

			<th style="border:#D1D1D1 1px solid; padding:5px;"> Minute</th>
			<th style="border:#D1D1D1 1px solid; padding:5px;"> Hour</th>
			<th style="border:#D1D1D1 1px solid; padding:5px;"> Day of Month</th>
			<th style="border:#D1D1D1 1px solid; padding:5px;"> Month</th>
			<th style="border:#D1D1D1 1px solid; padding:5px;"> Days</th>
		</tr>
		<tr>
			<td style="border:#D1D1D1 1px solid; padding:5px;"><input type = "checkbox" name = "min_check" """+minute_chk_val+""" id="chk" style="margin-left: 44%;" onclick = 'return snap_select_hide();'></td>
			<td style="border:#D1D1D1 1px solid; padding:5px;"><input type = "checkbox" name = "hour_check" """+hour_chk_val+""" id="chk1" style="margin-left: 44%;" onclick = 'return snap_select_hide1();'></td>
			<td style="border:#D1D1D1 1px solid; padding:5px;"><input type = "checkbox" name = "day_month_check" id="chk2" """+day_month_chk_val+""" style="margin-left: 44%;" onclick = 'return snap_select_hide2();'></td>
			<td style="border:#D1D1D1 1px solid; padding:5px;"><input type = "checkbox" name = "month_check" id="chk3" """+month_chk_val+""" style="margin-left: 44%;" onclick = 'return snap_select_hide3();'></td>

			<td style="border:#D1D1D1 1px solid; padding:5px;"><input type = "checkbox" name = "day_check" id="chk4" """+day_chk_val+""" style="margin-left: 44%;" onclick = 'return snap_select_hide4();'></td>
		</tr>
		<tr>
			<td style="border:#D1D1D1 1px solid; padding:5px;">
			<select style="margin-left: 34%;width: 54%;display:"""+display_min1+"""" id ="select_id1" name = "select_min" multiple>
			<option></option>"""
for min_num in select_opt_min:
	print""" <option value= '"""+str(min_num)+"""'"""
	
	if((select_min_val !='') and (select_min_val != None)):
		for min_list in select_min_val:
		
			if(min_list == str(min_num)):
				print """selected = 'selected'"""

	print""">"""+str(min_num)+"""</option>"""
print"""
			</select>

 <select style="margin-left: 34%;width: 54%;display:"""+display_min+""";" id ="select_id6" name = "select_min1" >
                        <option>*</option>"""
for min_num in select_opt_min_single:
        print""" <option value= '"""+str(min_num)+"""'"""
        
        if(select_min_val !=''):
                if(select_min_val == str(min_num)):
                        print """selected = 'selected'"""

        print""">"""+str(min_num)+"""</option>"""
print"""
                        </select>


			
			</td>


			<td style="border:#D1D1D1 1px solid; padding:5px;">
			<select style="margin-left: 34%;width: 54%;display:"""+display_hour1+""";" id ="select_id2" name = "select_hour" multiple>
			<option></option>"""
for hour_num in select_opt_hour:
	print""" <option value = '"""+str(hour_num)+"""'"""
	if((select_hour_val !='') and (select_hour_val != None)):
		for hour_list in select_hour_val:
			if(hour_list == str(hour_num)):
				print """selected = 'selected'"""


	print""">"""+str(hour_num)+"""</option>"""
print"""
			</select>

 <select style="margin-left: 34%;width: 54%;display:"""+display_hour+""";" id ="select_id7" name = "select_hour1" >
                        <option>*</option>"""
for hour_num in select_opt_hour_single:
        print""" <option value = '"""+str(hour_num)+"""'"""
        if(select_hour_val !=''):
                if(select_hour_val == str(hour_num)):
                        print """selected = 'selected'"""


        print""">"""+str(hour_num)+"""</option>"""
print"""
                        </select>


			</td>



			<td style="border:#D1D1D1 1px solid; padding:5px;">
			<select style="margin-left: 34%; width:32%;display:"""+display_day_month1+""";" id ="select_id3" name = "select_day_month" multiple>
			<option></option>"""
for day_month_num in select_opt_day_month:
	print""" <option value = '"""+str(day_month_num)+"""'"""
	if((select_day_month_val !='') and (select_day_month_val != None)):
		for day_month_list in select_day_month_val:
			if(day_month_list == str(day_month_num)):
				print"""selected = 'selected'"""

	print""">"""+str(day_month_num)+"""</option>"""
print"""
			</select>

<select style="margin-left: 34%; width:32%;display:"""+display_day_month+""";" id ="select_id8" name = "select_day_month1" >
                        <option>*</option>"""
for day_month_num in select_opt_day_month:
        print""" <option value = '"""+str(day_month_num)+"""'"""
        if(select_day_month_val !=''):
                if(select_day_month_val == str(day_month_num)):
                        print"""selected = 'selected'"""

        print""">"""+str(day_month_num)+"""</option>"""
print"""
                        </select>
			</td>


			<td style="border:#D1D1D1 1px solid; padding:5px;">
			<select style="margin-left: 34%; width: 54%;display:"""+display_month1+""";" id ="select_id4" name= "select_month" multiple>
			<option></option>"""
for month_num in select_opt_month:
	print""" <option value = '"""+str(month_num)+"""'"""

	if((select_month_val !='') and (select_month_val != None)):
		for month_list in select_month_val:
			if(month_list == str(month_num)):
				print"""selected ='selected'"""

	print""">"""+str(month_num)+"""</option>"""
print"""
			</select>

 <select style="margin-left: 34%; width: 54%;display:"""+display_month+""";" id ="select_id9" name= "select_month1">
                        <option>*</option>"""
for month_num in select_opt_month:
        print""" <option value = '"""+str(month_num)+"""'"""

        if(select_month_val !=''):
                if(select_month_val == str(month_num)):
                        print"""selected ='selected'"""

        print""">"""+str(month_num)+"""</option>"""
print"""
                        </select>


			</td>


			<td style="border:#D1D1D1 1px solid; padding:5px;">
			<select style="margin-left: 34%; width:66%;display:"""+display_day1+"""" id ="select_id5" name = "select_day" multiple>
			<option></option>"""
for day_num in select_opt_day:
	print""" <option value = '"""+str(day_num)+"""'"""
	if((select_day_val !='') and (select_day_val != None)):
		for day_list in select_day_val:
			if(day_list == str(day_num)):
				print"""selected = 'selected'"""


	print""">"""+str(day_num)+"""</option>"""
print"""
			</select>

<select style="margin-left: 34%; width:66%;display:"""+display_day+""";" id ="select_id10" name = "select_day1" >
                        <option>*</option>"""
for day_num in select_opt_day:
        print""" <option value = '"""+str(day_num)+"""'"""
        if(select_day_val !=''):
                if(select_day_val == str(day_num)):
                        print"""selected = 'selected'"""


        print""">"""+str(day_num)+"""</option>"""
print"""
                        </select>


			</td>
		</tr>


                </table>
<div style="float:right;margin-right:-276%;">
	
         <button class="buttonClass" type="submit" name = 'submit_snap' value = 'snap_val' onclick = 'return validate_snapshot_schedule();'>Schedule</button>
</div>

<!--<div style="float:right;margin-right:-335%;">
        
         <button class="buttonClass" type="submit" name = 'remove_snap' value = 'snap_rem' onclick = 'return validate_snapshot_schedule_rem();'>Remove</button>
</div>-->


        </form>
"""
