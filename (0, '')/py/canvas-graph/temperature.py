#!/usr/bin/python
import sys, commands, string

sys.path.append('/var/www/fs4/py/')
import memory_information

sys.path.append('/var/nasexe/python/')
import tools
from tools import sync
from tools import ipmi

node = tools.get_ha_nodename()
sync_time = sync.get_time()

all_cpu_temp = ipmi.cpu_temp()
print all_cpu_temp

def getsystemperature(): 
        systemperature = commands.getstatusoutput('sudo sensors|grep "Core 0"');

        if (systemperature[0] == 0):
                tempstring = systemperature[1];
                temperature = tempstring[tempstring.find('Core 0:') + len('Core 0:'):tempstring.find('\xc2\xb0')];

                if (temperature.find('+') >= 0):
                        temperature = temperature.replace('+', '');

                temperature = temperature.strip();
   
                return temperature
    
        else:
                return False


status = getsystemperature()
time_temp = sync_time+":"+status+"\n"


fot = open("/var/www/fs4/py/canvas-graph/ajax_val_temperature", "rw+")
fot.write("")
fot.write(status)
fot.close()

cpu1 = open("/var/www/fs4/py/canvas-graph/cpu1", "rw+")
cpu1.write("")
cpu1.write(all_cpu_temp["CPU1"])
cpu1.close()

cpu2 = open("/var/www/fs4/py/canvas-graph/cpu2", "rw+")
cpu2.write("")
cpu2.write(all_cpu_temp["CPU2"])
cpu2.close()

#fot = open("/var/www/fs4/py/canvas-graph/data/time_temp_file", "a")
#fot.write("")
#fot.write(time_temp)
#fot.close()

#write_query = 'mysql -uroot -pnetweb fs2 -e "insert into temperature (timestamp,temp,node) values (\''+str(sync_time)+'\',\''+str(status)+'\',\''+str(node)+'\');"'
write_query = 'mysql -uroot -pnetweb fs2data -e "insert into temperature (timestamp,temp,cpu1,cpu2,node) values (\''+str(sync_time)+'\',\''+str(status)+'\',\''+str(all_cpu_temp["CPU1"])+'\',\''+str(all_cpu_temp["CPU2"])+'\',\''+str(node)+'\');"'
write_cmd = commands.getstatusoutput(write_query)

memory_info = memory_information.mem_information()
used_mem = memory_info["used"]
free_mem = memory_info["free"]

write_query = 'mysql -uroot -pnetweb fs2data -e "insert into memory_data (timestamp,used,free,node) values (\''+str(sync_time)+'\',\''+str(used_mem)+'\',\''+str(free_mem)+'\',\''+str(node)+'\');"'
write_cmd = commands.getstatusoutput(write_query)

#print status
#print used_mem
#print free_mem

commands.getstatusoutput("sudo > /var/www/fs4/py/canvas-graph/ajax_val_mem_used")
fou = open("/var/www/fs4/py/canvas-graph/ajax_val_mem_used", "rw+")
fou.write("")
fou.write(used_mem)
fou.close()

commands.getstatusoutput("sudo > /var/www/fs4/py/canvas-graph/ajax_val_mem_free")
fof = open("/var/www/fs4/py/canvas-graph/ajax_val_mem_free", "rw+")
fof.write(" ")
fof.write(free_mem)
fof.close()



