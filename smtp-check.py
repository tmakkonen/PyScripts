#!/usr/bin/env python
import argparse
import string
import subprocess
import re
import smtplib

def get_mxs(domain):
    rx = re.compile('exchanger.*')
    res = subprocess.check_output('nslookup -type=mx %s' %domain, shell=True) 
    mxs = {}
    for v in [l.group(0).split() for l in rx.finditer(res)]:
        mxs[v[-1].rstrip('.')] = v[-2]

    return mxs

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', action = "store", dest="email")
    results = parser.parse_args()
    email = results.email
    [name, domain] = string.split(email, '@')
   
    print "Looking up MX hosts on domain '%s'" % domain
    hosts = get_mxs(domain)
    for k in hosts.keys():
        print "%s [priority %s]" % (k, hosts[k])

    for h in hosts.keys():
        print "Extensions on '%s':" % h
	srv = smtplib.SMTP(h)
	srv.ehlo()
	for k, v in  srv.esmtp_features.iteritems():
	    print "\t" + k, v
	srv.quit()
