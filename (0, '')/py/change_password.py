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
	                print "Passwords do not match!"
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
<title>LogIn</title>
<link href="../css/style.css" rel="stylesheet" type="text/css" />
<link href="../css/style_new.css" rel="stylesheet" type="text/css" />
<script language = 'javascript' src = '../js/commons.js'></script>
<script type="text/javascript" src="../js/jquery-1.7.min.js"></script>
<script>
$(document).ready(function(){

	$(".buttonClass").click(function(){
		$(this).removeClass("buttonClass");
		$(this).addClass("buttonClassActive");
	});

});
</script>
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
<div class="logInPage">
  <div class="logInWrapper">
    <div class="logo"> <img src="images/images/logo.png"/></div>
    <div class="logInContainer">
    <div class="loginbg">
      <img src="images/images/leftbg.jpg" height="302px" /> </div>
      <div class="textBoxWrapper">
	<form name = "change_password_form" id = "login" method = "POST" action = 'change_password.py'>
	<div class="textlabel">ENTER OLD PASSWORD</div>
	<div class="textboxContainer">
	  <input type="password" name="old_password" class="password" required />
	</div>
	<div class="textlabel">ENTER NEW PASSWORD</div>
	<div class="textboxContainer">
	  <input type="password" name="new_password" class="password" required />
	</div>
	<div class="textlabel">RE-ENTER NEW PASSWORD</div>
	<div class="textboxContainer">
	  <input type="password" name="re_new_password" class="password" required />
	</div>
	<div class="userAction"> <a href="login.py" class="userActionText">Back to Login Page</a> | <a href="#" class="userActionText">Contact Administrator</a> </div>
	<div class="buttonWrapper">
	  <input type="submit" value="Change Password" name="change_password" class="buttonClass2" onclick="return validate_change_password();" />
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
