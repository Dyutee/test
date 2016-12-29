#!/usr/bin/python
import traceback, sys, common_methods
sys.path.append('../modules/')
import disp_except;

try:
     
	import cgitb, cgi, commands,  random, os, hashlib, datetime, string, time, urllib2, httplib
	cgitb.enable()

	form = cgi.FieldStorage()

	#print "Content-Type: text/html\n"

	########################
	#System login time
	########################
	#httplib.HTTPConnection.debuglevel = 1
	#request = urllib2.Request('https://192.168.0.59/fs4/py/signin.py')
	#opener = urllib2.build_opener()
	#f = opener.open(request)
	#print f
	#for x in f:
	#	print x
	curr_time = commands.getoutput('sudo date')
	system_curr_time = curr_time.replace("IST", ",")
	#print system_curr_time
	#create_file = commands.getstatusoutput('touch current_time.txt');
	#print create_file
	file_permission = commands.getstatusoutput('sudo chmod 777 current_time.txt');
	system_current_time = open('current_time.txt', 'w')
	#print system_current_time
	system_login_time = system_current_time.write('<b>Current login:</b><BR>'+system_curr_time)
	

	######
	#End
	#####

	#------------------------
	# System last login
	##################

	last_login_time = commands.getoutput('sudo date')
	system_last_login_time = last_login_time.replace("IST", ",")
	#print system_last_login_time
	
	create_last_file = commands.getstatusoutput('sudo touch last_time.txt')
	last_file_permission = commands.getstatusoutput('sudo chmod 777 last_time.txt')
	system_last_time = open('last_time.txt', 'w')
	last_login_time = system_last_time.write('<b>Last login:</b><BR>'+system_last_login_time)

		
	#----------------
	#End
	#-----------------

	#-----------------------------------------
	#Session Start Here
	#------------------------------------------

	randomNumber = cgi.escape(os.environ["REMOTE_ADDR"])
	
	username = form.getvalue("username")
	password = form.getvalue("password")
	password = hashlib.md5(password).hexdigest()

	concat_user = username + ":" + password;
	getpwd = commands.getoutput('sudo grep "'+username+'" /var/www/global_files/users_file')  
	session_time = datetime.datetime.now().replace(microsecond=0)
	#session_time = time.asctime( time.localtime(time.time()) )
	def id_generator(size=9, chars=string.ascii_uppercase + string.digits):
		 return ''.join(random.choice(chars) for x in range(size))
	
	#randomNumber = id_generator()

	session_key = 0
	# Define function to create a session.
	def create_session(username):
		session_key = randomNumber
		import MySQLdb
        	db = MySQLdb.connect("localhost","root","netweb","fs2" )
        	cursor = db.cursor() 
		select_query = "select * from session where remote_ip='"+randomNumber+"';"
		status = cursor.execute(select_query)
		db.commit()
		fetch_all = cursor.fetchone ()
                #for row in fetch_all:
                if(fetch_all == None):
                        query = "insert into session(remote_ip,username,time)values('"+str(session_key)+"','"+str(username)+"','"+str(session_time)+"');"
                #print query
                        status = cursor.execute(query)
                        db.commit()
		else:
                        get_session_ip = fetch_all[1]
			#print get_session_ip
			#print '<br/>'
			#print randomNumber
			#print '<br/>'
                        if(randomNumber == get_session_ip):

                                update_query = "update session set time='"+str(session_time)+"'where remote_ip='"+str(randomNumber)+"';"
                                #print update_query
                                update_status = cursor.execute(update_query)
                                db.commit()
        			db.close()
		#permission = commands.getoutput('sudo chmod 777 /tmp/.sessions/sessions.txt')
		#session_file = open('/tmp/.sessions/sessions.txt', 'a')
		#session_file.write(session_key+":"+username+":"+str(session_time)+"\n")
		#session_file.close()
		return session_key
	   
	if getpwd == concat_user:
		remotevars = common_methods.remote_ip + '=';

		temp = [];
		temp.append(remotevars);

		#filetowrite = '/tmp/outputvars';

		#checkline = commands.getstatusoutput('sudo grep "%s" %s' % (remotevars, filetowrite));

		#if (checkline[0] > 0):
		#	common_methods.append_file(filetowrite, temp);

		if (session_key == 0): 
			session_key = create_session(username)
		#cmd = commands.getstatusoutput('sudo scp /tmp/.sessions/sessions.txt 192.168.0.59:/tmp/.sessions/')
		#print 'CMD:'+str(cmd) 
	
		print """ <script> location.href = 'main.py?page=first' </script>""" 

	else:
		print """
			<script>
				alert('Incorrect UserID or Password!')
				location.href = 'login.py'
			</script>

		"""
except Exception as e:
        disp_except.display_exception(e);

