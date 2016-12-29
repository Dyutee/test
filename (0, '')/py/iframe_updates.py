#!/usr/bin/python
import cgitb, sys, cgi, include_files
cgitb.enable()

try: # Windows needs stdio set for binary mode.
    import msvcrt
    msvcrt.setmode (0, os.O_BINARY) # stdin  = 0
    msvcrt.setmode (1, os.O_BINARY) # stdout = 1
except ImportError:
    pass

#################################################
################ import modules #################
#################################################
sys.path.append('/var/nasexe/python/')
import patch
import tools
from tools import db
#--------------------- END --------------------#

################################################
################ Check HA Status ###############
################################################
check_ha = tools.check_ha()
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
#--------------------- END --------------------#

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
        <td class="text_css">Using this page, you can upgrade FS2's firmware.</td>
        </tr>
        </table>"""
if(check_ha == True):
	print"""
</span></a> Updates Information ("""+show_tn+""")
	<span style="float:right; margin:0;"><a onclick="return onclick_loader();" class="resource_links" href="https://"""+other_node_ip+"""/fs4/py/iframe_updates.py">"""+show_on+"""</a></span>

	</div>"""
else:
	print"""</span></a><p class = "gap_text">Updates Information</p></div>"""
print"""
          <!--<div class="infoheader">
            <div id="tabs">
              <ul>
                <li><a href="#tabs-1">Updates</a></li>
              </ul>
              <div id="tabs-1">-->

	<!--form container starts here-->
        <div class="form-container">
          <div class="inputwrap">
            <div class="formleftside-content">
	<form enctype="multipart/form-data" action="upload.py" method="post">

	 <table width = "550" border = "0" cellspacing = "0" cellpadding = "0" class="outer_border"  >
                                                        <tr>
                                                                <td height="33px" class = 'table_heading' colspan = '3' align='left'>
                                                              <input type = "file" name = "file" size = '60'>
                                                        </td>
                                                        </tr>
                                                        <tr>
                                                       <td height="33px" class = 'table_heading' colspan = '3' align='right' >
                                                              <input type = 'hidden' name = 'proceed_page' value = 'proceed'>
                                                        <input type = 'hidden' name = 'hidpage' value = 'swupdate'>
                                                        <BR><!--<input class = "input1" name = "action" type = "submit" value = "Update File" onclick = 'validate_sw_update_file();' disabled>-->
                                                                                                
                                                            <div><!--<span id="button-one"><button type = 'submit' name = "update" value = "update" style = 'width:83px; background-color:#ffffff; border:none; float: right;font-size: 93%;' onclick = 'validate_sw_update_file();'  title="Update"><a href = '#'  style="font-size:85%;  width: 100%;">Update File</a></button></span>-->

<button class = 'buttonClass' type="submit" name = 'update' value = 'update' onclick = 'validate_sw_update_file();' style="margin:0 0 10px 0;" >Update</button>

</div>
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
"""
