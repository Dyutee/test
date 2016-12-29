#!/usr/bin/python
import cgitb, sys,  common_methods, cgi ,include_files
cgitb.enable()

sys.path.append('/var/nasexe/python/')
import tools
from tools import db

sys.path.append('/var/nasexe/storage')
import storage_op
import sys,os
from lvm_infos import *
from functions import *
import san_disk_funs

form = cgi.FieldStorage()
display_ini = ''
display_disk = ''
display_target = ''
display_node = ''
display_btn= 'block'
inuser_name = ''
inuser_pwd = ''
#---------Get Information from Db-------
querystring = os.environ['QUERY_STRING'];
target_name = form.getvalue("target")

db_list_target = [target_name]

iscsi_status = common_methods.get_iscsi_status();
target_list =''
display_create = ''
display_delete_target = ''
show_target = ''
initiator_list = ''
show_auth_target = ''
optionsstring = '';
target_select_delete_prop = ''
random_target=san_disk_funs.get_iscsi_target_name()
remove_targets_list= san_disk_funs.iscsi_list_all_tgt()

select_targets=san_disk_funs.iscsi_list_all_tgt_att()



#------------------------iScsi User Start-----------------------------
if(form.getvalue('iscsi_user')):
        show_auth_target = form.getvalue('auth_list')
        #for target_list_all in select_targets:
        #       print target_list_all
        #print '<script>location.href ="main.py?page=iscsi_prop&"""+querystring+"""#subtabs-4";</script>'
        #print "<script>location.href = 'main.py?page=iscsi_prop&page=iscsi_prop#tabs-4';</script>"
        incoming_usr_list = []
        incoming_usr_list = form.getvalue('in_usr_pwd_list[]')
        inuser_name = form.getvalue('in_user')
        inuser_pwd = form.getvalue('in_pwd')

	display_btn = 'none'
        #print inuser_pwd
        #print inuser_name
        #exit();

        #checkforbraces = str(incoming_usr_list).find('[');

        #if (checkforbraces < 0):
        #iu = form.getvalue('in_user');

                #iu = iu.replace('/', ' ');
                #iu = "'" + iu + "'";

        iu = 'IncomingUser=' +str(inuser_name)+' '+str(inuser_pwd);
        #print iu
        iu = "'" + iu + "'";
        #print iu

                #print iu + '<BR>'

        addincominguser = san_disk_funs.iscsi_set_tgt_attr(target=show_auth_target,attr=iu)
        if(addincominguser == True):
                print"""<div id = 'id_trace'>"""
                print "Successfully Add the Incoming User!"
                print "</div>"
                print "<script>location.href = 'iframe_iscsi_authentication.py?target="+target_name+"#tabs-1';</script>"
        else:
                print"""<div id = 'id_trace_err'>"""
                print "Error occured while Adding !"
                print "</div>"
                print "<script>location.href = 'iframe_iscsi_authentication.py?target="+target_name+"#tabs-1';</script>"


#------------------------------End-------------------------------#

#-----------Remove Incoming User---------------------------------#
if(form.getvalue('remove_user')):
        remove_target = form.getvalue("auth_list")
        #print remove_target
        incoming_user = []
        incoming_user = form.getvalue("in_usr_pwd_list[]")
        incoming_usr_list = []
        incoming_usr_list = form.getvalue('in_usr_pwd_list[]')
        inuser_name = form.getvalue('in_user')
        inuser_pwd = form.getvalue('in_pwd')
        #print inuser_pwd
        #print inuser_name
        #exit();

        #checkforbraces = str(incoming_usr_list).find('[');

        #if (checkforbraces < 0):
        #iu = form.getvalue('in_user');

                #iu = iu.replace('/', ' ');
                #iu = "'" + iu + "'";

        iu = 'IncomingUser=' +str(inuser_name)+' '+str(inuser_pwd);
        #print iu
        iu = "'" + iu + "'";
        #print iu
        remove_incoming = san_disk_funs.iscsi_rem_tgt_attr(target = remove_target, attr=iu)
        if(remove_incoming == True):
                print"""<div id = 'id_trace'>"""
                print "Successfully Remove the Incoming User!"
                print "</div>"
                print "<script>location.href = 'iframe_iscsi_authentication.py?target="+target_name+"#tabs-1';</script>"
        else:
                print"""<div id = 'id_trace_err'>"""
                print "Error occured while Removing !"
                print "</div>"
                print "<script>location.href = 'iframe_iscsi_authentication.py?target="+target_name+"#tabs-1';</script>"
        #print remove_incoming
