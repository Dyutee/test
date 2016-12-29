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

dd_val = 'None'
burst_length = '1048576'
hd_val = 'None'
idata_val = 'No'
init_val = 'No'
max_busrst_length = '1048576'
max_R2t = '32'
max_receive_data_segment = '1048576'
max_session = '0'
nop_interval = '30'
max_xmi_length  = '1048576'
qued_command = '32'
rsp_timeout = '90'
address_method ='PERIPHERAL'
enabled = '1'
per_portal ='1'
input_grouping ='auto'

random_target=san_disk_funs.get_iscsi_target_name()
remove_targets_list= san_disk_funs.iscsi_list_all_tgt()

select_targets=san_disk_funs.iscsi_list_all_tgt_att()

#-----------------------Target Properties------------------------#
#----------------------Select the Target name to Get the Information of the selected target-----------------------------------

if(form.getvalue('target_prop_delete')):
        target_select_delete_prop = form.getvalue('target_prop_delete')
        target_name = target_select_delete_prop.strip()
        print "<script>location.href = 'iframe_iscsi_properties_new.py?target="+target_name+"#tabs-1';</script>"
if(form.getvalue('iscsi_props')):

        target_select_prop_name = form.getvalue('target_prop_delete')
        target_name = target_select_prop_name.strip()
        data_digest = form.getvalue('ddigest')
        burst_len = form.getvalue('fbl')
        header_dig = form.getvalue('hd')
        im_data = form.getvalue('idata')
        in_r2t  = form.getvalue('initr2t')
        max_burst_len = form.getvalue('mbl')
        max_out = form.getvalue('mor2t')
        max_receive_data = form.getvalue('mrdsl')
        max_sess = form.getvalue('max_conn')
        max_xmit = form.getvalue('medsl')
        nop_intervals = form.getvalue('nopinterval')
        qued_comm = form.getvalue('qc')
        rsp_time = form.getvalue('rspto')
        attrstring = '';

        iscsi_prop_name = 'DataDigest='+str(data_digest)
        blength         = 'FirstBurstLength='+str(burst_len);
        headerdigest = 'HeaderDigest='+str(header_dig)
        imd_data = 'ImmediateData='+str(im_data)
        in_r2 = 'InitialR2T='+str(in_r2t)
        max_bursts_len = 'MaxBurstLength='+str(max_burst_len)
        max_receive_d = 'MaxRecvDataSegmentLength='+str(max_receive_data)
        max_sess_n = 'MaxSessions='+str(max_sess)
        max_xmit_len = 'MaxXmitDataSegmentLength='+str(max_xmit)
        nop_inter = 'NopInTimeout='+str(nop_intervals)
        qued_con = 'QueuedCommands='+str(qued_comm)
        rsp_times = 'RspTimeout=' +str(rsp_time)

        attrstring = '"'+ iscsi_prop_name + ','+ blength +','+headerdigest +','+ in_r2 + ',' + max_bursts_len + ','+ max_receive_d + ',' + max_sess_n + ',' + max_xmit_len + ',' + nop_inter + ',' + qued_con + ',' + rsp_times +'"'
        target_set_attribute = san_disk_funs.iscsi_set_tgt_attr(target=target_select_prop_name, attr=attrstring)

        if(target_set_attribute == True):
                print"""<div id = 'id_trace'>"""
                print "Successfully Set the Target!"
                print "</div>"
                print "<script>location.href = 'iframe_iscsi_properties_new.py?target="+target_name+"#tabs-1';</script>"
        else:
                print"""<div id = 'id_trace_err'>"""
                print "Error occured while Set the Target !"
                print "</div>"
                print "<script>location.href = 'iframe_iscsi_properties_new.py?target="+target_name+"#tabs-1';</script>"
#--------------------------------End-------------------------------------------#

