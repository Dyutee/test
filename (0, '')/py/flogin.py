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
<title>LogIn</title>
<link href="../css/style.css" rel="stylesheet" type="text/css" />
<link href="../css/style_new.css" rel="stylesheet" type="text/css" />
<script type="text/javascript" src="../js/jquery-1.7.min.js"></script>
<script>
$(document).ready(function(){

	$(".buttonClass").click(function(){
		$(this).removeClass("buttonClass");
		$(this).addClass("buttonClassActive");
	});

});
</script>
</head>

<body>
<div class="logInPage">
  <div class="logInWrapper">
    <div class="logo"> <img src="images/images/logo.png"/></div>
    <div class="logInContainer">
    <div class="loginbg">
      <img src="images/images/leftbg.jpg" /> </div>
      <div class="textBoxWrapper">
	<form name = "signin" id = "login" method = "POST" action = ''>
	<div class="textlabel">ENTER MASTER PASSWORD</div>
	<div class="textboxContainer">
	  <input type="password" name="username" class="password" required />
	</div>
	<div class="userAction"> <a href="login.py" class="userActionText">Back to Login Page</a> | <a href="#" class="userActionText">Contact Administrator</a> </div>
	<div class="buttonWrapper">
	  <input type="submit" value="Get Access" name="master_pass" class="buttonClass">
	</form>
	</div>
      </div>
    </div>
  </div>
</div>
</body>
</html>

"""

#except Exception as e:
#        disp_except.display_exception(e);
