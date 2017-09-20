# -*- coding: utf-8 -*-
import time, sys, re
import requests
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from PIL import Image

username=''
passwd=''

driver=webdriver.PhantomJS(executable_path='C:\\Python27\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')
driver.get('https://passport.58.com/login')
time.sleep(2)

pwdLogin=driver.find_element_by_id('pwdLogin')
pwdLogin.click()

# 输入用户名
usernameUser=driver.find_element_by_id('usernameUser')
usernameUser.send_keys(username)

time.sleep(1)
passwordUserText=driver.find_element_by_id('passwordUserText')
passwordUserText.click()

# 输入密码
passwordUser=driver.find_element_by_id('passwordUser')
passwordUser.send_keys(passwd)

# 点击登陆
btnSubmitUser=driver.find_element_by_id('btnSubmitUser')
btnSubmitUser.click()
time.sleep(3)

''' 获取驱动Cookie '''
dict1_cookie={}
cookie_tmp=[]
for cookie in driver.get_cookies():
    data="{}={}".format(cookie['name'], cookie['value'])
    dict1_cookie[cookie['name']]=cookie['value']
    cookie_tmp.append(data)
_cookie=';'.join(cookie_tmp)


HEADERS={
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding":"gzip, deflate, br",
    "Connection":"keep-alive",
    "Host":"my.58.com",
    "Cookie":_cookie
}

''' 通过COOKIE抓取数据'''
session = requests.session()
response=session.get('https://my.58.com/index', headers=HEADERS)
print(response.text)



第2中方法,调用自带的js进行模拟登陆

# -*- coding: utf-8 -*-
import time, sys, re, json
import requests
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

username=''
passwd=''

''' 设置浏览器的User-Agent '''
desired_capabilities= DesiredCapabilities.PHANTOMJS.copy()
desired_capabilities['phantomjs.page.customHeaders.User-Agent'] = (
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
)
driver=webdriver.PhantomJS(executable_path='C:\\Python27\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe', desired_capabilities=desired_capabilities)

driver.get('https://passport.58.com/login')
time.sleep(1)

''' 执行58js获取加密串 '''
rsaModulus=driver.find_element_by_id('rsaModulus').get_attribute('value')
rsaExponent=driver.find_element_by_id('rsaExponent').get_attribute('value')

''' 获取加密串密码 '''
timespan=str(int(round(time.time() * 1000)))
p1_user="return encryptString('{}{}', '{}', '{}')"
encrypt_passwd=driver.execute_script(p1_user.format(timespan, passwd, rsaExponent, rsaModulus))

Fingerprint2=driver.execute_script('return new Fingerprint2().get()')
getTokenId=driver.execute_script('return getTokenId()')
fingerprint=driver.find_element_by_id('fingerprint').get_attribute('value')

session = requests.session()

headers={
     "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Origin":"https://passport.58.com",
    'Content-Type':'application/x-www-form-urlencoded',
    "Upgrade-Insecure-Requests":"1",
    'Referer':'https://passport.58.com/login?path=http://my.58.com/?pts=' + str(int(round(time.time() * 1000)))
}

postData={
    "source":"pc-login",
    "path":'http://my.58.com/?pts=' + str(int(round(time.time() * 1000))),
    "password":encrypt_passwd,
    "timesign":'',
    "isremember":"false",
    "callback":"successFun",
    "yzmstate":"",
    "fingerprint":"",
    "finger2":fingerprint,
    "tokenId":getTokenId,
    "username":username,
    "validcode":"",
    "vcodekey":"",
    "btnSubmit":"登录中..."
}

rep=session.post('https://passport.58.com/login/dologin', data=postData, headers=headers)
match=re.search('\((\{.*?\})\)', rep.text)
if match:
    res_json=json.loads(match.group(1))
    print(res_json)
    if res_json['code'] == 0:
        print('登陆成功!')
    else:
        print(res_json['msg'])
