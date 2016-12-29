#!/usr/bin/python
import cgitb, header, sys, common_methods
cgitb.enable()


import left_nav
print
print """
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Untitled Document</title>
<link rel="stylesheet" href="css/jquery-ui.css">
<!--<script src="js/jquery-1.10.2.js"></script>
<script src="js/jquery-ui.js"></script>-->
<link rel="stylesheet" href="/resources/demos/style.css">
<link rel="stylesheet" type="text/css" href="css/corntab.css" />
<script>
  $(function() {
    $( "#accordion" ).accordion();
  });
  </script>
</head>

<body onload="drawszlider(121, 56);">
<div id="accordion">
  <h3>Minute</h3>
  <div id="tabs">
    <ul>
      <li><a href="#tabs-1">every minute</a></li>
      <li><a href="#tabs-2">every <em>n</em> minutes</a></li>
      <li><a href="#tabs-3">each selected minute</a></li>
    </ul>
    <div id="tabs-1">
    <p>*</p>
    </div>
    <div id="tabs-2">
<div id="slider"></div>
    </div>
    <div id="tabs-3">
   <p>Date: <input type="text" id="datepicker"></p>
    </div>
  </div>
<h3>Month</h3>
  <div id="tab1">
    <ul>
      <li><a href="#tabs-1">Date</a></li>
      <li><a href="#tabs-2">Time</a></li>
      <li><a href="#tabs-3">Year</a></li>
    </ul>
    <div id="tabs-1">
      <p>xcvbvbvn</p>
    </div>
    <div id="tabs-2">
      <p>xcxvcbvbv</p>
    </div>
    <div id="tabs-3">
      <p>fdgfvcbvbv</p>
    </div>
  </div>
  <h3>Day of Month</h3>
  <div id="tab2">
    <ul>
      <li><a href="#tabs-1">every day</a></li>
      <li><a href="#tabs-2">each selected day</a></li>
    </ul>
    <div id="tabs-1">

    </div>
    <div id="tabs-2">

    </div>
  </div>

</div>
<script>
  $(function() {
    $( "#tabs" ).tabs();
  });
  </script>
<script>
  $(function() {
    $( "#tab1" ).tabs();
  });
  </script>
<script>
  $(function() {
    $( "#tab2" ).tabs();
  });
  </script>
<script>
  $(function() {
    $( "#slider" ).slider();
  });
  </script>
  <script>
  $(function() {
    $( "#datepicker" ).datepicker();
  });
  </script>
</body>
</html>


hi
"""
