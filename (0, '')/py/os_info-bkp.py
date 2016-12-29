#!/usr/bin/python

import traceback, sys, header
sys.path.append('../modules/')
import disp_except;

try:
	import cgitb, os, cgi, sys,opslag_info, memory_information
	cgitb.enable()

	memory_info = memory_information.mem_information()
	
	#-----------------------All Information Getting from Tools -----------------------
        sys.path.append('/var/nasexe/python/')
        from tools import scan_remount
        from tools import shutdown

        cpu_new_model = scan_remount.cpu_model()

        server_ip_cmd = scan_remount.server_ip()

        remote_ip_cmd = scan_remount.remote_ip()

	server_cmd = scan_remount.server_name()

	uptime_cmd = scan_remount.up_time()

	cpu_use_cmd = scan_remount.cpu_use()


	last_login_cmd = scan_remount.last_login()

	current_login_cmd = scan_remount.current_login()
	#status_dump= shutdown.dump_configuration_module()
        #print status_dump


	import left_nav
	print"""
	      <!--Right side body content starts from here-->
	      <div class="rightsidecontainer">
		<div class="insidepage-heading" style = "color:#575757;float:right;" > RESOURCES >>Resources Information >><span class="content">OS Information</span></div>
		<!--tab srt-->
		<div class="searchresult-container">
		  <div class="infoheader">
		    <!--<div id="tabs">-->
		<div class="topinputwrap-heading">OS Information</div>
		      <!--<ul>
			<li><a href="#tabs-1">OS Information</a></li>
		      </ul>-->
			
			<div id="tabs-1">
			<!--<div class="form-container">-->
			<div class="inputwrap">
                    <div class="formleftside-content">CPU:</div>
                    <div class="formrightside-content"><img src='../images/cpu_img1.png'></div><div class="formrightside-content" style="margin-top: -4%; margin-left: 34%;">"""+cpu_new_model+"""</div>
                  </div>
                  <div class="topinputwrap">
                    <div class="formleftside-content">Server IP:</div>
                    <div class="formrightside-content">""" +server_ip_cmd+ """</div>
                 </div>
		 <div class="inputwrap">
                    <div class="formleftside-content">Remote IP:</div>
                    <div class="formrightside-content"> """ +remote_ip_cmd+ """</div>
                  </div>
                  <div class="altinputwrap">
                    <div class="formleftside-content">HostName:</div>
                    <div class="formrightside-content">""" + server_cmd + """</div>
                  </div>
                  <div class="inputwrap">
                    <div class="formleftside-content">Uptime:</div>
                    <div class="formrightside-content">""" + uptime_cmd + """</div>
                  </div>
                  <div class="altinputwrap">
                    <div class="formleftside-content">Current Login:</div>
                    <div class="formrightside-content" style="margin-top: -2%;">""" +current_login_cmd+ """</div>
                  </div>
                 <div class="inputwrap">
                    <div class="formleftside-content">Last Login:</div>
                    <div class="formrightside-content" style="margin-top: -2%;">""" +last_login_cmd+ """</div>
                  </div>
                 <div class="altinputwrap">
                    <div class="formleftside-content">Memory(MB):</div>
                    <div class="formrightside-content">""" +memory_info["total"]+ """</div>
                  </div>
                
                <div class="inputwrap">
                    <div class="formleftside-content">Used Memory(MB):</div>
                    <div class="formrightside-content">""" +memory_info["used"]+ """</div>
                  </div>

		  <div class="altinputwrap">
                    <div class="formleftside-content">Free Memory(MB):</div>
                    <div class="formrightside-content">""" +memory_info["free"]+ """</div>
                  </div>
                 <div class="inputwrap">
                    <div class="formleftside-content">Cpu usage:</div>
                    <div class="formrightside-content">""" +cpu_use_cmd+ """</div>
                  </div>
		<div class="altinputwrap">
                    <div class="formleftside-content">OS:</div>
                    <div class="formrightside-content">""" + opslag_info.getos('oss') + """</div>
                  </div>
                 <div class="inputwrap">
                    <div class="formleftside-content">Version:</div>
                    <div class="formrightside-content">""" + opslag_info.getos('version') + """</div>
                  </div>
		<div class="altinputwrap">
                    <div class="formleftside-content">Build:</div>
                    <div class="formrightside-content">""" + opslag_info.getos('build') + """</div>
                  </div>
                 <div class="inputwrap">
                    <div class="formleftside-content">Model:</div>
                    <div class="formrightside-content">""" + opslag_info.getos('model') +"""</div>
                  </div>

		  <div class="altinputwrap">
                    <div class="formleftside-content">Serial:</div>
                    <div class="formrightside-content">""" + opslag_info.getos('serial') + """</div>
                  </div>
                 <div class="inputwrap">
                    <div class="formleftside-content">Dispatch Date:</div>
                    <div class="formrightside-content">""" + opslag_info.getos('disp_date') +"""</div>
                  </div>
		</div>
		<p>&nbsp;</p>
		      </div>
			
                  </div>
                </div>
                <!--form container ends here-->
                <!--form container starts here-->
                <!--form container ends here-->
              </div>
              <!--Right side body content ends here-->
            </div>
                </div>
            <!--Footer starts from here-->
            <div class="insidefoter footer_content"><a href= "http://tyronesystems.com" style= "text-decoration:none;color:#666666;margin-left:966px;">&copy; 2014 Opslag FS2</a></div>

                <!-- Footer ends here-->
          </div>
          <!--inside body wrapper end-->
        </div>
	<!--body wrapper end-->
	</body>
	</html>"""

except Exception as e:
        disp_except.display_exception(e);
