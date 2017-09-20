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

#设置一个cookie处理器，它负责从服务器下载cookie到本地，并且在发送请求时带上本地的cookie
cj = cookielib.LWPCookieJar()
cookie_support = urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(cookie_support, MultipartPostHandler.MultipartPostHandler)
urllib2.install_opener(opener)

class QCWY:
    """ 前程无忧模拟登陆 """
    def __init__(self):
        index = self.request_login()
        hidAccessKey=re.search('id\=\"hidAccessKey\" value=\"(.*?)\"', index)
        fksc=re.search('id\=\"fksc\" value=\"(.*?)\"', index)
        hidVGuid=re.search('id\=\"hidVGuid\" value=\"(.*?)\"', index)
        hidTkey=re.search('id\=\"hidTkey\" value=\"(.*?)\"', index)
        hidEhireGuid=re.search('id\=\"hidEhireGuid\" value=\"(.*?)\"', index)
        __VIEWSTATE=re.search('id\=\"__VIEWSTATE\" value=\"(.*?)\"', index)

        self.hidAccessKey=hidAccessKey.group(1)
        self.fksc=fksc.group(1)
        self.hidVGuid=hidVGuid.group(1)
        self.hidTkey=hidTkey.group(1)
        self.hidEhireGuid=hidEhireGuid.group(1)
        self.__VIEWSTATE=__VIEWSTATE.group(1)

    def request_login(self):
        ''' 载入登陆页面获取一些参数 '''
        headers = {
                    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                    'Host':'ehire.51job.com',
                    'Referer':'http://www.51job.com/?from=baidupz'
                }
        req = urllib2.Request('http://ehire.51job.com/', headers=headers)
        return opener.open(req).read()

    def verify(self):
        ''' 验证码 '''
        headers = {
                    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                    'Accept' : 'image/webp,image/*,*/*;q=0.8',
                    'Host':'ehire.51job.com',
                    'Referer':'http://ehire.51job.com/'
                }

        req = urllib2.Request('http://ehire.51job.com/ajax/Validate/LoginValidate.aspx?doType=getverify&key=' + self.hidAccessKey + '&guid=' + self.hidVGuid, headers=headers)
        picture = opener.open(req).read()
        local = open('image.jpg', 'wb')
        local.write(picture)
        local.close()

        postData = {
                    'dotype' : 'checkverift',
                    'key' : self.hidAccessKey,
                    'guid':self.hidVGuid
                }
        # 打开验证码图片
        webbrowser.open('Untitled-1.html')
        p=input('输入验证码:')
        postData['p']=str(p)

        headers = {
                    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                    'Accept' : 'application/xml, text/xml, */*',
                    'Host':'ehirelogin.51job.com',
                    'Referer':'http://ehire.51job.com/'
                }

        postData = urllib.urlencode(postData)
        request = urllib2.Request('http://ehire.51job.com/ajax/Validate/LoginValidate.aspx', postData, headers)
        response = opener.open(request)
        text = response.read()
        code=re.search('CDATA\[(\d)\]', text)
        if code.group(1) == 0:
            raise Exception, '验证失败'

    def login(self, ctmname, user, passwd):
        ''' 登陆 '''
        headers = {
                    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                    'Accept' : 'application/xml, text/xml, */*',
                    'Host':'ehirelogin.51job.com',
                    'Referer':'http://ehire.51job.com/'
                }
        postData = {
                    'd' : 'gt',
                    'key' : self.fksc
                }

        postData = urllib.urlencode(postData)
        request = urllib2.Request('http://ehire.51job.com/ajax/Sec/v.aspx', postData, headers)
        response = opener.open(request)
        text = response.read()

        sk=re.search('\.*?\[CDATA\[(.*?)\]\]', text)
        self.sk=sk.group(1)

        postData = {
            '__VIEWSTATE': self.__VIEWSTATE,
            'checkCode': '',
            'ctmName': ctmname,
            'ec': self.hidEhireGuid,
            'fksc': self.fksc,
            'hidAccessKey': self.hidAccessKey,
            'hidEhireGuid': self.hidEhireGuid,
            'hidLangType': 'Lang=&Flag=1',
            'hidRetUrl': '',
            'hidTkey': self.sk,
            'hidVGuid': self.hidVGuid,
            'isRememberMe': 'false',
            'langtype': 'Lang=&Flag=1',
            'oldAccessKey': self.hidAccessKey,
            'password': passwd,
            'referrurl': '',
            'returl': '',
            'sc': self.fksc,
            'sk': self.sk,
            'tk': '',
            'txtMemberNameCN': ctmname,
            'txtPasswordCN': passwd,
            'txtUserNameCN': user,
            'userName': user,
            'verifyGuid': self.hidVGuid
        }

        postData = urllib.urlencode(postData)
        request = urllib2.Request('https://ehirelogin.51job.com/Member/UserLogin.aspx?', postData, headers)
        response = opener.open(request)
        text = response.read()

        # 如果在其他浏览器已经登陆,先退出在登陆
        from_re = re.search('(UserOffline\.aspx\?tokenId.*?)\"', text)
        if from_re:
            useroffline='http://ehire.51job.com/Member/{}'.format(from_re.group(1))
            useroffline=useroffline.replace('amp;','')

            __VIEWSTATE=re.search('id\=\"__VIEWSTATE\" value=\"(.*?)\"', text)
            postData = {
                    '__EVENTARGUMENT' : 'KickOut$0',
                    '__EVENTTARGET' : 'gvOnLineUser',
                    '__VIEWSTATE' : __VIEWSTATE.group(1)
                }
            headers = {
                        'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                        'Accept' : 'application/x-ms-application, image/jpeg, application/xaml+xml, image/gif, image/pjpeg, application/x-ms-xbap, */*',
                        'Content-Type':'application/x-www-form-urlencoded',
                        'Accept-Language':'zh-CN',
                        'Host':'ehire.51job.com',
                        'Referer':useroffline
                    }
            postData = urllib.urlencode(postData)
            request = urllib2.Request(useroffline, postData, headers)
            response = opener.open(request)
            text = response.read()
        print text

    def start(self):
        # 会员名
        ctmname=''
        # 用户名
        user=''
        # 密码
        passwd=''
        self.verify()
        self.login(ctmname, user, passwd)

if __name__ == "__main__":
    obj=QCWY()
    obj.start()
HTML

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>无标题文档</title>
<style>

.clearFix:after{display:block;content:'';height:0;clear:both;visibility:hidden;}
.clearFix{display:block;*zoom:1;}
.clearfix:after{display:block;content:'';height:0;clear:both;visibility:hidden;}
.clearfix{display:block;*zoom:1;}
i { display:block; float:left;}
</style>

</head>

<body>
<div class="clearfix">
<i style=" display:block;width:22px; height:40px; background-image:url(image.jpg);background-position: -264px 0px;"></i>
<i style=" display:block;width:22px; height:40px; background-image:url(image.jpg);background-position: -154px 0px;"></i>
<i style=" display:block;width:22px; height:40px; background-image:url(image.jpg);background-position: -44px 0px;"></i>
<i style=" display:block;width:22px; height:40px; background-image:url(image.jpg);background-position: -242px 0px;"></i>
<i style=" display:block;width:22px; height:40px; background-image:url(image.jpg);background-position: -110px 0px;"></i>
<i style=" display:block;width:22px; height:40px; background-image:url(image.jpg);background-position: -176px 0px;"></i>
<i style=" display:block;width:22px; height:40px; background-image:url(image.jpg);background-position: -88px 0px;"></i>
</div>
<br/>
<div id="imgtest" style="width:330px; height:116px; background:url(image.jpg) no-repeat;">
<div class="clearfix">
<i style="display display:block;width:6.666%; height:58px; background-image:url(image.jpg);background-position: -66px -40px;"></i>
<i style=" :block;width:6.666%; height:58px; background-image:url(image.jpg);background-position: -286px -40px;"></i>
<i style=" display:block;width:6.666%; height:58px; background-image:url(image.jpg);background-position: -66px -98px;"></i>
<i style=" display:block;width:6.666%; height:58px; background-image:url(image.jpg);background-position: -44px -40px;"></i>
<i style=" display:block;width:6.666%; height:58px; background-image:url(image.jpg);background-position: -154px -40px;"></i>
<i style=" display:block;width:6.666%; height:58px; background-image:url(image.jpg);background-position: -22px -40px;"></i>
<i style=" display:block;width:6.666%; height:58px; background-image:url(image.jpg);background-position: -88px -98px;"></i>
<i style=" display:block;width:6.666%; height:58px; background-image:url(image.jpg);background-position: -198px -40px;"></i>
<i style=" display:block;width:6.666%; height:58px; background-image:url(image.jpg);background-position: -198px -98px;"></i>
<i style=" display:block;width:6.666%; height:58px; background-image:url(image.jpg);background-position: -264px -98px;"></i>
<i style=" display:block;width:6.666%; height:58px; background-image:url(image.jpg);background-position: -308px -40px;"></i>
<i style=" display:block;width:6.666%; height:58px; background-image:url(image.jpg);background-position: -176px -40px;"></i>
<i style=" display:block;width:6.666%; height:58px; background-image:url(image.jpg);background-position: -0px -98px;"></i>
<i style=" display:block;width:6.666%; height:58px; background-image:url(image.jpg);background-position: -132px -98px;"></i>
<i style=" display:block;width:6.666%; height:58px; background-image:url(image.jpg);background-position: -132px -40px;"></i>
<div class="clearfix">
</div>
<i style=" display:block;width:6.666%; height:58px; background-image:url(image.jpg);background-position: -176px -98px;"></i>
<i style=" display:block;width:6.666%; height:58px; background-image:url(image.jpg);background-position: -88px -40px;"></i>
<i style=" display:block;width:6.666%; height:58px; background-image:url(image.jpg);background-position: -154px -98px;"></i>
<i style=" display:block;width:6.666%; height:58px; background-image:url(image.jpg);background-position: -220px -40px;"></i>
<i style=" display:block;width:6.666%; height:58px; background-image:url(image.jpg);background-position: -264px -40px;"></i>
<i style=" display:block;width:6.666%; height:58px; background-image:url(image.jpg);background-position: -110px -40px;"></i>
<i style=" display:block;width:6.666%; height:58px; background-image:url(image.jpg);background-position: -242px -98px;"></i>
<i style=" display:block;width:6.666%; height:58px; background-image:url(image.jpg);background-position: -286px -98px;"></i>
<i style=" display:block;width:6.666%; height:58px; background-image:url(image.jpg);background-position: -0px -40px;"></i>
<i style=" display:block;width:6.666%; height:58px; background-image:url(image.jpg);background-position: -242px -40px;"></i>
<i style=" display:block;width:6.666%; height:58px; background-image:url(image.jpg);background-position: -44px -98px;"></i>
<i style=" display:block;width:6.666%; height:58px; background-image:url(image.jpg);background-position: -220px -98px;"></i>
<i style=" display:block;width:6.666%; height:58px; background-image:url(image.jpg);background-position: -22px -98px;"></i>
<i style=" display:block;width:6.666%; height:58px; background-image:url(image.jpg);background-position: -308px -98px;"></i>
<i style=" display:block;width:6.666%; height:58px; background-image:url(image.jpg);background-position: -110px -98px;"></i>
</div>
</div>

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
