#!/usr/bin/python
import cgitb, sys, header, common_methods, string
cgitb.enable()


#print 'Content-Type: text/html'
import left_nav

get_share = header.form.getvalue("share_name")


                                               


print
print """

      <!--Right side body content starts from here-->
      <div class="rightsidecontainer">
	<div class="insidepage-heading">Nas >> <span class="content">Configure Information</span></div>
	<!--tab srt-->
	<div class="searchresult-container">
	  <div class="infoheader">
	    <div id="tabs">
	      <ul>
		<li><a href="#tabs-1">AFP Settings</a></li>
	      </ul>
	      <div id="tabs-1">

	<!--form container starts here-->
	<div class="form-container">
	<!--<div class="topinputwrap-heading">AFP Settings for '"""+get_share+"""'</div>-->
	<div><font color ="#EC1F27">You are Configuring AFP Settings for</font><b>'<font color="green">ShareName</font>'</b></div>

	 <div class="view_option" style = 'border: 0px solid;'><a href = 'main.py?page=cs'><img title = 'Back to shares' src = '../images/go-back-icon.png' /></a></div>

	  <div class="inputwrap">


                <form name = 'afp_form' method = 'POST' action='' onsubmit = 'return validate_share_afp();' >
                        <table width = "685" border = "0" cellspacing = "0" cellpadding = "0" name = 'disp_tables' id = 'id_afp_settings' style = 'display:block  ;'>
                        <tr>
                                <td>
                        <table width = '100%'>
                                <tr>
                                        <td colspan = '3'Style="color:#999999;">
                                                <input type = 'checkbox' name = 'use_afp' onclick = 'return show_afp_params();'>&nbsp;<b>Enable AFP</b>
                                        </td>
                                </tr>
                        </table>
                                <BR><div width = '100%' id = 'afp_params' style = 'display: none;'>
                                <table width = '100%' style='padding:0 0 0 30px;'>
                                        <tr>
                                                <td style="color:#999999;">
                                                        <input type = 'checkbox' name = 'read_only' > Read only<BR>
                                                </td>
                                        </tr>
                                        <tr>
                                                <td>
                                                        <BR><span  style="color:darkred;"><b>User access permissions</b></span>:<br/><br/>
                                                        <input type = 'radio' name = 'afp_priv' value = 'guest'  guest_checked  onclick = 'return show_afp_users_groups();'> <span  style="color:#999999;">Guest</span><BR>
                                                        <input type = 'radio' name = 'afp_priv' value = 'valid_user' onclick = 'return show_afp_users_groups();'><span  style="color:#999999;">Authenticated User</span><br/>
                                                </td>
                                        </tr>

                                        <tr>
                                        <td></td>
                                        </tr>

                                        <tr>
                                                <td>


                                                        <div  width = '100%' id = 'afp_users_list' style = 'display: none;' >

<!-- users can authenticate to afp only when authentication method is set to local authentication-->
         <table width = '100%' style = 'color: darkred;'>
                <tr>
                        <td >
                                Authentication is set to NIS!
                        </td>
                </tr>
                </table>

        <table width = '100%'>
                <tr>
                        <td colspan = '2'>
                                <BR><span style="color:#ED2C33;">Users list</span>:
                        </td>
                </tr>
                <tr>
                        <td style="color:#999999;">
                                Available:
                        </td>
                        <td style="color:#999999;">
                                Authorized:
                        </td>
                </tr>
                <tr>
                        <td>
                                        <select class = 'input' style = 'width: 200px; height: 150px;' id = 'afp_available' name = 'avail_users' multiple onclick = "return afp_move_users(this.form.afp_available, this.form.afp_granted, '1');\" >


                        <option value = '' title = ''></option>

        </select>
                        </td>
                        <td>
                                <select class = 'input' style = 'width: 200px; height: 150px;' id = 'afp_granted' name = 'afp_grant_users[]' multiple onclick = "return afp_move_users(this.form.afp_granted, this.form.afp_available, '2');\" >

                        <option value = '' selected title = ''></option>
        #print afp_users_dropdown 

               </select>
                        </td>
                </tr>
                <tr>
                        <td></td>
                </tr>
                <tr>
                <td colspan = '2' style="color:#ED2C33;">
                        <BR>Groups list:
                </td>
        </tr>
        <tr>
                <td style="color:#999999;">
                        Available:
                </td>
                <td style="color:#999999;">
                        Authorized:
                </td>
        </tr>
        <tr>
                <td>
                        <select class = 'input' style = 'width: 200px; height: 150px;' id = 'afp_available_groups' name = 'avail_groups' multiple onclick = "return afp_move_groups(this.form.afp_available_groups, this.form.afp_granted_groups, '1');\" >


                <option value = '' title = ''></option>

                              </select>
                </td>
                <td>
                        <select class = 'input' style = 'width: 200px; height: 150px;' id = 'afp_granted_groups' name = 'afp_grant_groups[]' multiple onclick = "return afp_move_groups(this.form.afp_granted_groups, this.form.afp_available_groups, '2');\">

                        <option value = '' selected title = ''></option>
        #print afp_groups_dropdown; 

        </select>
                </td>
        </tr>
                        </table>
                        
                        
                        </div>
                        </td>
                </tr>
                                        <tr>
                                                <td><br/>
                                                        <input type = 'checkbox'  name = 'advanced_per' onclick = 'return show_advance_per(this.checked);' >&nbsp;<span style="color:darkred;">Advance Permission</span><BR>
                                                </td>
                                        </tr>
<tr>
<td>

                                                        <div  width = '100%' id = 'afp_advanced_list' style = 'display:none; margin:20px 0 0 0;' >
<table width = '43%' style="margin:0 0 0 40px;">
<tr>
        <td style="color:#999999;">Host Allow:</td>
        <td><input type='text' name='host_allow' size ="10"id='host_allow' value=''/></td>
</tr>

<tr>
        <td style="color:#999999;">Host Deny:</td>
        <td><input type='text' name='host_deny' size = "10" id='host_deny' value='' /></td>
</tr>

<tr>
        <td style="color:#999999;">Umask:</td>
        <td><input type='text' name='umask' size= "10" id='umask' value=''/></td>
        <input type='hidden' name='file_perm' value='' />
        <input type='hidden' name='dir_perm' value='' />
</tr>


</table>
</div>

</td>
</tr>
                </table>
	<div style="width:700px;">
	<button class="button_example" type="submit" name = 'local_action_but'  id = 'local_action_but' value = 'Apply'  onclick = 'validate_local_auth();' style="float:right; margin:0 100px 10px 0;">Apply</button>
	</div>
        </div>
        <table width = '100%'>
                <tr>
                        <td>
               </td>
                        <td align = 'right'>
                                <BR><!--<input class = 'input1' type = 'submit' name = 'action_but' value = 'Apply' >-->
                                

                                <input type = 'hidden' name = 'proceed_page' value = 'proceed'>
                                <input type = 'hidden' name = 'hid_share' value = ''>
                                <input type = 'hidden' name = 'hid_share_path' value = ''>
                                <input type = 'hidden' name = 'hid_connection_status' value = ''>
                        </td>
                </tr>
                <input type = 'hidden' name = 'hid_session_user' value = ' session_user '>
        </table>
        </td>
        </tr>
        </table>
                                                                                                         




         </div>
        </form>
</div>
<!--form container ends here-->
<p>&nbsp;</p>
      </div>

  </div>
</div>
</div>
<!--form container ends here-->
<!--form container starts here-->
<!--form container ends here-->
</div>
<!--Right side body content ends here-->
</div>
<!--Footer starts from here-->
<div class="insidefooter footer_content">&copy; 2013 Opslag FS2</div>
<!-- Footer ends here-->
</div>
<!--inside body wrapper end-->
</div>
<!--body wrapper end-->
</body>
</html>
"""
