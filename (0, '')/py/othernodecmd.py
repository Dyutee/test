#!/usr/bin/python
import cgitb, sys, commands, include_files, cgi
cgitb.enable()
form = cgi.FieldStorage()

sys.path.append("/var/nasexe/python")
import fs2nis
import authentication
import ads
import manage_users
import tools
from tools import db
sys_node_name = tools.get_ha_nodename()
if(sys_node_name == "node1"):
	other_node = "node2"
	this_node = "node1"
	show_tn = "Node1"
	show_on = "Node2"
else:
	other_node = "node1"
	this_node = "node22"
	show_tn = "Node2"
	show_on = "Node1"

query="select * from network_ifaces where (name='eth1' and node='"+other_node+"')"
status=db.sql_execute(query)
for x in status["output"]:
	other_node_ip = x["ip"]

query2="select * from network_ifaces where (name='eth1' and node='"+this_node+"')"
status2=db.sql_execute(query2)
for x in status2["output"]:
	this_node_ip = x["ip"]

print
if(form.getvalue("act") == "create_user"):
	username = form.getvalue("username")
	password = form.getvalue("password")
	new_user ={"user_name":username,"passwd":password,"group":"USER","sub_groups":[]}
	create_user = manage_users.create_user(new_user)
	if(create_user["id"] == 0):
		execution = "success"
                execval = create_user['desc']
	else:
		execution = "fail"
                execval = create_user['desc']	
	print """<script>location.href = 'https://"""+other_node_ip+"""/fs4/py/iframe_user_maintenance.py?execution="""+execution+"""&execval="""+execval+"""'</script>"""

if(form.getvalue("act") == "force_create_user"):
	username = form.getvalue("username")
	password = form.getvalue("password")
	new_user ={"user_name":username,"passwd":password,"group":"USER","sub_groups":[]}
	create_user = manage_users.create_user(new_user,force=True)
	if(create_user["id"] == 0):
		execution = "success"
                execval = create_user['desc']
	else:
		execution = "fail"
                execval = create_user['desc']	
	print """<script>location.href = 'https://"""+other_node_ip+"""/fs4/py/iframe_user_maintenance.py?execution="""+execution+"""&execval="""+execval+"""'</script>"""

if(form.getvalue("act") == "create_group"):
	group = form.getvalue("group")
	create_new_group = manage_users.add_group(group)
	if(create_new_group["id"] == 0):
		execution = "success"
                execval = create_new_group['desc']
	else:
		execution = "fail"
                execval = create_new_group['desc']	
	print """<script>location.href = 'https://"""+other_node_ip+"""/fs4/py/iframe_user_maintenance.py?execution="""+execution+"""&execval="""+execval+"""#tabs-2'</script>"""

if(form.getvalue("act") == "modify_user"):
	user_name = form.getvalue("user_name")
	passwd = form.getvalue("passwd")
	group = form.getvalue("group")
	sub_groups = form.getvalue("sub_groups")
	if(sub_groups == None):
		sub_groups = []
	else:
		sub_groups = sub_groups.split()
	user_info={"user_name":user_name,"passwd":passwd,"group":group,"sub_groups":sub_groups}
	if (passwd == None):
		passwd = ''
	if(passwd == ''):
		change_user_credentials = manage_users.change_credentials(user_info)
		if(change_user_credentials["id"] == 0):
			execution = "success"
			execval = change_user_credentials['desc']
		else:
			execution = "fail"
			execval = change_user_credentials['desc']	
	else:
		change_user_credentials = manage_users.change_credentials(user_info,"yes")
		if(change_user_credentials["id"] == 0):
			execution = "success"
			execval = change_user_credentials['desc']
		else:
			execution = "fail"
			execval = change_user_credentials['desc']	
	print """<script>location.href = 'https://"""+other_node_ip+"""/fs4/py/iframe_user_maintenance.py?execution="""+execution+"""&execval="""+execval+"""#tabs-4'</script>"""

