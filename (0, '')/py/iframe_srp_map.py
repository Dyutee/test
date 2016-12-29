#!/usr/bin/python
import cgitb, sys, common_methods, include_files, cgi
cgitb.enable()
sys.path.append('../modules/')
import disp_except;
try:
	#---------------------Assined a Blanck value for variable----------------------------
	select_target_val = ''
	get_value_db = {'output':()}
	stgt_info = ''
	dtgt_info = ''
	node_info = ''
	time_info = ''
	src_tgt = ''
	dest_tgt = ''
	display_list = 'none' 
	display_target = 'block'
	#-----------------------------End---------------------------------------------------
	#-----------------------------Import mysql database-------------------------------
	import MySQLdb
        db = MySQLdb.connect("localhost","root","netweb","fs2" )
        cursor = db.cursor()
	#from tools import 
	sys.path.append('/var/nasexe/python/')
	import tools
	from tools import scan_remount
	from tools import db
	#---------------------------------------------------End------------------------------
	form = cgi.FieldStorage()
	#---------------------------------Check ha sataus------------------------------------------
	check_ha = tools.check_ha()
	#------------------------------------End--------------------------------------------------
	#---------------------------------Get Node name-----------------------------------------------------

	sys_node_name = tools.get_ha_nodename()
        if(sys_node_name == "node1"):
                other_node = "node2"
                show_tn = "Node1"
                show_on = "Node2"
        else:
                other_node = "node1"
                show_tn = "Node2"
                show_on = "Node1"

        query="select * from network_ifaces where (name='eth1' and node='"+other_node+"')"
        status=db.sql_execute(query)
        for x in status["output"]:
                other_node_ip = x["ip"]
	#------------------------------------------------End--------------------------------------------------
	
	srp_query = "select * from ib_tgt"
	srp_status = db.sql_execute(srp_query)
	#-------------------------------------Get a value from value from form and pass in the backend function--------------------------
	if(form.getvalue('get_value')):
		src_tgt = form.getvalue('select_source')
		src_select_query = "select state from ib_tgt where tgt='"+src_tgt+"';"
        	fetch_dest_status = cursor.execute(src_select_query)
        	data = cursor.fetchone()
		select_src_id = data[0]
		dest_tgt = form.getvalue('select_destination')
		dest_select_query = "select state from ib_tgt where tgt='"+dest_tgt+"';"
		fetch_dest_status = cursor.execute(dest_select_query)
		row = cursor.fetchone()
                select_dest_id = row[0]
		node = form.getvalue('node_name')
		if(select_src_id == 1 and select_dest_id == 1):
			srp_insert = tools.insert_ib_map(src_tgt, dest_tgt, node)
			if(srp_insert['id'] == 0):
				print "<div id='id_trace'>"
                        	#print "Successfully map the SRP Information!"
				print "SRP targets mapped successfully!"
                        	print "</div>"
		else:
			#print False
			print "<div id='id_trace_err'>"
                        print "Error occurred while mapping!"
                        print "</div>"
		print "<script>location.href = 'iframe_srp_map.py#tabs-1';</script>"
	#---------------------------------End----------------------------------------------------------------------------------------------
	#-----------------Retreive a value from backend function--------------------
	if(form.getvalue('select_source1')):
		select_target_val = form.getvalue('select_source1')
		get_value_db =  tools.retrieve_ib_map(select_target_val)
		display_target = 'none'
		display_list = 'block'
		print "<script>location.href = 'iframe_srp_map.py#tabs-2';</script>"
	#-----------------------------------End---------------------------------------

	#import left_nav
	print
	print """
		<div id="loader-div" style="text-align:center; display:none;" ><img style="margin-top:20%;" src="../images/ajax-loader.gif" /><br/> Loading...</div>
	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer" id="body-div">
		<!--tab srt-->
		<div class="searchresult-container">
		 <div style="margin:0 0 0px 0;" class="topinputwrap-heading"><a class="demo" href ="#"><img src ="../images/help_icon1.png" style="width:13px;"><span class="tooltip" >
                 <table border="0">
        <tr>     
        <td class="text_css">This page allows you to map SRP targets between 2 nodes. You can also view the mapping details for targets.</td>
        </tr>
        </table>"""
	if(check_ha == True):
		print"""
	
	</span></a><span style="color:#fff;margin-left:7px;">SRP Map Information ("""+show_tn+""")</span>
                <span style="float:right; margin:0 0px 0 0;"><a onclick="return onclick_loader();" class="resource_links" href="https://"""+other_node_ip+"""/fs4/py/iframe_srp_map.py">"""+show_on+"""</a></span>

                </div>"""
	else:
		print """ </span></a>SRP Map Information </div>"""
	print"""
		  <div class="infoheader">
		    <div id="tabs">
		      <ul>
			<li><a href="#tabs-1">SRP</a></li>
			<li><a href="#tabs-2">SRP List</a></li>
		      </ul>
		      <div id="tabs-1">

		<!--form container starts here-->
		<div class="form-container">
		  <div class="inputwrap">
		    <div class="formleftside-content">
	<form name='form1' method='post' action=''>
	 <table  width = "480" border = "0"  cellspacing = "0" cellpadding = "0">
                <tr>
 <td valign="top">
  <label>Source Target:<font color ="#EC1F27">*</font></label>
 </td>
 <td valign="top">
	<div class="styled-select2" style="width:218px;">
                        <select name = 'select_source' style="width:230px;">
                        <option value = 'select_src_val'>Select Target </option>"""

	for src_target_list in srp_status["output"]:
		target_list = src_target_list["tgt"]
		print"""
		<option value = '"""+target_list+"""'"""
		if(src_tgt !=''):
			if(target_list == src_tgt):
				print"""selected ='selected'""" 

		print""">"""+target_list+"""</option>"""
	print"""

			</select>
	</div>
 </td>
</tr>

	<tr>
 <td valign="top">
  <label>Destination Target:<font color ="#EC1F27">*</font></label>
 </td>
 <td valign="top">
        <div class="styled-select2" style="width:218px;">
                        <select name = 'select_destination'style="width:230px;">
                        <option value = 'select_dest_val'>Select Target </option>"""

	for dest_target_list in srp_status["output"]:
		target_list1 = dest_target_list["tgt"]
		print"""
			 <option value = '"""+target_list1+"""'"""
		if(dest_tgt !=''):
			if(target_list1 == dest_tgt):
				print """selected ='selected'"""
		print""">"""+target_list1+"""</option>"""
	print"""
                        </select>
        </div>
        
 </td>
</tr>

	<tr>
 <td valign="top">
  <label>Node:<font color ="#EC1F27">*</font></label>
 </td>
 <td valign="top">
         <input  type="text" class = 'textbox' name="node_name" readonly maxlength="100" size="25" value = '"""+sys_node_name+"""' style="width: 218px;">
 </td>
</tr>
<tr>
<td colspan = "2">
                <button class="buttonClass" type="submit" name = 'get_value'  id = 'id_create_but'  value = 'Apply' onclick ='return srp_map();'style ="float:right;">Apply</button>
</td>
</tr>
	</table>
	</form>
		</div>
		  </div>
		</div>
		<!--form container ends here-->
		<p>&nbsp;</p>
		      </div>

<div id="tabs-2">

                <!--form container starts here-->
                <div class="form-container">
                  <div class="inputwrap">
                    <div class="formleftside-content">
		
	        <form name='form2' method='post' action=''>
         <table  width = "480" border = "0"  cellspacing = "0" cellpadding = "0">
                <tr>
 <td valign="top">
  <label>Source Target:<font color ="#EC1F27">*</font></label>
 </td>
 <td valign="top">
        <div class="styled-select2" style="width:218px;">
                        <select name = 'select_source1'style="width:230px;"  onchange='this.form.submit()'>
                        <option value = 'select_source1_val'>Select Target </option>"""
	for select_target_list in srp_status["output"]:
		sel_target_list = select_target_list["tgt"]
		print""" <option value = '"""+sel_target_list+"""'"""
		if(select_target_val !=''):
			if(select_target_val == sel_target_list):
				print """selected='selected'"""
		

		print""">"""+sel_target_list+"""</option>"""
		
	print"""
                        </select>
        </div>
        
 </td>
</tr>
</table>
<table width = "680" style="margin-top: 13%;">
                <tr>
                <th style="border:#D1D1D1 1px solid;width:22%;">Source Target</th>
                <th style="border:#D1D1D1 1px solid;">Destination Target</th>
                <th style="border:#D1D1D1 1px solid;">Node</th>
                <th style="border:#D1D1D1 1px solid;">Time</th>
                </tr>

		<tr>
                <td  style="border:#D1D1D1 1px solid;padding-top:16%;text-align:center;margin-right:-530px;display:"""+display_target+"""";" colspan = "4">
                <span>Select the Target to Get Information</span>
                </td>
                </tr>
		"""
	if(get_value_db["output"] != ()):
		for info_list in get_value_db["output"]:
			stgt_info = info_list["stgt"]
			dtgt_info = info_list["dtgt"]
			node_info = info_list["node"]
			time_info = info_list["time"]
	
		print"""<tr>
                        <td style = "text-align:center;border:#D1D1D1 1px solid;">"""+stgt_info+"""</td>
                        <td style = "text-align:center;border:#D1D1D1 1px solid;">"""+dtgt_info+"""</td>
                        <td style = "text-align:center;border:#D1D1D1 1px solid;">"""+node_info+"""</td>
                        <td style = "text-align:center;border:#D1D1D1 1px solid;">"""+str(time_info)+"""</td>
			</tr>"""

	else:
        	print"""<tr>
                <td style="border:#D1D1D1 1px solid;padding-top: 3%; text-align: center;margin-right:-530px;display:"""+display_list+""";"  colspan = "4"><span>No Information is Available for Target <p style="color:green; ">"""+select_target_val+""" </span></td>
                </tr>"""
	print"""
</table>

</form>

</div>
                  </div>
                </div>
                <!--form container ends here-->
                <p>&nbsp;</p>
                      </div>

	"""
except Exception as e:
        disp_except.display_exception(e);
