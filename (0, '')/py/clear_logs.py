#!/usr/bin/python
import cgitb, common_methods, commands

cgitb.enable();

clear_logs_status = commands.getstatusoutput('sudo /var/nasexe/clear_logs');

print "<script>alert('Ok! Log files cleared.');</script>";
print "<script>location.href = 'main.py?page=support';</script>";