if (iscsi_status > 0):

        print
        print """
              <!--Right side body content starts from here-->
              <div class="rightsidecontainer" style="margin:0;width:711px;padding-left:0px;">
                <!--<div class="insidepage-heading">I-Scsi >> <span class="content">I-Scsi Configuration</span></div>-->
                <!--tab srt-->
                <div class="searchresult-container">
                  <!--<div class="infoheader">
                    <div id="tabs">
                      <ul>
                        <li><a href="#tabs-1">Target Properties</a></li>
                      </ul>
                      <div id="tabs-1">-->

                <!--form container starts here-->
		
                <div class="form-container">
		 <div class="topinputwrap-heading">Target Properties</div>
                  <div class="inputwrap">
                    <div class="formrightside-content">

	<form name = 'add_properties1' method = 'POST'>
                <table width = "685" border = "0" cellspacing = "0" cellpadding = "0" name = 'disp_tables' id = 'id_target_properties'>

        <tr>
                        <td width = '23%' class = "table_heading" height = "35px" valign = "middle">
                        Select target
                        </td>
                        <td class = "table_content" height = "35px" valign = "middle">
                        <div class="styled-select2" style="width:518px;">
                        <select class = 'input' name = 'target_prop_delete' onchange = 'this.form.submit();' style = 'width:531px;'>
                        <option value='prop_val'>Select Target</option>"""
	#-----------------display Target Information in selectbox-----------------------------------
        for  prop_target_det in db_list_target:
                print """<option value = '"""+prop_target_det+"""'"""
                if(target_select_delete_prop !=''):
                        if(target_select_delete_prop == prop_target_det):
                                print """selected = 'selected'"""
                print """>"""+prop_target_det+"""</option>"""
	#---------------------------------End--------------------------------------------------

        print"""</select></div>
        </td>
        </tr>"""

        if (select_targets != [{}]):
                for target_prop in select_targets:
                        #print 'tar1:'+str(target_prop['target'])
                        #print '<br/>'
                        #print 'tar2:'+str(target_select_delete_prop)

                        #if(target_prop['target']==target_select_delete_prop):
                        if(target_prop['target'].strip()==target_name.strip()):
                                #print target_prop
                                dd_val = target_prop['DataDigest']
                                #print dd_val
                                burst_length = target_prop['FirstBurstLength']
                                #print burst_length
                                hd_val = target_prop['HeaderDigest']
                                idata_val = target_prop['ImmediateData']
                                init_val = target_prop['InitialR2T']
                                max_busrst_length = target_prop['MaxBurstLength']
                                max_R2t = target_prop['MaxOutstandingR2T']
                                max_receive_data_segment = target_prop['MaxRecvDataSegmentLength']
                                max_session = target_prop['MaxSessions']
                                nop_interval = target_prop['NopInInterval']
                                max_xmi_length = target_prop['MaxXmitDataSegmentLength']
                                qued_command = target_prop['QueuedCommands']
                                rsp_timeout = target_prop['RspTimeout']
                                address_method = target_prop['addr_method']
                                enabled = target_prop['enabled']
                                per_portal= target_prop['per_portal_acl']
                                input_grouping = target_prop['io_grouping_type']
	print"""<tr>

                        <td width = '40%' class = "table_heading" height = "35px" valign = "middle">
                                Data digest
                        </td>
                        <td class = "table_content" height = "35px" valign = "middle">
                                <div class="styled-select2" style="width:118px;">
                                <select class = 'input' name = 'ddigest'>"""

        if (dd_val == 'None'):

                print"""<option value = 'None' selected>None</option>""";
                print"""<option value = 'CRC32C'>CRC32C</option>""";


        elif (dd_val == 'CRC32C'):

                print"""<option value = 'None'>None</option>""";
                print"""<option value = 'CRC32C' selected>CRC32C</option>""";


        else:

                print"""<option value = 'None' selected>None</option>""";
                print"""<option value = 'CRC32C'>CRC32C</option>""";


        print"""</select></div>
        </td>
        </tr>"""
        print"""<tr>
                <td class = "table_heading" height = "35px" valign = "middle">
                        First burst length
                </td>
                <td class = "table_content" height = "35px" valign = "middle">
                        <input class = 'textbox' type = 'text' name = 'fbl' value = '"""+burst_length+"""'>
                </td>
                </tr>"""
        print"""<tr>
                <td class = "table_heading" height = "35px" valign = "middle">
                        Header digest
                </td>
                <td class = "table_content" height = "35px" valign = "middle">
                        <div class="styled-select2" style="width:118px;">
                        <select class = 'input' name = 'hd'>"""
        if (hd_val == 'None'):

                print"""<option value = 'None' selected>None</option>""";
                print"""<option value = 'CRC32C'>CRC32C</option>""";

	elif (hd_val == 'CRC32C'):

                print"""<option value = 'None'>None</option>""";
                print"""<option value = 'CRC32C' selected>CRC32C</option>""";


        else:

                print"""<option value = 'None' selected>None</option>""";
                print"""<option value = 'CRC32C'>CRC32C</option>""";

                print"""</select></div>
                </td>
                </tr>"""

        print"""<tr>
                        <td class = "table_heading" height = "35px" valign = "middle">
                                Immediate data
                        </td>
                        <td class = "table_content" height = "35px" valign = "middle">
                                <div class="styled-select2" style="width:118px;">
                                <select class = 'input' name = 'idata'>"""

        if (idata_val == 'Yes' or idata_val == ''):

                print"""<option value = 'Yes' selected>Yes</option>""";
                print"""<option value = 'No'>No</option>""";


        else:

                print"""<option value = 'Yes'>Yes</option>""";
                print"""<option value = 'No' selected>No</option>""";


        print"""</select></div>
        </td>
        </tr>"""
        print"""<tr>
        <td class = "table_heading" height = "35px" valign = "middle">
                Initial R2T
        </td>
        <td class = "table_content" height = "35px" valign = "middle">
                <div class="styled-select2" style="width:118px;">
                <select class = 'input' name = 'initr2t'>"""

        if (init_val == 'No' or init_val == ''):

                print"""<option value = 'Yes'>Yes</option>""";
                print"""<option value = 'No' selected>No</option>""";

	else:

                print"""<option value = 'Yes' selected>Yes</option>""";
                print"""<option value = 'No'>No</option>""";

        print"""</select></div>
        </td>
        </tr>"""
        print"""<tr>
                        <td class = "table_heading" height = "35px" valign = "middle">
                                Max burst length
                        </td>
                        <td class = "table_content" height = "35px" valign = "middle">
                                <input class = 'textbox' type = 'text' name = 'mbl' value = '"""+max_busrst_length+"""'>
                        </td>
                        </tr>
                        <tr>
                        <td class = "table_heading" height = "35px" valign = "middle">
                                Max outstanding R2T
                        </td>
                        <td class = "table_content" height = "35px" valign = "middle">
                                <input class = 'textbox' type = 'text' name = 'mor2t' value = '"""+max_R2t+"""'>
                        </td>
                        </tr>
                        <tr>
                        <td class = "table_heading" height = "35px" valign = "middle">
                                Max recv. data segment length
                        </td>
                        <td class = "table_content" height = "35px" valign = "middle">
                                <input class = 'textbox' type = 'text' name = 'mrdsl' value = '"""+max_receive_data_segment+"""'>
                        </td>
                        </tr>
                        <tr>
                        <td class = "table_heading" height = "35px" valign = "middle">

                 Max sessions
                        </td>
                        <td class = "table_content" height = "35px" valign = "middle">
                                <input class = 'textbox' type = 'text' name = 'max_conn' value = '"""+max_session+"""'>
                        </td>
                        </tr>
                        <tr>
                        <td class = "table_heading" height = "35px" valign = "middle">
                                Max xmit data segment length
                        </td>
                        <td class = "table_content" height = "35px" valign = "middle">
                                <input class = 'textbox' type = 'text' name = 'medsl' value = '"""+max_xmi_length+"""'>
                        </td>
                        </tr>
			<tr>
                        <td class = "table_heading" height = "35px" valign = "middle">
                                Nop in interval
                        </td>
                        <td class = "table_content" height = "35px" valign = "middle">
                                <input class = 'textbox' type = 'text' name = 'nopinterval' value = '"""+nop_interval+"""'>
                        </td>
                        </tr>
                        <tr>
                        <td class = "table_heading" height = "35px" valign = "middle">
                                Queued commands
                        </td>
                        <td class = "table_content" height = "35px" valign = "middle">
                                <input class = 'textbox' type = 'text' name = 'qc' value = '"""+qued_command+"""'>
                        </td>
                        </tr>
                        <tr>
                        <td class = "table_heading" height = "35px" valign = "middle">
                                RSP timeout
        </td>
                        <td class = "table_content" height = "35px" valign = "middle">
                                <input class = 'textbox' type = 'text' name = 'rspto' value = '"""+rsp_timeout+"""'>
                        </td>
                        </tr>

                        <tr>
                        <td class = "table_heading" height = "35px" valign = "middle">
                                Address Method
                        </td>
                        <td class = "table_content" height = "35px" valign = "middle">
                                <input class = 'textbox' type = 'text' name = 'addr_method' value = '"""+address_method+"""' readonly>
                        </td>
                        </tr>

                        <tr>
                        <td class = "table_heading" height = "35px" valign = "middle">
                                Enabled
                        </td>
                        <td class = "table_content" height = "35px" valign = "middle">
                                <input class = 'textbox' type = 'text' name = 'enab' value = '"""+enabled+"""' readonly>
                        </td>
                        </tr>

                        <tr>
                        <td class = "table_heading" height = "35px" valign = "middle">
                                Per Portal
                        </td>
                        <td class = "table_content" height = "35px" valign = "middle">
                                <input class = 'textbox' type = 'text' name = 'port' value = '"""+per_portal+"""' readonly>
                        </td>
        </tr>
			 <tr>
                        <td class = "table_heading" height = "35px" valign = "middle">
                                Io Grouping
                        </td>
                        <td class = "table_content" height = "35px" valign = "middle">
                                <input class = 'textbox' type = 'text' name = 'port' value = '"""+input_grouping+"""' readonly>
                        </td>
                        </tr>

        <tr>
        <td>
        <div>
        <td style="float:right;">
        <button class = 'buttonClass' type="submit" name = 'iscsi_props' value = 'Apply' onclick = 'return validate_iscsi_props_nw();'>Apply</button></td>
        <!--<button class = 'buttonClass' type="submit" name = 'iscsi_props' value = 'Apply' onclick = 'return validate_iscsi_props(this.form.name, this.form.elements.length);'>Apply</button></td>-->
        </div>
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
else:
        print "<div style = 'margin-top: 10%; margin-bottom: 10%; margin-left: auto; margin-right: auto; text-align: center; vertical-align: center; color: darkred; width: 65%; font: 16px Arial;'>Check the 'Enable/Disable i-SCSI' option in Maintenance -><a href ='main.py?page=sr'style ='text-decoration:underline;'>Services</a>.</div>"

