#!/usr/bin/python
import cgitb, os, cgi, commands, sys, common_methods
cgitb.enable()

sys.path.append('../modules/');
import disp_except

form = cgi.FieldStorage()
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

	#print 'Content-type: text/html'
	print

	print """
	<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
	<html xmlns="http://www.w3.org/1999/xhtml">
	<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<title>LogIn</title>
	<link href="../css/style_new.css" rel="stylesheet" type="text/css" />

	</head>
	<script type="text/javascript"> 
	window.onload = function () { 
	setTimeout(function () { 
	var div = document.getElementById('outer'); 
	div.innerHTML = 'Machine is Down!';  
	}, 20000); 
	} 
	</script> 

	<body >
	<div class="logInPage">
	  <div class="logInWrapper">
	    <div class="logo"> <img src="images/images/logo.png"/></div>
	    <!--<div class="logo"> <img src="../images/final_logo.png"/></div>-->
	    <div class="logInContainer" style="background-color:#FFF;">
	    <div class="loginbg">
	      <img src="images/images/leftbg.jpg" /> </div>
	      <div class="textBoxWrapper" style="background-color:#FFF;">
		<form name = "signin" id = "login" method = "POST" action = 'signin.py'>
		<div id="outer" style="margin:100px 0 0 100px; font-size:13px;"><img id="sync-loading-ftp" style="width:20px; height:20px; vertical-align: middle;" src="../images/sync-loading.GIF" alt="clear logs" /> Shutting Down ...</div>
		<div id="text" style="display:none">Text here</div>
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

	if(form.getvalue("hid_top_val")):
		sys.path.append('/var/nasexe/python/')
                import tools
                from tools import shutdown
		status = shutdown.shutdown()
		if(status != 0):
			print """<script>parent.location.href = 'main.py?page=sd';</script>"""
	else:
		print """<script>parent.location.href = 'login.py';</script>"""
	

except Exception as e:
	disp_except.display_exception(e);
