#!/usr/bin/python
import cgitb, common_methods
cgitb.enable()

a = 423;
b = 556;

c = common_methods.add(a, b, '-');

print 'In TestFunction: ' + str(c);

