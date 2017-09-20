# -*- coding: utf-8 -*-
import time, sys, re
import requests
import urllib
import webbrowser
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from PIL import Image

'''
用的驱动的版本是火狐51版本，低版本的智联检测的到无法出验证码，高版本的selenium不支持，其他浏览器版本智联也检测的到
'''

HEADERS={
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding":"gzip, deflate, br",
    "Connection":"keep-alive",
}

driver=webdriver.Firefox()
driver.get('https://passport.zhaopin.com/org/login?')
time.sleep(2)

def click_login():
    ''' 随便点击一下用户名框框，模拟真实请求 '''
    LoginName=driver.find_element_by_id('LoginName')
    LoginName.click()

def get_cookie():
    ''' 获取驱动Cookie '''
    dict1_cookie={}
    cookie_tmp=[]
    for cookie in driver.get_cookies():
        data="{}={}".format(cookie['name'], cookie['value'])
        dict1_cookie[cookie['name']]=cookie['value']
        cookie_tmp.append(data)
    _cookie=';'.join(cookie_tmp)
    return _cookie

def get_verify_code():
    ''' 点出验证码, 进行区域截图，将验证码截图出来，用于发送到打码兔识别验证码 '''
    code1=driver.find_element_by_id('CheckCodeCapt')
    code1.click()

    time.sleep(2)
    driver.get_screenshot_as_file('windows.jpg')

    im = Image.open("windows.jpg")
    im = im.convert('RGB')

    img = im.crop((499, 420, 773, 550))
    img.save('code.jpg')

    img2 = im.crop((680, 370, 773, 410))
    img2.save('code1.jpg')
    time.sleep(1)
    input_code_select = driver.find_element_by_xpath('//*[@id="captcha-img-sprites"]/div/i[3]')
    input_code_select.click()

