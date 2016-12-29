#!/usr/bin/python
import cgi, cgitb
cgitb.enable()

print 'Content-Type: text/html'
print

print "hello" 
print """<iframe src='http://docs.google.com/gview?url=http://www.cualidosoft.com/images/cualidosoft-brochure.pdf&embedded=true' style='width:100%; height:100%;' frameborder='0'></iframe>"""

print """<iframe src="http://docs.google.com/gview?url=http://www.cualidosoft.com/images/cualidosoft-brochure.pdf&embedded=true" style="width:100%; height:100%;" frameborder="0"></iframe>"""

