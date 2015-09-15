# -*- coding: UTF-8 -*-
import re
from string import strip
import urllib

__author__ = 'barryqiu'

import urllib2


def get_score(mobile_num):
    url = "http://life.httpcn.com/mobile.asp#main"
    values = {'isbz': '0',
              'word': mobile_num,
              'data_type': '0',
              'act': 'submit',
              'sex': '1'
              }

    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'User-Agent': user_agent}

    proxy = urllib2.ProxyHandler({'http': 'proxy.tencent.com:8080'})
    opener = urllib2.build_opener(proxy)
    urllib2.install_opener(opener)

    data = urllib.urlencode(values)
    req = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(req)
    the_page = response.read()
    the_page = the_page.decode('gbk').encode('utf-8')

    # get score
    try:
        first_index = the_page.index('<b>数理评分：</b><font class="red">') + len('<b>数理评分：</b><font class="red">')
    except Exception, e:
        first_index = -1

    try:
        if first_index < 0:
            first_index = the_page.index('<b>数理评分：</b><font class="blue">') + len('<b>数理评分：</b><font class="blue">')
    except Exception, e:
        first_index = -1

    try:
        if first_index < 0:
            first_index = the_page.index('<b>数理评分：</b><font class="green">') + len('<b>数理评分：</b><font class="green">')
    except Exception, e:
        first_index = -1

    sub_page = the_page[first_index:-1]
    score = sub_page[0:sub_page.index('分')]

    # get 吉
    pattern = re.compile('(\d+签\s\S+签)')
    match = pattern.search(sub_page)
    index = pattern.search(sub_page).span()[1]
    ji1 = match.group()

    # get 吉2
    match = pattern.search(sub_page[index:-1])
    ji2 = match.group()

    return score + " " +ji1 + " " + ji2


file = open("mobile.txt")
file2 = open("result.txt", 'w')
num = 1
while 1:
    line = file.readline()
    if not line:
        break
    score = get_score(strip(line))
    s = "%d %s %s" % (num, score, line)
    print(s)
    num += 1
    file2.write(score + " " + line)
file2.flush()
