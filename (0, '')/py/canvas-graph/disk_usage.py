#!/usr/bin/python
import sys, commands, string

sys.path.append('/var/nasexe/storage/')
import storage_op
from lvm_infos import *
from functions import *

sys.path.append('/var/nasexe/python/')
import tools
from tools import nas_disks
from tools import sync

node = tools.get_ha_nodename()
sync_time = sync.get_time()

st = nas_disks.get_all_stats()
#print st
for i in st:
#	if 'used' in i.keys() and (i["type"] == "NAS" or i['type'] == "VTL"):
	if 'used' in i.keys() and (i["type"] == "NAS"):
		#print i
		#print "\n"
		cmd = 'sudo iostat /dev/'+i["vg_name"]+'/NAS-'+i["name"]+'| grep dm'
		run_cmd = commands.getstatusoutput(cmd)
		kb_read = 0
		kb_write = 0
		if(run_cmd[0] == 0):
			split_rc = run_cmd[1].split()
			kb_read = split_rc[2]
			kb_write = split_rc[3]
		#free_size = i["total_size"] - i["used"]
		
		create_file = commands.getstatusoutput("sudo touch /var/www/fs4/py/canvas-graph/disk_usage_"+i["name"])
		fou = open("/var/www/fs4/py/canvas-graph/disk_usage_"+i["name"], "rw+")
		fou.write("")
		fou.write(str(kb_read)+":"+str(kb_write))
		fou.close()

		write_query = 'mysql -uroot -pnetweb fs2data -e "insert into disk_usage (timestamp,disk_name,kb_read,kb_write,node) values (\''+str(sync_time)+'\',\''+str(i["name"])+'\',\''+str(kb_read)+'\',\''+str(kb_write)+'\',\''+str(node)+'\');"'
		write_cmd = commands.getstatusoutput(write_query)





