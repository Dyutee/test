#!/usr/bin/python
#_*_ coding: UTF-8 _*_

#enable debugging
import cgitb, cgi, commands, re, string
#cgitb.enable()

def mem_information():
	#mem_string_kb = commands.getoutput("free|grep Mem")
	mem_string_mb = commands.getoutput("free -m|grep Mem")
	#mem_string_gb = commands.getoutput("free -g|grep Mem")
	split_mem_string = string.split(mem_string_mb)
	memory_list = {'total': split_mem_string[1], 'used': split_mem_string[2], 'free': split_mem_string[3], 'shared': split_mem_string[4], 'buffers': split_mem_string[5], 'cached': split_mem_string[6]} 
	return memory_list

def cpu_information():
	cpu_string = commands.getoutput("sensors|grep 'Core 0'")
	split_cpu_string = string.split(cpu_string)
	print split_cpu_string[2]
