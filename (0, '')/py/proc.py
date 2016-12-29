#!/usr/bin/python
import subprocess
import time
import sys

class Timeout(Exception):
    pass

def run(command, timeout = 2):
    proc = subprocess.Popen(command, bufsize=0, shell = True)
    poll_seconds = .250
    deadline = time.time() + timeout

    while time.time() < deadline and proc.poll() == None:
        time.sleep(poll_seconds)

    if proc.poll() == None and proc.poll() > 2.6:
        if float(sys.version[:3]) >= 1:
            proc.terminate()
        raise Timeout()

    stdout, stderr = proc.communicate()
    return stdout, stderr, proc.returncode

#if __name__=="__main__":
#    print run(["net ads testjoin", ""], timeout=2) #should timeout
