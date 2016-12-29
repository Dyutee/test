#!/usr/bin/python
#_*_ coding: UTF-8 _*_

#enable debugging
import cgi, cgitb, header, os, sys, commands, common_methods

image_icon = common_methods.getimageicon();
sys.path.append('../modules/');
import disp_except;

cgitb.enable();

try:
	filetodownload = '../downloads/BUG-REPORT*';

	linktext = '';

	farray     = [];
	linksarray = [];

	files = commands.getstatusoutput('sudo ls -t %s' % filetodownload);

	if (files[0] == 0):
		farray = files[1].split('\n');

		for files in farray:
			filename = files[files.rfind('/') + 1:];

			checkfile = commands.getstatusoutput('sudo ls ../downloads/BUG-REPORT*.tar.bz2');

			if (checkfile[0] > 0):
				zipstatus = commands.getstatusoutput('sudo tar -jcf %s.tar.bz2 %s' % (filename, files));
				
				if (zipstatus[0] == 0):
					remstatus = commands.getstatusoutput('sudo rm -r ../downloads/BUG-REPORT*');
			
					if (remstatus[0] == 0):
						mvstatus = commands.getstatusoutput('sudo mv BUG-REPORT*.bz2 ../downloads/');

			dispname = filename.replace(':', '\:');
			filename = filename.strip();
			linktext = '<a class = "share_link" href = "../downloads/' + dispname + '.tar.bz2">' + filename + '.tar.bz2</a>';
			linktext = linktext.replace('.tar.bz2.tar.bz2', '.tar.bz2');

			linksarray.append(linktext);
			
	linktext = linktext[:linktext.rfind('||')];
	linktext = linktext.strip();

	print """
							<table width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#f9f9f9">
								<tr>
									<td height="450px" valign="top" align="center">

	   
	 <center><?= $wait_for_response ?></center>
				<form  name = 'get_support' method = "POST">
				<table border = "0" cellspacing = "0" cellpadding = "0" align = 'center' width = '50%'>
				      <tr>
					<td height = "33px" width = "8" align = "left">
						<img src = "../images/rightside_left.jpg" width = "8" height = "33" />
					</td>
					<td width = "550" height = "33px" align = "left" valign = "middle" class = "right_bg rightsidemenuheading">
			<div id="item_2" class="item" style="width:15%;">         
                        """+image_icon+""" Support
                        <div class="tooltip_description" style="display:none" title="Support Information">
                                <span>This gives information about the resources that are being used by the system.</span><br/><br/>
                                <table border="0">
                                <tr class="spaceUnder">
                                <td valign="top" align="left"><strong style="color:#b2b2b2; padding:0px 2px 0px 2px;">FS2 documnet:</strong></td>
                                <td>Download the Pdf document of Fs2</td>
                                </tr>
				 <tr class="spaceUnder">
                                <td valign="top" align="left"><strong style="color:#b2b2b2; padding:0px 2px 0px 2px;">Fs2 Logs:</strong></td>
                                <td>Download the Logs of Fs2</td>
                                </tr>

                                </table>
                                </div></div>

				       </td>
					<td height = "33px" width = "8" align = "right">
						<img src = "../images/rightside_right.jpg" />
					</td>
				</tr>
					    <tr>
					<td colspan = "3" align = "left" valign = "top">
						<table width = "100%" border = "0" cellspacing = "0" cellpadding = "0" class="outer_border"  bgcolor = "#f5f5f5">
							<tr>
								<td height="33px" class = 'table_heading' colspan = '3' align='left'>
									Click on the image to get the OpslagFS2 support doc, or <BR>Right click on the image and click 'Save Link As' to get OpslagFS2 support doc.
								</td>
								<td align = 'right'>
									<!--<img onclick = "location.href = '../downloads/Opslag Manual.pdf';" src = '../images/pdf_logo.png' />-->
									<a target = 'new' href = '../downloads/Opslag Manual.pdf'><img src = '../images/pdf_logo.png' /></a>
									<!--<input type = 'button' name = 'download' src = '../images/pdf_logo.png' onclick = 'return get_docs();'>-->
								</td>
							</tr>
					       </table>
					 </td>
					  </tr></table></form> """
	   
	if (len(linksarray) > 0):
		print common_methods.wait_for_response;
		print """                        <form  name = 'delete_bugs' method = "POST">
				<BR><BR><table border = "0" cellspacing = "0" cellpadding = "0" align = 'center' width = '50%' class = 'outer_border'>
				      <tr>
					<td height = "33px" width = "8" align = "left">
						<img src = "../images/rightside_left.jpg" width = "8" height = "33" />
					</td>
					<td width = "550" height = "33px" align = "left" valign = "middle" class = "right_bg rightsidemenuheading">
							<?= $image_icon ?>
							Get Bug Report File
				       </td>
					<td height = "33px" width = "8" align = "right">
						<img src = "../images/rightside_right.jpg" />
					</td>
				</tr>
					    <tr>
					<td colspan = "3" align = "left" valign = "top">
						<table width = "100%" border = "0" cellspacing = "0" cellpadding = "0" class="outer_border"  bgcolor = "#f5f5f5">
							<tr>
								<td class = 'table_heading'>
									<input type = 'checkbox' id = 'id_select_all_bugs' onclick = 'return select_all_entries(document.getElementById("id_select_all_bugs"), document.delete_bugs.elements["bugsreps[]"], document.getElementById("id_bugrep"));'>
								</td>
								<td class = 'table_heading'>
									File name
								</td>
	"""
		for i in linksarray:
			filetodelete = i[i.find('>') + 1:i.rfind('<')];
			print """
							<tr>
								<td>
									<input id = 'id_bugrep' name = 'bugsreps[]' type = 'checkbox' value = '""" + filetodelete + """'>
								</td>
							      <td height="33px" class = 'table_heading' colspan = '3' align='left'>"""
			print i
			print """                                                        </td>
							</tr>"""
		print """						<tr>
								<td colspan = '2' align = 'right'>
									<div><span id="button-one"><button type = 'button' name = 'dload' onclick = 'return validate_delentries(document.delete_bugs.elements["bugsreps[]"], document.getElementById("id_bugrep"), "");' style = 'background-color:#FFFFFF;border:none; float:right;  font-size: 86%; ' title="Delete Selected"><a style="font-size:86%;"  >Delete Selected</a></button></span></div>
		</div>
								</td>
							</tr>
					       </table>
					 </td>
					 </tr></table></form> """

	filetodownload = '/var/www/fs4/downloads/';

	linktext = '';

	farray     = [];
	linksarray = [];

	files = commands.getstatusoutput('sudo ls -t %s' % filetodownload);
	target = '';

	if (files[0] == 0):
		farray = files[1].split('\n');

		for files in farray:
			filename = files[files.rfind('/') + 1:];

			filename = filename.strip();

			checkfile = os.path.isdir('/var/www/fs4/downloads/' + filename);

			if (checkfile == False):
				if (filename != '' and filename.find('BUG-REPORT') < 0):
					tarext = filename.find('.tar.');

					if (tarext < 0):
						target = 'target = "new"';

					linktext = '<a ' + target + ' class = "share_link" href = "../downloads/' + filename + '">' + filename + '</a>';

					linksarray.append(linktext);
			
	linktext = linktext[:linktext.rfind('||')];
	linktext = linktext.strip();

	if (len(linksarray) > 0):
		print common_methods.wait_for_response;
		print """                        <form  name = 'delete_files' method = "POST">
				<BR><BR><table border = "0" cellspacing = "0" cellpadding = "0" align = 'center' width = '50%'>
				      <tr>
					<td height = "33px" width = "8" align = "left">
						<img src = "../images/rightside_left.jpg" width = "8" height = "33" />
					</td>
					<td width = "550" height = "33px" align = "left" valign = "middle" class = "right_bg rightsidemenuheading">
							<?= $image_icon ?>
							Download Files
				       </td>
					<td height = "33px" width = "8" align = "right">
						<img src = "../images/rightside_right.jpg" />
					</td>
				</tr>
					    <tr>
					<td colspan = "3" align = "left" valign = "top">
						<table width = "100%" border = "1" cellspacing = "0" cellpadding = "0" class="border"  bgcolor = "#f5f5f5">
							<tr>
								<td class = 'table_heading'>
									<input type = 'checkbox' id = 'id_select_all_files' onclick = 'return select_all_entries(document.getElementById("id_select_all_files"), document.delete_files.elements["files[]"], document.getElementById("id_file"));'>
								</td>
								<td class = 'table_heading'>
									File name
								</td>
							</tr>
	"""
		for i in linksarray:
			filetodelete = i[i.find('>') + 1:i.rfind('<')];
			print """
							<tr>
								<td width = '4%'>
									<input id = 'id_file' name = 'files[]' type = 'checkbox' value = '""" + filetodelete + """'>
								</td>
							      <td height="33px" class = 'table_heading' colspan = '3' align='left'>"""
			print i
			print """                                                        </td>
							</tr>"""
		print """		       </table>"""
		print """				<table width = '100%' align = 'center' border = '0'>
								<tr>
								<td colspan = '2' align = 'right'>
									<div><span id="button-one"><button type = 'button' name = 'dload' onclick = 'return validate_delentries(document.delete_files.elements["files[]"], document.getElementById("id_file"), "oth");' style = 'background-color:#FFFFFF;border:none; float:right;  font-size: 86%; ' title="Delete Selected"><a style="font-size:86%;"  >Delete Selected</a></button></span></div>
		</div>
								</td>
							</tr>
						</table>
					 </td>
					 </tr></table></form> 

	"""

except Exception as e:
	disp_except.display_exception(e);
