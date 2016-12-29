#!/usr/bin/python
import cgitb, header, sys, common_methods
cgitb.enable()


select_opt_min = range(0, 60)
select_opt_hour = range(0, 24)
select_opt_day = range(0, 7)
select_opt_day_month = range(0, 32)
select_opt_month = range(1, 13)

#--------------------------Snapshot------------------
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
if(header.form.getvalue("submit_snap")):
	minute_chk = header.form.getvalue("min_check")
	select_value = header.form.getvalue("select_min1")
	multi_select_value = header.form.getvalue("select_min")

	print minute_chk
	print "<br/>"
	print select_value
	print "<br/>"
	print multi_select_value
	print "<br/>"

	exit()

	if(minute_chk == 'on' and select_value == "*"):
		select_min_val = select_value 
		minute_chk = "*"

	elif((minute_chk == None) and (multi_select_value == None)):
		minute_chk_val = 'checked'
		minute_chk = "*"
		select_min_val = ''

	elif((minute_chk == None) and (multi_select_value != None)):
		minute_chk_val = 'checked'
		minute_chk = ""
		select_min_val = header.form.getvalue("select_min")


	if(minute_chk_val == 'checked' and select_min_val != ''):
		per_min_val ="*"+'/'+str(select_min_val)
	#	minute_chk = "checked"
		display_min = 'block'
		display_min1 = 'none'
		#print per_min_val
#
	elif(minute_chk_val == 'checked' and select_min_val == ''):
		per_min_val ="*"
		display_min = 'block'
                display_min1 = 'none'

	elif(minute_chk_val == '' and select_min_val == ''):
		per_min_val ="*"
                display_min = 'block'
                display_min1 = 'none'

	print per_min_val
	exit()
		
	#else:
	#	minute_chk = ""
	#	per_min_val = select_min_val
	#	display_min = 'none'
	#	display_min1 = 'block'
	
	#else:
	#	minute_chk = ""
	#	select_min_val= header.form.getvalue("select_min")
		#print 'LIS:' +str(select_min_val) 



	hour_chk = header.form.getvalue("hour_check")
	if(hour_chk == 'on'):
		hour_chk_val = 'checked'
		select_hour_val = header.form.getvalue("select_hour1")
		hour_chk = "*"
	else:
		hour_chk = ""
		select_hour_val = header.form.getvalue("select_hour")

	
	day_month_chk = header.form.getvalue("day_month_check")

	if(day_month_chk == 'on'):
		day_month_chk_val = 'checked'
		select_day_month_val = header.form.getvalue("select_day_month1")
		day_month_chk = "*"
	else:
		day_month_chk =""
		select_day_month_val = header.form.getvalue("select_day_month")

	month_chk = header.form.getvalue("month_check")
	if(month_chk == 'on'):
		month_chk_val = 'checked'
		select_month_val = header.form.getvalue("select_month1")
		month_chk = "*"
	else:
		month_chk = ""
		select_month_val = header.form.getvalue("select_month")


	day_chk = header.form.getvalue("day_check")

	if(day_chk == 'on'):
		day_chk_val = 'checked'
		select_day_val = header.form.getvalue("select_day1")
		day_chk = "*"
	else:
		day_chk = ""
		select_day_val = header.form.getvalue("select_day")
	#select_min_val = header.form.getvalue("select_min")
	#print 'MIN1'+str(select_min_val)
	#select_hour_val = header.form.getvalue("select_hour")
	#select_day_val = header.form.getvalue("select_day")
	#select_day_month_val = header.form.getvalue("select_day_month")
	#select_month_val = header.form.getvalue("select_month")

	#if (isinstance(select_min_val, str) == True):
	#	select_min_val =[select_min_val]
		#print 'list chk:'+str(select_min_val)

	print "<br/>"
	print "<br/>"
		
	#if(minute_chk_val == None and select_min_val ==''):
	#	select_min_val = "*"
	#	display_min = 'block'
         #       display_min1 = 'none'
		

	#elif(minute_chk_val == None and select_min_val !=''):
	#	per_min_val = select_min_val
	#	minute_chk = ""
	#	display_min = 'none'
	#	display_min1 = 'block'

	
	#elif(minute_chk_val == None and select_min_val ==''):
	#	per_min_val = select_min_val
	#	minute_chk = "checked"
	#	display_min = 'none'
	#	display_min1 = 'block'

	if(hour_chk_val == 'checked' and select_hour_val !=''):
		per_hour_val = "*"+'/'+str(select_hour_val)
		hour_chk = "checked"
		display_hour = 'block'
		display_hour1 = 'none'
		
		#print per_hour_val
	else:
		hour_chk = ""
		per_hour_val = select_hour_val
		display_hour = 'none'
		display_hour1 = 'block'
		#print per_hour_val
	#if (isinstance(select_day_val, str) == True):
	#	select_day_val =[select_day_val]

	if(day_chk_val == 'checked' and select_day_val !=''):
                per_day_val = "*"+'/'+str(select_day_val)
		day_chk = "checked"
		display_day = 'block'
		display_day1 = 'none'
                #print per_day_val
        else:
		day_chk = ""
                per_day_val = select_day_val
		display_day = 'none'
		display_day1 = 'block'
                #print per_day_val

	#if (isinstance(select_day_month_val, str) == True):
	#	select_day_month_val =[select_day_month_val]

	if(day_month_chk_val == 'checked' and select_day_month_val !=''):
                per_day_month_val = "*"+'/'+str(select_day_month_val)
		day_month_chk = "checked"
		display_day_month = 'block'
		display_day_month1 = 'none'
                #print per_day_month_val
        else:
		day_month_chk = ""
                per_day_month_val = select_day_month_val
		display_day_month = 'none'
		display_day_month1 = 'block'
                #print per_day_month_val

	
	#if (isinstance(select_month_val, str) == True):
	#	select_month_val =[select_month_val]
	if(month_chk_val == 'checked' and select_month_val !=''):
                per_month_val = "*"+'/'+str(select_month_val)
		month_chk = "checked"
                #print per_month_val
		display_month='block'
		display_month1='none'
        else:
		month_chk =""
                per_month_val = select_month_val
                #print per_month_val
		display_month1='block'
		display_month='none'
	
	
	#all_snap = str(minute_chk)+str(hour_chk)+str(day_chk)+str(day_month_chk)+str(month_chk)
	#print 'Checked_value:'+ all_snap
	print '<br/>'
	per_min_val = str(per_min_val).replace("[", '')
	per_min_val = str(per_min_val).replace("]", '')
	per_hour_val = str(per_hour_val).replace("[", '')
	per_hour_val = str(per_hour_val).replace("]", '')
	per_day_val = str(per_day_val).replace("[", '')
	per_day_val = str(per_day_val).replace("]", '')
	per_day_month_val = str(per_day_month_val).replace("[", '')
	per_day_month_val = str(per_day_month_val).replace("]", '')
	per_month_val = str(per_month_val).replace("[", '')
	per_month_val = str(per_month_val).replace("]", '')
	
	New_val = str(per_min_val)+str(per_hour_val)+str(per_day_month_val)+str(per_month_val)+str(per_day_val)
	

	if "/*" in str(New_val):
		New_val= New_val.replace("/*", '')

	
	print 'NEW:'+str(New_val)

	all_per_value = str(per_min_val)+str(per_hour_val)+str(per_day_month_val)+str(per_month_val)+str(per_day_val)
	#print 'All Value:'+ str(all_per_value)
	
	#display_min1 = 'block'
	#display_hour1 = 'block'
	#display_day1 = 'block'
	#display_day_month1 = 'block'
	#display_month1='block'

	print '<br/>'
	if(str(all_per_value) == "*****"):
		month_chk_val = 'checked'
		day_month_chk_val ='checked'
		day_chk_val = 'checked'
		hour_chk_val = 'checked'
		minute_chk_val = 'checked'
	if "/*" in str(all_per_value):
		all_per_value= all_per_value.replace("/*", '')



