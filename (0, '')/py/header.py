#!/usr/bin/python
import cgitb, os, cgi, commands, sys, common_methods, datetime, string, time, socket
cgitb.enable()

sys.path.append('../modules/')
import disp_except

try:
	sys.path.append('/var/nasexe/python/')
	import tools
	get_ha_nodename = tools.get_ha_nodename()

	remoteip = cgi.escape(os.environ["REMOTE_ADDR"]);
	#remoteips = cgi.escape(os.environ["SERVER_ADDR"]);

	cpu1_temp_command = ''
	cpu2_temp_command = ''
	circle_icon_image1 = ''
	circle_icon_image2 = ''
	#cpu1_temp_command = 'critical'
	#print(socket.gethostname())
	cpu1_temp_command = commands.getoutput("sudo ipmitool sdr|grep -i 'cpu1 temp'|awk -F '|' {\'print $3\'}|sed 's/ //g'")

	if (cpu1_temp_command.lower() == 'ok'):
		#cpu1_temp_command = cpu1_temp_command.strip();
		circle_icon_image1 = "<img src = '../images/cputemp.jpg' style='width:14px;height: 31px;'>";

	#cpu1_temp_command = 'critical'

	#elif (cpu1_temp_command == 'NA'):
	#       circle_icon_image1 = "";

	if (cpu1_temp_command.lower() == 'critical'):
		circle_icon_image1 = "<span class = 'img1'><img src = '../images/cpucritical.jpg' style = 'width:14px;height:31px;'></span>"

	#else:
	#       circle_icon_image1 = "";

	cpu2_temp_command = commands.getoutput("sudo ipmitool sdr|grep -i 'cpu2 temp'|awk -F '|' {\'print $3\'}|sed 's/ //g'")

	#if (cpu2_temp_command != 'NA'):

	if (cpu2_temp_command.lower() == 'ok'):
		circle_icon_image2 = "<img src = '../images/cputemp.jpg' style='width:14px;height: 31px;'>";
	#elif (cpu2_temp_command == 'NA'):
	#       circle_icon_image2 = "";

	if (cpu2_temp_command.lower() == 'critical'):
		circle_icon_image2 = "<span class = 'img1'> <img src = '../images/cpunw.jpg' style = 'width:46px;height:30px;'></span>"

	#else:
	#       circle_icon_image2 = "";

	form = cgi.FieldStorage()
	pageval = common_methods.getpageval();
	page_val = common_methods.get_title(pageval)

	user_access = common_methods.get_session_user();
	#print user_access
	querystring = os.environ['QUERY_STRING'];

	if (querystring.find('&stat=') > 0):
		response = common_methods.getsubstr(querystring, '&stat=', '&');


	#########################################
	#Session code start here 
	#########################################
	#session_user = 'x';

	session_user = common_methods.get_session_user();
	#print 'SeSS:'+str(session_user)
	#print '<br/>'
	#session_user_new = common_methods.get_session_user_new();
	#print 'NEWSESS:'+str(session_user_new)
	if(session_user == ''):
		print ("<script>location.href = 'login.py';</script>")

	randomNumber = cgi.escape(os.environ["REMOTE_ADDR"])

	#login_time = '';
	#session_update_line = '';

	#login_line = commands.getoutput('sudo grep "' + randomNumber + ':" /tmp/.sessions/sessions.txt|tail -1')
	#print login_line
	#print '<br/>'
	#------------------------get Time from this command-----------------------------
	new_curenttime = datetime.datetime.now().replace(microsecond=0)
	#------------------------------End----------------------------------------------
	#------------------------Get Value from Database--------------------------------------------
	import MySQLdb
        db = MySQLdb.connect("localhost","root","netweb","fs2" )
        cursor = db.cursor()
	query = "select * from session where remote_ip='"+randomNumber+"';"
	status = cursor.execute(query)
	if(status > 0):
		fetch_all = cursor.fetchall()
		for row in fetch_all:
			#up_time = row[1]
			time_stamp = row[3]
			login_time_new = datetime.datetime.strptime(time_stamp, '%Y-%m-%d %H:%M:%S')
			#print login_time_new
			#print '<br/>'
			update_query = "update session set time='"+str(new_curenttime)+"'where remote_ip='"+str(randomNumber)+"';"
			#print update_query
			update_status = cursor.execute(update_query)
			db.commit()
			#print update_query
			new_session_time = str(datetime.datetime.now().replace(microsecond=0))
			session_currenttime_new = datetime.datetime.strptime(new_session_time, '%Y-%m-%d %H:%M:%S')
			difference_session_new = session_currenttime_new - login_time_new
			difference_session_new =str(difference_session_new)
			difference_session_value_new= difference_session_new[:difference_session_new.find(',')]
			session_day_new= difference_session_value_new.replace('day', '')
			session_day_new=difference_session_value_new.replace('days', '')
			session_hour_new = difference_session_new[:difference_session_new.find(':')]
			#session_hour_new=int(session_hour_new)
			session_minute_new = difference_session_new[difference_session_new.find(':')+1:difference_session_new.rfind(':')]

			session_hour_new = difference_session_new[:difference_session_new.find(':')]
			session_minute_new= int(session_minute_new)
			if((session_minute_new > 20)):
				delete_query = "delete from session where remote_ip='"+str(randomNumber)+"'"
				del_status = cursor.execute(delete_query)
				db.commit()
				db.close()
				print ("<script>location.href = 'login.py';</script>")
			
		#	print
		#print '<br/>'
		#print randomline
	#print replace_line_command
	#replace_line = commands.getoutput(replace_line_command);
	#print replace_line

	##############################
	#Session End
	##############################
	curr_date_time = datetime.datetime.now();

	system_curr_time = curr_date_time.strftime('%b %d %Y / %H:%M');

	#cpu1_temp = '10.0';
	#cpu2_temp = '30.9';

	cpu_array = [];

	blink_text   = '';
	blink_text   = '';
	heat1_image  = '';
	head2_image  = '';
	blink1_begin = '';
	blink1_end   = '';
	blink2_begin = '';
	blink2_end   = '';

	alertimage = '';

	#-----------------------------------------------------End------------------------------------------------------------
	#print 'Content-Type: text/html'

	print
	print """
	<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
	<html xmlns="http://www.w3.org/1999/xhtml">
	<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<title>...:::Opslag FS2:::...</title>
	<link href="../css/style.css" rel="stylesheet" type="text/css"/>
	 <script type="text/javascript" src="../js/jquery.min(1).js"></script>
	<link href="../css/drop-down/ddmenuMst.css" rel="stylesheet" type="text/css" />
	<link href="../css/chart_graph.css" rel="stylesheet" type="text/css" />
	<link href="../css/drop-down/accordionmenu.css" rel="stylesheet" type="text/css" />
	<link href = "../css/jquery.alerts.css" rel = "stylesheet" type = "text/css" />
	<script src="../js/commons.js" type="text/javascript"></script>
	<script type="text/javascript" src="../js/jquery.alerts.js"></script>
	<script src="../js/drop-down/ddmenuMst.js" type="text/javascript"></script>
	<script src="../js/drop-down/accordionmenu.js" type="text/javascript"></script>
	<link rel="stylesheet" href="../css/jquery-ui.css" />
	<link rel="stylesheet" href="../css/main.css" />
	<link rel="stylesheet" href="../css/new_menu.css" />
	<script src="../js/jquery1.7.js"></script>
	<script type="text/javascript" src="../js/jquery.flot.min.js"></script>
	<script type="text/javascript" src="../js/jquery.flot.time.js"></script>
	<script type="text/javascript" src="../js/jshashtable-2.1.js"></script>
	<script type="text/javascript" src="../js/jquery.numberformatter-1.2.3.min.js"></script>
	<script type="text/javascript" src="../js/jquery.flot.symbol.js"></script>
	<script type="text/javascript" src="../js/jquery.flot.axislabels.js"></script>
	<script type="text/javascript" src="../js/ts_picker.js"></script>

	<script src="../js/chart_graph1.js" type="text/javascript"></script>
	<script src="../js/chart_graph2.js" type="text/javascript"></script>
	<script src="../js/jquery.alerts.js"></script>
	<script src="../js/jquery-ui.js"></script>
	<!--<script type = 'text/javascript' src="../js/jquery-latest.js"></script>-->
	<!--<link rel="stylesheet" href="../resources/demos/style.css" />-->
	<link rel="stylesheet" href="../css/style.css" />
	<link rel="stylesheet" href="../css/help_tooltip.css" />
	<link rel="stylesheet" href="../css/style_new.css" />
	 <link rel="stylesheet" href="../css/turbine.css" />
	<script src="../js/propeller.js"></script>

	 <script src="../js/jss.js"></script>
	<style type="text/css">.js div#preloader { position: fixed; left: 0; top: 0; z-index: 999; width: 100%; height: 100%; overflow: visible; background: #fff url('../images/loader.gif') no-repeat center center; }</style>
	<script>
	  $(function() {
	    $( "#tabs" ).tabs();
	  });
	  </script>

	<style type="text/css">
              
              div.item { width:100px; height:0px; background-color: #fff; text-align:center; padding-top:0px; }
              div#item_1 { top: 0px; width: 35px; height: 15px; float:left; }
              div#item_2 { top: 80px; width: 145px; height: 20px; }      
              div#item_3 { top: 80px; width: 165px; height: 20px; }            
              div#item_4 { top: 0px; width: 10px; height:26px; padding:0 162px 0 0;  }                 
              tr.spaceUnder > td{ padding-bottom: 7px;} 
            </style>
	<SCRIPT language=Javascript>
      
      function isNumberKey(evt)
      {
         var charCode = (evt.which) ? evt.which : event.keyCode
         if (charCode > 31 && (charCode < 46 || charCode > 57 || charCode == 190))
            return false;

            return true;

      }
     
        </SCRIPT>

	<!--Session Timer Start-->
	<script type="text/javascript">
	var timeoutHandle = null;

	function startTimer(timeoutCount) {
	if (timeoutCount == 0) {                
		window.location.href = 'logout.py';
		window.opener='x'
		window.close();
	} 
	else if (timeoutCount < 900) {
		document.getElementById('sessionTimer').innerHTML = 'Session Timer : ' + (timeoutCount * 60/3600).toFixed(parseInt(2)) ;
	}

	timeoutHandle = setTimeout(function () { startTimer(timeoutCount-1);}, '900');
	}

	function refreshTimer() {
		killTimer(timeoutHandle);
		startTimer(900);
	}

	</script>
	<!--Session Timer Ends-->

	<!-- ####### Auto Fade Notification Start ####### -->

	<script type = "text/javascript">
	function hideMessage() {
			$("#id_trace_err").fadeOut(2000);
			$("#id_trace").fadeOut(2000);
	}
		
	var tim = window.setTimeout("hideMessage()", 10000);  // 10000 milliseconds = 10 seconds
	</script>

	<!-- ####### Auto Fade Notification Ends ####### -->

	<script src="../js/datetimepicker.js" type="text/javascript"></script>

	<script type="text/javascript" src="popup/pop.js"></script>  
	<link type="text/css" rel="stylesheet" href="popup/popup.css" />
	<script type="text/javascript">
	$(document).ready(function() {
//Mouseover color change to red
   $(".firstLevelItemWrap, .SecondLevelItemWrap, .ThirdLevelItemWrap").mouseenter(function(){
                $(this).children("h2, h3").css("color","#e10019");         
   });
//Mouseout color change to black
   $(".firstLevelItemWrap, .SecondLevelItemWrap, .ThirdLevelItemWrap").mouseleave(function(e){
                $(this).children("h2, h3").css("color","#585858");
                if($(this).children("h2, h3").hasClass("MenuActiveClass")){
                        $(this).children("h2, h3").css("color","#e10019");
                }
                           
   });
//Active state arrow and active color
   if($("h2, h3").hasClass("MenuActiveClass")){
        $(".MenuActiveClass").css("color","#e10019");
                $(".MenuActiveClass").css("color","#e10019");
                $(".MenuActiveClass").parent(".ThirdLevelItemWrap").parent("a").parent(".3rdLevel").css("display","block");
                $(".MenuActiveClass").parent(".ThirdLevelItemWrap").parent(".3rdLevel").css("display","block");
                $(".MenuActiveClass").parent(".ThirdLevelItemWrap").parent("a").parent(".3rdLevel").prev(".SecondLevelItemWrap").parent(".2ndLevel").css("display","block");                    
                $(".MenuActiveClass").parent(".SecondLevelItemWrap").parent("a").parent(".2ndLevel").css("display","block");
                $(".MenuActiveClass").parent(".SecondLevelItemWrap").parent(".2ndLevel").css("display","block");
                $(".MenuActiveClass").parent(".SecondLevelItemWrap").parent("a").parent(".2ndLevel").prev(".SecondLevelItemWrap").parent(".2ndLevel").css("display","block");
                $(".MenuActiveClass").parent(".SecondLevelItemWrap").parent("a").parent(".2ndLevel").prev(".firstLevelItemWrap").children(".firstLevelRightarrow").find(".firstLevelArrow").attr("src","images/firstrightArrowDown.png");
                $(".MenuActiveClass").parent(".SecondLevelItemWrap").parent(".2ndLevel").prev(".firstLevelItemWrap").children(".firstLevelRightarrow").find(".firstLevelArrow").attr("src","images/firstrightArrowDown.png");
                $(".MenuActiveClass").parent(".ThirdLevelItemWrap").parent("a").parent(".3rdLevel").prev(".SecondLevelItemWrap").children(".secondLevelRightarrow").find(".secondLevelArrow").attr("src","images/secondrightArrowDown.png");
                $(".MenuActiveClass").parent(".ThirdLevelItemWrap").parent("a").parent(".3rdLevel").prev(".SecondLevelItemWrap").parent(".2ndLevel").prev(".firstLevelItemWrap").children(".firstLevelRightarrow").find(".firstLevelArrow").attr("src","images/firstrightArrowDown.png");                                       
   } 
//Firstlevel click event   
   $(".firstLevelItemWrap").click(function(){      
           $(".2ndLevel").slideUp("slow");
           $(".firstLevelArrow").attr("src","images/firstrightArrow.png");      
           if ($(this).next(".2ndLevel").is(":hidden")) {
                                $(this).next(".2ndLevel").slideDown("slow");
                                $(this).find(".firstLevelArrow").attr("src","images/firstrightArrowDown.png");  
                        }  
   });

//Secondlevel click event
   $(".SecondLevelItemWrap").click(function(){     
          $(".3rdLevel").slideUp("slow");
          $(".secondLevelArrow").attr("src","images/secondrightArrow.png");     
           if ($(this).next(".3rdLevel").is(":hidden")) {
                                $(this).next(".3rdLevel").slideDown("slow");
                                $(this).find(".secondLevelArrow").attr("src","images/secondrightArrowDown.png");        
                        }  
   });
      
});


</script>


	</head>
	<body class="js">"""
	if("page=fs2" in querystring):
		print"""<!--<div id="id_trace" >testing please wait... <a href="#" style="float:right; margin:0 50px 0 0; color:#000; font-weight:bold;" onclick="return close_id_trace_div();" title="Close">X</a></div>-->"""
	else:
		#print"""<div id="blanket_cover" ><img style="margin-top:20%;" src="../images/spin.gif" /> Loading...</div>"""
		print """<div id="preloader"></div>"""
	print"""
	<script>
	window.onload = function () { startTimer(900); document.getElementById("blanket_cover").style.display='none'; }</script>

	<!--body wrapper srt-->
	<div class = "top_border">
	<div class = "header_center">
<!--top container srt-->
	    <div class="top_container">
	      <div class="top_container_left" ><a href="main.py?page=first"><img src="../images/logo_tyroneopslag.jpg" class="borderless" style = "margin-top:6px;"/></a></div>
	      <div class="top_container_right content">
		<span style = "color:#575757;" id="sessionTimer"></span> |
		<span>"""+time.strftime('%d %h %Y')+" / "+time.strftime('%H:%M')+"""</span> |
		<span style = "color:#575757;">"""+user_access+"""</span> |
		<span style = "color:#575757;">"""+get_ha_nodename+"""</span>
		
		</div>
		<div class = "top_container_new_right"><div style="float:left;width:99px;text-align:center;margin-left:-12px;" ><a href="main.py?page=change_pass" style = "color:#575757;"><img src="../images/key-20.png" class="borderless" /><br/>Change&nbsp;Password</a></div>&nbsp;&nbsp;
		<div style="float:left;width:51px;text-align:center;margin-left: 9px; margin-top: -17px;" ><a href="logout.py" style = "color:#575757;"><img src="../images/logout.jpg" class="borderless" /><br/>Logout</a></div>
 </div>
	      </div>
	    </div>
	    <!--top container end-->



	</div>
	<div class="insidepagewrapper insidebg">
	  <!--inside body wrapper srt-->
	  <div class="body_wrapper">
	    	"""
except Exception as e:
        disp_except.display_exception(e);
