#!/usr/bin/env python
import cgi, os
import cgitb; cgitb.enable()

form = cgi.FieldStorage()
def save_uploaded_file (filen, upload_dir):
	"""This saves a file uploaded by an HTML form.
	The form_field is the name of the file input field from the form.
	For example, the following form_field would be "file_1":
	   <input name="file_1" type="file">
	The upload_dir is the directory where the file will be written.
	If no file was uploaded or if the field does not exist then
	this does nothing.
	"""
	if not form.has_key(filen): return
	fileitem = form[filen]
	print fileitem
	if not fileitem.file: return
	fout = file (os.path.join(upload_dir, fileitem.filename), 'wb')
	while 1:
		chunk = fileitem.file.read(100000)
		if not chunk: break
		fout.write (chunk)
	fout.close()
print"""Content-Type: text/html\n"""
print"""<html><body>
<form enctype="multipart/form-data" action="" method="post">
<p>File: <input type="file" name="filen"></p>
<p><input type="submit" value="Upload"></p>
</form>
</body></html>"""



