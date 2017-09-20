python2.7 Selenium 打码兔实现自动登陆phpcms后台 
# -*- coding: utf-8 -*-
# Create your views here.
import urllib2, re, time
import hashlib
import urllib2
import json
import base64

from selenium import webdriver
from PIL import Image
import damatu

''' 生成最简单的配置,这样浏览器加载的更快 '''
profileDir = "E:\\dir\\taobao\\gpfl1uyq.selects"
profile = webdriver.FirefoxProfile(profileDir)
driver = webdriver.Firefox(profile)
driver.get("http://www.hrloo.com/hrloo.php?m=admin&c=index&a=login&&pc_hash=")

''' 输入用户名 '''
input_username= driver.find_element_by_name('username')
input_username.send_keys('用户名')

''' 输入密码 '''
input_password= driver.find_element_by_name('password')
input_password.send_keys('密码')

time.sleep(2)
''' 验证码文本框 '''
input_code_select = driver.find_element_by_xpath('//*[@id="login_bg"]/div[1]/form/input[4]')


''' 由于这个验证码需要，点击input才能显示,所以我直接调用里面的js '''
driver.execute_script("document.getElementById('yzm').style.display='block'")

'''
# 也可通过 这种方法直接模拟点击,但是总会延迟
input_code_select.click()
'''

# 获取验证码图片地址
input_code = driver.find_element_by_xpath('//*[@id="code_img"]')

# 定义一个保存图片快照
driver.get_screenshot_as_file('windows.jpg')

''' 通过快照截图验证码部分图片 '''
location = input_code.location
size = input_code.size
left = location['x']
top =  location['y']
right = location['x'] + size['width']
bottom = location['y'] + size['height']
a = Image.open("windows.jpg")
im = a.crop((left,top,right,bottom))
im.save('code.jpg')

''' 此处的调用第3方打码接口,将code.jpg解码 '''
code=damatu.get_code()

''' 输入验证码 '''
input_code_select.send_keys(code)

time.sleep(2)

''' 登陆 '''
driver.find_element_by_xpath('//*[@id="login_bg"]/div[1]/form/input[1]').submit()
driver.close()


使用无窗口默认，需要设置未全屏，否则截图位置不对

driver=webdriver.PhantomJS(executable_path='C:\\Python27\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')
driver.maximize_window()
