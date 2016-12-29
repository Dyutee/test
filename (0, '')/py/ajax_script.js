$(document).ready(function(){
$("#submit").click(function(){
var name = $("#name").val();
alert (name);
var password = $("#password").val();
// Returns successful data submission message when the entered information is stored in database.
var dataString = 'name1='+ name + '&password1='+ password +;
if(name==''||password=='')
{
alert("Please Fill All Fields");
}
else
{
// AJAX Code To Submit Form.
$.ajax({
type: "POST",
url: "ajaxsubmit.php",
data: dataString,
cache: false,
success: function(result){
alert(result);
}
});
}
return false;
});
});
