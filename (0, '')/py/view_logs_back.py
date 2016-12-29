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

print 
print """
<html>
<title>View Logs</title>
<head>
<link href="../css/TableCSSCode.css" rel="stylesheet" type="text/css"/>
<script type="text/javascript" src="../js/virtualpaginate.js"></script>

<style>
.paginationstyle{ width:96%; position:fixed; background-color:#003366; top:0; padding:10px; border-bottom:#FFF 1px solid; margin:0 0 0 1px;}
.paginationstyle a{color:#000; font-size:12px !important; text-decoration:none; background-color:#FFF; padding:4px 7px 4px 7px; margin:0 5px 0 0;}
.paginationstyle a:hover{text-decoration:underline;}
.table_head_logs {position:fixed; width:98%; margin:30px 0 0 0;}
</style>

</head>
<body>


<div class="CSSTableGenerator">


<div id="scriptspaginate" class="paginationstyle" >
<a href="#" rel="first">First</a> <a href="#" rel="previous">Prev</a> <span class="paginateinfo" style="margin: 0 30px; color:#FFF; font-weight: bold"></span> <a href="#" rel="next">Next</a> <a href="#" rel="last">Last</a>
</div>

<div class="table_head_logs">
<table style="margin:0;">
        <tr>
        <td width="20%">Time</td>
        <td width="20%">Type</td>
        <td width="60%">Message</td>
        </tr>
</table>

</div>"""

i=1
j=0
while (i<slots):
        sql = """SELECT * FROM logs ORDER BY sno DESC LIMIT 50 OFFSET """+str(j)
        cursor.execute(sql)
        results = cursor.fetchall()


	print """<div class="virtualpage2 hidepiece">
	<table width=100% style="margin:30px 0 0 0px;">
	<tr>
	<td >Time</td>
	<td >Type</td>
	<td >Message</td>
	</tr>"""

	for rows in results:
		print """<tr>
		<td width="20%">"""+str(rows[1])+"""</td>
		<td width="20%">"""+str(rows[2])+"""</td>
		<td width="60%">"""+str(rows[3])+"""</td>
		</tr>"""

	print """</table>
	</div>"""
	i=i+1
	j=j+50



print """<script type="text/javascript">

var newscripts=new virtualpaginate({
	piececlass: "virtualpage2",
	piececontainer: 'div', //Let script know you're using "p" tags as separator (instead of default "div")
	pieces_per_page: 1,
	defaultpage: 0,
	wraparound: false,
	persist: true
})

newscripts.buildpagination(["scriptspaginate", "scriptspaginate2"])

</script>

</div>
</body>
</html>
"""
db.close()
