#!/usr/bin/python
import cgi, cgitb, sys, os
cgitb.enable()
#sys.path.append('/var/www/fs2/py/')
#import test_func
print "Content-type: text/html"
form = cgi.FieldStorage()

#if(form.getvalue("sub")):
	#	print 'test'
	#get_first = form.getvalue("one")
	#print get_first
	#get_two = form.getvalue("two")
	#get_three =form.getvalue("thre")
	#all_val = test_func.sum(get_first,get_two,get_three)
if(form.getvalue('sub_but')):
	print "test"
	#print all_val
print """
<form name = "frm" action = "" method = "post">
<table>
<tr>
 <td valign="top">
  <label>First:<font color ="#EC1F27">*</font></label>
 </td>
 <td valign="top">
  <input type name="one" value = "" maxlength="100" size="25">
 </td>
</tr>
<tr>
 <td valign="top">
  <label>Two:<font color ="#EC1F27">*</font></label>
 </td>
 <td valign="top">
  <input type = "text" name="two" value = ""maxlength="100" size="25">
 </td>
</tr>
<tr>
 <td valign="top">
  <label>Three:<font color ="#EC1F27">*</font></label>
 </td>
 <td valign="top">
  <input type name="thre" value = "" maxlength="100" size="25" >
 </td>
</tr>
<tr>
<td colspan = "2">
<input type="submit" name = "sub_but" value="submit">
</td></tr>
</table></form>"""
