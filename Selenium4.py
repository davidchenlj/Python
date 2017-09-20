Selenium模拟搜索点击搜索功能.
# -*- coding: utf-8 -*-
# Create your views here.
import urllib2, re, time
from selenium import webdriver

driver = webdriver.Firefox()
driver.get("http://blog.arthl.com/blog/index/")

''' 打开URL 输入python 点击搜索'''
input_key = driver.find_element_by_xpath('/html/body/div[1]/div/nav/form/div/input')
input_key.send_keys('python')
input_key.submit()

''' 获取源码 '''
html_source = driver.page_source
print html_source

driver.close()
