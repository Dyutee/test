#!/usr/bin/python
import cgi, cgitb, commands

cgitb.enable()

print 'Content-Type: text/html'

print 
print """"""
import MySQLdb
import tarfile

db = MySQLdb.connect("localhost","root","netweb","fs2" )
cursor = db.cursor()

sql = """SELECT * FROM logs ORDER BY sno DESC"""
cursor.execute(sql)
results = cursor.fetchall()

#-------------------------------- Writing to text file ---------------------------------#
chown_file = commands.getoutput('sudo chown www-data:www-data system_logs_file.txt')
fo = open("system_logs_file.txt", "w")
for row in results:
	print>>fo, str(row[1])+" ::::::: "+str(row[2])+" ::::::: "+str(row[3])+"\n"
fo.close()
db.close()

#------------------------------- Converting text file to tar.gz ------------------------#
chown_file = commands.getoutput('sudo chown www-data:www-data sys_logs.tar.gz')
tar = tarfile.open("sys_logs.tar.gz", "w:gz")
for name in ["system_logs_file.txt"]:
	tar.add(name)
tar.close()

print """<script>location.href='sys_logs.tar.gz';</script>"""
