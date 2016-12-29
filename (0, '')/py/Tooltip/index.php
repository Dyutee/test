<html>
<head>
<link href = "Tooltip.css" rel = "stylesheet" type = "text/css" />
   <script type="text/javascript" src="Tooltip.js"></script>

  <script type="text/javascript" src="jquery.alerts.js"></script>
</head>

<span class="tooltip" onmouseover="tooltip.add(this, 'demo2_tip')">cpu</span> <div id="demo2_tip" style="display:none;">  The content is taken from the inner HTML of an element on the page. So this approach of setting tooltip content is <b>SEO friendly</b> (search engine friendly). </div>

<a href="#" onclick="tooltip.pop(this, '#demo3_tip', {overlay:true, position:4}); return false;">Click me</a> <div style="display:none;"> <div id="demo3_tip"> Name: <asp:TextBox ID="TextBox1" runat="server" /><br /> <asp:Button ID="Button1" runat="server" Text="Login" onclick="Button1_Click" /> <input type="button" onclick = "tooltip.hide()" value="Cancel" /> </div> </div>
</html>
