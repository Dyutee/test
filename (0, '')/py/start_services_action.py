#!/usr/bin/python
import cgi, cgitb, commands, common_methods, sys;
cgitb.enable();

logstring = '';
logfile = common_methods.log_file;
logarray = [];

sys.path.append('/var/nasexe/python/modules/');
import disp_except;

sys.path.append('/var/nasexe/storage/');
import san_disk_funs;

form = cgi.FieldStorage();

try:
	service  = form.getvalue('service');
	checkval = form.getvalue('st');

	if (service == 'iscsi'):
		if (checkval == 'true'):
			start_iscsi = san_disk_funs.iscsi_enable(act='ENABLE');

			if (start_iscsi == True):
				print
				#print "<script>alert('Successfully enabled i-SCSI!');</script>";

			else:
				print "<script>alert('Could not enable i-SCSI!');</script>";

			logstring = str(common_methods.now) + '<<>>From: start_services_action.py<<>>' + str(start_iscsi);
			logarray.append(logstring);
			print "<script>location.href = 'iframe_start_services.py?act=iscsienb#tabs-1';</script>";

		else:
			check_targets = san_disk_funs.iscsi_list_all_tgt_att();

			if (check_targets == [{}]):
				stop_iscsi = san_disk_funs.iscsi_enable(act='DISABLE');

				if (stop_iscsi == True):
					print
					#print "<script>alert('Successfully disabled i-SCSI!');</script>";

				else:
					print "<script>alert('Could not disable i-SCSI!');</script>";

				logstring = str(common_mnethos.now) + '<<>>From: start_services_action.py<<>>' + str(stop_iscsi);
				logarray.append(logstring);

			else:
				print "<script>alert('iSCSI targets exist! Cannot disable iSCSI');</script>";

			print "<script>location.href = 'iframe_start_services.py?act=iscsi#tabs-1';</script>";

	elif (service == 'fc'):
		if (checkval == 'true'):
			start_fc = san_disk_funs.fc_enable_disable(targets = '', opp = 'ENABLE');

			if (start_fc == True):
				print

			else:
				print "<script>alert('Failed to enable FC');</script>";

			logstring = str(common_methods.now) + '<<>>From: start_services_action.py<<>>' + str(start_fc);
			logarray.append(logstring);
			print "<script>location.href = 'iframe_start_services.py?act=fcenb#tabs-2';</script>";

		else:
			stop_fc = san_disk_funs.fc_enable_disable(targets = '', opp = 'DISABLE')

			if (stop_fc == True):
				print

			logstring = str(common_methods.now) + '<<>>From: start_services_action.py<<>>' + str(stop_fc);
			logarray.append(logstring);
			print "<script>location.href = 'iframe_start_services.py?act=fc#tabs-2';</script>";

	elif (service == 'srp'):
		if (checkval == 'true'):
			start_srp = san_disk_funs.ib_enable_disable(targets = '', opp = 'ENABLE');

			if (start_srp == True):
				print

			else:
				print "<script>alert('Failed to start SRP');</script>";

			logstring = str(common_methods.now) + '<<>>From: start_services_action.py<<>>' + str(start_srp);
			logarray.append(logstring);
			print "<script>location.href = 'iframe_start_services.py?act=srpenb#tabs-3';</script>";

		else:
			stop_srp = san_disk_funs.ib_enable_disable(targets = '', opp = 'DISABLE');

			if (stop_srp == True):
				print

			else:
				print "<script>alert('Failed to stop SRP');</script>";

			logstring = str(common_methods.now) + '<<>>From: start_services_action.py<<>>' + str(stop_srp);
			logarray.append(logstring);

			print "<script>location.href = 'iframe_start_services.py?act=srp#tabs-3';</script>";

	elif (service == 'nfs'):
		#if (checkval == 'true'):

		#else:
		
		print "<script>location.href = 'iframe_start_services.py?act=nfs#tabs-4';</script>";

	common_methods.append_file(logfile, logarray);

except Exception as e:
	disp_except.display_exception(e);
