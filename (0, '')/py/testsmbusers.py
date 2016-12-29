#!/usr/bin/python
import cgitb, os;
cgitb.enable();

print 'Content-type: text/html'
print

getuser  = '';
getgroup = '';

querystring = os.environ['QUERY_STRING'];

if (querystring.find('l=') >= 0):
	getuser = querystring[querystring.find('l=') + 2:querystring.find('&grp=')];

if (querystring.find('g=') >=0):
	getgroup = querystring[querystring.find('g=') + 2:querystring.find('&usr=')];

print """
<html>
	<head>
		<script type = 'text/javascript' src = '../js/jquery-latest.js'></script>
		<script type = 'text/javascript'>
			function get_user_list(usergroup)
			{
				message = '';

				if (usergroup == 'user')
				{
					document.getElementById('id_smbusers_list').style.display = 'table';

					username = document.smbusers.smbuser.value;
					message  = 'You need to enter user name!';
					divid    = '#id_smbusers_list';
				}

				if (usergroup == 'group')
				{
					document.getElementById('id_smbgroups_list').style.display = 'table';

					username = document.smbusers.smbgroup.value;
					messsage = 'You need to enter groupname!';
					divid    = '#id_smbgroups_list';
				}

				if (username == '')
				{
					alert('Name Required!');
					return false;
				}

				username = username.replace(/\+/g, '[PLUS]');

				$.ajax(
				{
					type: 'POST',
					url: 'get_users_list.py',
					data: 'u=' + username + '&ug=' + usergroup,

					success: function(html)
					{
						$(divid).html(html);
					}
				});
			}
		</script>
	</head>
	<body>
		<form name = 'smbusers' method = 'POST'>
			<input id = 'id_smb_user'  type = 'text' name = 'smbuser' value = '""" + getuser + """' />
			<input type = 'button' name = 'butt_smbuser' value = 'Check User' onclick = 'return get_user_list("user");' />
			<div id  = 'id_smbusers_list' style = 'border: 1px solid #BDBDBD; color: gray; display: none;' onclick = 'this.style.display: none;'></div><BR><BR>

			<input type = 'text' name = 'smbgroup' value = '""" + getgroup + """' />
			<input type = 'button' name = 'butt_smbgroup' value = 'Check Group' onclick = 'return get_user_list("group");' />
			<div id  = 'id_smbgroups_list' style = 'border: 1px solid #BDBDBD; color: gray; display: none;' onclick = 'this.style.display: none;'></div>
		</form>
	</body>
</html>"""
