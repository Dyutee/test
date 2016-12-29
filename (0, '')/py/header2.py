#!/usr/bin/python
#_*_ coding: UTF-8 _*_

#enable debugging
import cgitb, commands, cgi, os, datetime, string, time
cgitb.enable()

remoteip = cgi.escape(os.environ["REMOTE_ADDR"]);

form = cgi.FieldStorage()
#pageval = common_methods.getpageval();

#pge_val = common_methods.get_title(pageval)

#user_access = common_methods.get_session_user();
user_access = '';
querystring = os.environ['QUERY_STRING'];

response = '';

#if (querystring.find('&stat=') > 0):
#	response = common_methods.getsubstr(querystring, '&stat=', '&');
response = '';
print response;

#################################
#Session Start here 
#################################

##############################
#Session End
##############################
curr_date_time = datetime.datetime.now();

system_curr_time = curr_date_time.strftime('%b %d %Y / %H:%M');
	
"""
def getallinfo(element):
	#get the attributes for cpu temperature
	sensor_info_command = 'sudo /var/nasexe/sensor_info';

	allarray = [];
	allarray = commands.getoutput(sensor_info_command).split('#');

	fan_array  = [];
	core_array = [];
	cpu_array  = [];

	cpu_array  = allarray[0].split(' ');
	core_array = allarray[1].split(' ');
	fan_array  = allarray[2].split(' ');

	if (element == 'fan'):
		return fan_array;

	if (element == 'core'):
		return core_array;

	if (element == 'cpu_array'):
		return cpu_array;
"""
cpu1_temp = '10.0';
cpu2_temp = '30.9';

cpu_array = [];
#cpu_array = getallinfo('cpu_array');

#cpu1_templine = cpu_array[0];
#cpu1_temp  = cpu1_templine[cpu1_templine.find('[') + 1:cpu1_templine.find(']')].strip();

#if (len(cpu_array) > 1):
#	cpu2_templine = cpu_array[1];
#	cpu2_temp  = cpu2_templine[cpu2_templine.find('[') + 1:cpu2_templine.find(']')].strip();

#core_info_array       = explode(' ', core_array);
blink_text   = '';
blink_text   = '';
heat1_image  = '';
head2_image  = '';
blink1_begin = '';
blink1_end   = '';
blink2_begin = '';
blink2_end   = '';

alertimage = '';

if (cpu1_temp != 'NA'):
	if (float(cpu1_temp) >= 0 and float(cpu1_temp) <= 62):
		bgcolor = 'bgcolor = \'#8afb17\'';
		heat1_image = "<img src = '../images/active.png' width = '12' height = '12'/>";

	elif (float(cpu1_temp) > 62 and float(cpu1_temp) <= 70):
		bgcolor = 'bgcolor = \'#fdd017\'';
		heat1_image = '<img src = \'../images/yellow.png\' width = \'12\' height = \'12\' />';

	elif (float(cpu1_temp) > 70 and float(cpu1_temp) <= 72):
		bgcolor = 'bgcolor = \'orange\'';
		heat1_image = '<img src = \'../images/yellow.png\' width = \'12\' height = \'12\' />';

	elif (float(cpu1_temp) > 72):
		bgcolor = 'bgcolor = \'#f62817\'';
		blink1_begin = '<blink>';
		blink1_end   = '</blink>';
		heat1_image = '<img src = \'../images/inactive.png\' width = \'12\' height = \'12\' />';
		alertimage  = "<img src = '../images/On_red.gif' /><BR><B><font color = 'red'>Check the CPU temperature</font></B>";

if (cpu2_temp != 'NA'):
	if (float(cpu2_temp) >= 0 and float(cpu2_temp) <= 62):
		bgcolor1 = 'bgcolor = \'#8afb17\'';
		heat2_image = '<img src = \'../images/active.png\' width = \'12\' height = \'12\' />';

	elif (float(cpu2_temp) > 62 and float(cpu2_temp) <= 70):
		bgcolor1 = 'bgcolor = \'#fdd017\'';
		heat2_image = '<img src = \'../images/yellow.png\' width = \'12\' height = \'12\' />';

	elif (float(cpu2_temp) > 70 and float(cpu2_temp) <= 72):
		bgcolor1 = 'bgcolor = \'orange\'';
		heat2_image = '<img src = \'../images/yellow.png\' width = \'12\' height = \'12\' />';

	elif (float(cpu2_temp) > 72):
		bgcolor1 = 'bgcolor = \'#f62817\'';
		blink2_begin = '<blink>';
		blink2_end   = '</blink>';
		heat2_image = '<img src = \'../images/inactive.png\' width = \'12\' height = \'12\' />';
		alertimage  = "<img src = '../images/On_red.gif' /><BR><B><font color = 'red'>Check the CPU temperature</font></B>";


