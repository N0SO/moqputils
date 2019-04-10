#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2

#proxy_support = urllib2.ProxyHandler({'http':'http://www-stl-proxy:80'})
#proxy_support = urllib2.ProxyHandler({})
#opener = urllib2.build_opener(proxy_support)
#urllib2.install_opener(opener)

#proxy = {'http': 'http:/www-stl-proxy:80'}
response = urllib2.urlopen('http://www.1x1callsigns.org/index.php/search')
html = response.read()
print html
#www-stl-proxy
