#!/usr/bin/python
import json, sys
sys.path.append("/var/nasexe/python/")
import smb
sharesmbdetails = smb.show('apple','node1');
print sharesmbdetails 
json_data=open('json_data')
data = json.load(json_data)
print(data)
with open('database.txt','w') as myfile:
	json.dump(sharesmbdetails,myfile)
json_data.close()