print '''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
        <head>
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
                <title>..::Tyrone Opslag FS2::..</title>
                <script language = 'javascript' src = '../js/bindevents.js'></script><!-- to display auto generated list -->
                <script language = 'javascript' src = '../js/ip_validation.js'></script><!-- to validate ip -->
                <script language = 'javascript' src = '../js/autosuggest.js'></script><!-- to display auto generated list -->
                <script language = 'javascript' src = '../js/group_autosuggest.js'></script><!-- to display auto generated list -->
                <script language = 'javascript' src = '../js/ftp_autosuggest.js'></script><!-- to display auto generated list -->
                <script language = 'javascript' src = '../js/ftp_group_autosuggest.js'></script><!-- to display auto generated list -->
                <script language = 'javascript' src = '../js/disable_forms.js'></script>
		<script language = 'javascript' src = '../js/datetimepicker.js'></script>
                <script language = 'javascript' src = '../js/jquery-latest.js'></script>
                <script language = 'javascript' src = '../js/ts_picker.js'></script>
                <script language = 'javascript' src = '../js/commons.js'></script>
                <script type="text/javascript" src="../js/flexdropdown.js"></script>
		<script type="text/javascript" src="../js/jquery.alerts.js"></script>
		<script language = 'javascript' src = '../js/jquery-tool.js'></script>
		<script language = 'javascript' src = '../js/jtip.js'></script>
                <link rel = 'shortcut icon' href = '../images/favicon.ico' />
                <link rel = 'stylesheet' type = 'text/css' href = '../css/content.css' />
                <link rel = 'stylesheet' type = 'text/css' href = '../css/design.css' />
                <link href = "../css/style.css" rel = "stylesheet" type = "text/css" />
                <link href = "../css/flexdropdown.css" rel = "stylesheet" type = "text/css" />
		<link href = "../css/jquery.alerts.css" rel = "stylesheet" type = "text/css" />
		 <link rel = 'info.gif' href = '../images/info.gif' />
		<link rel = 'stylesheet' type = 'text/css' href = '../css/jquery.tooltip.css' />
		<script language = 'javascript' src = '../js/jquery.tooltip.js'></script>
		<script type="text/javascript">
                $j = jQuery.noConflict();
                $j(document).ready(function(){
                $j("div.item").tooltip();
                });
                </script>

		<!--<link rel = 'stylesheet' type = 'text/css' href = '../css/global.css' />-->
		<!--<style type="text/css">
			div.item { width:171px; text-align:left; }
			div#item_1 { top: 0px; left: 0px; }
			div#item_2 { top: 500px; left: 0px; }
			div#item_3 {  left: 500px; }
			div#item_4 { position: absolute; top: 500px; left: 500px; }
		</style>-->

		<style type="text/css">
      
      div.item { width:100px; height:0px; background-color: #fff; text-align:center; padding-top:0px; }
      div#item_1 { top: 0px; width: 35px; height: 15px; float:left; }
      div#item_2 { top: 80px; width: 145px; height: 20px; }      
      div#item_3 { top: 80px; width: 165px; height: 20px; }            
      div#item_4 { top: 0px; width: 10px; height:26px; padding:0 162px 0 0;  }                 
      tr.spaceUnder > td{ padding-bottom: 7px;} 
    </style>

<script type = "text/javascript">
function hideMessage() {
$(document).ready(
        function(){
                $("#id_trace_err").fadeOut(2000);
                $("#id_trace").fadeOut(2000);
                }
);
}
var tim = window.setTimeout("hideMessage()", 10000);  // 10000 milliseconds = 10 seconds
</script>

<script language = 'javascript' src = '../js/jquery-latest-fade.js'></script>
        </head>
        <body class="body" onload = 'return confirm_enter_model(" ");'>
<div id = 'app_page'>
                        <table width="100%" border="0" cellspacing="0" cellpadding="0">
                                <tr>
                                        <td class="header_bg" align="center" valign="top">
                                                <table width="100%" border="0" cellspacing="0" cellpadding="0">
                                                        <tr>
                                                                <td class="header_background" valign="top" align="left">
                                                                        <table width="100%" border="0" cellspacing="0" cellpadding="0">
                                                                                <tr>
<td width="514" height="99px" align="left" valign="middle"><a href = 'main.py?page=sys'><img border = '0' src="../images/opslag_fs2_logo.png" alt="Opslag_fs2_logo" width="237" height="84" /></a>
                                                                                        </td>
                                                                                        <td width="486" align="right" valign="middle"><span class="welcometext">You are accessing as ['''+ user_access + ''']!</span></a><br />
												<a href="flogin.py" class="headingtext">Unable to login?</a><span class="separator">|</span>
                                                                                                <a href="main.py?page=chpwd" class="headingtext">Change Password</a> <span class="separator">|</span> <a href="logout.py" class="headingtext">Logout</a><BR><BR><a class = 'time_link' href = 'main.py?page=date'>
</a><br/>
<a  class = 'time_link' href ="main.py?page=date">'''+ system_curr_time +'''</a>
                                                                                        </td>
                                                                                </tr>
</table>
                                                                </td>
                                                        </tr>
                                                </table>
                                        </td>
                                </tr>
                                <tr>
                                        <td align="center" valign="top" class="menu_bg">
                                                <table width="100%" border="0" cellspacing="0" cellpadding="0">
                                                       
 <tr>
                                                                <td width="126" height="34px" align="center" valign="middle"><a href="#" class="menu_text_active topBTNTEXT" data-flexmenu="flexmenu1" data-dir: h>Basic Setup</a></td>
                                                                <td width="176" height="34px" align="center" valign="middle"><a href="#" class="menu_text topBTNTEXT" data-flexmenu="flexmenu2">Advanced Setup</a></td>
                                                                <td width="125" height="34px" align="center" valign="middle"><a href="#" class="menu_text topBTNTEXT" data-flexmenu="flexmenu3">Maintenance</a></td>
                                                                <td width="202" height="34px" align="center" valign="middle"><a href="#" class="menu_text topBTNTEXT" data-flexmenu="flexmenu4">Volume Configuration</a></td>
                                                                <td width="15" height="34px" align="center" valign="middle"><a href="#" class="menu_text topBTNTEXT" data-flexmenu="flexmenu5">Backup/Restore</a></td>
                                                                <td width="114" height="34px" align="center" valign="middle"><a href="#" class="menu_text topBTNTEXT" data-flexmenu="flexmenu6">RAID</a></td>
                                                                <td width="98"  height="34px" align="center" valign="middle"><a href="#" class="menu_text topBTNTEXT" data-flexmenu="flexmenu7">Help</a></td>
                                                        </tr>
                                                        <tr>
								<td>
                                                
                                                        <ul id="flexmenu1" class="flexdropdownmenu jqflexmenu" style="display:none;">
                                                                <li><a href="main.py?page=date" class="submenu_text">Date/Time Settings</a></li>
                                                                <li><a href="main.py?page=network" class="submenu_text">Network Settings</a></li>
                                                                <li><a href="main.py?page=nas" class="submenu_text">NAS Settings</a></li>
                                                                <li><a href="main.py?page=iscsi" class="submenu_text">iSCSI Settings</a></li>
                                                                <li><a href="main.py?page=snmp" class="submenu_text">SNMP Settings</a></li>
 <li><a href="main.py?page=smb" class="submenu_text">SMB Settings For ADS</a></li>
                                                        </ul>
                                                        <ul id="flexmenu2" class="flexdropdownmenu jqflexmenu" style="display:none;">
                                                                <li><a href="main.py?page=auth" class="submenu_text">Authentication</a></li>
                                                                <li><a href="main.py?page=infini" class="submenu_text">Infiniband Settings</a></li>
                                                                <li><a href="main.py?page=fc" class="submenu_text">FC Settings</a></li>
                                                                <li><a href="main.py?page=srp" class="submenu_text">SRP Settings</a></li>
                                                        </ul>
                                                        <ul id="flexmenu3" class="flexdropdownmenu jqflexmenu" style="display:none;">
                                                                <li><a href="main.py?page=sd" class="submenu_text">Shutdown</a></li>
                                                                <li><a href="main.py?page=logs" class="submenu_text">Logs</a></li>
                                                                <li><a href="main.py?page=fs2" class="submenu_text">FS2 Backup/Restore</a></li>
                                                                <li><a href="main.py?page=conn" class="submenu_text">Connections</a></li>
                                                                <li><a href="main.py?page=ss" class="submenu_text">Snapshot</a></li>
                                                                <li><a href="main.py?page=mu" class="submenu_text">Manage Users</a></li>
                                                                <li><a href="main.py?page=updts" class="submenu_text">Updates</a></li>
                                                                <li><a href="main.py?page=st" class="submenu_text">Scheduled Tasks</a></li>
								<li><a href="main.py?page=gr" class="submenu_text">FS2 Data Analysis</a></li>
								<!--<li><a href="main.py?page=tgr" class="submenu_text">Test Graphs</a></li>-->
                                                                <li><a href="main.py?page=scan" class="submenu_text">Scan Volume</a></li>
								<li><a href="main.py?page=re_mount" class="submenu_text">Remount</a></li>
                                                        </ul>
                                                        <ul id="flexmenu4" class="flexdropdownmenu jqflexmenu" style="display:none;">
                                                                <li><a href="main.py?page=nd" class="submenu_text">NAS Disk Configuration</a></li>
                                                                <li><a href="main.py?page=bd" class="submenu_text">Block Disk Configuration</a></li>
                                                        </ul>
                                                        <ul id="flexmenu5" class="flexdropdownmenu jqflexmenu" style="display:none;">
                                                                <li><a href="main.py?page=bckp" class="submenu_text">Backup</a></li>
                                                        </ul>
                                                        <ul id="flexmenu6" class="flexdropdownmenu jqflexmenu" style="display:none;">
                                                                <li><a href="main.py?page=rs" class="submenu_text">RAID Settings</a></li>
                                                        </ul>
                                                        <ul id="flexmenu7" class="flexdropdownmenu jqflexmenu" style="display:none;">
                                                                <li><a href="main.py?page=sys" class="submenu_text">System Status</a></li>
                                                                <li><a href="show_opslag_doc.py" target = 'new' class="submenu_text">FS2 Help</a></li>
                                                                <li><a href="#" class="submenu_text">SSL Certificate</a></li>
                                                                <li><a href="http://www.tyronesystems.com/fs2.html" target = 'new' class="submenu_text">About OpslagFS2</a></li>
                                                                <li><a href="main.py?page=support" class="submenu_text">Support</a></li>
                                                        </ul>
                                                </td></tr>
                                                </table>
                                        </td>
                                </tr>
                                <tr>
                                </tr>
                                <tr>
                                        <td align="center" valign="top" bgcolor="#eae9e9">
<table width = "100%" border = "0" cellspacing = "0" cellpadding = "0" bgcolor = "#f9f9f9">
<tr>
                                                                <td height = "40px" class = "hierarchyarrow" valign = "middle" align = "left" width = '33%'>
                                                                        
                                                                        <a href = "#" class = "hierarchy">  </td>
                                                                <td width = '33%' align = 'center'></td>
                                                                <td width = '33%'>
                                                                </td>
                                                                <td align = 'center' nowrap>
                                                                        <B>CPU1</B>

<br><sup>o</sup> C<BR></td>


<td valign = 'middle' style = 'border: 1px solid;'>
                                                                </td>
                                                                <td align = 'center' nowrap>
                                                                 <B>CPU2</B>

<br><sup>o</sup> C<BR></td>
                                                        </tr>
                                                        <tr>
                                                                <td colspan = "3" height = "40px" class = "hierarchyarrow" valign = "middle" align = "center">'''

#if (result != '' and response != ''):
#	print '''<div id = 'id_result' style = 'border: 1px solid orange; color: #888888; margin-top: 1%; background: #FFDDCC; width: 40%; text-align: justify; font: 14px Arial; font-weight: bold; -moz-border-radius: 5px; border-radius: 5px;'><a class = 'share_link' href = '#' onclick = 'document.getElementById("id_result").style.display = "none";'><img border = '0' src = '../images/closewin.png' style = 'margin-top: 6px; margin-bottom: 1px;' /></a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;''' + result + '''<BR></div>'''

print '''                                                                </td>
                                                        </tr>
                                                </table>                                                '''
