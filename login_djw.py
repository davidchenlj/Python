#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import time
import json
import sys
import requests
import re

#请求对象
session = requests.session()

#请求头信息
HEADERS = {
    'Referer': 'https://passport.lagou.com/login/login.html',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:51.0) Gecko/20100101 Firefox/51.0',
}

def login(username, passwd):
    login_headers = HEADERS.copy()
    login_headers.update({
        'Referer':'https://www.dajie.com/',
        'x-requested-with':'XMLHttpRequest',
        'Host':'www.dajie.com'
    })
    postData = {
            'captcha' : '',
            'email' : username,
            'password': passwd,
            'rememberMe': '1'
        }
    response=session.post('https://www.dajie.com/account/newloginsubmitm?callback=NEW_VERSION_LOGIN_CALLBACK&_CSRFToken=&ajax=1', data=postData, headers=login_headers)
    print(response.content)

    login_headers = HEADERS.copy()
    login_headers.update({
        'Host':'job.dajie.com',
        'Referer':'https://www.dajie.com/'
    })
    response=session.get('https://job.dajie.com/auth/checking',  headers=login_headers)
    print(response.text)


if __name__ == "__main__":
    username=''
    passwd=''
    login(username, passwd)
