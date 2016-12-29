#!/usr/bin/python
#_*_ coding: UTF-8 _*_

#enable debugging
import cgitb, common_methods, os, commands, cgi
cgitb.enable()

#print "Content-Type: text/html\n"

#sessions_op.destroy();
randomNumber = cgi.escape(os.environ["REMOTE_ADDR"])
#print randomNumber
#get_logout = commands.getoutput('sudo grep "'+randomNumber+':" /tmp/.sessions/sessions.txt')
import MySQLdb
db = MySQLdb.connect("localhost","root","netweb","fs2" )
cursor = db.cursor()
query = "delete from session where remote_ip='"+randomNumber+"';"
status = cursor.execute(query)
db.commit()
db.close()
#status = commands.getstatusoutput('sudo sed -i "/^' + randomNumber + ':/d" /tmp/.sessions/sessions.txt' );

if (status == 0):
	remove_tar_file_command =commands.getoutput('sudo /var/nasexe/check_tar_file');
	commands.getoutput('sudo mv last_time.txt last.txt')

print ("<script>location.href = 'login.py';</script>")
