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

	if (session_user != ''):
		print """<script>location.href = 'main.py?page=sys'</script>""";

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
	<body onload = 'parent.document.signin.password.focus();'>
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
		<div class="heading_text">Login to Opslag Fs2</div>
	    <div class="login_banner_container">
	      <div class="login_banner_img"><img src="../images/login_banner.jpg" width="349" height="292" /></div>
	      <div class="login_text_container">
		<div class="login_inside_text_container">
			<form name = "signin" id = "login" method = "POST" action = 'signin.py'>
		  <div class="user_id_row">
		    <input type="text" name="username" onblur="if (this.value == '') {this.value='User ID'}" onfocus="if (this.value =='User ID') {this.value = ''}" class="text_box3" value="Full Access" />
		<!--<div class="text_box4">
		<select name="username">
		<option>Full Access</option>
		<option>Maintainance Access</option>
		<option>User</option>
		</select>
		</div>-->
		  </div>
		  <div class="password_row">
		    <input type="password" name="password" onblur="if (this.value == '') {this.value='Password'}" onfocus="if (this.value =='Password') {this.value = ''}" class="text_box3" value="" />
		  </div>
		  <div class="login_btm_row">
		    <input type="submit" class="login_btm" value="Login" />
		    </div>
		  <div class="forgot_change_password_row">
		   <a href="flogin.py"><input type="button" class="forgot_change_btm" value="Forgot Password" /></a>
		   <a href="change_password.py"><input type="button" class="forgot_change_btm" value="Change Password" /></a>
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

except Exception as e:
	disp_except.display_exception(e);
