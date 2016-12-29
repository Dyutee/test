#!/usr/bin/python
import sys;

sys.path.append('/var/nasexe/python/');
import commons;

# add example
number1 = int(raw_input('Enter first number: '));
number2 = int(raw_input('Enter second number: '));

operator = raw_input('Enter operator: ');

result = commons.add(number1, number2, operator);

print 'In TestFunc1: ' + str(result);
#================

# array example

arr = [];
new_arr = [];

arr.append('Sunny');
arr.append('Mohan');
arr.append('Good Sanjeev');
arr.append('Rahul');

new_arr = commons.get_array_size(arr, new_arr);

print 'Old Array Values:\n';
print '-------------------\n';

for i in arr:
	print i;

print '--------------------\n';
print 'New Array Values:\n';
print '-------------------\n';

for i in new_arr:
	print i;

print '-----------------------\n';
