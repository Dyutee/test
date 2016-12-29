#!/usr/bin/python

import cookielib
import urllib2

cookies = cookielib.LWPCookieJar()
handlers = [
    urllib2.HTTPHandler(),
    urllib2.HTTPSHandler(),
    urllib2.HTTPCookieProcessor(cookies)
    ]
opener = urllib2.build_opener(*handlers)

def fetch(uri):
    req = urllib2.Request(uri)
    return opener.open(req)

def dump():
    for cookie in cookies:
        print cookie.name, cookie.value

uri = 'http://www.google.com/'
res = fetch(uri)
dump()

res = fetch(uri)
dump()

# save cookies to disk. you can load them with cookies.load() as well.
cookies.save('mycookies.txt')
