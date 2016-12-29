#!/usr/bin/python
import cgitb, datetime, sys, commands, memory_information
cgitb.enable();

sys.path.append('/var/nasexe/python/');
import commons;

count = 0;
lines = 0;

currdate = datetime.datetime.now();

memorystatus = memory_information.mem_information()

#{'used': '671', 'cached': '321', 'free': '7320', 'shared': '0', 'total': '7992', 'buffers': '5'} 
total = memorystatus['total'];
used  = memorystatus['used'];
free  = memorystatus['free'];

used = float(used) / 1024;

currdatetime = currdate.strftime("%Y-%m-%d %H:%M:%S");
day  = currdatetime[:currdatetime.find(' ')];
time = currdatetime[currdatetime.find(' ') + 1:];

day  = day.strip();
time = time.strip();

memtemp = time + ':::' + str(used);

filetocreate  = '/var/www/fs4/py/memfile_' + day;
filetocreate1 = '/var/www/fs4/py/memfile_old_' + day;

commands.getstatusoutput('sudo chmod 777 %s' % filetocreate);
commands.getstatusoutput('sudo chmod 777 %s' % filetocreate1);

fh  = open(filetocreate, 'a');
fh1 = open(filetocreate1, 'a');

fh1.write(memtemp + '\n');
fh1.close();

linescount = commands.getstatusoutput('sudo wc -l %s' % filetocreate);

if (linescount[0] == 0):
        lines = linescount[1];
        lines = lines[:lines.find(' ')];
        lines = str(lines).strip();

if (int(lines) < 30):
	fh.write(memtemp + '\n');

else:
        fh = open(filetocreate, 'w');
        fh.write('');

fh.close();
