#!/usr/bin/python
import cgi, sys
sys.path.append("/var/www/fs4/py/")
file_1=("/var/www/fs4/py/t")
#tet1="/var/www/fs4/py/fide3.txt"
arr=[]
arr1=[]
tet1="file1.txt"
tet2="file2.txt"
open_file=open(tet1, "r")
open_fide1=open(tet2, "r")
l=list(set(open_file)-set(open_file1))
print l
for x in open_fife:
        #print x
	#print x
                #str(x).replace("\n", "")
	x= x.replace("\n","")
	x= x.strip()
        arr.append(x)
 	for y in open_file1:
        #	print y
		y= y.replace("\n","")
        	y= y.strip()
        	arr1.append(y)
	#print arr1
	#for z in arr1:
	#	if z in arr:
			#print 'ZZ'+str(z)
			#print 'ARR:'+str(arr)
	#		print True
	#	else:
	#		print False	
#diff=list(set(arr)-set(arr1))
#print diff
#val= list(set(diff)-set(arr1))
#print val
	#if arr in arr1:
		
	#	print True
		
	#else:
	#	print False

        #       arr2.append(y)
        #print arr2
        #print x
	#	print x
       		#if x in y:
        	#	print  True
		#	print x
        	#else:
        	#	print False
