#!/usr/bin/python
import cgitb, os, cgi, commands, sys, common_methods
cgitb.enable()

sys.path.append('../modules/');
import disp_except

sys.path.append('/var/nasexe/python/');
import tools


import hashlib

form = cgi.FieldStorage()

if(form.getvalue("master_pass")):
	get_master_pass = form.getvalue("username")
	if(get_master_pass != None):
		encrypt_mp = encrypt_old_pass = hashlib.md5(get_master_pass.strip()).hexdigest()
		construct_str = "Master:"+encrypt_mp

		get_pwd_line = ''
		getpwd = commands.getstatusoutput('sudo grep "Master" /var/www/global_files/users_file')
		if(getpwd[0] == 0):
			get_pwd_line = getpwd[1].strip()

		else:
			print "<div id='id_trace_err'>"
	                print "No Master Password Set! Contact Administrator."
	                print "</div>"

		if(get_pwd_line == construct_str):
			change_pass = tools.change_pass_from_master()
			if(change_pass["id"] == 0):
				print "<div id='id_trace'>"
				print change_pass["desc"]
				print "</div>"
			else:
				print "<div id='id_trace_err'>"
                                print change_pass["desc"]
                                print "</div>"
			
		else:
			print "<div id='id_trace_err'>"
                        print "Wrong Master Password!"
                        print "</div>"
			
	else:
		print "<div id='id_trace_err'>"
		print "Enter Master Pasword!"
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
	<div class="heading_text">Forgot Password</div>
    <div class="login_banner_container">
      <div class="login_banner_img"><img src="../images/login_banner.jpg" width="349" height="292" /></div>
      <div class="login_text_container">
        <div class="login_inside_text_container">
		<form name = "signin" id = "login" method = "POST" action = ''>
          <div class="user_id_row">
            <input type="password" name="username" class="text_box3" placeholder="Enter Master Password"/>
          </div>
          <div class="login_btm_row">
            <input type="submit" name="master_pass" class="login_btm" value="Get Access" />
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
