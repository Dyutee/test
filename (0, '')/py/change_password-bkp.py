#!/usr/bin/python
import cgitb, os, cgi, commands, sys, common_methods
cgitb.enable()

form = cgi.FieldStorage()

sys.path.append('../modules/');
import disp_except

sys.path.append("/var/nasexe/python/")
import tools

#change_pass_cmd = tools.change_password("Full Access","netweb","opslag")
#print change_pass_cmd

if(form.getvalue("change_password")):
	get_old_pass = form.getvalue("old_password")
	get_new_pass = form.getvalue("new_password")
	get_re_new_pass = form.getvalue("re_new_password")
	#print get_old_pass
	#print "<br/>"
	#print get_new_pass
	#print "<br/>"
	#print get_re_new_pass
	#print "<br/>"
	if((get_old_pass != None) and (get_new_pass != None)):
		if(get_new_pass == get_re_new_pass):
			change_pass_cmd = tools.change_password("Full Access",get_old_pass,get_new_pass)
			if(change_pass_cmd["id"] == 0):
				print "<div id='id_trace'>"
				print change_pass_cmd["desc"]
				print "</div>"
			else:
				print "<div id='id_trace_err'>"
				print change_pass_cmd["desc"]
				print "</div>"
	else:
		print "<div id='id_trace_err'>"
                print "Please enter all the fields!"
                print "</div>"




#print 'Content-type: text/html'
print

print """

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>...:::Opslag FS2:::...</title>
<link href="../css/style.css" rel="stylesheet" type="text/css" />

<script src="../js/jquery1.7.js"></script>
<script language = 'javascript' src = '../js/commons.js'></script>
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


</head>
<body>
<!--body wrapper srt-->
<div class="wrapper">
  <!--inside body wrapper srt-->
  <div class="body_wrapper">
    <!--top container srt-->
    <div class="top_container"><img src="../images/opslag-fs2.png" alt="OPSLAG FS2" width="230" height="61" /><br />
      <br />
    </div>
    <!--top container end-->
    <!--login container srt-->
	<div class="heading_text">Change Password</div>
    <div class="login_banner_container">
      <div class="login_banner_img"><img src="../images/login_banner.jpg" width="349" height="292" /></div>
      <div class="login_text_container">
        <div class="change_pass_inside_text_container">
		<form name = "change_password_form" id = "login" method = "POST" action = 'change_password.py'>
          <div class="user_id_row">
            <input type="password" name="old_password" class="text_box3" placeholder="Enter Old Password"/>
          </div>
          <div class="user_id_row">
            <input type="password" name="new_password" class="text_box3" placeholder="Enter New Password"/>
          </div>
          <div class="user_id_row">
            <input type="password" name="re_new_password" class="text_box3" placeholder="Re-Enter New Password"/>
          </div>
          <div class="login_btm_row">
            <input type="submit" class="login_btm" name="change_password" value="Change Pass" onclick="return validate_change_password();" />
            </div>
	    <div class="forgot_change_password_row">
           <a href="login.py"><input type="button" class="forgot_change_btm" value="Back to Login Page" /></a>
            <input type="button" class="forgot_change_btm" value="Contact Administrator" />
	   </form>
 	   </div>
        </div>
      </div>
    </div>
    <!--login container end-->
    <!--footer container srt-->
    <div class="footer_container footer_content"> Copyright 2013 Opslag FS2 all right reserved. </div>
    <!--footer container end-->
  </div>
  <!--inside body wrapper end-->
</div>
<!--body wrapper end-->
</body>
</html>
"""

#except Exception as e:
#        disp_except.display_exception(e);
