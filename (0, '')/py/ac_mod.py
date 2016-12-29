#!/usr/bin/python
import sys
sys.path.append('/var/www/fs4/py/mod/')
sys.path.append('/var/www/fs4/py/mod/mod_sub/')
import mod1
import mod
import test1
#from mod import mod
#from mod import mod1
#from mod import *
import test1
#import mod.mod1  
#import mod.mod_sub
#from mod import mod_sub
#import test1
#from mod.mod_sub import test1
ac= mod.a
print ac
print 
ad= mod1.b
print ad
print 
af=mod_sub.d
print af

