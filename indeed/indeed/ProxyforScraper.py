#! /usr/bin/env python
# -*- coding: utf-8 -*-

import re,requests,random


header={'headers':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

class GatherProxy(object):
    '''To get proxy from http://gatherproxy.com/'''
    url='http://gatherproxy.com/proxylist/anonymity/?t=Elite'
    pre1=re.compile(r'<tr.*?>(?:.|\n)*?</tr>')
    pre2=re.compile(r"(?<=\(\').+?(?=\'\))")
    def getelite(self,pages=1,uptime=70,fast=True):
        '''Get Elite Anomy proxy
        Pages define how many pages to get
        Uptime define the uptime(L/D)
        fast define only use fast proxy with short reponse time'''

        proxies=set()
        for i in range(1,pages+1):
            #params={"Type":"elite","PageIdx":str(i),"Uptime":str(uptime)}
            r=requests.get(self.url,headers=header)
            for td in self.pre1.findall(r.text):
                print(td)
                if 'fast' and 'center fast' not in td:
                    continue 
                try:
                    tmp= self.pre2.findall(str(td))
                    if(len(tmp)==2):
                        proxies.add(tmp[0]+":"+str(int('0x'+tmp[1],16)))
                except:
                    pass
        return proxies

class ProxyPool(object):
    '''A proxypool class to obtain proxy'''
    gatherproxy=GatherProxy()

    def __init__(self):
        self.pool=set()

    def updateGatherProxy(self,pages=1,uptime=70,fast=True):
        '''Use GatherProxy to update proxy pool'''
        self.pool.update(self.gatherproxy.getelite(pages=pages,uptime=uptime,fast=fast))

    def removeproxy(self,proxy):
        '''Remove a proxy from pool'''
        if proxy in self.pool:
            self.pool.remove(proxy)

    def randomchoose(self):
        '''Random Get a proxy from pool'''
        if self.pool:
            return random.sample(self.pool,1)[0]
        else:
            self.updateGatherProxy()
            return random.sample(self.pool,1)[0]

    def checkProxy(self):
        '''Get a dict format proxy randomly'''
        for proxy in self.pool:
            proxies={'http':'http://'+proxy,'https':'https://'+proxy}
            try:
                r=requests.get('http://www.indeed.com/m',proxies=proxies,timeout=1, headers=header)
                if (r.status_code == 200):
                    pass
                else:
                    self.removeproxy(proxy)
            except:
                self.removeproxy(proxy)

    def updateSQL(self):
        # update all proxies to SQL
        pass


if __name__ =='__main__':
    proxies=GatherProxy()
    print(proxies.getelite())
    