#!/usr/bin/python
import cgitb
cgitb.enable(format='text')
#cgitb.enable("t")
def func1(arg1):
    local_var = arg1 * 2
    print '<br/>'
    return func1(local_var)
    #return local_var
"""
def func2(arg2):
    local_var = arg2 + 2
    return func2(local_var)

def func3(arg3):
    local_var = arg2 / 2
    return local_var
"""
print func1(5)
