#!/usr/bin/python
import cgi, os, cgitb
cgitb.enable()
print 'Content-Type: text/html'
#print 'Content-Type: text/html'
print """
<!DOCTYPE html>
<html>

<head>
<!--<script src= "http://ajax.googleapis.com/ajax/libs/angularjs/1.2.26/angular.min.js"></script>-->
<script src= "angular_js_file.js"></script>
</head>

<body>

<div ng-app="">
 
<p>Input something in the input box:</p>
<p>Name: <input type="text" ng-model="name" value="John"></p>
<p ng-bind="name"></p>

</div>

</body>
</html>
"""