#----------------------------------End---------------------------------------------------

select_targets=san_disk_funs.iscsi_list_all_tgt_att()
#------------------------Authentication Listing-----------------------------------
optionsstring = '';
if(form.getvalue('auth_list')):
        show_auth_target = form.getvalue('auth_list')

        #print "<script>location.href = 'main.py?page=iscsi_prop#tabs-4';</script>"

        #print select_targets
        #print '<br/>'
        #print '<br/>'
        #for target_list_all in db_list_target:
        for target_list_all in select_targets:
		if(target_list_all["target"].strip() == target_name.strip()):
			#print target_list_all["IncomingUser"]
		#if(target_name in target_list_all):
			in_com = target_list_all['IncomingUser']
			#print in_com
			if(in_com != ' '):
				split_in_com = in_com.split()
				inuser_name = split_in_com[0]
				#print 'INUSR:'+str(inuser_name)
				#print '<br/>'
				inuser_pwd = split_in_com[1]
				#print 'INPWD:'+str(inuser_pwd)
				display_btn = 'none'
			else:
				inuser_name = ''
				inuser_pwd = ''
				display_btn = 'block'

			#print inuser_pwd
			if(target_list_all['target']==show_auth_target):
				for key_list in target_list_all:
					if str(key_list).__contains__("IncomingUser"):
						#print key_list + ":" + target_list_all[key_list];
						#print 'Incoming User:'+str(incoming_user_list) 
						target_get_list = target_list_all[key_list]
						#print target_get_list
						target_get_list = target_get_list.strip();
						replace_key = target_get_list.replace(' ', '/')
						if (replace_key != ''):
							optionsstring += "<option value = '" + replace_key + "' selected>" + replace_key + "</option>";

#----------------------------End---------------------------------

