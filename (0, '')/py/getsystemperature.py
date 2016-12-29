#!/usr/bin/python
import cgitb, datetime, sys, commands, time
cgitb.enable();

sys.path.append('/var/nasexe/python/');
import commons;

count = 0;
lines = 0;

#while count <= 10:
currdate = datetime.datetime.now();
systemperature = commons.getsystemperature();

#currdatetime = currdate.strftime("%Y-%m-%d %H:%M:%S");
currdatetime = currdate.strftime("%Y-%m-%d %H:%M");

#checkts = datetime.datetime.strptime(currdatetime, '%Y-%m-%d %H:%M:%S');
#currtimestamp = time.mktime(checkts.timetuple());

#currtimestamp = str(currtimestamp);
#currtimestamp = currtimestamp[:currtimestamp.find('.')];

day  = currdatetime[:currdatetime.find(' ')];
time = currdatetime[currdatetime.find(' ') + 1:];

day  = day.strip();
time = time.strip();

#timetemp = currtimestamp + ':::' + str(systemperature);
timetemp = time + ':::' + str(systemperature);

filetocreate  = '/var/www/fs4/py/tempfile_' + day;
filetocreate1 = '/var/www/fs4/py/tempfile_old_' + day;

linescount = commands.getstatusoutput('sudo wc -l %s' % filetocreate);

commands.getstatusoutput('sudo chmod 777 %s' % filetocreate);
commands.getstatusoutput('sudo chmod 777 %s' % filetocreate1);

fh  = open(filetocreate, 'a');
fh1 = open(filetocreate1, 'a');

fh1.write(timetemp + '\n');
fh1.close();

if (linescount[0] == 0):
	lines = linescount[1];
	lines = lines[:lines.find(' ')];
	lines = str(lines).strip();

if (int(lines) < 5):
	fh.write(timetemp + '\n');

else:
	fh = open(filetocreate, 'w');
	fh.write('');

fh.close();
