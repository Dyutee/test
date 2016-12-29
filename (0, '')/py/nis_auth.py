#!/usr/bin/python
#_*_ coding: UTF-8 _*_

#enable debugging
import cgitb, os, sys, commands, string, cgi, common_methods, traceback, include_files
cgitb.enable()

get_shares = common_methods.get_shares_array()

sys.path.append('../modules/');
import disp_except;


sys.path.append('/var/nasexe/python/')
import smb
import afp
import authentication
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


try:
	# write output to log file declared in common_methods.py
        log_array = [];
        log_file = common_methods.log_file;
        logstring = '';

	sys.path.append('/var/nasexe/python/')
	import ads
	import tools
	import fs2nis
	import manage_users
		
	ha_status = tools.check_ha()
	#print ha_status
	form = cgi.FieldStorage()
	
	#print common_methods.wait_for_response;
	####### Connect to Local Server #######
	if(form.getvalue("local_action_but")):
		auth_info = {'type':'local'}
		cmd = authentication.set_auth_type(auth_info)
		if (cmd["id"] == 0):
			if(ha_status == True):
				print """<script>location.href = 'https://"""+other_node_ip+"""/fs4/py/othernodecmd.py?act=local_conf'</script>"""
			else:
				execution = 'success'
				execval = cmd["desc"]
	        #disconnect_frm_nis = fs2nis.disconnect()       ####### Disconnect from NIS Server #######
	        #disconnect_frm_ads = ads.disconnect()          ####### Disconnect from ADS Server #######
	        #if((disconnect_frm_nis["id"] == 0) and (disconnect_frm_ads["id"] == 0)):
		#	commands.getstatusoutput("sudo chmod 777 nis_connect")
	         #       nis_connect_file = open('nis_connect', 'w')      ####### open 'nis_connect' file #######
	          #      nis_connect_file.write('')                       ####### empty it #######
	           #     nis_connect_file.close()                         ####### close the file #######
		#	commands.getstatusoutput("sudo chmod 644 nis_connect")
	
		#	commands.getstatusoutput("sudo chmod 777 ads_connect")
	         #       ads_connect_file = open('ads_connect', 'w')      ####### open 'ads_connect' file #######
	          #      ads_connect_file.write('')                       ####### empty it #######
	           #     ads_connect_file.close()                         ####### close the file #######
		#	commands.getstatusoutput("sudo chmod 644 ads_connect")

		#	i=0                                                             ###############################
		#	for val in get_shares:                                          ###############################
		#		split_get_shares = string.split(val, ':')               ###############################
				#smb.unconfigure(split_get_shares[0])                    ####### Unconfigure SMB #######
				#afp.unconfigure(split_get_shares[0])                    ####### Unconfigure AFP #######
		#		i=i+1                                                   ###############################

		#	commands.getoutput('sudo rm -rf /tmp/getusers');
			#common_methods.unconfigureallshares();
		#	execution = "success"
	         #       execval = "Successfully Connected to Local Server!"
		#	ss = "Local Server Connected Successfully"

	        #else:
		#	execution = "fail"
	         #       execval = "Error connecting to Local Server!"
		#	ss = "Error Connecting Local Server"

	#	logstring = str(common_methods.now) + '||From: ' + common_methods.remote_ip + '<<>>' + str(ss);
	#	log_array.append(logstring);

		#if(form.getvalue("other")):
		#	print """<script>location.href = 'https://"""+other_node_ip+"""/fs4/py/iframe_copy_authentication.py?execution="""+execution+"""&execval="""+execval+"""'</script>"""
		#else:
		#	print """<iframe src='https://"""+other_node_ip+"""/fs4/py/nis_auth.py?other=yes&local_action_but=yes' style="width:795px; border:none; min-height: 500px; height:auto !important; height: 500px;" ></iframe>"""
	
		print """
	        <script>location.href = 'iframe_copy_authentication.py?execution="""+execution+"""&execval="""+execval+"""'</script>
	        """
	####### End #######
	
	####### Connect to Network Information Server (NIS) #######
	if(form.getvalue("nis_action_but")):
	        ip_add = form.getvalue("ip_add")
	        domain = form.getvalue("domain")
	        nis_info = {"server_ip":ip_add,"domain_name":domain}
	        #disconnect_frm_ads = ads.disconnect()                 ####### Disconnect from ADS Server #######
	        #if(disconnect_frm_ads["id"] == 0):
		#	commands.getstatusoutput("sudo chmod 777 ads_connect.py")
		#	commands.getoutput('sudo chmod 777 ads_connect');
	        #        ads_connect_file = open('ads_connect', 'w')   ########################################
	        #        ads_connect_file.write('')                    ####### Empty 'ads_connect' file #######
	        #        ads_connect_file.close()                      ########################################
		#	commands.getstatusoutput("sudo chmod 644 ads_connect.py")
	        connect_nis = fs2nis.connect(nis_info)
		if(connect_nis["id"] == 0):
			if(ha_status == True):
				print """<script>location.href = 'https://"""+other_node_ip+"""/fs4/py/othernodecmd.py?act=nis_conf&ip_add="""+str(ip_add)+"""&domain="""+domain+"""'</script>"""
			#common_methods.unconfigureallshares();
			#commands.getoutput('sudo > /etc/global.conf.include');
			#commands.getstatusoutput("sudo chmod 777 nis_connect.py")
			#commands.getoutput('sudo chmod 777 nis_connect');
	                #nis_connect_file = open('nis_connect', 'w')   ##################################################
	                #nis_connect_file.write(ip_add+' '+domain)     ####### Write values to 'nis_connect' file #######
	                #nis_connect_file.close()                      ##################################################
			#commands.getstatusoutput("sudo chmod 644 ads_connect.py")

			#i=0                                                             ###############################
			#for val in get_shares:                                          ###############################
			#	split_get_shares = string.split(val, ':')               ###############################
				#smb.unconfigure(split_get_shares[0])                    ####### Unconfigure SMB #######
				#afp.unconfigure(split_get_shares[0])                    ####### Unconfigure AFP #######
			#	i=i+1                                                   ###############################

			#commands.getoutput('sudo rm -rf /tmp/getusers');
			#delete_all_users = manage_users.delete_all_users(exclude_samba_user="no") ####### Delete all Users  #######
			#delete_all_groups = manage_users.delete_all_groups_exception()            ####### Delete all Groups #######
			execution = "success"
			execval = connect_nis['desc']
			ss = "Successfully Connected to NIS Server"
	        else:
			execution = "fail"
			execval = connect_nis['desc']
			ss = "Error Connecting to NIS server"
		
		logstring = str(common_methods.now) + '||From: ' + common_methods.remote_ip + '<<>>' + str(ss);
                log_array.append(logstring);
	
		print """
		<script>location.href = 'iframe_copy_authentication.py?execution="""+execution+"""&execval="""+execval+"""'</script>
		"""
	####### End #######
	
	####### Connect to Active Directory Server (ADS) #######
	if(form.getvalue("ads_action_but")):
	        username = form.getvalue("username")
	        password = form.getvalue("password")
	        fqn = form.getvalue("fqn")
	        dns = form.getvalue("dns")
	        ads_info={'admin_user':username,'admin_passwd':password,'domain':fqn,'dns_ip':dns}
	        #disconnect_frm_nis = fs2nis.disconnect()               ####### Disconnect from NIS Server #######
	        #if(disconnect_frm_nis["id"] == 0):
		#	commands.getstatusoutput("sudo chmod 777 nis_connect")
	        #        nis_connect_file = open('nis_connect', 'w')    ########################################
	        #        nis_connect_file.write('')                     ####### Empty 'nis_connect' file #######
	        #        nis_connect_file.close()                       ########################################
		#	commands.getstatusoutput("sudo chmod 644 nis_connect")
	        connect=ads.connect(ads_info)
	        if(connect['id']==2):
			execution = "fail"
	                execval = connect['desc']
			ss = "Error Connecting to ADS Server"
	        elif(connect['id']==0):
			if(ha_status == True):
				print """<script>location.href = 'https://"""+other_node_ip+"""/fs4/py/othernodecmd.py?act=ads_conf&username="""+str(username)+"""&password="""+password+"""&fqn="""+fqn+"""&dns="""+dns+"""'</script>"""
			#common_methods.unconfigureallshares();
			#status = commands.getstatusoutput('sudo > /etc/global.conf.include');
			#commands.getstatusoutput("sudo chmod 777 ads_connect")
	                #ads_connect_file = open('ads_connect', 'w')                     ##################################################  
	                #ads_connect_file.write(username+' '+password+' '+fqn+' '+dns)   ####### Write values to 'ads_connect' file #######
	                #ads_connect_file.close()                                        ##################################################
			#commands.getstatusoutput("sudo chmod 644 ads_connect")

			#i=0                                                             ###############################
			#for val in get_shares:                                          ###############################
			#	split_get_shares = string.split(val, ':')               ###############################
				#smb.unconfigure(split_get_shares[0])                    ####### Unconfigure SMB #######
				#afp.unconfigure(split_get_shares[0])                    ####### Unconfigure AFP #######
			#	i=i+1                                                   ###############################

			#commands.getoutput('sudo rm -rf /tmp/getusers');

			#delete_all_users = manage_users.delete_all_users(exclude_samba_user="no") ####### Delete all Users  #######
			#delete_all_groups = manage_users.delete_all_groups_exception()            ####### Delete all Groups #######
			execution = "success"
	                execval = connect['desc']
			ss = "Successfully Connected to ADS Server"
		
		logstring = str(common_methods.now) + '||From: ' + common_methods.remote_ip + '<<>>' + str(ss);
                log_array.append(logstring);

	
		#if(form.getvalue("other")):
		#	print """<script>location.href = 'https://"""+other_node_ip+"""/fs4/py/iframe_copy_authentication.py?execution="""+execution+"""&execval="""+execval+"""'</script>"""
		#else:
		#	print """<iframe src='https://"""+other_node_ip+"""/fs4/py/nis_auth.py?other=yes&ads_action_but=yes&username="""+username+"""&password="""+password+"""&fqn="""+fqn+"""&dns="""+dns+"""' style="width:795px; border:none; min-height: 500px; height:auto !important; height: 500px;" ></iframe>"""
	
		print """
	        <script>location.href = 'iframe_copy_authentication.py?execution="""+execution+"""&execval="""+execval+"""'</script>
	        """
	####### End #######

	if(form.getvalue("ldap_action_but")):
		ldapserverip 		= form.getvalue("ldapserverip")
		ldapservername 		= form.getvalue("ldapservername")
		sambaserverip 		= form.getvalue("sambaserverip")
		sambaservername 	= form.getvalue("sambaservername")
		searchbase 		= form.getvalue("searchbase")
		admindn 		= form.getvalue("admindn")
		adminpasswd 		= form.getvalue("adminpasswd")
		sambaadminuser 		= form.getvalue("sambaadminuser")
		sambaadminpasswd 	= form.getvalue("sambaadminpasswd")
		sambadomainname 	= form.getvalue("sambadomainname")
		portno 			= form.getvalue("portno")
		ssl 			= form.getvalue("ssl")
		ldapusersuffix 		= form.getvalue("ldapusersuffix")
		ldapgroupsuffix 	= form.getvalue("ldapgroupsuffix")
		ldapmachinesuffix 	= form.getvalue("ldapmachinesuffix")
		ldapidmapsuffix 	= form.getvalue("ldapidmapsuffix")
		sysdomainname 		= form.getvalue("sysdomainname")
		ldapversion 		= form.getvalue("ldapversion")
		advance_option		= form.getvalue("advance_option")
		
		if(advance_option != "on"):
			portno 			= "389" 
			ssl 			= "False"
			ldapusersuffix 		= "ou=People"
			ldapgroupsuffix 	= "ou=Groups"
			ldapmachinesuffix 	= "ou=Computers"
			ldapidmapsuffix 	= "ou=Idmap"
			ldapversion 		= "3"
			

		if((ldapserverip != None) and (ldapservername != None) and (sambaserverip != None) and (sambaservername != None) and (searchbase != None) and (admindn != None) and (adminpasswd != None) and (sambaadminuser != None) and (sambaadminpasswd != None) and (sambadomainname != None) and (portno != None) and (ssl != None) and (ldapusersuffix != None) and (ldapgroupsuffix != None) and (ldapmachinesuffix != None) and (ldapidmapsuffix != None) and (sysdomainname != None) and (ldapversion != None)):

			if(ssl.strip() == "False"):
				ssl = False
			elif(ssl.strip() == "True"):
				ssl = True
			
			ldap_info = {'ldapserverip':ldapserverip.strip(),'ldapservername':ldapservername.strip(),
				'sambaserverip':sambaserverip.strip(),'sambaservername':sambaservername.strip(),
				'searchbase':searchbase.strip(),'admindn':admindn.strip(),'adminpasswd':adminpasswd.strip(),
				'sambaadminuser':sambaadminuser.strip(),'sambaadminpasswd':sambaadminpasswd.strip(),'sambadomainname':sambadomainname.strip(),
				'portno':portno.strip(),'ssl':ssl,
				'ldapusersuffix':ldapusersuffix.strip(),'ldapgroupsuffix':ldapgroupsuffix.strip(),
				'ldapmachinesuffix':ldapmachinesuffix.strip(),'ldapidmapsuffix':ldapidmapsuffix.strip(),
				'sysdomainname':sysdomainname.strip(),'ldapversion':ldapversion.strip()}

			ldap_dict = {'type':'ldap','info':ldap_info}

			ldap_connect_cmd = authentication.set_auth_type(ldap_dict)
			if(ldap_connect_cmd["id"] == 0):
				execution = "success"
	                        execval = ldap_connect_cmd['desc']
			else:
				execution = "fail"
	                        execval = ldap_connect_cmd['desc']

		else:
			execution = "fail"
			execval = "Error: Enter all the fields!"

		print """
	        <script>location.href = 'iframe_copy_authentication.py?execution="""+execution+"""&execval="""+execval+"""'</script>
	        """



	common_methods.append_file(log_file, log_array);

except Exception as e:
        disp_except.display_exception(e);
