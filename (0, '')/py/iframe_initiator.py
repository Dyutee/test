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

sys.path.append('/var/nasexe/')
import net_manage_newkernel as net_manage_bond

get_all_iface = net_manage_bond.get_all_ifaces_config()
        #print get_all_iface

if(get_all_iface["id"]==0):
        iface_info = get_all_iface["all_conf"]

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


#----------------------ADD Initiator-----------------------------------#
#----------Get a targetname,portal and all portals from form and pass the variable like target_name and checkall in backend function for add initiator 
#if(form.getvalue('list_targets')):
#       target_list = form.getvalue('list_targets')
#       print "<script>location.href = 'main.py?page=prop_iscsi#tabs-1';</script>"
if(form.getvalue('iscsi_ips')):

        ini_target_list = form.getvalue('list_targets')
        target_name = ini_target_list.strip()
        add_ini = form.getvalue('all_portal')
        add_ips = form.getvalue('check_portal[]')
        checkall = form.getvalue('check_all_portal')
        get_ini_array = [];
        gets_initiator_list = san_disk_funs.iscsi_ini_list(ini_target_list)
        #print 'GET INI:'+str(gets_initiator_list)
        used_disks_name = san_disk_funs.iscsi_used_disks_tgt(ini_target_list)
        if(used_disks_name ==[]):
                 print"""<div id = 'id_trace_err'>"""
                 print "First add the Disk!"
                 print "</div>"
        else:
                 #print "<script>location.href = 'main.py?page=iscsi_prop#tabs-1';</script>"
        #print used_disks_name
                for l in gets_initiator_list:
                        #print 'L'+str(l)
                        get_ini1 = l[:l.find('#') + 1]
                        get_ini_array.append(get_ini1);
                        #print 'INI2:'+str(get_ini_array)


                test_ini = add_ini + '#';
                test_ini = test_ini.strip();

                #print test_ini;
                #print get_ini_array;

                #print 'GET ARRAY'+str(get_ini_array)
                if(add_ini + '#' in get_ini_array):
                        #print 'True'
                        #print 'Error'

                        print"""<div id = 'id_trace_err'>"""
                        print "Duplicate Entry!"
                        print "</div>"
                else:
                        #rint 'True'
			add_ips = str(add_ips);
                        add_ips = add_ips.replace('[', '');
                        add_ips = add_ips.replace(']', '');
                        add_ips = add_ips.replace("'", "");
                        add_ips = add_ips.replace(' ', '');

                        if (checkall == '*'):
                                add_ips = '*';

                        ini_ip_string = add_ini + '#' + add_ips;

                        #print ini_ip_string;

                        check_add_ips = isinstance(add_ips, str)
                        #print check_add_ips
                        if(check_add_ips == True):

                                add_initiator=san_disk_funs.iscsi_ini_add(ini_target_list,ini_ip_string)

                        #else:
                        #       add_ips = set(add_ips)
                        #       for ips_val in add_ips:
                        #               add_initiator=san_disk_funs.iscsi_ini_add(ini_target_list,ini_ip_string)
                        #add_initiator=san_disk_funs.iscsi_ini_add(ini_target_list,ini_ip_string)
                                if(add_initiator == True):
                                        print"""<div id = 'id_trace'>"""
                                        print "Successfully Added the Initiator!"
                                        print "</div>"
                                        print "<script>location.href = 'iframe_initiator.py?target="+target_name+"#tabs-1';</script>"
                                else:
                                        print"""<div id = 'id_trace_err'>"""
                                        print "Error occured while Adding !"
                                        print "</div>"
                                        print "<script>location.href = 'iframe_initiator.py?target="+target_name+"#tabs-1';</script>"
#---------------------------------End--------------------------------#
#-------------------Check Session is Active or Not--------------------
ses_ip = ''

#-------------------End-----------------------------------------------

#---------------------- Delete Initiator------------------------------#
#---------------Get a tagetname and initiator name from form and pass "show_list_target" and ini_name in backend function for remove the Initiator-------------
if(form.getvalue('choose_list')):
        show_target = form.getvalue('choose_list')
        target_name = show_target.strip()

        #-------------Check Session is Active or not---------------#
        sesion_tar =san_disk_funs.iscsi_session(show_target)
        #------------------End-------------------------------------#

        print "<script>location.href = 'iframe_initiator.py?target="+target_name+"#tabs-2';</script>"
        initiator_list = san_disk_funs.iscsi_ini_list(show_target)