class ZLZP:
    def __init__(self, user, passwd):
        self.user=user
        self.passwd=passwd

    def _get_setcookie(self, set_cookie):
        ''' 处理请求反会的set-cookie,这边只需要排除掉domain expires path 只需要cookie '''
        dict_cookie=[]
        print(set_cookie)
        for row in set_cookie.split('; '):
            x=row.strip().split('=')
            if x[0] in ['domain', 'expires', 'path']:
                continue
            dict_cookie.append('{}={}'.format(x[0], x[1]))
        return dict_cookie

    def _verify(self):
        '''
            验证码处理
            记得将参数p写在时间戳的前面，关于这个问题，搞了我２天多．
        '''
        get_verify_code()
        cookie=get_cookie()
        headers=HEADERS.copy()
        headers.update({
            'Host':'passport.zhaopin.com',
            'Content-Type':'application/x-www-form-urlencoded',
            'X-Requested-With':'XMLHttpRequest',
            'Cookie': cookie,
            'Referer':'https://passport.zhaopin.com/org/login?'}
        )
        webbrowser.open('zl_code.html')
        p=input('输入验证码:')
        postData={}
        postData['p']=p
        postData['time']=str(int(round(time.time() * 1000)))
        response=session.post('https://passport.zhaopin.com/chk/verify?callback=jsonpCallback?', data=postData, headers=headers)
        MessageText=re.search('\:\"(\w+)\"', response.text)
        if MessageText:
            CheckCode=MessageText.group(1)
        else:
            raise Exception('验证失败')
        return CheckCode


    def _login(self, CheckCode):
        click_login()
        cookie=get_cookie()
        headers=HEADERS.copy()
        headers.update({
            'Host':'passport.zhaopin.com',
            "Origin":"https://passport.zhaopin.com",
            'Content-Type':'application/x-www-form-urlencoded',
            'Cookie': cookie,
            "Upgrade-Insecure-Requests":"1",
            'Referer':'https://passport.zhaopin.com/org/login'}
        )

        postData={
            "bkurl":"",
            "LoginName":self.user,
            "Password":self.passwd,
            "CheckCode":CheckCode,
            "IsServiceCheck":"true",
            "servicecheckinput":"已勾选",
        }

        ''' 登陆的url后面需要加这一串数字 '''
        login_url="https://passport.zhaopin.com/org/login?DYWE=" + str(int(round(time.time() * 1000))) + ".235490.1496713205.149671765.3"
        response=session.post(login_url, data=postData, headers=headers)
        loginproc_new=re.search('window.location.href \= \"(.*?)\"', response.text)
        if not loginproc_new:
            raise Exception('登陆失败!')
        new_cookie=self._get_setcookie(response.headers['Set-Cookie'].replace('path=/,', ''))
        param={
            'new_cookie':cookie + ';' + ';'.join(new_cookie),
            'loginproc_new':loginproc_new.group(1)
        }
        return param

    def update_cookie(self, setcookie, oldcookie):
        '''
        将最新的cookie更新至驱动的cookie，关键性的一部，如果不处理无法进入下一步
        '''

        ''' 旧的COOKIE转换成dict1 '''
        oldcookie_dict={}
        for row in oldcookie.split(';'):
            row=row.strip()
            row_split=row.split('=')
            oldcookie_dict[row_split[0]]=row_split[1]

        ''' 新的COOKIE转换成dict1 '''
        newcookie={}
        for row in setcookie.split('; '):
            x=row.strip().split('=')
            if x[0] in ['domain', 'expires', 'path']:
                continue
            newcookie[x[0]]=x[1]

        ''' 更新新的cookie '''
        oldcookie_dict.update(newcookie)
        cookie_tmp=[]
        for cookie in oldcookie_dict:
            data="{}={}".format(cookie, oldcookie_dict[cookie])
            cookie_tmp.append(data)
        return ';'.join(cookie_tmp)

    def _chooise(self, param):
        headers=HEADERS.copy()
        headers.update({
            'Cookie': param['new_cookie'],
            "Upgrade-Insecure-Requests":"1"}
        )
        ''' allow_redirects = False 禁止302跳转, 因为下一步需要获取接口返回的cookie '''
        response=session.get(param['loginproc_new'],headers=headers, allow_redirects = False)
        login_jump_url=param['loginproc_new'].replace('http','https')

        response=session.get(login_jump_url, headers=headers, allow_redirects = False)
        check_choose=re.search('NewPinUserInfo', response.headers['Set-Cookie'])
        if not check_choose:
            raise Exception('选择频道失败')
        new_cookie=self.update_cookie(response.headers['Set-Cookie'].replace('path=/,', ''), param['new_cookie'])

        ''' id=112869402 是频道名称，自己用正则去获取 '''
        headers['Cookie']=new_cookie
        response=session.get('https://rd2.zhaopin.com/s/loginmgr/choose.asp', headers=headers, allow_redirects = False)
        window_location="https://rd2.zhaopin.com/s/loginmgr/loginpoint.asp?id=112869402&BkUrl=&deplogincount=3";
        response=session.get(window_location, headers=headers)
        login_success=re.search('公司编号：(\d+)', response.text)
        if login_success:
            print('公司编号：' + login_success.group(1))
        else:
            print(response.text)

    def _start(self):
        checkcode=self._verify()
        print(checkcode)
        param=self._login(checkcode)
        print(param)
        self._chooise(param)

if __name__ == "__main__":
    # 初始化
    session = requests.session()
    obj=ZLZP('用户名', '密码')
    obj._start()



手动打码进入控制台，直接点

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>无标题文档</title>
<style>
</style>

</head>

<body style="margin:0px;padding:0px">
<img id="imgtest" src="code.jpg" /><br />
<img src="code1.jpg" />
<script src="http://blog.abchack.com/static/jquery.min.js"></script>
<script type="text/javascript">
   var xy = '';
   $('#imgtest').click(function(e){
   if (xy == ''){
      xy = (e.pageX - $('#imgtest').offset().left ) +','+ (e.pageY - $('#imgtest').offset().top);
   }else{
      xy= xy + ';' + (e.pageX - $('#imgtest').offset().left ) +','+ (e.pageY - $('#imgtest').offset().top);
   }
    console.log("'" + xy + "'");
});
</script>
</body>
</html>