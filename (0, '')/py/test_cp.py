#!/usr/bin/python
#import cgi, cgitb, sys, os, commands
#cgitb.enable()
import cgitb, header, sys, common_methods, commands
cgitb.enable()
sys.path.append('/var/nasexe/python/')
import smb, commons
sys.path.append('../modules/')
import disp_except;
try:
        test_arr =[]
        read_file = open('test.txt', 'r')
        for line in read_file:
                line_count1 = line
                line_count1 = line_count1.replace('\n', '')
                test_arr.append(line_count1)
        file_txt = []
        for val in test_arr:
                print val
                filetowrite = "cp_text.txt"
                #write_file = open('cp_text.txt', 'w')

                file_txt.append(val)
                commons.write_file(filetowrite, file_txt)
	print"""<select name = "sel_nm" multiple style="width:150px;height:310px;display:"""+display_sel+"""">"""
        for val in test_arr:
                print"""
                <option value = '"""+val+"""' id="opt_id"></option>"""
        print"""
                
                </select>"""

except Exception as e:
        disp_except.display_exception(e);
