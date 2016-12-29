#!/usr/bin/python

import MySQLdb

# Open database connection
db = MySQLdb.connect("localhost","root","netweb","fs2" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("SELECT VERSION()")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()

#print "Database version : %s " % data

sql = """SELECT * FROM logs LIMIT 5"""
cursor.execute(sql)
results = cursor.fetchall()

for rows in results:
	print rows
	print "\n"

# disconnect from server
db.close()
