#!/usr/bin/python
import cgi,os,cgitb
cgitb.enable()
print 'Content-Type: text/html'
print
print""" 
<!DOCTYPE html>
<html>
<head>

<title>Submit Form Using AJAX and jQuery</title>
<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
<link href="css/refreshform.css" rel="stylesheet">
<script src="ajax_script.js"></script>
</head>
<body>
<!--<form name="nme" method="post" action="">-->
<div id="mainform">
<div id="form">
<div>
<label>Name :</label>
<input id="name" type="text">
<label>Password :</label>
<input id="password" type="password">
<input id="submit" type="button" value="Submit">
</div>
</div>
</div>
<!--</form>-->
</body>
</html>"""
