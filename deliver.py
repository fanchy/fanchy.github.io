#-*- coding:utf-8 -*-

import urllib2
import os

URL_PREFIX = 'http://192.168.84.1/h2web/'
def downloadFile(fileName, savePrefix = ''):
    print('downloaded %s'%(fileName))
    request = urllib2.Request(URL_PREFIX + fileName)
    response = urllib2.urlopen(URL_PREFIX + fileName)
    ret = response.read()
    ret = ret.replace('\r\n', '\n')
    f = open(savePrefix+fileName, 'w')
    f.write(ret)
    f.close()
    #print(ret)
    print('downloadFile......'+fileName)
    return True
    
    

# downloadFile('index.html')
files = os.listdir('./markdown/')
for k in files:
    if k[-3:] != '.md':
        continue
    downloadFile(k[:-3]+'.html')
files = os.listdir('./markdown/docs')
for k in files:
    if k[:-3] != '.md':
        continue
    downloadFile(k[:-3]+'.html')



