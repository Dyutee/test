#!/usr/bin/python
import cgitb, os, sys, cgi, include_files
cgitb.enable()

#import left_nav
sys.path.append('/var/nasexe/python/')
import tools
from tools import db
#from tools import 

check_ha = tools.check_ha()

form = cgi.FieldStorage()
sys_node_name = tools.get_ha_nodename()
if(sys_node_name == "node1"):
	other_node = "node2"
	show_tn = "Node1"
	show_on = "Node2"
else:
	other_node = "node1"
	show_tn = "Node2"
	show_on = "Node1"

query="select * from network_ifaces where (name='eth1' and node='"+other_node+"')"
status=db.sql_execute(query)
for x in status["output"]:
	other_node_ip = x["ip"]

if(form.getvalue("down_pdf")):
	print "Content-Type: application/pdf"
	print "Content-Disposition: attachment; Tyronemanual.pdf"
	#print "<script>location.href='../images/Tyronemanual.pdf';</script>"

print
print """

      <!--Right side body content starts from here-->
      <div class="rightsidecontainer" style="width:740px;">
        <!--<div class="insidepage-heading">Help >> <span class="content">Help Information</span></div>-->
        <!--tab srt-->
        <div class="searchresult-container">
	<div style="margin:0 0 0px 0;" class="topinputwrap-heading"><a class="demo" href ="#"><img src ="../images/help_icon1.png" style="width:13px;"><span class="tooltip" >
        <div class="text_css">On this page you can find the support options and documentation for your FS2 system.</div>"""
if(check_ha == True):
	print"""
</span></a> Support Information ("""+show_tn+""")
	<span style="float:right; margin:0px 0px 0 0;"><a onclick="return onclick_loader();" class="resource_links" href="https://"""+other_node_ip+"""/fs4/py/support_nw.py">"""+show_on+"""</a></span>

	</div>"""
else:
	print""" </span></a><p class = "gap_text">Support Information</p></div>"""
