#!/usr/bin/python
import cgitb, os, cgi, commands, sys, common_methods, datetime, string, time
cgitb.enable()

sys.path.append('../modules/')
import disp_except

print
print """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>...:::Opslag FS2:::...</title>
<link href="../css/style.css" rel="stylesheet" type="text/css"/>
<link href="../css/style_new.css" rel="stylesheet" type="text/css"/>
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
<link rel="stylesheet" href="../css/help_tooltip.css" />
<script src="../js/jquery1.7.js"></script>
<script type="text/javascript" src="../js/jquery.flot.min.js"></script>
<script type="text/javascript" src="../js/jquery.flot.time.js"></script>
<script type="text/javascript" src="../js/jshashtable-2.1.js"></script>
<script type="text/javascript" src="../js/jquery.numberformatter-1.2.3.min.js"></script>
<script type="text/javascript" src="../js/jquery.flot.symbol.js"></script>
<script type="text/javascript" src="../js/jquery.flot.axislabels.js"></script>
<script type="text/javascript" src="../js/ts_picker.js"></script>

<link rel="stylesheet" href="../fancyBox/source/jquery.fancybox.css" type="text/css" media="screen" />
<script type="text/javascript" src="../fancyBox/source/jquery.fancybox.pack.js"></script>

<script src="../js/chart_graph1.js" type="text/javascript"></script>
<script src="../js/chart_graph2.js" type="text/javascript"></script>
<script src="../js/jquery.alerts.js"></script>
<script src="../js/jquery-ui.js"></script>
<!--<script type = 'text/javascript' src="../js/jquery-latest.js"></script>-->
<!--<link rel="stylesheet" href="../resources/demos/style.css" />-->
<link rel="stylesheet" href="../css/style.css" />

<script src="../js/propeller.js"></script>
<link rel="stylesheet" href="../css/turbine.css" />
<script>
  $(function() {
    $( "#tabs" ).tabs();
  });
  </script>
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

/*$(".firstLevelItemWrap, .SecondLevelItemWrap, .ThirdLevelItemWrap").mouseenter(function(){

	$(this).children("h2, h3").css("color","#e10019");         

});

$(".firstLevelItemWrap, .SecondLevelItemWrap, .ThirdLevelItemWrap").mouseleave(function(){
	if($(this).hasClass("MenuActiveClass")){
		$(this).children("h2, h3").css("color","#e10019");
	}

	$(this).children("h2, h3").css("color","#585858");         

});*/

if($("h2, h3").hasClass("MenuActiveClass")){
	$(".MenuActiveClass").css("color","#e10019");
	$(".MenuActiveClass").css("color","#e10019");
	$(".MenuActiveClass").parent(".ThirdLevelItemWrap").parent("a").parent(".3rdLevel").removeAttr("style");
	$(".MenuActiveClass").parent(".ThirdLevelItemWrap").parent("a").parent(".3rdLevel").prev(".SecondLevelItemWrap").parent(".2ndLevel").removeAttr("style");
$(".MenuActiveClass").parent(".SecondLevelItemWrap").parent("a").parent(".2ndLevel").removeAttr("style");
	$(".MenuActiveClass").parent(".SecondLevelItemWrap").parent("a").parent(".2ndLevel").prev(".SecondLevelItemWrap").parent(".2ndLevel").removeAttr("style");
	
} 



$(".firstLevelItemWrap").click(function(){       

   $(".2ndLevel").css("display","none");           

   if ($(this).next(".2ndLevel").is(":hidden")) {

			$(this).next(".2ndLevel").removeAttr("style");

			//$(this).find(".tariffheadericon").attr("src","assets/images/minus-icon.png"); 

		}  

});

$(".SecondLevelItemWrap").click(function(){     

   $(".3rdLevel").css("display","none"); 

   if ($(this).next(".3rdLevel").is(":hidden")) {

			$(this).next(".3rdLevel").removeAttr("style");

			//$(this).find(".tariffheadericon").attr("src","assets/images/minus-icon.png"); 

		}  

});



});

</script>
<script>
        window.onload = function () { startTimer(900); document.getElementById("iframe_blanket_cover").style.display='none'; }</script>
"""
