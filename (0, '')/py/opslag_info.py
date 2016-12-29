#!/usr/bin/python
import commands;

oss          = commands.getoutput('sudo grep "Operating Sytem" /var/nasconf/OS-INFO');
version      = commands.getoutput('sudo grep "Version-Id" /var/nasconf/OS-INFO');
build        = commands.getoutput('sudo grep "Build-Id" /var/nasconf/OS-INFO');
license      = commands.getoutput('sudo grep "Licence Build Model 1" /var/nasconf/OS-INFO');
license_type = commands.getoutput('sudo grep "License=" /var/nasconf/OS-INFO');
serial       = commands.getoutput('sudo grep "SERIAL NO" /var/nasconf/OS-INFO');
model        = commands.getoutput('sudo grep "^MODEL" /var/nasconf/OS-INFO');
disp_date    = commands.getoutput('sudo grep "^DISPATCH" /var/nasconf/OS-INFO');

ltarray = [];

getparam = '';

def getos(param):
	if (param == 'oss'):
		if (oss != ''):
			os_array = oss.split('=');
			getparam = os_array[1].strip();

	if (param == 'version'):
		if (version != ''):
			version_array = version.split('=');
			getparam      = version_array[1].strip().upper();

	if (param == 'build'):
		if (build != ''):
			build_array = build.split('=');
			getparam    = build_array[1].strip().upper();

	if (param == 'license'):
		if (license != ''):
			license_array = license.split('=');
			getparam      = license_array[1].strip().upper();

	if (param == 'ltype'):
		if (license_type != ''):
			ltarray  = license_type.split('=');
			getparam = ltarray[1].strip().upper();

	if (param == 'serial'):
		if (serial != ''):
			serial_array = serial.split('=');
			getparam     = serial_array[1].strip().upper();

	if (param == 'model'):
		if (model != ''):
			model_array = model.split('=');
			getparam    = model_array[1].strip().upper();

	if (param == 'disp_date'):
		if (disp_date != ''):
			dispdate_array = disp_date.split('=');
			getparam       = dispdate_array[1].strip().upper();

	return getparam;
