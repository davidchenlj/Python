Python抓取自动登录自动打码抓取社保后台账户,目前这个版本仅仅是抓取深圳/东莞社保局的,打码采用联众打码平台,代码抓取后自动保存数据，写入数据部分，自己微调下.
# 深圳版本社保局

#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import sys, os
import HTMLParser
import urlparse
import urllib
import urllib2
import cookielib
import webbrowser
import string
import re, json
import MultipartPostHandler
from BeautifulSoup import BeautifulSoup

from login_sb.models import sb_list, user_list


reload(sys)
sys.setdefaultencoding('utf-8')

user_name='联众平台账户'
user_pw='联众平台密码'

''' 登陆社保局获取社保账户 '''

# 登录的主页面
url = 'https://wssb6.szsi.gov.cn/NetApplyWeb/index.jsp'

#设置一个cookie处理器，它负责从服务器下载cookie到本地，并且在发送请求时带上本地的cookie
cj = cookielib.LWPCookieJar()
cookie_support = urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(cookie_support, MultipartPostHandler.MultipartPostHandler)
urllib2.install_opener(opener)

class Dict(dict):
    def __missing__(self, key):
        rv = self[key] = type(self)()
        return rv

def api_code():
	''' 自动打码用户名密码 '''
    data ={
        "user_name":user_name,
        "user_pw":user_pw,
        "yzm_minlen":"",
        "yzm_maxlen":"",
        "yzmtype_mark":"",
        "zztool_token":"",
        "upload":open('image.jpg', "rb")
    }

    response=opener.open('http://v1-http-api.jsdama.com/api.php?mod=php&act=upload', data)
    text = response.read()
    response.close()
    json_data=json.loads(text)
    if json_data['result'] == True:
        return json_data['data']['val']
    else:
        raise Exception, '获取CODE失败!'

class LOGINSB:
    def __init__(self, username='', passwd='', pk=''):
        self.headers = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
            'Referer' : 'https://wssb6.szsi.gov.cn/NetApplyWeb/index.jsp'
        }
        self.username=username
        self.passwd=passwd
        self.pk=pk

    def login(self):
        ''' 登陆 '''
        #pscode = input("code:")
        #pscode=str(pscode).strip()
        pscode=api_code()

        postData = {
            'user' : self.username,
            'password' : self.passwd,
            'pscode' : pscode,
            'isIE' : 0,
            'type' : ''
        }
        postData = urllib.urlencode(postData)
        request = urllib2.Request(url, postData, self.headers)
        response = opener.open(request)
        text = response.read()
        text=text.decode('gbk')
        m=re.search('pid=(.*?)\';', text)
        if not m:
            raise Exception, '登陆失败!'
        print '登陆成功..'
        # 返回登陆后的pid
        return m.group(1)

    def get_pscode(self):
        ''' 获取登陆验证码写入本地 '''
        req = urllib2.Request('https://wssb6.szsi.gov.cn/NetApplyWeb/CImages', headers=self.headers)
        picture = opener.open(req).read()
        local = open('image.jpg', 'wb')
        local.write(picture)
        local.close()

    def get_data(self, pid, page=1, currPage=1):
        postData = {
            'type' : 1,
            'PageNum' : 1,
            'PagePDCode' : 0,
            'pid' : pid,
            'queryType' : 1,
            'queryCode' : '',
            'queryId' : '',
            'queryDept' : '',
            'currPage' : currPage,
            'currPage1' : '',
            'page' : page
        }
        headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                   'Referer' : 'https://wssb6.szsi.gov.cn/NetApplyWeb/dwyggl/dwrycx.jsp'}
        postData = urllib.urlencode(postData)
        request = urllib2.Request('https://wssb6.szsi.gov.cn/NetApplyWeb/dwyggl/dwrycx.jsp', postData, headers)
        response = opener.open(request)
        text = response.read()
        text=text.decode('gbk')
        return text

    def para_html(self, text):
		''' 抓取数据，解析table '''
        soup = BeautifulSoup(text)
        tables = soup.findAll(attrs={'onmouseout':re.compile("this.className=''")})
        c=1
        for i in range(0, 11):
            try:
                tab = tables[i]
            except:
                continue
            p=0
            dict1=Dict()
            for tr in tab.findAll('td'):
                if p == 1:
                    dict1[i]['name']=tr.getText()
                if p == 2:
                    dict1[i]['num']=tr.getText()
                if p == 3:
                    dict1[i]['huj']=tr.getText()
                if p == 4:
                    dict1[i]['shenfz']=tr.getText()
                if p == 5:
                    dict1[i]['gongz']=tr.getText()
                if p == 6:
                    dict1[i]['status']=tr.getText()
                if p == 7:
                    dict1[i]['yangl']=tr.getText()
                if p == 8:
                    dict1[i]['gongs']=tr.getText()
                if p == 9:
                    dict1[i]['yil']=tr.getText()
                if p == 10:
                    dict1[i]['shiy']=tr.getText()
                if p == 11:
                    dict1[i]['shengy']=tr.getText()
                p=p+1

            # 插入数据
            for row in dict1:
                row=dict1[row]
                sb_list.objects.create(
                    name=row['name'],
                    num=row['num'],
                    huj=row['huj'],
                    shenfz=row['shenfz'],
                    gongz=row['gongz'],
                    status=row['status'],
                    yangl=row['yangl'],
                    gongs=row['gongs'],
                    yil=row['yil'],
                    shiy=row['shiy'],
                    shengy=row['shengy'],
                    dateline = int(time.time()),
                    user_id = self.pk
                )

