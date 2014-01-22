#!/usr/bin/env python

# This script will help to access sshd service behind firewall
# or router(no public ip)
# It need an server that have public ip.
# more see man ssh or http://wiki.chengh.com/doku.php?id=linux:sshd
#
# Created by: Koonwah Chen (cadmuxe AT gmail.com)
# Jan. 22 2014

from subprocess import Popen
from subprocess import PIPE
import time

def check_ssh(host, port):
    """
    check whether the remote sshd is working
    """
    p = Popen(["nc", "-z", str(host), str(port)], stdout = PIPE)
    p.wait()
    rsl = p.communicate()
    try:
        rsl[0].index("succeeded")
        return True
    except ValueError:
        return False

def ssh_firewall(sshd_port, remote_host, remote_port, username, 
        time_interval, identity_file):
    """
        sshd_port: sshd port of the local machine(behind firewall)
        remote_host: public machine address
        remote_port: public machine port that you want to use
        username: account of public machine
        time_interval: the interval for ssh test
        identity_file: the identity file for ssh
    """
    p = Popen(["ssh", "-R *:%s:localhost:%s" % (str(remote_port), str(sshd_port)), 
        "-N", "-i%s" % identity_file,"%s@%s" % (username, remote_host)], stdout = PIPE)

    while True:
        time.sleep(time_interval)
        if check_ssh(remote_host, remote_port):
            continue
        else:
            p.kill()
            p = Popen(["ssh", "-R *:%s:localhost:%s" % (str(remote_port), str(sshd_port)),
                "-N", "%s@%s" % (username, remote_host)], stdout = PIPE)


if __name__ == "__main__":
    ssh_firewall(22, "your.server.com", 19880, "nologin", 30*60, "")