if(form.getvalue("act") == "modify_group"):
	get_available_users = form.getvalue("get_available_users")
	grp_modify_str = form.getvalue("grp_modify_str")
	usr_list_modify = form.getvalue("usr_list_modify")
	grp_modify = form.getvalue("grp_modify")
	if(get_available_users != None):
		get_available_users = get_available_users.split()
	else:
		get_available_users = []
	usr_list_modify = usr_list_modify.split()
	grp_modify = grp_modify.split()

	if((get_available_users != []) or (get_available_users != '')):
		for x in get_available_users:
			delete_usr_from_grp = manage_users.del_user_from_group(grp_modify_str,x)

	if((usr_list_modify != None) or (usr_list_modify != '')):
		for n in usr_list_modify:
			add_usr_to_grp = manage_users.add_new_groups_to_user(n,grp_modify)
	print """<script>location.href = 'https://"""+other_node_ip+"""/fs4/py/iframe_user_maintenance.py#tabs-5'</script>"""

if(form.getvalue("act") == "delete_user"):
	get_user_to_delete = form.getvalue("get_user_to_delete")
	delete_usr_command = manage_users.delete_user(get_user_to_delete)
	if(delete_usr_command["id"] == 0):
		execution = "success"
		execval = delete_usr_command['desc']
	else:
		execution = "fail"
		execval = delete_usr_command['desc']	
	print """<script>location.href = 'https://"""+other_node_ip+"""/fs4/py/iframe_user_maintenance.py?execution="""+execution+"""&execval="""+execval+"""#tabs-6'</script>"""

if(form.getvalue("act") == "delete_group"):
	get_group_to_delete = form.getvalue("get_group_to_delete")
	delete_group_command = manage_users.delete_group(get_group_to_delete)
	if(delete_group_command["id"] == 0):
		execution = "success"
		execval = delete_group_command['desc']
	else:
		execution = "fail"
		execval = delete_group_command['desc']	
	print """<script>location.href = 'https://"""+other_node_ip+"""/fs4/py/iframe_user_maintenance.py?execution="""+execution+"""&execval="""+execval+"""#tabs-7'</script>"""

if(form.getvalue("act") == "ads_conf"):
	username = form.getvalue("username")
	password = form.getvalue("password")
	fqn = form.getvalue("fqn")
	dns = form.getvalue("dns")
	ads_info={'admin_user':username,'admin_passwd':password,'domain':fqn,'dns_ip':dns}
	connect=ads.connect(ads_info)
	if(connect['id']==2):
		execution = "fail"
		execval = connect['desc']
		ss = "Error Connecting to ADS Server"
	elif(connect['id']==0):
		execution = "success"
		execval = connect['desc']
		ss = "Successfully Connected to ADS Server"
	print """<script>location.href = 'https://"""+other_node_ip+"""/fs4/py/iframe_copy_authentication.py?execution="""+execution+"""&execval="""+execval+"""'</script>"""


if(form.getvalue("act") == "local_conf"):
	auth_info = {'type':'local'}
	cmd = authentication.set_auth_type(auth_info)
	if(cmd["id"] == 0):
		execution = "success"
		execval = cmd["desc"]
	else:
		execution = "fail"
		execval = cmd["desc"]
	print """<script>location.href = 'https://"""+other_node_ip+"""/fs4/py/iframe_copy_authentication.py?execution="""+execution+"""&execval="""+execval+"""'</script>"""


if(form.getvalue("act") == "nis_conf"):
	ip_add = form.getvalue("ip_add")
	domain = form.getvalue("domain")
	nis_info = {"server_ip":ip_add,"domain_name":domain}
	connect_nis = fs2nis.connect(nis_info)
	if(connect_nis["id"] == 0):
		execution = "success"
		execval = connect_nis['desc']
	else:
		execution = "fail"
		execval = connect_nis['desc']
	print """<script>location.href = 'https://"""+other_node_ip+"""/fs4/py/iframe_copy_authentication.py?execution="""+execution+"""&execval="""+execval+"""'</script>"""

if(form.getvalue("act") == "sync_users_grps"):
	sync_users_cmd = authentication.sync_user_credentials()
	if(sync_users_cmd["id"] == 0):
		execution = "success"
		execval = sync_users_cmd['desc']
	else:
		execution = "fail"
		execval = sync_users_cmd['desc']
	print """<script>location.href = 'https://"""+other_node_ip+"""/fs4/py/iframe_user_maintenance.py?execution="""+execution+"""&execval="""+execval+"""#tabs-8'</script>"""
