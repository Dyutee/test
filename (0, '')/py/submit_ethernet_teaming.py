#!/usr/bin/python
#_*_ coding: UTF-8 _*_

#enable debugging
import cgitb, commands, sys, cgi, header
cgitb.enable()

#print "Content-Type: text/html\n"

sys.path.append('/var/nasexe/')
import net_manage as net_manage_bond

if(header.form.getvalue("submit_ethernet_bond")):
	#print "submit"
        getbondcount = header.form.getvalue("bond_count")
        getbondcount = int(getbondcount)
        getbond_type = header.form.getvalue("bond_type")
        #print getbondcount
        #print getbond_type
        create_bonding=net_manage_bond.create_bond_iface(getbondcount,getbond_type)
	if(create_bonding["id"]==0):
		success="submit:yes"
	else:
		success="submit:no"
	print """<script>location.href = 'main.py?page=network&success="""+success+"""';</script>"""

if(header.form.getvalue("submit_remove")):
	#print "submit_remove"
        bond_remove=net_manage_bond.delete_all_bond_ifaces()
	print """<script>location.href = 'main.py?page=network';</script>"""

if(header.form.getvalue("submit_slave")):
	#print "submit_slave"
        getbond_list = header.form.getvalue("bond_list")
        geteth_list = header.form.getvalue("eth_list[]")
	checkString = isinstance(geteth_list, str)
        if(checkString==True):
                geteth_list = [geteth_list]
        #print getbond_list
        #print geteth_list
        add_slave_ifaces=net_manage_bond.add_slave_ifaces_to_bond(getbond_list,geteth_list)
	print """<script>location.href = 'main.py?page=network';</script>"""
