#!/usr/bin/python
import commands, sys, os, datetime;

sys.path.append('/var/nasexe/python/');
import commons;

logstring = '';
logfile = commons.log_file;
logarray = [];
checkrrdpath = commands.getstatusoutput('ls /storage/rrd_data/rrddata/db/');

if (checkrrdpath[0] > 0):
	commands.getoutput('/etc/init.d/storage start');

createstatus = (-1, '');

fromrange = "None";
torange = "None";

fromrangets = 0;
torangets   = 0;

temperature = commons.getsystemperature();

currdatestring = datetime.datetime.now();
currdatestring = str(currdatestring);

currdate = currdatestring[:currdatestring.find(' ')];
currdate = currdate.strip();

if (float(temperature) <= 62.0):
	color = '#336666';

elif (float(temperature) > 62.0 and float(temperature) <= 70.0):
	color = '#FFB60B';

elif (float(temperature) > 70.0 and float(temperature) <= 72.0):
	color = '#FF800D';

elif (float(temperature) > 72.0):
	color = '#FF0000';

checkrrd = commands.getstatusoutput('ls /storage/rrd_data/rrddata/db/temperature.rrd');

currtimestamp = commands.getoutput('date +%s');

#creategraph = commands.getstatusoutput('/usr/bin/rrdtool graph /storage/rrd_data/rrddata/png/temperature/' + currdate + '_temperature.png "-t Temperature Chart for ' + currdate + '" "-h" "600" "-w" "1000" --x-grid MINUTE:10:HOUR:1:MINUTE:60:0:%R --slope-mode -c "GRID#000000" -c "MGRID#000000" -c "ARROW#000000" "-v degrees C" --x-grid MINUTE:10:HOUR:1:MINUTE:60:0:%R --slope-mode "DEF:temp=/storage/rrd_data/rrddata/db/temperature.rrd:temp:AVERAGE" "VDEF:max=temp,MAXIMUM" "VDEF:min=temp,MINIMUM" "LINE2:temp#336666:temp" "GPRINT:temp:MIN:  Min\: %2.1lf" "GPRINT:temp:MAX: Max\: %2.1lf" "GPRINT:temp:AVERAGE: Avg\: %4.1lf" "GPRINT:temp:LAST: Current\: %2.1lf degrees C"');
creategraph = commands.getstatusoutput('/usr/bin/rrdtool graph ../rrddata/png/temperature/temperature.png "-t Temperature Chart for ' + currdate + '" "-h" "600" "-w" "1000" --x-grid MINUTE:10:HOUR:1:MINUTE:60:0:%R --slope-mode -c "GRID#000000" -c "MGRID#000000" -c "ARROW#000000" "-v degrees C" --x-grid MINUTE:10:HOUR:1:MINUTE:60:0:%R --slope-mode "DEF:temp=/storage/rrd_data/rrddata/db/temperature.rrd:temp:AVERAGE" "VDEF:max=temp,MAXIMUM" "VDEF:min=temp,MINIMUM" "LINE2:temp#336666:temp" "GPRINT:temp:MIN:  Min\: %2.1lf" "GPRINT:temp:MAX: Max\: %2.1lf" "GPRINT:temp:AVERAGE: Avg\: %4.1lf" "GPRINT:temp:LAST: Current\: %2.1lf degrees C"');

logstring = commons.currdate + '<<>>From: /var/www/fs4/py/createrrdtemp.py<<>>' + str(creategraph);
print 'CREATE GRAPH: ' + str(creategraph);