def run_main(username, passwd, pk):
	''' 社保局用户名/密码 '''
    obj=LOGINSB(username, passwd, pk)
    print 'get_code'
    pascode=obj.get_pscode()
    print 'login'
    pid=obj.login()
    print pid
    for i in range(1,200):
        print '第%s页' % i
        if i == 1:
            text=obj.get_data(pid)
            obj.para_html(text)
        else:
            page=i-1
            currPage=i
            try:
                text=obj.get_data(pid, page, currPage)
                obj.para_html(text)
            except:
                print '获取结束...'
                return

# 东莞社保局
#!/usr/bin/python
# -*- coding: utf-8 -*-
import xlrd
import xlwt
import time
import sys, os
import HTMLParser
import urlparse
import urllib
import urllib2
import cookielib
import webbrowser
import string
import re, json
import ssl
import MultipartPostHandler
from BeautifulSoup import BeautifulSoup
from login_sb.models import sb_dg_list, user_list
#from login_sb.models import sb_list, user_list


reload(sys)
sys.setdefaultencoding('utf-8')

''' 登陆社保局获取社保账户 '''

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

# 登录的主页面
url = 'https://wssb.dgsi.gov.cn/action/LoginAcessAction'

post_url='https://wssb.dgsi.gov.cn/action/LoginAcessAction'

#设置一个cookie处理器，它负责从服务器下载cookie到本地，并且在发送请求时带上本地的cookie
cj = cookielib.LWPCookieJar()
cookie_support = urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(cookie_support, MultipartPostHandler.MultipartPostHandler)
urllib2.install_opener(opener)

class Dict(dict):
    def __missing__(self, key):
        rv = self[key] = type(self)()
        return rv

def api_code():
    data ={
        "user_name":"",
        "user_pw":"",
        "yzm_minlen":"",
        "yzm_maxlen":"",
        "yzmtype_mark":"",
        "zztool_token":"",
        "upload":open('image.jpg', "rb")
    }

    response=opener.open('http://v1-http-api.jsdama.com/api.php?mod=php&act=upload', data)
    text = response.read()
    response.close()
    json_data=json.loads(text)
    if json_data['result'] == True:
        return json_data['data']['val']
    else:
        raise Exception, '获取CODE失败!'

