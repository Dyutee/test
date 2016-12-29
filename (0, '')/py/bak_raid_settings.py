#!/usr/bin/python
import cgitb, header, os, sys
cgitb.enable()

import left_nav
print
print """

      <!--Right side body content starts from here-->
      <div class="rightsidecontainer">
        <div class="insidepage-heading">Raid Configuration >> <span class="content">Raid/Volume Set Options</span></div>
        <!--tab srt-->
        <div class="searchresult-container">
          <div class="infoheader">
            <div id="tabs">
              <ul>
                <li><a href="#tabs-1">Configure Raid Set</a></li>
                <li><a href="#tabs-2">Add Volume</a></li>
                <li><a href="#tabs-3">Remove Volume</a></li>
		<li><a href="#tabs-4">Volume Info</a></li>
              </ul>
	      <div id="tabs-2">
        <!--form container starts here-->
        <div class="form-container">
          <div class="topinputwrap-heading">Add Volume Group</div>
          <div class="inputwrap">
	 <div class="formleftside-content">
	
	Create Volume

	</div>
          </div>
        </div>
        <!--form container ends here-->
	<p>&nbsp;</p>
              </div>

              <div id="tabs-1">


		 <div id="subtabs">

                  <ul>
		    <li><a href="#subtabs-1">Configure Raid Set</a></li>
                    <li><a href="#subtabs-2">Configure Volume Set</a></li>

                    <li><a href="#subtabs-3">Configure Physical Drives</a></li>

                    <li><a href="#subtabs-4">Information</a></li>

                  </ul>
		 <div id="subtabs-1">
		 <div id="subsubtabs">

                  <ul>

                    <li><a href="#subsubtabs-1">Create Raid</a></li>

                    <li><a href="#subsubtabs-2">Delete Raid</a></li>

                    <li><a href="#subsubtabs-3">Expand Raid</a></li>
		    <li><a href="#subsubtabs-4">Offline Raid</a></li>
		   <li><a href="#subsubtabs-5">Activate Raid</a></li>
		  <li><a href="#subsubtabs-6">Create hotspare</a></li>
		  <li><a href="#subsubtabs-7">Delete hotspare</a></li>


                  </ul>

                  <div id="subsubtabs-1">

		Create Raid

                  </div>
		<div id="subsubtabs-2">

                Delete Raid

                  </div>
		<div id="subsubtabs-3">

                Expand Raid

                  </div>

		<div id="subsubtabs-4">

                Offline Raid

                  </div>

 	<div id="subsubtabs-5">

                Activate Raid

                  </div>

	<div id="subsubtabs-6">

                Create hotspare

                  </div>

	<div id="subsubtabs-7">

                Delete hotspare

                  </div>
	</div>

	</div>
		 <div id="subtabs-2">
<div>

		Configure Volume		

                  </div>

                  </div>


  <div id="subtabs-3">
                        <div>

                Physical Drives 

                        </div>
                  </div>

  <div id="subtabs-4">
                        <div>

                Information

                        </div>
                  </div>

	

</div>

	<!--form container starts here-->
        <!--form container ends here-->
	<p>&nbsp;</p>
	</div>
	<div id="tabs-3">
        <!--form container starts here-->
        <div class="form-container">
          <div class="topinputwrap-heading">Remove Volume Group</div>
          <div class="inputwrap">
         <div class="formleftside-content">
        
        Remove Volume

        </div>
          </div>
        </div>
        <!--form container ends here-->
        <p>&nbsp;</p>
              </div>
	
<div id="tabs-4">
        <!--form container starts here-->
        <div class="form-container">
          <div class="topinputwrap-heading">Volume Group Information</div>
          <div class="inputwrap">
         <div class="formleftside-content">
        
         Volume Information

        </div>
          </div>
        </div>
        <!--form container ends here-->
        <p>&nbsp;</p>
              </div>

	
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

<!-- ####### Sub Tabs Start ####### -->

<script>
$("#tabs, #subtabs").tabs();
$("#tabs, #subsubtabs").tabs();
</script>

<!-- ####### Sub Tabs End ####### -->

"""
