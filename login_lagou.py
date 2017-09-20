#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import time
import json
import sys
import subprocess
import requests
import hashlib
import re

#请求对象
session = requests.session()

#请求头信息
HEADERS = {
    'Referer': 'https://passport.lagou.com/login/login.html',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:51.0) Gecko/20100101 Firefox/51.0',
}

def encrypt_password(passwd):
    '''对密码进行了md5双重加密 veennike 这个值是在js文件找到的一个写死的值 '''
    passwd = hashlib.md5(passwd.encode('utf-8')).hexdigest()
    passwd = 'veenike'+passwd+'veenike'
    passwd = hashlib.md5(passwd.encode('utf-8')).hexdigest()
    return passwd

def get_token():
    login_page = 'https://passport.lagou.com/login/login.html'
    data = session.get(login_page, headers=HEADERS)
    X_Anti_Forge_Token=re.search('(\w+\-\w+\-\w+\-\w+\-\w+)', data.content)
    X_Anti_Forge_Code=re.search('X_Anti_Forge_Code.*?\'(\d+)\'', data.content)
    return (X_Anti_Forge_Token.group(1), X_Anti_Forge_Code.group(1))

def login(username, passwd):
    X_Anti_Forge_Token,X_Anti_Forge_Code=get_token()
    login_headers = HEADERS.copy()
    login_headers.update({'X-Requested-With':'XMLHttpRequest','X-Anit-Forge-Token':X_Anti_Forge_Token,'X-Anit-Forge-Code':X_Anti_Forge_Code})
    postData = {
            'isValidate' : 'true',
            'username' : username,
            'password': encrypt_password(passwd),
            'request_form_verifyCode': '',
            'submit': '',
        }
    response=session.post('https://passport.lagou.com/login/login.json', data=postData, headers=login_headers)
    print response.content

    del login_headers['Referer']
    del login_headers['X-Requested-With']
    del login_headers['X-Anit-Forge-Token']
    del login_headers['X-Anit-Forge-Code']

    req = session.get('https://easy.lagou.com/dashboard/index.htm?from=gray', headers=login_headers)
    print req.content

if __name__ == "__main__":
    username=''
    passwd=''
    login(username, passwd)