import left_nav
print
print """
 <!--Right side body content starts from here-->
              <div class="rightsidecontainer">
                <div class="insidepage-heading">Maintenance >> <span class="content">Snap</span></div>
                <!--tab srt-->
                <div class="searchresult-container">
                  <div class="infoheader">
                    <div id="tabs">
                      <ul>
                        <li><a href="#tabs-1">Snap</a></li>
                      </ul>
                      <div id="tabs-1">

                <!--form container starts here-->
                <div class="form-container">
                  <div class="inputwrap">
                    <div class="formleftside-content">
		
 <form name='form1' method='post' action=''>
    	            <table  width = "600" bgcolor="#f5f5f5" border = "0"  cellspacing = "0" cellpadding = "0" class = 'outer_border'>

			<th style="border:#D1D1D1 1px solid; padding:5px;"> Minute</th>
			<th style="border:#D1D1D1 1px solid; padding:5px;"> Hour</th>
			<th style="border:#D1D1D1 1px solid; padding:5px;"> Day of Month</th>
			<th style="border:#D1D1D1 1px solid; padding:5px;"> Month</th>
			<th style="border:#D1D1D1 1px solid; padding:5px;"> Days</th>

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
for min_num in select_opt_min:
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
	if(select_hour_val !=''):
		for hour_list in select_hour_val:
			if(hour_list == str(hour_num)):
				print """selected = 'selected'"""


	print""">"""+str(hour_num)+"""</option>"""
print"""
			</select>

 <select style="margin-left: 34%;width: 54%;display:"""+display_hour+""";" id ="select_id7" name = "select_hour1" >
                        <option>*</option>"""
for hour_num in select_opt_hour:
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
	if(select_day_month_val !=''):
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

	if(select_month_val !=''):
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
	if(select_day_val !=''):
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
	
         <button class="button_example" type="submit" name = 'submit_snap' value = 'snap_val'>SnapShot</button>
</div>


        </form>

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
"""