class LOGINSB:
    def __init__(self, username='', passwd='', pk=''):
        self.headers = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
            'Referer' : 'https://wssb.dgsi.gov.cn/'
        }
        self.username=username
        self.passwd=passwd
        self.pk=pk

    def login(self):
        ''' 登陆 '''
        pscode=api_code()
        postData = {
            'dwshbzh' : self.username,
            'password' : self.passwd,
            'imagecheck' : pscode,
            'logintype' : 1,
            'signData' : ''
        }
        postData = urllib.urlencode(postData)
        request = urllib2.Request(url, postData, self.headers)
        response = opener.open(request)
        text = response.read()
        text=text.decode('gbk')

        ''' 判断是否登陆 '''
        is_no_login=re.search('此用户已经登陆，不能重复登录，请稍候再试', text)
        if is_no_login:
            raise Exception, text

        is_login=re.search('(https.*?&caid=)', text)
        if not is_login: raise Exception, text

        ''' 登陆后需要请求一次返回的链接  '''
        request = urllib2.Request(is_login.group(1), self.headers)
        response = opener.open(request)
        text = response.read()
        text=text.decode('gbk')

        ''' 打开台账菜单 '''
        request = urllib2.Request('https://wssb.dgsi.gov.cn/dwwssb/action/MainAction?menuid=103403&ActionType=q_dwjftzcx&target=q_dwjftzcx_yqyf', self.headers)
        response = opener.open(request)
        text = response.read()
        text=text.decode('gbk')

        ''' 获取excel链接 '''
        excel_url=re.search('(/dwwssb/pages/svc_writeExcel.jsp.*?)\"', text)
        if not excel_url: raise Exception, '获取excel链接失败!'

        ''' 按照2进制方式写入excel '''
        request = urllib2.Request('https://wssb.dgsi.gov.cn%s' % excel_url.group(1), self.headers)
        response = opener.open(request)
        text = response.read()
        local = open('excel.xls', 'wb')
        local.write(text)
        local.close()

    def get_pscode(self):
        ''' 获取登陆验证码写入本地 '''
        reqs = urllib2.Request('https://wssb.dgsi.gov.cn/', headers=self.headers)
        opener.open(reqs).read()
        req = urllib2.Request('https://wssb.dgsi.gov.cn/pages/checkimage.JSP', headers=self.headers)
        picture = opener.open(req).read()
        local = open('image.jpg', 'wb')
        local.write(picture)
        local.close()

    def get_data(self, pid, page=1, currPage=1):
        postData = {
            'type' : 1,
            'PageNum' : 1,
            'PagePDCode' : 0,
            'pid' : pid,
            'queryType' : 1,
            'queryCode' : '',
            'queryId' : '',
            'queryDept' : '',
            'currPage' : currPage,
            'currPage1' : '',
            'page' : page
        }
        headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                   'Referer' : 'https://wssb6.szsi.gov.cn/NetApplyWeb/dwyggl/dwrycx.jsp'}
        postData = urllib.urlencode(postData)
        request = urllib2.Request('https://wssb6.szsi.gov.cn/NetApplyWeb/dwyggl/dwrycx.jsp', postData, headers)
        response = opener.open(request)
        text = response.read()
        text=text.decode('gbk')
        return text

    def logout(self):
        ''' 此平台每次登陆后需要退出，否则会显示已经有账号登陆 '''
        reqs = urllib2.Request('https://wssb.dgsi.gov.cn/dwwssb/action/MainAction?menuid=000098&ActionType=quit', headers=self.headers)
        opener.open(reqs).read()
        print '退出'

    def write_data(self):
        ''' 写入数据 '''
        ''' 打开excel '''
        workbook = xlrd.open_workbook(r'excel.xls',encoding_override="cp1252")
        ''' 获取第一列 '''
        sheet2_name = workbook.sheet_names()[0]
        sheet2 = workbook.sheet_by_name(sheet2_name)
        ''' 获取excel多少行 '''
        sheet_count = sheet2.nrows
        ''' 读取数据 '''
        for row in range(sheet_count):
            if row == 0: continue
            rows = sheet2.row_values(row)
            sb_dg_list.objects.create(
                number=rows[1],
                name=rows[2],
                dates=rows[3],
                insured=rows[4],
                base=rows[5],
                employer=rows[6],
                personal=rows[7],
                employer_bj=rows[8],
                personal_bj=rows[9],
                buj_lx=rows[10],
                znj=rows[11],
                total=rows[12],
                dateline = int(time.time()),
                user_id = self.pk
            )

def run_main(username, passwd, pk):
    obj=LOGINSB(username, passwd, pk)
    print 'get_code'
    pascode=obj.get_pscode()
    print 'login'
    try:
        obj.login()
        print '写EXCEL'
        obj.write_data()
        print '开始退出'
        obj.logout()
    except Exception as error:
        print str(error)
        obj.logout()
        raise Exception, str(error)
