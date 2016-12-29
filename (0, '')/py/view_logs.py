#!/usr/bin/python
import cgi, cgitb

cgitb.enable()

print 'Content-Type: text/html'

import MySQLdb

db = MySQLdb.connect("localhost","root","netweb","fs2" )
cursor = db.cursor()

#-------------------- Count total rows -----------------#
query = """SELECT * FROM logs"""
cursor.execute(query)
get_num = cursor.rowcount
slots = get_num/50


sql = """SELECT * FROM logs ORDER BY sno DESC LIMIT 50"""
cursor.execute(sql)
results = cursor.fetchall()

#for rows in results:
#        print rows
#        print "\n"



print 
print """
<html>
<title>View Logs</title>
<head>
<link href="../css/TableCSSCode.css" rel="stylesheet" type="text/css"/>
</head>
<body>

<div class="CSSTableGenerator">"""
print get_num
print "<br/>"
print slots
print """
<table width=100%>
<tr>
<td >Time</td>
<td >Type</td>
<td >Message</td>
<td >Page</td>
<td >More Info</td>
</tr>"""

for rows in results:
	print """<tr>
	<td >"""+str(rows[1])+"""</td>
	<td >"""+str(rows[2])+"""</td>
	<td >"""+str(rows[3])+"""</td>
	<td >"""+str(rows[4])+"""</td>
	<td >"""+str(rows[5])+"""</td>
	</tr>"""

print """</table>

</div>
</body>
</html>
"""
db.close()
