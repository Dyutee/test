if(querystring == 'page=nd' or querystring == 'page=disk_list' or querystring == 'page=rs' or querystring =='page=crs' or querystring =='page=cvs'):

                print"""
                        <li><a href="main.py?page=nd" style ="color:#333333;">RAID</a>"""
        else:
                print"""<li>RAID"""
        print"""
                          <ul>"""
        if(querystring == 'page=nd' or querystring == 'page=disk_list'):
                print"""<li><a href="main.py?page=nd" style ="color:#333333;">Volume Configuration</a>"""
        else:
                print"""<li>Volume Configuration"""
        print"""
                              <ul>"""
        if(querystring == 'page=nd'):
                print"""<li><a href="main.py?page=nd" style ="color:#EC1F27;font-weight:bold;">Disk Configuration</a></li>"""
        else:
                print"""
                        <li><a href="main.py?page=nd">Disk Configuration</a></li>"""
        if(querystring == 'page=disk_list'):

                print"""<li><a href="main.py?page=disk_list" style ="color:#EC1F27;font-weight:bold;">Disk List</a></li>"""
        else:

                print"""<li><a href="main.py?page=disk_list">Disk List</a></li>"""
        print"""
                              </ul>
                            </li>"""

