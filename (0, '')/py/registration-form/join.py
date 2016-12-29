#!/usr/bin/python
import cgi, cgitb;
cgitb.enable();

print 'Content-type: text/html';
print

form = cgi.FieldStorage();

name     = form.getvalue('name');
username = form.getvalue('username');
password = form.getvalue('password');
gender   = form.getvalue('gender');

print name + '<BR>';
print username + '<BR>';
print password + '<BR>';
print gender + '<BR>';
