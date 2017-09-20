打码兔自动打码接口,官方只提供python3.2版本现修改为支持python2.7版本.

# -*- coding: utf-8 -*-
#python版本2.7

import hashlib
import urllib2
import urllib
import json
import base64

def md5str(str): #md5加密字符串
    m=hashlib.md5(str.encode(encoding = "utf-8"))
    return m.hexdigest()

def md5(byte): #md5加密byte
    return hashlib.md5(byte).hexdigest()

class DamatuApi():

    ID = '40838'
    KEY = 'ca9507e17e8d5ddf7c57cd18d8d33010'
    HOST = 'http://api.dama2.com:7766/app/'


    def __init__(self,username,password):
        self.username=username
        self.password=password

    def getSign(self,param=b''):
        return md5(self.KEY + self.username + param)[:8]

    def getPwd(self):
        return md5str(self.KEY +md5str(md5str(self.username) + md5str(self.password)))

    def post(self,path,params={}):
        data = urllib.urlencode(params)
        url = self.HOST + path
        response = urllib2.Request(url,data)
        return urllib2.urlopen(response).read()

    def getBalance(self):
        ''' 查询余额 return 是正数为余额 如果为负数 则为错误码 '''
        data={'appID':self.ID,
        'user':self.username,
        'pwd':self.getPwd(),
        'sign':self.getSign()
        }
        res = self.post('d2Balance',data)
        res = str(res)
        jres = json.loads(res)
        if jres['ret'] == 0:
            return jres['balance']
        else:
            return jres['ret']

    def decode(self,filePath,type):
        ''' 上传验证码 参数filePath 验证码图片路径 如d:/1.jpg type是类型，查看http://wiki.dama2.com/index.php?n=ApiDoc.Pricedesc  return 是答案为成功 如果为负数 则为错误码 '''
        f=open(filePath,'rb')
        fdata=f.read()
        filedata=base64.b64encode(fdata)
        f.close()
        data={
            'appID':self.ID,
            'user':self.username,
            'pwd':self.getPwd(),
            'type':type,
            'fileDataBase64':filedata,
            'sign':self.getSign(fdata)
        }
        res = self.post('d2File',data)
        res = str(res)
        jres = json.loads(res)
        if jres['ret'] == 0:
            #注意这个json里面有ret，id，result，cookie，根据自己的需要获取
            return(jres['result'])
        else:
            return jres['ret']

    def decodeUrl(self,url,type):
        ''' url地址打码 参数 url地址  type是类型(类型查看http://wiki.dama2.com/index.php?n=ApiDoc.Pricedesc) return 是答案为成功 如果为负数 则为错误码 '''
        data={
            'appID':self.ID,
            'user':self.username,
            'pwd':self.getPwd(),
            'type':type,
            'url':urllib.parse.quote(url),
            'sign':self.getSign(url.encode(encoding = "utf-8"))
        }
        res = self.post('d2Url',data)
        res = res
        jres = json.loads(res)
        if jres['ret'] == 0:
            #注意这个json里面有ret，id，result，cookie，根据自己的需要获取
            return jres['result']
        else:
            return jres['ret']

    def reportError(self,id):
        ''' 报错 参数id(string类型)由上传打码函数的结果获得 return 0为成功 其他见错误码 '''
        data={'appID':self.ID,
            'user':self.username,
            'pwd':self.getPwd(),
            'id':id,
            'sign':self.getSign(id.encode(encoding = "utf-8"))
        }
        res = self.post('d2ReportError',data)
        res = str(res)
        jres = json.loads(res)
        return jres['ret']
 
 
# 调用类型实例：
#1.实例化类型 参数是打码兔用户账号和密码 
dmt=DamatuApi("用户名","密码")
# 2.调用方法：
print(dmt.getBalance()) #查询余额 
print(dmt.decode('hrloo.jpg',200)) #上传打码
#print(dmt.decodeUrl('http://captcha.qq.com/getimage?aid=549000912&r=0.7257105156128585&uin=3056517021',200)) #上传打码
#print(dmt.reportError('894657096')) #上报错误
