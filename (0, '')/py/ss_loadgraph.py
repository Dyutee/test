#!/usr/bin/python
import cgitb
cgitb.enable()

print 'Content-type: text/html'
print

import datetime
now = datetime.datetime.now()

print """
 <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <html>
                <head>
		<script src="../js/jquery1.7.js"></script>
		</head>

		<body>


		<script>	
			$(document).ready(function() {
  var div = $('#Images');
  setInterval(function() {
    div.load('ss_get_chart.py?' + Math.random());
  }, 10000);
});
		</script>

			<div id="Images"></div>	
		</body>

	</html>

"""
