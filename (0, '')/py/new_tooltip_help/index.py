#!/usr/bin/python
import cgitb, sys
sys.path.append('/var/www/fs4/py/')
import include_files
print"""
 <script src="new_tooltip_help/lptooltip.js"></script>
        <link rel='stylesheet' type='text/css' href='new_tooltip_help/lptooltip.css' />
<span style = "color:green;cursor:pointer;" class="btn btnPluginDownload lpTooltip lpRight" data-tooltip-text='hello sanjeev'>Test</span>"""
