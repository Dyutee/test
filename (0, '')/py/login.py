#!/usr/bin/python
import cgitb, os, cgi, commands, sys, common_methods
cgitb.enable()

sys.path.append('../modules/');
import disp_except

try:
	#sys.path.append('/var/www/fs4/py/')
	check_ip = commands.getoutput('sudo grep "^%s:" /tmp/.sessions/sessions.txt' % common_methods.remote_ip);

	users_array = [];

	users_file = '/var/www/global_files/users_file';

	users_array = common_methods.read_file(users_file);
	users_array.sort();

	error_array = [];
	#commands.getoutput('sudo chmod 1777 /tmp/');
	os.chdir('/tmp/');

	checktmp = commands.getstatusoutput('ls .sessions');

	if (checktmp[0] > 0):
		os.mkdir('.sessions');

		fh = open('/tmp/.sessions/sessions.txt', 'a');

	querystring = os.environ["QUERY_STRING"];

	pageval = common_methods.getpageval();

	if (pageval == 'shutdown'):
		print """<script>alert('Shutdown in progress...');</script>""";

	randomNumbers = cgi.escape(os.environ["REMOTE_ADDR"])
	getline = commands.getoutput('sudo grep "' + randomNumbers + ':" /tmp/.sessions/sessions.txt')

	session_user = common_methods.get_session_user();
	#session_user_n = common_methods.get_session_user_new();

	if (session_user != ''):
		print """<script>location.href = 'main.py?page=sys'</script>""";

	#print 'Content-type: text/html'
	print

	print """
	<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
	<html xmlns="http://www.w3.org/1999/xhtml">
	<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<title>LogIn</title>
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

	<body onLoad="document.signin.password.focus()">
	<div class="logInPage">
	  <div class="logInWrapper">
	    <div class="logo"> <img src="images/images/logo.png"/></div>
	    <!--<div class="logo"> <img src="../images/final_logo.png"/></div>-->
	    <div class="logInContainer">
	    <div class="loginbg">
	      <img src="images/images/leftbg.jpg" /> </div>
	      <div class="textBoxWrapper">
		<form name = "signin" id = "login" method = "POST" action = 'signin.py'>
		<div class="textlabel">USERNAME</div>
		<div class="textboxContainer">
		  <input type="text" name="username" class="username" value="Full Access" required />
		</div>
		<div class="textlabel">PASSWORD</div>
		<div class="textboxContainer">
		  <input type="password" name="password" class="password" required />
		</div>
		<div class="userAction"> <a href="change_password.py" class="userActionText">Change Password</a> | <a href="flogin.py" class="userActionText">Forgot Password</a> </div>
		<div class="buttonWrapper">
		  <input type="submit" value="Login" name="login" class="buttonClass">
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

except Exception as e:
	disp_except.display_exception(e);