if(form.getvalue('delete_initiator')):
        show_list_target = form.getvalue('choose_list')

        #---------------Check Session is Active or not--------------#
        sesion_tar =san_disk_funs.iscsi_session(show_list_target)
        #-----------------End---------------------------------------#

        ini_name = form.getvalue('initr_list')
        #abc = []
        check_used_disk = san_disk_funs.iscsi_used_disks_tgt(show_list_target)

        if(sesion_tar ==[]):
                remove_ini = san_disk_funs.iscsi_ini_del(show_list_target,ini_name)
                if(remove_ini == True):

                        print"""<div id = 'id_trace'>"""
                        print "Successfully Deleted the Initiator!"
                        print "</div>"
                        print "<script>location.href = 'iframe_initiator.py?target="+target_name+"#tabs-2';</script>"
                else:

                        print"""<div id = 'id_trace_err'>"""
                        print "Error Occurred while deleting Initiator!"
                        print "</div>"
                        print "<script>location.href = 'iframe_initiator.py?target="+target_name+"#tabs-2';</script>"
        else:
                print"""<div id = 'id_trace_err'>"""
                print "First logout from Session !"
                print "</div>"
                print "<script>location.href = 'iframe_initiator.py?target="+target_name+"#tabs-2';</script>"
#--------------------------------End-----------------------------#

