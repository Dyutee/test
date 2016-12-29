#!/usr/bin/python
import cgitb
cgitb.enable()

print 'Content-type: text/html'
print

print """
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <html>
                <head>
		</head>
	

	<img src = '../rrddata/png/temperature/temperature.png' alt="graph">

	</html>"""
