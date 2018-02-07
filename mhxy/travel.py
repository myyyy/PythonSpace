#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
import urllib2
import sqlite3

from supickle import pickledb

def get_travel_list():
    # rs = requests.get('http://xyq.163.com/2011/zhuanyi/js/travel_list.js')
    # import pdb;pdb.set_trace()

        # zone_name = self.get_argument('zone_name')
    request = urllib2.Request("http://xyq.163.com/2011/zhuanyi/js/travel_list.js")
    response = urllib2.urlopen(request)

    data = response.read()
    data = json.loads(data[12:])
    db = pickledb('json.db', True)
    db.set('travel',data)
def bool_db():
    db = pickledb('json.db', True)
    send = db.lgetall('send')
    travel = db.get('travel')
    for s in send:
        if s[1] in  travel.get(s[0]):
            print s[0],s[1],s[2], ','.join(travel.get(s[0]))
if __name__ == '__main__':
    get_travel_list()
    bool_db()