if (iscsi_status > 0):

        print
        print """
              <!--Right side body content starts from here-->
              <div class="rightsidecontainer"  style="margin:0;width:711px;padding-left:0px;">
                <!--<div class="insidepage-heading">I-Scsi >> <span class="content">I-Scsi Configuration</span></div>-->
                <!--tab srt-->
                <div class="searchresult-container">
                  <div class="infoheader">
                    <div id="tabs">
                      <ul>
                        <li><a href="#tabs-1">Add Initiator</a></li>
                        <li><a href="#tabs-2">Delete Initiator</a></li>
                      </ul>
                      <div id="tabs-1">

                <!--form container starts here-->
                <div class="form-container">
                  <!--<div class="topinputwrap-heading">Add Initiator </div>-->
                  <div class="inputwrap">
                    <div class="formrightside-content">
                <form name = 'add_ips_form' method = 'POST'>

                  <table width = "685" border = "0" cellspacing = "0" cellpadding = "0">
                                                                <tr>
                                                                        <td width = '23%' height = "35px" >
                                                                                Choose a target
                                                                        </td>
                                                                        <td>
                        <!--<div class="styled-select2" style="width:518px;">
                        <select name = 'list_targets' class = 'input' style = 'width:103%;'>
                        <option value = 'list_ini_val'>Select Target</option>-->
                        <input class = 'textbox' type = 'text' name = 'list_targets' value = '"""+str(target_name)+"""'style = 'width: 96%;'>

                        """
	print"""</td>
        </tr>"""


	print"""

        <tr>
                                                        <td width = '30%' class = "table_heading" height = "35px" valign = "middle">
                                                                Enter initiator name
                                                        </td>
                                                        <td class = "table_content" height = "35px" valign = "middle">
                                                                <input id = 'id_add_props' class = 'textbox' type = 'text' name = 'all_portal' style = 'width: 96%;'>
                                                        </td>
                                                </tr>


                                                <tr>

        <td>
                                                <input type= "hidden" name = "ini_list" value= '"""+target_list+"""'>
                                                </td>
                                                </tr>

        <tr>
                                                        <td height = "35px" valign = "middle" style ="color:Black;font-family:serif;">
                                                                Check the portal(s)
                                                        </td>
        </tr>
        </table>
        <table width = "685" border = "1" cellspacing = "0" cellpadding = "0" style="border-style:ridge;">
        <tr style = 'background-color:#999999; font-weight: bold;'>
                                                                        <td height = "30px" valign = "middle" style = 'color: #FFF;text-align:center;'>
                                                                                Device
                                                                        </td>
                                                                        <td height = "30px" valign = "middle" style = 'color: #FFF;text-align:center;'>
                                                                                IP
                                                                        </td>
                                                                        <td height = "30px" valign = "middle" style = 'color: #FFF;text-align:center;'>
                                                                                Status
                                                                        </td>

	 </tr>"""


	for ip_info in iface_info:
                #print ip_info
                device_info = ip_info['iface']
                #print device_info
                ip_information = ip_info['address']
                status_info = ip_info['status']

                #print ip_information +'<br/>'

                print"""<tr>
                <td style = "text-align:center;">

                """+device_info+"""
                </td>
                <td style = "text-align:center;">

                """+ip_information+""" 
                </td>
                <td style = "text-align:center;">
                """+status_info+"""
                </td>
                <td height = "35px" valign = "middle" style = "text-align:center;">
                <input type = 'checkbox' name = 'check_portal[]' value = '""" + ip_information + """' onclick = 'return uncheck_all();'>
                </td>
                </tr>

        """
        print"""</table>


        <table>
        <tr>
        <td colspan = "2">
        <input type = 'checkbox' name = 'check_all_portal' value = '*' onclick = 'return uncheck_all();'><B>Add All</B>
        <div>
        <td style="width: 5%; padding-left: 39%;">
        <button class = 'buttonClass' type="submit" name = 'iscsi_ips' value = 'Apply' onclick = 'return validate_add_initiator();'>Apply</button></td></div>
        </td></tr></table>
                                                


        </form>"""


        print"""
                   </div>
                  </div>
                </div>
                <!--form container ends here-->
                <p>&nbsp;</p>
                      </div>
	 <div id="tabs-2">
                <!--form container starts here-->
                <div class="form-container">
                  <!--<div class="topinputwrap-heading">Delete Initiator</div>-->
                  <div class="inputwrap">
                <div class="formrightside-content">
                <form name = 'del_initr_from_target' action = '#' method = 'POST'>
                <table width = "685" border = "0" cellspacing = "0" cellpadding = "0" id = "id_del_ini">
                                                                                        <tr>
                                                                                        <td width = '23%' height = "35px" valign = "middle">
                                                                                                Choose Target
                                                                                        </td>
                                                                                        <td class = "table_content" height = "35px" valign = "middle">
                         <div class="styled-select2" style="width:518px;">
                        <select class = 'input' name = 'choose_list' onchange='this.form.submit()' style = 'width:103%;'>

                        <option value = 'choose_list_val'>Select Target</option>"""

        #for choose_list in remove_targets_list:
        for choose_list in db_list_target:
                print """<option value = '"""+str(choose_list)+"""'"""
                if(show_target !=''):
                        if(show_target == choose_list):
                                print """selected = 'selected'"""
                print """>"""+str(choose_list)+"""</option>"""

        print"""</select></div>
        </td>
        </tr>"""

        print"""
                                                                                <tr>
                                                                                        <td width = '23%' class = "table_heading" height = "35px" valign = "middle">
                                                                                                Choose initiator
                                                                                        </td>
                                                                                        <td class = "table_content" height = "35px" valign = "middle">
                        <div class="styled-select2" style="width:518px;">
                        <select class = 'input' name = 'initr_list' style = 'width:103%;'>
                        <option value = 'initr_list_val'>Select Initiator</option>"""

	for ini_list in initiator_list:
                #if(ini_list == '*#*'):
                #       ini_list = '*'

                #       print """<option value = '"""+ini_list+"""'>"""+ini_list+"""</option>"""
                #else:

                print """<option value = '"""+ini_list+"""'>"""+ini_list+"""</option>"""


        print"""</select></div>
        </td>
        </tr>"""
        print"""<tr>
        <td>
        <div>
        <td style="float:right;"> 
        <button class = 'buttonClass' type="submit" name = 'delete_initiator' value = 'Remove initiator' onclick = 'return validate_remove_ini();'>Delete</button>
        </td>
        </div>
        </tr>"""
        print"""</table>
        </form>
        """




        print"""        </div>
                </div>
                </div>
                <!--form container ends here-->
                <p>&nbsp;</p>
                      </div>"""
