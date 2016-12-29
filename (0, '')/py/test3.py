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
	'''
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
		
	print file_txt	
	test_arr = []
	cmd  = commands.getstatusoutput('cp test.txt test9.txt')
	read_file = open('test.txt', 'r')
	for line in read_file:
		line_count1 = line
		line_count1 +'<br/>'
		test_arr.append(line_count1)
		
	print test_arr
		
	'''
	display_sel='block'
	if(header.form.getvalue("sels_nm")):
        	print 'test'
		display_sel = 'block'
	print"""
	<html>
	    <head>
		<meta charset="utf-8" />
		<title>My jQuery Ajax test</title>
		<style type="text/css">
		    #mybox {
			width: 150px;
			height: 310px;
			border: 1px solid #999;
		    }
		</style>
		<script language = 'javascript' src = '../js/jquery1.7.js'></script>
		<!--<script>                         
			function myCall() {
			    var request = $.ajax({
				url: "test.txt",
				type: "GET",           
				dataType: "html"
			    });
	 
			    request.done(function(msg) {
				$("#mybox").html(msg);         
				multipleValues = $( "#multiple" ).val() || [];
			    });
	 
				request.fail(function(jqXHR, textStatus) {
				alert( "Request failed: " + textStatus );
			    });
			}
		     
		</script>-->
		<script>
		function myCall()
			{
				var xmlhttp;
				if (window.XMLHttpRequest)
				  {
				  xmlhttp=new XMLHttpRequest();
				  }

				else

				  {// code for IE6, IE5

				  xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");

				  }

				xmlhttp.onreadystatechange=function()
				  {
				  if (xmlhttp.readyState==4 && xmlhttp.status==200)
				    {
				    document.getElementById("opt_id").innerHTML=xmlhttp.responseText;
				    }
				  }
				xmlhttp.open("GET","cp_text.txt",true);
				xmlhttp.send();


			}

		 function mygrp()
                        {
                                var xmlhttp;
                                if (window.XMLHttpRequest)
                                  {
                                  xmlhttp=new XMLHttpRequest();
                                  }

                                else

                                  {// code for IE6, IE5

                                  xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");

                                  }

                                xmlhttp.onreadystatechange=function()
                                  {
                                  if (xmlhttp.readyState==4 && xmlhttp.status==200)
                                    {
                                    document.getElementById("opt_id").innerHTML=xmlhttp.responseText;
                                    }
                                  }
                                xmlhttp.open("GET","cp_text1.txt",true);
                                xmlhttp.send();


                        }
		</script>
	    </head>
	    <body>
		<form name = "frmname" method = "post" action = "">
		<input type ="text" name = "inpt" >
		<input type = "hidden" name = "sel_nm"> 
		</form>
		<select name = "sel_nm" multiple style="width:150px;height:310px;" onchange='this.form.submit()'>"""
	print"""
		<option value = '' id="opt_id"><br></option>"""
	print"""
		
		</select>
		<!--<button><input type="submit" name ="but" value ="check" onclick="myCall();" >new</button>
		<input type="button" name = "but" value="check" onclick="myCall()" />-->
		<select name = "sels_nm" onchange='this.form.submit()' value="check" />
		<option value = '' >select</option>
		<option value = '' onclick="myCall()">user</option>
		<option value = '' onclick="mygrp()">group</option>
		</select>
		
	    </body>
	</html>"""
except Exception as e:
        disp_except.display_exception(e);
