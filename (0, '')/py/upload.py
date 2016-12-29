#!/usr/bin/env python
import cgi, os, sys;
import cgitb; cgitb.enable();
import hashlib;
import datetime;

sys.path.append('../modules/');
import disp_except;

try:
	sys.path.append('/var/nasexe/python/');
	import patch;

	print 'Content-type: text/html'
	print
	#   Copyright (C) Stephen Reese http://www.rsreese.com
	#
	#   This program is free software: you can redistribute it and/or modify
	#   it under the terms of the GNU General Public License as published by
	#   the Free Software Foundation, either version 3 of the License, or
	#   (at your option) any later version.
	#
	#   This program is distributed in the hope that it will be useful,
	#   but WITHOUT ANY WARRANTY; without even the implied warranty of
	#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	#   GNU General Public License for more details.
	#
	#   You should have received a copy of the GNU General Public License
	#   along with this program.  If not, see <http://www.gnu.org/licenses/>.


	try: # Windows needs stdio set for binary mode.
		import msvcrt;
		import uuid;
		msvcrt.setmode (0, os.O_BINARY); # stdin  = 0
		msvcrt.setmode (1, os.O_BINARY); # stdout = 1

	except ImportError:
		pass;

	# Generator to buffer file chunks
	def fbuffer(f, chunk_size=10000):
		while True:
			chunk = f.read(chunk_size);

			if not chunk: break;
			yield chunk;

	form = cgi.FieldStorage();

	# A nested FieldStorage instance holds the file
	fileitem = form['file'];

	# Test if the file was uploaded
	if fileitem.filename:
		# strip leading path from file name to avoid directory traversal attacks
		fn = os.path.basename(fileitem.filename);
	  
		# Internet Explorer will attempt to provide full path for filename fix
		fn = fn.split('\\')[-1];
	 
		# This path must be writable by the web server in order to upload the file.
		path = '/tmp/';
		filepath = path + fn;

		# Open the file for writing 
		f = open(filepath , 'wb', 10000);

		h = hashlib.sha256();
		datalength = 0;

		# Read the file in chunks
		for chunk in fbuffer(fileitem.file):
			f.write(chunk);
			h.update(chunk);
			datalength += len(chunk);

		hexdigest = h.hexdigest();
		f.close();

		# Include date in filename, increment version and append hash value
		count = 0;
		tmp_fn = filepath;

		message = 'success';

	else:
		message = 'failed';

	if (message == 'success'):
		patchfile = tmp_fn[tmp_fn.rfind('/') + 1:];
		status = patch.update(patchfile);

		if (status['id'] == 0):
			print "<script>alert('Patch update SUCCESSFUL!');</script>";
			#print jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:6%; padding-top: 4%; font-family: status-bar;">Patch Update Successful!.</div>', 'Alert Dialog');

		else:
			print "<script>alert('%s');</script>" % status['desc'];
			#print jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:6%; padding-top: 4%; font-family: status-bar;">Patch Update Successful!.</div>', 'Alert Dialog');


	print "<script>location.href = 'iframe_updates.py';</script>";
except Exception as e:
	disp_except.display_exception(e);
