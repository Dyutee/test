#!/usr/bin/python
import cgitb, header, sys, common_methods
cgitb.enable()


select_min_val = []
select_opt = range(0, 30)
print select_opt
#for i in select_opt:
#	select_min_val.append(i)

import left_nav
print
print """
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Untitled Document</title>
<link rel="stylesheet" href="../snap_css/jquery-ui.css">
<script src="../snap_js/jquery-1.10.2.js"></script>
<script src="../snap_js/jquery-ui.js"></script>
<link rel="stylesheet" href="/resources/demos/style.css">
<link rel="stylesheet" type="text/css" href="../snap_css/corntab.css" />
<script>
  $(function() {
    $( "#accordion" ).accordion();
  });
  </script>
</head>

<div id="accordion">
  <h3>Minute</h3>
	
  <div id="tabs">
<th>Minute</th>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<th>Hour</th>
<div>
<input type = "checkbox" name = "snap_check">
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<input type = "checkbox" name = "hour_check">
</div>
<div>
<select name = "snap_min_select">
<option>select</option>
</select>
</div>

  </div>
<h3>Month</h3>
  <div id="tab1">
	TEst2
  </div>
  <h3>Day of Month</h3>
  <div id="tab2">
Test3
  </div>
</body>
</html>
"""
