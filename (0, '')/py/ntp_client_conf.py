#!/usr/bin/python
import commands
import sys
def conf(server):
    """ this function is configuring the ntp.conf  file with server  option"""
    se_name=str(server)
    #cmd="sudo sed -i \"/server/d\" /etc/ntp.conf"
    #st=commands.getstatusoutput(cmd)
    st=unconf(se_name)
    if str(st) == "FAIL":
        status="FAIL"
        return status 
    cmd="sudo sed -i \"$ a\\server "+str(se_name)+"\" /etc/ntp.conf "
    st=commands.getstatusoutput(cmd)
    if st[0] != 0:
        status="FAIL"
        return status 
    status="SUCCESS"
    return status
def unconf(server):
    """  this  function is for removing the  server  information from ntp.conf"""
    #se_name=str(server)
    cmd="sudo sed -i \"/server/d\" /etc/ntp.conf"
    st=commands.getstatusoutput(cmd)
    if st[0] != 0:
        status="FAIL"
        return status
    status="SUCCESS"
    return status
def server():
    """ this  function is for getting the server name for ntp"""
    cmd="cat /etc/ntp.conf|grep server|awk -F \" \" '{print $2}'"
    st=commands.getstatusoutput(cmd)
    if st[1] == '':
        status=''
        return status
    status=str(st[1])
    return status
def stop_ntp():
    """ this function is for stoping the ntp date server"""
    cmd="sudo  chkconfig ntpdate off" 
    st=commands.getstatusoutput(cmd)
    if st[0] != 0:
        status="FAIL"
        return  status
    cmd="sudo /etc/init.d/ntpdate stop"
    st=commands.getstatusoutput(cmd)
    if st[0] != 0:
        status="FAIL"
        return status
    status="SUCCESS"
    return status
def start_ntp():
    """ this function is for starting the ntp date server"""
    cmd="sudo  chkconfig ntpdate on" 
    st=commands.getstatusoutput(cmd)
    if st[0] != 0:
        status="FAIL"
        return  status
    cmd="sudo /etc/init.d/ntpdate start"
    st=commands.getstatusoutput(cmd)
    if st[0] != 0:
        status="FAIL"
        return status
    status="SUCCESS"
    return status
def enable_ntp(server):
    """ this will  start eable the ntp server"""
    server=str(server)
    st=conf(server)
    if st == "FAIL":
        return "FAIL"
    st=stop_ntp()
    if st == "FAIL":
        return "FAIL"
    st=start_ntp()
    if st == "FAIL":
        return "FAIL"
    return "SUCCESS"
def disable_ntp(server):
    """ this will disable the ntp date server """
    server=str(server)
    st=unconf(server)
    if st == "FAIL":
        return "FAIL"
    st=stop_ntp()
    if st == "FAIL":
        return "FAIL"
    return "SUCCESS"
if __name__ =="__main__":
    WARNING='\033[93m'
    RED='\033[94m'
    ENDC='\033[0m'
    print WARNING+"USAGE: "+ENDC
    print WARNING+"    ntp_client_conf.enable_ntp('server')"+ENDC+ RED +"# this will enable the ntp date  return 'FAIL' on failure 'SUCCESS' on success"+ENDC
    print WARNING+"    ntp_client_conf.disable_ntp('server')"+ENDC+ RED +"# this will disable the ntp date return 'FAIL' on failure 'SUCCESS' on success "+ENDC
    print WARNING+"    ntp_client_conf.server()"+ENDC+ RED +"# this will return server name if configured other wise return ''  "+ENDC
    print WARNING+"    ntp_client_conf.start_ntp() ,ntp_client_conf.stop_ntp() "+ENDC+ RED +"# these function for starting and stoping the ntpdate adn will return  'FAIL'  on failure 'SUCCESS' on success ''  "+ENDC
    #st=enable_ntp(str(sys.argv[1]))
    #print st
    #stop_ntp()
    #start_ntp()
    #st=disable_ntp(str(sys.argv[1]))
    #print st
    #st=server()
    #print st
    
    
