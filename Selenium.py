# -*- coding: utf-8 -*- 
import time, sys, re
import requests
from selenium import webdriver
driver=webdriver.Firefox()
from http.cookies import SimpleCookie
rawdata='uid=CgEKnVjwNboO1DJ6AwMGAg==; gr_user_id=f7a40ec2-a9c6-4bc1-859f-468d1f5f8673; POPUP_FOR_ADDQQ=1; isShowScribeGuide=true; isShowGuide=true; Hm_lvt_dd58e556038953b607e324882d88e683=1492411328,1493201818,1493946119,1494224111; _wxbind_cookie=1; HR_GLOBAL_POP=MFkQcFhnUTNiQ3RMNVU9; hauth=WS1MT3R4SEFZV1FjalRvcFV0dysyMkRNejZWU1JhZThJUkZaVGdPRjAvQnpWMVc2THVCM3pvdjVWdUplMFdrajR3cmRrZEVydEVucUFzPQ%3D%3D; CE2u_fb25_auth=971ejMRcXnzOjXD7dB8QslvQOVdZ7ODx%2FNhHowK9K8RN38T4bARkxKMDcy3ds11ENKppEHaLd0zM0yrwpm44VUF7; PHPSESSID=3dcda944e674cb8f5373c6d6638d1ea6; fensiNumCount=0; _ga=GA1.2.1921903929.1492137418; _gid=GA1.2.588160865.1499656859; Hm_lvt_9a72351d0103e8e2a62c3abba9bb349e=1499154666,1499656859,1499681916,1499735473; Hm_lpvt_9a72351d0103e8e2a62c3abba9bb349e=1499735475'

cookie = SimpleCookie(rawdata)
driver.get('http://www.hrloo.com')

for i in cookie.values():
    driver.add_cookie({'name':i.key, 'value':i.value, 'path':'/', 'secure':False})
driver.get('http://www.hrloo.com/hrloo.php?m=admin&c=index&a=init&&pc_hash=')
