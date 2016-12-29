var textPadding = 3; // Padding at the left of tab text - bigger value gives you wider tabs
var strictDocType = true;
var tabView_maxNumberOfTabs = 6;	// Maximum number of tabs

/* Don't change anything below here */
var dhtmlgoodies_tabObj = new Array();
var activeTabIndex = new Array();
var MSIE = navigator.userAgent.indexOf('MSIE')>=0?true:false;

var regExp = new RegExp(".*MSIE ([0-9]\.[0-9]).*","g");
var navigatorVersion = navigator.userAgent.replace(regExp,'$1');

var ajaxObjects = new Array();
var tabView_countTabs = new Array();
var tabViewHeight = new Array();
var tabDivCounter = 0;
var closeImageHeight = 8;	// Pixel height of close buttons
var closeImageWidth = 8;	// Pixel height of close buttons
var error;
var user_priv;
	
var ip_error;
var netmask_error;
var gateway_error;
var search_active_session = -1;

var value_array    = new Array();
var in_user_array  = new Array();
var out_user_array = new Array();
var g_portal_array = new Array();
var globalpath = '';
var blinkid = '';

//Disable return key
function stopRKey(evt)
{
	var evt  = (evt) ? evt : ((event) ? event : null);
	var node = (evt.target) ? evt.target : ((evt.srcElement) ? evt.srcElement : null);

	if ((evt.keyCode == 13) && (node.type == "text"))
	{
		return false;
	}
}

document.onkeypress = stopRKey;
//End of disable return key

function show_alert1(ip)
{
	alert('IP '+ip+' is used for replication. Can not be changed!');
	return false;
}

function check_ftp_ip(ip)
{
	var error = "";

	var ipPattern = /^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$|^\*$|^$/;
	var ip_array = ip.match(ipPattern);

	if (ip == '')
	{
		error = 'Please enter a valid IP!';
	}

	if (ip == "0.0.0.0")
	{
		error = ip+' is not a valid IP';
	}
	
	else if (ip == "255.255.255.255")
	{
		error = ip+' is not a valid IP';
	}

	if (ip_array == null)
	{
		if (ip != '')
		{
			error = ip+' is not a valid IP!';
		}

		else
		{
			error = 'Both the IPs are required!';
		}
	}

	else if (ip_array != null)
	{
		for (i = 1; i <= 4; i++)
		{
			thisSegment = ip_array[i];

			if (thisSegment > 255)
			{
				error = ip+' is not a valid IP';
				i = 4;
			}
	
			if ((i == 0) && (thisSegment > 255))
			{
				error = ip+' is not a valid IP';
				i = 4;
			}
		}
	}

	return error;
}

function check_ip(ip)
{
	var error = "";

	var ipPattern = /^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/;
	var ip_array = ip.match(ipPattern);

	if (ip == '')
	{
		error = 'Please enter a valid IP!';
	}

	if (ip == "0.0.0.0")
	{
		error = ip+' is not a valid IP';
	}
	
	else if (ip == "255.255.255.255")
	{
		error = ip+' is not a valid IP';
	}

	if (ip_array == null)
	{
		error = ip+' is not a valid IP!';
	}

	else if (ip_array != null)
	{
		for (i = 1; i <= 4; i++)
		{
			thisSegment = ip_array[i];

			if (thisSegment > 255)
			{
				error = ip+' is not a valid IP';
				i = 4;
			}
	
			if ((i == 0) && (thisSegment > 255))
			{
				error = ip+' is not a valid IP';
				i = 4;
			}
		}
	}

	return error;
}

function fn_clear_log(log_size)
{
	if (parseFloat(log_size) >= 200)
	{
		alert('Log files reached the size limit. Clearing them! For logs you can download the \'fs2_logs.tar\' from \'Maintenance > Logs\' option.');
		document.location.href = 'clear_logs.php';
	}
}

function expand_shares()
{
	document.share_form.share_names.style.visibility = 'visible';
}

function show_share_det()
{
	document.getElementById('wait').style.display = 'block';

	var share     = document.shares.share_list.value;
	var from_page = document.shares.hid_from_page.value;
		
	alert(from_page);

	if (from_page == 'add_share')
	{
		var share_from_page      = document.shares.hid_share_from.value;
		var path_from_page       = document.shares.hid_path_from.value;
		var comment_from_page    = document.shares.hid_comment_from.value;

		$.ajax(
		{
			type: 'POST',
			url: 'find_share_det.php',
			data: 'proceed_page=proceed&s='+share_from_page+'&pth='+path_from_page+'&c='+comment_from_page+'&p=nas / share maintenance&from_page=add_share',

			success: function(html)
			{
				$('#response').html(html);
			}
		});
	}

	else
	{
		$.ajax(
		{
			type: 'POST',
			url: 'show_shares.php',
			data: 's='+share+'&check_to_proceed=proceed',

			success: function(html)
			{
				$('#response').html(html);
			}
		});
	}
}

function show_shares(sharepath, mounteddisks)
{
	string = '/storage/';

	diskname = sharepath.substring(sharepath.indexOf(string) + string.length, sharepath.lastIndexOf('/'));
	share  = sharepath.substring(sharepath.lastIndexOf('/') + 1, sharepath.length);

	checkmounteddisk = mounteddisks.indexOf(':' + diskname + ':');

	if (parseInt(checkmounteddisk) >= 0)
	{
        	location.href = 'show_shares.py?s1='+share+'&act=edit_share_done&md=' + diskname;
	}

	else
	{
		alert('You can\'t modify this share, since the disk on which it is created, is not mounted! Please run \'Rescan Volumes\', \'Remount Volumes\' from \'Maintenance\' menu.');

        	location.href = 'show_shares.py?s1='+share+'&act=edit_share_done&md=' + diskname;

		return false;
	}
}

function hide_configure_share()
{
	document.shares.share_list.style.visibility = 'hidden';
}

function show_dns_params()
{
	var dns_option = document.dns_form.use_dns.checked;
	var dns_params = document.getElementById('id_add_dns_val');

	if (dns_option == true)
	{
		dns_params.style.display = 'block';
	}

	else
	{
		dns_params.style.display = 'none';
	}
}

function validate_form()
{
        var hostname = document.server_change.hostname.value;
        var oldhostname = document.server_change.oldhostname.value;
        var sp_chars  = "\ \ !@#$%^&*()+=[]\\\';,/{}|\":<>?_";

        if (hostname == '')
        {
                //alert('Enter a valid name for host!');
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:6%; padding-top: 4%; font-family: status-bar;">Enter a valid Name for host.</div>', 'Alert Dialog');
                return false;
        }

        else
        {
                for (var i = 0;  i < hostname.length;  i++)
                {
                        if (sp_chars.indexOf(hostname.charAt(i)) != -1)
                        {
                                //alert('Special characters other than \'-\' and \'.\' are not allowed for host name!');
				jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:-1%; padding-top: 4%; font-family: status-bar;"> Special characters other than \'-\' and \'.\' are not allowed for host name!.</div>', 'Alert Dialog');
                                return false;
                        }
                }

                document.getElementById('wait').style.display = 'block';

                $.ajax(
                {
                        type: 'POST',
                        url: 'change_host.php',
                        data: 'hostname='+document.server_change.hostname.value+'&oldhostname='+document.server_change.oldhostname.value+'&proceed_page=proceed',

                        success: function(html)
                        {
                                $('#response').html(html);
                        }
                });
	}
}


function validate_high_availability()
{
        var harole = document.ha_form.harole.value;
        var interfaces = document.ha_form.interface.value;
        var ipaddress = document.ha_form.ipaddress.value;

        if (harole == 'status')
        {
                alert('Select a value for Ha Role!');
		document.ha_form.harole.focus();
                return false;
        }

	if (interfaces == 'select')
        {
                alert('Select a value for Interface!');
		document.ha_form.interface.focus();
                return false;
        }

	if (ipaddress == '')
        {
                alert('Enter a value for IP Address!');
		document.ha_form.ipaddress.focus();
                return false;
        }

	error = validate_access_ip(ipaddress);

	if (error != '')
	{
		alert(error)
		document.ha_form.ipaddress.focus();
		document.ha_form.ipaddress.value='';
		return false;
	}
}

function close_div()
{
	document.getElementById('response').style.display    = 'none';
	document.getElementById('dns_conf').style.display    = 'none';
	document.getElementById('eth_bonding').style.display = 'none';
}

function disable_button()
{
	document.getElementById('wait').style.display = 'block';

	$.ajax(
	{
		type: 'POST',
		url: 'remove_eth_binding.php',
		data: 'proceed_page=proceed',

		success: function(html)
		{
			$('#response').html(html);
		}
	});

	document.rem_bond_list.btn_remove.disabled = true;
	disable_all_other_forms('rem_bond_list');
}

function show_alert(eth)
{
	$(document).ready(function()
	{
        	var string = 'id_activate_button_'+eth;

	        document.getElementById(string).style.background = 'green';

		alert('Please look for the blinking port and wait for 10 seconds.');

		blinkid = document.getElementById('wait');
		blinkid.style.display = 'block';

		$.ajax(
		{
			type: 'POST',
			url: 'activate_device.php',
			data: 'hid_activate='+eth,

			success: function(html)
			{
				$('#response').html(html);
			}
		});
	});
}

function blink_interface_alert(eth_val)
{
	var eth_val = document.getElementById('hid_activate').value;
	alert(eth_val);

	alert('Please look for the blinking port and wait for 10 seconds.');

	document.getElementById('wait').style.display = 'table';


	$.ajax(
	{
		type: 'POST',
		url: 'blink_interface.py',
		data: 'blink_value='+eth_val,

		success: function(html)
		{
			$('#response').html(html);
		}
	});
}


function validate_plan_team()
{
	alert("hello");
	var bond_count    = document.plan_eth.bond_count.value;
	var eth_count     = document.plan_eth.hid_eth_count.value;
	var options_array = document.getElementsByName('bond_type');
		
	if (bond_count == '' || bond_count == 0)
	{
		alert('Please enter a valid number for number of bonds!');
		return false;
	}

	else
	{
		var count_pattern = /^(\d{1,3})$/;
		var count_array = bond_count.match(count_pattern);
			
		if (count_array == null)
		{
			alert('Please enter an integer value for number of bonds!');
			return false;
		}

		else
		{
			if (parseInt(bond_count) > parseInt(eth_count))
			{
				alert('Bond count can\'t exceed eth count!');
				return false;
			}
		}
	}

	if (options_array[0].checked == false && options_array[1].checked == false)
	{
		alert ('Choose a bond type!');
		return false;
	}

	else
	{
		document.getElementById('wait').style.display = 'block';

		if (options_array[0].checked == true)
		{
			bond_type = options_array[0].value;
		}

		if (options_array[1].checked == true)
		{
			bond_type = options_array[1].value;
		}

		$.ajax(
		{
			type: 'POST',
			url: 'plan_eth.php',
			data: 'bond_count='+bond_count+'&bond_type='+bond_type+'&proceed_page=proceed',
				
			success: function(html)
			{
				$('#response').html(html);
			}
		});
	}

	document.plan_eth.btn_plan_eth.disabled = true;
	disable_all_other_forms('plan_eth');
}

function validate_teaming_form()
{
	var bond_name  = document.assign_eth.bond_list.value;
	var eth_list   = document.assign_eth.elements["eth_list[]"];
	var eth_test   = document.assign_eth.elements["eth_list[]"].value;
	var eth_string = '';

	if (bond_name == '')
	{
		//alert('Choose a bond!');
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:6%; padding-top: 4%; font-family: status-bar;">Choose a bond.</div>', 'Alert Dialog');
		return false;
	}

	if (eth_test.length == 0)
	{
		//alert('Please choose an eth from the list!');
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:6%; padding-top: 4%; font-family: status-bar;">Please choose an eth from the list.</div>', 'Alert Dialog');
		return false;
	}

	else
	{
		for (i = 0;  i < eth_list.length;  i++)
		{
			if (eth_list[i].selected == true)
			{
				eth_string += '@@@'+eth_list[i].value;
			}
		}

		document.getElementById('wait').style.display = 'block';

		$.ajax(
		{
			type: 'POST',
			url: 'assign_eth_to_bond.php',
			data: 'bond_list='+bond_name+'&eth_list='+eth_string,

			success: function(html)
			{
				$('#response').html(html);
			}
		});
	}

	document.assign_eth.btn_assign.disabled = true;
	disable_all_other_forms('assign_eth');
}

function show_unbonded_eths()
{
	var bond = document.assign_eth.bond_list.value;

	document.assign_eth.action = 'find_eths_for_bond.php?bond='+bond;
	document.assign_eth.submit();
}

function validate_dns_entry(dns_ip)
{
	var dns_option = document.dns_form.use_dns.checked;

	if (dns_option == true)
	{
		dns_error = '';
		var ipPattern;
		
		ipPattern = /^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/;

		var dns_array = dns_ip.match(ipPattern);

		if (dns_ip == "0.0.0.0")
		{
			dns_error = dns_ip+' is not a valid IP';
		}
		
		else if (dns_ip == "255.255.255.255")
		{
			dns_error = dns_ip+' is not a valid IP';
		}

		else if (dns_ip == "")
		{
			dns_error = 'DNS IP is required!';
		}
		
		if (dns_array == null)
		{
			dns_error = 'Enter a valid IP for DNS';
		}

		else if (dns_array != null)
		{
			for (i = 1; i <= 4; i++)
			{
				thisSegment = dns_array[i];

				if (thisSegment > 255)
				{
					dns_error = dns_ip+' is not a valid IP';
					i = 4;
				}
			
				if ((i == 0) && (thisSegment > 255))
				{
					dns_error = dns_ip+' is not a valid IP';
					i = 4;
				}
			}
		}

		if (dns_error != '')
		{
			alert(dns_error);
			return false;
		}

		else
		{
			document.getElementById('wait').style.display = 'block';

			$.ajax(
			{
				type: 'POST',
				url: 'configure_dns.php',
				data: 'dns_value='+document.dns_form.dns_value.value+'&use_dns=on&proceed_page=proceed',

				success: function(html)
				{
					$('#response').html(html);
				}
			});
		}
	}

	else
	{
		document.getElementById('wait').style.display = 'block';

		$.ajax(
		{
			type: 'POST',
			url: 'configure_dns.php',
			data: 'use_dns=false&proceed_page=proceed',

			success: function(html)
			{
				$('#response').html(html);
			}
		});
	}
}

function show_date_time()
{
	var options    = document.getElementsByName('set_mode');
	var time_input = document.getElementById('id_set_time');
	var ntp_id     = document.getElementById('id_ntp_time');

	for (var i = 0;  i < options.length;  i++)
	{
		if (options[i].checked)
		{
			if (options[i].value == 'manual')
			{
				time_input.style.display = 'block';
				ntp_id.style.display     = 'none';
				document.set_time.action_but.disabled = false;
			}

			else if (options[i].value == 'pc_time')
			{	
				time_input.style.display = 'none';
				ntp_id.style.display     = 'none';
				document.set_time.action_but.disabled = false;
			}

			else if (options[i].value == 'ntp_time')
			{
				time_input.style.display = 'none';
				ntp_id.style.display     = 'block';
				document.set_time.action_but.disabled = true;
			}
		}
	}
}

function submit_nas_disk_form()
{
	document.nas_config.submit();
}

function nas_advance_config()

	{
		if(document.getElementById('adv_chk').checked == true)

			{

				 document.getElementById('inpt1_adv1').style.display = 'block';
	                         document.getElementById('inpt2_adv2').style.display = 'block';
				 document.getElementById('adv_txt1').style.display = 'block';
				 document.getElementById('adv_txt2').style.display = 'block';


                         }
	else
		{
				 document.getElementById('inpt1_adv1').style.display = 'none';
	                         document.getElementById('inpt2_adv2').style.display = 'none';
				 document.getElementById('adv_txt1').style.display = 'none';
				 document.getElementById('adv_txt2').style.display = 'none';


		}
	}

function nas_advance_config2()
{
	if(document.getElementById('adv_chk').checked == true)
	{

		 document.getElementById('adv_txt1').style.display = 'block';
	}
        else
        {
                document.getElementById('adv_txt1').style.display = 'none';
	}
}

function set_acl_permission()
{
alert('test');
/*
	if(document.getElementById('set_id').value == 'Acl')
	{
		document.getElementById('id_table').style.display = 'block';
		document.getElementById('id_butt').style.display = 'block';
		document.getElementById('set_id').disabled = true;
	}
	else

	{
		
		document.getElementById('id_table').style.display = 'none';
		document.getElementById('id_butt').style.display = 'none';
		document.getElementById('set_id').disabled = false;
	}*/
}

function validate_snap_schedule()
{
	var snap_file= document.form1.file_name.value

	if(snap_file == 'file_val')
		{
		 jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:24%; padding-top: 4%; font-family: status-bar;">First Select the File</div>', 'Alert Dialog');
                return false;

		}

}
/*
function validate set_path_acl()
{

	var set_path = document.access_control_form.selected_file.value;

	alert(set_path);
	if(set_path == '')
		{
		 jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:24%; padding-top: 4%; font-family: status-bar;">First Set the Path</div>', 'Alert Dialog');
		return false;

		}
}

*/
function validate_set_acl()
{
	   //var avail_user =document.user_acl.ads_user_text.value
	   var select_domain =document.user_acl.domainslist.value
	  //var auth_user = document.getElementById('granted').value
	 var set_path_val = document.getElementById('set_path_id').value;

	/*if(auth_user == '')

		 {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:4%; padding-top: 4%; font-family: status-bar;">Authorised User Cant"t Empty !</div>', 'Auth Alert');
                return false
                }
	*/

        if(set_path_val == '')

                {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:4%; padding-top: 4%; font-family: status-bar;">Go to the First tab and First Set the Path</div>', 'Path Alert');
                return false
                }

	if(select_domain == 'sel_domain')
	{
	 jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:15%; padding-top: 4%; font-family: status-bar;">Select the Domain Name</div>', 'Alert Dialog');
                return false;

	} 

}	

function sched_select_hide()
{
        if(document.getElementById('chk_sch').checked == true)
        {
                document.getElementById('select_id1').style.display = 'none';

                document.getElementById('select_id6').style.display = 'block';
 }

        else
        {
                document.getElementById('select_id1').style.display = 'block';
                document.getElementById('select_id6').style.display = 'none';



        }
}

function sched_select_hide1()
{
        if(document.getElementById('chk1_sch').checked == true)
        {
                document.getElementById('select_id2').style.display = 'none';
                document.getElementById('select_id7').style.display = 'block';

 }

        else
        {
                document.getElementById('select_id2').style.display = 'block';

                document.getElementById('select_id7').style.display = 'none';


        }
}

function sched_select_hide2()
{
        if(document.getElementById('chk2_sch').checked == true)
        {
                document.getElementById('select_id3').style.display = 'none';
                document.getElementById('select_id8').style.display = 'block';
        
 }              
                
        else    
        {       
                document.getElementById('select_id3').style.display = 'block';
                document.getElementById('select_id8').style.display = 'none';
                
                
                
        }
}

function sched_select_hide3()
{
        if(document.getElementById('chk3_sch').checked == true)
        {
                document.getElementById('select_id4').style.display = 'none';
                document.getElementById('select_id9').style.display = 'block';
        
 }              
                
        else    
        {       
                document.getElementById('select_id4').style.display = 'block';
                
                document.getElementById('select_id9').style.display = 'none';
                
                
        }
}

function sched_select_hide4()
{
        if(document.getElementById('chk4_sch').checked == true)
        {
                document.getElementById('select_id5').style.display = 'none';

                document.getElementById('select_id10').style.display = 'block';
 }

        else
        {
                document.getElementById('select_id5').style.display = 'block';

                document.getElementById('select_id10').style.display = 'none';


        }
}

function snap_select_hide()
{
        if(document.getElementById('chk').checked == true)
        {
                document.getElementById('select_id1').style.display = 'none';

                document.getElementById('select_id6').style.display = 'block';
 }

        else
        {
                document.getElementById('select_id1').style.display = 'block';
                document.getElementById('select_id6').style.display = 'none';



        }
}

function snap_select_hide1()
{
        if(document.getElementById('chk1').checked == true)
        {
                document.getElementById('select_id2').style.display = 'none';
                document.getElementById('select_id7').style.display = 'block';

 }

        else
        {
                document.getElementById('select_id2').style.display = 'block';

                document.getElementById('select_id7').style.display = 'none';


        }
}

function snap_select_hide2()
{
        if(document.getElementById('chk2').checked == true)
        {
                document.getElementById('select_id3').style.display = 'none';
                document.getElementById('select_id8').style.display = 'block';
        
 }              
                
        else    
        {       
                document.getElementById('select_id3').style.display = 'block';
                document.getElementById('select_id8').style.display = 'none';
                
                
                
        }
}
function snap_select_hide3()
{
        if(document.getElementById('chk3').checked == true)
        {
                document.getElementById('select_id4').style.display = 'none';
                document.getElementById('select_id9').style.display = 'block';
        
 }              
                
        else    
        {       
                document.getElementById('select_id4').style.display = 'block';
                
                document.getElementById('select_id9').style.display = 'none';
                
                
        }
}

function snap_select_hide4()
{
        if(document.getElementById('chk4').checked == true)
        {
                document.getElementById('select_id5').style.display = 'none';

                document.getElementById('select_id10').style.display = 'block';
 }

        else
        {
                document.getElementById('select_id5').style.display = 'block';

                document.getElementById('select_id10').style.display = 'none';


        }
}


function sched_shutdown_hide()
{
        if(document.getElementById('chk').checked == true)
        {
                document.getElementById('select_id1').style.display = 'none';

                document.getElementById('select_id6').style.display = 'block';
 }

        else
        {
                document.getElementById('select_id1').style.display = 'block';
                document.getElementById('select_id6').style.display = 'none';



        }
}

function sched_shutdown_hide1()
{
        if(document.getElementById('chk1').checked == true)
        {
                document.getElementById('select_id2').style.display = 'none';
                document.getElementById('select_id7').style.display = 'block';

 }

        else
        {
                document.getElementById('select_id2').style.display = 'block';

                document.getElementById('select_id7').style.display = 'none';


        }
}

function sched_shutdown_hide2()
{
        if(document.getElementById('chk2').checked == true)
        {
                document.getElementById('select_id3').style.display = 'none';
                document.getElementById('select_id8').style.display = 'block';
        
 }              
                
        else    
        {       
                document.getElementById('select_id3').style.display = 'block';
                document.getElementById('select_id8').style.display = 'none';
                
                
                
        }
}
function sched_shutdown_hide3()
{
        if(document.getElementById('chk3').checked == true)
        {
                document.getElementById('select_id4').style.display = 'none';
                document.getElementById('select_id9').style.display = 'block';
        
 }              
                
        else    
        {       
                document.getElementById('select_id4').style.display = 'block';
                
                document.getElementById('select_id9').style.display = 'none';
                
                
        }
}

function sched_shutdown_hide4()
{
        if(document.getElementById('chk4').checked == true)
        {
                document.getElementById('select_id5').style.display = 'none';

                document.getElementById('select_id10').style.display = 'block';
 }

        else
        {
                document.getElementById('select_id5').style.display = 'block';

                document.getElementById('select_id10').style.display = 'none';


        }
}


function sched_restart_hide()
{
        if(document.getElementById('chk').checked == true)
        {
                document.getElementById('select_id1').style.display = 'none';

                document.getElementById('select_id6').style.display = 'block';
 }

        else
        {
                document.getElementById('select_id1').style.display = 'block';
                document.getElementById('select_id6').style.display = 'none';



        }
}

function sched_restart_hide1()
{
        if(document.getElementById('chk1').checked == true)
        {
                document.getElementById('select_id2').style.display = 'none';
                document.getElementById('select_id7').style.display = 'block';

 }

        else
        {
                document.getElementById('select_id2').style.display = 'block';

                document.getElementById('select_id7').style.display = 'none';


        }
}

function sched_restart_hide2()
{
        if(document.getElementById('chk2').checked == true)
        {
                document.getElementById('select_id3').style.display = 'none';
                document.getElementById('select_id8').style.display = 'block';
        
 }              
                
        else    
        {       
                document.getElementById('select_id3').style.display = 'block';
                document.getElementById('select_id8').style.display = 'none';
                
                
                
        }
}
function sched_restart_hide3()
{
        if(document.getElementById('chk3').checked == true)
        {
                document.getElementById('select_id4').style.display = 'none';
                document.getElementById('select_id9').style.display = 'block';
        
 }              
                
        else    
        {       
                document.getElementById('select_id4').style.display = 'block';
                
                document.getElementById('select_id9').style.display = 'none';
                
                
        }
}

function sched_restart_hide4()
{
        if(document.getElementById('chk4').checked == true)
        {
                document.getElementById('select_id5').style.display = 'none';

                document.getElementById('select_id10').style.display = 'block';
 }

        else
        {
                document.getElementById('select_id5').style.display = 'block';

                document.getElementById('select_id10').style.display = 'none';


        }
}





function create_text()
{
        if(document.getElementById('chk').checked == true)
	{
		document.getElementById('txt').style.display = 'block';
		document.getElementById('txt1').style.display = 'block';
		document.rotate_log.create_value.style.display='block';
		document.getElementById('inpt').style.display = 'block';
		document.getElementById('inpt1').style.display = 'block';
		//document.rotate_log.check.disabled=true;
		document.rotate_log.fetch_info.disabled=true;
		document.rotate_log.submit_rotate_log.disabled=true;
		document.rotate_log.fetch_info.style.display='none';
		document.rotate_log.submit_rotate_log.style.display='none';
		document.getElementById('conf_dis').style.display = 'none';
		document.getElementById('conf_file_dis').style.display = 'none';
		document.getElementById('conf_name_hide').style.display = 'none';
		document.getElementById('hid_allfile').style.display = 'none';
		document.rotate_log.avail_users.disabled=true;
	}

        else
	{
		document.getElementById('txt').style.display = 'none';
		document.getElementById('txt1').style.display = 'none';
		document.rotate_log.create_value.style.display='none';
		document.getElementById('inpt').style.display = 'none';
		document.getElementById('inpt1').style.display = 'none';
		

		//document.rotate_log.check.disabled=false;
		document.rotate_log.fetch_info.disabled=false;
		document.rotate_log.submit_rotate_log.disabled=false;
		document.rotate_log.fetch_info.style.display='block';
		document.rotate_log.submit_rotate_log.style.display='block';
		document.getElementById('conf_dis').style.display = 'block';
		document.getElementById('conf_file_dis').style.display = 'block';
		document.getElementById('conf_name_hide').style.display = 'block';
		document.getElementById('hid_allfile').style.display = 'block';
		 document.rotate_log.avail_users.disabled=false;


		
	}
}

function rotate_log_disable()
{

	if (document.rotate_log.check.checked)
	{
		document.rotate_log.avail_users.disabled=true;
		document.rotate_log.chk.disabled=true;
		document.rotate_log.fetch_info.disabled=true;
		//document.rotate_log.submit_rotate_log.disabled=true;
	}

	else
	{
		document.rotate_log.avail_users.disabled=false;
		document.rotate_log.chk.disabled=false;
		document.rotate_log.fetch_info.disabled=false;
		//document.rotate_log.submit_rotate_log.disabled=false;

	}
}

function fetch_log()
{
	var fetch_log_value = document.rotate_log.avail_users.value;
	var fetch_check_value = document.rotate_log.check.checked;

	if (fetch_check_value != true)
	{
		if(fetch_log_value == '')
		{

			jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:-5%; padding-top: 4%; font-family: status-bar;"> Please select Configuration Name.</div>', 'Log Alert');

                	document.rotate_log.avail_users.focus();
                	return false;
        	}
	}
}

function validate_create_rotate_configuration()
{
        var new_rotate = document.rotate_log.inpt.value;
        var rotate_path =document.rotate_log.inpt1.value;
	var freq_gb = document.rotate_log.set_freq.value;
	var select_log_rotate = document.rotate_log.freq_rotate.value;
	var log_size = document.rotate_log.size.value;

        if (new_rotate == '')
        {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 0%; padding-top: 4%; font-family: status-bar;"> Configuration Name is required.</div>', 'Log Alert');

                document.rotate_log.inpt.focus();
                return false;
        }

        if (rotate_path == '')
        {

                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 0%; padding-top: 4%; font-family: status-bar;"> Configuration Path is required.</div>', 'Log Alert');
                document.rotate_log.inpt1.focus();
                return false;

        }

	if (freq_gb == '')
	{
		 jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 28%; padding-top: 4%;" font-family: status-bar;"> Frequency is required.</div>', 'Log Alert');
		document.rotate_log.set_freq.focus();
		return false;

	}
	
	if (select_log_rotate == '')
	{
		   jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 21%; padding-top: 4%;" font-family: status-bar;"> Log Rotate Frequency is required.</div>', 'Log Alert');
                document.rotate_log.freq_rotate.focus();
                return false;
	}

	if (log_size == '')
        {
                   jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 34%; padding-top: 4%;" font-family: status-bar;"> Log Size is required.</div>', 'Log Alert');
                document.rotate_log.size.focus();
                return false;
        }
}

function validate_increase_size()
{
	var increase_size= document.add_disk.update_size.value

	if(increase_size == '')
	{
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 17%; padding-top: 4%; font-family: status-bar;"> Increase Size is required.</div>', 'Log Alert');
		document.add_disk.update_size.focus
		return false;
	}
}

function validate_fio_image()
{
	var select_volume = document.create_image.volume_con.value;
	var  create_images = document.create_image.img_name.value;
	var  image_size = document.create_image.img_size.value;

	if (select_volume == 'select-container')
        {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 36%; padding-top: 4%; font-family: status-bar;"> Select Container</div>', 'Container Alert');
                document.create_image.volume_con.focus();
                return false;
        }

if (create_images == '')

        {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 32%; padding-top: 4%; font-family: status-bar;">Enter Image Name</div>', 'Image Alert');
                document.create_image.img_name.focus();
                return false;
        }

if (image_size == '')

        {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 32%; padding-top: 4%; font-family: status-bar;">Enter Image Size</div>', 'Image Alert');
                document.create_image.img_size.focus();
                return false;
        }
}

function validate_remove_container()
{
	var select_volume = document.remove_container.volume.value

	if (select_volume == 'select-volume')
        {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:15%; padding-top: 4%; font-family: status-bar;"> Select Container to remove.</div>', 'Container Alert');
                document.remove_container.volume.focus();
                return false;
        }
}

function validate_remove_image()
{
        var select_volume = document.remove_image.volume_con_rm.value

	if (select_volume == 'select-container')
        {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:15%; padding-top: 4%; font-family: status-bar;"> Select Container to remove Image.</div>', 'Alert Dialog');
                document.remove_image.volume_con_rm.focus();
                return false;
        }
}

function validate_fio_container()
{
	var select_volume = document.create_container.volume.value;
	var  create_cont = document.create_container.container_name.value;
	var  container_size = document.create_container.container_size.value;

	if (select_volume == 'select-volume')
        {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 36%; padding-top: 4%; font-family: status-bar;"> Select Volume</div>', 'Alert Dialog');
                document.create_container.volume.focus();
                return false;
        }

	if (create_cont == '')
        {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 15%; padding-top: 4%; font-family: status-bar;">Enter Container Name</div>', 'Alert Dialog');
                document.create_container.container_name.focus();
                return false;
        }

	if ((create_cont / 1) <= 0 || (create_cont / 1) > 0)
        {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 20%; padding-top: 4%; font-family: status-bar;">Disk name should be Alpha numeric!</div>', 'Alert Dialog');
                return false;
        }

        if(create_cont.length > 8)
        {
                jAlert("<img src='../images/info.gif'><div style='float: right; margin-right: 20%; padding-top: 4%; font-family: status-bar;'>Your Container Name can't be more than 8 Character!</div>", 'Alert Dialog');
                document.create_container.container_name.focus();
                return false;
        }

        if (create_cont.indexOf(' ') >= 0)
        {

                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 20%; padding-top: 4%; font-family: status-bar;">Spaces not allowed in Container name!</div>', 'Alert Dialog');
                return false;
        }

	if (container_size == '')
        {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 15%; padding-top: 4%; font-family: status-bar;"> Enter Container Size</div>', 'Alert Dialog');
                document.create_container.container_size.focus();
                return false;
        }
}

function validate_san_remove()
{
	var  san_nm = document.getElementsByName('san_name');
	var checkoptions = document.getElementsByName('select_disk_rm');
	var optstring = '';

	for (i = 0;  i < checkoptions.length;  i++)
	{
		if (checkoptions[i].checked == true)
		{
			optstring += checkoptions[i].value;
		}
	}

	if (optstring == '')
	{
		//alert('Choose either "BIO" or "FIO"');

		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:23 %; padding-top: 4%; font-family: status-bar;">Choose either "BIO" or "FIO"</div>', 'Alert Dialog');

		return false;
	}

	//return false;
}

function validate_add_to_san()
{
	var name = document.getElementById("s_name");
	var select_size = document.getElementById("select_block");

	alert(name.value);
	if(name.value == '')
	{
		alert("Enter SAN Name!");
		return false;
	}

	if(select_size.value == 'select-size')
	{
		alert("Select Block Size!");
		return false;
	}
}

function validate_san_configuration()
{

	//var checkoptions = document.add_group.select_disk.checked;
	var bio_checked = document.getElementById("bio_chk").checked;
	var fio_checked = document.getElementById("fio_chk").checked;
	var select_volume = document.add_group.select_block.value;	
	var  san_nm = document.add_group.san_name.value;


	if ((bio_checked == false) && (fio_checked == false))
	{
		//alert('Choose either "BIO" or "FIO"');

		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:23 %; padding-top: 4%; font-family: status-bar;">Choose either "BIO" or "FIO"</div>', 'Alert Dialog');

		return false;
	}

	if (san_nm == '')
        {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:40%; padding-top: 4%; font-family: status-bar;">Enter SAN Name</div>', 'Alert Dialog');
                //document.del_group.san_name.focus();
                return false;
        }

if ((san_nm / 1) <= 0 || (san_nm / 1) > 0)
        {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 20%; padding-top: 4%; font-family: status-bar;">San name should be Alpha numeric!</div>', 'Alert Dialog');
                return false;
        }

        if(san_nm.length > 8)

        {
                jAlert("<img src='../images/info.gif'><div style='float: right; margin-right: 20%; padding-top: 4%; font-family: status-bar;'>Your SAN Name can't be more than 8 Character!</div>", 'Alert Dialog');
                document.add_group.san_name.focus();
                return false;
        }


        if (san_nm.indexOf(' ') >= 0)

        {

                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 20%; padding-top: 4%; font-family: status-bar;">Spaces not allowed in SAN name!</div>', 'Alert Dialog');
                return false;
        }


if (select_volume == 'option_block')

        {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 36%; padding-top: 4%; font-family: status-bar;"> Select Block Size</div>', 'Alert Dialog');
                document.add_group.select_block.focus();
                return false;
        }

}

function validate_bio_configuration()
{
	var free_size= document.bio_config.free_size2.value

	free_size = free_size.replace("GB", "")
	free_size = parseFloat(free_size);
			 
	var size_type =/^(^\d*.?\d*[1-9]+\d*$)|(^[1-9]+\d*.\d*$)$/;
	var disk  = document.bio_config.disk.value;
	var size  = document.bio_config.size.value;
	//var gb_mb = document.nas_config.gb_mb.value;
	
	if (disk == '')
	{
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 36%; padding-top: 4%; font-family: status-bar;"> Disk is required.</div>', 'Alert Dialog');
		document.bio_config.disk.focus();
		return false;
	}
	
	if ((disk / 1) <= 0 || (disk / 1) > 0)
	{
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 20%; padding-top: 4%; font-family: status-bar;">Disk name should be Alpha numeric!</div>', 'Alert Dialog');
		return false;
	}
	
	if(disk.length > 8)
	{
		jAlert("<img src='../images/info.gif'><div style='float: right; margin-right: 20%; padding-top: 4%; font-family: status-bar;'>Your Disk Name can't be more than 8 Character!</div>", 'Alert Dialog');
		document.bio_config.disk.focus();
		return false;
	}
	
	if (disk.indexOf(' ') >= 0)
	{

		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 20%; padding-top: 4%; font-family: status-bar;">Spaces not allowed in disk name!</div>', 'Alert Dialog');
		return false;
	}

	if (size == '')
	{
		
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 36%; padding-top: 4%; font-family: status-bar;"> Size is required.</div>', 'Alert Dialog');
		document.bio_config.size.focus();
		return false;
	}

	if (size < 10)
        {

                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:20%; padding-top: 4%; font-family: status-bar;">Please Enter Atleast 10Gb of size.</div>', 'Alert Dialog');
                document.bio_config.size.focus();
                return false;
        }

	if(size > free_size)
	{
	 
	   jAlert("<img src='../images/info.gif'><div style='float: right; margin-right: 15%; padding-top: 4%; font-family: status-bar;'> You Can't Enter more than Available Size!.</div>", 'Alert Dialog');
	   //alert('Entered size can\'t be more than available size!');
	   document.bio_config.size.focus();	
	   return false;
	}

	/*if (gb_mb == 'select')
	{
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 36%; padding-top: 4%; font-family: status-bar;"> Select Size units</div>', 'Alert Dialog');
		document.nas_config.gb_mb.focus();
		return false;
	}*/
}

function validate_vtl_configuration()
{
	var free_size= document.vtl_config.free_size2.value

	free_size = free_size.replace("GB", "")
	free_size = parseFloat(free_size);
			 
	var size_type =/^(^\d*.?\d*[1-9]+\d*$)|(^[1-9]+\d*.\d*$)$/;
	var disk  = document.vtl_config.disk.value;
	var size  = document.vtl_config.size.value;
	//var gb_mb = document.nas_config.gb_mb.value;

	if (disk == '')
	{
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 36%; padding-top: 4%; font-family: status-bar;"> Disk is required.</div>', 'Alert Dialog');

		document.vtl_config.disk.focus();
		return false;
	}
	
	if ((disk / 1) <= 0 || (disk / 1) > 0)
	{
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 20%; padding-top: 4%; font-family: status-bar;">Disk name should be Alpha numeric!</div>', 'Alert Dialog');
		return false;
	}
	
	if(disk.length > 8)
	{
		jAlert("<img src='../images/info.gif'><div style='float: right; margin-right: 20%; padding-top: 4%; font-family: status-bar;'>Your Disk Name can't be more than 8 Character!</div>", 'Alert Dialog');
		document.vtl_config.disk.focus();
		return false;
	}
	
	if (disk.indexOf(' ') >= 0)
	{

		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 20%; padding-top: 4%; font-family: status-bar;">Spaces not allowed in disk name!</div>', 'Alert Dialog');
		return false;
	}

	if (size == '')
	{
		
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 36%; padding-top: 4%; font-family: status-bar;"> Size is required.</div>', 'Alert Dialog');
		document.vtl_config.size.focus();
		return false;
	}

	if(size > free_size)
	{
	 
	   jAlert("<img src='../images/info.gif'><div style='float: right; margin-right: 15%; padding-top: 4%; font-family: status-bar;'> You Can't Enter more than Available Size!.</div>", 'Alert Dialog');
	   document.vtl_config.size.focus();	
	   return false;
	}

	/*if (gb_mb == 'select')
	{
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 36%; padding-top: 4%; font-family: status-bar;"> Select Size units</div>', 'Alert Dialog');
		document.nas_config.gb_mb.focus();
		return false;
	}*/
}

function validate_snapshot_schedule_rem()

{
var disk_name=  document.form1.disk_name.value;

if(disk_name == 'disk_val')

                {
                        jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:12%; padding-top: 4%; font-family: status-bar;">First select the disk name</div>', 'Alert Dialog');
                return false;
                }

}

function validate_snapshot_schedule()
{

	var disk_name=  document.form1.disk_name.value;
	var free_size = document.form1.free_vol.value; 
	free_size = free_size.replace("GB", "")
        free_size = parseFloat(free_size);
	var snap_name = document.form1.snap_name.value; 
	var chk_name = /^[A-Za-z0-9 ]{3,20}$/;
	var snap_max = document.form1.max_snap.value; 
	var snap_size = document.form1.snap_size.value; 
	var sp_chars   = "\ \ !@#$%^&*()+=-[]\\\';,/{}|\":<>?`~";


	if(disk_name == 'disk_val')

		{
			jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:12%; padding-top: 4%; font-family: status-bar;">First select the disk name</div>', 'Snapshot Alert');
                return false;
		}
	
	if(snap_name == '')
        {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:25%; padding-top: 4%; font-family: status-bar;">Enter the Snap Name</div>', 'Snapshot Alert');
                return false;

        }


	if(snap_name.length != 6)
        {
                jAlert("<img src='../images/info.gif'><div style='float: right; margin-right:4%; padding-top: 4%; font-family: status-bar;'>Snapshot name should always be 6 characters</div>", 'Snapshot Alert');
                return false;
        }

	var iChars = "!@#$%^&*()+=-[]_\\\';,./{}|\":<>?";

  for (var i = 0; i < snap_name.length; i++) {
        if (iChars.indexOf(snap_name.charAt(i)) != -1) {
        //alert ("Your username has special characters. \nThese are not allowed.\n Please remove them and try again.");
	 jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:15%; padding-top: 4%; font-family: status-bar;">Special Character not allowed</div>', 'Snapshot Alert');
        return false;
        }
  }

	//if(snap_name.match(sp_chars))
	/*if (sp_chars.indexOf(snap_name))
        {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:15%; padding-top: 4%; font-family: status-bar;">Special Character not allowed</div>', 'Alert Dialog');
                return false;

        }*/

	if(snap_max == '')
	{
	 	jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:25%; padding-top: 4%; font-family: status-bar;">Enter the Max Snap</div>', 'Snapshot Alert');
                return false;

	}

	if(snap_size == '')
        {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family: status-bar;">Enter the Snap size</div>', 'Snapshot Alert');
                return false;

        }
	if(snap_size > free_size)
        {

           jAlert("<img src='../images/info.gif'><div style='float: right; margin-right: 15%; padding-top: 4%; font-family: status-bar;'> You Can't Enter more than Available Size!.</div>", 'Snapshot Alert');
           return false;
        }


}

function validate_schedule_log()
{
	var select_day= document.autoschedulelogs.freq.value
	
	if(select_day == 'sel_day')
	{
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:18%; padding-top: 4%; font-family: status-bar;">Please select the Day !</div>', 'Alert Dialog');
                return false;
	}
	
	
}



function validate_nas_configuration()
{
	var free_size= document.nas_config.free_size2.value

	free_size = free_size.replace("GB", "")
	free_size = parseFloat(free_size);
			 
	var size_type =/^(^\d*.?\d*[1-9]+\d*$)|(^[1-9]+\d*.\d*$)$/;
	var disk  = document.nas_config.disk.value;
	var size  = document.nas_config.size.value;
	//var gb_mb = document.nas_config.gb_mb.value;

	if (disk == '')
	{
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 36%; padding-top: 4%; font-family: status-bar;"> Disk is required.</div>', 'Disk Dialog');

		document.nas_config.disk.focus();
		return false;
	}
	
	if ((disk / 1) <= 0 || (disk / 1) > 0)
	{
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 20%; padding-top: 4%; font-family: status-bar;">Disk name should be Alpha numeric!</div>', 'Disk Dialog');
		return false;
	}
	
	if(disk.length > 8)
	{
		jAlert("<img src='../images/info.gif'><div style='float: right; margin-right: 20%; padding-top: 4%; font-family: status-bar;'>Your Disk Name can't be more than 8 Character!</div>", 'Disk Dialog');
		document.nas_config.disk.focus();
		return false;
	}
	
	if (disk.indexOf(' ') >= 0)
	{

		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 20%; padding-top: 4%; font-family: status-bar;">Spaces not allowed in disk name!</div>', 'Disk Dialog');
		return false;
	}

	if (size == '')
	{
		
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 36%; padding-top: 4%; font-family: status-bar;"> Size is required.</div>', 'Disk Dialog');
		document.nas_config.size.focus();
		return false;
	}

	 if (size < 10)
        {

                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:20%; padding-top: 4%; font-family: status-bar;">Please Enter Atleast 10Gb of size.</div>', 'Size Dialog');
                document.nas_config.size.focus();
                return false;
        }

	
	if(size > free_size)
	{
	 
	   jAlert("<img src='../images/info.gif'><div style='float: right; margin-right: 15%; padding-top: 4%; font-family: status-bar;'> You Can't Enter more than Available Size!.</div>", 'Disk Dialog');
	   document.nas_config.size.focus();	
	   return false;
	}

	/*if (gb_mb == 'select')
	{
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 36%; padding-top: 4%; font-family: status-bar;"> Select Size units</div>', 'Alert Dialog');
		document.nas_config.gb_mb.focus();
		return false;
	}*/
}


function validate_block_configuration()
{
	
	var free_size= document.nas_config.free_size.value
	free_size =free_size.replace("GB", "")
	    
	//alert(free_size)
	
	free_size = parseFloat(free_size);
			 
	var size_type =/^(^\d*.?\d*[1-9]+\d*$)|(^[1-9]+\d*.\d*$)$/;
	var disk = document.nas_config.disk.value;
	var size = document.nas_config.size.value;
	//size = parseFloat(size);
	//size = parseInt(size);
	//alert(size);
	var gb_mb =document.nas_config.gb_mb.value;
	//var intRegex = /^\d+$/;

	if (disk == '')
	{
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 36%; padding-top: 4%; font-family: status-bar;"> Disk is required.</div>', 'Alert Dialog');

		document.nas_config.disk.focus();
		return false;
	}
	

	if ((disk / 1) <= 0 || (disk / 1) > 0)
	{
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 20%; padding-top: 4%; font-family: status-bar;">Disk name should be Alpha numeric!</div>', 'Alert Dialog');
		return false;
	}
	
	if(disk.length > 8)
	{
		jAlert("<img src='../images/info.gif'><div style='float: right; margin-right: 20%; padding-top: 4%; font-family: status-bar;'>Your Disk Name can't be more than 8 Character!</div>", 'Alert Dialog');
		document.nas_config.disk.focus();
		return false;
	}
	
	if (disk.indexOf(' ') >= 0)
	{

		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 20%; padding-top: 4%; font-family: status-bar;">Spaces not allowed in disk name!</div>', 'Alert Dialog');
		return false;
	}

	if (size == '')
	{
		
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 36%; padding-top: 4%; font-family: status-bar;"> Size is required.</div>', 'Alert Dialog');
		document.nas_config.size.focus();
		return false;
	
	}

	if(size > free_size)
	{
	 
	   jAlert("<img src='../images/info.gif'><div style='float: right; margin-right: 15%; padding-top: 4%; font-family: status-bar;'> You Can't Enter more than Available Size!.</div>", 'Alert Dialog');
	   document.nas_config.size.focus();	
	   return false;
	}

	if (gb_mb == 'select')
	{
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 36%; padding-top: 4%; font-family: status-bar;"> Select Size units</div>', 'Alert Dialog');
		document.nas_config.gb_mb.focus();
		return false;
	}
}

function validate_mail_configuration()
{
	var server_nm = document.mail_form.server_name.value;
	var auth_nm = document.mail_form.select_auth.value;
	var port_nm = document.mail_form.port_name.value;
	var tsl_nm = document.mail_form.select_tsl.value;
	var user_nm = document.mail_form.user_name.value;
	var from_nm = document.mail_form.from_email.value;
	var password_nm = document.mail_form.user_pass.value;
	var to_nm = document.mail_form.to_mail.value;

	var chk_server_filter = /^([a-zA-Z0-9_\.\-])+(\.)+([a-zA-Z0-9]{2,4})+$/;
	var filter = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;

	if(server_nm == "")
	{
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:0; padding-top: 4%; font-family: status-bar;">Please enter a server name</div>', 'Mail Alert');
		return false;
	}
	if(!chk_server_filter.test(server_nm))
	{
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:16%; padding-top: 4%; font-family: status-bar;">Please enter a valid server name</div>', 'Mail Alert ');
                return false;
	}
	
	if(auth_nm == 'select_auth_val')
	{
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:27%; padding-top: 4%; font-family: status-bar;"> Please select an authentication option</div>', 'Mail Alert');
                return false;
	}

	if(port_nm == "")
	{
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:29%; padding-top: 4%; font-family: status-bar;">Please specify the port</div>', 'Mail Alert');
                return false;
	}

	 if(port_nm > 65536)
        {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:29%; padding-top: 4%; font-family: status-bar;">Please enter a valid Port Number</div>', 'Mail Alert');
                return false;
        }

	if(tsl_nm == 'select_tsl_val')
        {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:56%; padding-top: 4%; font-family: status-bar;">Please select one of the TLS options</div>', 'Mail Alert');
                return false;
        }
	if(from_nm == "")
        {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 30%; padding-top: 4%; font-family: status-bar;">Please Enter the From name</div>', 'Mail Alert');
                return false;
        }
        if (!filter.test(from_nm))

        {

                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:29%; padding-top: 4%; font-family: status-bar;">Please enter the from value in the correct format</div>', 'Mail Alert');
                return false;
        }

	if(auth_nm == 'on')
	{
	 if(user_nm == "")
        {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:29%; padding-top: 4%; font-family: status-bar;">Please Enter the Username</div>', 'Mail Alert');
                return false;
        }

	}
	/*
	if (!filter.test(user_nm))
	
	{

		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:30%; padding-top: 4%; font-family: status-bar;">Please Enter the valid Username</div>', 'Mail Alert');
                return false;
	}

	*/
	 if(auth_nm == 'on')
        {
 
	 if(password_nm == "")
        {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:12%; padding-top: 4%; font-family: status-bar;">Please Enter the Password</div>', 'Mail Alert');
                return false;
        }
	}
	if(to_nm == "")
        {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 36%; padding-top: 4%; font-family: status-bar;">Field Can not be Blank</div>', 'Mail Alert');
                return false;
        }

	 if (!filter.test(to_nm))

        {

                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:29%; padding-top: 4%; font-family: status-bar;">Please enter the to value in the correct format</div>', 'Mail Alert');
                return false;
        }

}

function validate_chk_server_nm()
{
        var server_nm = document.mail_form.server_name.value;
	var chk_server_filter = /^([a-zA-Z0-9_\.\-])+(\.)+([a-zA-Z0-9]{2,4})+$/;

	if(server_nm == "")
        {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:0; padding-top: 4%; font-family: status-bar;">Please Enter the Server name</div>', 'Mail Alert');
                return false;
        }

	 if(!chk_server_filter.test(server_nm))
        {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:16%; padding-top: 4%; font-family: status-bar;">Please Enter the valid Server name</div>', 'Alert Dialog');
                return false;
        }
}

function validate_ethernet_details()
{
        var ipaddress = document.change_network.ipaddress.value;
        var netmask = document.change_network.netmask.value;

        if (ipaddress == '')
        {
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 11%; padding-top: 4%; font-family: status-bar;">IP Address cannot be blank</div>', 'Alert Dialog');


                document.change_network.ipaddress.focus();
                return false;
        }

        error = validate_access_ip(ipaddress);

        if (error != '')

        {
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 11%; padding-top: 4%; font-family: status-bar;">Please Select a valid Ip Address</div>', 'Alert Dialog');
                document.change_network.ipaddress.focus();
                document.change_network.ipaddress.value='';
                return false;
        }

        if (netmask == '')
        {
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 11%; padding-top: 4%; font-family: status-bar;">Netmask cannot be blank </div>', 'Alert Dialog');
		

                //alert('Netmask cannot be blank!');
                document.change_network.netmask.focus();
                return false;
        }

        error = validate_netmask(netmask);

        if (error != '')
        {
                //alert(error)
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 11%; padding-top: 4%; font-family: status-bar;">Please select a valid Netmask</div>', 'Alert Dialog');
                document.change_network.netmask.focus();
                document.change_network.netmask.value='';
                return false;
        }

}

function dns_form_validation()
{

	var pdns = document.dns_form.pdns.value;
	var sdns = document.dns_form.sdns.value;

	if((pdns=='') && (sdns!=''))
	{
		alert("You can't add secondary DNS without adding primary DNS!");
		document.dns_form.pdns.focus();
		return false;
	}

}

function retain_status()
{
	var options = document.getElementsByName('set_mode');
	var time_input = document.getElementById('id_set_time');
	var hid_session_user = document.set_time.hid_session_user.value;

	if (hid_session_user != 'Full Access')
	{
		var form_count = document.forms.length;

		for (i = 0;  i < form_count;  i++)
		{
			var elem_count = document.forms[i].elements.length;

			for (j = 0;  j < elem_count;  j++)
			{
				document.forms[i].elements[j].disabled = true;
			}
		}
	}
		
	for (var i = 0;  i < options.length;  i++)
	{
		if (options[i].checked)
		{
			if (options[i].value == 'manual')
			{
				time_input.style.display = 'block';
			}

			else
			{
				time_input.style.display = 'none';
			}
		}
	}
}


function create_hid_date()
{
	var cur_date = new Date();

	var month=new Array();
	month[0]="Jan";
	month[1]="Feb";
	month[2]="Mar";
	month[3]="Apr";
	month[4]="May";
	month[5]="Jun";
	month[6]="Jul";
	month[7]="Aug";
	month[8]="Sep";
	month[9]="Oct";
	month[10]="Nov";
	month[11]="Dec";

	var date  = cur_date.getDate();
	var month2 = month[cur_date.getMonth()];
	var year  = cur_date.getFullYear();
	var hours = cur_date.getHours();
	var mins  = cur_date.getMinutes();
	var secn  = cur_date.getSeconds();

	var cur_date_time = date+'-'+month2+'-'+year+' '+hours+':'+mins+':'+secn;
	document.set_time.hid_pc_time.value = cur_date_time;

}

function validate_apply_new_date()
{
	var date_val = document.set_time.setDate.value;
	if(date_val == '')
	{
		//alert("Please select date from calendar!");
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:16%; padding-top: 4%; font-family: status-bar;">Please select date from calendar</div>', 'Date  Alert ');
		return false;
	}
}

function validate_date_time_form()
{
	var options = document.getElementsByName('set_mode');
	var date_val = document.set_time.setDate.value;
	var ntp_server = document.set_time.ntp_server.value;

	for (var i = 0;  i < options.length;  i++)
	{
		if (options[i].checked)
		{
			if (options[i].value == 'manual')
			{
				if (date_val == '')
				{
					alert('Please choose a date from the date picker!');
					return false;
				}

				else
				{
					var date_pattern = /^(\d{1,2})\-(\d{1,2})\-(\d{4})\ (\d{1,2}):(\d{1,2}):(\d{1,2})$/;
					correct_date = date_val.match(date_pattern);

					/*if (correct_date == null)
					{
						alert('Please enter date in proper format!');
						document.set_time.new_date.value = '';
						return false;
					}*/

					//else
					//{
						/*waitid.style.display = 'block';

						$.ajax(
						{
							type: 'POST',
							url: 'set_date_time.php',
							data: 'new_date='+date_val+'&mode=manual&hid_curdate='+document.set_time.hid_curdate.value+'&hid_curtime='+document.set_time.hid_curtime.value,

							success: function(html)
							{
								$('#response').html(html);
							}
						});*/
					//}
				}
			}

			else if (options[i].value == 'pc_time')
			{
				var cur_date = new Date();

				var month=new Array();
				month[0]="Jan";
				month[1]="Feb";
				month[2]="Mar";
				month[3]="Apr";
				month[4]="May";
				month[5]="Jun";
				month[6]="Jul";
				month[7]="Aug";
				month[8]="Sep";
				month[9]="Oct";
				month[10]="Nov";
				month[11]="Dec";

				var date  = cur_date.getDate();
				var month2 = month[cur_date.getMonth()];
				var year  = cur_date.getFullYear();
				var hours = cur_date.getHours();
				var mins  = cur_date.getMinutes();
				var secn  = cur_date.getSeconds();

				var cur_date_time = date+'-'+month2+'-'+year+' '+hours+':'+mins+':'+secn;
				document.set_time.hid_pc_time.value = cur_date_time;

			}

			else if(options[i].value == 'ntp_time')
			{
				if (ntp_server == '')
                                {
                                        //alert('Please enter a valid ntp server address!');
					jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:29%; padding-top: 4%; font-family: status-bar;">Please enter a valid ntp server address</div>', 'NTP Alert ');
                                        return false;
                                }
			}
		}
	}

	document.set_time.submit();
}

function run_ntp_sync(sync_ntp)
{
	var wait_id = document.getElementById('wait');

	if (sync_ntp == true)
	{
		var ntp_server = document.set_time.ntp_server.value;

		if (ntp_server == '')
		{
			//alert('Please enter a valid ntp server address!');
			jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:29%; padding-top: 4%; font-family: status-bar;">Please enter a valid ntp server address</div>', 'NTP Alert ');
			return false;
		}

		//wait_id.style.display = 'block';

		location.href = 'set_date_time.py?sync_option='+sync_ntp+'&mode=ntp_time&ntp_server='+ntp_server;

		/*$.ajax(
		{
			type: 'POST',
			url: 'set_date_time.py',
			data: 'sync_option='+sync_ntp+'&mode=ntp_time&ntp_server='+ntp_server,

			success: function(html)
			{
				$('#response').html(html);
			}
		});*/
	}
}

function sync_ntp_server(sync_ntp)
{
	if(sync_ntp == "Enter NTP Server Name")
	{
		//alert("Please enter a valid ntp server address!");
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:20%; padding-top: 4%; font-family: status-bar;">Please enter a valid ntp server address</div>', 'NTP Alert ');
		return false;
	}
}

function close_div()
{
	document.getElementById('response').style.display = 'none';
}

function do_login()
{
	var username = document.signin.username.value;
	var password = document.signin.password.value;
	/*if (username == '')
	{
		alert('Username is required');
		return false;
		document.username.focus();
	}*/


	if (password == '')
	{
		alert('Password can\'t be empty');
		return false;
		document.signin.password.focus();
	}
	/*if (username && password == '' )
	{
		alert('Please Enter the Username and Password');
		return false;
		document.username.focus();
	}*/	

	document.getElementById('wait').style.display = 'block';
	document.signin.submit();

	$.ajax(
	{
		type: 'POST',
		url: 'signin.py',
		data: 'username='+document.signin.username.value+'&password='+document.signin.password.value,

		success: function(html)
		{
			$('#response').html(html);
		}
	});
}

function set_focus()
{
	window.document.signin.password.focus();
}

function get_key()
{
	return ev.keyCode;
}

function generate_user_list(id_available, id_autosuggest, users_groups_string, user_group, form)
{
	var assigned_users  = '';
	var assigned_groups = '';

	if (form == 'share_edit')
	{
		assigned_users  = document.share_edit.hid_ads_assigned_users.value;
		assigned_groups = document.share_edit.hid_ads_assigned_groups.value;
	}

	else if (form == 'set_ftp_params')
	{
		assigned_users  = document.set_ftp_params.hid_ftp_assigned_users.value;
		assigned_groups = document.set_ftp_params.hid_ftp_assigned_groups.value;
	}

	if (form == 'user_auota')
	{
		assigned_users  = document.user_quota.hid_ads_users_only.value;
		assigned_groups = document.user_quota.hid_ads_groups_only.value;
	}

	var assigned_users_array  = assigned_users.split(':');
	var assigned_groups_array = assigned_groups.split(':');

	if (user_group == 'users')
	{
		var user_arr2str  = assigned_users_array.toString();
	}

	else if (user_group == 'groups')
	{
		var user_arr2str  = assigned_groups_array.toString();
	}

	id_available.setAttribute("autocomplete","off");
	id_autosuggest.style.display = 'none';

	if (id_available.value != '')
	{
		suggestions_array = new Array();
		suggestions_string = '';

		if (user_group == 'users')
		{
			users_groups_array = users_groups_string.split(':');
		}

		else if (user_group == 'groups')
		{
			users_groups_array = users_groups_string.split(':');
		}

		for (i = 0;  i < users_groups_array.length;  i++)
		{
			if (users_groups_array[i].indexOf(id_available.value) == '0')
			{
				if (user_arr2str.search(users_groups_array[i]) < 0)
				{
					suggestions_array.push(users_groups_array[i]);
				}
			}
		}
		
		suggestions_array.sort();

		for (i = 0;  i < suggestions_array.length;  i++)
		{
			suggestions_string += "<option value = '"+suggestions_array[i]+"'>"+suggestions_array[i]+"</option>";
		}

		id_autosuggest.innerHTML = suggestions_string;
		id_autosuggest.style.display = 'block';
		id_available.focus();
	}

	else
	{
		id_autosuggest.style.display = 'none';
	}
}

function um_generate_user_list(id_available, id_autosuggest, users_groups_string, user_group, form)
{	
	var assigned_users  = '';
	var assigned_groups = '';
	var suggestions_string = '';

	assigned_users  = document.show_users.hid_local_assigned_users.value;
	
	id_available.setAttribute("autocomplete","off");

	if (id_available.value != '')
	{
		suggestions_array = new Array();

		if (user_group == 'users')
		{
			users_groups_array = users_groups_string.split(':');
		}

		else if (user_group == 'groups')
		{
			users_groups_array = users_groups_string.split(':');
		}

		for (i = 0;  i < users_groups_array.length;  i++)
		{
			if (users_groups_array[i].indexOf(id_available.value) == '0')
			{
				if (users_groups_array[i] != 'USER')
				{
					suggestions_array.push(users_groups_array[i]);
				}
			}
		}

		if (id_available.value == ' ')
		{
			for (i = 0;  i < users_groups_array.length;  i++)
			{
				if (users_groups_array[i] != 'USER')
				{
					suggestions_array.push(users_groups_array[i]);
				}
			}
		}

		suggestions_array.sort();

		for (i = 0;  i < suggestions_array.length;  i++)
		{
			suggestions_string += "<option value = '"+suggestions_array[i]+"'>"+suggestions_array[i]+"</option>";
		}

		if (suggestions_string != '')
		{
			id_autosuggest.style.display = 'block';
			id_autosuggest.innerHTML = suggestions_string;
		}
	
		else
		{
			alert('No records found starting with \''+id_available.value+'\'');

			if (form == 'manage_users')
			{
				document.manage_users.users.value = '';
				document.manage_users.users.focus();
			}

			if (form == 'manage_groups')
			{
				document.manage_groups.groups.value = '';
				document.manage_groups.groups.focus();
			}

			if (form == 'del_user')
			{
				document.del_user.delete_users.value = '';
				document.delete_users.delete_users.focus();
			}

			if (form == 'del_group')
			{
				document.del_group.delete_groups.value = '';
				document.del_group.delete_groups.focus();
			}

			if (form == 'show_users')
			{
				document.show_users.local_user_text.value = '';
				document.show_users.local_user_text.focus();
			}
		}
	}

	else
	{
		id_autosuggest.style.display = 'none';
	}
}

function set_user(id_available, id_autosuggest, value)
{
	id_available.value = value;
	//id_autosuggest.style.display = 'none';
}

function submit_smb_form()
{
	var u_string      = '';
	var g_string      = '';
	//var smbclicked    = document.share_edit.use_smb.checked;
	var options_count = document.getElementById('id_assign_options').options.length;

	var audit_options_string = '';
        var recycle      = '';

	if (document.getElementById("id_select_adv").checked == true)
	{
		if (document.getElementById('id_auditing').checked == false && document.getElementById('id_enable_recycle').checked == false)
		{
			alert('You need to choose an option for Auditing/Recycle option!');
			return false;
		}
	}

	if (document.getElementById('id_auditing').checked == true)
	{
		if (options_count == 0)
		{
			alert('Choose an option for audit!');
			return false;
		}
	
		for (i = 0;  i < options_count;  i++)
		{
			audit_options_string += document.getElementById('id_assign_options').options[i].value + 'xxx';
		}

		audit_options_string = audit_options_string.substr(0, audit_options_string.lastIndexOf('xxx'));
	}

	if (document.getElementById('id_enable_recycle').checked == true)
	{
		recycle = document.share_edit.recycle_path.value;
	}

	var options_array = document.getElementsByName('priv');

	for (i = 0;  i < options_array.length;  i++)
	{
		if (options_array[i].checked)
		{
			if (options_array[i].value == 'valid_user')
			{
				user_priv = 'valid_user';

				var users_array  = document.share_edit.elements["grant_users[]"];
				var groups_array = document.share_edit.elements["grant_groups[]"];

				if (smbclicked == true)
				{
					if (users_array.length == 0 && groups_array.length == 0)
					{
						alert('Please choose a user/group!');
						return false;
					}
				}
			}

			else if (options_array[i].value == 'guest')
			{
				user_priv = 'guest';
			}

			else if (options_array[i].value == 'public')
			{
				user_priv = 'public';
			}
		}
	}
	
	var id_users  = document.getElementById('granted');
	var id_groups = document.getElementById('granted_groups');

	for (i = 0;  i < id_users.options.length; i++)
	{
		u_string += '$$' + id_users.options[i].value;
	}

	for (i = 0;  i < id_groups.options.length; i++)
	{
		g_string += '$$' + id_groups.options[i].value;
	}

	var i = u_string.indexOf('+');
	var j = g_string.indexOf('+');

	if (i > 0)
	{
		u_string = u_string.replace(/\+/g, '<PLUS>');
	}

	if (j > 0)
	{
		g_string = g_string.replace(/\+/g, '<PLUS>');
	}

	document.getElementById('wait').style.display = 'block';

	/*$.ajax(
	{
		type: 'POST',
		url: 'edit_shares.py',
		data: 'hidpage_from=checked&u_string='+u_string+'&g_string='+g_string+'&use_smb='+document.share_edit.use_smb.checked+'&hid_ads='+document.share_edit.hid_ads.value+'&hid_nis='+document.share_edit.hid_nis.value+'&share_name='+document.share_edit.hid_share.value+'&hid_comm='+document.share_edit.hid_comm.value+'&hid_path='+document.share_edit.hid_path.value+'&read_only='+document.share_edit.read_only.checked+'&visible='+document.share_edit.visible.checked+'&priv='+user_priv+'&aud_rec='+document.getElementById('id_select_adv').checked+'&audit_string='+audit_options_string+'&recycle='+recycle+'&recycle_opt='+document.getElementById("id_enable_recycle").checked+'&audit_option='+document.getElementById("id_auditing").checked,

		success: function(html)
		{
			$('#response').html(html);
		}
	});*/

	document.share_edit.submit();
	disable_all_other_forms('share_edit');
}

function remove_share_form()
{
	document.getElementById('wait').style.display = 'block';

	$.ajax(
	{
		type: 'POST',
		url: 'delete_share.php',
		data: 'hidpage_from=checked&hid_share='+document.delete_share.hid_share.value+'&hid_path='+document.delete_share.hid_path.value,

		success: function(html)
		{
			$('#response').html(html);
		}
	});

	document.delete_share.action_but.disabled = true;
	disable_all_other_forms('delete_share');
}

function permission_form()
{
	document.getElementById('wait').style.display = 'block';

	uread  = 0;
	uwrite = 0;
	uexec  = 0;

	gread  = 0;
	gwrite = 0;
	gexec  = 0;

	oread  = 0;
	owrite = 0;
	oexec  = 0;

	if (document.share_permissions.o_read_perm.checked == true)
	{
		uread = document.share_permissions.o_read_perm.value;
	}

	if (document.share_permissions.o_write_perm.checked == true)
	{
		uwrite = document.share_permissions.o_write_perm.value;
	}

	if (document.share_permissions.o_exec_perm.checked == true)
	{
		uexec = document.share_permissions.o_exec_perm.value;
	}

	if (document.share_permissions.g_read_perm.checked == true)
	{
		gread = document.share_permissions.g_read_perm.value;
	}

	if (document.share_permissions.g_write_perm.checked == true)
	{
		gwrite = document.share_permissions.g_write_perm.value;
	}

	if (document.share_permissions.g_exec_perm.checked == true)
	{
		gexec = document.share_permissions.g_exec_perm.value;
	}

	if (document.share_permissions.oth_read_perm.checked == true)
	{
		oread = document.share_permissions.oth_read_perm.value;
	}

	if (document.share_permissions.oth_write_perm.checked == true)
	{
		owrite = document.share_permissions.oth_write_perm.value;
	}

	if (document.share_permissions.oth_exec_perm.checked == true)
	{
		oexec = document.share_permissions.oth_exec_perm.value;
	}

	var purpose = document.share_permissions.perm_type.value;

	$.ajax(
	{
		type: 'POST',
		url: 'share_permissions.py',
		data: 'hidpage_from=checked&o_read_perm='+uread+'&o_write_perm='+uwrite+'&o_exec_perm='+uexec+'&g_read_perm='+gread+'&g_write_perm='+gwrite+'&g_exec_perm='+gexec+'&oth_read_perm='+oread+'&oth_write_perm='+owrite+'&oth_exec_perm='+oexec+'&hid_path='+document.share_permissions.hid_path.value+'&hid_share='+document.share_permissions.hid_share.value+'&restrict='+document.share_permissions.restrict.checked+'&inherit='+document.share_permissions.inherit.checked+'&purpose='+purpose,

		success: function(html)
		{
			$('#response').html(html);
		}
	});

	document.share_permissions.assign_perms.disabled = true;
	//document.share_permissions.submit();
	//disable_all_other_forms('share_permissions');
}

function submit_edit_share_form()
{
	document.getElementById('wait').style.display = 'block';

	alert(document.edit_this_share.comment.value);

	$.ajax(
	{
		type: 'POST',
		url: 'edit_this_share_action.py',
		data: 'share_name='+document.edit_this_share.share.value+'&comment='+document.edit_this_share.comment.value+'&share_path='+document.edit_this_share.share_path.value,

		success: function(html)
		{
			$('#response').html(html);
		}
	});

	document.edit_this_share.action_but.disabled = true;
	disable_all_other_forms('edit_this_share');
}

function validate_ownership(process)
{
	var user_val  = document.change_owner.users.value;
	var group_val = document.change_owner.groups.value;

	user_val = user_val.replace('+', '<PLUS>');
	group_val = group_val.replace('+', '<PLUS>');

	var reassign = '';
	var reset    = '';

	if (process == 'reassign')
	{
		reassign = 'ReAssign';
	}

	if (process == 'reset')
	{
		reassign = 'Reset Ownership';
	}

	if (user_val == '' && group_val == '')
	{
		//alert ('Please choose a user or a group to assign');
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 19%; padding-top: 4%; font-family: status-bar;">Please choose a user or a group to assign.</div>', 'Owner Alert');
		return false;
	}

	document.getElementById('share_own_wait').style.display = 'block';

	$.ajax(
	{
		type: 'POST',
		url: 'change_ownership.py',
		data: 'users='+user_val+'&groups='+group_val+'&inherit='+document.change_owner.inherit.checked+'&hid_share='+document.change_owner.hid_share.value+'&hid_path='+document.change_owner.hid_path.value+'&reassign='+reassign,
		
		success: function(html)
		{
			$('#id_share_own_wait').html(html);
		}
	});

	disable_all_other_forms('change_owner');
}

function show_frame()
{
	var val = document.nfs_setup.use_nfs.checked;
	var val1 = document.getElementById('nfs_param');
	
	if (val == true)
	{
		document.nfs_setup.no_root.checked = true;
		val1.style.display = 'block';
		document.nfs_setup.hid_nfs.value = val;
		document.nfs_setup.action_but1.style.visibility = 'hidden';
	}

	else
	{
		val1.style.display = 'none';
		document.nfs_setup.action_but1.style.visibility = 'visible';
	}
}

function move_users(fbox, tbox, val)
{
	if (val == '1000')
	{
		for (i = 0;  i < fbox.options.length;  i++)
		{
			if (fbox.options[i].selected == true)
			{
				fbox.options[i] = null;
			}

			if (fbox.options[i].value != '')
			{
				fbox.options[i].selected = true;
			}
		}
	}

	var arrFbox = new Array();
	var arrTbox = new Array();
	var arrLookup = new Array();
	var i;

	for (i = 0; i < tbox.options.length; i++)
	{
		arrLookup[tbox.options[i].text] = tbox.options[i].value;
		arrTbox[i] = tbox.options[i].text;
	}
	
	var fLength = 0;
	var tLength = arrTbox.length;

	for(i = 0; i < fbox.options.length; i++)
	{
		arrLookup[fbox.options[i].text] = fbox.options[i].value;

		if (fbox.options[i].selected && fbox.options[i].value != "")
		{
			arrTbox[tLength] = fbox.options[i].text;
			tLength++;
		}
			
		else
		{
			arrFbox[fLength] = fbox.options[i].text;
			fLength++;
		}
	}
	
	fbox.length = 0;
	tbox.length = 0;
	var c;
	
	for(c = 0; c < arrFbox.length; c++)
	{
		var no = new Option();
		
		no.value = arrLookup[arrFbox[c]];
		no.text = arrFbox[c];
		fbox[c] = no;
		
		if (val == '2')
		{
			fbox[c].selected = true;
		}
	}
	
	for(c = 0; c < arrTbox.length; c++)
	{
		var no = new Option();
		
		no.value = arrLookup[arrTbox[c]];
		no.text = arrTbox[c];
		tbox[c] = no;
		
		if (val == '1')
		{
			tbox[c].selected = true;
		}
	}
}

function move_groups(fbox, tbox, val)
{
	if (val == '1000')
	{
		for (i = 0;  i < fbox.options.length;  i++)
		{
			if (fbox.options[i].selected == true)
			{
				fbox.options[i] = null;
			}

			if (fbox.options[i].value != '')
			{
				fbox.options[i].selected = true;
			}
		}
	}

	var arrFbox = new Array();
	var arrTbox = new Array();
	var arrLookup = new Array();
	var i;

	for (i = 0; i < tbox.options.length; i++)
	{
		arrLookup[tbox.options[i].text] = tbox.options[i].value;
		arrTbox[i] = tbox.options[i].text;
	}
	
	var fLength = 0;
	var tLength = arrTbox.length;

	for(i = 0; i < fbox.options.length; i++)
	{
		arrLookup[fbox.options[i].text] = fbox.options[i].value;

		if (fbox.options[i].selected && fbox.options[i].value != "")
		{
			arrTbox[tLength] = fbox.options[i].text;
			tLength++;
		}
			
		else
		{
			arrFbox[fLength] = fbox.options[i].text;
			fLength++;
		}
	}
	
	fbox.length = 0;
	tbox.length = 0;
	var c;
	
	for(c = 0; c < arrFbox.length; c++)
	{
		var no = new Option();
		
		no.value = arrLookup[arrFbox[c]];
		no.text = arrFbox[c];
		fbox[c] = no;
		
		if (val == '2')
		{
			fbox[c].selected = true;
		}
	}
	
	for(c = 0; c < arrTbox.length; c++)
	{
		var no = new Option();
		
		no.value = arrLookup[arrTbox[c]];
		no.text = arrTbox[c];
		tbox[c] = no;
		
		if (val == '1')
		{
			tbox[c].selected = true;
		}
	}
}

function move_text_to_dropdown(txtbox, drpdwn, val)
{
	//var hid_ads_domain   = document.share_edit.hid_ads_domain.value;
	//var hidadsusers      = document.share_edit.hidadsusers.value;
	//var ads_users_string = document.share_edit.hid_ads_users.value;
	var to_id            = document.getElementById('granted');

	//checkusersstring = ':' + ads_users_string + ':';

	//if (txtbox.value)
	//{
		for (i = drpdwn.options.length;  i <= to_id.options.length;  i++)
		{
			//if (hidadsusers.indexOf('\\') > 0)
			//{
				//var users_ads = hid_ads_domain + '\\' + txtbox.value;
				var users_ads = txtbox.value;
			//}

			//else
			//{
				//var users_ads = hid_ads_domain + '+' + txtbox.value;
				//var users_ads = txtbox.value;
			//}

			//checkval = ':' + txtbox.value + ':';

			//if (checkusersstring.indexOf(checkval) >= 0)
			//{
				document.getElementById("granted").options[i] = new Option(txtbox.value, users_ads);
				document.getElementById("granted").options[i].selected = true;
			//}

			txtbox.value = '';

			AutoSuggest('', '', document.getElementById("granted").options[i].text);
			break;
		}
	//}
}

function move_group_to_dropdown(txtbox, drpdwn, val)
{
	var hid_ads_domain   = document.share_edit.hid_ads_domain.value;
	var hidadsgroups     = document.share_edit.hidadsgroups.value;
	var ads_groups_string = parent.document.share_edit.hid_ads_groups.value;
	var to_id            = document.getElementById('granted_groups');

	checkgroupsstring = ':' + ads_groups_string + ':';

	if (txtbox.value)
	{
		for (i = drpdwn.options.length;  i <= to_id.options.length;  i++)
		{
			if (hidadsgroups.indexOf('\\') > 0)
			{
				var users_ads = '@' + hid_ads_domain + '\\' + txtbox.value;
			}

			else
			{
				var users_ads = '@' + hid_ads_domain + '+' + txtbox.value;
			}

			checkval = ':' + txtbox.value + ':';

			if (checkgroupsstring.indexOf(checkval) >= 0)
			{
				document.getElementById("granted_groups").options[i] = new Option(txtbox.value, users_ads);
				document.getElementById("granted_groups").options[i].selected = true;
			}

			txtbox.value = '';

			AutoSuggest('', '', document.getElementById("granted_groups").options[i].text);
			break;
		}
	}
}

function move_quota_text_to_dropdown(txtbox, drpdwn, val)
{
	var hid_ads_domain   = document.user_quota.adsdomain.value;
	var hidadsusers      = document.user_quota.ads_users_string.value;
	var ads_users_string = document.user_quota.hid_ads_users_only.value;
	var to_id            = document.getElementById('id_user_list');

	checkusersstring = ':' + ads_users_string + ':';

	if (txtbox.value)
	{
		for (i = drpdwn.options.length;  i <= to_id.options.length;  i++)
		{
			if (hidadsusers.indexOf('\\') > 0)
			{
				var users_ads = hid_ads_domain + '\\' + txtbox.value;
			}

			else
			{
				var users_ads = hid_ads_domain + '+' + txtbox.value;
			}

			checkval = ':' + txtbox.value + ':';

			if (checkusersstring.indexOf(checkval) >= 0)
			{
				document.getElementById("id_user_list").options[i] = new Option(txtbox.value, users_ads);
				document.getElementById("id_user_list").options[i].selected = true;
			}

			txtbox.value = '';

			AutoSuggest('', '', document.getElementById("id_user_list").options[i].text);
			break;
		}
	}
}

function move_quota_group_to_dropdown(txtbox, drpdwn, val)
{
	var hid_ads_domain   = document.user_quota.adsdomain.value;
	var hidadsusers      = document.user_quota.ads_groups_string.value;
	var ads_users_string = document.user_quota.hid_ads_groups_only.value;
	var to_id            = document.getElementById('id_group_list');

	checkusersstring = ':' + ads_users_string + ':';

	if (txtbox.value)
	{
		for (i = drpdwn.options.length;  i <= to_id.options.length;  i++)
		{
			if (hidadsusers.indexOf('\\') > 0)
			{
				var users_ads = hid_ads_domain + '\\' + txtbox.value;
			}

			else
			{
				var users_ads = hid_ads_domain + '+' + txtbox.value;
			}

			checkval = ':' + txtbox.value + ':';

			if (checkusersstring.indexOf(checkval) >= 0)
			{
				document.getElementById("id_group_list").options[i] = new Option(txtbox.value, users_ads);
				document.getElementById("id_group_list").options[i].selected = true;
			}

			txtbox.value = '';

			AutoSuggest('', '', document.getElementById("id_group_list").options[i].text);
			break;
		}
	}
}


function ftp_move_text_to_dropdown(txtbox, drpdwn, val)
{
	var hid_ads_domain = document.set_ftp_params.hid_ftp_domain.value;
	var ads_users_string = parent.document.set_ftp_params.hid_ads_users.value;
	var fullusersstring = document.set_ftp_params.hidadsusers.value;

	checkusersstring = ':' + ads_users_string + ':';

	var to_id = document.getElementById('ftp_granted');

	if (txtbox.value)
	{
		for (i = drpdwn.options.length;  i <= to_id.options.length;  i++)
		{
			if (fullusersstring.indexOf('+') > 0)
			{
				var users_ads = hid_ads_domain + '+' + txtbox.value;
			}

			else if (fullusersstring.indexOf('\\') > 0)
			{
				var users_ads = hid_ads_domain + '\\' + txtbox.value;
			}

			checkval = ':' + txtbox.value + ':';

			if (checkusersstring.indexOf(checkval) >= 0)
			{
				document.getElementById("ftp_granted").options[i] = new Option(txtbox.value, users_ads);
				document.getElementById("ftp_granted").options[i].selected = true;
			}

			txtbox.value = '';
			
			AutoSuggest('', '', document.getElementById("ftp_granted").options[i].text);
			break;
		}
	}
}

function ftp_move_group_to_dropdown(txtbox, drpdwn, val)
{
	var hid_ads_domain    = document.set_ftp_params.hid_ftp_domain.value;
	var fullusersstring   = document.set_ftp_params.hidadsusers.value;
	var ads_groups_string = document.set_ftp_params.hid_ads_groups.value;
	var to_id             = document.getElementById('ftp_granted_groups');

	checkgroupsstring = ':' + ads_groups_string + ':';

	if (txtbox.value)
	{
		for (i = drpdwn.options.length;  i <= to_id.options.length;  i++)
		{
			if (fullusersstring.indexOf('+') > 0)
			{
				var users_ads = '@'+hid_ads_domain+'+'+txtbox.value;
			}

			else if (fullusersstring.indexOf('\\') > 0)
			{
				var users_ads = '@' + hid_ads_domain + '\\' + txtbox.value;
			}

			checkval = ':' + txtbox.value + ':';

			if (checkgroupsstring.indexOf(checkval) >= 0)
			{
				document.getElementById("ftp_granted_groups").options[i] = new Option(txtbox.value, users_ads);
				document.getElementById("ftp_granted_groups").options[i].selected = true;
			}

			txtbox.value = '';
			
			AutoSuggest('', '', document.getElementById("ftp_granted_groups").options[i].text);
			break;
		}
	}
}

function afp_move_users(fbox, tbox, val)
{
	var arrFbox = new Array();
	var arrTbox = new Array();
	var arrLookup = new Array();
	var i;

	for (i = 0; i < tbox.options.length; i++)
	{
		arrLookup[tbox.options[i].text] = tbox.options[i].value;
		arrTbox[i] = tbox.options[i].text;
	}
	
	var fLength = 0;
	var tLength = arrTbox.length;

	for(i = 0; i < fbox.options.length; i++)
	{
		arrLookup[fbox.options[i].text] = fbox.options[i].value;

		if (fbox.options[i].selected && fbox.options[i].value != "")
		{
			arrTbox[tLength] = fbox.options[i].text;
			tLength++;
		}
			
		else
		{
			arrFbox[fLength] = fbox.options[i].text;
			fLength++;
		}
	}
	
	fbox.length = 0;
	tbox.length = 0;
	var c;
	
	for(c = 0; c < arrFbox.length; c++)
	{
		var no = new Option();
		
		no.value = arrLookup[arrFbox[c]];
		no.text = arrFbox[c];
		fbox[c] = no;
		
		if (val == '2')
		{
			fbox[c].selected = true;
		}
	}
	
	for(c = 0; c < arrTbox.length; c++)
	{
		var no = new Option();
		
		no.value = arrLookup[arrTbox[c]];
		no.text = arrTbox[c];
		tbox[c] = no;
		
		if (val == '1')
		{
			tbox[c].selected = true;
		}
	}
}

function afp_move_groups(fbox, tbox, val)
{
	var arrFbox = new Array();
	var arrTbox = new Array();
	var arrLookup = new Array();
	var i;

	for (i = 0; i < tbox.options.length; i++)
	{
		arrLookup[tbox.options[i].text] = tbox.options[i].value;
		arrTbox[i] = tbox.options[i].text;
	}
	
	var fLength = 0;
	var tLength = arrTbox.length;

	for(i = 0; i < fbox.options.length; i++)
	{
		arrLookup[fbox.options[i].text] = fbox.options[i].value;

		if (fbox.options[i].selected && fbox.options[i].value != "")
		{
			arrTbox[tLength] = fbox.options[i].text;
			tLength++;
		}
			
		else
		{
			arrFbox[fLength] = fbox.options[i].text;
			fLength++;
		}
	}
	
	fbox.length = 0;
	tbox.length = 0;
	var c;
	
	for(c = 0; c < arrFbox.length; c++)
	{
		var no = new Option();
		
		no.value = arrLookup[arrFbox[c]];
		no.text = arrFbox[c];
		fbox[c] = no;
		
		if (val == '2')
		{
			fbox[c].selected = true;
		}
	}
	
	for(c = 0; c < arrTbox.length; c++)
	{
		var no = new Option();
		
		no.value = arrLookup[arrTbox[c]];
		no.text = arrTbox[c];
		tbox[c] = no;
		
		if (val == '1')
		{
			tbox[c].selected = true;
		}
	}
}

function ftp_move_users(fbox, tbox, val)
{
	if (val == '1000')
	{
		for (i = 0;  i < fbox.options.length;  i++)
		{
			if (fbox.options[i].selected == true)
			{
				fbox.options[i] = null;
			}

			if (fbox.options[i].value != '')
			{
				fbox.options[i].selected = true;
			}
		}
	}

	var arrFbox = new Array();
	var arrTbox = new Array();
	var arrLookup = new Array();
	var i;

	for (i = 0; i < tbox.options.length; i++)
	{
		arrLookup[tbox.options[i].text] = tbox.options[i].value;
		arrTbox[i] = tbox.options[i].text;
	}
	
	var fLength = 0;
	var tLength = arrTbox.length;

	for(i = 0; i < fbox.options.length; i++)
	{
		arrLookup[fbox.options[i].text] = fbox.options[i].value;

		if (fbox.options[i].selected && fbox.options[i].value != "")
		{
			arrTbox[tLength] = fbox.options[i].text;
			tLength++;
		}
			
		else
		{
			arrFbox[fLength] = fbox.options[i].text;
			fLength++;
		}
	}
	
	fbox.length = 0;
	tbox.length = 0;
	var c;
	
	for(c = 0; c < arrFbox.length; c++)
	{
		var no = new Option();
		
		no.value = arrLookup[arrFbox[c]];
		no.text = arrFbox[c];
		fbox[c] = no;
		
		if (val == '2')
		{
			fbox[c].selected = true;
		}
	}
	
	for(c = 0; c < arrTbox.length; c++)
	{
		var no = new Option();
		
		no.value = arrLookup[arrTbox[c]];
		no.text = arrTbox[c];
		tbox[c] = no;
		
		if (val == '1')
		{
			tbox[c].selected = true;
		}
	}
}

function ftp_move_groups(fbox, tbox, val)
{
	if (val == '1000')
	{
		for (i = 0;  i < fbox.options.length;  i++)
		{
			if (fbox.options[i].selected == true)
			{
				fbox.options[i] = null;
			}

			if (fbox.options[i].value != '')
			{
				fbox.options[i].selected = true;
			}
		}
	}

	var arrFbox = new Array();
	var arrTbox = new Array();
	var arrLookup = new Array();
	var i;

	for (i = 0; i < tbox.options.length; i++)
	{
		arrLookup[tbox.options[i].text] = tbox.options[i].value;
		arrTbox[i] = tbox.options[i].text;
	}
	
	var fLength = 0;
	var tLength = arrTbox.length;

	for(i = 0; i < fbox.options.length; i++)
	{
		arrLookup[fbox.options[i].text] = fbox.options[i].value;

		if (fbox.options[i].selected && fbox.options[i].value != "")
		{
			arrTbox[tLength] = fbox.options[i].text;
			tLength++;
		}
			
		else
		{
			arrFbox[fLength] = fbox.options[i].text;
			fLength++;
		}
	}
	
	fbox.length = 0;
	tbox.length = 0;
	var c;
	
	for(c = 0; c < arrFbox.length; c++)
	{
		var no = new Option();
		
		no.value = arrLookup[arrFbox[c]];
		no.text = arrFbox[c];
		fbox[c] = no;
		
		if (val == '2')
		{
			fbox[c].selected = true;
		}
	}
	
	for(c = 0; c < arrTbox.length; c++)
	{
		var no = new Option();
		
		no.value = arrLookup[arrTbox[c]];
		no.text = arrTbox[c];
		tbox[c] = no;
		
		if (val == '1')
		{
			tbox[c].selected = true;
		}
	}
}

function show_smb_params()
{
	var valclicked = document.share_edit.use_smb.checked;
	table_id       = document.getElementById('smb_params');

	if (valclicked == true)
	{
		table_id.style.display = 'block';
	}
	
	else
	{
		table_id.style.display = 'none';
	}
}

function show_afp_params()
{
	var afp_clicked    = document.afp_form.use_afp.checked;
	afp_table_id       = document.getElementById('afp_params');

	if (afp_clicked == true)
	{
		afp_table_id.style.display = 'block';
	}
	
	else
	{
		afp_table_id.style.display = 'none';
	}
}

function show_smb_users_groups()
{
	var radio_array = document.getElementsByName('priv'); 
	var users_list  = document.getElementById('users_list');
	var groupslist1  = document.getElementById('groups_list1');
	//var groups_list = document.getElementById('groups_list');

	for (var i = 0;  i < radio_array.length;  i++)
	{
		if (radio_array[i].checked)
		{
			if (radio_array[i].value == 'valid_user')
			{
				user_priv = 'valid_user';

				users_list.style.display  = 'block';
				groupslist1.style.display = 'block';
				//groups_list.style.display = 'block';
			}

			else if (radio_array[i].value == 'guest')
			{
				user_priv = 'guest';

				users_list.style.display  = 'none';
				groupslist1.style.display = 'none';
				//groups_list.style.display = 'none';
			}

			else if (radio_array[i].value == 'public')
			{
				user_priv = 'public';

				users_list.style.display = 'none';
				groupslist1.style.display = 'none';
				//groups_list.style.display = 'none';
			}
		}
	}
}

function show_afp_users_groups()
{
	var radio_array = document.getElementsByName('afp_priv'); 
	var users_list  = document.getElementById('afp_users_list');
	var groups_list = document.getElementById('afp_groups_list');

	for (var i = 0;  i < radio_array.length;  i++)
	{
		if (radio_array[i].checked)
		{
			if (radio_array[i].value == 'valid_user')
			{
				users_list.style.display  = 'block';
				groups_list.style.display = 'block';
			}

			else if (radio_array[i].value == 'guest')
			{
				users_list.style.display  = 'none';
				groups_list.style.display = 'none';
			}

			else if (radio_array[i].value == 'advanced_per')
                        {
                                users_list.style.display  = 'none';
                                groups_list.style.display = 'none';
                        }
		}
	}
}


function show_advance_per(blnchecked) {
if(blnchecked)
{	
	document.getElementById("afp_advanced_list").style.display = "block";
}
else
{
	document.getElementById("afp_advanced_list").style.display = "none";
}

}

function validate_access_ip(access_ip_val)
{
	error = '';
	access_ip_val = access_ip_val.replace(/,\ /g, ',');
	
	access_ip_array = access_ip_val.split(',');
	
	for (i = 0;  i < access_ip_array.length;  i++)
	{
		var ipPattern = /^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$|^\*$|^$/;
		var accessip_array = access_ip_array[i].match(ipPattern);

		if (access_ip_array[i] == '0.0.0.0' || access_ip_array[i] == '255.255.255.255')
		{
			error = access_ip_array[i]+' is not a valid IP! Make sure you don\'t give any spaces.';
		}
		
		if (accessip_array == null)
		{
			error = access_ip_array[i]+' is not a valid IP! Make sure you don\'t give any spaces.';
		}
		
		else
		{
			for (j = 1;  j < accessip_array.length;  j++)
			{	
				if (accessip_array[j] > 255)
				{
					error = access_ip_array[i]+' is not a valid IP! Make sure you don\'t give any spaces.';
				}
			}
		}
	}

	return error;
}

function validate_ftp_access_ip(ftp_access_ip_val)
{
	var read_only_option = document.set_ftp_params.ftp_read_only.checked;
	ftp_access_ip_val = ftp_access_ip_val.replace(/;\ /g, ';');

	error = '';

	if (read_only_option == true)
	{
		var ipPattern = /^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$|^\*$|^$/;
	}

	else
	{
		var ipPattern = /^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$|^\*$|^$/;
	}

	ftp_access_ip_array = ftp_access_ip_val.split(';');
	
	for (i = 0;  i < ftp_access_ip_array.length;  i++)
	{
		var ftp_accessip_array = ftp_access_ip_array[i].match(ipPattern);

		if (ftp_access_ip_array[i] == '0.0.0.0' || ftp_access_ip_array[i] == '255.255.255.255')
		{
			error = ftp_access_ip_array[i]+' is not a valid IP!';
		}
		
		if (ftp_accessip_array == null)
		{
			error = 'Please enter a valid IP!';

		}
		
		else
		{
			for (j = 1;  j < ftp_accessip_array.length;  j++)
			{	
				if (ftp_accessip_array[j] > 255)
				{
					error = ftp_access_ip_array[i]+' is not a valid IP!';
				}
			}
		}
	}
}

function enable_button()
{
	document.nfs_setup.action_but.disabled = false;
}

function validate_nfs_form()
{
	var use_nfs   = document.nfs_setup.conf.value;
	var access_ip = document.nfs_setup.access_ip.value;
	var write_ip  = document.nfs_setup.write_ip.value;
	/*var optional  = document.nfs_setup.optional.value;

	var spchars   = "~`!@#$%^&*()+-[]\\\';/{}|\"<>?";

	if (optional.indexOf(' ') >= 0)
	{
		alert('Spaces are not allowed !');
		return false;
	}

	for (i = 0;  i < optional.length;  i++)
	{
		if (spchars.indexOf(optional.charAt(i)) != -1)
		{
			alert('Special characters other than comma(,) are not allowed !');
			return false;
		}
	}*/

	access_ip = access_ip.replace(/,\ /g, ',');
	write_ip  = write_ip.replace(/,\ /g, ',');

	if (access_ip.indexOf('*') >= 0)
	{
		document.nfs_setup.access_ip.value = '*';
	}

	if (write_ip.indexOf('*') >= 0)
	{
		document.nfs_setup.write_ip.value = '*';
	}

	if (use_nfs == 'configure' || use_nfs == 'reconf')
	{
		use_nfs_option = 'on';

		if (access_ip == ',')
		{
			alert('Enter a valid access IP!');
			return false;
		}

		if (write_ip == ',')
		{
			alert('Enter a valid write IP!');
			return false;
		}

		if (access_ip == '' && write_ip == '')
		{
			alert('Both access ip and write ip can not be blank!');
			return false;
		}

		else
		{
			error = validate_access_ip(access_ip);
			
			if (error != '')
			{
				alert(error);
				return false;
			}

			error = validate_access_ip(write_ip);

			if (error != '')
			{
				alert(error);
				return false;
			}
		}
	
		var options_array = new Array();

		options_array = document.getElementsByName('no_root');
	
		for (i = 0;  i < options_array.length;  i++)
		{
			if (options_array[i].checked)
			{
				if (options_array[i].value == 'no_root')
				{
					no_root = 'no_root';
				}

				else if (options_array[i].value == 'all_squash')
				{
					no_root = 'all_squash';
				}
			}
		}

		document.getElementById('wait').style.display = 'block';

		access_ip = access_ip.replace(/\ /g, '');
		write_ip  = write_ip.replace(/\ /g, '');

		//document.nfs_setup.submit();

		insecure    = document.nfs_setup.insecure.checked ? "on" : "off";
		synchronous = document.nfs_setup.synchronous.checked ? "on" : "off";
		ins_locks   = document.nfs_setup.ins_locks.checked ? "on" : "off";

		$.ajax(
		{
			type: 'POST',
			url: 'nfs_settings.py',
			data: 'hidpage_from=checked&insecure='+insecure+'&synchronous='+synchronous+'&ins_locks='+ins_locks+'&no_root='+no_root+'&access_ip='+access_ip+'&write_ip='+write_ip+'&use_nfs='+use_nfs_option+'&hid_path='+document.nfs_setup.hid_path.value+'&hid_share='+document.nfs_setup.hid_share.value+'&hid_comment='+document.nfs_setup.hid_comment.value,

			success: function(html)
			{
				$('#response').html(html);
			}
		});
	}

	else
	{
		use_nfs_option = '';

		document.getElementById('wait').style.display = 'block';
		//document.nfs_setup.submit();

		$.ajax(
		{
			type: 'POST',
			url: 'nfs_settings.py',
			data: 'hidpage_from=checked&use_nfs=off&hid_path='+document.nfs_setup.hid_path.value+'&hid_share='+document.nfs_setup.hid_share.value+'&hid_comment='+document.nfs_setup.hid_comment.value,

			success: function(html)
			{
				$('#response').html(html);
			}
		});
	}
	
	document.nfs_setup.action_but.disabled = true;
	disable_all_other_forms('nfs_setup');
}

function set_ftp_parameters()
{
	var read_only_option = document.set_ftp_params.ftp_read_only.checked;
	var ftp_options      = document.getElementsByName('choose_ftp_options');

	var table_id     = document.getElementById('ftp_params_table');
	var users_table  = document.getElementById('ftp_users_list');
	var access_ip_id = document.getElementById('id_access_ip');
	var write_ip_id  = document.getElementById('id_write_ip');

	for (var i = 0;  i < ftp_options.length;  i++)
	{
		if (ftp_options[i].checked)
		{
			if (ftp_options[i].value == 'anonymous')
			{
				table_id.style.display = 'block';
				users_table.style.display = 'none';
				access_ip_id.focus();
				document.set_ftp_params.ftp_read_only.disabled = false;
				write_ip_id.style.background = '';
				write_ip_id.disabled = false;
				
				if (read_only_option == true)
				{
					table_id.style.display = 'block';
					users_table.style.display = 'none';
					access_ip_id.focus();
					write_ip_id.style.background = 'darkred';
					write_ip_id.disabled = true;
					write_ip_id.value = '';
				}

				else
				{
					table_id.style.display = 'block';
					users_table.style.display = 'none';
					access_ip_id.focus();
					write_ip_id.style.background = '';
					write_ip_id.disabled = false;
				}
			}

			else if (ftp_options[i].value == 'authenticated')
			{
				table_id.style.display = 'none';
				users_table.style.display = 'block';
				document.set_ftp_params.ftp_read_only.disabled = true;
			}
		}
	}
}

function ftp_update_validation()
{
	var ftp_read_ip  = '';
	var ftp_write_ip = '';

	var ftp_options_array = document.getElementsByName('choose_ftp_options');
	//var ftp_check_click   = document.set_ftp_params.ftp_button.value;
	var ftp_read_only     = document.set_ftp_params.ftp_read_only.checked;
	var grant_user        = document.getElementById('granted');
	var grant_groups      = document.getElementById('granted_groups');

	for (i = 0;  i < ftp_options_array.length;  i++)
	{
		if (ftp_options_array[i].checked == true)
		{
			if (ftp_options_array[i].value == 'anonymous')
			{
				ftp_read_ip       = document.set_ftp_params.ftp_access_ip.value;
				ftp_write_ip      = document.set_ftp_params.ftp_write_ip.value;

				if (ftp_read_ip == '' && ftp_write_ip == '')
				{
					//alert('Atleast one IP is required!');
					jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 19%; padding-top: 4%; font-family: status-bar;"> Atleast one IP is required!.</div>', 'Alert Dialog');
					document.set_ftp_params.ftp_access_ip.focus();
					return false;
				}

				error = validate_access_ip(ftp_read_ip);

				if(error != '')
				{
					//alert(error);
					jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 23%; padding-top: 4%; font-family: status-bar;">' + error + ' !</div>', 'Alert Dialog');
					document.set_ftp_params.ftp_access_ip.focus();
					//document.set_ftp_params.ftp_access_ip.value='';
					return false;
				}

				error = validate_access_ip(ftp_write_ip);
		
				if(error != '')
				{
					//alert("Please select a valid Ip")
					 jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 23%; padding-top: 4%; font-family: status-bar;">' + error + ' !</div>', 'Alert Dialog');

					document.set_ftp_params.ftp_write_ip.focus();
					//document.set_ftp_params.ftp_write_ip.value='';
					return false;
				}
			}

			else if (ftp_options_array[i].value == 'authenticated')
			{
				if(grant_user.value == '' && grant_groups.value == '')
				{
					//alert('Please Select Atleast Users OR Groups!');
					jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 23%; padding-top: 4%; font-family: status-bar;">No user/group selected for FTP config. !</div>', 'Alert Dialog');

					return false;
				}
			}
		}
	}

	//This code is commented here and used on the "set_ftp_settings.py" page because this has to run after "configure()" function

	var r =confirm("The Active connections will be Reset for making the configuration changes. Do you want to Restart Pro FTP?");

	if(r == true)
	{
		alert("Pro FTP is Restarting!");

		$.ajax(
		{
			type: 'POST',
	                url: 'restart-proftpd.py',
        	        data: 'proceed_page=proceed',

                	success: function(html)
        	        {	
                        	$('#response').html(html);
	                }
		});
	}

	else
	{
		alert("You choose not to restart Pro FTP this time but, you need to restart it to make changes occur!");
	}
}

function fp_update_validation()
{
	var ftp_access_ip    = document.set_ftp_params.ftp_access_ip.value;
	var ftp_write_ip     = document.set_ftp_params.ftp_write_ip.value;
	var ftp_options      = document.getElementsByName('choose_ftp_options');
	var read_only_option = document.set_ftp_params.ftp_read_only.checked;
	//var enable_ftp_opt   = document.set_ftp_params.enable_ftp.checked;

	var grant_users  = document.getElementById('ftp_granted');
	var grant_groups = document.getElementById('ftp_granted_groups');

	var ftp_read_only = '';
	var enable_ftp = '';

	ftp_access_ip_array = new Array();
	ftp_write_ip_array  = new Array();

	ftp_access_ip_array = ftp_access_ip.split(',');
	ftp_write_ip_array  = ftp_write_ip.split(',');

	for (var i = 0;  i < ftp_options.length;  i++)
	{
		if (ftp_options[i].checked)
		{
			if (ftp_options[i].value == 'authenticated' && enable_ftp_opt == true)
			{
				enable_ftp = 'on';

				document.set_ftp_params.ftp_access_ip.value = '';
				document.set_ftp_params.ftp_write_ip.value  = '';

				ftp_authenticated = 'authenticated';

				if (grant_users.value == '' || grant_groups.value == '')
				{
					alert('Grant user or group can\'t be empty!');
					return false;
				}
			}
	
			else if (ftp_options[i].value == 'anonymous' && enable_ftp_opt == true)
			{
				enable_ftp = 'on';

				ftp_authenticated = 'anonymous';

				if (read_only_option == true)
				{
					ftp_read_only = 'on';
				}

				else
				{
					ftp_read_only = '';
				}

				if (read_only_option == true)
				{
					if (ftp_access_ip == '')
					{
						alert('Enter a valid IP!');
						//jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 11%; padding-top: 4%; font-family: status-bar;">Please Enter a Valid Ip .</div>', 'Alert Dialog')
						return false;
					}

					for (i = 0;  i < ftp_access_ip_array.length;  i++)
					{
						error = check_ftp_ip(ftp_access_ip_array[i]);
					
						if (error != '')
						{
							alert(error);
							return false;
						}
					}
				}

				else
				{
					if (ftp_access_ip == '' && ftp_write_ip == '')
					{
						alert('Both IP\'s can\'t be empty!');
						return false;
					}

					else
					{
						if (ftp_access_ip != '')
						{
							for (i = 0;  i < ftp_access_ip_array.length;  i++)
							{
								error = check_ftp_ip(ftp_access_ip_array[i]);
					
								if (error != '')
								{
									alert(error);
									return false;
								}
							}
						}

						else
						{
							alert('Both IPs are required!');
							return false;
						}
						
						if (ftp_write_ip != '')
						{
							for (i = 0;  i < ftp_write_ip_array.length;  i++)
							{
								error = check_ftp_ip(ftp_write_ip_array[i]);
					
								if (error != '')
								{
									alert(error);
									return false;
								}
							}
						}
					
						else
						{
							alert('Both IPs are required!');
							return false;
						}
					}
				}
			}
		}
	}

	/*if (enable_ftp_opt == true)
	{
		var ftp_u_string = '';
		var ftp_g_string = '';

		ftp_uid = document.getElementById('ftp_granted');
		ftp_gid = document.getElementById('ftp_granted_groups');

		for (i = 0;  i < ftp_uid.options.length;  i++)
		{
			ftp_u_string += '$$' + ftp_uid.options[i].value;
		}

		for (i = 0;  i < ftp_gid.options.length;  i++)
		{
			ftp_g_string += '$$' + ftp_gid.options[i].value;
		}

		var i = ftp_u_string.indexOf('+');
		var j = ftp_g_string.indexOf('+');

		while (i > 0)
		{
			ftp_u_string = ftp_u_string.replace('+', '<PLUS>');
			i = ftp_u_string.indexOf('+');
		}

		while (j > 0)
		{
			ftp_g_string = ftp_g_string.replace('+', '<PLUS>');
			j = ftp_g_string.indexOf('+');
		}

		document.getElementById('ftp_wait').style.display = 'block';

		$.ajax(
		{
			type: 'POST',
			url: 'set_ftp_params.py',
			data: 'proceed_page=proceed&enable_ftp='+enable_ftp+'&hid_share='+document.set_ftp_params.hid_share.value+'&hid_path='+document.set_ftp_params.hid_path.value+'&hid_comment='+document.set_ftp_params.hid_comment.value+'&ftp_read_only='+ftp_read_only+'&choose_ftp_options='+ftp_authenticated+'&ftp_access_ip='+ftp_access_ip+'&ftp_write_ip='+ftp_write_ip+'&grant_users='+ftp_u_string+'&grant_groups='+ftp_g_string,

			success: function(html)
			{
				$('#id_ftp_wait').html(html);
			}
		});*/
	//}
/*
	else
	{
		document.getElementById('wait').style.display = 'block';

		$.ajax(
		{
			type: 'POST',
			url: 'set_ftp_params.py',
			data: 'proceed_page=proceed&enable_ftp=off&hid_share='+document.set_ftp_params.hid_share.value+'&hid_path='+document.set_ftp_params.hid_path.value+'&hid_comment='+document.set_ftp_params.hid_comment.value,

			success: function(html)
			{
				$('#response').html(html);
			}
		});
	}
	*/
	document.set_ftp_params.ftp_button.disabled = true;
	disable_all_other_forms('set_ftp_params');
}

function show_ftp_params()
{
	var ftp_params_tab_id = document.getElementById('id_ftp_parameters');
	var enable_ftp_opt    = document.set_ftp_params.enable_ftp.checked;
	var table_id          = document.getElementById('ftp_params_table');
	var users_table       = document.getElementById('ftp_users_list');

	set_ftp_parameters();

	if (enable_ftp_opt == true)

	{
		ftp_params_tab_id.style.display = 'block';
	}

	else
	{
		ftp_params_tab_id.style.display = 'none';
		table_id.style.display          = 'none';
		users_table.style.display       = 'none';
	}
}

function validate_share_afp()
{
	var use_afp    = document.afp_form.use_afp.checked;
	var radio_array = document.getElementsByName('afp_priv');
	var afp_grant_users  = document.afp_form.elements["afp_grant_users[]"];
        var afp_grant_groups = document.afp_form.elements["afp_grant_groups[]"];
	var advanced_per = document.afp_form.advanced_per.checked;
	var host_allow = document.getElementById('host_allow');
	var host_deny = document.getElementById('host_deny');
	var umask = document.getElementById('umask');
	var spacesExp = /[\s]/;
	var numbers = /^[0-7]+$/;

	if (use_afp == true)
        {
                for (i = 0;  i < radio_array.length;  i++)
                {
                        if (radio_array[i].checked)
                        {
                                if (radio_array[i].value == 'valid_user')
                                {
                                        afp_priv = 'valid_user';

                                        if ((afp_grant_users.length == 0) && (afp_grant_groups.length == 0) )
                                        {
                                                alert('Please choose either a user or a group!');
                                                return false;
                                        }

                                }

                                else
                                {
                                        afp_priv = 'guest';
                                }
                        }
                }
	}
	
	if (advanced_per == true)
	{
		if ((host_allow.value=='') && (host_deny.value=='') && (umask.value==''))
                {
                	alert('Please enter at least one value or Uncheck Advance Permission!');
                	return false;
		}

		if (host_allow.value == ',')
                {
                        alert('Enter a valid Host allow IP!');
                        return false;
                }

                if (host_deny.value == ',')
                {
                        alert('Enter a valid Host Deny IP!');
                        return false;
                }

		if(host_allow.value.match(spacesExp))
        	{
                	alert('Spaces are not allowed in Host allow IP!');
                	return false;
        	}

		if(host_deny.value.match(spacesExp))
                {
                        alert('Spaces are not allowed in Host deny IP!');
                        return false;
                }

		else
                {
                        error = validate_access_ip(host_allow.value);

                        if (error != '')
                        {
                                alert(error);
                                return false;
                        }

                        error = validate_access_ip(host_deny.value);

                        if (error != '')
                        {
                                alert(error);
                                return false;
                        }
                }

		if(umask.value!='')
		{
			if(umask.value.charAt(0) != '0') 
			{
				alert( 'First number in umask should be "0" !');
				return false;
			}

			if(umask.value.length != 4)
			{
				alert('Exact Four numbers are allowed in umask!');
				return false;
			}

			if(!umask.value.match(numbers))
			{	
				alert('First number in umask should be "0" other three numbers should be in the range "0-7" !');
				return false;
			}

			if(umask.value=="0777")
			{
				alert('"0777" value is not acceptable!');
				return false;
			}


		}
		
	
	}
}

function validate_afp_form()
{
	radio_array = new Array();
	var use_afp    = document.afp_form.use_afp.checked;
	var radio_array = document.getElementsByName('afp_priv');
	var ads_connection_status = document.afp_form.hid_connection_status.value;

	var afp_grant_users  = document.afp_form.elements["afp_grant_users[]"];
	var afp_grant_groups = document.afp_form.elements["afp_grant_groups[]"];

	var users_id  = document.getElementById('afp_granted');
	var groups_id = document.getElementById('afp_granted_groups');

	var afp_u_string = '';
	var afp_g_string = '';
	var afp_priv = '';

	if (use_afp == true)
	{
		for (i = 0;  i < radio_array.length;  i++)
		{
			if (radio_array[i].checked)
			{
				if (radio_array[i].value == 'valid_user')
				{
					afp_priv = 'valid_user';

					if (afp_grant_users.length == 0)
					{
						alert('Please choose a user!');
						return false;
					}
				}

				else
				{
					afp_priv = 'guest';
				}
			}
		}
	
		document.getElementById('wait').style.display = 'block';

		if (ads_connection_status != 'Join is OK')
		{
			for (i = 0;  i < users_id.options.length;  i++)
			{
				afp_u_string += '$$' + users_id.options[i].value;
			}

			for (i = 0;  i < groups_id.options.length;  i++)
			{
				afp_g_string += '$$' + groups_id.options[i].value;
			}
		}

		else
		{
			afp_u_string = 'x';
			afp_g_string = 'x';
		}

	/*	$.ajax(
		{
			type: 'POST',
			url: 'set_afp_params.py',
			data: 'hid_share='+document.afp_form.hid_share.value+'&proceed_page=proceed&hid_share_path='+document.afp_form.hid_share_path.value+'&use_afp=on&read_only='+document.afp_form.read_only.checked+'&afp_priv='+afp_priv+'&proceed_page=proceed&afp_u_string='+afp_u_string+'&afp_g_string='+afp_g_string,
			success: function(html)
			{
				$('#response').html(html);
			}
		});*/
	}

	else
	{
		document.getElementById('wait').style.display = 'block';

		$.ajax(
		{
			type: 'POST',
			url: 'set_afp_params.py',
			data: '&use_afp=off&proceed_page=proceed&hid_share='+document.afp_form.hid_share.value+'&hid_share_path='+document.afp_form.hid_share_path.value,
			success: function(html)
			{
				$('#response').html(html);
			}
		});
	}

	document.afp_form.action_but.disabled = true;
	disable_all_other_forms('afp_form');
}

function set_size()
{
	var iframe1_id = parent.document.getElementById('id_contents');
	var iframe2_id = parent.document.getElementById('id_users_list');
	var iframe3_id = parent.document.getElementById('id_perms_list');

	iframe1_id.style.width  = '99%';
	iframe1_id.style.height = '150px';

	iframe2_id.style.width  = '99%';
	iframe2_id.style.height = '200px';

	iframe3_id.style.width  = '99%';
	iframe3_id.style.height = '200px';
}

function validate_access_control_form()
{
	var file_path = document.access_control_form.selected_file.value;
	var ug_val    = parent.users_groups_frame.document.users_groups.granted_ug.value;


	if (file_path == '')
	{
		alert('You need to choose a file!');
		return false;
	}
	
	if (ug_val == '')
	{
		alert('You need to choose a user/group!');
		return false;
	}


	users_string = document.access_control_form.elements["hid_users[]"].value;

	document.getElementById('wait').style.display = 'block';

	$.ajax(
	{
		type: 'POST',
		url: 'set_access_control.py',
		data: 'proceed_page=proceed&selected_file='+file_path+'&users_groups='+document.access_control_form.users_groups.value+'&hid_users='+users_string+'&hid_share='+document.access_control_form.hid_share.value+'&hid_comment='+document.access_control_form.hid_comment.value+'&hid_path='+document.choose_share.share_list.value+'&hid_page='+document.access_control_form.hid_page.value,

		success: function(html)
		{
			$('#response').html(html);
		}
	});

	document.access_control_form.action_but.disabled = true;
	disable_all_other_forms('access_control_form');
}

function move_users_groups(fbox, tbox, val)
{
	if (val == 2 && fbox.value != '')
	{
		share   = parent.document.access_control_form.hid_share.value;
		comment = parent.document.access_control_form.hid_comment.value;
		path    = parent.document.access_control_form.selected_file.value;

		parent.document.access_control_form.action = 'remove_acl.py?string='+fbox.value+'&share='+share+'&comment='+comment+'&path='+path;
		parent.document.access_control_form.submit();
	}

	var arrFbox = new Array();
	var arrTbox = new Array();
	var arrLookup = new Array();
	var i;

	for (i = 0; i < tbox.options.length; i++)
	{
		arrLookup[tbox.options[i].text] = tbox.options[i].value;
		arrTbox[i] = tbox.options[i].text;
	}
	
	var fLength = 0;
	var tLength = arrTbox.length;

	for(i = 0; i < fbox.options.length; i++)
	{
		arrLookup[fbox.options[i].text] = fbox.options[i].value;

		if (fbox.options[i].selected && fbox.options[i].value != "")
		{
			arrTbox[tLength] = fbox.options[i].text;
			tLength++;
		}
			
		else
		{
			arrFbox[fLength] = fbox.options[i].text;
			fLength++;
		}
	}
	
	fbox.length = 0;
	tbox.length = 0;
	var c;
	
	for(c = 0; c < arrFbox.length; c++)
	{
		var no = new Option();
		
		no.value = arrLookup[arrFbox[c]];
		no.text = arrFbox[c];
		fbox[c] = no;
	}
	
	for(c = 0; c < arrTbox.length; c++)
	{
		var no = new Option();
		
		no.value = arrLookup[arrTbox[c]];
		no.text = arrTbox[c];
		tbox[c] = no;
	}
}

function show_users_perms(user_perms)
{
	//document.getElementById('granted_ug').selected.background = 'gray';
	var assigned_ug = '';

	index_of_u = user_perms.indexOf(':u:');
	index_of_g = user_perms.indexOf(':g:');

	if (index_of_u > 0 || index_of_g > 0)
	{
		assigned_ug = 'assigned';
	}
	
	if (assigned_ug != 'assigned')
	{
		if (user_perms != '')
		{
			var cur_user = parent.document.access_control_form.users_groups.value;

			parent.document.access_control_form.users_groups.value = '';
			parent.document.access_control_form.users_groups.value = cur_user + '|' + user_perms;

			parent.user_permissions.document.user_permission_form.o_read_perm.disabled  = false;
			parent.user_permissions.document.user_permission_form.o_write_perm.disabled = false;
			parent.user_permissions.document.user_permission_form.o_exec_perm.disabled  = false;
			parent.user_permissions.document.user_permission_form.recursive.disabled    = false;
			parent.user_permissions.document.user_permission_form.set.disabled          = false;

			parent.user_permissions.document.user_permission_form.o_read_perm.checked  = false;
			parent.user_permissions.document.user_permission_form.o_write_perm.checked = false;
			parent.user_permissions.document.user_permission_form.o_exec_perm.checked  = false;
			parent.user_permissions.document.user_permission_form.recursive.checked    = false;
		}

		else
		{
			parent.user_permissions.document.user_permission_form.o_read_perm.disabled  = true;
			parent.user_permissions.document.user_permission_form.o_write_perm.disabled = true;
			parent.user_permissions.document.user_permission_form.o_exec_perm.disabled  = true;
			parent.user_permissions.document.user_permission_form.recursive.disabled    = true;
		}
	}

	else if (assigned_ug == 'assigned')
	{
		if (user_perms != '')
		{
			var cur_user = parent.document.access_control_form.users_groups.value;

			parent.document.access_control_form.users_groups.value = '';
			parent.document.access_control_form.users_groups.value = cur_user + '|' + user_perms;
		}

		var user;
		var perms;

		user_perms = user_perms.replace(':u:', '::');
		user_perms = user_perms.replace(':g:', '::');

		disp_path = user_perms.substring(0, user_perms.indexOf(':'));
		user_perms1 = user_perms.substring(user_perms.indexOf('::') + 2, user_perms.length);

		user  = user_perms1.substring(0, user_perms1.indexOf(':'));
		perms = user_perms.substring(user_perms.indexOf(':') + user.length + 3, user_perms.length);

		r_perm = perms.indexOf('r');
		w_perm = perms.indexOf('w');
		x_perm = perms.indexOf('x');

		if (r_perm >= 0)
		{
			parent.user_permissions.document.user_permission_form.o_read_perm.checked = 'checked';
		}

		else
		{
			parent.user_permissions.document.user_permission_form.o_read_perm.checked = '';
		}

		if (w_perm > 0)
		{
			parent.user_permissions.document.user_permission_form.o_write_perm.checked = 'checked';
		}

		else
		{
			parent.user_permissions.document.user_permission_form.o_write_perm.checked = '';
		}

		if (x_perm > 0)
		{
			parent.user_permissions.document.user_permission_form.o_exec_perm.checked = 'checked';
		}

		else
		{
			parent.user_permissions.document.user_permission_form.o_exec_perm.checked = '';
		}

		if (parent.document.access_control_form.selected_file.value == '')
		{
			parent.document.access_control_form.selected_file.value = disp_path;
		}
		
		parent.user_permissions.document.user_permission_form.o_read_perm.disabled  = false;
		parent.user_permissions.document.user_permission_form.o_write_perm.disabled = false;
		parent.user_permissions.document.user_permission_form.o_exec_perm.disabled  = false;
		parent.user_permissions.document.user_permission_form.recursive.disabled    = false;
		parent.user_permissions.document.user_permission_form.set.disabled          = false;
	}
}

function reload_users_groups()
{
	parent.users_groups_frame.location.reload(true);
}

function write_val_to_textbox(read, write, exec, recur)
{
	var user = parent.document.access_control_form.users_groups.value;

	if (read == true)
	{
		r_perm = 'r';
	}

	else
	{
		r_perm = '-';
	}

	if (write == true)
	{
		w_perm = 'w';
	}
		
	else
	{
		w_perm = '-';
	}

	if (exec == true)
	{
		x_perm = 'x';
	}

	else
	{
		x_perm = '-';
	}

	if (recur == true)
	{
		recur = '-R';
	}

	else
	{
		recur = '';
	}
	
	perm = r_perm + w_perm + x_perm + ':' + recur;
	parent.document.access_control_form.users_groups.value = user + ':' + perm;

	var user_params = new Array();

	user_params.push(parent.document.access_control_form.users_groups.value);
	parent.document.access_control_form.elements['hid_users[]'].value = user_params;

	document.user_permission_form.set.disabled = true;
}

function show_path(path, file, dir_file)
{
	//parent.users_groups_frame.location.reload(true);
	//parent.user_permissions.location.reload(true);

	if (dir_file == 'file')
	{
		path = path.replace('%20', ' ');
		file = file.replace('%20', ' ');
	}

	else
	{
		if (file != '2dots')
		{
			path = path.replace('%20', ' ');
			file = file.replace('%20', ' ');

			parent.document.access_control_form.selected_file.value = path + '/' + file;
			parent.document.user_acl.selected_file.value            = path + '/' + file;
			parent.document.acl_info.selected_file.value            = path + '/' + file;
			parent.document.chang_owner_form.acl_path.value         = path + '/' + file;
			parent.document.reset_acl_form.selected_file.value      = path + '/' + file;
			parent.document.perm_form.selected_file.value           = path + '/' + file;
			parent.document.access_control_form.hid_dir_file.value  = dir_file;
			document.write('');
		}

		else
		{
			path = path.substr(0, path.lastIndexOf('/') + 1);
			path = path.replace('%20', ' ');

			parent.document.access_control_form.selected_file.value = path;
			parent.document.user_acl.selected_file.value            = path;
			parent.document.acl_info.selected_file.value            = path;
			parent.document.chang_owner_form.acl_path.value         = path;
			parent.document.reset_acl_form.selected_file.value      = path;
			parent.document.perm_form.selected_file.value           = path;
			document.write('');
		}
	}
}

function show_lpath(path, file, dir_file)
{
	if (dir_file == 'file')
	{
		path = path.replace('%20', ' ');
		file = file.replace('%20', ' ');

		//location.href = 'open_file.py?file=' + file;
		window.open('open_file.py?file=' + file);
	}

	else
	{
		if (file != '2dots')
		{
			path = path.replace('%20', ' ');
			file = file.replace('%20', ' ');

			document.write('');
		}

		else
		{
			path = path.substr(0, path.lastIndexOf('/') + 1);
			path = path.replace('%20', ' ');

			document.write('');
		}
	}
}

function show_iscsi_params()
{
	var iscsi_opt = document.iscsi_info.option_iscsi.checked;
	var iscsi_tab = document.getElementById('iscsi_table');
	var page_val  = document.iscsi_info.hid_page.value;

	if (iscsi_opt == true)
	{
		document.getElementById('wait').style.display = 'block';

		$.ajax(
		{
			type: 'POST',
			url: 'write_iscsi_options.php',
			data: 'check_to_proceed=proceed&p=on&pg='+page_val,

			success: function(html)
			{
				$('#response').html(html);
			}
		});
	}

	else
	{
		var exist_tgt = document.iscsi_info.hid_existing_target.value;

		if (exist_tgt != '')
		{
			alert('Active targets exist! Please delete all the initiators, hosts of all the targets(if any), and delete the targets.');
			return false;
		}

		else if (exist_tgt == '')
		{
			document.getElementById('wait').style.display = 'block';

			$.ajax(
			{
				type: 'POST',
				url: 'write_iscsi_options.php',
				data: 'check_to_proceed=proceed&p=off&pg='+page_val,

				success: function(html)
				{
					$('#response').html(html);
				}
			});
		}
	}

	disable_all_other_forms('iscsi_info');
}

function expand_options()
{
	var options_id  = document.getElementById('id_options');
	var opt_clicked = document.add_disk.expand.value;

	if (opt_clicked == 'Show Options')
	{
		options_id.style.display = 'block';
		document.add_disk.expand.value = 'Hide Options';
		document.add_disk.hid_expand.value = 'Hide Options';
	}

	else
	{
		options_id.style.display = 'none';
		document.add_disk.expand.value = 'Show Options';
		document.add_disk.hid_expand.value = 'Show Options';
	}
}

function show_chap_options()
{
	var chap_option   = document.add_disk.chap_option.checked;
	var id_chap_table = document.getElementById('id_chap_options');

	if (chap_option == true)
	{
		id_chap_table.style.display = 'block';
	}

	else
	{
		id_chap_table.style.display = 'none';
	}
}

function validate_delete_target()
{
	var select_target = document.delete_target.target_to_delete.value;
        if(select_target == 'tar_to_del')
        {
	        jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family: status-bar;">Select the target to Delete</div>', 'Alert Dialog');
        	document.delete_target.target_to_delete.focus();
	        return false;
	}

	else
        {
                document.getElementById('wait').style.display = 'block';

        }


}

function validate_remove_ini()
{
	var select_target = document.del_initr_from_target.choose_list.value;
	var select_ini_name = document.del_initr_from_target.initr_list.value;

        if(select_target == 'choose_list_val')
        {
	        jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family: status-bar;">Select the target to Delete</div>', 'Alert Dialog');
        	document.del_initr_from_target.choose_list.focus();
	        return false;
        }

	if(select_ini_name == 'initr_list_val')
        {
        	jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family: status-bar;">Select the Initiator name to Delete</div>', 'Alert Dialog');
	        document.del_initr_from_target.initr_list.focus();
        	return false;
        }
}

function validate_add_initiator()
{
	var select_target = document.add_ips_form.list_targets.value;
	var ini_name = document.add_ips_form.all_portal.value;
	var checkoptions = document.add_ips_form.check_all_portal.checked;
	var checkips     = document.add_ips_form.elements["check_portal[]"];

	var initiatorpattern = new RegExp("^iqn\\.[0-9]{4}\-[0-9]{2}\\.");

	var iniarray = new Array();
	iniarray     = ini_name.split(':');

	if (iniarray.length < 2 && ini_name != '*')
	{
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:-7%; padding-top: 0; font-family: monospace; width:100%;">Enter a proper initiator name! Format: "iqn.Date(<span><font color="darkred"><b>0000-00</b></font></span>).Naming Authority(<span><font color="darkgreen"><b>com.example</b></font></span>):String defined by naming authority!"</div>', 'Iscsi Alert');
		document.add_ips_form.list_targets.focus();
	}
	
	checkstring = '';

	if(select_target == 'list_ini_val')
	{
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:32%; padding-top: 4%; font-family: status-bar;">Choose the target</div>', 'Iscsi Alert');
		document.add_ips_form.list_targets.focus();
		return false;
	}

	if(ini_name == '')
	{
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family: status-bar;">Initiator name can not be blank!</div>', 'Iscsi Alert');
		document.add_ips_form.all_portal.focus();
		return false;
	}

	if (ini_name.indexOf('iqn.') != 0 && ini_name != '*')
	{

		 jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family: status-bar;">Initiator name should Start with "iqn." or it should be "*"!</div>', 'Iscsi Alert');
		//alert('Initiator name should start with "iqn." or it should be "*"!');
		return false;
	}

	if (ini_name == 'iqn.' && ini_name != '*')
	{
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family: status-bar;">Enter a proper initiator name! There should be name after "iqn."</div>', 'Iscsi Alert');
		return false;
	}

	if (initiatorpattern.exec(ini_name) == null && ini_name != '*')
	{
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: -7%; padding-top: 0;width:100%;font-family:monospace;">Enter a proper initiator name! Format: "iqn.Date(<span><font color="darkred"><b>0000-00</b></font></span>).Naming Authority(<span><font color="darkred"><b>com.example</b></font></span>):String defined by naming authority"</div>', 'Iscsi Alert');
		return false;
	}

	for (i = 0;  i < checkips.length;  i++)
	{
		if (checkips[i].checked == true)
		{
			checkstring += checkips[i].value;
		}
	}

	if (checkstring == '' && checkoptions == false)
	{
		//alert('Choose an IP or check the "Add All" option!');
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family: status-bar;">Select the Interface</div>', 'Iscsi Alert');
		return false;
	}

	
}

function validate_assign_target()
{
	var select_target = document.add_disk_to_target.target_for_disk.value;
	var sel_disk = document.add_disk_to_target.select_disk.value;
	var sel_lun = document.add_disk_to_target.select_lun.value;

        if(select_target == 'assign_tar')
        {
	        jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family: status-bar;">Select the target to Assign</div>', 'Alert Dialog');
        	document.add_disk_to_target.target_for_disk.focus();
	        return false;
        }

	if(sel_disk == 'select_dis_val')
	{
	        jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family: status-bar;">Select the Disk to Assign</div>', 'Alert Dialog');
        	document.add_disk_to_target.select_disk.focus();
	        return false;
        }

	if(sel_lun == 'select_lun_val')
        {
	        jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family: status-bar;">Select the Lun to Assign</div>', 'Alert Dialog');
        	document.add_disk_to_target.select_lun.focus();
	        return false;
        }
}


function validate_enable_fc()
{
        var select_target = document.enable_fc.enable_tar_name.value;
        //var enable_all_tar = document.enable_fc.enable_all.checked;

        if(select_target == '')
        {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:15%; padding-top: 4%; font-family: status-bar;">Select Target to Enable</div>', 'Alert Dialog');
                document.enable_fc.enable_tar_name.focus();
                return false;
        }
}

function validate_enable_srp()
{
        var select_target = document.enable_srp.enable_tar_name.value;
        //var enable_all_tar = document.enable_fc.enable_all.checked;

        if(select_target == '')
        {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:15%; padding-top: 4%; font-family: status-bar;">Select Target to Enable</div>', 'Alert Dialog');
                document.enable_srp.enable_tar_name.focus();
                return false;
        }
}


function validate_disable_fc()
{
        var select_target = document.disable_fc.disable_target_name.value;
        //var disable_all_tar = document.disable_fc.disable_all.checked;

        if(select_target == '')  
        {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:15%; padding-top: 4%; font-family: status-bar;">Select the Target to Disable</div>', 'Alert Dialog');
                document.disable_fc.disable_target_name.focus();
                return false;
        }
}

function validate_disable_srp()
{
        var select_target = document.disable_srp.disable_target_name.value;
        //var disable_all_tar = document.disable_fc.disable_all.checked;

        if(select_target == '')
        {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:15%; padding-top: 4%; font-family: status-bar;">Select the Target to Disable</div>', 'Alert Dialog');
                document.disable_srp.disable_target_name.focus();
                return false;
        }
}



function validate_fc_assign_target()
{
        var select_target = document.add_disk_to_fc_target.assign_disk_nm.value;
        var sel_disk = document.add_disk_to_fc_target.select_disk.value;
        var sel_lun = document.add_disk_to_fc_target.select_lun.value;

        if(select_target == 'assign_tar')
        {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family: status-bar;">Select the target to Assign</div>', 'Alert Dialog');
                document.add_disk_to_fc_target.assign_disk_nm.focus();
                return false;
        }

        if(sel_disk == 'select_dis_val')
        {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family: status-bar;">Select the Disk to Assign</div>', 'Alert Dialog');
                document.add_disk_to_fc_target.select_disk.focus();
                return false;
        }

        if(sel_lun == 'select_lun_val')
        {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family: status-bar;">Select the Lun to Assign</div>', 'Alert Dialog');
                document.add_disk_to_fc_target.select_lun.focus();
                return false;
        }
}

function validate_srp_assign_target()
{
        var select_target = document.add_disk_to_srp_target.assign_disk_nm.value;
        var sel_disk = document.add_disk_to_srp_target.select_disk.value;
        var sel_lun = document.add_disk_to_srp_target.select_lun.value;

        if(select_target == 'assign_tar')
        {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family: status-bar;">Select the target to Assign</div>', 'Alert Dialog');
                document.add_disk_to_srp_target.assign_disk_nm.focus();
                return false;
        }

        if(sel_disk == 'select_dis_val')
        {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family: status-bar;">Select the Disk to Assign</div>', 'Alert Dialog');
                document.add_disk_to_srp_target.select_disk.focus();
                return false;
        }

        if(sel_lun == 'select_lun_val')
        {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family: status-bar;">Select the Lun to Assign</div>', 'Alert Dialog');
                document.add_disk_to_srp_target.select_lun.focus();
                return false;
        }
}

function validate_del_fc_assign_target()
{
        var select_target = document.del_disk_from_fc_target.delete_target_name.value;
        var disk_del = document.del_disk_from_fc_target.select_disk_remove.value;

        if(select_target == 'del_assign_tar')
        {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family: status-bar;">Select the target to Delete</div>', 'Alert Dialog');
                document.del_disk_from_fc_target.delete_target_name.focus();
                return false;
        }

        if(disk_del == 'disk_del_op')
        {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family: status-bar;">Select the Disk to Delete</div>', 'Alert Dialog');
                document.del_disk_from_fc_target.select_disk_remove.focus();
                return false;
        }
}


function validate_del_srp_assign_target()
{
        var select_target = document.del_disk_from_srp_target.delete_target_name.value;
        var disk_del = document.del_disk_from_srp_target.select_disk_remove.value;

        if(select_target == 'del_assign_tar')
        {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family: status-bar;">Select the target to Delete</div>', 'Alert Dialog');
                document.del_disk_from_srp_target.delete_target_name.focus();
                return false;
        }

        if(disk_del == 'disk_del_op')
        {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family: status-bar;">Select the Disk to Delete</div>', 'Fc Alert');
                document.del_disk_from_srp_target.select_disk_remove.focus();
                return false;
        }
}

function fc_map()
{
	var src_target = document.form1.select_source.value;
	var dest_target = document.form1.select_destination.value;
	if(src_target == 'select_src_val')
		{
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family: status-bar;">select the Source target</div>', 'Fc Alert');
		return false;

		}
	if(dest_target == 'select_dest_val')
                {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family: status-bar;">select the destination target</div>', 'Fc Alert');
                return false;

                }
}

function srp_map()
{
        var src_target = document.form1.select_source.value;
        var dest_target = document.form1.select_destination.value;
        if(src_target == 'select_src_val')
                {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family: status-bar;">select the Source target</div>', 'Srp Alert');
                return false;

                }
        if(dest_target == 'select_dest_val')
                {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family: status-bar;">select the destination target</div>', 'Srp Alert');
                return false;

                }
}


function validate_fc_add_initiator()
{
	var select_target = document.add_fc_ini.list_targets.value;
	var ini_name = document.add_fc_ini.all_portal.value;
	//alert(ini_name)
	var validChar='*012345678ABCDEFabcdef:';   // legal chars
	
	var strlen=ini_name.length; 
	//alert(strlen)
	
	var array_nw = new Array();
	var array_nw = ini_name.split(':');
	//alert(array_nw)
	//var ini_name=ini_name.toUpperCase(); // case insensitive

	if(select_target == 'list_ini_val')
	{
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family: status-bar;">Choose the target</div>', 'Alert Dialog');
		document.add_fc_ini.list_targets.focus();
		return false;
	}

	if(ini_name == '')
	{
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family: status-bar;">Initiator name can not be blank!</div>', 'Alert Dialog');
		document.add_fc_ini.all_portal.focus();
		return false;
	}

	if (ini_name != '*')
	{
// Now scan for illegal characters
		for(idx = 0;  idx < strlen;  idx++)
		{
			if(validChar.indexOf(ini_name.charAt(idx)) < 0)
			{
				//alert("Entry must be hexadecimal!");
				jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family:monospace;">Initiator name will be Hexadecimal format or (<span><font color= "darkred">*</font></span>)!</div>', 'Alert Dialog');
				return false;
			}		
		
		}
		
		if(array_nw.length !=8 ) 
		{
			//alert('must be 8 of group')
			jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family: status-bar;">Must be 8 of group!</div>', 'Alert Dialog');
			return false;
		}

		for(i = 0;  i < array_nw.length;  i++)
		{
			if(array_nw[i].length != 2)
			{
				//alert('must be a 2 in a group')
				jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family: status-bar;">Must be a 2 a group!</div>', 'Alert Dialog');
				return false
			}
		}
	}
}

function validate_srp_add_initiator()
{
	var select_target = document.add_srp_ini.list_targets.value;
	var ini_name = document.add_srp_ini.all_portal.value;
	//alert(ini_name)
	var validChar='*012345678ABCDEFabcdef:';   // legal chars
	
	var strlen=ini_name.length; 
	//alert(strlen)
	
	var array_nw = new Array();
	var array_nw = ini_name.split(':');
	//alert(array_nw)
	//var ini_name=ini_name.toUpperCase(); // case insensitive

	if(select_target == 'list_ini_val')
	{
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:35%; padding-top: 4%; font-family: status-bar;">Choose the target</div>', 'Alert Dialog');
		document.add_srp_ini.list_targets.focus();
		return false;
	}

	if(ini_name == '')
	{
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family: status-bar;">Initiator name can not be blank!</div>', 'Alert Dialog');
		document.add_srp_ini.all_portal.focus();
		return false;
	}

	if (ini_name != '*')
	{
		//alert(ini_name)
// Now scan for illegal characters
		for(idx = 0;  idx < strlen;  idx++)
		{
			//alert(strlen)
			if(validChar.indexOf(ini_name.charAt(idx)) < 0)
			{
				//alert(in)
				//alert("Entry must be hexadecimal!");
				jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family:monospace;">Initiator name will be Hexadecimal format or (<span><font color= "darkred">*</font></span>)!</div>', 'Alert Dialog');
				  return false;

			}		
		
		}
		
		if(array_nw.length != 4 ) 
		{
			//alert(array_nw)
			//alert('must be 8 of group')
			jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family: status-bar;">Must be 4 of group!</div>', 'Alert Dialog');
			return false;
		}

		for(i = 0;  i < array_nw.length;  i++)
		{
			if(array_nw[i].length != 4)
			{
				//alert('must be a 2 in a group')
				jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family: status-bar;">Must be a 4 a group!</div>', 'Alert Dialog');
				return false
			}
		}
	}
}





function validate_fc_remove_ini()
{
        var select_target = document.fc_ini_delete.choose_list.value;
        var select_ini_name = document.fc_ini_delete.initr_list.value;

        if(select_target == 'choose_list_val')
        {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family: status-bar;">Select the target to Delete</div>', 'Alert Dialog');
                document.fc_ini_delete.choose_list.focus();
                return false;
        }

        if(select_ini_name == 'initr_list_val')
        {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family: status-bar;">Select the Initiator name to Delete</div>', 'Alert Dialog');
                document.fc_ini_delete.initr_list.focus();
                return false;
        }
}

function validate_srp_remove_ini()
{
        var select_target = document.srp_ini_delete.choose_list.value;
        var select_ini_name = document.srp_ini_delete.initr_list.value;

        if(select_target == 'choose_list_val')
        {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family: status-bar;">Select the target to Delete</div>', 'Alert Dialog');
                document.srp_ini_delete.choose_list.focus();
                return false;
        }

        if(select_ini_name == 'initr_list_val')
        {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family: status-bar;">Select the Initiator name to Delete</div>', 'Alert Dialog');
                document.srp_ini_delete.initr_list.focus();
                return false;
        }
}



function validate_del_assign_target()
{
	var select_target = document.del_disk_from_target.target_remove.value;
	var disk_del = document.del_disk_from_target.select_disk_remove.value;

        if(select_target == 'del_assign_tar')
        {
	        jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family: status-bar;">Select the target to Delete</div>', 'Alert Dialog');
        	document.del_disk_from_target.target_remove.focus();
	        return false;
        }

	if(disk_del == 'disk_del_op')
        {
	        jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family: status-bar;">Select the Disk to Delete</div>', 'Alert Dialog');
        	document.del_disk_from_target.select_disk_remove.focus();
	        return false;
        }
}

function validate_iscsi_target_form()
{
	var targetpattern = new RegExp("^iqn\\.[0-9]{4}\-[0-9]{2}\\.");
	var iscsi_val     = document.add_disk.iscsi_target.value;
	var sp_chars      = "~`\ !@#$%^&*()+=[]\\\';,/{}|\"<>?";

	var target_array = iscsi_val.split(':');

	if (target_array.length < 2)
	{
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:20%; padding-top:2%; font-family: status-bar;">Please enter a valid target name! Should be in the format "iqn.<year>-<month>.<com>.<domainname>:<somevalue>"</div>', 'Alert Dialog');
		return false;
	}

	for (var i = 0;  i < iscsi_val.length;  i++)
	{
		if (sp_chars.indexOf(iscsi_val.charAt(i)) != -1)
		{
			jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:20%; padding-top:2%; font-family: status-bar;">Please enter a valid target name! Special characters not allowed</div>', 'Alert Dialog');
                
			return false;
		}
	}

	if (target_array[1] == '')
	{
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:20%; padding-top:2%; font-family: status-bar;">Enter a proper name for target like: "iqn.targetname"!</div>', 'Alert Dialog');
		return false;
	}

	//if (iscsi_val.indexOf(target) != 0)
	else if (targetpattern.exec(iscsi_val) == null)
	{
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:20%; padding-top:2%; font-family: status-bar;">Target name should be in the format "iqn.2009-05.com.somedomain"</div>', 'Alert Dialog');
                
		return false;
	}

	else
	{
		document.getElementById('wait').style.display = 'block';

	}
}

function validate_iscsi_properties_form()
{
	var target    = 'iqn.2009-05.com.tyronesystems';
	var iscsi_val = document.add_disk.iscsi_target.value;
	var butt_val  = document.add_disk.expand.value;

	var ddigest     = document.add_disk.ddigest.value;
	var fbl         = document.add_disk.fbl.value;
	var hd          = document.add_disk.hd.value;
	var idata       = document.add_disk.idata.value;
	var initr2t     = document.add_disk.initr2t.value;
	var mbl         = document.add_disk.mbl.value;
	var mor2t       = document.add_disk.mor2t.value;
	var mrdsl       = document.add_disk.mrdsl.value;
	var max_conn    = document.add_disk.max_conn.value;
	var medsl       = document.add_disk.medsl.value;
	var nopinterval = document.add_disk.nopinterval.value;
	var ppacl       = document.add_disk.ppacl.value;
	var qc          = document.add_disk.qc.value;
	var rspto       = document.add_disk.rspto.value;

	if (ddigest == '' || fbl == '' || hd == '' || idata == '' || initr2t == '' || mbl == '' || mor2t == '' || mrdsl == '' || max_conn == '' || medsl == '' || nopinterval == '' || ppacl == '' || qc == '' || rspto == '')
	{
		alert('All fields are mandatory!');
		return false;
	}

	else
	{
		var num_pattern = /^([0-9]{1,8})\.([0-9]{1,8})|([0-9]{1,8})$/;

		fbl_array         = fbl.match(num_pattern) ;
		mbl_array         = mbl.match(num_pattern);
		mor2t_array       = mor2t.match(num_pattern);
		mrdsl_array       = mrdsl.match(num_pattern);
		max_conn_array    = max_conn.match(num_pattern);
		medsl_array       = medsl.match(num_pattern);
		nopinterval_array = nopinterval.match(num_pattern);
		ppacl_array       = ppacl.match(num_pattern);
		qc_array          = qc.match(num_pattern);
		rspto_array       = rspto.match(num_pattern);

		if (fbl_array == null)
		{
			alert('Enter a valid value for [Default first burst length]!');
			return false;
		}

		if (mbl_array == null)
		{
			alert('Enter a valid value for [Max burst length]!');
			return false;
		}

		if (mor2t_array == null)
		{
			alert('Enter a valid value for [Max outstanding R2T]!');
			return false;
		}

		if (mrdsl_array == null)
		{
			alert('Enter a valid value for [Max recv. data segment length]!');
			return false;
		}

		if (max_conn_array == null)
		{
			alert('Enter a valid value for [Max sessions]!');
			return false;
		}

		if (medsl_array == null)
		{
			alert('Enter a valid value for [Max xmit data segment length]!');
			return false;
		}

		if (nopinterval_array == null)
		{
			alert('Enter a valid value for [Nop in interval]!');
			return false;
		}

		if (ppacl_array == null)
		{
			alert('Enter a valid value for [Per portal ACL]!');
			return false;
		}

		if (qc_array == null)
		{
			alert('Enter a valid value for [Queued command]!');
			return false;
		}

		if (rspto_array == null)
		{
			alert('Enter a valida value for [RSP timeout]!');
			return false;
		}
	}

	var target_array = iscsi_val.split(':');

	if (target_array[0] != target)
	{
		alert('Make sure target name starts with \''+target+':\'');
		return false;
	}

	document.getElementById('wait').style.display = 'block';

	$.ajax(
	{
		type: 'POST',
		url: 'add_disk.php',
		data: 'proceed_page=proceed&iscsi_target='+iscsi_val+'&alias='+alias_val+'&hid_expand='+butt_val+'&ddigest='+ddigest+'&fbl='+fbl+'&hd='+hd+'&idata='+idata+'&initr2t='+initr2t+'&mbl='+mbl+'&mor2t='+mor2t+'&mrdsl='+mrdsl+'&max_conn='+max_conn+'&medsl='+medsl+'&nopinterval='+nopinterval+'&ppacl='+ppacl+'&qc='+qc+'&rspto='+rspto,

		success: function(html)
		{
			$('#response').html(html);
		}
	});

	document.add_disk.action_butt.disabled = true;
	disable_all_other_forms('add_disk');
}

function run_get_luns()
{
        var target_for_disk = document.add_disk_to_target.target_for_disk.value;

        if (target_for_disk != '')
        {
                document.getElementById('menu').style.display = 'block';

                $.ajax(
                {
                        type: 'POST',
                        url: 'find_lun_for_target.php',
                        data: 'target='+target_for_disk,

                        success: function(html)
                        {
                                $('#menu').html(html);
                        }
                });
        }
}

function confirm_delete_target(target, active_session_string)
{
        if (active_session_string != '')
        {
        	search_active_session = active_session_string.indexOf(target);

                tgt_init_array = new Array();

                tgt_init_array = active_session_string.split('->');

                initiator = tgt_init_array[1];
                initiator = initiator.replace(' ', ', ');
	}

        if (search_active_session >= 0)
        {
		var response = confirm('\''+target+'\' is in use under the initiator name \''+initiator+'\'. Do you still want to delete the target?');

		if (response == true)
		{
			document.getElementById('wait').style.display = 'block';

			$.ajax(
			{
				type: 'POST',
				url: 'delete_target.php',
				data: 'proceed_page=proceed&target_to_delete='+target,

				success: function(html)
				{
					$('#response').html(html);
				}
			});
		}

		else
		{
			return false;
		}
	}

	else
	{
		document.getElementById('wait').style.display = 'block';

                $.ajax(
		{
               		type: 'POST',
                	url: 'delete_target.php',
	                data: 'proceed_page=proceed&target_to_delete='+target,

       		        success: function(html)
               		{
                       		$('#response').html(html);
                        }
       	        });
	}
}

function validate_add_iscsi_target()
{
	var target = document.add_disk_to_target.target_for_disk.value;
	var disk   = document.add_disk_to_target.disk_to_add.value;

	if (target == '')
	{
		alert('Please choose a target name!');
		return false;
	}

	if (disk == '')
	{
		alert('Please choose a disk!');
		return false;
	}

	document.getElementById('wait').style.display = 'block';

	$.ajax(
	{
		type: 'POST',
		url: 'add_disk_to_target.php',
		data: 'proceed_page=proceed&target_for_disk='+target+'&disk_to_add='+disk+'&lun_to_add='+document.add_disk_to_target.lun_to_add.value,

		success: function(html)
		{
			$('#response').html(html);
		}
	});

	document.add_disk_to_target.add_disk.disabled = true;
	disable_all_other_forms('add_disk_to_target');
}

function validate_initiator_form()
{
	var target_name = document.add_initiator.target_initiator.value;
	var hostname    = document.add_initiator.hostname.value;
	var ip_addr     = document.add_initiator.ip.value;
	var initiator   = document.add_initiator.initr_name.value;

	if (target_name == '')
	{
		alert('Please choose a target name!');
		return false;
	}

	if (hostname != '' && ip_addr != '')
	{
		alert('Please enter either hostname or IP! Can\'t allow both!');
		return false;
	}

	if (hostname == '' && ip_addr == '')
	{
		alert('Both hostname and IP can\'t be blank!');
		return false;
	}

	if (ip_addr != '')
	{
		var ip_error = '';
		var ipPattern;
	
		ipPattern = /^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/;

		var ip_array = ip_addr.match(ipPattern);

		if (ip_addr == "0.0.0.0")
		{
			ip_error = ip_addr+' is not a valid IP';
		}
	
		else if (ip_addr == "255.255.255.255")
		{
			ip_error = ip_addr+' is not a valid IP';
		}

		if (ip_array == null)
		{
			ip_error = ip_addr+' is not a valid IP';
		}

		else if (ip_array != null)
		{
			for (i = 1; i <= 4; i++)
			{
				thisSegment = ip_array[i];

				if (thisSegment > 255)
				{
					ip_error = ip_addr+' is not a valid IP';
					i = 4;
				}
			
				if ((i == 0) && (thisSegment > 255))
				{
					ip_error = ip_addr+' is not a valid IP';
					i = 4;
				}
			}
		}

		if (ip_error != '')
		{
			alert(ip_error);
			return false;
		}
	}

	if (hostname != '')
	{
		var sp_chars  = "\ \ !@#$%^&*()+=[]\\\';,/{}|.\":<>?";

		for (var i = 0;  i < hostname.length;  i++)
		{
			if (sp_chars.indexOf(hostname.charAt(i)) != -1)
			{
				alert('Please enter a valid host name! Special characters other than \'-\' and \'_\' not allowed! ');
				return false;
			}
		}
	}

	if (initiator == '')
	{
		alert('Please enter an initiator name!');
		return false;
	}

		
	document.getElementById('wait').style.display = 'block';

	$.ajax(
	{
		type: 'POST',
		url: 'add_initiator.php',
		data: 'proceed_page=proceed&target_initiator='+target_name+'&hostname='+hostname+'&ip='+ip_addr+'&initr_name='+initiator,
		success: function(html)
		{
			$('#response').html(html);
		}
	});

	disable_all_other_forms('add_initiator');
}

function run_get_disks()
{
	var target_val = document.del_disk_from_target.target_list.value;

        if(target_val != '')
        {
	        document.getElementById('deletedisk').style.display = 'block';
        	
		$.ajax(
	        {
        	         type: 'POST',
                	 url: 'find_disk_for_target.php',
                	 data: 't='+target_val,
			 success: function(html)
        	         {
                	         $('#deletedisk').html(html);
	                 }
	        });
	}
}

function run_get_initrs()
{
	var target_val = document.del_initr_from_target.target_list.value;

	if (target_val != '')
	{
		document.del_initr_from_target.action = 'find_initr_for_target.php?t='+target_val;
		document.del_initr_from_target.submit();
	}
}

function get_hosts()
{
	var target_val = document.del_host_from_target.target_list.value;

	document.getElementById('get_hosts').style.display = 'block';

	$.ajax(
	{
		type: 'POST',
		url: 'find_host_for_target.php',
		data: 'h='+target_val,

		success: function(html)
		{
			$('#id_get_hosts').html(html);
		}
	});
}

function validate_del_disk(target, disk, active_session_string)
{
	if (target == '' || disk == '')
	{
		alert('This operation requires both target name and disk name!');
		return false;
	}

	if (active_session_string != '')
	{
		search_active_session = active_session_string.indexOf(target);

		tgt_init_array = new Array();

		tgt_init_array = active_session_string.split('->');

		initiator = tgt_init_array[1];
		initiator = initiator.replace(' ', ', ');
	}

	if (search_active_session >= 0)
	{
		var response = confirm('\''+disk+'\' is in use under the initiator name \''+initiator+'\'. Do you still want to delete the disk?');

		if (response == true)
		{
			document.getElementById('wait').style.display = 'block';

			$.ajax(
			{
				type: 'POST',
				url: 'del_disk_from_target.php',
				data: 'target_list='+target+'&proceed_page=proceed&disks_list='+disk,

				success: function(html)
				{
					$('#response').html(html);
				}
			});
		}
		
		else
		{
			return false;
		}
	}
		
	else
	{
		document.getElementById('wait').style.display = 'block';

		$.ajax(
		{
			type: 'POST',
			url: 'del_disk_from_target.php',
			data: 'target_list='+target+'&proceed_page=proceed&disks_list='+disk,

			success: function(html)
			{
				$('#response').html(html);
			}
		});
	}

	disable_all_other_forms('del_disk_from_target');
}

function validate_fc_del_disk(target, disk, active_session_string)
{
	delete_all = 'Remove selected disk';
	
	if (target == '' || disk == '')
	{
		alert('This operation requires both target name and disk name!');
		return false;
	}

	if (active_session_string != '')
	{
		search_active_session = active_session_string.indexOf(target);

		tgt_init_array = new Array();

		tgt_init_array = active_session_string.split('->');

		initiator = tgt_init_array[1];
		initiator = initiator.replace(' ', ', ');
	}
	
	if (search_active_session >= 0)
	{
		var response = confirm('\''+disk+'\' is in use under the initiator name \''+initiator+'\'. Do you still want to delete the disk?');

		if (response == true)
		{
			document.getElementById('fc_del_disk').style.display = 'block';

			$.ajax(
			{
				type: 'POST',
				url: 'del_disk_from_zone.php',
				data: 'zone_list='+target+'&proceed_page=proceed&disks_list='+disk+'&del_from_zone='+delete_all,
				success: function(html)
				{
					$('#id_fc_del_disk').html(html);
				}
			});
		}
		
		else
		{
			return false;
		}
	}
	
	else
	{
		document.getElementById('fc_del_disk').style.display = 'block';

		$.ajax(
		{
			type: 'POST',
			url: 'del_disk_from_zone.php',
			data: 'zone_list='+target+'&proceed_page=proceed&disks_list='+disk+'&del_from_zone='+delete_all,
			success: function(html)
			{
				$('#id_fc_del_disk').html(html);
			}
		});
	}

	disable_all_other_forms('del_disk_from_zone');
}

function validate_del_initr(initiator, active_session_string)
{
	if (initiator == '')
	{
		alert('You need to choose an initiator!');
		return false;
	}

	var target = document.add_properties.list_targets.value;
	var test_initiator = '';
	var initiator1 = '';
	var target_arr = '';

	var find_initiator = initiator.indexOf('*');

	if (find_initiator == 0)
	{
		var find_target = active_session_string.indexOf(target);
		
		if (find_target >= 0)
		{
			var response = confirm('Initiator is in use. Do you still want to delete the initiator?');

			if (response == true)
			{
				document.getElementById('wait').style.display = 'block';

				$.ajax(
				{
					type: 'POST',
					url: 'del_initr_from_target.php',
					data: 'proceed_page=proceed&target_list='+target+'&initr_list='+initiator,

					success: function(html)
					{
						$('#response').html(html);
					}
				});

				disable_all_other_forms('del_initr_from_target');
			}

			else
			{
				return false;
			}
		}

		else
		{
			document.getElementById('wait').style.display = 'block';

			$.ajax(
			{
				type: 'POST',
				url: 'del_initr_from_target.php',
				data: 'proceed_page=proceed&target_list='+target+'&initr_list='+initiator,

				success: function(html)
				{
					$('#response').html(html);
				}
			});

			disable_all_other_forms('del_initr_from_target');
		}
	}

	else
	{
		test_initiator = initiator.substring(0, initiator.indexOf('#'));

		if (test_initiator == '')
		{
			test_initiator = initiator;
		}

        	if (active_session_string != '' || initiator == '*')
	        {
        		search_active_session = active_session_string.indexOf(initiator);
	
        	        tgt_init_array = new Array();

                	tgt_init_array = active_session_string.split('->');
			target_arr = tgt_init_array[0];

        	        if (find_initiator == 0)
			{
				initiator1 = '*';
			}

			else
			{
				initiator1 = tgt_init_array[1];
		                initiator1 = initiator1.replace(' ', ', ');
				initiator1 = initiator1.substring(0, initiator1.indexOf('#'));
			}
		}
	
		if (test_initiator == initiator1 && target == target_arr)
		{
			var response = confirm('Initiator \''+initiator1+'\' is in use. Do you still want to delete the initiator?');

			if (response == true)
			{
				document.getElementById('wait').style.display = 'block';

				$.ajax(
				{
					type: 'POST',
					url: 'del_initr_from_target.php',
					data: 'proceed_page=proceed&target_list='+target+'&initr_list='+initiator,

					success: function(html)
					{
						$('#response').html(html);
					}
				});

				disable_all_other_forms('del_initr_from_target');
			}

			else
			{
				return false;
			}
		}

		else
		{
			document.getElementById('wait').style.display = 'block';

			$.ajax(
			{
				type: 'POST',
				url: 'del_initr_from_target.php',
				data: 'proceed_page=proceed&target_list='+target+'&initr_list='+initiator,

				success: function(html)
				{
					$('#response').html(html);
				}
			});

			disable_all_other_forms('del_initr_from_target');
		}
	}
}

function validate_del_host(target, host)
{
	if (target == '' || host == '')
	{
		//alert('This operation requires both target name and host name!');
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:-4%; padding-top: 4%; font-family: status-bar;">This operation requires both target name and host name</div>', 'Alert Dialog');
		return false;
	}

	document.getElementById('wait').style.display = 'block';

	$.ajax(
	{
		type: 'POST',
		url: 'del_host_from_target.php',
		data: 'proceed_page=proceed&target_list='+target+'&host_list='+host,

		success: function(html)
		{
			$('#response').html(html);
		}
	});
}

function validate_snmp_settings_form()
{
	var dest_ip   = document.snmp_settings.dest_ip.value;
	var community = document.snmp_settings.community.value;

	if (dest_ip == '' || community == '')
	{
		//alert('All fields are mandatory!');
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:17%; padding-top: 4%; font-family: status-bar;">All fields are mandatory</div>', 'Alert Dialog');
		return false;
	}

	else
	{
		error = check_ip(dest_ip);

		if (error != '')
		{
			alert(error);
			return false;
		}
	}

	document.getElementById('wait').style.display = 'block';

	$.ajax(
	{
		type: 'POST',
		url: 'do_snmp_settings.py',
		data: 'proceed_page=proceed&ip_list='+document.snmp_settings.ip_list.value+'&dest_ip='+dest_ip+'&community='+community,

		success: function(html)
		{
			$('#response').html(html);
		}
	});

	document.snmp_settings.action_but.disabled = true;
}

function disp_smb_params()
{
	var opt_clicked = document.smb_settings.use_smb.checked;
	var smb_table = document.getElementById('smb_table');

	if (opt_clicked == true)
	{
		smb_table.style.display = 'block';
	}

	else
	{
		smb_table.style.display = 'none';
	}
}

function validate_ip(ip)
{
	var error = "";
	var choose_privs = document.smb_settings.choose_privs.value;

	var ipPattern = /^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$|^$/;
	var ip_array = ip.match(ipPattern);
	var smb_opt = document.smb_settings.use_smb.checked;

	wins_ip = document.smb_settings.wins_ip.value;

	if (choose_privs == '')
	{
		//alert('You need to choose a user!');
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:-4%; padding-top: 4%; font-family: status-bar;">You need to choose a user</div>', 'Alert Dialog');
		return false;
	}

	if (wins_ip == null || wins_ip == '')
	{
		wins_ip = document.smb_settings.adsserver.value;
	}

	if (smb_opt == true)
	{
		if (ip == "0.0.0.0")
		{
			error = ip+' is not a valid IP';
		}
	
		else if (ip == "255.255.255.255")
		{
			error = ip+' is not a valid IP';
		}

		if (ip_array == null)
		{
			error = ip+' is not a valid IP';
		}

		else if (ip_array != null)
		{
			for (i = 1; i <= 4; i++)
			{
				thisSegment = ip_array[i];

				if (thisSegment > 255)
				{
					error = ip+' is not a valid IP';
					i = 4;
				}
	
				if ((i == 0) && (thisSegment > 255))
				{
					error = ip+' is not a valid IP';
					i = 4;
				}
			}
		}

		if (error != '')
		{
			alert(error);
			return false;
		}
	}

	document.getElementById('smb_global').style.display = 'block';

	$.ajax(
	{
		type: 'POST',
		url: 'smb_setup.py',
		data: 'hid_proceed=proceed&use_smb='+smb_opt+'&wins_ip='+wins_ip+'&choose_privs='+choose_privs+'&simple='+document.smb_settings.simple.checked+'&store_dos='+document.smb_settings.store_dos.checked+'&preserve_hid='+document.smb_settings.preserve_hid.checked+'&preserve_system='+document.smb_settings.preserve_system.checked+'&hidden_spl='+document.smb_settings.hidden_spl.checked+'&synch_uid='+document.smb_settings.synch_uid.checked,

		success: function(html)
		{
			$('#id_smb_global').html(html);
		}
	});

	document.smb_settings.action_but.disabled = true;
}

function validate_local_auth()
{
	//var confirm_local = confirm("All shares will be deleted! Do you still want to continue?");

	if (confirm_local == true)
	{
		document.getElementById('wait').style.display = 'block';
		//alert("Reboot the system after Local Server is connected!");
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 19%; padding-top: 4%; font-family: status-bar;">Reboot the system after Local Server is connected</div>', 'Authentication Alert');
		$.ajax(
		{
			type: 'POST',
			url: 'nis_auth.py',
			data: 'local_action_but=proceed',

			success: function(html)
			{
				$('#response').html(html);
			}
		});
	}
	else
	{
		return false;
	}
}

function choose_option(value)
{
	var options        = document.getElementsByName('auth_type')
	var nis_table      = document.getElementById('nis_auth_table')
	var ads_table      = document.getElementById('ads_auth_table')
	var local_table      = document.getElementById('local_auth_table')
	var ldap_table      = document.getElementById('ldap_auth_table')
	
	if(value=='nis'){
		nis_table.style.display = 'block';
		ads_table.style.display = 'none';
		local_table.style.display = 'none';
		ldap_table.style.display = 'none';
	}
	if(value=='adc'){
		nis_table.style.display = 'none';
		ads_table.style.display = 'block';
		local_table.style.display = 'none';
		ldap_table.style.display = 'none';
	}
	if(value=='local'){
		local_table.style.display = 'block';
		nis_table.style.display = 'none';
		ads_table.style.display = 'none';
		ldap_table.style.display = 'none';
	}
	if(value=='ldap'){
		local_table.style.display = 'none';
		nis_table.style.display = 'none';
		ads_table.style.display = 'none';
		ldap_table.style.display = 'block';
	}
}
/*
function choose_option()
{
	var options        = document.getElementsByName('auth_type');
	var button         = document.getElementById('local_action_but');
	var nis_table      = document.getElementById('nis_auth_table');
	var ads_table      = document.getElementById('ads_auth_table');
	var nis_ads_id     = document.getElementById('id_nis_ads');
	var ads_connection = document.setup_auth.hid_ads_connection.value;
	var nis_connection = document.setup_auth.hid_nis_connection.value;
	var users_present  = document.setup_auth.hid_users_present.value;
	alert(options);

	for (var i = 0;  i < options.length;  i++)
	{
		if (options[i].checked)
		{
			if (options[i].value == 'ADS/DC')
			{
				if (ads_connection != 'Join is OK' && nis_connection != 'nis is running')
				{
					if (users_present == 'yes')
					{
						var ans = confirm('All the local users/groups will be deleted! Proceed with ADS?');
						if (ans == true)
						{
							nis_table.style.display     = 'none';
							ads_table.style.display     = 'block';
							nis_ads_id.style.visibility = 'visible';
							button.style.visibility     = 'hidden';
							document.setup_auth.username.focus();
						}

						else
						{
							return false;
						}
					}

					else
					{
						nis_table.style.display     = 'none';
						ads_table.style.display     = 'block';
						nis_ads_id.style.visibility = 'visible';
						button.style.visibility     = 'hidden';
						document.setup_auth.username.focus();
					}
				}

				else
				{
					nis_table.style.display     = 'none';
					ads_table.style.display     = 'block';
					nis_ads_id.style.visibility = 'visible';
					button.style.visibility     = 'hidden';
					document.setup_auth.username.focus();
				}
			}

			else if (options[i].value == 'NIS')
			{
				if (ads_connection != 'Join is OK' && nis_connection != 'nis is running')
				{
					if (users_present == 'yes')
					{
						var ans = confirm('All the local users/groups will be deleted! Proceed with NIS?');
						if (ans == true)
						{
							ads_table.style.display   = 'none';
							nis_table.style.display   = 'block';
							nis_ads_id.style.visibility = 'visible';
							button.style.visibility   = 'hidden';
							document.setup_auth.ip_add.focus();
						}

						else
						{
							return false;
						}
					}

					else
					{
						ads_table.style.display   = 'none';
						nis_table.style.display   = 'block';
						nis_ads_id.style.visibility = 'visible';
						button.style.visibility   = 'hidden';
						document.setup_auth.ip_add.focus();
					}
				}

				else
				{
					ads_table.style.display   = 'none';
					nis_table.style.display   = 'block';
					nis_ads_id.style.visibility = 'visible';
					button.style.visibility   = 'hidden';
					document.setup_auth.ip_add.focus();
				}
			}

			else
			{
				if (ads_connection == 'Join is OK' || nis_connection == 'nis is running')
				{
					alert('Please reboot the system in order to work with Local connection!');
					ads_table.style.display   = 'none';
					nis_table.style.display   = 'none';
					button.style.visibility   = 'visible';
					nis_ads_id.style.visibility = 'hidden';
					nis_table.style.display   = 'none';
					ads_table.style.display   = 'none';
				}

				else
				{
					ads_table.style.display   = 'none';
					nis_table.style.display   = 'none';
					button.style.visibility   = 'visible';
					nis_ads_id.style.visibility = 'hidden';
					nis_table.style.display   = 'none';
					ads_table.style.display   = 'none';
				}
			}
		}
	}
}
*/
function show_users_groups()
{
	var local_users  = document.getElementById('id_local_users');
	var local_groups = document.getElementById('id_local_groups');

	if (show_users == true)
	{
		local_users.style.visibility  = 'visible';
		local_groups.style.visibility = 'visible';
	}

	else
	{
		local_users.style.visibility  = 'hidden';
		local_groups.style.visibility = 'hidden';
	}
}

function validate_nis_form(number)
{
	var ip_add = document.setup_auth.ip_add.value;
	var domain = document.setup_auth.domain.value;

	if (ip_add == '' || domain == '')
	{
		alert('All fields are mandatory');
		return false;
	}

	else
	{
		var ip = document.setup_auth.ip_add.value;
		var ip_error = '';

		var ipPattern;
	
		ipPattern = /^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/;

		var ip_array = ip.match(ipPattern);

		if (ip == "0.0.0.0")
		{
			ip_error = ip+' is not a valid IP';
		}
	
		else if (ip == "255.255.255.255")
		{
			ip_error = ip+' is not a valid IP';
		}

		else if (ip == "")
		{
			ip_error = 'IP is required! Sorry!!';
		}
		
		if (ip_array == null)
		{
			ip_error = ip+' is not a valid IP';
		}

		else if (ip_array != null)
		{
			for (i = 1; i <= 4; i++)
			{
				thisSegment = ip_array[i];

				if (thisSegment > 255)
				{
					ip_error = ip+' is not a valid IP';
					i = 4;
				}
			
				if ((i == 0) && (thisSegment > 255))
				{
					ip_error = ip+' is not a valid IP';
					i = 4;
				}
			}
		}

		if (ip_error != '')
		{
			alert(ip_error);
			return false;
		}
	}
	
	choice = true;

	if (parseInt(number) > 0)
	{
		//var choice = confirm("All shares, users & groups will be deleted! Do you still want to continue?");
	}

	if(choice == true)
	{
		document.getElementById('wait').style.display = 'block';
		$.ajax(
		{
			type: 'POST',
			url: 'nis_auth.php',
			data: 'proceed_page=proceed&ip_add='+ip_add+'&domain='+domain+'&hid_nis='+document.setup_auth.hid_nis.value,
			success: function(html)
			{
				$('#response').html(html);
			}
		});
	}
	else
	{
		return false;
	}

	document.setup_auth.nis_action_but.disabled = true;
}

function validate_new_nis_form(number)
{
	var ip_add = document.setup_auth.ip_add.value;
	var domain = document.setup_auth.domain.value;

	if (ip_add == '' || domain == '')
	{
		alert('All fields are mandatory');
		return false;
	}

	else
	{
		var ip = document.setup_auth.ip_add.value;
		var ip_error = '';

		var ipPattern;
	
		ipPattern = /^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/;

		var ip_array = ip.match(ipPattern);

		if (ip == "0.0.0.0")
		{
			ip_error = ip+' is not a valid IP';
		}
	
		else if (ip == "255.255.255.255")
		{
			ip_error = ip+' is not a valid IP';
		}

		else if (ip == "")
		{
			ip_error = 'IP is required! Sorry!!';
		}
		
		if (ip_array == null)
		{
			ip_error = ip+' is not a valid IP';
		}

		else if (ip_array != null)
		{
			for (i = 1; i <= 4; i++)
			{
				thisSegment = ip_array[i];

				if (thisSegment > 255)
				{
					ip_error = ip+' is not a valid IP';
					i = 4;
				}
			
				if ((i == 0) && (thisSegment > 255))
				{
					ip_error = ip+' is not a valid IP';
					i = 4;
				}
			}
		}

		if (ip_error != '')
		{
			alert(ip_error);
			return false;
		}
	}

	choice = true;

	/*if (parseInt(number) > 0)
	{
		var choice = confirm("You need to re-configure shares and local users will be removed... Do you wish to continue?");
	}*/

        if(choice == true)
	{
		document.getElementById('wait').style.display = 'block';
		$.ajax(
        	{
                	type: 'POST',
                	url: 'nis_auth.py',
                	data: 'nis_action_but=proceed&ip_add='+ip_add+'&domain='+domain+'&hid_nis='+document.setup_auth.hid_nis.value,
                	success: function(html)
                	{
                        	$('#response').html(html);
                	}
        	});
	}
	else
	{
		return false;
	}

	document.setup_auth.nis_action_but.disabled = true;
}

function validate_ads_form(number)
{
        var username = document.setup_auth.username.value;
        var password = document.setup_auth.password.value;
        var fqdn     = document.setup_auth.fqn.value;
        var action   = document.setup_auth.ads_action_but.value;
        var dns = document.setup_auth.dns.value;

        if (username == '')
        {
                alert('Please enter username!');
                document.getElementById('username').focus();
                return false;
        }

        if (password == '')
        {
                alert('Please enter Password');
                document.getElementById('password').focus();
                return false;
        }

        if (fqdn == '')
        {
                alert('Please enter FQDN');
                document.getElementById('fqn').focus();
                return false;
        }

        if (dns == '')
        {
                alert('Please enter DNS');
                document.getElementById('dns').focus();
                return false;
        }

        else
        {
		var dns_error = '';

		var ipPattern;
	
		ipPattern = /^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/;

		var dns_array = dns.match(ipPattern);

		if (dns == "0.0.0.0")
		{
			dns_error = dns+' is not a valid IP';
		}
	
		else if (dns == "255.255.255.255")
		{
			dns_error = dns+' is not a valid IP';
		}

		else if (dns == "")
		{
			dns_error = 'IP is required! Sorry!!';
		}
		
		if (dns_array == null)
		{
			dns_error = dns+' is not a valid IP';
		}

		else if (dns_array != null)
		{
			for (i = 1; i <= 4; i++)
			{
				thisSegment = dns_array[i];

				if (thisSegment > 255)
				{
					dns_error = dns+' is not a valid IP';
					i = 4;
				}
			
				if ((i == 0) && (thisSegment > 255))
				{
					dns_error = dns+' is not a valid IP';
					i = 4;
				}
			}
		}

		if (dns_error != '')
                {
                        alert(dns_error+'. Please enter a valid IP!');
                        document.getElementById('dns').focus();
                        return false;
                }
        }

	choice = true;

	/*if (parseInt(number) > 0)
	{
		var choice = confirm("All local users will be deleted and shares will be unconfigured if there are any... Do you wish to continue?");
	}*/

	if(choice == true)
	{
        	document.getElementById('wait').style.display = 'block';
        	$.ajax(
        	{
                	type: 'POST',
               		url: 'nis_auth.py',
                	data: 'ads_action_but=proceed&username='+username+'&password='+password+'&fqdn='+fqdn+'&dns='+dns,

                	success: function(html)
                	{
                        	$('#response').html(html);
                	}
        	});
	}
	else
	{
		return false;
	}
}

function show_infini_params()
{
	var inf_clicked = document.infiniband.enable_infiniband.checked;
	var inf_table   = document.getElementById('id_infini');
	var hid_page    = document.infiniband.hid_page.value;

	if (inf_clicked == true)
	{
		document.getElementById('wait').style.display = 'block';

		$.ajax(
		{
			type: 'POST',
			url: 'infiniband_only.php',
			data: 'infini_only=infiniband_only&inf='+inf_clicked+'&p='+hid_page,

			success: function(html)
			{
				$('#response').html(html);
			}
		});
	}

	else
	{
		document.getElementById('wait').style.display = 'block';

		$.ajax(
		{
			type: 'POST',
			url: 'infiniband_only.php',
			data: 'infini_only=infiniband_only&inf='+inf_clicked+'&p='+hid_page,

			success: function(html)
			{
				$('#response').html(html);
			}
		});
	}
}

function show_ib_chassis()
{
	var ib_option = document.infiniband.ib_chassis.checked;
	var hid_page  = document.infiniband.hid_page.value;

	document.getElementById('wait').style.display = 'block';

	$.ajax(
	{
		type: 'POST',
		url: 'ib_only.php',
		data: 'ib_only_word=infiniband_only&ib='+ib_option+'&p='+hid_page,

		success: function(html)
		{
			$('#response').html(html);
		}
	});
}

function ip_over_infiniband()
{
	var ip_option = document.infiniband.ip_over.checked;
	var hid_page  = document.infiniband.hid_page.value;

	document.getElementById('wait').style.display = 'block';

	$.ajax(
	{
		type: 'POST',
		url: 'ip_over_infiniband.php',
		data: 'ip_over_inf=infiniband_only&ip='+ip_option+'&p='+hid_page,

		success: function(html)
		{
			$('#response').html(html);
		}
	});
}

function run_nfs_over_rdma(nfs_rdma)
{
	document.getElementById('wait').style.display = 'block';

	$.ajax(
	{
		type: 'POST',
		url: 'run_nfs_rdma.php',
		data: 'opt='+nfs_rdma,

		success: function(html)
		{
			$('#response').html(html);
		}
	});
}

function choose_mode()
{
	var options_array = document.getElementsByName('target_mode');

	for (i = 0;  i < options_array.length;  i++)
	{
		if (options_array[i].checked)
		{
			document.target_type.action = 'setup_fc.php?type='+options_array[i].value+'&stat=yes';
			document.target_type.submit();
		}
	}
}

function run_fc()
{
	var fc_option = document.enable_fc.fc_option.checked;
			
	document.getElementById('wait').style.display = 'block';

	$.ajax(
	{
		type: 'POST',
		url: 'enable_fc.php',
		data: 'proceed_page=proceed&fc_option='+fc_option,

		success: function(html)
		{
			$('#response').html(html);
		}
	});
}

function disable_page(user)
{
	if (user != 'Full Access')
	{
		var form_count = document.forms.length;

		for (i = 0;  i < form_count;  i++)
		{
			var elem_count = document.forms[i].elements.length;

			for (j = 0;  j < elem_count;  j++)
			{
				document.forms[i].elements[j].disabled = true;
			}
		}
	}

	document.getElementById('id_create_share').setAttribute("autocomplete","off");
}

function run_get_fc_luns()
{
	var zone_for_disk = document.add_disk_to_zone.zone_list.value;

	document.getElementById('id_get_fc_luns').style.display = 'table';

	$.ajax(
	{
		type: 'POST',
		url: 'find_lun_for_zone.php',
		data: 'target='+zone_for_disk,

		success: function(html)
		{
			$('#id_get_fc_luns').html(html);
		}
	});
}

function validate_add_disk(zone, disk)
{
	if (zone == '' || disk == '')
	{
		alert('This operation requires both zone name and disk name!');
		return false;
	}

	document.getElementById('fc_add_disk').style.display = 'block';

	$.ajax(
	{
		type: 'POST',
		url: 'add_disk_to_zone.php',
		data: 'proceed_page=proceed&zone_list='+zone+'&disks_list='+disk+'&lun_num_list='+document.add_disk_to_zone.lun_num_list.value,

		success: function(html)
		{
			$('#id_fc_add_disk').html(html);
		}
	});
}

function validate_zone_form()
{
	var zone = document.fc_settings.fc_zone.value;
	var zone_format = 'FC'

	if (zone == '')
	{
		alert('Enter a name for zone!');
		return false;
	}

	else
	{
		var zone_array = zone.split(':');

		if (zone_array[0] != zone_format)
		{
			alert('Zone name should start with \''+zone_format+':\'');
			return false;
		}
	}

	document.getElementById('mfc_add_disk').style.display = 'block';

	$.ajax(
	{
		type: 'POST',
		url: 'fc_settings_action.php',
		data: 'proceed_page=proceed&fc_zone='+zone,

		success: function(html)
		{
			$('#id_mfc_add_disk').html(html);
		}
	});
}

function validate_initr_form()
{
	var zone = document.add_initr_to_zone.zone_list.value; 
	var initiator   = document.add_initr_to_zone.initr.value;
	var valid_chars = "abcdefABCDEF0123456789:";

	if (initiator == '' || zone == '')
	{
		alert('Enter a valid value for both zone and initiator!');
		return false;
	}

	else
	{
		for (var i = 0;  i < initiator.length;  i++)
		{
			if (valid_chars.indexOf(initiator.charAt(i)) == -1)
			{
				alert('Please enter a valid initiator name! Only numbers [0-9] and hexadecimal characters [a-f] allowed');
				return false;
                        }
                }
	}

	document.getElementById('fc_add_init').style.display = 'block';

	$.ajax(
	{
		type: 'POST',
		url: 'add_initr_to_zone.php',
		data: 'proceed_page=proceed&zone_list='+zone+'&initr='+initiator,

		success: function(html)
		{
			$('#id_fc_add_init').html(html);
		}
	});
}

function run_get_fc_disks()
{
	var zone_val = document.del_disk_from_zone.zone_list.value;

	document.getElementById('id_get_added_disks').style.display = 'table';

	$.ajax(
	{
		type: 'POST',
		url: 'find_disk_for_zone.php',
		data: 'z='+zone_val,

		success: function(html)
		{
			$('#id_get_added_disks').html(html);
		}
	});
}

function run_get_initiators()
{
	var zone_val = document.del_init_from_zone.zone_list.value;

	if (zone_val != '')
	{
		document.getElementById('id_get_init').style.display = 'block';

		$.ajax(
		{
			type: 'POST',
			url: 'find_init_for_zone.php',
			data: 'z='+zone_val+'&type=manual',

			success: function(html)
			{
				$('#get_init').html(html);
			}
		});
	}
}

function validate_add_disk(zone, disk)
{
	if (zone == '' || disk == '')
	{
		alert('This operation requires both zone name and disk name!');
		return false;
	}

	document.getElementById('fc_add_disk').style.display = 'block';

	$.ajax(
	{
		type: 'POST',
		url: 'add_disk_to_zone.php',
		data: 'proceed_page=proceed&zone_list='+zone+'&disks_list='+disk+'&lun_num_list='+document.add_disk_to_zone.lun_num_list.value,

		success: function(html)
		{
			$('#id_fc_add_disk').html(html);
		}
	});

}

function validate_del_zone(zone, active_session_string)
{
        if (active_session_string != '')
        {
        	search_active_session = active_session_string.indexOf(zone);

                tgt_init_array = new Array();

                tgt_init_array = active_session_string.split('->');

                initiator = tgt_init_array[1];
                initiator = initiator.replace(' ', ', ');
	}

	if (search_active_session >= 0)
        {
        	var response = confirm('\''+zone+'\' is in use under the initiator name \''+initiator+'\'. Do you still want to delete the zone?');

                if (response == true)
                {
			document.getElementById('fc_del_zone').style.display = 'block';

			$.ajax(
			{
				type: 'POST',
				url: 'delete_zone.php',
				data: 'proceed_page=proceed&zone_list='+zone,

				success: function(html)
				{
					$('#id_fc_del_zone').html(html);
				}
			});
		}

		else
		{
			return false;
		}
	}

	else
	{
		document.getElementById('fc_del_zone').style.display = 'block';

		$.ajax(
                {
	        	type: 'POST',
               	        url: 'delete_zone.php',
                       	data: 'proceed_page=proceed&zone_list='+zone,

                        success: function(html)
       	                {
       		              	$('#id_fc_del_zone').html(html);
                       	}
                });
	}
}

function run_get_srp_luns()
{
	var group_for_disk = document.add_disk_to_group.group_list.value;
	
	document.getElementById('id_get_srp_luns').style.display = 'table';

	$.ajax(
	{
		type: 'POST',
		url: 'find_lun_for_group.php',
		data: 'target='+group_for_disk,

		success: function(html)
		{
			$('#id_get_srp_luns').html(html);
		}
	});
}

function run_get_srp_disks()
{
	var group_val = document.del_disk_from_group.group_list.value;

	document.getElementById('id_get_srp_disks').style.display = 'table';

	$.ajax(
	{
		type: 'POST',
		url: 'find_disk_for_group.php',
		data: 'g='+group_val,

		success: function(html)
		{
			$('#id_get_srp_disks').html(html);
		}
	});
}
			
function validate_srp_groups(group, disk)
{
	if (group == '' || disk == '')
	{
		alert('This operation requires both group name and disk name');
		return false;
	}

	document.getElementById('srp_add_disk').style.display = 'block';

	$.ajax(
	{
		type: 'POST',
		url: 'add_disk_to_group.php',
		data: 'proceed_page=proceed&group_list='+group+'&disks_list='+disk+'&lun_num_list='+document.add_disk_to_group.lun_num_list.value,

		success: function(html)
		{
			$('#id_srp_add_disk').html(html);
		}
	});
}

function validate_del_srp_disk(group, disk, active_session_string)
{
	delete_all = 'Remove selected disk';

	if (group == '' || disk == '')
	{
		alert('This operation requires both group name and disk name!');
		return false;
	}

        if (active_session_string != '')
        {
        	search_active_session = active_session_string.indexOf(group);

                tgt_init_array = new Array();

                tgt_init_array = active_session_string.split('->');

                initiator = tgt_init_array[1];
                initiator = initiator.replace(' ', ', ');
	}

        if (search_active_session >= 0)
        {
	        var response = confirm('\''+disk+'\' is in use under the initiator name \''+initiator+'\'. Do you still want to delete the disk?');

        	if (response == true)
                {
                	document.getElementById('srp_del_disk').style.display = 'block';

                        $.ajax(
                        {
	                        type: 'POST',
                                url: 'del_disk_from_group.php',
                                data: 'group_list='+group+'&proceed_page=proceed&disks_list='+disk+'&del_from_group='+delete_all,
                                success: function(html)
                                {
          	                	$('#id_srp_del_disk').html(html);
                                }
                        });
		}

                else
                {
                	return false;
                }
	}

	else
	{
		document.getElementById('srp_del_disk').style.display = 'block';

		$.ajax(
		{
			type: 'POST',
			url: 'del_disk_from_group.php',
			data: 'proceed_page=proceed&group_list='+group+'&disks_list='+disk+'&del_from_group='+delete_all,

			success: function(html)
			{
				$('#id_srp_del_disk').html(html);
			}
		});
	}
}

function show_srp_params()
{
	var srp_clicked = document.srp_form.enable_srp.checked;
	var hid_page  = document.srp_form.hid_page.value;

	document.getElementById('wait').style.display = 'block';

	$.ajax(
	{
		type: 'POST',
		url: 'srp_only.php',
		data: 'srp='+srp_clicked+'&p='+hid_page,

		success: function(html)
		{
			$('#response').html(html);
		}
	});
}

function do_schedule_shutdown()
{
	var week_array = document.getElementsByName('week');

	var hour  = document.sched_shutdown.hours.value;
	var mins  = document.sched_shutdown.mins.value;
	var days  = document.sched_shutdown.day.value;
	var month = document.sched_shutdown.month.value;

	for (i = 0;  i < week_array.length;  i++)
	{
		if (week_array[i].checked)
		{
			week_val = week_array[i].value;
		}
	}

	if (week_val == '*' && hour == '*' && days == '*' && month == '*')
	{
		if (mins < 40 || mins == '*')
		{
			alert('Can\'t be scheduled for less than 40 minutes!');
			return false;
		}
	}

	document.getElementById('wait').style.display = 'block';

	$.ajax(
	{
		type: 'POST',
		url: 'schedule_shutdown.py',
		data: 'hours='+hour+'&mins='+mins+'&day='+days+'&month='+month+'&week='+week_val+'&proceed_page=proceed',

		success: function(html)
		{
			$('#response').html(html);
		}
	});

	return false;
}

function do_schedule_restart()
{
	var r_week_array = document.getElementsByName('r_week');

	var r_hour  = document.sched_restart.hours.value;
	var r_mins  = document.sched_restart.mins.value;
	var r_days  = document.sched_restart.day.value;
	var r_month = document.sched_restart.month.value;

	r_week_val = '*';

	for (i = 0;  i < r_week_array.length;  i++)
	{
		if (r_week_array[i].checked)
		{
			r_week_val = r_week_array[i].value;
		}
	}

	if (r_week_val == '*' && r_hour == '*' && r_days == '*' && r_month == '*')
	{
		if (r_mins < 40 || r_mins == '*')
		{
			alert('Can\'t be scheduled for less than 40 minutes!');
			return false;
		}
	}

	document.getElementById('wait').style.display = 'block';

	$.ajax(
	{
		type: 'POST',
		url: 'schedule_restart.py',
		data: 'hours='+r_hour+'&mins='+r_mins+'&day='+r_days+'&month='+r_month+'&r_week='+r_week_val+'&proceed_page=proceed',

		success: function(html)
		{
			$('#response').html(html);
		}
	});
}

function confirm_shutdown(action)
{
	var response = confirm('Are you sure you want to ' + action + ' ?');

	if (response == true && action == 'shutdown')
	{
		document.shutdown.action = 'shutdown_action.py';
		document.shutdown.submit();
	}
	
	else if (response == true && action == 'restart')
	{
		document.shutdown.action = 'restart.py';
		document.shutdown.submit();
	}

	else if (response == false)
	{
		return false;
	}
}

function disable_day(day_id, week_array, week, checkbox_id)
{
	if (week == '*')
	{
		day_id.disabled = false;
		checkbox_id.disabled = false;
	}

	for (i = 0;  i < week_array.length;  i++)
	{
		if (week_array[i].checked && week != '*')
		{
			day_id.disabled = true;
			checkbox_id.disabled = true;
		}
	}
}

function disable_week(day_id, week_array)
{
	if (day_id.value != '*')
	{
		for (i = 0;  i < week_array.length;  i++)
		{
			week_array[i].disabled = true;
		}
	}

	else
	{
		for (i = 0;  i < week_array.length;  i++)
		{
			week_array[i].disabled = false;
		}
	}
}

function confirm_clear(action)
{
	if (action == 'Clear Logs')
	{
		var response = confirm('You are going to clear all logs! Are you sure?');

		if (response == true)
		{
			document.getElementById('wait').style.display = 'block';
			location.href = 'show_downloads.py?proceed_page=proceed&action_but1=' + action;

			/*$.ajax(
			{
				type: 'POST',
				url: 'show_downloads.py',
				data: 'proceed_page=proceed&action_but1='+action,
	
				success: function(html)
				{
					$('#response').html(html);
				}
			});*/
		}

		else
		{
			return false;
		}
	}

	else
	{
		document.getElementById('wait').style.display = 'block';
		location.href = 'show_downloads.py?proceed_page=proceed&action_but1=' + action;

		/*$.ajax(
		{
			type: 'POST',
			url: 'show_downloads.py',
			data: 'proceed_page=proceed&action_but1='+action,
	
			success: function(html)
			{
				$('#response').html(html);
			}
		});*/
	}
}

function submit_fs2backup_form()
{
        document.getElementById('wait').style.display = 'block';

	$.ajax(
	{
		type: 'POST',
		url: 'show_fs2_backups.py',
		data: 'p=p',

		success: function(html)
		{
			$('#response').html(html);
		}
	});
}

function run_take_backup()
{
	document.fs2_backup.action = 'show_fs2_backups.py';
	document.fs2_backup.submit();
}

function validate_file(file)
{
	if (file == '')
	{
		alert('You need to choose a file for upload!');
		return false;
	}

	document.upload_file.submit();
}

function restart_services(service)
{
	if (service == 'smb')
	{
		smb = 'on';
		ftp = '';
		srp = '';
	}

	else if (service == 'ftp')
	{
		ftp = 'on';
		smb = '';
		srp = '';
	}

	else if (service == 'srp')
	{
		srp = 'on';
		smb = '';
		ftp = '';
	}

	document.getElementById('wait').style.display = 'block';

	$.ajax(
	{
		type: 'POST',
		url: 'connections_reset.py',
		data: 'ser='+service, 

		success: function(html)
		{
			$('#response').html(html);
		}
	});
}

function show_button()
{
	var ftp_option = document.connections_reset.ftp.checked;
	var smb_option = document.connections_reset.smb.checked;
	var srp_option = document.connections_reset.srp.checked;

	if (ftp_option == true || smb_option == true || srp_option == true)
	{
		document.connections_reset.action_but.disabled = false;
	}

	else
	{
		document.connections_reset.action_but.disabled = true;
	}
}

function show_share_params(type, value)
{
	if (value == '')
	{
		return false;
	}

	else
	{
		document.show_smb_params.action = 'get_smb_details.py?type='+type+'&val='+value;
		document.show_smb_params.submit();
	}
}

function show_machine_status(type, machine_file)
{
	document.active_file_transfer.action = 'get_machine_file_status.py?type='+type+'&mf='+machine_file;
	document.active_file_transfer.submit();
}

function enable_smb(snapshot)
{
	disable_all_other_forms('delete_snapshot');

	document.getElementById('wait').style.display = 'block';
	var smb_check_id = document.getElementById('id_smb_check');

	var snap_id = 'id_'+snapshot;
	var snapshot_checked = document.getElementById(snap_id).checked;

	if (snapshot_checked == true)
	{
		$.ajax(
		{
			type: 'POST',
			url: 'smb_snapshot.php',
			data: 's='+snapshot+'&smb=on',
			success: function(html)
			{
				$('#response').html(html);
			}
		});
	}

	else
	{
		$.ajax(
		{
			type: 'POST',
			url: 'smb_snapshot.php',
			data: 's='+snapshot+'&smb=off',
			success: function(html)
			{
				$('#smb_response').html(html);
			}
		});
	}
}

function show_iscsi_snapshot_params()
{
	var snapshot_option = document.iscsi_snapshot_form.iscsi_snapshot.checked;
	var snapshot_table  = document.getElementById('id_iscsi_snapshot');

	if (snapshot_option == true)
	{
		snapshot_table.style.display = 'block';
	}

	else
	{
		snapshot_table.style.display = 'none';
	}
}

function get_iscsi_vg_from_disk()
{	
	var snap_shot = document.iscsi_snapshot_form.iscsi_snapshot.checked;
	var disk_name = document.iscsi_snapshot_form.iscsi_disks.value;
	
	if (disk_name == '')
	{
		alert('Choose a valid disk');
		return false;
	}

	else
	{
		document.iscsi_snapshot_form.action = 'show_iscsi_volume.php?ss='+snap_shot+'&dn='+disk_name;
		document.iscsi_snapshot_form.submit();
	}
}

function run_get_snapshot_luns()
{
	var target_for_disk = document.add_disk_to_target.target_for_disk.value;
	var iscsi_snap_string = document.add_disk_to_target.hid_iscsi_snap_string.value;

	if (target_for_disk != '')
	{
		document.getElementById('wait').style.display = 'block';

		$.ajax(
		{
			type: 'POST',
			url: 'snapshot_lun_for_target.php',
			data: 'target='+target_for_disk+'&iscsi_string='+iscsi_snap_string,

			success: function(html)
			{
				$('#response').html(html);
			}
		});
	}
}

function validate_iscsi_form()
{
	var user_size = document.iscsi_snapshot_form.size.value;
	var max_size  = document.iscsi_snapshot_form.hid_size.value;
	var disk_name = document.iscsi_snapshot_form.iscsi_disks.value;
	var min_size  = document.iscsi_snapshot_form.min_lv_size.value;
	var free_size = document.iscsi_snapshot_form.free_size.value;
	
	var size_pattern = /^(\d{1,4})\.(\d{1,4})$|^(\d{1,4})$/;
	var size_array   = user_size.match(size_pattern);

	if (size_array == null)
	{
		alert('Please enter a valid size!');
		return false;
	}

	if (disk_name == '')
	{
		alert('Please choose a disk');
		return false;
	}

	if (user_size == '')
	{
		alert('Please enter a valid size!');
		return false;
	}

	if (parseFloat(user_size) > parseFloat(max_size))
	{
		alert('Size exceeded max limit. Please enter a valid size');
		document.iscsi_snapshot_form.size.value = '';
		document.iscsi_snapshot_form.size.focus();
		return false;
	}

	if (parseFloat(user_size) > parseFloat(free_size))
	{
		alert('Snapshot exceeded the volume free space!');
		document.iscsi_snapshot_form.size.value = '';
		document.iscsi_snapshot_form.size.focus();
		return false;
	}

	else
	{
		if (parseFloat(user_size) < parseFloat(min_size) && (parseFloat(user_size) < parseFloat(max_size) || parseFloat(user_size < parseFloat(free_size))))
		{
			var response = confirm('Minimum size recommended for snapshot: '+min_size+' GB! To re-enter size, click on \'Cancel\'. To proceed with given size, click on \'OK\'.');
			if (response == true)
			{
				document.getElementById('wait').style.display = 'block';

				$.ajax(
				{
					type: 'POST',
					url: 'create_iscsi_snapshot.php',
					data: 'proceed_page=proceed&iscsi_snapshot='+document.iscsi_snapshot_form.iscsi_snapshot.checked+'&iscsi_disks='+disk_name+'&size='+user_size,
					success: function(html)
					{
						$('#response').html(html);
					}
				});
			}

			else
			{
				return false;
			}
		}

		else
		{
			document.getElementById('wait').style.display = 'block';

			$.ajax(
			{
				type: 'POST',
				url: 'create_iscsi_snapshot.php',
				data: 'proceed_page=proceed&iscsi_snapshot='+document.iscsi_snapshot_form.iscsi_snapshot.checked+'&iscsi_disks='+disk_name+'&size='+user_size,
				success: function(html)
				{
					$('#response').html(html);
				}
			});
		}
	}
}

function run_get_snapshot_disks()
{
	var target_val = document.del_disk_from_target.target_list.value;

	document.del_disk_from_target.action = 'find_snapshot_for_target.php?t='+target_val;
	document.del_disk_from_target.submit();
}

function enable_nfs(snapshot)
{
	disable_all_other_forms('delete_snapshot');

	var nfs_check_id = document.getElementById('id_nfs_check');
	var nfs_id = 'nfsid_'+snapshot;
	var nfs_checked = document.getElementById(nfs_id).checked;
	
	if (nfs_checked == true)
	{
		window.showModalDialog("set_nfs_allow_ip.php?snpsht="+snapshot, "Allow IP", "dialogWidth: 350px; dialogHeight: 150px; border: 1px solid;");
	}

	else
	{
		document.getElementById('wait').style.display = 'block';

		$.ajax(
		{
			type: 'POST',
			url: 'snapshot_access.php',
			data: 'snpsht='+snapshot+'&nfs_snap=off',

			success: function(html)
			{
				$('#response').html(html);
			}
		});
	}
}

function show_snapshot_params()
{
	var snapshot_option = document.snapshot_form.snapshot.checked;
	var snapshot_table  = document.getElementById('id_snapshot');

	if (snapshot_option == true)
	{
		snapshot_table.style.display = 'block';
	}

	else
	{
		snapshot_table.style.display = 'none';
	}
}

function get_vg_from_disk()
{	
	var snap_shot = document.snapshot_form.snapshot.checked;
	var disk_name = document.snapshot_form.disks.value;
	
	if (disk_name == '')
	{
		//alert('Choose a valid disk');
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 19%; padding-top: 4%; font-family: status-bar;">Choose a valid disk</div>', 'Vg Alert');
		return false;
	}

	else
	{
		document.getElementById('wait').style.display = 'block';

		$.ajax(
		{
			type: 'POST',
			url: 'show_volume.php',
			data: 'ss='+snap_shot+'&dn='+disk_name,

			success: function(html)
			{
				$('#response').html(html);
			}
		});
	}

	var form_count = document.forms.length;

	for (i = 0;  i < form_count;  i++)
	{
		var elem_count = document.forms[i].elements.length;

		for (j = 0;  j < elem_count;  j++)
		{
			document.forms[i].elements[j].disabled = true;
		}
	}
}

function validate_snapshot_form()
{
	var user_size = document.snapshot_form.size.value;
	var max_size  = document.snapshot_form.hid_size.value;
	var disk_name = document.snapshot_form.disks.value;
	var min_size  = document.snapshot_form.min_lv_size.value;
	var free_size = document.snapshot_form.free_size.value;

	var size_pattern = /^(\d{1,4})\.(\d{1,4})$|^(\d{1,4})$|^\.(\d{1,4})$/;
	var size_array   = user_size.match(size_pattern);

	if (size_array == null)
	{
		alert('Please enter a valid size!');
		return false;
	}

	if (disk_name == '')
	{
		alert('Please choose a disk');
		return false;
	}

	if (user_size == '')
	{
		alert('Please enter a valid size!');
		return false;
	}

	if (parseFloat(user_size) > parseFloat(max_size))
	{
		alert('Size exceeded max limit. Please enter a valid size');
		document.snapshot_form.size.value = '';
		document.snapshot_form.size.focus();
		return false;
	}

	if (parseFloat(user_size) > parseFloat(free_size))
	{
		alert('Snapshot exceeded the volume free space!');
		document.snapshot_form.size.value = '';
		document.snapshot_form.size.focus();
		return false;
	}

	else
	{
		if (parseFloat(user_size) < parseFloat(min_size) && (parseFloat(user_size) < parseFloat(max_size) || parseFloat(user_size < parseFloat(free_size))))
		{
			var resp = confirm('Minimum size recommended for snapshot: '+min_size+' GB! To re-enter size, click on \'Cancel\'. To proceed with given size, click on \'OK\'.');
			if (resp == true)
			{
				document.getElementById('wait').style.display = 'block';

				$.ajax(
				{
					type: 'POST',
					url: 'create_snapshot.php',
					data: 'proceed_page=proceed&snapshot='+document.snapshot_form.snapshot.checked+'&disks='+disk_name+'&size='+user_size,
					success: function(html)
					{
						$('#response').html(html);
					}
				});
			}

			else
			{
				return false;
			}
		}

		else
		{
			document.getElementById('wait').style.display = 'block';

			$.ajax(
			{
				type: 'POST',
				url: 'create_snapshot.php',
				data: 'proceed_page=proceed&snapshot='+document.snapshot_form.snapshot.checked+'&disks='+disk_name+'&size='+user_size,
				success: function(html)
				{
					$('#response').html(html);
				}
			});
		}
	}
}

function validate_snapshot_form2()
{
	var disk_name = document.create_snap_form.disk_name.value;
	var size = document.create_snap_form.size.value;
	if((disk_name == 'sel_disk'))
	{	
		//alert("Please select a Disk!");
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:27%; padding-top: 4%; font-family: status-bar;">Please select a Disk</div>', 'Snapshot Alert');
		//document.create_snap_form.disk_name.focus();
		return false;
	}

	if(size == '')
	{
		//alert("Please enter size!");
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:31%; padding-top: 4%; font-family: status-bar;">Please Enter Size</div>', 'Snapshot Alert');
		//document.create_snap_form.size.focus();
		return false;
	}

	if(isNaN(size) == true)
	{
		//alert("Size should be a numeric value!");
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:31%; padding-top: 4%; font-family: status-bar;">Size should be a numeric value</div>', 'Snapshot Alert');
		document.create_snap_form.size.focus();
		return false;
	}	
}

function nas_select_all()
{
	var check_all_option = document.getElementById('id_select_all');
	var disk_array = document.delete_snapshot.elements["delete_option[]"];

	if (disk_array.length == undefined)
	{
		var delete_id = document.getElementById('id_disk_array');

		if (check_all_option.checked == true)
		{
			if (delete_id.disabled != true)
			{
				delete_id.checked = true;
			}
		}

		else
		{
			delete_id.checked = false;
		}
	}

	if (check_all_option.checked == true)
	{
		for (i = 0;  i < disk_array.length;  i++)
		{
			if (disk_array[i].disabled != true)
			{
				disk_array[i].checked = true;
			}
		}
	}

	else
	{
		for (i = 0;  i < disk_array.length;  i++)
		{
			disk_array[i].checked = false;
		}
	}
}

function iscsi_snap_select_all()
{
	var check_all_option = document.getElementById('id_iscsi_select_all');
	var disk_array = document.delete_iscsi_snapshot.elements["iscsi_delete_option[]"];

	if (disk_array.length == undefined)
	{
		var delete_id = document.getElementById('id_snap_array');

		if (check_all_option.checked == true)
		{
			if (delete_id.disabled != true)
			{
				delete_id.checked = true;
			}
		}

		else
		{
			delete_id.checked = false;
		}
	}

	if (check_all_option.checked == true)
	{
		for (i = 0;  i < disk_array.length;  i++)
		{
			if (disk_array[i].disabled != true)
			{
				disk_array[i].checked = true;
			}
		}
	}

	else
	{
		for (i = 0;  i < disk_array.length;  i++)
		{
			disk_array[i].checked = false;
		}
	}
}

function validate_delete_snapshot()
{
	var snap_array = document.delete_snapshot.elements["delete_option[]"];
	var snap_array_value = document.getElementById('id_disk_array').value;
	var string = '';

	if (snap_array.length == undefined)
	{
		var delete_id1 = document.getElementById('id_disk_array');

		if (delete_id1.checked != true)
		{
			alert('Please choose a snapshot!');
			return false;
		}

		else
		{
			string = snap_array_value;
		}
	}
	
	else if (snap_array.length > 0)
	{
		for (var i = 0;  i < snap_array.length;  i++)
		{
			if (snap_array[i].checked == true)
			{
				string = string + '@@@' + snap_array[i].value;
			}
		}

		if (string == '')
		{
			alert('Please choose a snapshot!');
			return false;
		}
	}

	document.getElementById('wait').style.display = 'block';

	$.ajax(
	{
		type: 'POST',
		url: 'delete_snapshot.php',
		data: 'proceed_page=proceed&hid_path='+document.delete_snapshot.hid_path.value+'&hid_disk='+document.delete_snapshot.hid_disk.value+'&hid_snapshot='+document.delete_snapshot.hid_snapshot.value+'&hid_size='+document.delete_snapshot.hid_size.value+'&del_disk_array='+string,
		success: function(html)
		{
			$('#response').html(html);
		}
	});
}

function validate_delete_iscsi_snapshot()
{
	var snap_array = document.delete_iscsi_snapshot.elements["iscsi_delete_option[]"];
	var snap_array_value = document.getElementById('id_snap_array').value;
	var string = '';

	if (snap_array.length == undefined)
	{
		var delete_id1 = document.getElementById('id_snap_array');

		if (delete_id1.checked != true)
		{
			alert('Please choose a snapshot!');
			return false;
		}

		else
		{
			string = snap_array_value;
		}
	}
	
	else if (snap_array.length > 0)
	{
		for (var i = 0;  i < snap_array.length;  i++)
		{
			if (snap_array[i].checked == true)
			{
				string = string + '@@@' + snap_array[i].value;
			}
		}

		if (string == '')
		{
			alert('Please choose a snapshot!');
			return false;
		}
	}

	document.getElementById('wait').style.display = 'block';

	$.ajax(
	{
		type: 'POST',
		url: 'delete_iscsi_snapshot.php',
		data: 'proceed_page=proceed&hid_path='+document.delete_iscsi_snapshot.hid_path.value+'&hid_disk='+document.delete_iscsi_snapshot.hid_disk.value+'&hid_snapshot='+document.delete_iscsi_snapshot.hid_snapshot.value+'&hid_size='+document.delete_iscsi_snapshot.hid_size.value+'&del_snap_array='+string,
		success: function(html)
		{
			$('#response').html(html);
		}
	});
}

function validate_add_iscsi_snapshot(target, snapshot, lun)
{
	if (target == '' || snapshot == '' || lun == '')
	{
		alert('All fields are mandatory!');
		return false;
	}

	document.getElementById('wait').style.display = 'block';

	$.ajax(
	{
		type: 'POST',
		url: 'add_snapshot_to_target.php',
		data: 'proceed_page=proceed&target_for_disk='+target+'&disk_to_add='+document.add_disk_to_target.disk_to_add.value+'&lun_to_add='+document.add_disk_to_target.lun_to_add.value,

		success: function(html)
		{
			$('#response').html(html);
		}
	});
}

function validate_del_snapshot(target, disk, active_session_string)
{
	if (target == '' || disk == '')
	{
		alert('This operation requires both target name and disk name!');
		return false;
	}

        if (active_session_string != '')
        {
        	search_active_session = active_session_string.indexOf(target);
                tgt_init_array = new Array();

                tgt_init_array = active_session_string.split('->');

                initiator = tgt_init_array[1];
                initiator = initiator.replace(' ', ', ');
	}

        if (search_active_session >= 0)
	{
        	var response = confirm('\''+disk+'\' is in use under the initiator name \''+initiator+'\'. Do you still want to delete the disk?');

                if (response == true)
                {
			document.getElementById('wait').style.display = 'block';

			$.ajax(
			{
				type: 'POST',
				url: 'del_snapshot_from_target.php',
				data: 'proceed_page=proceed&target_list='+target+'&disks_list='+disk,
		
				success: function(html)
				{
					$('#response').html(html);
				}
			});
		}
		
		else
		{
			return false;
		}
	}

	else
	{
		document.getElementById('wait').style.display = 'block';

		$.ajax(
		{
			type: 'POST',
			url: 'del_snapshot_from_target.php',
			data: 'proceed_page=proceed&target_list='+target+'&disks_list='+disk,
	
			success: function(html)
			{
				$('#response').html(html);
			}
		});
	}
}

function validate_user_create_form()
{
        var username  = document.user_creation.username.value;
        var password  = document.user_creation.password.value;
        var cpassword = document.user_creation.c_password.value;
        var sp_chars  = "\ !@#$%^&*()+=[]\\\';,/{}|\":<>?";
        var spacesExp = /[\s]/;

        var dot_index  = username.indexOf('-');
        var line_index = username.indexOf('_');

        if (username == '')
        {
                //alert('Both username and password are required!');
		 jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:16%; padding-top: 4%; font-family: status-bar;">Please Enter a username</div>', 'User Alert');
                return false;
        }

	 if (password == '')
        {
                //alert('Both username and password are required!');
                 jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:16%; padding-top: 4%; font-family: status-bar;">Please Enter a Password</div>', 'Password Alert');
                return false;
        }

        if (username == 'user' || username == 'group')
        {
                //alert('Please use a different name for user!');
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:19%; padding-top: 4%; font-family: status-bar;">Please use a different name for user</div>', 'User Alert');
                return false;
        }

	
        if (username.length == 1)
        {
                //alert('Please enter a valid string for username!');
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:19%; padding-top: 4%; font-family: status-bar;">Please enter a valid string for username</div>', 'User Alert');
                return false;
        }

        if (dot_index == 0 || line_index == 0 || isNaN(username[0]) == false)
        {
                //alert('User name should start with an alphabet only!');
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:19%; padding-top: 4%; font-family: status-bar;">User name should start with an alphabet only</div>', 'User Alert');
                return false;
        }

        else
        {
                for (var i = 0;  i < username.length;  i++)
		{
                        if (sp_chars.indexOf(username.charAt(i)) != -1)
                        {
                                //alert('Username can contain only alphabets, numbers, \'-\',  \'_\' or \'.\'  !');
				jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:0%; padding-top: 4%; font-family: status-bar;">Username can contain only alphabets, numbers, \'-\',  \'_\' or \'.\'</div>', 'User Alert')
                                return false;
                        }
                }

	        if(username.match(spacesExp))
        	{
                	//alert('Spaces are not allowed in Username!');
			jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:19%; padding-top: 4%; font-family: status-bar;">Spaces are not allowed in Username</div>', 'User Alert');
	                return false;
        	}

	        if(password.length <= 5)
        	{
                	//alert("Password should contains more than 5 characters!");
			jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:19%; padding-top: 4%; font-family: status-bar;">Password should contains more than 5 characters</div>', 'Password Alert');
	                return false;
        	}

	        if(password.match(spacesExp))
        	{
                	//alert("Spaces are not allowed in password!");
			jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:19%; padding-top: 4%; font-family: status-bar;">Spaces are not allowed in password</div>', 'Password Alert');
	                return false;
        	}
		 if(cpassword == '') 
                {
                        //alert("Spaces are not allowed in password!");
                        jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:19%; padding-top: 4%; font-family: status-bar;">Please Enter a Confirm Password</div>', 'Password Alert');
                        return false;
                }

	        if (password != cpassword)
        	{
                	//alert('Passwords do not match!');
			jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:17%; padding-top: 4%; font-family: status-bar;">Passwords do not match</div>', 'Password Alert');
	                return false;
        	}
        }
}

function validate_group_form(group)
{
        if (group == '')
        {
                //alert('Please enter a group name!');
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:19%; padding-top: 4%; font-family: status-bar;">Please enter a group name</div>', 'Group Alert');
                return false;
        }

        else if (group.length == 1)
        {
                //alert('Please enter a valid string for group name!');
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:22%; padding-top: 4%; font-family: status-bar;">Please enter a valid string for group name</div>', 'Group Alert');
                return false;
        }

        else if (group == 'user' || group == 'group')
        {
                //alert('Group name can\'t be \'user\' or \'group\'!');
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:22%; padding-top: 4%; font-family: status-bar;">Group name can\'t be \'user\' or \'group\'</div>', 'Group Alert');
                return false;
        }

        else
        {
                var sp_chars  = "\ !@#$%^&*()+=[]\\\';,/{}|\":<>?";

                var g_dot_index  = group.indexOf('-');
                var g_line_index = group.indexOf('_');

                if (g_dot_index == 0 || g_line_index == 0 || isNaN(group[0]) == false)
                {
                        jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:22%; padding-top: 4%; font-family: status-bar;">Group name should start with an alphabet only</div>', 'Group Alert');
			//alert('Group name should start with an alphabet only!');
                        //document.getElementById("group").focus();
                        return false;
                }

                for (var i = 0;  i < group.length;  i++)
                {
                        if (sp_chars.indexOf(group.charAt(i)) != -1)
                        {
				//alert('Group can contain only only alphabets, numbers, \'-\',  \'_\' or \'.\'  !');
				jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:22%; padding-top: 4%; font-family: status-bar;">Group can contain only only alphabets, numbers, \'-\',  \'_\' or \'.\'</div>', 'Group Alert');
                                return false;
                        }
                }

                document.getElementById('wait').style.display = 'block';

                $.ajax(
                {
                        type: 'POST',
                        url: 'add_groups.php',
                        data: 'group='+group,

                        success: function(html)
                        {
                                $('#response').html(html);
                        }
                });
        }
}

function show_add_group()
{
	var text_box_id = document.getElementById('group_add');
	var button_id   = document.getElementById('group_add_but');
	
	text_box_id.style.visibility = 'visible';
	button_id.style.visibility = 'visible';
	document.user_creation.group.focus();
}

function submit_form()
{
	document.user_creation.action = 'create_groups.php';
	document.user_creation.submit();
}

function show_create_users()
{
	var create_id = document.getElementById('id_user_creation');
	var list_id   = document.getElementById('id_show_user');
	var delete_id = document.getElementById('id_del_user');

	create_id.style.display = 'block';
	delete_id.style.display = 'none';
	list_id.style.display   = 'none';
}

function show_users()
{
	var id = document.getElementById('id_del_user');
	var list_id   = document.getElementById('id_show_user');
	var create_id = document.getElementById('id_user_creation');

	list_id.style.display   = 'none';
	id.style.display        = 'block';
	create_id.style.display = 'none';
}

function show_list_users()
{
	var list_id   = document.getElementById('id_show_user');
	var create_id = document.getElementById('id_user_creation');
	var delete_id = document.getElementById('id_del_user');

	list_id.style.display   = 'block';
	create_id.style.display = 'none';
	delete_id.style.display = 'none';
}


function show_groups_of_users(user)
{
        if (user == 'select-user')
        {
                //alert("Please select a User!");
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:19%; padding-top: 4%; font-family: status-bar;">"Please select a User</div>', 'User Alert ');
                return false;
        }
}

function modify_user_information()
{
        var new_pwd  = document.manage_users.new_pwd.value;
        var c_new_pwd = document.manage_users.c_new_pwd.value;
        var sp_chars  = "\ !@#$%^&*()+=.[]\\\';,/{}|\":<>?";
        var spacesExp = /[\s]/;
	
	/*if(new_pwd == '')
	{

		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:19%; padding-top: 4%; font-family: status-bar;">Please Enter a New Password</div>', 'Password Alert ');
		return false;

	}*/
        if(new_pwd != '')
        {

	        if(new_pwd.match(spacesExp))
        	{
                	//alert("Spaces are not allowed in Password!");
			jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:19%; padding-top: 4%; font-family: status-bar;">Spaces are not allowed in Password</div>', 'Password Alert ');
	                //document.getElementById("new_pwd").focus();
	                return false;
	        }

        	if(new_pwd.length <= 5)
	        {
	                //alert("Password should contain more than 5 characters!");
			jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:19%; padding-top: 4%; font-family: status-bar;">Password should contain more than 5 characters</div>', 'Password Alert ');
	                //document.getElementById("new_pwd").focus();
	                return false;
	        }
	
	        if(c_new_pwd == '')
	        {
	                //alert("Please confirm New Password!");
			jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:19%; padding-top: 4%; font-family: status-bar;">Please confirm New Password</div>', 'Password Alert ');
	                //document.getElementById("c_new_pwd").focus();
	                return false;
	        }
	
	        if(new_pwd != c_new_pwd)
	        {
	                //alert("Passwords do not match!");
			jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:19%; padding-top: 4%; font-family: status-bar;">Passwords do not match</div>', 'Password Alert ');
	                //document.getElementById("c_new_pwd").focus();
       		        return false;
	        }
	}

}

function show_users_of_group(group)
{
        if (group == 'select-user')
        {
                //alert("Please select a Group!");
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:19%; padding-top: 4%; font-family: status-bar;">Please Select  a Group</div>', 'Group Alert ');
                return false;
        }

}

function show_users_to_delete(user)
{
        if (user == 'select-user')
        {
                //alert("Please select a User!");
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:29%; padding-top: 4%; font-family: status-bar;">Please Select a user</div>', 'User Alert ');
                return false;
        }

}


function user_maint_move_groups(fbox, tbox, val)
{
	var arrFbox = new Array();
	var arrTbox = new Array();
	var arrLookup = new Array();
	var i;

	for (i = 0; i < tbox.options.length; i++)
	{
		arrLookup[tbox.options[i].text] = tbox.options[i].value;
		arrTbox[i] = tbox.options[i].text;
	}
	
	var fLength = 0;
	var tLength = arrTbox.length;

	for(i = 0; i < fbox.options.length; i++)
	{
		arrLookup[fbox.options[i].text] = fbox.options[i].value;

		if (fbox.options[i].selected && fbox.options[i].value != "")
		{
			arrTbox[tLength] = fbox.options[i].text;
			tLength++;
		}
			
		else
		{
			arrFbox[fLength] = fbox.options[i].text;
			fLength++;
		}
	}
	
	fbox.length = 0;
	tbox.length = 0;
	var c;
	
	for(c = 0; c < arrFbox.length; c++)
	{
		var no = new Option();
		
		no.value = arrLookup[arrFbox[c]];
		no.text = arrFbox[c];
		fbox[c] = no;
		
		if (val == '2')
		{
			fbox[c].selected = true;
		}
	}
	
	for(c = 0; c < arrTbox.length; c++)
	{
		var no = new Option();
		
		no.value = arrLookup[arrTbox[c]];
		no.text = arrTbox[c];
		tbox[c] = no;
		
		if (val == '1')
		{
			tbox[c].selected = true;
		}
	}
}

function move_data(fbox, tbox, val)
{
	var arrFbox = new Array();
	var arrTbox = new Array();
	var arrLookup = new Array();
	var i;

	for (i = 0; i < tbox.options.length; i++)
	{
		arrLookup[tbox.options[i].text] = tbox.options[i].value;
		arrTbox[i] = tbox.options[i].text;
	}
	
	var fLength = 0;
	var tLength = arrTbox.length;

	for(i = 0; i < fbox.options.length; i++)
	{
		arrLookup[fbox.options[i].text] = fbox.options[i].value;

		if (fbox.options[i].selected && fbox.options[i].value != "")
		{
			arrTbox[tLength] = fbox.options[i].text;
			tLength++;
		}
			
		else
		{
			arrFbox[fLength] = fbox.options[i].text;
			fLength++;
		}
	}
	
	fbox.length = 0;
	tbox.length = 0;
	var c;
	
	for(c = 0; c < arrFbox.length; c++)
	{
		var no = new Option();
		
		no.value = arrLookup[arrFbox[c]];
		no.text = arrFbox[c];
		fbox[c] = no;
		
		if (val == '2')
		{
			fbox[c].selected = true;
		}
	}
	
	for(c = 0; c < arrTbox.length; c++)
	{
		var no = new Option();
		
		no.value = arrLookup[arrTbox[c]];
		no.text = arrTbox[c];
		tbox[c] = no;
		
		if (val == '1')
		{
			tbox[c].selected = true;
		}
	}
}

function validate_user_form(user, pwd, c_pwd, g_count)
{
	if (user == '')
	{
		alert('Please choose a valid user from the list!');
		return false;
	}

	if (pwd != c_pwd)
	{
		alert('Passwords do not match!');
		return false;
	}

	if (g_count == 0)
	{
		alert('You need to choose atleast one group!');
		return false;
	}
}

function validate_modify_group_form(group, users_count)
{
	if (group == '')
	{
		//alert('Please choose a valid group from the list!');
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:19%; padding-top: 4%; font-family: status-bar;">Please choose a valid group from the list</div>', 'Group Alert ');
		return false;
	}
}

function enable_button()
{
	document.manage_users.modifyusers.disabled = false;
}

function init_set_focus()
{
	var hid_session_user = document.user_creation.hid_session_user.value;

	if (hid_session_user != 'Full Access')
	{
		var form_count = document.forms.length;

		for (i = 0;  i < form_count;  i++)
		{
			var elem_count = document.forms[i].elements.length;

			for (j = 0;  j < elem_count;  j++)
			{
				document.forms[i].elements[j].disabled = true;
			}
		}
	}

	document.user_creation.username.focus();
	document.manage_users.primary_group.value = document.manage_users.hid_primary.value;
}

function do_delete_users(user_to_delete)
{
	document.getElementById('wait').style.display = 'block';

	$.ajax(
	{
		type: 'POST',
		url: 'delete_users.php',
		data: 'proceed_page=proceed&delete_users='+user_to_delete+'&del_user=Delete',

		success: function(html)
		{
			$('#response').html(html);
		}
	});
}

function do_delete_groups(group_to_delete)
{
	if (group_to_delete == 'USER')
	{
		//alert('Group \'USER\' can\'t be deleted!');
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:19%; padding-top: 4%; font-family: status-bar;">Group \'USER\' can\'t be deleted</div>', 'Group Alert ');
		return false;
	}

	document.getElementById('wait').style.display = 'block';

	$.ajax(
	{
		type: 'POST',
		url: 'delete_groups.php',
		data: 'delete_groups='+group_to_delete+'&del_group=Delete',

		success: function(html)
		{
			$('#response').html(html);
		}
	});
}
			
function select_all()
{
	var check_all_option = document.getElementById('id_select_all');
	var task_array = document.scheduled_tasks.elements["delete_tasks[]"];

	if (task_array.length == undefined)
	{
		var delete_id = document.getElementById('id_del_tasks');

		if (check_all_option.checked == true)
		{
			if (delete_id.disabled != true)
			{
				delete_id.checked = true;
			}
		}

		else
		{
			delete_id.checked = false;
		}
	}

	if (check_all_option.checked == true)
	{
		for (i = 0;  i < task_array.length;  i++)
		{
			if (task_array[i].disabled != true)
			{
				task_array[i].checked = true;
			}
		}
	}

	else
	{
		for (i = 0;  i < task_array.length;  i++)
		{
			task_array[i].checked = false;
		}
	}
}

function validate_delete_tasks()
{
	var string = '';

	var task_array = new Array();
	task_array = document.scheduled_tasks.elements["delete_tasks[]"];

	if (task_array.length == null)
	{
		var task_id    = document.getElementById('id_del_tasks');
		
		if (task_id.checked != true)
		{
			//alert('Please choose a task to delete!');
			jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:19%; padding-top: 4%; font-family: status-bar;">Please choose a task to delete</div>', 'Task Alert ');
			return false;
		}

		else
		{
			string = task_id.value;
		}
	}

	else
	{
		for (i = 0;  i < task_array.length;  i++)
		{
			if (task_array[i].checked == true)
			{
				string = string + '@@@' + task_array[i].value;
			}
		}

		if (string == '')
		{
			alert('Please choose a task!');
			return false;
		}

		string = string.replace(/&/g, '<AND>');
		string = string.replace(/\ /g, '<SPACE>');
	}
	
	document.getElementById('wait').style.display = 'block';

	$.ajax(
	{
		type: 'POST',
		url: 'remove_tasks.py',
		data: 'btn_remove=Remove&hid_cron_entry='+string,

		success: function(html)
		{
			$('#response').html(html);
		}
	});
}

function confirm_nas_disk_delete()
{
	var process;
	process = document.process_form.hid_lock_var.value;

	/* Add a line (process = 'done';) to unlock the process temporarily */

	/*
	==================================================
	To ensure that when one delete process is going on,
	deletion for others should be disabled.
	==================================================
	*/
		
	var string = '';

	var disk_array = document.disk_to_delete.elements["delete_option[]"];

	if (disk_array.length == null)
	{
		var disk_id    = document.getElementById('id_disk_array');
		
		if (disk_id.checked != true)
		{
			alert('Please choose a disk to delete!');
			return false;
		}
		/*if (disk_id.checked == true)
		{
			
			confirm ('Are you sure want to delete');
			return false;
		}*/
		else
		{
			if (process == 'in progress')
			{
				alert('Can not delete disk now! Please reload the page and try again.');
				return false;
			}

			else if (process == 'done')
			{
				var response = confirm("Delete the disk?");

				if (response == true)
				{
					var response1 = confirm("Sure? Data will be lost!");

					if (response1 == true)
					{
						string = disk_id.value;

						document.getElementById('wait').style.display = 'block';
						$.ajax(
						{
							type: 'POST',
							url: 'delete_disks.py',
							data: 'hid_protocol='+document.disk_to_delete.hid_protocol.value+'&delete_but=Delete selected&hid_page='+document.disk_to_delete.hid_page.value+'&disks_string='+string,

							success: function(html)
							{
								$('#response').html(html);
							}
						});
					}
				
					else
					{
						alert('Action Canceled');
						return false;
					}
				}
	
				else
				{
					alert('Action Canceled');
					return false;
				}
			}
		}
	}

	else
	{
		for (i = 0;  i < disk_array.length;  i++)
		{
			if (disk_array[i].checked == true)
			{
				string = string + '@@@' + disk_array[i].value;
			}
		}

		if (string == '')
		{
			alert('Please choose a disk!');
			return false;
		}

		else
		{
			if (process == 'in progress')
			{
				alert('Can not delete disk now! Please reload the page and try again.');
				return false;
			}

			else if (process == 'done')
			{
				var response = confirm("Delete the disk?");

				if (response == true)
				{
					var response1 = confirm("Sure? Data will be lost!");

					if (response1 == true)
					{
						document.getElementById('wait').style.display = 'block';
						$.ajax(
						{
							type: 'POST',
							url: 'delete_disks.php',
							data: 'hid_protocol='+document.disk_to_delete.hid_protocol.value+'&delete_but=Delete selected&hid_page='+document.disk_to_delete.hid_page.value+'&disks_string='+string,

							success: function(html)
							{
								$('#response').html(html);
							}
						});
					}
				
					else
					{
						alert('Action Canceled');
						return false;
					}
				}
	
				else
				{
					alert('Action Canceled');
					return false;
				}
			}
		}
	}
}

function nas_disk_delete()
{
	var string = '';
	

        var delete_option = document.disk_to_delete.elements["delete_option[]"];

        if (delete_option.length == null)
        {
                var volume_id    = document.getElementById('id_disk_array');

                if (volume_id.checked != true)
                {
                        alert('Please select a Nas Disk to delete!');
                        return false;
			
                }

                else
                {
                        var response = confirm("Are you sure want to delete");

                        if (response == true)
                        {
                                string = volume_id.value;

                                document.getElementById('wait').style.display = 'block';
				$.ajax(
                                {
                                        type: 'POST',
                                        url: 'remove_volume.php',
                                        data: 'proceed_page=proceed&volume_string='+string,

                                        success: function(html)
                                        {
                                                $('#response').html(html);
                                        }
                                });
                        }
			
                        else
                        {
                                //alert('Action Canceled');
                                return false;
                        }
                }

        }

        else
        {
                for (i = 0;  i < delete_option.length;  i++)
                {
                        if (delete_option[i].checked == true)
                        {
                                string = string + '@@@' +delete_option[i].value;
                        }
                }

		if (string == '')
                {
                        alert('Please select a Nas Disk to delete!');
                        return false;
                }

                else
                {
                        var response = confirm("Are you sure want to delete");

                        if (response == true)
                        {
                                document.getElementById('wait').style.display = 'block';

                                $.ajax(
                                {
                                        type: 'POST',
                                        url: 'remove_volume.php',
                                        data: 'proceed_page=proceed&volume_string='+string,

                                        success: function(html)
                                        {
                                                $('#response').html(html);
                                        }
                                });
                        }

                        else
                        {
                               // alert('Action Canceled');
                                return false;
                        }
                }
        }
}



function san_disk_delete()
{
	var string = '';
	
        var delete_option = document.san_det_list.elements["delete_option_san[]"];

        if (delete_option.length == null)
        {
                var volume_id    = document.getElementById('id_disk_array_san');

                if (volume_id.checked != true)
                {
                       // alert('Please select a SAN Disk to delete!');
			 jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:-4%; padding-top: 4%; font-family: status-bar;">Please select a SAN Disk to delete</div>', 'Alert Dialog');
                        return false;
			
                }

                else
                {
                        var response = confirm("Are you sure want to delete");

                        if (response == true)
                        {
                                string = volume_id.value;

                                document.getElementById('wait').style.display = 'block';
				$.ajax(
                                {
                                        type: 'POST',
                                        url: 'remove_volume.php',
                                        data: 'proceed_page=proceed&volume_string='+string,

                                        success: function(html)
                                        {
                                                $('#response').html(html);
                                        }
                                });
                        }
			
                        else
                        {
                                //alert('Action Canceled');
                                return false;
                        }
                }

        }

        else
        {
                for (i = 0;  i < delete_option.length;  i++)
                {
                        if (delete_option[i].checked == true)
                        {
                                string = string + '@@@' +delete_option[i].value;
                        }
                }

		if (string == '')
                {
                        //alert('Please select a SAN Disk to delete!');
			jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:-4%; padding-top: 4%; font-family: status-bar;">Please select a SAN Disk to delete</div>', 'Alert Dialog');
                        return false;
                }

                else
                {
                        var response = confirm("Are you sure want to delete");

                        if (response == true)
                        {
                                document.getElementById('wait').style.display = 'block';

                                $.ajax(
                                {
                                        type: 'POST',
                                        url: 'remove_volume.php',
                                        data: 'proceed_page=proceed&volume_string='+string,

                                        success: function(html)
                                        {
                                                $('#response').html(html);
                                        }
                                });
                        }

                        else
                        {
                               // alert('Action Canceled');
                                return false;
                        }
                }
        }
}


function vtl_disk_delete(act_proc)
{
	var string = '';
	
        var delete_option = document.san_det_list.elements["delete_option_san[]"];

        if (delete_option.length == null)
        {
                var volume_id    = document.getElementById('id_disk_array_san');

                if (volume_id.checked != true)
                {
                       // alert('Please select a SAN Disk to delete!');
			 alert("Please select a VTL Library to delete");
			 //jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:-4%; padding-top: 4%; font-family: status-bar;">Please select a VTL Library to delete</div>', 'Alert Dialog');
                        return false;
			
                }

                else
                {
			document.getElementById('keep').style.display = 'block';
                        document.getElementById('second_butt').style.display='none';
                }

        }

        else
        {
                for (i = 0;  i < delete_option.length;  i++)
                {
                        if (delete_option[i].checked == true)
                        {
                                string = string + '@@@' +delete_option[i].value;
                        }
                }

		if (string == '')
                {
                        //alert('Please select a SAN Disk to delete!');
			//jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:-4%; padding-top: 4%; font-family: status-bar;">Please select a VTL Library to delete</div>', 'Alert Dialog');
			alert("Please select a VTL Library to delete");
                        return false;
                }

                else
                {
			document.getElementById('keep').style.display = 'block';
			document.getElementById('second_butt').style.display='none';

                }
        }

	if(act_proc == 'yes')
	{
		document.san_det_list.action = 'iframe_vtl_settings.py#tabs-2';
		document.getElementById('wait').style.display = 'block';
	}
}

function cancel_disk_delete()
{
	document.getElementById('keep').style.display = 'none';
	document.getElementById('second_butt').style.display='block';
}

function create_vtl_disk()
{
	var size = document.getElementById('tape_size');
	var hid_vtl_size = document.getElementById('hid_vtl_size');
	
	if(size.value == '')
	{
		alert('Please Enter Tape Size.');
		document.create_container.tape_size.focus();
		return false;
	}

	if(isNaN(size.value) == true)
	{
		alert("Enter only integer value in Tape Size.");
		document.create_container.tape_size.focus();
		return false;
	}


	if(parseFloat(size.value) > parseFloat(hid_vtl_size.value))
	{
		alert("Tape size cannot be greater that VTL disk size!");
		return false;
	}

	document.getElementById('wait').style.display = 'block';

}

function validate_add_to_target()
{
	var library_name = document.getElementById("id_library_name");
	var initiator_name = document.getElementById("id_initiator_name");
	var hasChecked = false;

	if(library_name.value == "select-vtl-library")
	{
		//alert("Please Select a Library!");
		//document.add_target_form.library_name.focus();
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:16%; padding-top: 4%; font-family: status-bar;">Please Select a Library.</div>', 'Vtl Alert');
		return false;
	}

	if(initiator_name.value == '')
	{
		//alert("Please Enter Initiator Name!");
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:16%; padding-top: 4%; font-family: status-bar;">Please Enter Initiator Name.</div>', 'Vtl Alert');
		//document.add_target_form.initiator_name.focus();
		return false;
	}
	
	document.getElementById('wait').style.display = 'block';
}

function add_tape_to_library()
{
	var tape_density = document.getElementById('tape_density');
	var tape_type = document.getElementById('tape_type');
	var tape_size = document.getElementById('tape_size');

	if(tape_density.value == '')
	{
		alert('Please Select Tape Density.');
		document.add_tape_form.tape_density.focus();
		return false;
	}

	if(tape_type.value == '')
	{
		alert('Please Select Tape Type.');
		document.add_tape_form.tape_type.focus();
		return false;
	}

	if(tape_size.value == '')
	{
		alert('Please Enter Tape Size.');
		document.add_tape_form.tape_size.focus();
		return false;
	}

	if(isNaN(tape_size.value) == true)
	{
		alert("Enter only integer value in Tape Size.");
		document.add_tape_form.tape_size.focus();
		return false;
	}

	document.add_tape_form.action = 'iframe_vtl_settings.py#tabs-2';	

}

function bio_disk_delete()
{
	var string = '';
	
        var delete_option = document.disk_to_delete.elements["delete_option[]"];

        if (delete_option.length == null)
        {
                var volume_id    = document.getElementById('id_disk_array');

                if (volume_id.checked != true)
                {
			jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:-4%; padding-top: 4%; font-family: status-bar;">Please select a Block Disk to delete</div>', 'Alert Dialog');
                        return false;
                }

                else
                {
                        var response = confirm("Are you sure want to delete");

                        if (response == true)
                        {
                                string = volume_id.value;

                                document.getElementById('wait').style.display = 'block';
				$.ajax(
                                {
                                        type: 'POST',
                                        url: 'remove_volume.php',
                                        data: 'proceed_page=proceed&volume_string='+string,

                                        success: function(html)
                                        {
                                                $('#response').html(html);
                                        }
                                });
                        }
			
                        else
                        {
                                return false;
                        }
                }

        }

        else
        {
                for (i = 0;  i < delete_option.length;  i++)
                {
                        if (delete_option[i].checked == true)
                        {
                                string = string + '@@@' +delete_option[i].value;
                        }
                }

		if (string == '')
                {
			jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:-4%; padding-top: 4%; font-family: status-bar;">Please select a Block Disk to delete</div>', 'Alert Dialog');
                        return false;
                }

                else
                {
                        var response = confirm("Are you sure want to delete");

                        if (response == true)
                        {
                                document.getElementById('wait').style.display = 'block';

                                $.ajax(
                                {
                                        type: 'POST',
                                        url: 'remove_volume.php',
                                        data: 'proceed_page=proceed&volume_string='+string,

                                        success: function(html)
                                        {
                                                $('#response').html(html);
                                        }
                                });
                        }

                        else
                        {
                                return false;
                        }
                }
        }
}



function fio_disk_delete()
{
	var string = '';
	
        var delete_option = document.img_deletion.elements["delete_option_img[]"];

        if (delete_option.length == null)
        {
                var volume_id    = document.getElementById('id_disk_array_img');

                if (volume_id.checked != true)
                {
                        //alert('Please select a FIO Disk to delete!');
			jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:5%; padding-top: 4%; font-family: status-bar;">Please select a FIO Disk to delete</div>', 'Alert Dialog');
                        return false;
			
                }

                else
                {
                        var response = confirm("Are you sure want to delete");

                        if (response == true)
                        {
                                string = volume_id.value;

                                document.getElementById('wait').style.display = 'block';
				$.ajax(
                                {
                                        type: 'POST',
                                        url: 'remove_volume.php',
                                        data: 'proceed_page=proceed&volume_string='+string,

                                        success: function(html)
                                        {
                                                $('#response').html(html);
                                        }
                                });
                        }
			
                        else
                        {
                                //alert('Action Canceled');
                                return false;
                        }
                }

        }

        else
        {
                for (i = 0;  i < delete_option.length;  i++)
                {
                        if (delete_option[i].checked == true)
                        {
                                string = string + '@@@' +delete_option[i].value;
                        }
                }

		if (string == '')
                {
                       // alert('Please select a FIO Disk to delete!');
			jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:5%; padding-top: 4%; font-family: status-bar;">Please select a FIO Disk to delete</div>', 'Alert Dialog');
                        return false;
                }

                else
                {
                        var response = confirm("Are you sure want to delete");

                        if (response == true)
                        {
                                document.getElementById('wait').style.display = 'block';

                                $.ajax(
                                {
                                        type: 'POST',
                                        url: 'remove_volume.php',
                                        data: 'proceed_page=proceed&volume_string='+string,

                                        success: function(html)
                                        {
                                                $('#response').html(html);
                                        }
                                });
                        }

                        else
                        {
                               // alert('Action Canceled');
                                return false;
                        }
                }
        }
}

function select_nas_disks_all()
{
	var check_all_option = document.getElementById('id_select_all');
	var disk_array = document.disk_to_delete.elements["delete_option[]"];

	if (disk_array.length == undefined)
	{
		var delete_id = document.getElementById('id_disk_array');

		if (check_all_option.checked == true)
		{
			if (delete_id.disabled != true)
			{
				delete_id.checked = true;
			}
		}

		else
		{
			delete_id.checked = false;
		}
	}

	if (check_all_option.checked == true)
	{
		for (i = 0;  i < disk_array.length;  i++)
		{
			if (disk_array[i].disabled != true)
			{
				disk_array[i].checked = true;
			}
		}
	}

	else
	{
		for (i = 0;  i < disk_array.length;  i++)
		{
			disk_array[i].checked = false;
		}
	}
}

function confirm_iscsi_disks_delete()
{
	var process;
	process = document.process_form.hid_lock_var.value;

	/* Add the line (process = 'done';) to unlock the process temporarily */

	/*
	==================================================
	To ensure that when one delete process is going on,
	deletion for others should be disabled.
	==================================================
	*/
		
	var string = '';

	var disk_array = document.disk_to_delete.elements["delete_option[]"];

	if (disk_array.length == null)
	{
		var disk_id    = document.getElementById('id_disk_array');
		
		if (disk_id.checked != true)
		{
			alert('Please choose a disk to delete!');
			return false;
		}

		else
		{
			if (process == 'in progress')
			{
				alert('Can not delete disk now! Please reload the page and try again.');
				return false;
			}

			else if (process == 'done')
			{
				var response = confirm("Delete the disk?");

				if (response == true)
				{
					var response1 = confirm("Sure? Data will be lost!");

					if (response1 == true)
					{
						string = disk_id.value;

						document.getElementById('wait').style.display = 'block';
						$.ajax(
						{
							type: 'POST',
							url: 'delete_disks.php',
							data: 'hid_protocol='+document.disk_to_delete.hid_protocol.value+'&delete_but=Delete selected&hid_page='+document.disk_to_delete.hid_page.value+'&disks_string='+string,

							success: function(html)
							{
								$('#response').html(html);
							}
						});
					}
				
					else
					{
						alert('Action Canceled');
						return false;
					}
				}
	
				else
				{
					alert('Action Canceled');
					return false;
				}
			}
		}
	}

	else
	{
		for (i = 0;  i < disk_array.length;  i++)
		{
			if (disk_array[i].checked == true)
			{
				string = string + '@@@' + disk_array[i].value;
			}
		}

		if (string == '')
		{
			alert('Please choose a disk!');
			return false;
		}

		else
		{
			if (process == 'in progress')
			{
				alert('Can not delete disk now! Please reload the page and try again.');
				return false;
			}

			else if (process == 'done')
			{
				var response = confirm("Delete the disk?");

				if (response == true)
				{
					var response1 = confirm("Sure? Data will be lost!");

					if (response1 == true)
					{
						document.getElementById('wait').style.display = 'block';
						$.ajax(
						{
							type: 'POST',
							url: 'delete_disks.php',
							data: 'hid_protocol='+document.disk_to_delete.hid_protocol.value+'&delete_but=Delete selected&hid_page='+document.disk_to_delete.hid_page.value+'&disks_string='+string,

							success: function(html)
							{
								$('#response').html(html);
							}
						});
					}
				
					else
					{
						alert('Action Canceled');
						return false;
					}
				}
	
				else
				{
					alert('Action Canceled');
					return false;
				}
			}
		}
	}
}

function select_iscsi_disks_all()
{
	var check_all_option = document.getElementById('id_select_all');
	var disk_array = document.disk_to_delete.elements["delete_option[]"];

	if (disk_array.length == undefined)
	{
		var delete_id = document.getElementById('id_disk_array');

		if (check_all_option.checked == true)
		{
			if (delete_id.disabled != true)
			{
				delete_id.checked = true;
			}
		}

		else
		{
			delete_id.checked = false;
		}
	}

	if (check_all_option.checked == true)
	{
		for (i = 0;  i < disk_array.length;  i++)
		{
			if (disk_array[i].disabled == false)
			{
				if (disk_array[i].disabled != true)
				{
					disk_array[i].checked = true;
				}
			}
		}
	}

	else
	{
		for (i = 0;  i < disk_array.length;  i++)
		{
			disk_array[i].checked = false;
		}
	}
}



function select_san_disks_all()
{
	var check_all_option = document.getElementById('id_select_all_san');
	var disk_array = document.san_det_list.elements["delete_option_san[]"];

	if (disk_array.length == undefined)
	{
		var delete_id = document.getElementById('id_disk_array_san');

		if (check_all_option.checked == true)
		{
			if (delete_id.disabled != true)
			{
				delete_id.checked = true;
			}
		}

		else
		{
			delete_id.checked = false;
		}
	}

	if (check_all_option.checked == true)
	{
		for (i = 0;  i < disk_array.length;  i++)
		{
			if (disk_array[i].disabled == false)
			{
				if (disk_array[i].disabled != true)
				{
					disk_array[i].checked = true;
				}
			}
		}
	}

	else
	{
		for (i = 0;  i < disk_array.length;  i++)
		{
			disk_array[i].checked = false;
		}
	}
}

function select_all_portals_to_add()
{
	var check_all_option = document.getElementById('id_select_all_portals');
	var disk_array = document.add_target_form.elements["portals_array[]"];

	if (disk_array.length == undefined)
	{
		var delete_id = document.getElementById('id_portals_array');

		if (check_all_option.checked == true)
		{
			if (delete_id.disabled != true)
			{
				delete_id.checked = true;
			}
		}

		else
		{
			delete_id.checked = false;
		}
	}

	if (check_all_option.checked == true)
	{
		for (i = 0;  i < disk_array.length;  i++)
		{
			if (disk_array[i].disabled == false)
			{
				if (disk_array[i].disabled != true)
				{
					disk_array[i].checked = true;
				}
			}
		}
	}

	else
	{
		for (i = 0;  i < disk_array.length;  i++)
		{
			disk_array[i].checked = false;
		}
	}
}



function select_iscsi_disks_all_img()
{
	var check_all_option = document.getElementById('id_select_all_img');

	var disk_array = document.img_deletion.elements["delete_option_img[]"];

	if (disk_array.length == undefined)
	{
		var delete_id = document.getElementById('id_disk_array_img');

		if (check_all_option.checked == true)
		{
			if (delete_id.disabled != true)
			{
				delete_id.checked = true;
			}
		}

		else
		{
			delete_id.checked = false;
		}
	}

	if (check_all_option.checked == true)
	{
		for (i = 0;  i < disk_array.length;  i++)
		{
			if (disk_array[i].disabled == false)
			{
				if (disk_array[i].disabled != true)
				{
					disk_array[i].checked = true;
				}
			}
		}
	}

	else
	{
		for (i = 0;  i < disk_array.length;  i++)
		{
			disk_array[i].checked = false;
		}
	}
}

function select_iscsi_disks_all_img2()
{
	var check_all_option = document.getElementById('id_select_all_img');

	var disk_array = document.disk_to_delete.elements["delete_option_img[]"];

	if (disk_array.length == undefined)
	{
		var delete_id = document.getElementById('id_disk_array_img');

		if (check_all_option.checked == true)
		{
			if (delete_id.disabled != true)
			{
				delete_id.checked = true;
			}
		}

		else
		{
			delete_id.checked = false;
		}
	}

	if (check_all_option.checked == true)
	{
		for (i = 0;  i < disk_array.length;  i++)
		{
			if (disk_array[i].disabled == false)
			{
				if (disk_array[i].disabled != true)
				{
					disk_array[i].checked = true;
				}
			}
		}
	}

	else
	{
		for (i = 0;  i < disk_array.length;  i++)
		{
			disk_array[i].checked = false;
		}
	}
}

function setBoxValue(val, box)
{
	var b = document.getElementById('output' +box);
	val = Math.round(val * 1000) / 1000;
	b.value = val;
}

function add_disk_set_focus()
{
	document.add_disk.new_size.focus();
}

function validate()
{
	var size, mb_gb, n_size, mult, disk_size, size_id;

	mb_gb   = document.add_disk.gb_mb.value;
	n_size  = document.add_disk.new_size.value;
	size    = document.add_disk.size.value;
	size_id = document.getElementById('size_id');

	if (mb_gb == 'TB')
	{
		mult = 1024;
	}

	if (mb_gb == 'GB')
	{
		mult = 1;
	}

	else if (mb_gb == '')
	{
		mult = 0;
	}
	
	disk_size = n_size * mult;
	document.add_disk.new_size.value = disk_size;
	document.add_disk.gb_mb.value = 'GB';

	if (disk_size > size)
	{
		alert('New size can not be greater than existing size');
		document.add_disk.new_size.value = 1;
		document.add_disk.new_size.focus();
		document.add_disk.gb_mb.value = '';
		size_id.focus();
	}
}

function change_lable()
{
	var new_create;

	new_create = document.add_disk.lvolume.value;

	if (new_create == 'NEW')
	{
		document.add_disk.action_but.value = 'Create';
		document.add_disk.action_but.disabled = false;
	}

	else if (new_create == '')
	{
		alert('All fields are mandatory');
	}

	else
	{
		document.add_disk.action_but.value = 'Increase';
		document.add_disk.action_but.disabled = false;
	}
}

function validate_add_disk_form()
{
	var mb_gb, new_size, size, mult, disk_size, size_id;
	new_size = 0;

	mb_gb    = document.add_disk.gb_mb.value;
	new_size = document.add_disk.new_size.value;
	size    = document.add_disk.size.value;
	size_id = document.getElementById('size_id');

	var disk_size_array = null;

	var disk_size_pattern = /^([0-9]{1,8})\.([0-9]{1,8})|([0-9]{1,8})$/;
	disk_size_array = new_size.match(disk_size_pattern);

	if (mb_gb == "" || new_size == "")
	{
		alert ('All fields are mandatory. Please enter valid values');
		document.add_disk.new_size.value = 1;
		document.add_disk.new_size.focus();
		document.add_disk.gb_mb.value = '';
		return false;
	}

	if (new_size == 0)
	{
		alert ('Size can not be zero!');
		document.add_disk.new_size.value = 1;
		document.add_disk.new_size.focus();
		document.add_disk.gb_mb.value = '';
		return false;
	}

	if (mb_gb == 'TB')
	{
		mult = 1024;
	}

	if (mb_gb == 'GB')
	{
		mult = 1;
	}

	else if (mb_gb == '')
	{
		mult = 0;
	}
	
	disk_size = new_size * mult;
	document.add_disk.new_size.value = disk_size;
	document.add_disk.gb_mb.value = 'GB';

	if (disk_size > size)
	{
		alert('New size can not be greater than existing size');
		document.add_disk.new_size.value = 1;
		document.add_disk.new_size.focus();
		document.add_disk.gb_mb.value = '';
		size_id.focus();

		return false;
	}

	if (disk_size == 'NaN')
	{
		alert ('Please enter a valid size!');
		document.add_disk.new_size.value = 1;
		document.add_disk.new_size.focus();
		document.add_disk.gb_mb.value = '';
		return false;
	}
		
	if (new_size == 'NaN')
	{
		alert ('Please enter a valid size!');
		document.add_disk.new_size.value = 1;
		document.add_disk.new_size.focus();
		document.add_disk.gb_mb.value = '';
		return false;
	}

	if (disk_size_array == null)
	{
		alert ('Please enter a valid size!');
		document.add_disk.new_size.value = 1;
		document.add_disk.new_size.focus();
		document.add_disk.gb_mb.value = '';
		return false;
	}
		
	var type = document.add_disk.hid_page.value;

	if (type == 'NAS / VOLUME CONFIGURATION')
	{
		block_size = '';
	}

	if (type == 'ISCSI / DISK CONFIGURATION')
	{
		block_size = document.add_disk.block_size.value;
	}

	document.getElementById('wait').style.display = 'block';

	$.ajax(
	{
		type: 'POST',
		url: 'add_iscsi_nas_disk.php',
		data: 'new_size='+new_size+'&gb_mb='+mb_gb+'&hid_type='+type+'&lvolume=&hid_volume='+document.add_disk.hid_volume.value+'&action_but='+document.add_disk.action_but.value+'&block_size='+block_size+'&hid_size='+document.add_disk.hid_size.value+'&hid_page='+type+'&hid_frompg='+document.add_disk.hid_frompg.value+'&hid_diskname='+document.add_disk.hid_diskname.value+'&action_but1='+document.add_disk.action_but1.value,

		success: function(html)
		{
			$('#response').html(html);
		}
	});
}

function show_nas_disk_dropdown()
{
	var option_array = document.getElementsByName('create');
	var nas_disk_id  = document.getElementById('id_nas_disks');
	var b_disk_id    = document.getElementById('id_backup_disks');

	for (i = 0;  i < option_array.length;  i++)
	{
		if (option_array[i].checked)
		{
			if (option_array[i].value == 'Create')
			{
				nas_disk_id.style.visibility = 'visible';
				b_disk_id.style.visibility = 'hidden';
				document.add_del_disk.btn_create.value = 'Create backup disk';
			}

			else
			{
				b_disk_id.style.visibility = 'visible';
				nas_disk_id.style.visibility = 'hidden';
				document.add_del_disk.btn_create.value = 'Delete backup disk';
			}
		}
	}
}

function show_dirs_shares()
{
	var options_array = document.getElementsByName('backup_type');

	disks_options  = document.local_backup.hid_dirs.value;
	shares_options = document.local_backup.hid_shares.value;

	for (i = 0;  i < options_array.length;  i++)
	{
		if (options_array[i].checked)
		{
			if (options_array[i].value == 'disk_backup')
			{
				shares_options = '';
				
				document.local_backup.hid_disk_shares.value            = 'disks';
				document.getElementById('id_source_options').innerHTML = disks_options;
				document.getElementById('id_dest_options').innerHTML   = '';
			}

			else
			{
				disks_options = '';

				document.local_backup.hid_disk_shares.value            = 'shares';
				document.getElementById('id_source_options').innerHTML = shares_options;
				document.getElementById('id_dest_options').innerHTML   = '';
			}
		}
	}
}

function set_dest_disks()
{
	disks_shares   = document.local_backup.hid_disk_shares.value;
        disks_options  = document.local_backup.hid_dirs.value;
        shares_options = document.local_backup.hid_shares.value;
	
	diskshare_selected = document.getElementById('id_source_options').value;

	if (disks_shares == 'disks')
	{
		replace_string = '<option value = "' + diskshare_selected + '">' + diskshare_selected + '</option>';
		new_string = disks_options.replace(replace_string, '');
		new_string = new_string.replace('<option value = "">Choose a NAS disk</option>', '') ;
	}

	else
	{
		replace_string = "<option value = '" + diskshare_selected + "'>" + diskshare_selected + "</option>";
		new_string = shares_options.replace(replace_string, '');
		new_string = new_string.replace("<option value = ''>Choose a share</option>", "") ;
	}

	document.getElementById('id_dest_options').innerHTML = new_string;
}

function validate_backup_form()
{
	var options_array = document.getElementsByName('backup_type');
	var source_disk   = document.local_backup.source.value;
	var dest_disk     = document.local_backup.destination.value;
	
	for (i = 0;  i < options_array.length;  i++)
	{
		if (!options_array[0].checked && !options_array[1].checked)
		{
			alert('You need to choose an option!');
			return false;
		}

		else if (options_array[i].checked)
		{
			disk_share = options_array[i].value;
		}

		if (source_disk == '')
		{
			alert('Please choose a source disk!');
			return false;
		}

		if (dest_disk == '')
		{
			alert('Please choose a destination disk!');
			return false;
		}
	}

	var schedule_array = document.getElementsByName('week');

	for (i = 0;  i < schedule_array.length;  i++)
	{
		if (schedule_array[i].checked)
		{
			week_string = schedule_array[i].value;
		}
	}

	document.getElementById('wait').style.display = 'block';

	$.ajax(
	{
		type: 'POST',
		url: 'take_local_backup.py',
		data:'proceed_page=proceed&source='+source_disk+'&destination='+dest_disk+'&backup_type='+disk_share+'&schedule='+document.local_backup.schedule.checked+'&btn_backup='+document.local_backup.btn_backup.value+'&week='+week_string+'&hours='+document.local_backup.hours.value+'&mins='+document.local_backup.mins.value+'&day='+document.local_backup.day.value+'&month='+document.local_backup.month.value, 

		success: function(html)
		{
			$('#response').html(html);
		}
	});
}

function show_scheduler()
{
	var option   = document.local_backup.schedule.checked;
	var table_id = document.getElementById('id_scheduling');

	if (option == true)
	{
		table_id.style.display = 'block';
		document.local_backup.btn_backup.value = 'Schedule backup';
	}

	else
	{
		table_id.style.display = 'none';
		document.local_backup.btn_backup.value = 'Take backup';
	}
}

function validate_create_disks()
{
	var option_array = document.getElementsByName('create');

	for (i = 0;  i < option_array.length;  i++)
	{
		if (!option_array[0].checked && !option_array[1].checked)
		{
			alert('You need to choose an option!');
			return false;
		}

		else
		{
			if (option_array[i].checked)
			{
				var nas_disk = document.add_del_disk.n_disks.value;
				var bck_disk = document.add_del_disk.b_disks.value;

				if (option_array[i].value == 'Create')
				{
					if (nas_disk == '')
					{
						alert('Please choose a disk!');
						return false;
					}

					else
					{
						option = 'Create';
					}
				}

				else if (option_array[i].value == 'Delete')
				{
					if (bck_disk == '')
					{
						alert('Please choose a disk!');
						return false;
					}

					else
					{
						var response = confirm('Do you really want to delete this disk?');
						if (response == true)
						{
							document.getElementById('wait').style.display = 'block';

							$.ajax(
							{
								type: 'POST',
								url: 'add_del_disk.php',
								data: 'proceed_page=proceed&create=Delete&n_disks='+nas_disk+'&b_disks='+bck_disk,

								success: function html(html)
								{
									$('#response').html(html);
								}
							});
						}

						else
						{
							return false;
						}
					}
				}
			}
		}
	}

	document.getElementById('wait').style.display = 'block';

	$.ajax(
	{
		type: 'POST',
		url: 'add_del_disk.py',
		data: 'proceed_page=proceed&create='+option+'&n_disks='+nas_disk+'&b_disks='+bck_disk,

		success: function html(html)
		{
			$('#response').html(html);
		}
	});
}

function show_dest_disks(disk_share)
{
	var id_disk  = document.getElementById('id_dest_disks');
	var id_share = document.getElementById('id_dest_shares');

	if (disk_share == 'disks')
	{
		id_disk.style.visibility  = 'visible';
		id_share.style.visibility = 'hidden';
	}

	if (disk_share == 'shares')
	{
		id_share.style.visibility = 'visible';
		id_disk.style.visibility  = 'hidden';
	}
}

function validate_restore_form(backup, disk, share)
{
	if (backup == '' || (disk == '' && share == ''))
	{
		alert('You need to choose a backup and a destination directory/share!');
		return false;
	}
}

function select_all_volumes()
{
	var check_all_option = document.getElementById('id_select_all');
	var volume_array = document.remove_vol.elements["used_volumes_array[]"];

	if (volume_array.length == undefined)
	{
		var delete_id = document.getElementById('id_used_volumes');

		if (check_all_option.checked == true)
		{
			if (delete_id.disabled != true)
			{
				delete_id.checked = true;
			}
		}

		else
		{
			delete_id.checked = false;
		}
	}

	if (check_all_option.checked == true)
	{
		for (i = 0;  i < volume_array.length;  i++)
		{
			if (volume_array[i].disabled != true)
			{
				volume_array[i].checked = true;
			}
		}
	}

	else
	{
		for (i = 0;  i < volume_array.length;  i++)
		{
			volume_array[i].checked = false;
		}
	}
}

function select_all_checkboxes(form_name,para1,para2,para3)
{
	var check_all_option = document.getElementById(para1);
	var disk_array = document.forms[form_name].elements[para2];
	if (disk_array.length == undefined)
	{
		var delete_id = document.getElementById(para3);

		if (check_all_option.checked == true)
		{
			if (delete_id.disabled != true)
			{
				delete_id.checked = true;
			}
		}

		else
		{
			delete_id.checked = false;
		}
	}

	if (check_all_option.checked == true)
	{
		for (i = 0;  i < disk_array.length;  i++)
		{
			if (disk_array[i].disabled != true)
			{
				disk_array[i].checked = true;
			}
		}
	}

	else
	{
		for (i = 0;  i < disk_array.length;  i++)
		{
			disk_array[i].checked = false;
		}
	}
	show_input_textbox_multiple();
}

function select_all_disks()
{
	var check_all_option = document.getElementById('id_select_free_disks');
	var disk_array = document.add_volume.elements["volume_array[]"];
	
	if (disk_array.length == undefined)
	{
		var delete_id = document.getElementById('id_volume_array');

		if (check_all_option.checked == true)
		{
			if (delete_id.disabled != true)
			{
				delete_id.checked = true;
			}
		}

		else
		{
			delete_id.checked = false;
		}
	}

	if (check_all_option.checked == true)
	{
		for (i = 0;  i < disk_array.length;  i++)
		{
			if (disk_array[i].disabled != true)
			{
				disk_array[i].checked = true;
			}
		}
	}

	else
	{
		for (i = 0;  i < disk_array.length;  i++)
		{
			disk_array[i].checked = false;
		}
	}
	show_input_textbox_multiple();
}

function show_input_textbox()
{
	if(document.getElementById('x').type=='hidden')
	{
		document.getElementById('x').type='text';
	}

	/*else if(document.getElementById('x').type=='text')
	{
		document.getElementById('x').type='hidden';
	}*/

}

function show_input_textbox_multiple()
{
        if(document.getElementById('x').type=='hidden')
        {
                document.getElementById('x').type='text';
        }

        /*else if(document.getElementById('x').type=='text')
          {
                          document.getElementById('x').type='hidden';
                                  }*/

}

function confirm_delete_volume()
{
	var string = '';

	var volume_array = document.remove_vol.elements["used_volumes_array[]"];

	if (volume_array.length == null)
	{
		var volume_id    = document.getElementById('id_used_volumes');
		
		if (volume_id.checked != true)
		{
			alert('Please choose a volume to delete!');
			return false;
		}

		else
		{
			var response = confirm("Delete the volume ?");

			if (response == true)
			{
				string = volume_id.value;

				document.getElementById('wait').style.display = 'block';

				$.ajax(
				{
					type: 'POST',
					url: 'remove_volume.php',
					data: 'proceed_page=proceed&volume_string='+string,

					success: function(html)
					{
						$('#response').html(html);
					}
				});
			}
				
			else
			{
				alert('Action Canceled');
				return false;
			}
		}

	}

	else
	{
		for (i = 0;  i < volume_array.length;  i++)
		{
			if (volume_array[i].checked == true)
			{
				string = string + '@@@' + volume_array[i].value;
			}
		}

		if (string == '')
		{
			alert('Please choose a volume!');
			return false;
		}

		else
		{
			var response = confirm("Delete the volume ?");

			if (response == true)
			{
				document.getElementById('wait').style.display = 'block';

				$.ajax(
				{
					type: 'POST',
					url: 'remove_volume.php',
					data: 'proceed_page=proceed&volume_string='+string,

					success: function(html)
					{
						$('#response').html(html);
					}
				});
			}
				
			else
			{
				alert('Action Canceled');
				return false;
			}
		}
	}
}

function validate_create_vol_form()
{
	var string = '';

	var vol_array = document.add_volume.elements["volume_array[]"];
	var text_value = document.add_volume.elements["x"];
	var spacesExp = /[\s]/;
	
	if (vol_array.length == null)
	{
		var vol_id    = document.getElementById('id_volume_array');
		
		if (vol_id.checked != true)
		{
			alert('Please choose a volume!');
			return false;
		}
		else
		{
			string = vol_id.value;
		}
		if(text_value.value == 'Volume Name')
                {
                        alert('Please Enter Volume Name');
                        return false;
                }

		if(text_value.value.match(spacesExp))
		{
			alert('Spaces are not allowed!');
			return false;
		}
	}

	else
	{
		for (i = 0;  i < vol_array.length;  i++)
		{
			if (vol_array[i].checked == true)
			{
				string = string + '@@@' + vol_array[i].value;
			}
		}
		

		if (string == '')
		{
			alert('Please choose a volume!');
			return false;
		}

		if(text_value.value == 'Volume Name')
		{
			alert('Please Enter Volume Name');
			return false;
		}

		if(text_value.value.match(spacesExp))
                {
                        alert('Spaces are not allowed!');
                        return false;
                }
	}

	document.getElementById('wait').style.display = 'block';

	$.ajax(
	{
		type: 'POST',
		url: 'setup_diskmgr_add_volume.php',
		data: 'proceed_page=proceed&volume_string='+string,

		success: function(html)
		{
			$('#response').html(html);
		}
	});
}

function show_sub_options(type)
{
	var id1 = document.getElementById('id_raid_config');
	var id2 = document.getElementById('id_volume_config');
	var id3 = document.getElementById('id_pdrive_config');
	var id4 = document.getElementById('id_info_config');

	if (type == 'RAID')
	{
		id1.style.display = 'block';
		id2.style.display = 'none';
		id3.style.display = 'none';
		id4.style.display = 'none';
	}
	
	else if (type == 'VOLUME')
	{
		id1.style.display = 'none';
		id2.style.display = 'block';
		id3.style.display = 'none';
		id4.style.display = 'none';
	}

	else if (type == 'PDRIVE')
	{
		id1.style.display = 'none';
		id2.style.display = 'none';
		id3.style.display = 'block';
		id4.style.display = 'none';
	}

	else if (type == 'INFO')
	{
		id1.style.display = 'none';
		id2.style.display = 'none';
		id3.style.display = 'none';
		id4.style.display = 'block';
	}
}

function show_all()
{
	var id1 = document.getElementById('id_raid_config');
	var id2 = document.getElementById('id_volume_config');
	var id3 = document.getElementById('id_pdrive_config');
	var id4 = document.getElementById('id_info_config');

	id1.style.display = 'block';
	id2.style.display = 'block';
	id3.style.display = 'block';
	id4.style.display = 'block';
}

function hide_all()
{
	var id1 = document.getElementById('id_raid_config');
	var id2 = document.getElementById('id_volume_config');
	var id3 = document.getElementById('id_pdrive_config');
	var id4 = document.getElementById('id_info_config');

	id1.style.display = 'none';
	id2.style.display = 'none';
	id3.style.display = 'none';
	id4.style.display = 'none';
}

function show_repl_params()
{
	var repl_option = document.remote_repl.rem_repl.checked;
	var repl_table  = document.getElementById('id_repl_table');

	if (repl_option == true)
	{
		repl_table.style.display = 'table';
	}

	else
	{
		repl_table.style.display = 'none';
	}
}

function validate_repl_form(ip, device)
{
	if (ip == '' || device == '')
	{
		alert('All fields are required!');
		return false;
	}

	else
	{
		var ip_error = '';
		var ipPattern = /^([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})$/;

		var ip_array = ip.match(ipPattern);

		if (ip == "0.0.0.0")
		{
			ip_error = ip+' is not a valid IP';
		}
	
		else if (ip == "255.255.255.255")
		{
			ip_error = ip+' is not a valid IP';
		}

		else if (ip == "" && option == false)
		{
			ip_error = 'IP is required! Sorry!!';
		}
			
		if (ip_array == null)
		{
			ip_error = 'Please enter a valid IP';
		}

		else if (ip_array != null)
		{
			for (i = 1; i <= 4; i++)
			{
				thisSegment = ip_array[i];

				if (thisSegment > 255)
				{
					ip_error = ip+' is not a valid IP';
					i = 4;
				}
				
				if ((i == 0) && (thisSegment > 255))
				{
					ip_error = ip+' is not a valid IP';
					i = 4;
				}
			}
		}
	}

	if (ip_error != '')
	{
		alert(ip_error);
		return false;
	}
}

function change_values()
{
	var elem_count = document.remote_repl.elements.length;
	var id_raw_dev  = document.getElementById('id_raw_device');

	for (i = 0;  i < elem_count;  i++)
	{
		document.remote_repl.elements[i].disabled = false;
	}

	document.remote_repl.change_repl.disabled = true;
	id_raw_dev.style.visibility = 'hidden';
}

function show_table(id)
{
	var tables_array = document.getElementsByTagName('table');
	var browser_value = document.getElementById('id_browser_val').value;

	for (i in tables_array)
	{
		if (tables_array[i].id)
		{
			if (id == tables_array[i].id)
			{
				if (browser_value > 0)
				{
					tables_array[i].style.display = 'block';
				}

				else
				{
					tables_array[i].style.display = 'table';
				}
			}

			else
			{
				tables_array[i].style.display = 'none';
			}
		}
	}

	if (id == 'id_reset_acl')
	{
		//document.getElementById('id_acl_settings').style.display = 'table';
		document.getElementById('id_acl_settings').style.display = 'none';
	}

	if (id == 'fio_disk_conf')
	{
		get_dis = document.getElementById('show_fio_options').style.display;

		if(get_dis == 'none')
		{
			document.getElementById('show_fio_options').style.display = 'block';
			document.getElementById('show_fio_options2').style.display = 'block';
			document.getElementById('show_fio_options3').style.display = 'block';
			document.getElementById('show_fio_options4').style.display = 'block';
			document.getElementById('show_fio_list5').style.display = 'block';
		}
		else
		{
			document.getElementById('show_fio_options').style.display = 'none';
			document.getElementById('show_fio_options2').style.display = 'none';
			document.getElementById('show_fio_options3').style.display = 'none';
			document.getElementById('show_fio_options4').style.display = 'none';
			document.getElementById('show_fio_list5').style.display = 'none';

		}
	}


}

function show_on_click3(id)
{
        get_dis = document.getElementById('show_iscsi_options').style.display;
        
	 if (id == 'iscsi_config')
        {
                get_dis = document.getElementById('show_iscsi_options').style.display = 'block';

                if(get_dis == 'none')
                {
                        document.getElementById('show_iscsi_options').style.display = 'block';
			document.getElementById('show_dis_options').style.display = 'block';
                }
                else
                {
                        document.getElementById('show_iscsi_options').style.display = 'none';
			document.getElementById('show_dis_options').style.display = 'none';

                }
	}
}

function show_on_click4(id)
{
        get_dis = document.getElementById('show_iscsi_options1').style.display;


	if (id == 'show_target')
		{
			get_dis = document.getElementById('show_iscsi_options1').style.display;

			if(get_dis == 'none')
			{
				document.getElementById('show_iscsi_options1').style.display = 'block';
				document.getElementById('show_iscsi_options2').style.display = 'block';
			}
			else
			{
				document.getElementById('show_iscsi_options1').style.display = 'none';
				document.getElementById('show_iscsi_options2').style.display = 'none';

			}
		}



}


function show_on_clickfc(id)
{
        get_dis = document.getElementById('show_fc_options').style.display;


        if (id == 'show_target')
                {
                        get_dis = document.getElementById('show_fc_options').style.display;

                        if(get_dis == 'none')
                        {
                                document.getElementById('show_fc_options').style.display = 'block';
                                document.getElementById('show_fc_options1').style.display = 'block';
                        }
                        else
                        {
                                document.getElementById('show_fc_options').style.display = 'none';
                                document.getElementById('show_fc_options1').style.display = 'none';

                        }
                }



}


function show_on_clickfc1(id)
{
        get_dis = document.getElementById('show_fc_options3').style.display;
        if(id == 'disk_to_target')
        {
                if(get_dis == 'none')
                {
                        document.getElementById('show_fc_options2').style.display = 'block';
                        document.getElementById('show_fc_options3').style.display = 'block';
                }
                else
                {
                        document.getElementById('show_fc_options2').style.display = 'none';

                        document.getElementById('show_fc_options3').style.display = 'none';

                }
        }

}


function  show_on_clickfc2(id)
{
        get_dis = document.getElementById('show_fc_options4').style.display;


        if (id == 'show_prop')
                {
                        get_dis = document.getElementById('show_fc_options4').style.display;

                        if(get_dis == 'none')
                        {
                                document.getElementById('show_fc_options4').style.display = 'block';
                                document.getElementById('show_fc_options5').style.display = 'block';

                        }
                        else
                        {
                                document.getElementById('show_fc_options4').style.display = 'none';
                                document.getElementById('show_fc_options5').style.display = 'none';

                        }
                }



}




function show_on_clicksrp(id)
{
        get_dis = document.getElementById('show_srp_options').style.display;


        if (id == 'show_target')
                {
                        get_dis = document.getElementById('show_srp_options').style.display;

                        if(get_dis == 'none')
                        {
                                document.getElementById('show_srp_options').style.display = 'block';
                                document.getElementById('show_srp_options1').style.display = 'block';
                        }
                        else
                        {
                                document.getElementById('show_srp_options').style.display = 'none';
                                document.getElementById('show_srp_options1').style.display = 'none';

                        }
                }



}


function show_on_clicksrp1(id)
{
        get_dis = document.getElementById('show_srp_options2').style.display;
        if(id == 'disk_to_target')
        {
                if(get_dis == 'none')
                {
                        document.getElementById('show_srp_options2').style.display = 'block';
                        document.getElementById('show_srp_options3').style.display = 'block';
                }
                else
                {
                        document.getElementById('show_srp_options2').style.display = 'none';

                        document.getElementById('show_srp_options3').style.display = 'none';

                }
        }

}


function  show_on_clicksrp2(id)
{
        get_dis = document.getElementById('show_srp_options4').style.display;


        if (id == 'show_prop')
                {
                        get_dis = document.getElementById('show_srp_options4').style.display;

                        if(get_dis == 'none')
                        {
                                document.getElementById('show_srp_options4').style.display = 'block';
                                document.getElementById('show_srp_options5').style.display = 'block';

                        }
                        else
                        {
                                document.getElementById('show_srp_options4').style.display = 'none';
                                document.getElementById('show_srp_options5').style.display = 'none';

                        }
                }



}

function  show_on_click5(id)
{
        get_dis = document.getElementById('show_iscsi_options5').style.display;


        if (id == 'show_prop')
                {
                        get_dis = document.getElementById('show_iscsi_options5').style.display;

                        if(get_dis == 'none')
                        {
                                document.getElementById('show_iscsi_options5').style.display = 'block';
                                document.getElementById('show_iscsi_options6').style.display = 'block';
				document.getElementById('show_iscsi_options7').style.display = 'block';
				document.getElementById('show_iscsi_options8').style.display = 'block';
				document.getElementById('show_iscsi_options9').style.display = 'block';

                        }
                        else
                        {
                                document.getElementById('show_iscsi_options5').style.display = 'none';
                                document.getElementById('show_iscsi_options6').style.display = 'none';
				document.getElementById('show_iscsi_options7').style.display = 'none';
				document.getElementById('show_iscsi_options8').style.display = 'none';
				document.getElementById('show_iscsi_options9').style.display = 'none';

                        }
                }



}


function show_on_click(id)
{
	if(id == 'san_configuration')
	{
		get_dis_san = document.getElementById('show_fio_options11').style.display;
		if(get_dis_san == 'none')
		{
			document.getElementById('show_fio_options11').style.display = 'block';
			document.getElementById('show_fio_options12').style.display = 'block';
			document.getElementById('show_fio_options13').style.display = 'block';
		}
		else
		{
			document.getElementById('show_fio_options11').style.display = 'none';
			document.getElementById('show_fio_options12').style.display = 'none';
			document.getElementById('show_fio_options13').style.display = 'none';

		}
	}

	if(id == 'add_target_page')
	{
		get_add_tar = document.getElementById('show_add_tar_options11').style.display;
		if(get_add_tar == 'none')
		{
			document.getElementById('show_add_tar_options11').style.display = 'block';
			document.getElementById('show_add_tar_options12').style.display = 'block';
			document.getElementById('show_add_tar_options13').style.display = 'block';
			document.getElementById('plusandminus_main').innerHTML = '-';
		}
		else
		{
			document.getElementById('show_add_tar_options11').style.display = 'none';
			document.getElementById('show_add_tar_options12').style.display = 'none';
			document.getElementById('show_add_tar_options13').style.display = 'none';
			document.getElementById('plusandminus_main').innerHTML = '+';
			document.getElementById('show_iscsi_options11').style.display = 'none';
			document.getElementById('show_iscsi_options12').style.display = 'none';
			document.getElementById('show_iscsi_options13').style.display = 'none';
			document.getElementById('show_iscsi_options14').style.display = 'none';
			document.getElementById('plusandminus').innerHTML = '+';
			document.getElementById('show_fc_options11').style.display = 'none';
			document.getElementById('show_fc_options12').style.display = 'none';
			document.getElementById('show_fc_options13').style.display = 'none';
			document.getElementById('plusandminus_fc').innerHTML = '+';
			document.getElementById('show_src_options11').style.display = 'none';
			document.getElementById('show_src_options12').style.display = 'none';
			document.getElementById('show_src_options13').style.display = 'none';
			document.getElementById('plusandminus_src').innerHTML = '+';

		}
	}

	if(id == 'iscsi_options')
	{
		get_add_tar = document.getElementById('show_iscsi_options11').style.display;
		if(get_add_tar == 'none')
		{
			document.getElementById('show_iscsi_options11').style.display = 'block';
			document.getElementById('show_iscsi_options12').style.display = 'none';
			document.getElementById('show_iscsi_options13').style.display = 'block';
			document.getElementById('show_iscsi_options14').style.display = 'block';
			document.getElementById('plusandminus').innerHTML = '-';
		}
		else
		{
			document.getElementById('show_iscsi_options11').style.display = 'none';
			document.getElementById('show_iscsi_options12').style.display = 'none';
			document.getElementById('show_iscsi_options13').style.display = 'none';
			document.getElementById('show_iscsi_options14').style.display = 'none';
			document.getElementById('plusandminus').innerHTML = '+';

		}
	}

	if(id == 'fc_options')
	{
		get_add_tar = document.getElementById('show_fc_options11').style.display;
		if(get_add_tar == 'none')
		{
			document.getElementById('show_fc_options11').style.display = 'block';
			document.getElementById('show_fc_options12').style.display = 'block';
			document.getElementById('show_fc_options13').style.display = 'block';
			document.getElementById('plusandminus_fc').innerHTML = '-';
		}
		else
		{
			document.getElementById('show_fc_options11').style.display = 'none';
			document.getElementById('show_fc_options12').style.display = 'none';
			document.getElementById('show_fc_options13').style.display = 'none';
			document.getElementById('plusandminus_fc').innerHTML = '+';

		}
	}

	if(id == 'src_options')
	{
		get_add_tar = document.getElementById('show_src_options11').style.display;
		if(get_add_tar == 'none')
		{
			document.getElementById('show_src_options11').style.display = 'block';
			document.getElementById('show_src_options12').style.display = 'block';
			document.getElementById('show_src_options13').style.display = 'block';
			document.getElementById('plusandminus_src').innerHTML = '-';
		}
		else
		{
			document.getElementById('show_src_options11').style.display = 'none';
			document.getElementById('show_src_options12').style.display = 'none';
			document.getElementById('show_src_options13').style.display = 'none';
			document.getElementById('plusandminus_src').innerHTML = '+';

		}
	}
}

function show_on_click2(id)
{
	get_dis = document.getElementById('show_iscsi_options3').style.display;
	if(id == 'disk_to_target')
	{
		if(get_dis == 'none')
		{
			document.getElementById('show_iscsi_options3').style.display = 'block';
			document.getElementById('show_iscsi_options4').style.display = 'block';
		}
		else
		{
			document.getElementById('show_iscsi_options3').style.display = 'none';

			document.getElementById('show_iscsi_options4').style.display = 'none';

		}
	}

}


function validate_raidset_form()
{
	var disks_val = document.raid_set_form.elements["disks[]"];
	var id = document.getElementById('id_disks');
	var flag;

	flag = 0;

	if (disks_val.length == null)
	{
		if (id.checked == true)
		{
			flag = 1;
		}

		else
		{
			flag = 0;
		}
	}

	else
	{
		for (i = 0;  i < disks_val.length;  i++)
		{
			if (disks_val[i].checked == true)
			{
				flag = 1;
			}
		}
	}

	if (flag == 0)
	{
		//alert('Please choose atleast one disk!');
		 jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:6%; padding-top: 4%; font-family: status-bar;">Please choose atleast one disk.</div>', 'Alert Dialog');
		return false;
	}
}

function cancel_action()
{
	location.href = 'raid_fc_info.php?fp=raidset_create';
}

function confirm_delete_raidset()
{
	var options_array  = document.getElementsByName('raid_set');
	var options_string = '';

	for (i = 0;  i < options_array.length;  i++)
	{
		if (options_array[i].checked)
		{
			options_string += options_array[i].value;
		}
	}

	if (options_string == '')
	{
		//alert('You need to choose a raid set to delete!');
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:6%; padding-top: 4%; font-family: status-bar;">You need to choose a raid set to delete.</div>', 'Alert Dialog');
		return false;
	}

	var response = confirm('Please make sure that this RAID set is NOT in use! Data once lost can not be recovered! Do you still want to proceed?');

	if (response == true)
	{
		var response1 = confirm('Do you really wish to delete this RAID set?');

		if (response1 == true)
		{
			document.raid_set_delete_form.submit();
		}

		else
		{
			return false;
		}
	}

	else
	{
		return false;
	}
}

function validate_expand_raidset()
{
	var options_array  = document.getElementsByName('raid_set');
	var disks_val      = document.raid_set_form.elements["disks[]"];
	var id             = document.getElementById('id_disks');
	var flag;
	var options_string = '';

	flag = 0;

	for (i = 0;  i < options_array.length;  i++)
	{
		if (options_array[i].checked)
		{
			options_string += options_array[i].value;
		}
	}

	if (options_string == '')
	{
		//alert('You need to choose a raidset!');
		 jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:6%; padding-top: 4%; font-family: status-bar;">You need to choose a raidset.</div>', 'Alert Dialog');
		return false;
	}

	if (disks_val.length == null)
	{
		if (id.checked == true)
		{
			flag = 1;
		}

		else
		{
			flag = 0;
		}
	}

	else
	{
		for (i = 0;  i < disks_val.length;  i++)
		{
			if (disks_val[i].checked == true)
			{
				flag = 1;
			}
		}
	}

	if (flag == 0)
	{
		//alert('Please choose atleast one disk!');
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:6%; padding-top: 4%; font-family: status-bar;">Please choose atleast one disk.</div>', 'Alert Dialog');
		return false;
	}

	else
	{
		var response = confirm('After adding the disks to the RAID set, you CAN NOT detach the disks from the RAID set, unless you delete the RAID set completely. Do you want to continue?');

		if (response == true)
		{
			document.raid_set_form.submit();
		}

		else
		{
			return false;
		}
	}
}

function validate_hotspare_form()
{
	var disks_val = document.raid_set_form.elements["disks[]"];
	var id = document.getElementById('id_disks');
	var flag;

	flag = 0;

	if (disks_val.length == null)
	{
		if (id.checked == true)
		{
			flag = 1;
		}

		else
		{
			flag = 0;
		}
	}

	else
	{
		for (i = 0;  i < disks_val.length;  i++)
		{
			if (disks_val[i].checked == true)
			{
				flag = 1;
			}
		}
	}

	if (flag == 0)
	{
		//alert('Please choose atleast one disk!');
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:6%; padding-top: 4%; font-family: status-bar;">Please choose atleast one disk.</div>', 'Alert Dialog');
		return false;
	}
}

function validate_del_hotspare_form()
{
	var disks_val = document.raid_set_form.elements["disks[]"];
	var id = document.getElementById('id_disks');
	var flag;

	flag = 0;

	if (disks_val.length == null)
	{
		if (id.checked == true)
		{
			flag = 1;
		}

		else
		{
			flag = 0;
		}
	}

	else
	{
		for (i = 0;  i < disks_val.length;  i++)
		{
			if (disks_val[i].checked == true)
			{
				flag = 1;
			}
		}
	}
	
	if (flag == 0)
	{
		//alert('Please choose atleast one disk!');
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:6%; padding-top: 4%; font-family: status-bar;">Please choose atleast one disk.</div>', 'Alert Dialog');
		return false;
	}
}

function size_for_raid_level(raid_set_id)
{
	var raid_level = document.volume_set_create_form.raid_levels.value;
	var init_id = document.getElementById('id_init');
	var strp_id = document.getElementById('id_strp_size');

	document.volume_set_create_form.action = 'find_raid_level_size.php?rd_lv='+raid_level+'&raid_id='+raid_set_id;
	document.volume_set_create_form.submit();

	if (raid_level != 0)
	{
		init_id.disabled = false;
	}

	else
	{
		init_id.disabled = true;
	}

	if (raid_level == 3)
	{
		strp_id.disabled = true;
	}

	else
	{
		strp_id.disabled = false;
	}
}

function validate_volumeset_creation()
{
	var vol_size = document.volume_set_create_form.vol_capacity.value;
	var max_size = document.volume_set_create_form.max_cap_allow.value;

	if (vol_size == '' || vol_size == 0 || parseInt(vol_size) > parseInt(max_size))
	{
		document.volume_set_create_form.vol_capacity.value = document.volume_set_create_form.max_cap_allow.value;
		document.volume_set_create_form.submit();
	}
}

function show_luns_for_scsi_id()
{
	var elem_count = document.volume_set_create_form.elements.length;
	var elements_string = '';

	for (i = 0;  i < elem_count;  i++)
	{
		elements_string = elements_string + ':' + document.volume_set_create_form.elements[i].value;
	}

	document.volume_set_create_form.action = 'show_luns_for_scsi_id.php?form_string='+elements_string;
	document.volume_set_create_form.submit();
}

function confirm_delete_volumeset()
{
	var options_array  = document.getElementsByName('raid_set');
	var options_string = '';
	
	for (i = 0;  i < options_array.length;  i++)
	{
		if (options_array[i].checked)
		{
			options_string += options_array[i].value;
		}
	}

	if (options_string == '')
	{
		//alert('You need to choose a volume set!');
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:6%; padding-top: 4%; font-family: status-bar;">You need to choose a volume set.</div>', 'Alert Dialog');
		return false;
	}

	var response = confirm('Please make sure that this volume set is NOT in use! Data once lost can not be recovered! Do you still want to proceed?');

	if (response == true)
	{
		var response1 = confirm('Do you really wish to delete this volume set?');

		if (response1 == true)
		{
			document.raid_set_delete_form.submit();
		}

		else
		{
			return false;
		}
	}

	else
	{
		return false;
	}
}

function show_luns_for_pt_scsi_id()
{
	var elem_count = document.volume_set_create_form.elements.length;
	var elements_string = '';

	for (i = 0;  i < elem_count;  i++)
	{
		elements_string = elements_string + ':' + document.volume_set_create_form.elements[i].value;
	}

	document.volume_set_create_form.action = 'pass_thru_luns_for_scsi_id.php?form_string='+elements_string;
	document.volume_set_create_form.submit();
}

function confirm_delete_passthrough()
{
	var options_array  = document.getElementsByName('raid_set');
	var options_string = '';

	for (i = 0;  i < options_array.length;  i++)
	{
		if (options_array[i].checked)
		{
			options_string += options_array[i].value;
		}
	}

	if (options_string == '')
	{
		//alert('You need to choose a passthrough!');	
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:6%; padding-top: 4%; font-family: status-bar;">You need to choose a passthrough</div>', 'Alert Dialog');
		return false;
	}

	var response = confirm('Please make sure that this pass-through disk is NOT in use! Data once lost can not be recovered! Do you still want to proceed?');

	if (response == true)
	{
		var response1 = confirm('Do you really wish to delete this pass-through disk?');

		if (response1 == true)
		{
			document.raid_set_delete_form.submit();
		}

		else
		{
			return false;
		}
	}

	else
	{
		return false;
	}
}

function proceed_to_modify_passthrough(disk, disk_id)
{
	document.raid_set_delete_form.action = 'main.php?page=pm&disk='+disk+'&did='+disk_id;
	document.raid_set_delete_form.submit();
}

function show_luns_for_pass_scsi_id()
{
	var elem_count = document.volume_set_create_form.elements.length;
	var elements_string = '';

	for (i = 0;  i < elem_count;  i++)
	{
		elements_string = elements_string + ':' + document.volume_set_create_form.elements[i].value;
	}

	document.volume_set_create_form.action = 'passthru_luns_for_scsi_id.php?form_string='+elements_string;
	document.volume_set_create_form.submit();
}

function show_modal_window(id)
{
	window.showModalDialog("stop_blinking.php?drv="+id, "Info", "dialogWidth: 750px; dialogHeight: 150px");
}

function enable_append_mode()
{
        disable_all_other_forms('share_append');
        var mode = document.share_append.use_append_mode.checked;
	var path = document.share_append.hid_path.value;

        document.getElementById('wait').style.display = 'block';

	location.href = 'enable_append_mode.py?mode='+mode+'&path='+path;

        /*$.ajax(
        {
                type: 'POST',
                url: 'enable_append_mode.py',
                data: 'mode='+mode+'&hid_share='+document.share_append.hid_share.value+'&hid_path='+document.share_append.hid_path.value,

                success: function(html)
                {
                        $('#response').html(html);
                }
        });*/
}

function select_all_shares()
{
	var check_all_option = document.getElementById('id_select_all');
	var share_array = document.share_maintenance.elements["delete_share[]"];

	if (share_array.length == undefined)
	{
		var delete_id = document.getElementById('id_del_share');

		if (check_all_option.checked == true)
		{
			if (delete_id.disabled != true)
			{
				delete_id.checked = true;
			}
		}

		else
		{
			delete_id.checked = false;
		}
	}

	if (check_all_option.checked == true)
	{
		for (i = 0;  i < share_array.length;  i++)
		{
			if (share_array[i].disabled != true)
			{
				share_array[i].checked = true;
			}
		}
	}

	else
	{
		for (i = 0;  i < share_array.length;  i++)
		{
			share_array[i].checked = false;
		}
	}
}
	
function validate_delete_share()
{
	var string = '';

	var share_array = document.share_maintenance.elements["delete_share[]"];

	if (share_array.length == null)
	{
		var share_id    = document.getElementById('id_del_share');
					
		if (share_id.checked != true)
		{
			//alert('Please choose a share to delete!');
			jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:6%; padding-top: 4%; font-family: status-bar;">Please Choose a share to delete!</div>', 'Alert Dialog');
			return false;
		}

		else
		{
			string = share_id.value;
		}
	}

	else
	{
		for (i = 0;  i < share_array.length;  i++)
		{
			if (share_array[i].checked == true)
			{
				string = string + '@@@' + share_array[i].value;
			}
		}

		if (string == '')
		{
			alert('Please choose a share to delete!');
			return false;
		}
	}

	document.getElementById('del_wait').style.display = 'block';
	document.getElementById('id_delshare').style.background = '#2E2E2E';
	document.getElementById('id_delshare').style.color = '#fff';

	if (string.indexOf('@@@') >= 0)
	{
		string = string.substr(string.indexOf("@@@") + 3, string.length);
	}

	$.ajax(
	{
		type: 'POST',
		url: 'delete_share.py',
		data: 'str='+string,

		success: function(html)
		{
			$('#response_wait').html(html);
		}
	});
}

function validate_ip_addr(ip, option)
{
	ip_error = '';

	var ipPattern;
	
	if (option == true)
	{
		if (ip == '')
		{
			ip_error = 'Nothing to unconfigure!';
		}

		ipPattern = /^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$|^$/;
	}

	else
	{
		if (ip == '')
		{
			ip_error = 'Please enter a valid IP!';
		}

		ipPattern = /^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/;
	}

	var ip_array = ip.match(ipPattern);

	if (ip == "0.0.0.0")
	{
		ip_error = ip+' is not a valid IP';
	}
	
	else if (ip == "255.255.255.255")
	{
		ip_error = ip+' is not a valid IP';
	}

	else if (ip == "" && option == false)
	{
		ip_error = 'IP is required! Sorry!!';
	}
		
	if (ip_array == null)
	{
		ip_error = 'Please enter a valid IP';
	}

	else if (ip_array != null)
	{
		for (i = 1; i <= 4; i++)
		{
			thisSegment = ip_array[i];

			if (thisSegment > 255)
			{
				ip_error = ip+' is not a valid IP';
				i = 4;
			}
			
			if ((i == 0) && (thisSegment > 255))
			{
				ip_error = ip+' is not a valid IP';
				i = 4;
			}
		}
	}

	return ip_error;
}

function validate_netmask(netmask, option)
{
	netmask_error = '';
	var ipPattern;
	
	if (option == true)
	{
		ipPattern = /^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$|^$/;
	}

	else
	{
		if (netmask == '')
		{
			netmask_error = 'Please enter a valid value for netmask!';
		}

		ipPattern = /^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/;
	}

	var netmask_array = netmask.match(ipPattern);

	if (netmask == "0.0.0.0")
	{
		netmask_error = netmask+' is not a valid IP';
	}
	
	else if (netmask == "255.255.255.255")
	{
		netmask_error = netmask+' is not a valid IP';
	}

	else if (netmask == "" && option == false)
	{
		netmask_error = 'IP is required! Sorry!!';
	}
		
	if (netmask_array == null)
	{
		netmask_error = 'Enter a valid IP for netmask';
	}

	else if (netmask_array != null)
	{
		for (i = 1; i <= 4; i++)
		{
			thisSegment = netmask_array[i];

			if (thisSegment > 255)
			{
				netmask_error = netmask+' is not a valid IP';
				i = 4;
			}
			
			if ((i == 0) && (thisSegment > 255))
			{
				netmask_error = netmask+' is not a valid IP';
				i = 4;
			}
		}
	}

	return netmask_error;
}

function validate_gateway(gateway)
{
	gateway_error = '';

	var ipPattern;
	
	ipPattern = /^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$|^$/;

	var gateway_array = gateway.match(ipPattern);

	if (gateway == "0.0.0.0")
	{
		gateway_error = gateway+' is not a valid IP';
	}
	
	else if (gateway == "255.255.255.255")
	{
		gateway_error = gateway+' is not a valid IP';
	}
		
	if (gateway_array == null)
	{
		gateway_error = gateway+' is not a valid IP';
	}

	else if (gateway_array != null)
	{
		for (i = 1; i <= 4; i++)
		{
			thisSegment = gateway_array[i];

			if (thisSegment > 255)
			{
				gateway_error = gateway+' is not a valid IP';
				i = 4;
			}
			
			if ((i == 0) && (thisSegment > 255))
			{
				gateway_error = gateway+' is not a valid IP';
				i = 4;
			}
		}
	}

	return gateway_error;
}

function validate_ethernet_form()
{
	var ip = document.change_network.ipaddress.value;
	var nm = document.change_network.netmask.value;
	var gw = document.change_network.gateway.value;
	var device = document.change_network.hid_device.value;
	var hid_ip = document.change_network.hid_ip_add.value;
	var server_ip = document.change_network.hid_server_ip.value;
	var gn = document.change_network.gateway.name;
	var eth_status = document.change_network.hid_status.value;

	var unconfigure;
	var option;
	var response;

	device_pattern = /^bond/;

	var device_val = device.match(device_pattern);


	if (server_ip != ip && device_val != 'bond')
	{
		unconfigure = document.change_network.unconfigure.checked;
	}

	if (gn == 'gateway' && gw != '')
	{
		response = confirm('This IP in gateway field will be set as gateway for all the eth devices. Proceed?');

		if (response == false)
		{
			return false;
		}
	}

	/*if (ip == hid_ip)
	{
		alert('This IP is already assigned for eth0!');
		return false;
	}*/

	ip_error      = validate_ip_addr(ip, option);
	netmask_error = validate_netmask(nm, option);
	gateway_error = validate_gateway(gw);

	if (ip_error != '')
	{
		alert(ip_error);
		return false;
	}

	else if (netmask_error != '')
	{
		alert(netmask_error);
		return false;
	}

	else if (gateway_error != '')
	{
		alert(gateway_error);
		return false;
	}

	else
	{
		document.getElementById('wait').style.display = 'block';

		$.ajax(
		{
			type: 'POST',
			url: 'change_network.php',
			data: 'hid_device='+document.change_network.hid_device.value+'&ipaddress='+document.change_network.ipaddress.value+'&netmask='+document.change_network.netmask.value+'&gateway='+document.change_network.gateway.value+'&action_but='+document.change_network.action_but.value+'&unconfigure='+unconfigure+'&old_ip_val='+document.change_network.old_ip_val.value,

			success: function(html)
			{
				$('#response').html(html);
			}
		});
	}

	document.change_network.ipaddress.disabled  = false;
	document.change_network.netmask.disabled    = false;
	document.change_network.gateway.disabled    = false;
	document.change_network.action_but.disabled = true;
}

function enable_apply_button()
{
        document.getElementById('id_apply_but').disabled = false;
}

function ip_validation_func(dns)
{
		var ipPattern;

                ipPattern = /^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/;

                var dns_array = dns.match(ipPattern);

                if (dns == "0.0.0.0")
                {
                        dns_error = dns+' is not a valid IP';
                }

                else if (dns == "255.255.255.255")
                {
                        dns_error = dns+' is not a valid IP';
                }

                else if (dns == "")
                {
                        dns_error = 'IP is required! Sorry!!';
                }

                if (dns_array == null)
                {
                        dns_error = dns+' is not a valid IP';
                }

                else if (dns_array != null)
                {
                        for (i = 1; i <= 4; i++)
                        {
                                thisSegment = dns_array[i];

                                if (thisSegment > 255)
                                {
                                        dns_error = dns+' is not a valid IP';
                                        i = 4;
                                }
				
				if ((i == 0) && (thisSegment > 255))
                                {
                                        dns_error = dns+' is not a valid IP';
                                        i = 4;
                                }
                        }
                }

		return dns_error;

}


function validate_dns_conf()
{
	var pdns = document.dns_form.pdns.value;
	var sdns = document.dns_form.sdns.value;


	if(sdns != '')
		{
			if(pdns == '')
			{
				jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:2%; padding-top: 4%; font-family: status-bar;">Please Enter a primary DNS!</div>', 'Alert Dialog');
				return false;
			}
		}
 
}


/*function change_title()
{
	var title = document.change_network.edit_default.value;
	var old_ip_val = document.change_network.old_ip_val.value;
	var old_nm_val = document.change_network.old_nm_val.value;
	var old_gw_val = document.change_network.old_gw_val.value;

	if (title == 'Edit')
	{
		document.change_network.ipaddress.disabled = false;
		document.change_network.netmask.disabled = false;
		document.change_network.gateway.disabled = false;
		document.change_network.ipaddress.focus();
		document.change_network.edit_default.value = 'Keep old values';
		document.change_network.action_but.disabled = false;
		return false;
	}

	else if (title == 'Keep old values')
	{
		document.change_network.ipaddress.value = old_ip_val;
		document.change_network.netmask.value = old_nm_val;
		document.change_network.gateway.value = old_gw_val;
		document.change_network.ipaddress.disabled = true;
		document.change_network.netmask.disabled = true;
		document.change_network.gateway.disabled = true;
		document.change_network.edit_default.value = 'Edit';
		document.change_network.action_but.disabled = true;
		return false;
		window.close();
	}
}*/

function enable_apply_butt()
{
	var option = document.change_network.unconfigure.checked;

	if (option == true)
	{
		document.change_network.action_but.disabled = false;
	}

	else
	{
		document.change_network.action_but.disabled = true;
	}
}

function show_hide_file_dir() 
{
	var click_val    = document.user_share.use_manual.checked;
	var dir_list_val = document.getElementById('dir_list');
	var share_name   = document.user_share.share.value;

	if (click_val == true)
	{
		dir_list_val.style.display = 'block';
					
		var share   = document.user_share.share.value;
		var comment = document.user_share.comment.value;

		document.user_share.action = 'show_dir.py?sh='+share+'&com='+comment+'&use_manual=true';
		document.user_share.target = 'directories';
		document.user_share.submit();
	}

	else
	{
		dir_list_val.style.display = 'none';
		location.href = 'iframe_nas_settings.py';
	}
}

function update_path()
{
	var manual_clicked = document.user_share.use_manual.checked;

	if (manual_clicked != true)
	{
		var path_name  = '';
		var share_name = document.user_share.share.value;
		path_name      = document.user_share.path.value;

		path_array = new Array();

		path_array = path_name.split('/');
		storage_disk = path_array[0] + '/';

		var path_name_1 = storage_disk + share_name;
		document.user_share.path.value = path_name_1;
	}
				
	else if (manual_clicked == true)
	{
		var path_name  = '';
		var share_name = document.user_share.share.value;
		path_name      = document.user_share.path.value;

		path_array = new Array();

		path_array = path_name.split('/');
		storage_disk = path_array[0] + '/';

		var path_name_1 = storage_disk;
		document.user_share.path.value = path_name_1;
	}
}

function validate_add_share_form()
{
	var share_val  = document.user_share.share.value;
	var share_path = document.user_share.path.value;
	var sp_chars   = "\ \ !@#$%^&*()+=-[]\\\';,/{}|\":<>?`~";

	var dot_index  = share_val.indexOf('.');
	var line_index = share_val.indexOf('_');

	if (share_val.indexOf('storage') == 0 || share_val.indexOf('disk') == 0)
	{
		alert('Use a different name for share other than \'storage\' and \'disk\'');
		//jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:6%; padding-top: 4%; font-family: status-bar;">Please use a different name for share.</div>', 'Alert Dialog');
		document.user_share.share.focus();
		return false;
	}

	if (dot_index == 0 || line_index == 0)
	{
		alert('Share name should start with alpha numeric!');
		//jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:6%; padding-top: 4%; font-family: status-bar;">Share name should start with alpha numeric!</div>', 'Alert Dialog');
		return false;
	}

	if (share_val.length == 1 || share_val == '')
	{
		alert('Please enter a valid share name!');
		return false;
		//jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:6%; padding-top: 4%; font-family: status-bar;">Please enter a valid share name!</div>', 'Alert Dialog');
	}

	if (share_val.length > 24)
	{
		alert('Share name cannot be more than 24 characters!');
		return false;
	}

	var use_manual = document.user_share.use_manual.checked;

	if (use_manual == true)
	{
		for (var i = 0;  i < share_val.length;  i++)
		{
			if (sp_chars.indexOf(share_val.charAt(i)) != -1)
			{
				alert('Please enter a valid share name. Double spaces and special characters not allowed!');
				//jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:6%; padding-top: 4%; font-family: status-bar;">Please enter a valid share name. Double spaces and special characters not allowed!</div>', 'Alert Dialog');
				document.user_share.share.value = '';
				document.user_share.share.focus();
				return false;
			}
		}

		var response = confirm ("Do you want to create a new folder with this share name, in the choosen path, or do you want to make the choosen folder as a shared folder? Click 'OK' to create a new folder with the given share name or click 'Cancel' to use the existing path as a share.");

		if (response == true)
		{
			var response1 = confirm("Proceed with share creation? Click 'OK' to continue, click 'Cancel' to go back.");
			if (response1 == true)
			{
				new_share_path = share_path + '/' + share_val;
				new_share_path = new_share_path.replace('//', '/');
				document.user_share.path.value = new_share_path;
				document.getElementById('wait').style.display = 'block';

				document.user_share.action = 'add_share.py';
				document.user_share.submit();
			}

			else
			{
				return false;
			}
		}

		else
		{
			var response1 = confirm("Proceed with share creation? Click 'OK' to continue, click 'Cancel' to go back.");

			if (response1 == true)
			{
				new_share_path = share_path;
				new_share_path = new_share_path.replace('//', '');
				document.user_share.path.value = new_share_path;

				document.user_share.action = 'add_share.py';
				document.user_share.submit();
			}
				
			else
			{
				return false;
			}
		}
	}

	else
	{
		for (var i = 0;  i < share_val.length;  i++)
		{
			if (sp_chars.indexOf(share_val.charAt(i)) != -1)
			{
				//alert('Please enter a valid share name. Double spaces and special characters other than \'.\' and \'_\' are not allowed!');
				//alert("Spaces and special characters other than '.' and '_' are not allowed.");
				jAlert('<img src="../images/info.gif"><div style="float: right; margin-left:49px; margin-top:-4%; font-family: status-bar;">Please enter a valid share name. Spaces and special characters other than "." and "_" are not allowed.</div>', 'Share Dialog');
				return false;
			}
		}

		document.getElementById('wait').style.display = 'block';
		$.ajax(
		{
			type: 'POST',
			url: 'add_share.php',
			data: 'share='+share_val+'&path='+share_path+'&comment='+document.user_share.comment.value+'&hid_share_page='+document.user_share.hid_share_page.value,

			success: function(html)
			{
				$('#response').html(html);
			}
		});
	}

	/*document.user_share.submit();
	document.user_share.action = '../py/add_share.py';*/

	document.user_share.action_but.disabled = true;
	document.user_share.cancel_but.disabled = true;
}

function show_users_list()
{
	var user_option_array = document.getElementsByName('user');
	var user_list  = document.getElementById('id_user_list');
	var group_list = document.getElementById('id_group_list');
        var gtextboxid = document.getElementById('quota_available_groups');
        var gbuttonid  = document.getElementById('id_gbutton');
        var utextboxid = document.getElementById('quota_available');
        var ubuttonid  = document.getElementById('id_ubutton');

	for (i = 0;  i < user_option_array.length;  i++)
	{
		if (user_option_array[i].checked)
		{
			if (user_option_array[i].value == 'user')
			{
				user_list.style.visibility  = 'visible';

                                if (utextboxid != null)
                                {
                                        utextboxid.style.visibility = 'visible';
                                        ubuttonid.style.visibility  = 'visible';
	                        }

				group_list.style.display = 'none';

                                if (gtextboxid != null)
                                {
                                        gtextboxid.style.display = 'none';
                                        gbuttonid.style.display  = 'none';
                                }
			}

			else
			{
				user_list.style.visibility  = 'hidden';

                                if (utextboxid != null)
                                {
                                        utextboxid.style.visibility = 'hidden';
                                        ubuttonid.style.visibility  = 'hidden';
                                }

				group_list.style.display = 'table';

                                if (gtextboxid != null)
                                {
                                        gtextboxid.style.display = 'block';
                                        gbuttonid.style.display  = 'block';
                                }
			}
		}
	}
}

function show_search_users_list()
{
	var user_option_array = document.getElementsByName('search_user');
	var user_list  = document.getElementById('id_search_user_list');
	var group_list = document.getElementById('id_search_group_list');
        var userbutt   = document.getElementById('id_subutton');
        var groupbutt  = document.getElementById('id_sgbutton');
	var table_id   = document.getElementById('id_results_table');

	for (i = 0;  i < user_option_array.length;  i++)
	{
		if (user_option_array[i].checked)
		{
			table_id.style.display   = 'none';

			if (user_option_array[i].value == 'all')
			{
				user_list.style.display  = 'none';
				group_list.style.display = 'none';
			}

			else if (user_option_array[i].value == 'user')
			{
				user_list.style.display  = 'block';

				if (userbutt != null)
				{
					userbutt.style.display = 'table';
				}

				group_list.style.display = 'none';

				if (groupbutt != null)
				{
					groupbutt.style.display = 'none';
				}
			}

			else
			{
				user_list.style.display  = 'none';

				if (userbutt != null)
				{
					userbutt.style.display  = 'none';
				}

				group_list.style.display = 'block';

				if (groupbutt != null)
				{
					groupbutt.style.display = 'table';
				}
			}
		}
	}
}

function validate_user_quota_form()
{
	var disk_size = document.user_quota.disk_size.value;

	var user_var = '';
	var group_var = '';

	var quota_users  = document.user_quota.elements["grant_users[]"].value;
        var quota_groups = document.user_quota.elements["grant_groups[]"].value;

	if (quota_users.length == 0 && quota_groups.length == 0)
	{
		//alert('You must choose either USERS or GROUPS!');
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:5%; padding-top: 4%; font-family: status-bar;">You must choose either Users or Groups</div>', 'Quota Alert ');
		return false;
	}

	if (disk_size == '')
	{
		//alert('Please enter a valid size!');
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:19%; padding-top: 4%; font-family: status-bar;">Please enter a valid size</div>', 'Quota Alert ');
		return false;
	}

	else
	{
		var disk_size_pattern = /^([0-9]{1,8})\.([0-9]{1,8})|([0-9]{1,8})$/;
		disk_size_array = disk_size.match(disk_size_pattern);

		if (disk_size_array == null)
		{
			alert('Please enter a valid size!');
			document.user_quota.disk_size.value = '';
			document.user_quota.disk_size.focus();
			return false;
		}
	}

	document.getElementById('wait').style.display = 'block';

	/*$.ajax(
	{
		type: 'POST',
		url: 'add_user_quota.py',
		data: 'proceed_page=proceed&user_list='+u_string+'&group_list='+g_string+'&disk_size='+disk_size+'&user='+user_var,

		success: function(html)
		{
			$('#response').html(html);
		}
	});*/
	
	document.user_quota.submit();
	document.user_quota.conf.disabled = true;
	disable_all_other_forms('user_quota');
}

function validate_search_quota(button_value, user_value, usergroup)
{
	if (user_value == '' || user_value == null)
	{
		user_value = 'all';
	}

	var user_options = document.getElementsByName('search_user');

	document.search_user_quota.delete_search.value = button_value;
	document.search_user_quota.ugtext.value = usergroup;

	user_text  = '';
	group_text = '';

	if (usergroup == 'user')
	{
		user_text = user_value;
	}

	if (usergroup == 'group')
	{
		group_text = user_value;
	}

	if (button_value == 'Delete Quota')
	{
		var volume_id = document.getElementById('id_del_quota');
		
		if (volume_id.checked != true)
		{
			//alert('Please choose a user/group to delete!');
			jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:19%; padding-top: 4%; font-family: status-bar;">You need to select a user/group to delete</div>', 'Quota Alert ');
			return false;
		}
		/*
		count = 0;

		var delete_options = document.search_user_quota.elements["delete_option[]"].length;
		alert(delete_options);

		for (i = 0;  i <= delete_options;  i++)
		{
			if (document.search_user_quota.elements["delete_option[]"][i].checked == true)
			{
				count ++;
			}
		}

		alert(count);
		if (count == 0)
		{
			//alert('You need to select a user/group to delete !');
			jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:19%; padding-top: 4%; font-family: status-bar;">You need to select a user/group to delete</div>', 'Quota Alert ');
			return false;
		}
		*/
		for (i = 0;  i < user_options.length;  i++)
		{
			if (user_options[i].checked)
			{
				if (user_options[i].value == 'all')
				{
					user_str = 'all';
				}

				else if (user_options[i].value == 'user')
				{
					user_str = 'user';

					if (user_value == '')
					{
						//alert('Please choose a user!');
						jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:19%; padding-top: 4%; font-family: status-bar;">Please choose a user</div>', 'Quota Alert ');
						return false;
					}
				}

				else if (user_options[i].value == 'group')
				{
					user_str = 'group';

					if (group_value == '')
					{
						//alert('Please choose a group!');
						jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:19%; padding-top: 4%; font-family: status-bar;">Please choose a Group</div>', 'Quota Alert ');
						return false;
					}
				}
			}
		}
	}

	var hidvalue = '';

	document.getElementById('wait').style.display = 'block';
	
	/*$.ajax(
	{
		type: 'POST',
		url: 'search_user_quota.py',
		data: 'proceed_page=proceed&user_list='+user_value+'&group_list='+group_value+'&hid_action='+button_value+'&hid_user_text='+document.search_user_quota.hid_user_text.value+'&hid_user_parm='+hidvalue+'&search_user='+user_str+'&ut='+user_text+'&gt='+group_text,

		success: function(html)
		{
			$('#response').html(html);
		}
	});*/

	document.search_user_quota.submit();
	document.search_user_quota.search.disabled = true;
	disable_all_other_forms('search_user_quota');
}

function change_button_lable()
{
	document.search_user_quota.search.value = 'Show Details';
	document.search_user_quota.hid_action.value = 'Show Details';
}

function show_shares_path(path, dots, dir)
{
	if (dir == '/storage')
	{
		dir = path;
	}

	if (path.indexOf('/storage/') == 0)
	{
		path = path.replace('/storage/', '');
	}

	if (path == '')
	{
		path = dir + '/';
	}

	if (dots == 'dots')
	{
		if (path == dir)
		{
			var nasdisk = parent.document.user_share.hid_nas_disk.value;
			path = nasdisk + '/';
		}

		path = path.substr(0, path.lastIndexOf('/') + 1);
					
		if (path == '')
		{
			path = dir + '/';
		}
	}

	parent.document.user_share.path.value = path;
	return true;
}

function set_allow_ip_focus()
{
	document.nfs_snapshot.allow_ip.focus();
}
				
function validate_allow_access_ip(access_ip_val)
{
	error = '';
	
	access_ip_array = access_ip_val.split(',');
				
	for (i = 0;  i < access_ip_array.length;  i++)
	{
		var ipPattern = /^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$|^\*$/;
		var accessip_array = access_ip_array[i].match(ipPattern);

		if (access_ip_array[i] == '0.0.0.0' || access_ip_array[i] == '255.255.255.255')
		{
			error = access_ip_array[i]+' is not a valid IP!';
		}
					
		if (accessip_array == null)
		{
			error = 'Please enter a valid IP!';
		}
						
		else
		{
			for (j = 1;  j < accessip_array.length;  j++)
			{	
				if (accessip_array[j] > 255)
				{
					error = access_ip_array[i]+' is not a valid IP!';
				}
			}
		}
	}

	if (error != '')
	{
		alert(error);
		return false;
	}

	else
	{
		document.getElementById('wait').style.display = 'block';
	
		$.ajax(
		{
			type: 'POST',
			url: 'snapshot_access.php',
			data: 'hid_snapshot='+document.nfs_snapshot.hid_snapshot.value+'&allow_ip='+document.nfs_snapshot.allow_ip.value,
			success: function(html)
			{
				$('#response').html(html);
			}
		});
	}
}

function get_authorized_users(share, comment)
{
	var path_for_auth = document.access_control_form.selected_file.value;

	window.showModalDialog("find_auth_users.php?path="+path_for_auth+"&share="+share+"&comment="+comment, "Allow IP", "dialogWidth: 350px; dialogHeight: 150px; border: 1px solid;");
}

function reset_acl_params(share_path, page)
{
	//var share_name = document.reset_acl_settings.hid_share.value;
	var recur_checked = document.reset_acl_settings.acl_recur.checked;

	document.getElementById('wait').style.display = 'block';

	$.ajax(
	{
		type: 'POST',
		url: 'reset_acl_action.py',
		data: 'path='+share_path+'&recursive=true&proceed=proceed&hid_page='+document.choose_share.share_list.value+'&page='+page,
		//data: 'share_name='+share_name+'&path='+share_path+'&recursive=true&proceed=proceed&hid_page='+document.choose_share.share_list.value+'&page='+page,

		success: function (html)
		{
			$('#response').html(html);
		}
	});
}

function validate_drbd_form()
{
	var source_host      = document.remote_replication.source_host.value;
	var source_ip_string = document.remote_replication.source_ip.value;

	var source_ip_array = new Array();
	
	source_ip_array = source_ip_string.split('-');
	
	eth_device = source_ip_array[0];
	source_ip  = source_ip_array[1];
		
	var dest_host = document.remote_replication.dest_host.value;
	var dest_ip   = document.remote_replication.dest_ip.value;

	var free_disk     = document.remote_replication.disk_list.value;
	var options_array = document.getElementsByName('connection_type');

	if (source_host == '' || source_ip == '' || dest_host == '' || dest_ip == '')
	{
		alert('All fields are mandatory!');
		return false;
	}

	else
	{
		error = check_ip(source_ip);

		if (error != '')
		{
			alert('Source IP '+source_ip+' is not a valid IP!');
			return false;
		}

		error = check_ip(dest_ip);

		if (error != '')
		{
			alert('Destination IP '+dest_ip+' is not a valid IP!');
			return false;
		}
	}

	for (i = 0;  i < options_array.length;  i++)
	{
		if (options_array[i].checked)
		{
			if (options_array[i].value == 'active')
			{
				conn_type = 'active';
			}

			else if (options_array[i].value == 'passive')
			{
				conn_type = 'passive';
			}
		}
	}

	document.getElementById('wait').style.display = 'block';

	$.ajax(
	{
		type: 'POST',
		url: 'enable_remote_replication.php',
		data: 'source_host='+source_host+'&dest_host='+dest_host+'&source_ip='+source_ip+'&dest_ip='+dest_ip+'&disk_list='+free_disk+'&eth_list='+eth_device+'&conn_type='+conn_type,

		success: function(html)
		{
			$('#response').html(html);
		}
	});
}

function refresh_div(status_string)
{
	var status_array = new Array();
	status_array = status_string.split('###');

	var rows_string = '';

	for (i = 0;  i < status_array.length;  i++)
	{
		index_of_primary   = status_array[i].indexOf('Primary');
		index_of_secondary = status_array[i].indexOf('Secondary');

		if (index_of_primary > 0 || index_of_secondary > 0)
		{
			rows_string += "<tr><td>"+status_array[i]+"</td><td>SYNC</td></tr>";
		}
	}
	
	if (index_of_primary > 0 || index_of_secondary > 0)
	{
		document.getElementById('id_status').innerHTML = "<table class = 'innertable' align = 'center' width = '50%' style = 'font: 12px Arial;'  border = '1'><tr class = 'table_header'><td colspan = '2'>Replication status</td></tr><tr><td width = '30%'><B>Connection status</B></td><td><B>Sync status</B></td></tr>"+rows_string+"</table>";
	}
}

function start_primary()
{
	document.getElementById('wait').style.display = 'block';

	$.ajax(
	{
		type: 'POST',
		url: 'start_primary.php',
		data: 'proceed_page=proceed',

		success: function(html)
		{
			$('#response').html(html);
		}
	});
}

function add_ips(value_of_id)
{
	error = check_ip(value_of_id);
	
	if (error != '')
	{
		alert(error);
		return false;
	}

	if (value_of_id != '')
	{
		document.add_ips_form.iscsi_ips.disabled = false;
	}

	var old_array = document.add_ips_form.elements["portal_list[]"];

	for (i = 0;  i < old_array.length;  i++)
	{
		if (old_array[i].value == value_of_id)
		{
			return false;
		}
		
		else
		{
			document.getElementById('id_allow_ip_list').options[i] = new Option('', '');
		}
	}

	value_array.push(value_of_id);

	string = '';
	
	for (i = 0;  i < value_array.length;  i++)
	{
		string += "<option value = '"+value_array[i]+"' selected>"+value_array[i]+"</option>";
	}
	
	document.getElementById('id_allow_ip_list').innerHTML = string;
	document.getElementById('id_add_props').value = '';
	document.getElementById('id_add_props').focus();
}

function remove_ips()
{
	var target = document.add_properties.list_targets.value;
	var ips = document.getElementById('id_allow_ip_list');
	var remove_ips_string = '';
	
	for (i = 0;  i < ips.options.length;  i++)
	{
		if (ips.options[i].selected == true)
		{
			remove_ips_string += ips.options[i].value + ',';
		}
	}
	
	if (remove_ips_string == '')
	{
		//alert('You need to choose atleast one IP!');
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family: status-bar;">You need to choose atleast one IP</div>', 'Iscsi Alert');
		return false;
	}
	
	document.getElementById('wait').style.display = 'block';

	$.ajax(
	{
		type: 'POST',
		url: 'remove_iscsi_ips.php',
		data: 'tgt='+target+'&ip_string='+remove_ips_string,

		success: function(html)
		{
			$('#response').html(html);
		}
	});
}

function add_usr_pwd(user, pwd, in_out)
{
	if (in_out == 'IN')
	{
		string = 'incoming';
	}

	else
	{
		string = 'outgoing';
	}

	if (user == '' || pwd == '')
	{
		//alert('Both '+string+' username and password are required!');
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family: status-bar;">Both the field are required!</div>', 'Iscsi Alert');
		return false;
	}

	if (pwd.length < 12)
	{
		//alert('Password should contain minimum of 12 characters!');
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family: status-bar;">Password should contain minimum of 12 characters</div>', 'Iscsi Alert');
		return false;
	}

	if (user != '' && pwd != '')
	{
		document.add_users.iscsi_user.disabled = false;
	}

	user_pwd_string = user+'/'+pwd;

	if (in_out == 'IN')
	{
		var old_user_array = document.add_users.elements["in_usr_pwd_list[]"];

		for (i = 0;  i < old_user_array.length;  i++)
		{
			user_pwd_array = old_user_array[i].value.split('/');

			if (user_pwd_array[0] == user)
			{
				return false;
			}
			
			else
			{
				document.getElementById('id_in_users_array').options[i] = new Option('', '');
			}
		}

		in_user_array.push(user_pwd_string);

		in_users_string = '';

		for (i = 0;  i < in_user_array.length;  i++)
		{
			in_users_string += "<option value = '"+in_user_array[i]+"' selected>"+in_user_array[i]+"</option>";
		}
		
		document.getElementById('id_in_users_array').innerHTML = in_users_string;

		document.add_users.in_user.value = '';
		document.add_users.in_pwd.value = '';
		document.add_users.in_user.focus();
	}

	if (in_out == 'OUT')
	{
		var old_user_array = document.add_users.elements["out_usr_pwd_list[]"];

		for (i = 0;  i < old_user_array.length;  i++)
		{
			document.getElementById('id_out_users_array').options[i] = new Option('', '');
		}

		out_user_array.push(user_pwd_string);

		out_users_string = '';

		for (i = 0;  i < out_user_array.length;  i++)
		{
			out_users_string += "<option value = '"+out_user_array[i]+"' selected>"+out_user_array[i]+"</option>";
		}

		document.getElementById('id_out_users_array').innerHTML = out_users_string;

		document.add_users.out_user.value = '';
		document.add_users.out_pwd.value = '';
		document.add_users.out_user.focus();
	}
}

function remove_users(in_out)
{
	var target_name = document.add_properties.list_targets.value;

	if (in_out == 'IN')
	{
		users = document.getElementById('id_in_users_array');
		remove_in_users_string = '';
	
		for (i = 0;  i < users.options.length;  i++)
		{
			if (users.options[i].selected == true)
			{
				remove_in_users_string += users.options[i].value + ',';
			}
		}
	
		if (remove_in_users_string == '')
		{
			alert('Choose a user!');
			return false;
		}

		document.getElementById('users_wait1').style.display = 'block';

		$.ajax(
		{
			type: 'POST',
			url: 'remove_users.php',
			data: 'tgt_name='+target_name+'&rem_usr_string='+remove_in_users_string,

			success: function(html)
			{
				$('#remove_users_wait1').html(html);
			}
		});
	}
	
	else
	{
		users = document.getElementById('id_out_users_array');

		for (i = 0;  i < users.options.length;  i++)
		{
			if (users.options[i].selected == true)
			{
				users.options[i] = null;
				out_users_array.splice(i, 1);
			}
		}
	}
}

function validate_iscsi_props_nw()
{
	var tar_name = document.add_properties1.target_prop_delete.value;
	if(tar_name =='prop_val')
	{
	jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family: status-bar;">Please Select the target</div>', 'Alert Dialog');
	return false;
	}
}


function validate_iscsi_props(form_name, elem_count)
{
	var target_name = document.add_properties.list_targets.value;

	var ddigest     = document.add_properties1.ddigest.value;
	var fbl         = document.add_properties1.fbl.value;
	var hd          = document.add_properties1.hd.value;
	var idata       = document.add_properties1.idata.value;
	var initr2t     = document.add_properties1.initr2t.value;
	var mbl         = document.add_properties1.mbl.value;
	var mor2t       = document.add_properties1.mor2t.value;
	var mrdsl       = document.add_properties1.mrdsl.value;
	var max_conn    = document.add_properties1.max_conn.value;
	var medsl       = document.add_properties1.medsl.value;
	var nopinterval = document.add_properties1.nopinterval.value;
	var qc          = document.add_properties1.qc.value;
	var rspto       = document.add_properties1.rspto.value;

	var dd_val    = document.add_properties1.dd_val.value;
	var fbl_val   = document.add_properties1.fbl_val.value;
	var hd_val    = document.add_properties1.hd_val.value;
	var idata_val = document.add_properties1.idata_val.value;
	var init_val  = document.add_properties1.init_val.value;
	var mbl_val   = document.add_properties1.mbl_val.value;
	var mor2t_val = document.add_properties1.mor2t_val.value;
	var mrdsl_val = document.add_properties1.mrdsl_val.value;
	var ms_val    = document.add_properties1.ms_val.value;
	var medsl_val = document.add_properties1.medsl_val.value;
	var nop_val   = document.add_properties1.nop_val.value;
	var qc_val    = document.add_properties1.qc_val.value;
	var rsp_val   = document.add_properties1.rsp_val.value;

	var elem_string = '';

	for (i = 0;  i < elem_count;  i++)
	{
		name  = document.add_properties1.elements[i].name;
		value = document.add_properties1.elements[i].value;

		if (name != 'iscsi_props' && name != 'iscsi_ips' && name != 'iscsi_user' && name != 'dd_val' && name != 'fbl_val' && name != 'hd_val' && name != 'idata_val' && name != 'init_val' && name != 'mbl_val' && name != 'mor2t_val' && name != 'mrdsl_val' && name != 'ms_val' && name != 'medsl_val' && name != 'nop_val' && name != 'qc_val' && name != 'rsp_val')
		{
			if (value == '')
			{
				alert('All fields are mandatory!');
				return false;
			}
		}
	}
	
	if (ddigest != dd_val)
	{
		elem_string += 'ddigest='+ddigest;
	}

	if (fbl != fbl_val)
	{
		elem_string += '&fbl='+fbl;
	}

	if (hd != hd_val)
	{
		elem_string += '&hd='+hd;
	}

	if (idata != idata_val)
	{
		elem_string += '&idata='+idata;
	}

	if (initr2t != init_val)
	{
		elem_string += '&initr2t='+initr2t;
	}

	if (mbl != mbl_val)
	{
		elem_string += '&mbl='+mbl;
	}

	if (mor2t != mor2t_val)
	{
		elem_string += '&mor2t='+mor2t;
	}

	if (mrdsl != mrdsl_val)
	{
		elem_string += '&mrdsl='+mrdsl;
	}

	if (max_conn != ms_val)
	{
		elem_string += '&max_conn='+max_conn;
	}

	if (medsl != medsl_val)
	{
		elem_string += '&medsl='+medsl;
	}
	
	if (nopinterval != nop_val)
	{
		elem_string += '&nopinterval='+nopinterval;
	}
	
	if (qc != qc_val)
	{
		elem_string += '&qc='+qc;
	}

	if (rspto != rsp_val)
	{
		elem_string += '&rspto='+rspto;
	}

	if (elem_string == '')
	{
		alert('Configuration not changed!');
		return false;
	}
	
	params_string = elem_string;
	
	document.getElementById('tgtprops_wait').style.display = 'block';
	
	params_string = params_string.replace(/&/g, 'CONCAT');

	$.ajax(
	{
		type: 'POST',
		url: 'set_iscsi_props.php',
		data: 'tgt_name='+target_name+'&params_string='+params_string,

		success: function(html)
		{
			$('#id_props_wait').html(html);
		}
	});

}

function validate_iscsi_ips()
{
	var select_target    = document.add_ips_form.list_targets.value;
	alert(select_target);
	var portal_array     = document.add_ips_form.elements["portal_list[]"];
	var target_name      = document.add_properties.list_targets.value;
	var initr_name       = document.add_ips_form.all_portal.value;
	var check_all_portal = document.add_ips_form.check_all_portal.checked;
	var sp_chars         = "~`\ !@#$%^&()+=[]\\\';,/{}|\"<>?";

	var check_string  = '';
	var portal_string = '';
	var all_params    = 'no';

	var initr_pattern = /^iqn|^naa|^\*$/;


        if(select_target == 'list_ini_val')
        {

        jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family: status-bar;">Select the target to Delete</div>', 'Alert Dialog');
        document.add_ips_form.list_targets.focus();
        return false;
        }

	if (initr_name == '')
	{
		alert('Initiator name can\'t be empty!');
		return false;
	}

	var iqn_array = initr_name.match(initr_pattern);

	if (iqn_array == null)
	{
		alert('Initiator name should start with \'iqn\', \'naa\' or it should be only \'*\'');
		return false;
	}

	/*if (iqn_pos != 0 && initr_name != '*')
	{
		alert('Initiator name should start with \'iqn\' or it should be \'*\'');
		return false;
	}*/

	for (var i = 0;  i < initr_name.length;  i++)
	{
		if (sp_chars.indexOf(initr_name.charAt(i)) >= 0)
		{
			alert('Special characters other than \'.\' and \':\' are not allowed in initiator name!');
			document.add_ips_form.all_portal.value = '';
			document.add_ips_form.all_portal.focus();
			return false;
		}
	}

	if (portal_array.length == null)
	{
		portal_id = document.getElementById('portal_array');
		
		if (portal_id.checked == false)
		{
			if (check_all_portal == false)
			{
				alert('You need to check an IP!');
				return false;
			}
		}

		else
		{
			portal_string = portal_id.value;
		}
	}

	else
	{
		for (i = 0;  i < portal_array.length;  i++)
		{
			check_string += portal_array[i].checked;
		}

		if (check_string.indexOf('true') < 0)
		{
			if (check_all_portal == false)
			{
				alert('You need to check an IP!');
				return false;
			}
		}

		else
		{
			for (i = 0;  i < portal_array.length;  i++)
			{
				if (portal_array[i].checked == true)
				{
					portal_string += portal_array[i].value + 'xxx';
				}
			}
		}
	}
	
	if (check_all_portal == true && initr_name == '*')
	{
		all_params = 'yes';
		portal_string = '*';
	}

	else if (check_all_portal == true && initr_name != '*')
	{
		all_params = 'no';
		portal_string = '*';
	}

	document.getElementById('wait').style.display = 'block';
	
	$.ajax(
	{
		type: 'POST',
		url: 'set_iscsi_ips.php',
		data: 'tgt_name='+target_name+'&initr_name='+initr_name+'&portal_string='+portal_string+'&all_params='+all_params+'&check_all='+check_all_portal,

		success: function(html)
		{
			$('#response').html(html);
		}
	});
}

function validate_iscsi_users()
{
	var select_target = document.add_users.auth_list.value;
	var in_users_array  = document.add_users.elements["in_usr_pwd_list[]"];
	var in_users  = document.add_users.in_user.value;
	var in_password  = document.add_users.in_pwd.value;
	//var target_name     = document.add_properties.list_targets.value;
	in_pass_length = in_password.length;	
	if(select_target =='auth_list_val')
	{

		//alert(select_target);
	jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family: status-bar;">Select the Target Name</div>', 'Iscsi Alert');
        //document.add_users.auth_list.focus();
        return false;
	}

	if(in_users =='')
        {
                //alert(select_target);
        jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family: status-bar;">Please Enter the Username</div>', 'Iscsi Alert');
        //document.add_users.auth_list.focus();
        return false;
        }

	if(in_password =='')
        {
                //alert(select_target);
        jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family: status-bar;">Please Enter the Password</div>', 'Iscsi Alert');
        //document.add_users.auth_list.focus();
        return false;
        }
	
	if(in_pass_length < 12)
        {
                //alert(select_target);
        jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family: status-bar;">Password atleast 12 Character.</div>', 'Iscsi Alert');
        //document.add_users.auth_list.focus();
        return false;
        }

	if (in_users_array.length == 0 && out_users_array.length == 0)
	{

		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family: status-bar;">Both the field are required!</div>', 'Iscsi Alert');
		//alert("Both incoming/outgoing users list can't be empty!");
		return false;
	}

	in_users_string = '';

	for (i = 0;  i < in_users_array.length;  i++)
	{
		if (in_users_array[i].selected == true)
		{
			in_users_string += in_users_array[i].value + ','; 
		}
	}
	
	if (in_users_string == '')
	{

		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 12%; padding-top: 4%; font-family: status-bar;">Please Choose a User</div>', 'Iscsi Alert');
		//alert('Please choose a user!');
		return false;
	}

	out_users_string = '';

	document.getElementById('wait').style.display = 'block';
	
	/*$.ajax(
	{
		type: 'POST',
		url: 'set_iscsi_users.php',
		data: 'tgt_name='+target_name+'&in_users_string='+in_users_string+'&out_users_string='+out_users_string,

		success: function(html)
		{
			$('#response').html(html);
		}
	});*/
}

function run_get_properties(target)
{
	document.getElementById('wait').style.display = 'block';

	$.ajax(
	{
		type: 'POST',
		url: 'get_properties.php',
		data: 'target='+target,

		success: function(html)
		{
			$('#response').html(html);
		}
	});
}

function do_schedule_snapshot(nas_iscsi, disk_name, snap_size, snap_name, c_limit, hour, mins, days, month, vg_size)
{
	var sp_chars  = "~`\ !@#$%^&*()+=[]\\\'\.;,/{}|\":<>?";
	var sp_chars1 = "~`_-\ !@#$%^&*()+=[]\\\';,/{}|\":<>?qwertyuiopasdfghjklzxcvbnmiQWERTYUIOPASDFGHJKLZXCVBNM";

	var snap_array = new Array();

	var multi  = 0;
	var multi1 = 0;

	snap_array = disk_name.split('-');

	tot_snap_size = snap_array[1];

	tot_snap_size = parseInt(tot_snap_size);

	gb_unit = disk_name.indexOf('GB');
	mb_unit = disk_name.indexOf('MB');
	tb_unit = disk_name.indexOf('TB');
	
	gb_unit1 = vg_size.indexOf('GB');
	mb_unit1 = vg_size.indexOf('MB');
	tb_unit1 = vg_size.indexOf('TB');
	
	if (disk_name == '')
	{
		alert('You need to choose a disk!');
		return false;
	}

	if (snap_size == 0 || snap_size == '')
	{
		alert('Specify size for snapshot!');
		document.sched_snapshot.snap_size.value = '';
		document.sched_snapshot.snap_size.focus();
		return false;
	}

	if (snap_name == '')
	{
		alert('Specify a name for snapshot name!');
		document.sched_snapshot.snap_name.value = '';
		document.sched_snapshot.snap_name.focus();
		return false;
	}

	for (var i = 0;  i < snap_name.length;  i++)
	{
		if (sp_chars.indexOf(snap_name.charAt(i)) >= 0)
		{
			alert('Please enter a valid snapshot name!');
			document.sched_snapshot.snap_name.value = '';
			document.sched_snapshot.snap_name.focus();
			return false;
		}
	}

	for (var i = 0;  i < snap_size.length;  i++)
	{
		if (sp_chars1.indexOf(snap_size.charAt(i)) >= 0)
		{
			alert('Please enter a valid size for snapshot!');
			return false;
		}
	}

	for (var i = 0;  i < c_limit.length;  i++)
	{
		if (sp_chars1.indexOf(c_limit.charAt(i)) >= 0)
		{
			alert('Please enter a valid critical limit!');
			document.sched_snapshot.c_limit.value = '';
			document.sched_snapshot.c_limit.focus();
			return false;
		}
	}

	if (c_limit == 0 || c_limit == '')
	{
		alert('Specify a critical limit!');
		document.sched_snapshot.c_limit.value = '';
		document.sched_snapshot.c_limit.focus();
		return false;
	}
	
	
	if (gb_unit > 0)
	{
		multi = 1;
	}
	
	if (mb_unit > 0)
	{
		multi = (1 / 1024);
	}
	
	if (tb_unit > 0)
	{
		multi = 1024;
	}

	if (gb_unit1 > 0)
	{
		multi1 = 1;
	}

	if (mb_unit1 > 0)
	{
		multi1 = (1 / 1024);
	}

	if (tb_unit1 > 0)
	{
		multi1 = 1024;
	}

	tot_snap_size = tot_snap_size * multi;

	vg_size = parseInt(vg_size);
	vg_size = vg_size * multi1;
	
	/*if (snap_size > tot_snap_size)
	{
		alert('Size exceeded max limit!');
		document.sched_snapshot.snap_size.value = '';
		document.sched_snapshot.snap_size.focus();

		return false;
	}*/

	if (snap_size > vg_size)
	{
		alert('Size exceeded VG size!');
		document.sched_snapshot.snap_size.value = '';
		document.sched_snapshot.snap_size.focus();

		return false;
	}
	
	var week_array = new Array();

	if (nas_iscsi == 'ISCSI')
	{
		week_array = document.getElementsByName('week');
	}

	else if (nas_iscsi == 'NAS')
	{
		week_array = document.getElementsByName('nas_week');
	}
	
	for (i = 0;  i < week_array.length;  i++)
	{
		if (week_array[i].checked)
		{
			week_val = week_array[i].value;
		}
	}

	if (week_val == '*' && hour == '*' && (mins == '*' || mins < 15) && days == '*' && month == '*')
	{
		alert('Please set the minutes for atleast 15 minutes!');
		return false;
	}

	document.getElementById('wait').style.display = 'block';
	
	if (nas_iscsi == 'ISCSI')
	{
		var hour_checked = document.sched_snapshot.e_hour.checked;
		var min_checked  = document.sched_snapshot.e_min.checked;
		var day_checked  = document.sched_snapshot.e_day.checked;

		$.ajax(
		{
			type: 'POST',
			url: 'schedule_snapshot.php',
			data: 'disk_name='+disk_name+'&snap_size='+snap_size+'&snap_name='+snap_name+'&c_limit='+c_limit+'&hours='+hour+'&mins='+mins+'&day='+days+'&month='+month+'&week='+week_val+'&proceed_page=proceed&hchecked='+hour_checked+'&mchecked='+min_checked+'&dchecked='+day_checked,
	
			success: function(html)
			{
				$('#response').html(html);
			}
		});
	}

	else if (nas_iscsi == 'NAS')
	{
		var hour_checked = document.sched_nas_snapshot.e_hour.checked;
		var min_checked  = document.sched_nas_snapshot.e_min.checked;
		var day_checked  = document.sched_nas_snapshot.e_day.checked;

		$.ajax(
		{
			type: 'POST',
			url: 'schedule_nas_snapshot.php',
			data: 'disk_name='+disk_name+'&snap_size='+snap_size+'&snap_name='+snap_name+'&c_limit='+c_limit+'&hours='+hour+'&mins='+mins+'&day='+days+'&month='+month+'&week='+week_val+'&proceed_page=proceed&hchecked='+hour_checked+'&mchecked='+min_checked+'&dchecked='+day_checked,
	
			success: function(html)
			{
				$('#id_schedule_restart').html(html);
			}
		});
	}

	return false;
}

function validate_password()
{
	var password = document.change_password.pword.value;
	var cpasswrd = document.change_password.c_pword.value;

	if (password == '' || cpasswrd == '')
	{
		alert('All fields are mandatory!');
		return false;
	}

	if (password != cpasswrd)
	{
		alert('Passwords do not match!');

		document.change_password.pword.value = '';
		document.change_password.c_pword.value = '';
				
		document.change_password.pword.focus();
		return false;
	}
}

function set_pwd_focus()
{
	document.change_password.o_pword.focus();
}

function set_frame_size()
{
	document.getElementById('id_apps').style.width  = '100%';
	document.getElementById('id_apps').style.height = '100%';
}

function uncheck_all()
{
	var check_all_portal = document.add_ips_form.check_all_portal.checked;
	var portal_array     = document.add_ips_form.elements["portal_list[]"];

	if (check_all_portal == true)
	{
		for (i = 0;  i < portal_array.length;  i++)
		{
			portal_array[i].checked = false;
		}
	}

}

function reset_ads_script()
{
	document.getElementById('wait').style.display = 'block';

	$.ajax(
	{
		type: 'POST',
		url: 'reset_ads_connection.php',
		data: 'proceed=proceed',

		success: function(html)
		{
			$('#response').html(html);
		}
	});
}

function do_schedule_log(curval, frequency, noofcopies)
{
	/*if (curval != '')
	{
		alert('Backup already scheduled for this no. of backups! Please delete the existing scheduled log by clicking the \'Remove Scheduled Log\' button.');
		

		document.autoschedulelogs.del_sched_log.disabled = false;
		return false;
	}*/

	if (frequency == '')
	{
		alert('Frequency can\'t be empty!');
		return false;
	}

	document.getElementById('wait').style.display = 'block';

	$.ajax(
	{
		type: 'POST',
		url: 'schedule_logs.py',
		data: 'day=' + frequency + '&num=' + noofcopies,

		success: function(html)
		{
			$('#response').html(html);
		}
	});
}

function remove_schedule_log(val)
{
	if (val != '')
	{
		removeval = document.autoschedulelogs.del_sched_log.value;

		document.getElementById('wait').style.display = 'block';

		$.ajax(
		{
			type: 'POST',
			url: 'schedule_logs.py',
			data: 'rem=' + removeval,

			success: function(html)
			{
				$('#response').html(html);
			}
		});
	}

	else
	{
		alert('Not Scheduled!');
		return false;
	}
}

function disable_all(type, element, week_array)
{
	var week_val = '';

	if (type == 'NAS')
	{
		if (element == 'nhours')
		{
			for (i = 0;  i < week_array.length;  i++)
			{
				week_array[i].disabled = true;
			}

			if (document.sched_nas_snapshot.e_hour.checked == true)
			{
				document.getElementById('id_select_hours').innerHTML =
										"<option value = '1'>1</option>"+
                                                				"<option value = '2'>2</option>"+
				                                                "<option value = '3'>3</option>"+
                                                				"<option value = '4'>4</option>"+
                                                				"<option value = '5'>5</option>"+
                                                				"<option value = '6'>6</option>"+
                                                				"<option value = '7'>7</option>"+
                                                				"<option value = '8'>8</option>"+
                                                				"<option value = '9'>9</option>"+
                                                				"<option value = '10'>10</option>"+
                                                				"<option value = '11'>11</option>"+
                                                				"<option value = '12'>12</option>"+
                                                				"<option value = '13'>13</option>"+
                                                				"<option value = '14'>14</option>"+
                                                				"<option value = '15'>15</option>"+
                                                				"<option value = '16'>16</option>"+
                                                				"<option value = '17'>17</option>"+
                                                				"<option value = '18'>18</option>"+
                                                				"<option value = '19'>19</option>"+
                                                				"<option value = '20'>20</option>"+
                                                				"<option value = '21'>21</option>"+
                                                				"<option value = '22'>22</option>"+
                                                				"<option value = '23'>23</option>";
				document.sched_nas_snapshot.mins.disabled  = true;
				document.sched_nas_snapshot.day.disabled   = true;
				document.sched_nas_snapshot.e_day.disabled = true;
				document.sched_nas_snapshot.e_min.disabled = true;
				document.sched_nas_snapshot.month.disabled = true;
			}

			else
			{
				for (i = 0;  i < week_array.length;  i++)
				{
					week_array[i].disabled = false;

					if (week_array[i].checked)
					{
						week_val = week_array[i].value;
					}
				}

				document.getElementById('id_select_hours').innerHTML =
										"<option value = '*'>*</option>"+
                                                				"<option value = '0'>0</option>"+
                                                				"<option value = '1'>1</option>"+
                                                				"<option value = '2'>2</option>"+
				                                                "<option value = '3'>3</option>"+
                                                				"<option value = '4'>4</option>"+
                                                				"<option value = '5'>5</option>"+
                                                				"<option value = '6'>6</option>"+
                                                				"<option value = '7'>7</option>"+
                                                				"<option value = '8'>8</option>"+
                                                				"<option value = '9'>9</option>"+
                                                				"<option value = '10'>10</option>"+
                                                				"<option value = '11'>11</option>"+
                                                				"<option value = '12'>12</option>"+
                                                				"<option value = '13'>13</option>"+
                                                				"<option value = '14'>14</option>"+
                                                				"<option value = '15'>15</option>"+
                                                				"<option value = '16'>16</option>"+
                                                				"<option value = '17'>17</option>"+
                                                				"<option value = '18'>18</option>"+
                                                				"<option value = '19'>19</option>"+
                                                				"<option value = '20'>20</option>"+
                                                				"<option value = '21'>21</option>"+
                                                				"<option value = '22'>22</option>"+
                                                				"<option value = '23'>23</option>";
				document.sched_nas_snapshot.mins.disabled  = false;
			
				if (week_val == '*')
				{
					document.sched_nas_snapshot.day.disabled   = false;
					document.sched_nas_snapshot.e_day.disabled = false;
				}
		
				else
				{
					document.sched_nas_snapshot.day.disabled   = true;
					document.sched_nas_snapshot.e_day.disabled = true;
				}

				document.sched_nas_snapshot.e_min.disabled = false;
				document.sched_nas_snapshot.month.disabled = false;
			}
		}

		if (element == 'nmins')
		{
			for (i = 0;  i < week_array.length;  i++)
			{
				week_array[i].disabled = true;
			}

			if (document.sched_nas_snapshot.e_min.checked == true)
			{
				document.getElementById('id_select_mins').innerHTML =
										"<option value = '1'>1</option>"+
                                                				"<option value = '2'>2</option>"+
				                                                "<option value = '3'>3</option>"+
                                                				"<option value = '4'>4</option>"+
                                                				"<option value = '5'>5</option>"+
                                                				"<option value = '6'>6</option>"+
                                                				"<option value = '7'>7</option>"+
                                                				"<option value = '8'>8</option>"+
                                                				"<option value = '9'>9</option>"+
                                                				"<option value = '10'>10</option>"+
                                                				"<option value = '11'>11</option>"+
                                                				"<option value = '12'>12</option>"+
                                                				"<option value = '13'>13</option>"+
                                                				"<option value = '14'>14</option>"+
                                                				"<option value = '15'>15</option>"+
                                                				"<option value = '16'>16</option>"+
                                                				"<option value = '17'>17</option>"+
                                                				"<option value = '18'>18</option>"+
                                                				"<option value = '19'>19</option>"+
                                                				"<option value = '20'>20</option>"+
                                                				"<option value = '21'>21</option>"+
                                                				"<option value = '22'>22</option>"+
                                                				"<option value = '23'>23</option>"+
                                                				"<option value = '24'>24</option>"+
                                                				"<option value = '25'>25</option>"+
                                                				"<option value = '26'>26</option>"+
                                                				"<option value = '27'>27</option>"+
                                                				"<option value = '28'>28</option>"+
                                                				"<option value = '29'>29</option>"+
                                                				"<option value = '30'>30</option>"+
                                                				"<option value = '31'>31</option>"+
                                                				"<option value = '32'>32</option>"+
                                                				"<option value = '33'>33</option>"+
                                                				"<option value = '34'>34</option>"+
                                                				"<option value = '35'>35</option>"+
                                                				"<option value = '36'>36</option>"+
                                                				"<option value = '37'>37</option>"+
                                                				"<option value = '38'>38</option>"+
                                                				"<option value = '39'>39</option>"+
                                                				"<option value = '40'>40</option>"+
                                                				"<option value = '41'>41</option>"+
                                                				"<option value = '42'>42</option>"+
                                                				"<option value = '43'>43</option>"+
                                                				"<option value = '44'>44</option>"+
                                                				"<option value = '45'>45</option>"+
                                                				"<option value = '46'>46</option>"+
                                                				"<option value = '47'>47</option>"+
                                                				"<option value = '48'>48</option>"+
                                                				"<option value = '49'>49</option>"+
                                                				"<option value = '50'>50</option>"+
                                                				"<option value = '51'>51</option>"+
                                                				"<option value = '52'>52</option>"+
                                                				"<option value = '53'>53</option>"+
                                                				"<option value = '54'>54</option>"+
                                                				"<option value = '55'>55</option>"+
                                                				"<option value = '56'>56</option>"+
                                                				"<option value = '57'>57</option>"+
                                                				"<option value = '58'>58</option>"+
                                                				"<option value = '59'>59</option>";
				document.sched_nas_snapshot.hours.disabled  = true;
				document.sched_nas_snapshot.day.disabled    = true;
				document.sched_nas_snapshot.e_day.disabled  = true;
				document.sched_nas_snapshot.e_hour.disabled = true;
				document.sched_nas_snapshot.month.disabled  = true;
			}

			else
			{
				for (i = 0;  i < week_array.length;  i++)
				{
					week_array[i].disabled = false;

					if (week_array[i].checked)
					{
						week_val = week_array[i].value;
					}
				}

				document.getElementById('id_select_mins').innerHTML =
										"<option value = '*'>*</option>"+
                                                				"<option value = '0'>0</option>"+
                                                				"<option value = '1'>1</option>"+
                                                				"<option value = '2'>2</option>"+
				                                                "<option value = '3'>3</option>"+
                                                				"<option value = '4'>4</option>"+
                                                				"<option value = '5'>5</option>"+
                                                				"<option value = '6'>6</option>"+
                                                				"<option value = '7'>7</option>"+
                                                				"<option value = '8'>8</option>"+
                                                				"<option value = '9'>9</option>"+
                                                				"<option value = '10'>10</option>"+
                                                				"<option value = '11'>11</option>"+
                                                				"<option value = '12'>12</option>"+
                                                				"<option value = '13'>13</option>"+
                                                				"<option value = '14'>14</option>"+
                                                				"<option value = '15'>15</option>"+
                                                				"<option value = '16'>16</option>"+
                                                				"<option value = '17'>17</option>"+
                                                				"<option value = '18'>18</option>"+
                                                				"<option value = '19'>19</option>"+
                                                				"<option value = '20'>20</option>"+
                                                				"<option value = '21'>21</option>"+
                                                				"<option value = '22'>22</option>"+
                                                				"<option value = '23'>23</option>"+
                                                				"<option value = '24'>24</option>"+
                                                				"<option value = '25'>25</option>"+
                                                				"<option value = '26'>26</option>"+
                                                				"<option value = '27'>27</option>"+
                                                				"<option value = '28'>28</option>"+
                                                				"<option value = '29'>29</option>"+
                                                				"<option value = '30'>30</option>"+
                                                				"<option value = '31'>31</option>"+
                                                				"<option value = '32'>32</option>"+
                                                				"<option value = '33'>33</option>"+
                                                				"<option value = '34'>34</option>"+
                                                				"<option value = '35'>35</option>"+
                                                				"<option value = '36'>36</option>"+
                                                				"<option value = '37'>37</option>"+
                                                				"<option value = '38'>38</option>"+
                                                				"<option value = '39'>39</option>"+
                                                				"<option value = '40'>40</option>"+
                                                				"<option value = '41'>41</option>"+
                                                				"<option value = '42'>42</option>"+
                                                				"<option value = '43'>43</option>"+
                                                				"<option value = '44'>44</option>"+
                                                				"<option value = '45'>45</option>"+
                                                				"<option value = '46'>46</option>"+
                                                				"<option value = '47'>47</option>"+
                                                				"<option value = '48'>48</option>"+
                                                				"<option value = '49'>49</option>"+
                                                				"<option value = '50'>50</option>"+
                                                				"<option value = '51'>51</option>"+
                                                				"<option value = '52'>52</option>"+
                                                				"<option value = '53'>53</option>"+
                                                				"<option value = '54'>54</option>"+
                                                				"<option value = '55'>55</option>"+
                                                				"<option value = '56'>56</option>"+
                                                				"<option value = '57'>57</option>"+
                                                				"<option value = '58'>58</option>"+
                                                				"<option value = '59'>59</option>";
				document.sched_nas_snapshot.hours.disabled  = false;

				if (week_val == '*')
				{
					document.sched_nas_snapshot.day.disabled    = false;
					document.sched_nas_snapshot.e_day.disabled  = false;
				}

				else
				{
					document.sched_nas_snapshot.day.disabled    = true;
					document.sched_nas_snapshot.e_day.disabled  = true;
				}

				document.sched_nas_snapshot.e_hour.disabled  = false;
				document.sched_nas_snapshot.month.disabled  = false;
			}
		}

		if (element == 'ndays')
		{
			for (i = 0;  i < week_array.length;  i++)
			{
				week_array[i].disabled = true;
			}

			if (document.sched_nas_snapshot.e_day.checked == true)
			{
				document.getElementById('id_schedule_nas_day').innerHTML =
										"<option value = '1'>1</option>"+
                                                				"<option value = '2'>2</option>"+
				                                                "<option value = '3'>3</option>"+
                                                				"<option value = '4'>4</option>"+
                                                				"<option value = '5'>5</option>"+
                                                				"<option value = '6'>6</option>"+
                                                				"<option value = '7'>7</option>"+
                                                				"<option value = '8'>8</option>"+
                                                				"<option value = '9'>9</option>"+
                                                				"<option value = '10'>10</option>"+
                                                				"<option value = '11'>11</option>"+
                                                				"<option value = '12'>12</option>"+
                                                				"<option value = '13'>13</option>"+
                                                				"<option value = '14'>14</option>"+
                                                				"<option value = '15'>15</option>"+
                                                				"<option value = '16'>16</option>"+
                                                				"<option value = '17'>17</option>"+
                                                				"<option value = '18'>18</option>"+
                                                				"<option value = '19'>19</option>"+
                                                				"<option value = '20'>20</option>"+
                                                				"<option value = '21'>21</option>"+
                                                				"<option value = '22'>22</option>"+
                                                				"<option value = '23'>23</option>"+
                                                				"<option value = '24'>24</option>"+
                                                				"<option value = '25'>25</option>"+
                                                				"<option value = '26'>26</option>"+
                                                				"<option value = '27'>27</option>"+
                                                				"<option value = '28'>28</option>"+
                                                				"<option value = '29'>29</option>"+
                                                				"<option value = '30'>30</option>"+
                                                				"<option value = '31'>31</option>";
				document.sched_nas_snapshot.mins.disabled   = true;
				document.sched_nas_snapshot.hours.disabled  = true;
				document.sched_nas_snapshot.e_hour.disabled = true;
				document.sched_nas_snapshot.e_min.disabled  = true;
				document.sched_nas_snapshot.month.disabled  = true;
			}

			else
			{
				for (i = 0;  i < week_array.length;  i++)
				{
					week_array[i].disabled = false;
				}

				document.getElementById('id_schedule_nas_day').innerHTML =
										"<option value = '*'>*</option>"+
                                                				"<option value = '0'>0</option>"+
                                                				"<option value = '1'>1</option>"+
                                                				"<option value = '2'>2</option>"+
				                                                "<option value = '3'>3</option>"+
                                                				"<option value = '4'>4</option>"+
                                                				"<option value = '5'>5</option>"+
                                                				"<option value = '6'>6</option>"+
                                                				"<option value = '7'>7</option>"+
                                                				"<option value = '8'>8</option>"+
                                                				"<option value = '9'>9</option>"+
                                                				"<option value = '10'>10</option>"+
                                                				"<option value = '11'>11</option>"+
                                                				"<option value = '12'>12</option>"+
                                                				"<option value = '13'>13</option>"+
                                                				"<option value = '14'>14</option>"+
                                                				"<option value = '15'>15</option>"+
                                                				"<option value = '16'>16</option>"+
                                                				"<option value = '17'>17</option>"+
                                                				"<option value = '18'>18</option>"+
                                                				"<option value = '19'>19</option>"+
                                                				"<option value = '20'>20</option>"+
                                                				"<option value = '21'>21</option>"+
                                                				"<option value = '22'>22</option>"+
                                                				"<option value = '23'>23</option>"+
                                                				"<option value = '24'>24</option>"+
                                                				"<option value = '25'>25</option>"+
                                                				"<option value = '26'>26</option>"+
                                                				"<option value = '27'>27</option>"+
                                                				"<option value = '28'>28</option>"+
                                                				"<option value = '29'>29</option>"+
                                                				"<option value = '30'>30</option>"+
                                                				"<option value = '31'>31</option>";
				document.sched_nas_snapshot.hours.disabled  = false;
				document.sched_nas_snapshot.mins.disabled   = false;
				document.sched_nas_snapshot.e_hour.disabled = false;
				document.sched_nas_snapshot.e_min.disabled  = false;
				document.sched_nas_snapshot.month.disabled  = false;
			}
		}
	}

	if (type == 'ISCSI')
	{
		if (element == 'nhours')
		{
			for (i = 0;  i < week_array.length;  i++)
			{
				week_array[i].disabled = true;
			}

			if (document.sched_snapshot.e_hour.checked == true)
			{
				document.getElementById('id_iscsi_hours').innerHTML =
										"<option value = '1'>1</option>"+
                                                				"<option value = '2'>2</option>"+
				                                                "<option value = '3'>3</option>"+
                                                				"<option value = '4'>4</option>"+
                                                				"<option value = '5'>5</option>"+
                                                				"<option value = '6'>6</option>"+
                                                				"<option value = '7'>7</option>"+
                                                				"<option value = '8'>8</option>"+
                                                				"<option value = '9'>9</option>"+
                                                				"<option value = '10'>10</option>"+
                                                				"<option value = '11'>11</option>"+
                                                				"<option value = '12'>12</option>"+
                                                				"<option value = '13'>13</option>"+
                                                				"<option value = '14'>14</option>"+
                                                				"<option value = '15'>15</option>"+
                                                				"<option value = '16'>16</option>"+
                                                				"<option value = '17'>17</option>"+
                                                				"<option value = '18'>18</option>"+
                                                				"<option value = '19'>19</option>"+
                                                				"<option value = '20'>20</option>"+
                                                				"<option value = '21'>21</option>"+
                                                				"<option value = '22'>22</option>"+
                                                				"<option value = '23'>23</option>";
				document.sched_snapshot.mins.disabled  = true;
				document.sched_snapshot.day.disabled   = true;
				document.sched_snapshot.e_min.disabled = true;
				document.sched_snapshot.e_day.disabled = true;
				document.sched_snapshot.month.disabled = true;
			}

			else
			{
				for (i = 0;  i < week_array.length;  i++)
				{
					week_array[i].disabled = false;
					
					if (week_array[i].checked)
					{
						week_val = week_array[i].value;
					}
				}

				document.getElementById('id_iscsi_hours').innerHTML =
										"<option value = '*'>*</option>"+
                                                				"<option value = '0'>0</option>"+
                                                				"<option value = '1'>1</option>"+
                                                				"<option value = '2'>2</option>"+
				                                                "<option value = '3'>3</option>"+
                                                				"<option value = '4'>4</option>"+
                                                				"<option value = '5'>5</option>"+
                                                				"<option value = '6'>6</option>"+
                                                				"<option value = '7'>7</option>"+
                                                				"<option value = '8'>8</option>"+
                                                				"<option value = '9'>9</option>"+
                                                				"<option value = '10'>10</option>"+
                                                				"<option value = '11'>11</option>"+
                                                				"<option value = '12'>12</option>"+
                                                				"<option value = '13'>13</option>"+
                                                				"<option value = '14'>14</option>"+
                                                				"<option value = '15'>15</option>"+
                                                				"<option value = '16'>16</option>"+
                                                				"<option value = '17'>17</option>"+
                                                				"<option value = '18'>18</option>"+
                                                				"<option value = '19'>19</option>"+
                                                				"<option value = '20'>20</option>"+
                                                				"<option value = '21'>21</option>"+
                                                				"<option value = '22'>22</option>"+
                                                				"<option value = '23'>23</option>";
				document.sched_snapshot.mins.disabled  = false;

				if (week_val == '*')
				{
					document.sched_snapshot.day.disabled   = false;
					document.sched_snapshot.e_day.disabled = false;
				}

				else
				{
					document.sched_snapshot.day.disabled   = true;
					document.sched_snapshot.e_day.disabled = true;
				}

				document.sched_snapshot.e_min.disabled = false;
				document.sched_snapshot.month.disabled = false;
			}
		}

		if (element == 'nmins')
		{
			for (i = 0;  i < week_array.length;  i++)
			{
				week_array[i].disabled = true;
			}

			if (document.sched_snapshot.e_min.checked == true)
			{
				document.getElementById('id_iscsi_mins').innerHTML =
										"<option value = '1'>1</option>"+
                                                				"<option value = '2'>2</option>"+
				                                                "<option value = '3'>3</option>"+
                                                				"<option value = '4'>4</option>"+
                                                				"<option value = '5'>5</option>"+
                                                				"<option value = '6'>6</option>"+
                                                				"<option value = '7'>7</option>"+
                                                				"<option value = '8'>8</option>"+
                                                				"<option value = '9'>9</option>"+
                                                				"<option value = '10'>10</option>"+
                                                				"<option value = '11'>11</option>"+
                                                				"<option value = '12'>12</option>"+
                                                				"<option value = '13'>13</option>"+
                                                				"<option value = '14'>14</option>"+
                                                				"<option value = '15'>15</option>"+
                                                				"<option value = '16'>16</option>"+
                                                				"<option value = '17'>17</option>"+
                                                				"<option value = '18'>18</option>"+
                                                				"<option value = '19'>19</option>"+
                                                				"<option value = '20'>20</option>"+
                                                				"<option value = '21'>21</option>"+
                                                				"<option value = '22'>22</option>"+
                                                				"<option value = '23'>23</option>"+
                                                				"<option value = '24'>24</option>"+
                                                				"<option value = '25'>25</option>"+
                                                				"<option value = '26'>26</option>"+
                                                				"<option value = '27'>27</option>"+
                                                				"<option value = '28'>28</option>"+
                                                				"<option value = '29'>29</option>"+
                                                				"<option value = '30'>30</option>"+
                                                				"<option value = '31'>31</option>"+
                                                				"<option value = '32'>32</option>"+
                                                				"<option value = '33'>33</option>"+
                                                				"<option value = '34'>34</option>"+
                                                				"<option value = '35'>35</option>"+
                                                				"<option value = '36'>36</option>"+
                                                				"<option value = '37'>37</option>"+
                                                				"<option value = '38'>38</option>"+
                                                				"<option value = '39'>39</option>"+
                                                				"<option value = '40'>40</option>"+
                                                				"<option value = '41'>41</option>"+
                                                				"<option value = '42'>42</option>"+
                                                				"<option value = '43'>43</option>"+
                                                				"<option value = '44'>44</option>"+
                                                				"<option value = '45'>45</option>"+
                                                				"<option value = '46'>46</option>"+
                                                				"<option value = '47'>47</option>"+
                                                				"<option value = '48'>48</option>"+
                                                				"<option value = '49'>49</option>"+
                                                				"<option value = '50'>50</option>"+
                                                				"<option value = '51'>51</option>"+
                                                				"<option value = '52'>52</option>"+
                                                				"<option value = '53'>53</option>"+
                                                				"<option value = '54'>54</option>"+
                                                				"<option value = '55'>55</option>"+
                                                				"<option value = '56'>56</option>"+
                                                				"<option value = '57'>57</option>"+
                                                				"<option value = '58'>58</option>"+
                                                				"<option value = '59'>59</option>";
				document.sched_snapshot.hours.disabled  = true;
				document.sched_snapshot.day.disabled    = true;
				document.sched_snapshot.e_day.disabled  = true;
				document.sched_snapshot.e_hour.disabled = true;
				document.sched_snapshot.month.disabled  = true;
			}

			else
			{
				for (i = 0;  i < week_array.length;  i++)
				{
					week_array[i].disabled = false;

					if (week_array[i].checked)
					{
						week_val = week_array[i].value;
					}
				}

				document.getElementById('id_iscsi_mins').innerHTML =
										"<option value = '*'>*</option>"+
                                                				"<option value = '0'>0</option>"+
                                                				"<option value = '1'>1</option>"+
                                                				"<option value = '2'>2</option>"+
				                                                "<option value = '3'>3</option>"+
                                                				"<option value = '4'>4</option>"+
                                                				"<option value = '5'>5</option>"+
                                                				"<option value = '6'>6</option>"+
                                                				"<option value = '7'>7</option>"+
                                                				"<option value = '8'>8</option>"+
                                                				"<option value = '9'>9</option>"+
                                                				"<option value = '10'>10</option>"+
                                                				"<option value = '11'>11</option>"+
                                                				"<option value = '12'>12</option>"+
                                                				"<option value = '13'>13</option>"+
                                                				"<option value = '14'>14</option>"+
                                                				"<option value = '15'>15</option>"+
                                                				"<option value = '16'>16</option>"+
                                                				"<option value = '17'>17</option>"+
                                                				"<option value = '18'>18</option>"+
                                                				"<option value = '19'>19</option>"+
                                                				"<option value = '20'>20</option>"+
                                                				"<option value = '21'>21</option>"+
                                                				"<option value = '22'>22</option>"+
                                                				"<option value = '23'>23</option>"+
                                                				"<option value = '24'>24</option>"+
                                                				"<option value = '25'>25</option>"+
                                                				"<option value = '26'>26</option>"+
                                                				"<option value = '27'>27</option>"+
                                                				"<option value = '28'>28</option>"+
                                                				"<option value = '29'>29</option>"+
                                                				"<option value = '30'>30</option>"+
                                                				"<option value = '31'>31</option>"+
                                                				"<option value = '32'>32</option>"+
                                                				"<option value = '33'>33</option>"+
                                                				"<option value = '34'>34</option>"+
                                                				"<option value = '35'>35</option>"+
                                                				"<option value = '36'>36</option>"+
                                                				"<option value = '37'>37</option>"+
                                                				"<option value = '38'>38</option>"+
                                                				"<option value = '39'>39</option>"+
                                                				"<option value = '40'>40</option>"+
                                                				"<option value = '41'>41</option>"+
                                                				"<option value = '42'>42</option>"+
                                                				"<option value = '43'>43</option>"+
                                                				"<option value = '44'>44</option>"+
                                                				"<option value = '45'>45</option>"+
                                                				"<option value = '46'>46</option>"+
                                                				"<option value = '47'>47</option>"+
                                                				"<option value = '48'>48</option>"+
                                                				"<option value = '49'>49</option>"+
                                                				"<option value = '50'>50</option>"+
                                                				"<option value = '51'>51</option>"+
                                                				"<option value = '52'>52</option>"+
                                                				"<option value = '53'>53</option>"+
                                                				"<option value = '54'>54</option>"+
                                                				"<option value = '55'>55</option>"+
                                                				"<option value = '56'>56</option>"+
                                                				"<option value = '57'>57</option>"+
                                                				"<option value = '58'>58</option>"+
                                                				"<option value = '59'>59</option>";
				document.sched_snapshot.hours.disabled  = false;

				if (week_val == '*')
				{
					document.sched_snapshot.day.disabled    = false;
					document.sched_snapshot.e_day.disabled  = false;
				}

				else
				{
					document.sched_snapshot.day.disabled    = true;
					document.sched_snapshot.e_day.disabled  = true;
				}

				document.sched_snapshot.e_hour.disabled = false;
				document.sched_snapshot.month.disabled  = false;
			}
		}

		if (element == 'ndays')
		{
			for (i = 0;  i < week_array.length;  i++)
			{
				week_array[i].disabled = true;
			}

			if (document.sched_snapshot.e_day.checked == true)
			{
				document.getElementById('id_schedule_day').innerHTML =
										"<option value = '1'>1</option>"+
                                                				"<option value = '2'>2</option>"+
				                                                "<option value = '3'>3</option>"+
                                                				"<option value = '4'>4</option>"+
                                                				"<option value = '5'>5</option>"+
                                                				"<option value = '6'>6</option>"+
                                                				"<option value = '7'>7</option>"+
                                                				"<option value = '8'>8</option>"+
                                                				"<option value = '9'>9</option>"+
                                                				"<option value = '10'>10</option>"+
                                                				"<option value = '11'>11</option>"+
                                                				"<option value = '12'>12</option>"+
                                                				"<option value = '13'>13</option>"+
                                                				"<option value = '14'>14</option>"+
                                                				"<option value = '15'>15</option>"+
                                                				"<option value = '16'>16</option>"+
                                                				"<option value = '17'>17</option>"+
                                                				"<option value = '18'>18</option>"+
                                                				"<option value = '19'>19</option>"+
                                                				"<option value = '20'>20</option>"+
                                                				"<option value = '21'>21</option>"+
                                                				"<option value = '22'>22</option>"+
                                                				"<option value = '23'>23</option>"+
                                                				"<option value = '24'>24</option>"+
                                                				"<option value = '25'>25</option>"+
                                                				"<option value = '26'>26</option>"+
                                                				"<option value = '27'>27</option>"+
                                                				"<option value = '28'>28</option>"+
                                                				"<option value = '29'>29</option>"+
                                                				"<option value = '30'>30</option>"+
                                                				"<option value = '31'>31</option>";
				document.sched_snapshot.mins.disabled   = true;
				document.sched_snapshot.hours.disabled  = true;
				document.sched_snapshot.e_hour.disabled = true;
				document.sched_snapshot.e_min.disabled  = true;
				document.sched_snapshot.month.disabled  = true;
			}

			else
			{
				for (i = 0;  i < week_array.length;  i++)
				{
					week_array[i].disabled = false;
				}

				document.getElementById('id_schedule_day').innerHTML =
										"<option value = '*'>*</option>"+
                                                				"<option value = '0'>0</option>"+
                                                				"<option value = '1'>1</option>"+
                                                				"<option value = '2'>2</option>"+
				                                                "<option value = '3'>3</option>"+
                                                				"<option value = '4'>4</option>"+
                                                				"<option value = '5'>5</option>"+
                                                				"<option value = '6'>6</option>"+
                                                				"<option value = '7'>7</option>"+
                                                				"<option value = '8'>8</option>"+
                                                				"<option value = '9'>9</option>"+
                                                				"<option value = '10'>10</option>"+
                                                				"<option value = '11'>11</option>"+
                                                				"<option value = '12'>12</option>"+
                                                				"<option value = '13'>13</option>"+
                                                				"<option value = '14'>14</option>"+
                                                				"<option value = '15'>15</option>"+
                                                				"<option value = '16'>16</option>"+
                                                				"<option value = '17'>17</option>"+
                                                				"<option value = '18'>18</option>"+
                                                				"<option value = '19'>19</option>"+
                                                				"<option value = '20'>20</option>"+
                                                				"<option value = '21'>21</option>"+
                                                				"<option value = '22'>22</option>"+
                                                				"<option value = '23'>23</option>"+
                                                				"<option value = '24'>24</option>"+
                                                				"<option value = '25'>25</option>"+
                                                				"<option value = '26'>26</option>"+
                                                				"<option value = '27'>27</option>"+
                                                				"<option value = '28'>28</option>"+
                                                				"<option value = '29'>29</option>"+
                                                				"<option value = '30'>30</option>"+
                                                				"<option value = '31'>31</option>";
				document.sched_snapshot.hours.disabled  = false;
				document.sched_snapshot.mins.disabled   = false;
				document.sched_snapshot.e_hour.disabled = false;
				document.sched_snapshot.e_min.disabled  = false;
				document.sched_snapshot.month.disabled  = false;
			}
		}
	}

	if (type == 'SHUT')
	{
		if (element == 'nhours')
		{
			for (i = 0;  i < week_array.length;  i++)
			{
				week_array[i].disabled = true;
			}

			if (document.sched_shutdown.e_hour.checked == true)
			{
				document.getElementById('id_select_hours').innerHTML =
										"<option value = '1'>1</option>"+
                                                				"<option value = '2'>2</option>"+
				                                                "<option value = '3'>3</option>"+
                                                				"<option value = '4'>4</option>"+
                                                				"<option value = '5'>5</option>"+
                                                				"<option value = '6'>6</option>"+
                                                				"<option value = '7'>7</option>"+
                                                				"<option value = '8'>8</option>"+
                                                				"<option value = '9'>9</option>"+
                                                				"<option value = '10'>10</option>"+
                                                				"<option value = '11'>11</option>"+
                                                				"<option value = '12'>12</option>"+
                                                				"<option value = '13'>13</option>"+
                                                				"<option value = '14'>14</option>"+
                                                				"<option value = '15'>15</option>"+
                                                				"<option value = '16'>16</option>"+
                                                				"<option value = '17'>17</option>"+
                                                				"<option value = '18'>18</option>"+
                                                				"<option value = '19'>19</option>"+
                                                				"<option value = '20'>20</option>"+
                                                				"<option value = '21'>21</option>"+
                                                				"<option value = '22'>22</option>"+
                                                				"<option value = '23'>23</option>";
				document.sched_shutdown.mins.disabled  = true;
				document.sched_shutdown.day.disabled   = true;
				document.sched_shutdown.e_day.disabled = true;
				document.sched_shutdown.e_min.disabled = true;
				document.sched_shutdown.month.disabled = true;
			}

			else
			{
				for (i = 0;  i < week_array.length;  i++)
				{
					week_array[i].disabled = false;

					if (week_array[i].checked)
					{
						week_val = week_array[i].value;
					}
				}

				document.getElementById('id_select_hours').innerHTML =
										"<option value = '*'>*</option>"+
                                                				"<option value = '0'>0</option>"+
                                                				"<option value = '1'>1</option>"+
                                                				"<option value = '2'>2</option>"+
				                                                "<option value = '3'>3</option>"+
                                                				"<option value = '4'>4</option>"+
                                                				"<option value = '5'>5</option>"+
                                                				"<option value = '6'>6</option>"+
                                                				"<option value = '7'>7</option>"+
                                                				"<option value = '8'>8</option>"+
                                                				"<option value = '9'>9</option>"+
                                                				"<option value = '10'>10</option>"+
                                                				"<option value = '11'>11</option>"+
                                                				"<option value = '12'>12</option>"+
                                                				"<option value = '13'>13</option>"+
                                                				"<option value = '14'>14</option>"+
                                                				"<option value = '15'>15</option>"+
                                                				"<option value = '16'>16</option>"+
                                                				"<option value = '17'>17</option>"+
                                                				"<option value = '18'>18</option>"+
                                                				"<option value = '19'>19</option>"+
                                                				"<option value = '20'>20</option>"+
                                                				"<option value = '21'>21</option>"+
                                                				"<option value = '22'>22</option>"+
                                                				"<option value = '23'>23</option>";
				document.sched_shutdown.mins.disabled  = false;
			
				if (week_val == '*')
				{
					document.sched_shutdown.day.disabled   = false;
					document.sched_shutdown.e_day.disabled = false;
				}
		
				else
				{
					document.sched_shutdown.day.disabled   = true;
					document.sched_shutdown.e_day.disabled = true;
				}

				document.sched_shutdown.e_min.disabled = false;
				document.sched_shutdown.month.disabled = false;
			}
		}

		if (element == 'nmins')
		{
			for (i = 0;  i < week_array.length;  i++)
			{
				week_array[i].disabled = true;
			}

			if (document.sched_shutdown.e_min.checked == true)
			{
				document.getElementById('id_select_mins').innerHTML =
										"<option value = '1'>1</option>"+
                                                				"<option value = '2'>2</option>"+
				                                                "<option value = '3'>3</option>"+
                                                				"<option value = '4'>4</option>"+
                                                				"<option value = '5'>5</option>"+
                                                				"<option value = '6'>6</option>"+
                                                				"<option value = '7'>7</option>"+
                                                				"<option value = '8'>8</option>"+
                                                				"<option value = '9'>9</option>"+
                                                				"<option value = '10'>10</option>"+
                                                				"<option value = '11'>11</option>"+
                                                				"<option value = '12'>12</option>"+
                                                				"<option value = '13'>13</option>"+
                                                				"<option value = '14'>14</option>"+
                                                				"<option value = '15'>15</option>"+
                                                				"<option value = '16'>16</option>"+
                                                				"<option value = '17'>17</option>"+
                                                				"<option value = '18'>18</option>"+
                                                				"<option value = '19'>19</option>"+
                                                				"<option value = '20'>20</option>"+
                                                				"<option value = '21'>21</option>"+
                                                				"<option value = '22'>22</option>"+
                                                				"<option value = '23'>23</option>"+
                                                				"<option value = '24'>24</option>"+
                                                				"<option value = '25'>25</option>"+
                                                				"<option value = '26'>26</option>"+
                                                				"<option value = '27'>27</option>"+
                                                				"<option value = '28'>28</option>"+
                                                				"<option value = '29'>29</option>"+
                                                				"<option value = '30'>30</option>"+
                                                				"<option value = '31'>31</option>"+
                                                				"<option value = '32'>32</option>"+
                                                				"<option value = '33'>33</option>"+
                                                				"<option value = '34'>34</option>"+
                                                				"<option value = '35'>35</option>"+
                                                				"<option value = '36'>36</option>"+
                                                				"<option value = '37'>37</option>"+
                                                				"<option value = '38'>38</option>"+
                                                				"<option value = '39'>39</option>"+
                                                				"<option value = '40'>40</option>"+
                                                				"<option value = '41'>41</option>"+
                                                				"<option value = '42'>42</option>"+
                                                				"<option value = '43'>43</option>"+
                                                				"<option value = '44'>44</option>"+
                                                				"<option value = '45'>45</option>"+
                                                				"<option value = '46'>46</option>"+
                                                				"<option value = '47'>47</option>"+
                                                				"<option value = '48'>48</option>"+
                                                				"<option value = '49'>49</option>"+
                                                				"<option value = '50'>50</option>"+
                                                				"<option value = '51'>51</option>"+
                                                				"<option value = '52'>52</option>"+
                                                				"<option value = '53'>53</option>"+
                                                				"<option value = '54'>54</option>"+
                                                				"<option value = '55'>55</option>"+
                                                				"<option value = '56'>56</option>"+
                                                				"<option value = '57'>57</option>"+
                                                				"<option value = '58'>58</option>"+
                                                				"<option value = '59'>59</option>";
				document.sched_shutdown.hours.disabled  = true;
				document.sched_shutdown.day.disabled    = true;
				document.sched_shutdown.e_day.disabled  = true;
				document.sched_shutdown.e_hour.disabled = true;
				document.sched_shutdown.month.disabled  = true;
			}

			else
			{
				for (i = 0;  i < week_array.length;  i++)
				{
					week_array[i].disabled = false;

					if (week_array[i].checked)
					{
						week_val = week_array[i].value;
					}
				}

				document.getElementById('id_select_mins').innerHTML =
										"<option value = '*'>*</option>"+
                                                				"<option value = '0'>0</option>"+
                                                				"<option value = '1'>1</option>"+
                                                				"<option value = '2'>2</option>"+
				                                                "<option value = '3'>3</option>"+
                                                				"<option value = '4'>4</option>"+
                                                				"<option value = '5'>5</option>"+
                                                				"<option value = '6'>6</option>"+
                                                				"<option value = '7'>7</option>"+
                                                				"<option value = '8'>8</option>"+
                                                				"<option value = '9'>9</option>"+
                                                				"<option value = '10'>10</option>"+
                                                				"<option value = '11'>11</option>"+
                                                				"<option value = '12'>12</option>"+
                                                				"<option value = '13'>13</option>"+
                                                				"<option value = '14'>14</option>"+
                                                				"<option value = '15'>15</option>"+
                                                				"<option value = '16'>16</option>"+
                                                				"<option value = '17'>17</option>"+
                                                				"<option value = '18'>18</option>"+
                                                				"<option value = '19'>19</option>"+
                                                				"<option value = '20'>20</option>"+
                                                				"<option value = '21'>21</option>"+
                                                				"<option value = '22'>22</option>"+
                                                				"<option value = '23'>23</option>"+
                                                				"<option value = '24'>24</option>"+
                                                				"<option value = '25'>25</option>"+
                                                				"<option value = '26'>26</option>"+
                                                				"<option value = '27'>27</option>"+
                                                				"<option value = '28'>28</option>"+
                                                				"<option value = '29'>29</option>"+
                                                				"<option value = '30'>30</option>"+
                                                				"<option value = '31'>31</option>"+
                                                				"<option value = '32'>32</option>"+
                                                				"<option value = '33'>33</option>"+
                                                				"<option value = '34'>34</option>"+
                                                				"<option value = '35'>35</option>"+
                                                				"<option value = '36'>36</option>"+
                                                				"<option value = '37'>37</option>"+
                                                				"<option value = '38'>38</option>"+
                                                				"<option value = '39'>39</option>"+
                                                				"<option value = '40'>40</option>"+
                                                				"<option value = '41'>41</option>"+
                                                				"<option value = '42'>42</option>"+
                                                				"<option value = '43'>43</option>"+
                                                				"<option value = '44'>44</option>"+
                                                				"<option value = '45'>45</option>"+
                                                				"<option value = '46'>46</option>"+
                                                				"<option value = '47'>47</option>"+
                                                				"<option value = '48'>48</option>"+
                                                				"<option value = '49'>49</option>"+
                                                				"<option value = '50'>50</option>"+
                                                				"<option value = '51'>51</option>"+
                                                				"<option value = '52'>52</option>"+
                                                				"<option value = '53'>53</option>"+
                                                				"<option value = '54'>54</option>"+
                                                				"<option value = '55'>55</option>"+
                                                				"<option value = '56'>56</option>"+
                                                				"<option value = '57'>57</option>"+
                                                				"<option value = '58'>58</option>"+
                                                				"<option value = '59'>59</option>";
				document.sched_shutdown.hours.disabled  = false;

				if (week_val == '*')
				{
					document.sched_shutdown.day.disabled    = false;
					document.sched_shutdown.e_day.disabled  = false;
				}

				else
				{
					document.sched_shutdown.day.disabled    = true;
					document.sched_shutdown.e_day.disabled  = true;
				}

				document.sched_shutdown.e_hour.disabled  = false;
				document.sched_shutdown.month.disabled  = false;
			}
		}

		if (element == 'ndays')
		{
			for (i = 0;  i < week_array.length;  i++)
			{
				week_array[i].disabled = true;
			}

			if (document.sched_shutdown.e_day.checked == true)
			{
				document.getElementById('id_schedule_day').innerHTML =
										"<option value = '1'>1</option>"+
                                                				"<option value = '2'>2</option>"+
				                                                "<option value = '3'>3</option>"+
                                                				"<option value = '4'>4</option>"+
                                                				"<option value = '5'>5</option>"+
                                                				"<option value = '6'>6</option>"+
                                                				"<option value = '7'>7</option>"+
                                                				"<option value = '8'>8</option>"+
                                                				"<option value = '9'>9</option>"+
                                                				"<option value = '10'>10</option>"+
                                                				"<option value = '11'>11</option>"+
                                                				"<option value = '12'>12</option>"+
                                                				"<option value = '13'>13</option>"+
                                                				"<option value = '14'>14</option>"+
                                                				"<option value = '15'>15</option>"+
                                                				"<option value = '16'>16</option>"+
                                                				"<option value = '17'>17</option>"+
                                                				"<option value = '18'>18</option>"+
                                                				"<option value = '19'>19</option>"+
                                                				"<option value = '20'>20</option>"+
                                                				"<option value = '21'>21</option>"+
                                                				"<option value = '22'>22</option>"+
                                                				"<option value = '23'>23</option>"+
                                                				"<option value = '24'>24</option>"+
                                                				"<option value = '25'>25</option>"+
                                                				"<option value = '26'>26</option>"+
                                                				"<option value = '27'>27</option>"+
                                                				"<option value = '28'>28</option>"+
                                                				"<option value = '29'>29</option>"+
                                                				"<option value = '30'>30</option>"+
                                                				"<option value = '31'>31</option>";
				document.sched_shutdown.mins.disabled   = true;
				document.sched_shutdown.hours.disabled  = true;
				document.sched_shutdown.e_hour.disabled = true;
				document.sched_shutdown.e_min.disabled  = true;
				document.sched_shutdown.month.disabled  = true;
			}

			else
			{
				for (i = 0;  i < week_array.length;  i++)
				{
					week_array[i].disabled = false;
				}

				document.getElementById('id_schedule_day').innerHTML =
										"<option value = '*'>*</option>"+
                                                				"<option value = '0'>0</option>"+
                                                				"<option value = '1'>1</option>"+
                                                				"<option value = '2'>2</option>"+
				                                                "<option value = '3'>3</option>"+
                                                				"<option value = '4'>4</option>"+
                                                				"<option value = '5'>5</option>"+
                                                				"<option value = '6'>6</option>"+
                                                				"<option value = '7'>7</option>"+
                                                				"<option value = '8'>8</option>"+
                                                				"<option value = '9'>9</option>"+
                                                				"<option value = '10'>10</option>"+
                                                				"<option value = '11'>11</option>"+
                                                				"<option value = '12'>12</option>"+
                                                				"<option value = '13'>13</option>"+
                                                				"<option value = '14'>14</option>"+
                                                				"<option value = '15'>15</option>"+
                                                				"<option value = '16'>16</option>"+
                                                				"<option value = '17'>17</option>"+
                                                				"<option value = '18'>18</option>"+
                                                				"<option value = '19'>19</option>"+
                                                				"<option value = '20'>20</option>"+
                                                				"<option value = '21'>21</option>"+
                                                				"<option value = '22'>22</option>"+
                                                				"<option value = '23'>23</option>"+
                                                				"<option value = '24'>24</option>"+
                                                				"<option value = '25'>25</option>"+
                                                				"<option value = '26'>26</option>"+
                                                				"<option value = '27'>27</option>"+
                                                				"<option value = '28'>28</option>"+
                                                				"<option value = '29'>29</option>"+
                                                				"<option value = '30'>30</option>"+
                                                				"<option value = '31'>31</option>";
				document.sched_shutdown.hours.disabled  = false;
				document.sched_shutdown.mins.disabled   = false;
				document.sched_shutdown.e_hour.disabled = false;
				document.sched_shutdown.e_min.disabled  = false;
				document.sched_shutdown.month.disabled  = false;
			}
		}
	}

	if (type == 'REST')
	{
		if (element == 'nhours')
		{
			for (i = 0;  i < week_array.length;  i++)
			{
				week_array[i].disabled = true;
			}

			if (document.sched_restart.e_hour.checked == true)
			{
				document.getElementById('id_select_r_hours').innerHTML =
										"<option value = '1'>1</option>"+
                                                				"<option value = '2'>2</option>"+
				                                                "<option value = '3'>3</option>"+
                                                				"<option value = '4'>4</option>"+
                                                				"<option value = '5'>5</option>"+
                                                				"<option value = '6'>6</option>"+
                                                				"<option value = '7'>7</option>"+
                                                				"<option value = '8'>8</option>"+
                                                				"<option value = '9'>9</option>"+
                                                				"<option value = '10'>10</option>"+
                                                				"<option value = '11'>11</option>"+
                                                				"<option value = '12'>12</option>"+
                                                				"<option value = '13'>13</option>"+
                                                				"<option value = '14'>14</option>"+
                                                				"<option value = '15'>15</option>"+
                                                				"<option value = '16'>16</option>"+
                                                				"<option value = '17'>17</option>"+
                                                				"<option value = '18'>18</option>"+
                                                				"<option value = '19'>19</option>"+
                                                				"<option value = '20'>20</option>"+
                                                				"<option value = '21'>21</option>"+
                                                				"<option value = '22'>22</option>"+
                                                				"<option value = '23'>23</option>";
				document.sched_restart.mins.disabled  = true;
				document.sched_restart.day.disabled   = true;
				document.sched_restart.e_min.disabled = true;
				document.sched_restart.e_day.disabled = true;
				document.sched_restart.month.disabled = true;
			}

			else
			{
				for (i = 0;  i < week_array.length;  i++)
				{
					week_array[i].disabled = false;
					
					if (week_array[i].checked)
					{
						week_val = week_array[i].value;
					}
				}

				document.getElementById('id_select_r_hours').innerHTML =
										"<option value = '*'>*</option>"+
                                                				"<option value = '0'>0</option>"+
                                                				"<option value = '1'>1</option>"+
                                                				"<option value = '2'>2</option>"+
				                                                "<option value = '3'>3</option>"+
                                                				"<option value = '4'>4</option>"+
                                                				"<option value = '5'>5</option>"+
                                                				"<option value = '6'>6</option>"+
                                                				"<option value = '7'>7</option>"+
                                                				"<option value = '8'>8</option>"+
                                                				"<option value = '9'>9</option>"+
                                                				"<option value = '10'>10</option>"+
                                                				"<option value = '11'>11</option>"+
                                                				"<option value = '12'>12</option>"+
                                                				"<option value = '13'>13</option>"+
                                                				"<option value = '14'>14</option>"+
                                                				"<option value = '15'>15</option>"+
                                                				"<option value = '16'>16</option>"+
                                                				"<option value = '17'>17</option>"+
                                                				"<option value = '18'>18</option>"+
                                                				"<option value = '19'>19</option>"+
                                                				"<option value = '20'>20</option>"+
                                                				"<option value = '21'>21</option>"+
                                                				"<option value = '22'>22</option>"+
                                                				"<option value = '23'>23</option>";
				document.sched_restart.mins.disabled  = false;

				if (week_val == '*')
				{
					document.sched_restart.day.disabled   = false;
					document.sched_restart.e_day.disabled = false;
				}

				else
				{
					document.sched_restart.day.disabled   = true;
					document.sched_restart.e_day.disabled = true;
				}

				document.sched_restart.e_min.disabled = false;
				document.sched_restart.month.disabled = false;
			}
		}

		if (element == 'nmins')
		{
			for (i = 0;  i < week_array.length;  i++)
			{
				week_array[i].disabled = true;
			}

			if (document.sched_restart.e_min.checked == true)
			{
				document.getElementById('id_select_r_mins').innerHTML =
										"<option value = '1'>1</option>"+
                                                				"<option value = '2'>2</option>"+
				                                                "<option value = '3'>3</option>"+
                                                				"<option value = '4'>4</option>"+
                                                				"<option value = '5'>5</option>"+
                                                				"<option value = '6'>6</option>"+
                                                				"<option value = '7'>7</option>"+
                                                				"<option value = '8'>8</option>"+
                                                				"<option value = '9'>9</option>"+
                                                				"<option value = '10'>10</option>"+
                                                				"<option value = '11'>11</option>"+
                                                				"<option value = '12'>12</option>"+
                                                				"<option value = '13'>13</option>"+
                                                				"<option value = '14'>14</option>"+
                                                				"<option value = '15'>15</option>"+
                                                				"<option value = '16'>16</option>"+
                                                				"<option value = '17'>17</option>"+
                                                				"<option value = '18'>18</option>"+
                                                				"<option value = '19'>19</option>"+
                                                				"<option value = '20'>20</option>"+
                                                				"<option value = '21'>21</option>"+
                                                				"<option value = '22'>22</option>"+
                                                				"<option value = '23'>23</option>"+
                                                				"<option value = '24'>24</option>"+
                                                				"<option value = '25'>25</option>"+
                                                				"<option value = '26'>26</option>"+
                                                				"<option value = '27'>27</option>"+
                                                				"<option value = '28'>28</option>"+
                                                				"<option value = '29'>29</option>"+
                                                				"<option value = '30'>30</option>"+
                                                				"<option value = '31'>31</option>"+
                                                				"<option value = '32'>32</option>"+
                                                				"<option value = '33'>33</option>"+
                                                				"<option value = '34'>34</option>"+
                                                				"<option value = '35'>35</option>"+
                                                				"<option value = '36'>36</option>"+
                                                				"<option value = '37'>37</option>"+
                                                				"<option value = '38'>38</option>"+
                                                				"<option value = '39'>39</option>"+
                                                				"<option value = '40'>40</option>"+
                                                				"<option value = '41'>41</option>"+
                                                				"<option value = '42'>42</option>"+
                                                				"<option value = '43'>43</option>"+
                                                				"<option value = '44'>44</option>"+
                                                				"<option value = '45'>45</option>"+
                                                				"<option value = '46'>46</option>"+
                                                				"<option value = '47'>47</option>"+
                                                				"<option value = '48'>48</option>"+
                                                				"<option value = '49'>49</option>"+
                                                				"<option value = '50'>50</option>"+
                                                				"<option value = '51'>51</option>"+
                                                				"<option value = '52'>52</option>"+
                                                				"<option value = '53'>53</option>"+
                                                				"<option value = '54'>54</option>"+
                                                				"<option value = '55'>55</option>"+
                                                				"<option value = '56'>56</option>"+
                                                				"<option value = '57'>57</option>"+
                                                				"<option value = '58'>58</option>"+
                                                				"<option value = '59'>59</option>";
				document.sched_restart.hours.disabled  = true;
				document.sched_restart.day.disabled    = true;
				document.sched_restart.e_day.disabled  = true;
				document.sched_restart.e_hour.disabled = true;
				document.sched_restart.month.disabled  = true;
			}

			else
			{
				for (i = 0;  i < week_array.length;  i++)
				{
					week_array[i].disabled = false;

					if (week_array[i].checked)
					{
						week_val = week_array[i].value;
					}
				}

				document.getElementById('id_select_r_mins').innerHTML =
										"<option value = '*'>*</option>"+
                                                				"<option value = '0'>0</option>"+
                                                				"<option value = '1'>1</option>"+
                                                				"<option value = '2'>2</option>"+
				                                                "<option value = '3'>3</option>"+
                                                				"<option value = '4'>4</option>"+
                                                				"<option value = '5'>5</option>"+
                                                				"<option value = '6'>6</option>"+
                                                				"<option value = '7'>7</option>"+
                                                				"<option value = '8'>8</option>"+
                                                				"<option value = '9'>9</option>"+
                                                				"<option value = '10'>10</option>"+
                                                				"<option value = '11'>11</option>"+
                                                				"<option value = '12'>12</option>"+
                                                				"<option value = '13'>13</option>"+
                                                				"<option value = '14'>14</option>"+
                                                				"<option value = '15'>15</option>"+
                                                				"<option value = '16'>16</option>"+
                                                				"<option value = '17'>17</option>"+
                                                				"<option value = '18'>18</option>"+
                                                				"<option value = '19'>19</option>"+
                                                				"<option value = '20'>20</option>"+
                                                				"<option value = '21'>21</option>"+
                                                				"<option value = '22'>22</option>"+
                                                				"<option value = '23'>23</option>"+
                                                				"<option value = '24'>24</option>"+
                                                				"<option value = '25'>25</option>"+
                                                				"<option value = '26'>26</option>"+
                                                				"<option value = '27'>27</option>"+
                                                				"<option value = '28'>28</option>"+
                                                				"<option value = '29'>29</option>"+
                                                				"<option value = '30'>30</option>"+
                                                				"<option value = '31'>31</option>"+
                                                				"<option value = '32'>32</option>"+
                                                				"<option value = '33'>33</option>"+
                                                				"<option value = '34'>34</option>"+
                                                				"<option value = '35'>35</option>"+
                                                				"<option value = '36'>36</option>"+
                                                				"<option value = '37'>37</option>"+
                                                				"<option value = '38'>38</option>"+
                                                				"<option value = '39'>39</option>"+
                                                				"<option value = '40'>40</option>"+
                                                				"<option value = '41'>41</option>"+
                                                				"<option value = '42'>42</option>"+
                                                				"<option value = '43'>43</option>"+
                                                				"<option value = '44'>44</option>"+
                                                				"<option value = '45'>45</option>"+
                                                				"<option value = '46'>46</option>"+
                                                				"<option value = '47'>47</option>"+
                                                				"<option value = '48'>48</option>"+
                                                				"<option value = '49'>49</option>"+
                                                				"<option value = '50'>50</option>"+
                                                				"<option value = '51'>51</option>"+
                                                				"<option value = '52'>52</option>"+
                                                				"<option value = '53'>53</option>"+
                                                				"<option value = '54'>54</option>"+
                                                				"<option value = '55'>55</option>"+
                                                				"<option value = '56'>56</option>"+
                                                				"<option value = '57'>57</option>"+
                                                				"<option value = '58'>58</option>"+
                                                				"<option value = '59'>59</option>";
				document.sched_restart.hours.disabled  = false;

				if (week_val == '*')
				{
					document.sched_restart.day.disabled    = false;
					document.sched_restart.e_day.disabled  = false;
				}

				else
				{
					document.sched_restart.day.disabled    = true;
					document.sched_restart.e_day.disabled  = true;
				}

				document.sched_restart.e_hour.disabled = false;
				document.sched_restart.month.disabled  = false;
			}
		}

		if (element == 'ndays')
		{
			for (i = 0;  i < week_array.length;  i++)
			{
				week_array[i].disabled = true;
			}

			if (document.sched_restart.e_day.checked == true)
			{
				document.getElementById('r_id_schedule_day').innerHTML =
										"<option value = '1'>1</option>"+
                                                				"<option value = '2'>2</option>"+
				                                                "<option value = '3'>3</option>"+
                                                				"<option value = '4'>4</option>"+
                                                				"<option value = '5'>5</option>"+
                                                				"<option value = '6'>6</option>"+
                                                				"<option value = '7'>7</option>"+
                                                				"<option value = '8'>8</option>"+
                                                				"<option value = '9'>9</option>"+
                                                				"<option value = '10'>10</option>"+
                                                				"<option value = '11'>11</option>"+
                                                				"<option value = '12'>12</option>"+
                                                				"<option value = '13'>13</option>"+
                                                				"<option value = '14'>14</option>"+
                                                				"<option value = '15'>15</option>"+
                                                				"<option value = '16'>16</option>"+
                                                				"<option value = '17'>17</option>"+
                                                				"<option value = '18'>18</option>"+
                                                				"<option value = '19'>19</option>"+
                                                				"<option value = '20'>20</option>"+
                                                				"<option value = '21'>21</option>"+
                                                				"<option value = '22'>22</option>"+
                                                				"<option value = '23'>23</option>"+
                                                				"<option value = '24'>24</option>"+
                                                				"<option value = '25'>25</option>"+
                                                				"<option value = '26'>26</option>"+
                                                				"<option value = '27'>27</option>"+
                                                				"<option value = '28'>28</option>"+
                                                				"<option value = '29'>29</option>"+
                                                				"<option value = '30'>30</option>"+
                                                				"<option value = '31'>31</option>";
				document.sched_restart.mins.disabled   = true;
				document.sched_restart.hours.disabled  = true;
				document.sched_restart.e_hour.disabled = true;
				document.sched_restart.e_min.disabled  = true;
				document.sched_restart.month.disabled  = true;
			}

			else
			{
				for (i = 0;  i < week_array.length;  i++)
				{
					week_array[i].disabled = false;
				}

				document.getElementById('r_id_schedule_day').innerHTML =
										"<option value = '*'>*</option>"+
                                                				"<option value = '0'>0</option>"+
                                                				"<option value = '1'>1</option>"+
                                                				"<option value = '2'>2</option>"+
				                                                "<option value = '3'>3</option>"+
                                                				"<option value = '4'>4</option>"+
                                                				"<option value = '5'>5</option>"+
                                                				"<option value = '6'>6</option>"+
                                                				"<option value = '7'>7</option>"+
                                                				"<option value = '8'>8</option>"+
                                                				"<option value = '9'>9</option>"+
                                                				"<option value = '10'>10</option>"+
                                                				"<option value = '11'>11</option>"+
                                                				"<option value = '12'>12</option>"+
                                                				"<option value = '13'>13</option>"+
                                                				"<option value = '14'>14</option>"+
                                                				"<option value = '15'>15</option>"+
                                                				"<option value = '16'>16</option>"+
                                                				"<option value = '17'>17</option>"+
                                                				"<option value = '18'>18</option>"+
                                                				"<option value = '19'>19</option>"+
                                                				"<option value = '20'>20</option>"+
                                                				"<option value = '21'>21</option>"+
                                                				"<option value = '22'>22</option>"+
                                                				"<option value = '23'>23</option>"+
                                                				"<option value = '24'>24</option>"+
                                                				"<option value = '25'>25</option>"+
                                                				"<option value = '26'>26</option>"+
                                                				"<option value = '27'>27</option>"+
                                                				"<option value = '28'>28</option>"+
                                                				"<option value = '29'>29</option>"+
                                                				"<option value = '30'>30</option>"+
                                                				"<option value = '31'>31</option>";
				document.sched_restart.hours.disabled  = false;
				document.sched_restart.mins.disabled   = false;
				document.sched_restart.e_hour.disabled = false;
				document.sched_restart.e_min.disabled  = false;
				document.sched_restart.month.disabled  = false;
			}
		}
	}
}

function validate_create_passthrough_form()
{
	var options_array  = document.getElementsByName('disk');
	var options_string = '';

	for (i = 0;  i < options_array.length;  i++)
	{
		if (options_array[i].checked)
		{
			options_string += options_array[i].value;
		}
	}

	if (options_string == '')
	{
		alert('You need to choose a disk for passthrough!');
		return false;
	}
}

function confirm_offset_raid()
{
	var options_array  = document.getElementsByName('raid_set');
	var options_string = '';

	for (i = 0;  i < options_array.length;  i++)
	{
		if (options_array[i].checked)
		{
			options_string += options_array[i].value;
		}
	}

	if (options_string == '')
	{
		alert('You need to choose a raid set to make offline!');
		return false;
	}
}

function confirm_activate_raidset()
{
	var options_array  = document.getElementsByName('raid_set');
	var options_string = '';

	for (i = 0;  i < options_array.length;  i++)
	{
		if (options_array[i].checked)
		{
			options_string += options_array[i].value;
		}
	}

	if (options_string == '')
	{
		alert('You need to choose a raidset!');
		return false;
	}
}

function validate_create_volumeset()
{
	var options_array  = document.getElementsByName('raid_set');
	var options_string = '';

	for (i = 0;  i < options_array.length;  i++)
	{
		if (options_array[i].checked)
		{
			options_string += options_array[i].value;
		}
	}
	
	if (options_string == '')
	{
		alert('Choose a raidset!');
		return false;
	}
}

/*function disable_forms_all(flag)
{
	if (flag != '')
	{
		var form_count = document.forms.length;

		for (i = 0;  i < form_count;  i++)
		{
			var elem_count = document.forms[i].elements.length;

			for (j = 0;  j < elem_count;  j++)
			{
				document.forms[i].elements[j].disabled = true;
			}
		}
	}
}*/

function close_error_message()
{
	document.getElementById("id_result").style.display = "none";
	
	/*var form_count = document.forms.length;

	for (i = 0;  i < form_count;  i++)
	{
		var elem_count = document.forms[i].elements.length;

		for (j = 0;  j < elem_count;  j++)
		{
			document.forms[i].elements[j].disabled = 'false';
		}
	}*/
}

function show_hide(click, hide)
{
	if (click == true)
	{
		hide.style.display = 'block';
	}

	else
	{
		hide.style.display = 'none';
	}
}

function enable_smb_log_path(log_path)
{
	var share = document.smb_log_path.hid_share.value;
	var path  = document.smb_log_path.hid_path.value;

	if (log_path != "")
	{
		var response = confirm('SMB will restart causing interruption in the connection! Do you wish to continue?');

		if (response == true)
		{
			document.getElementById('wait').style.display = 'block';

			$.ajax(
			{
				type: 'POST',
				url: 'enable_log_path.php',
				data: 'log_path='+log_path+'&sn='+share+'&sp='+path,

				success: function(html)
				{
					$('#response').html(html);
				}
			});
		}

		else
		{
			return false;
		}
	}

	else
	{
		alert('You need to choose a path for log!');
		return false;
	}
}

function do_rotate_log(freq_rotate, size)
{
	var select_conf_file = document.rotate_log.avail_users.value;
	var select_gb = document.rotate_log.set_freq.value;
        var logs_rotate = document.rotate_log.freq_rotate.value;
        var logs_size = document.rotate_log.size.value;
	var fetch_allcheck_value = document.rotate_log.check.checked;

        if(fetch_allcheck_value != true)
        {
		
	

	 if (select_conf_file == '')
        {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 11%; padding-top: 4%; font-family: status-bar;"> Configuration Name is required.</div>', 'Alert Dialog');

                document.rotate_log.avail_users.focus();
                return false;
        }
}


        if (select_gb == '')
        {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 23%; padding-top: 4%; font-family: status-bar;"> Frequency is required.</div>', 'Alert Dialog');

                document.rotate_log.set_freq.focus();
                return false;
        }

	  if (logs_rotate == '')
        {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 42%; padding-top: 4%; font-family: status-bar;"> Log Rotate is required.</div>', 'Alert Dialog');

                document.rotate_log.freq_rotate.focus();
                return false;
        }


	  if (logs_size == '')
        {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 29%; padding-top: 4%; font-family: status-bar;"> Log Size is required.</div>', 'Alert Dialog');

                document.rotate_log.size.focus();
                return false;
        }


/*
	size = size + 'M';

	document.getElementById('wait').style.display = 'block';

	$.ajax(
	{
		type: 'POST',
		url: 'rotate_logs.php',
		data: 'freq='+freq+'&size='+size,

		success: function(html)
		{
			$('#response').html(html);
		}
	});*/
}

function confirm_enter_model(serial, model, date, page)
{
	if (page == 'sys' && (serial == '' || model == ''))
	{
		var response = confirm('Model/Serial/Date data is missing. Click \'OK\' to enter the Model/Serial/Date. Click \'Cancel\' to continue without Model/Serial/Date.');

		if (response == true)
		{
			location.href = '../mlogistics/php/mlogin.php?s='+serial+'&m='+model+'&d='+date;
		}

		else
		{
			return false;
		}
	}
}

function set_acl_params(path, page)
{
	if (path != '')
	{
		location.href = 'main.py?page=share_det&pacl='+path+'&act=share_acl_done';
	}
}

function get_docs()
{
	document.getElementById('wait').style.display = 'block';

	$.ajax(
	{
		type: 'POST',
		url: 'downloaddocs.php',
		data: 'proceed=yes',

		success: function(html)
		{
			$('#response').html(html);
		}
	});
}

/*function post(dest, params)
{
	if (window.XMLHttpRequest)
	{
		xmlhttp=new XMLHttpRequest();
	}

	xmlhttp.onreadystatechange=function()
	{
        	if (xmlhttp.readyState==0)
                {
                    return xmlhttp.responseText;
                }
        }

	xmlhttp.open("POST",dest,true);
        xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
        xmlhttp.send( params ); 
}*/

function test_luck()
{
	document.getElementById('wait').style.display = 'block';

	var name = document.testform.text1.value;

	$.ajax(
	{
		type: 'post',
		url: 'testajaxact.py',
		data: 'name='+name,

		success: function(html)
		{
			$('#response').html(html);
		}
	});
}

function enable_disable_button(one, two, three, recursive)
{
	parent.document.users_groups_frame.users_groups.granted_ug.background = '#BDBDBD';
}

function validate_sw_update(action, file)
{
	if (file == '')
	{
		alert('You need to choose a file!');
		return false;
	}

	document.getElementById('wait').style.display = 'block';

	$.ajax(
	{
		type: 'POST',
		url: 'file_upload.py',
		data: 'act='+action+'&file='+file,

		success: function(html)
		{
			$('#response').html(html);
		}
	});
}

function download_file()
{
	location.href = 'download.py';
}

function showhide()
{
	if (document.getElementById('id_showmore').value == '+')
	{
		document.getElementById('err_div').style.display = 'block';
		document.getElementById('id_showmore').value = '-';
	}

	else if (document.getElementById('id_showmore').value == '-')
	{
		document.getElementById('err_div').style.display = 'none';
		document.getElementById('id_showmore').value = '+';
	}
}

function update_to_file(string)
{
	document.getElementById('wait').style.display = 'table';
	document.error_form.submit();

	/*$.ajax(
	{
		type: 'POST',
		url: 'do_write_logs.py',
		data: 'str=' + string,

		success: function(html)
		{
			$('#response').html(html);
		}
	});*/
}

function select_all_entries(check_all_option, elems_array, delete_id)
{
        if (elems_array.length == undefined)
        {
                if (check_all_option.checked == true)
                {
                        if (delete_id.disabled != true)
                        {
                                delete_id.checked = true;
                        }
                }

                else
                {
                        delete_id.checked = false;
                }
        }

        if (check_all_option.checked == true)
        {
                for (i = 0;  i < elems_array.length;  i++)
                {
                        if (elems_array[i].disabled != true)
                        {
                                elems_array[i].checked = true;
                        }
                }
        }

        else
        {
                for (i = 0;  i < elems_array.length;  i++)
                {
                        elems_array[i].checked = false;
                }
        }

}

function validate_delentries(elems_array, bug_id, opt)
{
	var string = '';

	if (elems_array.length == null)
	{
		if (bug_id.checked != true)
		{
			alert('Please choose a file name to delete!');
			return false;
		}

		else
		{
			var response = confirm("Delete the selected file(s)?");

			if (response == true)
			{
				string = bug_id.value;

				document.getElementById('wait').style.display = 'block';

				$.ajax(
				{
					type: 'POST',
					url: 'delete_bugs.py',
					data: 'bugs_string='+string+'&opt='+opt,

					success: function(html)
					{
						$('#response').html(html);
					}
				});
			}

			else
			{
				alert('Action Canceled');
				return false;
			}
		}
	}

	else
	{
		for (i = 0;  i < elems_array.length;  i++)
		{
			if (elems_array[i].checked == true)
			{
				string = string + '@@@' + elems_array[i].value;
			}
		}

		if (string == '')
		{
			alert('Please choose a file name to delete!');
			return false;
		}

		else
		{
			var response = confirm("Delete the selected file(s)?");

			if (response == true)
			{
				document.getElementById('wait').style.display = 'block';

				$.ajax(
				{
					type: 'POST',
					url: 'delete_bugs.py',
					data: 'bugs_string='+string+'&opt='+opt,

					success: function(html)
					{
						$('#response').html(html);
					}
				});
			}

			else
			{
				alert('Action Canceled');
				return false;
			}
		}
	}
}

function start_services(service, checked)
{
	document.getElementById('wait').style.display = 'table';

	$.ajax(
	{
		type: 'POST',
		url: 'start_services_action.py',
		data: 'service=' + service + '&st=' + checked,
	
		success: function(html)
		{
			$('#response').html(html);
		}
	});
}

function make_online(lib_id)
{
	var return_val = confirm("Are you sure you want to make Online?");
	
	if(return_val == true)
	{
		document.getElementById('sync-loading-make-on'+lib_id).style.display = 'block';
		document.getElementById('sync-static-make-on'+lib_id).style.display = 'none';
		document.san_det_list.action = 'iframe_vtl_settings.py#tabs-2';
		document.getElementById('wait').style.display = 'table';
		return true;
	}
	else{
		return false;
	}

}	

function make_offline(lib_id)
{
	var return_val = confirm("Are you sure you want to make it Offline?");

	if(return_val == true)
	{
		document.getElementById('sync-loading-make-off'+lib_id).style.display = 'block';
		document.getElementById('sync-static-make-off'+lib_id).style.display = 'none';
		document.san_det_list.action = 'iframe_vtl_settings.py#tabs-2';
		document.getElementById('wait').style.display = 'table';
		return true;
	}
	else
	{
		return false;
	}
	
}


function validate_set_log_path()
{

	var select_path = document.smb_log_path.audit_path.value;
	
	if(select_path == "select")

	{
	
	jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:40%; padding-top: 4%; font-family: status-bar;">Select the Path</div>', 'SMB Log Alert');
	return false;
	}

	var return_val = confirm ("You are choosing this share to be set as SMB LOG PATH.Do you want to Continue?");

	if(return_val == true)
	{
		document.getElementById('wait').style.display = 'block';
		return true;
	}		
	else
	{
		return false;
	}
}

function form_action(value)
{
	if(value=="add_tape_to_library")
	{
		document.san_det_list.action = 'iframe_vtl_settings.py#tabs-5';
	}
	if(value=="remove_cleaning_tape")
	{
		document.san_det_list.action = 'iframe_vtl_settings.py#tabs-2';
	}
}

function select_submit(value)
{
	if(value=="select_volume")
	{
		document.disk_list_form.action = 'iframe_all_disk_list.py#tabs-1';
		document.disk_list_form.submit();
		return;
		
	}

	if(value=="update_disk")
	{
		document.update_disk_size.action = 'iframe_all_disk_list.py#tabs-1';
		//document.update_disk_size.submit();
		//return;
		
	}

	if(value="volume_confi")
	{
		document.disk_list_form.action = 'iframe_all_disk_list.py#tabs-1';
		document.disk_list_form.submit();
		return;
	}
}

function folder_click(id,no,start)
{
	var no = parseInt(no); 
	for(i=start; i<=no; i++){
		if(i!=id){
			document.getElementById(i).style.display="none";
		}
	}

	var e = document.getElementById(id).style.display;
	if(e=="none"){
		document.getElementById(id).style.display="block";
	}
	else{
		document.getElementById(id).style.display="none";
	}
		

}

function folder_mouseout(id)
{
	var e = document.getElementById(id).style.display;
	if(e=="block"){
		document.getElementById(id).style.display="none";
	}
}

function set_share_path_all()

{
var set_path_val = document.getElementById('set_path_id').value;

        if(set_path_val == '')

                {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:4%; padding-top:4%; font-family: status-bar;">Go to the First tab and First Set the Path</div>', 'Path Alert');
                return false
                }

}
function get_user_suggestions(usrdropdown, grpdropdown, readonly, visible, domainline, available, usergroup, separator, sharename, formname, usrgrpcount, conntype)
{
	var usroptionsselected = parseInt(usrdropdown.length);
	var grpoptionsselected = parseInt(grpdropdown.length);

	var usr_granted_string = '';
	var grp_granted_string = '';
	var domain_check = document.getElementsByName("domainslist")[0].value;

	 /*var set_path_val = document.getElementById('set_path_id').value;

        if(set_path_val == '')

                {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:4%; padding-top: 4%; font-family: status-bar;">Go to the First tab and First Set the Path</div>', 'Path Alert');
                return false
                }*/
        /*if(domain_check == 'sel_domain')
        {

                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:23%; padding-top: 4%; font-family: status-bar;">Please Select a domain</div>', 'Domain Alert');
                return false;

        }
		*/
	if (usroptionsselected > 0)
	{
		for (i = 0;  i < usroptionsselected;  i++)
		{
			if (usrdropdown[i].value != undefined)
			{
				usr_granted_string += usrdropdown[i].value + ':::';
			}
		}
	}

	if (grpoptionsselected > 0)
	{
		for (i = 0;  i < grpoptionsselected;  i++)
		{
			if (grpdropdown[i].value != undefined)
			{
				grp_granted_string += grpdropdown[i].value + ':::';
			}
		}
	}

	if (formname == 'ownership')
	{
		usr_granted_string = ':::' + usrdropdown + ':::';
		grp_granted_string = ':::' + grpdropdown + ':::';
	}

	if (separator == '\\')
	{
		separator = '\\\\';
	}

	if (domainline == '')
	{
		//alert('Choose a domain!');
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 36%; padding-top: 4%; font-family: status-bar;">Choose a domain</div>', 'Domain Alert');
		return false;
	}

	domain     = domainline.substring(0, domainline.indexOf('-'));
	usercount  = domainline.substring(domainline.indexOf('-') + 1, domainline.lastIndexOf('-'));
	groupcount = domainline.substring(domainline.lastIndexOf('-') + 1, domainline.length);

	if (formname != 'acl')
	{
		if (usergroup == 'users')
		{
			if (available == '' && parseInt(usercount) > 1000)
			{
				//alert('Enter the complete user name or the first few characters of user name!');
				jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 30%; padding-top: 4%; font-family: status-bar;">Search the User/Group</div>', 'User Alert ');

				if (formname == 'smb')
				{
					document.share_edit.ads_user_text.focus();
					document.getElementById('available_groups').style.display = 'none';
				}

				else if (formname == 'ftp')
				{
					document.set_ftp_params.ads_user_text.focus();
					document.getElementById('available_groups').style.display = 'none';
				}

				else if (formname == 'ownership')
				{
					document.chang_owner_form.ads_user_text.focus();
					document.getElementById('id_groups_list').style.display = 'none';
				}

				return false;
			}
		}

		if (usergroup == 'groups')
		{
			if (available == '' && groupcount > 1000)
			{
				//alert('Enter the complete group name or the first few characters of group name!');
				jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:30%; padding-top: 4%; font-family: status-bar;">Search the User/Group</div>', 'Group Alert ');

				if (formname == 'smb')
				{
					document.share_edit.ads_user_text.focus();
					document.getElementById('available').style.display = 'none';
				}

				else if (formnanme == 'ftp')
				{
					document.set_ftp_params.ads_group_text.focus();
					document.getElementById('available').style.display = 'none';
				}

				else if (formname == 'ownership')
				{
					document.chang_owner_form.ads_group_text.focus();
					document.getElementById('id_users_list').style.display = 'none';
				}

				return false;
			}
		}
	}

	else
	{
		if (available == '' && parseInt(usrgrpcount) > 1000)
		{
			//alert('Enter the complete user name or the first few characters of user name!');
			jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:30%; padding-top: 4%; font-family: status-bar;">Search the User/Group</div>', 'Group Alert ');
			//document.share_edit.ads_user_text.focus();

			return false;
		}
	}

	usr_granted_string = usr_granted_string.replace(/#/g, '[HASH]');
	usr_granted_string = usr_granted_string.replace(/\&/g, '[AND]');

	grp_granted_string = grp_granted_string.replace(/#/g, '[HASH]');
	grp_granted_string = grp_granted_string.replace(/\&/g, '[AND]');

	available = available.replace(/#/, '[HASH]');
	available = available.replace(/\&/, '[AND]');

	/*if (conntype == 'Join is OK')
	{
		fulluserstring = domain + separator + available;
	}

	else
	{*/
		fulluserstring = available;
	//}

	location.href = 'get_users_string.py?fs=' + fulluserstring + '&ug=' + usergroup + '&s=' + sharename + '&ro=' + readonly + '&v=' + visible + '&ugs=' + usr_granted_string + '&ggs=' + grp_granted_string + '&fn=' + formname + '&dom=' + domain;
}

function get_user_suggestions_acl(usrdropdown, grpdropdown, readonly, visible, domainline, available, usergroup, separator, sharename, formname, usrgrpcount, conntype)
{
	var usroptionsselected = parseInt(usrdropdown.length);
	var grpoptionsselected = parseInt(grpdropdown.length);

	var usr_granted_string = '';
	var grp_granted_string = '';
	var domain_check = document.getElementsByName("domainslist")[0].value;

	 var set_path_val = document.getElementById('set_path_id').value;

        if(set_path_val == '')

                {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:4%; padding-top: 4%; font-family: status-bar;">Go to the First tab and First Set the Path</div>', 'Path Alert');
                return false
                }
        /*if(domain_check == 'sel_domain')
        {

                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:23%; padding-top: 4%; font-family: status-bar;">Please Select a domain</div>', 'Domain Alert');
                return false;

        }
	*/
	if (usroptionsselected > 0)
	{
		for (i = 0;  i < usroptionsselected;  i++)
		{
			if (usrdropdown[i].value != undefined)
			{
				usr_granted_string += usrdropdown[i].value + ':::';
			}
		}
	}

	if (grpoptionsselected > 0)
	{
		for (i = 0;  i < grpoptionsselected;  i++)
		{
			if (grpdropdown[i].value != undefined)
			{
				grp_granted_string += grpdropdown[i].value + ':::';
			}
		}
	}

	if (formname == 'ownership')
	{
		usr_granted_string = ':::' + usrdropdown + ':::';
		grp_granted_string = ':::' + grpdropdown + ':::';
	}

	if (separator == '\\')
	{
		separator = '\\\\';
	}

	if (domainline == '')
	{
		//alert('Choose a domain!');
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 36%; padding-top: 4%; font-family: status-bar;">Choose a domain</div>', 'Domain Alert');
		return false;
	}

	domain     = domainline.substring(0, domainline.indexOf('-'));
	usercount  = domainline.substring(domainline.indexOf('-') + 1, domainline.lastIndexOf('-'));
	groupcount = domainline.substring(domainline.lastIndexOf('-') + 1, domainline.length);

	if (formname != 'acl')
	{
		if (usergroup == 'users')
		{
			if (available == '' && parseInt(usercount) > 1000)
			{
				//alert('Enter the complete user name or the first few characters of user name!');
				jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 30%; padding-top: 4%; font-family: status-bar;">Search the User/Group</div>', 'User Alert ');

				if (formname == 'smb')
				{
					document.share_edit.ads_user_text.focus();
					document.getElementById('available_groups').style.display = 'none';
				}

				else if (formname == 'ftp')
				{
					document.set_ftp_params.ads_user_text.focus();
					document.getElementById('available_groups').style.display = 'none';
				}

				else if (formname == 'ownership')
				{
					document.chang_owner_form.ads_user_text.focus();
					document.getElementById('id_groups_list').style.display = 'none';
				}

				return false;
			}
		}

		if (usergroup == 'groups')
		{
			if (available == '' && groupcount > 1000)
			{
				//alert('Enter the complete group name or the first few characters of group name!');
				jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:30%; padding-top: 4%; font-family: status-bar;">Search the User/Group</div>', 'Group Alert ');

				if (formname == 'smb')
				{
					document.share_edit.ads_user_text.focus();
					document.getElementById('available').style.display = 'none';
				}

				else if (formnanme == 'ftp')
				{
					document.set_ftp_params.ads_group_text.focus();
					document.getElementById('available').style.display = 'none';
				}

				else if (formname == 'ownership')
				{
					document.chang_owner_form.ads_group_text.focus();
					document.getElementById('id_users_list').style.display = 'none';
				}

				return false;
			}
		}
	}

	else
	{
		if (available == '' && parseInt(usrgrpcount) > 1000)
		{
			//alert('Enter the complete user name or the first few characters of user name!');
			jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:30%; padding-top: 4%; font-family: status-bar;">Search the User/Group</div>', 'Group Alert ');
			//document.share_edit.ads_user_text.focus();

			return false;
		}
	}

	usr_granted_string = usr_granted_string.replace(/#/g, '[HASH]');
	usr_granted_string = usr_granted_string.replace(/\&/g, '[AND]');

	grp_granted_string = grp_granted_string.replace(/#/g, '[HASH]');
	grp_granted_string = grp_granted_string.replace(/\&/g, '[AND]');

	available = available.replace(/#/, '[HASH]');
	available = available.replace(/\&/, '[AND]');

	/*if (conntype == 'Join is OK')
	{
		fulluserstring = domain + separator + available;
	}

	else
	{*/
		fulluserstring = available;
	//}

	location.href = 'get_users_string.py?fs=' + fulluserstring + '&ug=' + usergroup + '&s=' + sharename + '&ro=' + readonly + '&v=' + visible + '&ugs=' + usr_granted_string + '&ggs=' + grp_granted_string + '&fn=' + formname + '&dom=' + domain;
}




function get_user_sugg_afp(usrdropdown, grpdropdown, readonly, visible, domain, available, usergroup)
{
        if (domain == 'Select a Domain')
        {
                //alert('Choose a domain!');
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 36%; padding-top: 4%; font-family: status-bar;">Choose a domain</div>', 'Domain Alert ');
                return false;
        }

        if (available == '')
        {
                //alert('Enter the complete user name or the first few characters of user name!');
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 36%; padding-top: 4%; font-family: status-bar;">Search the Username</div>', 'User Alert ');
                //document.share_edit.ads_user_text.focus();

                return false;
        }

        var usroptionsselected = parseInt(usrdropdown.length);
        var grpoptionsselected = parseInt(grpdropdown.length);

        var usr_granted_string = '';
        var grp_granted_string = '';

        if (usroptionsselected > 0)
        {
                for (i = 0;  i < usroptionsselected;  i++)
                {
                        usr_granted_string += usrdropdown[i].value + ':::';
                }
        }

        if (grpoptionsselected > 0)
        {
                for (i = 0;  i < grpoptionsselected;  i++)
                {
                        grp_granted_string += grpdropdown[i].value + ':::';
                }
        }

        var separator = document.afp_form.hid_separator.value;
        var sharename = document.afp_form.hid_share.value;

        if (separator == '\\')
        {
                separator = '\\\\';
        }

        //separator = '+';
	usr_granted_string = usr_granted_string.replace(/#/g, '[HASH]');
        usr_granted_string = usr_granted_string.replace(/\&/g, '[AND]');

        grp_granted_string = grp_granted_string.replace(/#/g, '[HASH]');
        grp_granted_string = grp_granted_string.replace(/\&/g, '[AND]');

        available = available.replace(/#/, '[HASH]');
        available = available.replace(/\&/, '[AND]');

        /*if (conntype == 'Join is OK')
        {
                fulluserstring = domain + separator + available;
        }

        else
        {*/
                fulluserstring = available;
        //}


        //available = available.replace(/#/, '[HASH]');
        //available = available.replace(/\&/, '[AND]');

        //fulluserstring = domain + separator + available;
        location.href = 'get_users_string.py?fs=' + fulluserstring + '&ug=' + usergroup + '&s=' + sharename + '&ro=' + readonly + '&v=' + visible + '&ugs=' + usr_granted_string + '&ggs=' + grp_granted_string + '&fn=afp' + '&dom=' + domain;
}



function submit_domainlist(domain)
{
}

function enable_disable_option(readonly_checked, write_ip)
{
	if (readonly_checked == true)
	{
		write_ip.disabled   = true;
	}

	else
	{
		write_ip.disabled = false;
	}
}

function select_all_quotas()
{
	var check_all_option = document.getElementById('id_select_all');
	var quota_array = document.search_user_quota.elements["delete_option[]"];

	if (quota_array.length == undefined)
	{
		var delete_id = document.getElementById('id_del_quota');

		if (check_all_option.checked == true)
		{
			if (delete_id.disabled != true)
			{
				delete_id.checked = true;
			}
		}

		else
		{
			delete_id.checked = false;
		}
	}

	if (check_all_option.checked == true)
	{
		for (i = 0;  i < quota_array.length;  i++)
		{
			if (quota_array[i].disabled != true)
			{
				quota_array[i].checked = true;
			}
		}
	}

	else
	{
		for (i = 0;  i < quota_array.length;  i++)
		{
			quota_array[i].checked = false;
		}
	}
}

function show_search_usergroups(usergroup)
{
	alert(usergroup);

	if (usergroup == 'users')
	{
		alert(document.getElementById("id_set_owner").style.display);
		document.getElementById("id_set_owner").style.display = "block";
		document.getElementById("id_set_group").style.display = "none";
		alert(document.getElementById("id_set_owner").style.display);
	}

	else if (usergroup == 'groups')
	{
		document.getElementById("id_set_group").style.display = "block";
		document.getElementById("id_set_owner").style.display = "none";
	}
}

function check_services(service, state)
{
	document.getElementById('wait').style.display = 'block';

	if (state != 'True')
	{
		location.href = 'enable_services.py?s=' + service + '&state=' + state; 
	}
}


function close_id_trace_div()
{
	document.getElementById('id_trace').style.display = 'none';
}


function fetch_logs()
{

	//alert("Downloading system logs file....");
	//jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:19%; padding-top: 4%; font-family: status-bar;">Downloading system logs file....</div>', 'Log Alert ');
	$.ajax(
        {
                type: 'POST',
                url: 'system_logs.py',
                data: ' ',

                success: function(html)
                {
                        $('#response').html(html);
                }
        });

}

function validate_change_password()
{
	var old_pass = document.change_password_form.old_password.value;	
	var new_pass = document.change_password_form.new_password.value;	
	var re_new_pass = document.change_password_form.re_new_password.value;	
	var spacesExp = /[\s]/;

	if(old_pass == '')
	{
		//alert("Please enter old Password!");
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:19%; padding-top: 4%; font-family: status-bar;">Please enter old Password</div>', 'Password Alert ');
		//document.change_password_form.old_password.focus();
		return false;
	}

	if(new_pass == '')
	{
		//alert("Please enter new Password!");
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:19%; padding-top: 4%; font-family: status-bar;">Please enter new Password</div>', 'Password Alert ');
		//document.change_password_form.new_password.focus();
		return false;
	}

	if(new_pass.length < 6)
	{
		//alert("Password should be more than 5 characters long!");
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:19%; padding-top: 4%; font-family: status-bar;">Password should be more than 5 characters long</div>', 'Password Alert ');
		//document.change_password_form.new_password.focus();
		return false;
	}

	if(new_pass.match(spacesExp))
        {
        	//alert('Spaces are not allowed in Password!');
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:19%; padding-top: 4%; font-family: status-bar;">Spaces are not allowed in Password</div>', 'Password Alert ');
		//document.change_password_form.new_password.focus();
                return false;
        }

	if(re_new_pass == '')
	{
		//alert("Please re-enter new Password!");
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:19%; padding-top: 4%; font-family: status-bar;">Please re-enter new Password</div>', 'Password Alert ');
		//document.change_password_form.re_new_password.focus();
		return false;
	}

	if(new_pass != re_new_pass)
	{
		//alert("Passwords do not match!");
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:19%; padding-top: 4%; font-family: status-bar;">Passwords do not match</div>', 'Password Alert ');
		//document.change_password_form.re_new_password.focus();
		return false;
	}

}

function validate_create_container()
{
	var container_name = document.create_container.container_name.value;
	var container_size = document.create_container.container_size.value;
	var free_size= document.create_container.free_size2.value;

	if(container_name == '')
	{
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 36%; padding-top: 4%; font-family: status-bar;"> Please enter Container Name!</div>', 'Alert Dialog');
		document.create_container.container_name.focus();
		return false;
	}

	if ((container_name / 1) <= 0 || (container_name / 1) > 0)
        {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 20%; padding-top: 4%; font-family: status-bar;">Container name should be Alpha numeric!</div>', 'Alert Dialog');
                return false;
        }

        if(container_name.length > 8)
        {
                jAlert("<img src='../images/info.gif'><div style='float: right; margin-right: 20%; padding-top: 4%; font-family: status-bar;'>Your Container Name can't be more than 8 Character!</div>", 'Alert Dialog');
                return false;
        }

        if (container_name.indexOf(' ') >= 0)
        {

                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 20%; padding-top: 4%; font-family: status-bar;">Spaces not allowed in Container name!</div>', 'Alert Dialog');
                return false;
        }

	if(container_size == '')
	{
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right: 36%; padding-top: 4%; font-family: status-bar;"> Please enter Container Size!</div>', 'Alert Dialog');
		document.create_container.container_size.focus();
		return false;
	}

	if(container_size < 10)
        {
                jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:20%; padding-top: 4%; font-family: status-bar;"> Please Enter Atleast 10Gb of Size!</div>', 'Alert Dialog');
                document.create_container.container_size.focus();
                return false;
        }

	if(parseInt(container_size) > parseInt(free_size))
        {
           jAlert("<img src='../images/info.gif'><div style='float: right; margin-right: 15%; padding-top: 4%; font-family: status-bar;'> You Can't Enter more than Available Size!.</div>", 'Alert Dialog');
           return false;
        }


}


function validate_folder_quota_form()
{
	var size = document.folder_quota_form.size.value;
	if(size == "")
	{
		//alert("Please enter size! Only integer values are accepted.");
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:19%; padding-top: 4%; font-family: status-bar;">Please enter size! Only integer values are accepted</div>', 'Quota Alert ');
		//document.folder_quota_form.size.focus();
		return false;
	}

	if(size < 10)
	{
		//alert("Size cannot be less than 10 GB. Please enter greater value.");
		jAlert('<img src="../images/info.gif"><div style="float: right; margin-right:19%; padding-top: 4%; font-family: status-bar;">Size cannot be less than 10 GB. Please enter greater value</div>', 'Quota Alert ');
		//document.folder_quota_form.size.focus();
		return false;
	}

}

function adv_option_show()
{
	if(document.getElementById("advance_option").checked == true)
	{
		document.getElementById('adv_option_table').style.display = 'block';		
	}
	if(document.getElementById("advance_option").checked == false)
	{
		document.getElementById('adv_option_table').style.display = 'none';		
	}
}

function copy_textbox_content(from_id,to_id)
{
	var t1 = document.getElementById(from_id);
    	document.getElementById(to_id).value = t1.value;
}

function validate_ldap_form()
{
	var ldapserverip = document.setup_auth.ldapserverip.value;
	var ldapservername = document.setup_auth.ldapservername.value;
	var searchbase = document.setup_auth.searchbase.value;
	var admindn = document.setup_auth.admindn.value;
	var adminpasswd = document.setup_auth.adminpasswd.value;
	var sambaserverip = document.setup_auth.sambaserverip.value;
	var sambaservername = document.setup_auth.sambaservername.value;
	var sambaadminuser = document.setup_auth.sambaadminuser.value;
	var sambaadminpasswd = document.setup_auth.sambaadminpasswd.value;
	var sambadomainname = document.setup_auth.sambadomainname.value;
	var sysdomainname = document.setup_auth.sysdomainname.value;

	if(ldapserverip == '')
	{
		alert("Enter LDAP server Ip address!");
		document.setup_auth.ldapserverip.focus();
		return false;
	}

	if(ldapservername == '')
	{
		alert("Enter LDAP server name!");
		document.setup_auth.ldapservername.focus();
		return false;
	}

	if(searchbase == '')
	{
		alert("Enter Search Base!");
		document.setup_auth.searchbase.focus();
		return false;
	}

	if(admindn== '')
	{
		alert("Enter admin dn!");
		document.setup_auth.admindn.focus();
		return false;
	}

}

function onclick_loader()
{
	document.getElementById('loader-div').style.display = 'block';
	document.getElementById('body-div').style.display = 'none';
}

function onclick_logs_loader(tab)
{
	if(tab == "entire")
	{
		var response = confirm('Getting entire logs may take time! Do you still want to continue?');
		if (response == true)
		{
			document.getElementById('sync-loading').style.display = 'inline';
			document.getElementById('sync-static').style.display = 'none';
		}
		else{
			return false;
		}
	}

	if(tab == "clear")
	{
		var response = confirm('Are you sure you want to clear logs?');
		if (response == true)
		{
			document.getElementById('sync-loading-clear').style.display = 'inline';
			document.getElementById('sync-static-clear').style.display = 'none';
		}
		else{
			return false;
		}
	}
}

function onclick_sync_loader(conn,stat)
{
	if(conn != "local"){
		if(stat == "False"){
			alert(''+conn.toUpperCase()+' configured but connection is not active. Go to SYSTEM >> Authentication page.');
			return false;
		}
		else{
			var response = confirm('Syncronizing users from '+conn.toUpperCase()+' may take time. Do you still want to continue?');
			if (response == true)
			{
				document.getElementById('sync-loading').style.display = 'block';
				document.getElementById('sync-static').style.display = 'none';
				document.getElementById("sync-content").innerHTML = "Please Wait...";
			}
			else{
				return false;
			}
		}
	}
}

function onclick_loader_button(val)
{
	if(val == "san")
	{
		document.getElementById('sync-loading').style.display = 'block';
		document.getElementById('sync-static').style.display = 'none';
		document.getElementById("sync-content").innerHTML = "Restarting SAN...";
	}
	if(val == "nfs")
	{
		document.getElementById('sync-loading-nfs').style.display = 'block';
		document.getElementById('sync-static-nfs').style.display = 'none';
		document.getElementById("sync-content-nfs").innerHTML = "Restarting NFS...";
	}
	if(val == "smb")
	{
		document.getElementById('sync-loading-smb').style.display = 'block';
		document.getElementById('sync-static-smb').style.display = 'none';
		document.getElementById("sync-content-smb").innerHTML = "Restarting SMB...";
	}
	if(val == "afp")
	{
		document.getElementById('sync-loading-afp').style.display = 'block';
		document.getElementById('sync-static-afp').style.display = 'none';
		document.getElementById("sync-content-afp").innerHTML = "Restarting AFP...";
	}
	if(val == "ftp")
	{
		document.getElementById('sync-loading-ftp').style.display = 'block';
		document.getElementById('sync-static-ftp').style.display = 'none';
		document.getElementById("sync-content-ftp").innerHTML = "Restarting FTP...";
	}
	if(val == "raid")
	{
		document.getElementById('sync-loading-raid').style.display = 'block';
		document.getElementById('sync-static-raid').style.display = 'none';
		document.getElementById("sync-content-raid").innerHTML = "Restarting RAID Controller...";
	}

	 if(val == "ip_stat")
        {
                document.getElementById('sync-loading').style.display = 'block';
                document.getElementById('sync-static').style.display = 'none';
                document.getElementById("sync-content").innerHTML = "Enabling...";
        }

        if(val == "ip_st")
        {
                document.getElementById('sync-loading1').style.display = 'block';
                document.getElementById('sync-static1').style.display = 'none';
                document.getElementById("sync-content1").innerHTML = "Disabling...";
        }

	if(val == "nfs_stat")
        {
                document.getElementById('sync-loading2').style.display = 'block';
                document.getElementById('sync-static2').style.display = 'none';
                document.getElementById("sync-content2").innerHTML = "Enabling...";
        }

        if(val == "nfs_st")
        {
                document.getElementById('sync-loading3').style.display = 'block';
                document.getElementById('sync-static3').style.display = 'none';
                document.getElementById("sync-content3").innerHTML = "Disabling...";
        }


}

function auth_reset(val)
{
	if(val == 'nis')
	{
		document.forms["setup_auth"].elements["ip_add"].value = document.forms["setup_auth"].elements["ip_add_hid"].value;
		document.forms["setup_auth"].elements["domain"].value = document.forms["setup_auth"].elements["domain_hid"].value;
	}
	
	if(val == 'ads')
	{
		document.forms["setup_auth"].elements["username"].value = document.forms["setup_auth"].elements["u_hid"].value;
		document.forms["setup_auth"].elements["password"].value = document.forms["setup_auth"].elements["p_hid"].value;
		document.forms["setup_auth"].elements["fqn"].value = document.forms["setup_auth"].elements["f_hid"].value;
		document.forms["setup_auth"].elements["dns"].value = document.forms["setup_auth"].elements["d_hid"].value;
	}
	
	if(val == 'ldap')
	{
		document.forms["setup_auth"].elements["ldapserverip"].value = document.forms["setup_auth"].elements["ldapserverip_hid"].value;
		document.forms["setup_auth"].elements["ldapservername"].value = document.forms["setup_auth"].elements["ldapservername_hid"].value;
		document.forms["setup_auth"].elements["searchbase"].value = document.forms["setup_auth"].elements["searchbase_hid"].value;
		document.forms["setup_auth"].elements["admindn"].value = document.forms["setup_auth"].elements["admindn_hid"].value;
		document.forms["setup_auth"].elements["adminpasswd"].value = document.forms["setup_auth"].elements["adminpasswd_hid"].value;
		document.forms["setup_auth"].elements["sambaserverip"].value = document.forms["setup_auth"].elements["sambaserverip_hid"].value;
		document.forms["setup_auth"].elements["sambaservername"].value = document.forms["setup_auth"].elements["sambaservername_hid"].value;
		document.forms["setup_auth"].elements["sambaadminuser"].value = document.forms["setup_auth"].elements["sambaadminuser_hid"].value;
		document.forms["setup_auth"].elements["sambaadminpasswd"].value = document.forms["setup_auth"].elements["sambaadminpasswd_hid"].value;
		document.forms["setup_auth"].elements["sambadomainname"].value = document.forms["setup_auth"].elements["sambadomainname_hid"].value;
		document.forms["setup_auth"].elements["sysdomainname"].value = document.forms["setup_auth"].elements["sysdomainname_hid"].value;
		document.forms["setup_auth"].elements["portno"].value = document.forms["setup_auth"].elements["portno_hid"].value;
		document.forms["setup_auth"].elements["ssl"].value = document.forms["setup_auth"].elements["ssl_hid"].value;
		document.forms["setup_auth"].elements["ldapusersuffix"].value = document.forms["setup_auth"].elements["ldapusersuffix_hid"].value;
		document.forms["setup_auth"].elements["ldapgroupsuffix"].value = document.forms["setup_auth"].elements["ldapgroupsuffix_hid"].value;
		document.forms["setup_auth"].elements["ldapmachinesuffix"].value = document.forms["setup_auth"].elements["ldapmachinesuffix_hid"].value;
		document.forms["setup_auth"].elements["ldapidmapsuffix"].value = document.forms["setup_auth"].elements["ldapidmapsuffix_hid"].value;
	}
}

function show_hid_fields()
{
	var e = document.getElementById("show_graph_type");
	var strUser = e.options[e.selectedIndex].value;
	if(strUser=="interface")
	{
		document.getElementById('interface_list').style.display = 'block';
	}
}


function clicking_div()
{
	document.getElementById('error_div').style.display = 'none';
}

function show_on_select(selected_value)
{
	if(selected_value == "show_all"){
		document.getElementById('show_on_sel').style.display = 'none';
	}
	if(selected_value == "show_one"){
		document.getElementById('show_on_sel').style.display = 'block';
	}
}
