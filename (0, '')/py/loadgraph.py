#!/usr/bin/python
import cgitb
cgitb.enable()

print 'Content-type: text/html'
print

print """
	<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
	<html>
		<head>
			<script type = 'text/javascript'>
				$(document).ready(function()
				{
					var div = $('#Images');
					alert('Mohan Rao M');
					setInterval(function()
					{
						div.load('get_chart.py');
					}, 1000);
				});
			</script>
		</head>
		<body>
			<div id = 'Images'>"""
import get_chart
print """
			</div>
		</body>
	</html>
"""
