#!/usr/bin/python
import traceback, commands;

def display_exception(e):
	print "<script>alert('In disp_except.py');</script>";
        print e;
	chown_file = commands.getoutput('sudo chown www-data:www-data /var/www/fs4/py/temp')
	chown_file = commands.getoutput('sudo chmod 777 /var/www/fs4/py/temp')
        fh = open('/var/www/fs4/py/temp', 'w');
        fh.write(str(e));
        traceback.print_exc(file = fh);
        print "<script>parent.location.href = '/fs4/py/error.py';</script>";
        exit();

def display_exception1(e):
        print e;
        fh = open('/var/www/fs4/py/temp', 'w');
        fh.write(str(e));
        traceback.print_exc(file = fh);
        print "<script>location.href = '/fs4/py/error1.py';</script>";
        exit();

