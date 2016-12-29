#!/usr/bin/python
import cgitb
cgitb.enable();

print 'Content-type: text/html'
print

print """
	<html>
		<head>
			<script type = 'text/javascript' src = '../js/commons.js'></script>
		</head>
		<body>
			<form name = 'testform'>
				<select class = 'input' style = 'width: 300px; height: 150px;' id = 'available' name = 'avail_users' multiple onclick = 'return move_users(this.form.available, this.form.granted, "1");' onkeydown = 'return get_key();'>
					<option value = 'mohan'>Mohan</option>
					<option value = 'sunny'>Sunny</option>
					<option value = 'chutputgussa'>ChutputGussa</option>
					<option value = 'nautanki'>Nautanki</option>
				</select>

				<select class = 'input' style ="width:300px; height:150px;" id = 'granted' name = 'grant_users[]' multiple onclick = "return move_users(this.form.granted, this.form.available, '2');">
				</select>
			</form>
		</body>
	</html>
"""