print"""
          <div class="infoheader">

            <div id="tabs">
              <ul>
                <li><a href="#tabs-1">Support</a></li>
                <li><a href="#tabs-2">FS2 Help</a></li>
                <li><a href="#tabs-3">About FS2</a></li>
		<li style="display:none;"><a href="#tabs-4">SSL Certificate</a></li>
              </ul>
	      <div id="tabs-1">
        <!--form container starts here-->
        <div class="form-container">
          <div class="topinputwrap-heading">Support Information</div>
          <div class="inputwrap">
	 <div class="formleftside-content">

<p style="width:650px; text-align:justify; margin:0 0 10px 0;">Tyrone's dependable and customer-oriented after-sales support, christened Tyrone Care, is one of our biggest differentiators. As part of Tyrone Care, we extend the promise to be at your service for all maintenance and troubleshooting activities. </p>

<p style="width:650px; text-align:justify; margin:0 0 10px 0;">Tyrone Care offers basic warranty for all parts and a limited on-site warranty service. We also provide you the option to avail extended warranty services. You can also opt for our premier Gold Support plan that offers 24x7 support throughout the week with a response time of 4 hours.</p>

<p style="width:650px; text-align:justify; margin:0 0 10px 0;">The basic Warranty for Tyrone product is 36 / 24 Months Parts and Limited On-site Warranty Service. Warranty Terms & Conditions are contained in the accompanying Express Server Warranty document. Please take a moment to read through the Warranty Terms & Conditions.</p>

<style>
table { margin: 0 1em 1em 0; border-collapse: collapse; }
td, th { padding: .3em; border: 1px #ccc solid; }
td { text-align:left;}

a.inner{background:#ccc; padding:5px; border:#ccc 1px solid;}
a.inner:hover{border:#ccc 1px solid; background:#FFF;}
a.mail:hover{text-decoration:underline;}
</style>

<p style="width:650px; text-align:justify; margin:0 0 10px 0;"> If you need help regarding How to create Share, Set SMB settings etc. you can visit our <a class="inner" href="http://203.122.29.236/wiki/FAQ" target="_blank">FAQ page</a></p>

<div style="background:#ccc; padding:.3em; width:391px; font-weight:bold;">For Technical Support</div>
<table width="400px;">
<tr>
<td>Email</td>
<td><a class="mail" href="mailto:support@netwebindia.com">support@netwebindia.com</a></td>
</tr>
<tr>
<td>TeleFax</td>
<td>+91-11-43240000 / 29942258 / 29942297</td>
</tr>
</table>

	</div>
          </div>
        </div>
        <!--form container ends here-->
	<p>&nbsp;</p>
              </div>

              <div id="tabs-2">
	<div class="form-container">
	      <div class="topinputwrap-heading">FS2 help Information </div>
          <div class="inputwrap">
         <div class="formleftside-content">
	<form name="download" method="post" action="Tyronemanual.pdf" target="_blank">
	<!--<button name="down_pdf" value="down_pdf" type="submit" style="width:200px; padding:5px 7px 5px 7px; cursor:pointer; background:#D8D8D8; margin:0 0 10px 0;">View Documentation</button>-->
	<button class="buttonClass" type = 'submit'  name="down_pdf" value="down_pdf" style="width:150px; margin:0 0 20px 0;">View Documentation</button>
	</form>
	<form name="download" method="post" action="../images/Tyronemanual.pdf.zip">
	<!--<button name="down_pdf" value="down_pdf" type="submit" style="width:200px; padding:5px 7px 5px 7px; cursor:pointer; background:#D8D8D8; margin:0 0 20px 0;">Download Documentation</button>-->
	</form>

        </div>
          </div>



</div>

	<!--form container starts here-->
        <!--form container ends here-->
	<p>&nbsp;</p>
              </div>
                      <div id="tabs-3">
		<div class="form-container">

		 <div class="topinputwrap-heading">About FS2 </div>
          <div class="inputwrap">
         <div class="formleftside-content" style="overflow: auto; width:700px; height: 340px;">
<p style="width:650px; text-align:justify; margin:0 0 10px 0;">The era of having multiple units for different storage needs is passing as diverse storage products prevent optimum utilization and can be difficult to manage. Opslag FS2 series from Tyrone Systems, consolidates all your storage requirements in a single all-in-one storage solution which is the most flexible solution around. Apart from offering flexibility, it bundles enterprise class features such as extremely high scalability and redundancy along with a very high performance. It can serve the diverse requirements from high performance computing to post-production and broadcast industry.</p>

<p style="margin:0 0 5px 0; width:650px; font-weight:bold;">Flexible Scalability</p>
<p style="width:650px; text-align:justify; margin:0 0 10px 0;">Flexible data protection and redundancy Opslag FS2 is a highly scalable solution offering storage capacity starting from 8TB to well over 1 PetaByte. Storage capacity can be easily enhanced by adding JBOD units to primary storage. For customers requiring performance scaling along with capacity scaling, multiple FS2 units can be clustered together.</p>

<p style="margin:0 0 5px 0; width:650px; font-weight:bold;">Flexible data protection and redundancy</p>
<p style="width:650px; text-align:justify; margin:0 0 10px 0;">All Opslag FS2 solutions offer high level of redundant and data protection. All the systems support various RAID levels (0, 1, 0+1, 5, 6, 50 & 60) for protection against disk failure and are bundled with redundant power supply as a default feature. Opslag FS2 also supports multiple snapshots with scheduling as a default feature and supports local and remote replication. For customers looking for a highly-available system, Opslag FS2 supports fail-over clustering.</p>

<p style="width:650px; text-align:justify; margin:0 0 10px 0;">Since Opslag FS2 has been designed to be a flexible solution to cater to various requirements, it supports SSD caching for customers looking for extremely high IOPS. Our SSD caching algorithm is integrated at the hardware level and not at the system level and therefore offers performance acceleration irrespective of whether you are using file or block access protocol.</p>

<p style="margin:0 0 5px 0; width:650px; font-weight:bold;">Easy Management/Integration</p>
<p style="width:650px; text-align:justify; margin:0 0 10px 0;">Tyrone systems believes in keeping things simple. FS2 can seamlessly integrate with ADS & NIS and our web based management UI is very intuitive and easy to use. For system health monitoring, Opslag FS2 has support for IPMI 2.0 and for SNMP. </p>

<p style="width:650px; text-align:justify; margin:0 0 10px 0;">It supports a variety of file and block protocols, supports a wide variety of client systems and many different configurations for host connectivity.</p>

<div style="background:#ccc; padding:.3em; width:491px; font-weight:bold;">Clients/Protocols Supported by FS2</div>
<table width="500px;">
<tr>
<td>Clients supported</td>
<td>Windows, MAC OS, Linux, FreeBSD,Solaris</td>
</tr>

<tr>
<td>File Protocols</td>
<td>CIFS/SMB, AFP, FTP, NFS & NFS over RDMA</td>
</tr>

<tr>
<td>Block Protocols</td>
<td>iSCSI Target, FC Target, SRP Target</td>
</tr>

<tr>
<td>Host Interface(s)</td>
<td>Gigabit Ethernet -> Up to 12 ports (RJ45)<br/>
10G Ethernet -> Up to 4 ports (SFP+)<br/>
40G Ethernet -> Up to 2 ports (40GBASE-CR4)<br/>
Fibre-Channel -> Up to 2 ports<br/>
InfiniBand -> Up to 4 ports (QSFP)</td>
</tr>

</table>

        </div>
          </div>


        	</div>
	 <!--form container ends here-->
        <p>&nbsp;</p>


              </div>
		<div id="tabs-4">
		<div class="form-container">

                 <div class="topinputwrap-heading">SSL Certificate Information</div>
          <div class="inputwrap">
         <div class="formleftside-content">

        </div>
          </div>


                </div>
         <!--form container ends here-->
        <p>&nbsp;</p>

              </div>

<!-- ####### Sub Tabs Start ####### -->

<script>
$("#tabs, #subtabs").tabs();
$("#tabs, #subsubtabs").tabs();
</script>

<!-- ####### Sub Tabs End ####### -->

"""
