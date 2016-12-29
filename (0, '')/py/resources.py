#!/usr/bin/python
import cgitb, header
cgitb.enable()

#print 'Content-Type: text/html'
import left_nav
print
print """
      <!--Right side body content starts from here-->
      <div class="rightsidecontainer">
        <div class="insidepage-heading"> RESOURCES >> <span class="content">Resources Information</span></div>
        <!--tab srt-->
        <div class="searchresult-container">
          <div class="infoheader">
            <div id="tabs">
              <ul>
                <li><a href="#tabs-1">System Information</a></li>
                <li><a href="#tabs-2">Sensor Information</a></li>
                <li><a href="#tabs-3">Volume Group Information</a></li>
                <li><a href="#tabs-4">Disk Information</a></li>
              </ul>
              <div id="tabs-1">

	<!--form container starts here-->
        <div class="form-container">
          <div class="topinputwrap-heading"> System Information </div>
          <div class="topinputwrap">
            <div class="formleftside-content">Remote IP</div>
            <div class="formrightside-content"> 192.168.1.43 </div>
          </div>
          <div class="inputwrap">
            <div class="formleftside-content">Server IP</div>
            <div class="formrightside-content"> 192.468.1.51 </div>
          </div>
          <div class="altinputwrap">
            <div class="formleftside-content">Server Name</div>
            <div class="formrightside-content"> nasbox </div>
          </div>
          <div class="inputwrap">
            <div class="formleftside-content">Up Since</div>
            <div class="formrightside-content">52 minutes, 22seconds </div>
          </div>
        </div>
        <!--form container ends here-->
	<p>&nbsp;</p>
              </div>
              <div id="tabs-2">
        <!--form container starts here-->
        <div class="form-container">
          <div class="topinputwrap-heading"> Form  </div>
          <div class="topinputwrap">
            <table cellpadding="0" cellspacing="0" border="0" align="center">
              <tr>
                <td align="left" valign="top"><table width="665" border="0" cellspacing="0" cellpadding="0" >
                    <tr>
                      <td width="660px" class="content" align="left" valign="top"><form id="f1" name="f1" method="post" action="../configurator.php">
                          <div  align="left" style="height:20px; margin-top:0px;" class="menu_text_active"></div>
                          <table width="660" border="0" cellspacing="0" cellpadding="0">
                            <tr>
                              <td colspan="3" height="5px"></td>
                            </tr>
                            <tr>
                              <td width="101" align="left" valign="top" height="20px" class="content">Item Code<font color="#900">*</font></td>
                              <td  align="left" valign="top" width="7">:</td>
                              <td width="194" align="left" valign="middle" height="20px"><input name="firstname" id="firstname" class="textbox" type="Text" /></td>
                            </tr>
                            <tr>
                              <td colspan="3" height="5px"></td>
                            </tr>
                            <tr>
                              <td width="101" align="left" valign="top" height="20px" class="content">Date Format<font color="#900">*</font></td>
                              <td  align="left" valign="top" width="7">:</td>
                              <td width="194" align="left" valign="middle" height="20px"><input name="firstname" id="firstname" class="textbox" type="Date" /></td>
                            </tr>
                            <tr>
                              <td colspan="3" height="5px"></td>
                            </tr>
                            <tr>
                              <td class="content" align="left" valign="top" width="101">Time Format<font color="#900">*</font></td>
                              <td  align="left" valign="top" width="7">:</td>
                              <td align="left" colspan="4"><input name="memory" id="memory" class="textbox" type="Time" onkeypress="return numere(event)" onkeyup="return limitarelungime(this, 4)"/></td>
                            </tr>
                            <tr>
                              <td colspan="3" height="5px"></td>
                            </tr>
                            <tr>
                              <td width="210" align="left" valign="top" height="20px" class="content">textbox1<font color="#900">*</font></td>
                              <td  align="left" valign="top" width="7">:</td>
                              <td width="84" align="left" valign="middle" height="20px"><select name="raid" onchange="display(this,'text','image');" class="textbox">
                                  <option value="" selected="selected">--Select--</option>
                                  <option value="No">Resources Information</option>
                                  <option value="Yes">Date and time settings</option>
                                  <option value="Yes">OPSLAG info</option>
                                </select></td>
                              <td align="left" valign="top" colspan="3"><table width="345" border="0" cellspacing="0" cellpadding="0">
                                  <tbody id="image" >
                                  </tbody>
                                </table></td>
                            </tr>
                            <tr>
                              <td colspan="3" height="5px"></td>
                            </tr>
                            <tr>
                              <td class="content" align="left" valign="top" width="101">textbox2<font color="#900">*</font></td>
                              <td  align="left" valign="top" width="7">:</td>
                              <td align="left" colspan="4"><select name="form_factor" class="textbox" id="form_factor">
                                  <option value="" selected="selected">--Select--</option>
                                  <option value="1U">IP settings</option>
                                  <option value="2U">Authentication</option>
                                </select></td>
                            </tr>
                            <tr>
                              <td colspan="3" height="5px"></td>
                            </tr>
                            <tr>
                              <td class="content" align="left" valign="top" width="101">Multiselect Drop Down<font color="#900">*</font></td>
                              <td  align="left" valign="top" width="7">:</td>
                              <td align="left" colspan="4"><select name="cars" multiple class="mutidropdown" size="2">
                                  <option value="volvo">Resources Information</option>
                                  <option value="saab">Date and time settings</option>
                                  <option value="opel">OPSLAG info</option>
                                  <option value="audi">IP settings</option>
                                  <option value="audi">Authentication</option>
                                </select></td>
                            </tr>
                            <tr>
                              <td colspan="3" height="5px"></td>
                            </tr>
                            <tr>
                              <td class="content" align="left" valign="top" width="101">Date<font color="#900">*</font></td>
                              <td  align="left" valign="top" width="7">:</td>
                              <td align="left" colspan="4"><input type="radio" name="sex" value="male">
                                Date
                                <input type="radio" name="sex" value="female">
                                Time </td>
                            </tr>
                            <tr>
                              <td colspan="3" height="5px"></td>
                            </tr>
                            <tr>
                              <td class="content" align="left" valign="top" width="101">Check Box<font color="#900">*</font></td>
                              <td  align="left" valign="top" width="7">:</td>
                              <td align="left" colspan="4"><input type="checkbox" name="vehicle" value="Bike">
                                Date
                                <input type="checkbox" name="vehicle" value="Car">
                                Time </td>
                            </tr>
                            <tr>
                              <td colspan="3" height="5px"></td>
                            </tr>
                            <tr>
                              <td class="content" align="left" valign="top" width="101">Text Area<font color="#900">*</font></td>
                              <td  align="left" valign="top" width="7">:</td>
                              <td align="left" colspan="4"><textarea name="notes" id="notes" cols="25" rows="5" class="textarea"></textarea></td>
                            </tr>
                            <tr>
                              <td colspan="3" height="10px"></td>
                            </tr>
                            <tr>
                              <td align="left" valign="top" colspan="3" height="20px" class="content"><font color="#900">*</font> Fields are mandatory to fill up.</td>
                            </tr>
                            <tr>
                              <td>&nbsp;</td>
                              <td>&nbsp;</td>
                              <td><input name="submit" value="Submit" onclick="javascript:return verify();" type="submit" />
                                &nbsp;&nbsp;&nbsp;
                                <input name="Reset" value="Reset" type="Reset" /></td>
                            </tr>
                            <tr>
                              <td height="10px"></td>
                            </tr>
                          </table>
                        </form></td>
                    </tr>
                  </table></td>
              </tr>
            </table>
            <br />
          </div>
        </div>
        <!--form container ends here-->
	<p>&nbsp;</p>
              </div>
              <div id="tabs-3">
                <p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.<br />
<br />
 It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.</p>
              </div>
              <div id="tabs-4">
                <p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. <br />
<br />
It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.</p>
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