if (iscsi_status > 0):

        print
        print """
              <!--Right side body content starts from here-->
              <div class="rightsidecontainer"  style="margin:0;width:716px;padding-left:0px;">
                <!--<div class="insidepage-heading">I-Scsi >> <span class="content">I-Scsi Configuration</span></div>-->
                <!--tab srt-->
                <div class="searchresult-container">
                  <div class="infoheader">
                    <!--<div id="tabs">
                      <ul>
                        <li><a href="#tabs-1">Authentication</a></li>
                      </ul>
                      <div id="tabs-1">-->

                <!--form container starts here-->
                <div class="form-container">
		<div class="topinputwrap-heading">Authentication</div>
                  <div class="inputwrap">
                    <div class="formrightside-content">
	<form name = 'add_users' method = 'POST' action = 'iframe_iscsi_authentication.py?"""+querystring+"""#tabs-1'>
                <table width = "685" border = "0" cellspacing = "0" cellpadding = "0" id = 'id_auth_prop'>

                <tr>
                        <td width = '23%' class = "table_heading" height = "35px" valign = "middle">
                        Choose Target
                        </td>
                        <td class = "table_content" height = "35px" valign = "middle">
                        <div class="styled-select2" style="width:518px;">
                        <select class = 'input' name = 'auth_list' onchange='this.form.submit()' onclick = 'document.getElementById("id_remove_users").disabled = false;' style = 'width:531px;'>

                        <option value = 'auth_list_val'>Select Target</option>"""

        #for auth_target in remove_targets_list:
        for auth_target in db_list_target:
                print """<option value = '"""+auth_target+"""'"""
                if(show_auth_target !=''):
                        if(show_auth_target == auth_target):
                                print """selected = 'selected'"""
                print """>"""+auth_target+"""</option>"""

        print"""</select></div>
                </td>
                </tr>"""

        print"""
                                                
                                                <tr>
                                                        <td colspan = '2' class = "table_heading" height = "35px" valign = "middle">
                                                                <font color="Black"><B>Incoming user:</B></font>
                                                        </td>
                                                </tr>
                                                <tr>
                                                        <td class = "table_heading" height = "35px" valign = "middle">
                                                                Username
                                                        </td>
                                                        <td class = "table_content" height = "35px" valign = "middle">
                                                                <input id = 'id_incoming_usr' class = "textbox" type = 'text' name = 'in_user' value = '"""+inuser_name+"""' style = 'width: 40%;'>
                                                        </td>
                                                </tr>
                                                <tr>
                                                        <td class = "table_heading" height = "35px" valign = "middle">
                                                                Password
                                                        </td>
	<td class = "table_content" height = "35px" valign = "middle">
                                                                <!--<input id = 'id_incoming_pwd' class = 'textbox' type = 'password' name = 'in_pwd' value = '"""+inuser_pwd+""" style = 'width: 80%;'>&nbsp;<a style = 'font-weight: bold; font: 13px Arial; text-decoration: none;' href = '#zzz' onclick = 'return add_usr_pwd(document.getElementById("id_incoming_usr").value, document.getElementById("id_incoming_pwd").value, "IN");'><img style = 'border: 1px solid #BDBDBD;' src = '../images/plus.png' /></a>-->

					<input id = 'id_incoming_pwd' class = 'textbox' type = 'password' name = 'in_pwd' value = '"""+inuser_pwd+"""' style = 'width: 40%;'>&nbsp;<a style = 'font-weight: bold; font: 13px Arial; text-decoration: none;' href = '#zzz' onclick = 'return add_usr_pwd(document.getElementById("id_incoming_usr").value, document.getElementById("id_incoming_pwd").value, "IN");'><!--<img style = 'border: 1px solid #BDBDBD;' src = '../images/plus.png' />--></a>
                                                        </td>
                                                </tr>


        <!--<tr>
                                                        <td>
                                                        </td>
                                                        <td class = "table_content" height = "35px" valign = "middle">
                                                                <select id = 'id_in_users_array' class = 'input' name = 'in_usr_pwd_list[]' style = 'width: 90%; height: 100px;' multiple>"""
        #if (optionsstring != ''):
        #       print optionsstring;


        print """
                                                        
                                                                </select><BR>
        <button class = 'buttonClass' type="submit" name = 'remove_user'  id = 'id_remove_users' value = 'Remove User' onclick = 'return remove_users("IN");'>Remove User</button>

                                                        </td>
                                                </tr>-->


        <tr>
                                                        <td colspan = '3' align = 'right'>

        <!--<button class = 'buttonClass' type='submit' name = 'iscsi_user' value = 'Apply' onclick = 'return validate_iscsi_users();'>Apply</button>-->

        <button class = 'buttonClass' type='submit' name = 'iscsi_user' value = 'Apply' style ="display:"""+display_btn+""";float:left;margin-left:70%;" onclick = 'return validate_iscsi_users();'>Apply</button>
        <button class = 'buttonClass' type="submit" name = 'remove_user'  id = 'id_remove_users' value = 'Remove User' onclick = 'return remove_users("IN");'style= "font-size:11px;">Remove User</button>

	                                                        </td>
	</tr>
	"""




        print"""
        </table></form>


                </div>
                </div>
                </div>
                <!--form container ends here-->
                <p>&nbsp;</p>
                      </div>"""
