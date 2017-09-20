Selenium常用语法，原文地址http://www.cnblogs.com/luxiaojun/p/6144748.html
pageLoadTimeout 设置页面完全加载的超时时间，完全加载即完全渲染完成，同步和异步脚本都执行完

setScriptTimeout 设置异步脚本的超时时间

implicitlyWait 识别对象的智能等待时间

from selenium import webdriver
obj = webdriver.PhantomJS(executable_path="D:\Python27\Scripts\phantomjs.exe")
obj.set_page_load_timeout(5)
try:
    obj.get('http://www.xiaohuar.com')
    print obj.title
except Exception as e:
    print e
选择器
from selenium import webdriver
obj = webdriver.PhantomJS(executable_path="D:\Python27\Scripts\phantomjs.exe")
obj.set_page_load_timeout(5)
try:
    obj.get('http://www.baidu.com')
    obj.find_element_by_id('kw')                    #通过ID定位
    obj.find_element_by_class_name('s_ipt')         #通过class属性定位
    obj.find_element_by_name('wd')                  #通过标签name属性定位
    obj.find_element_by_tag_name('input')           #通过标签属性定位
    obj.find_element_by_css_selector('#kw')         #通过css方式定位
    obj.find_element_by_xpath("//input[@id='kw']")  #通过xpath方式定位
    obj.find_element_by_link_text("贴吧")           #通过xpath方式定位
 
    print obj.find_element_by_id('kw').tag_name   #获取标签的类型
except Exception as e:
    print e　　
调用启动的浏览器不是全屏的，有时候会影响我们的某些操作，所以我们可以设置全屏
from selenium import webdriver
obj = webdriver.PhantomJS(executable_path="D:\Python27\Scripts\phantomjs.exe")
obj.set_page_load_timeout(5)
obj.maximize_window()  #设置全屏
try:
    obj.get('http://www.baidu.com')
    obj.save_screenshot('11.png')  # 截取全屏，并保存
except Exception as e:
    print e
设置浏览器宽、高
from selenium import webdriver
obj = webdriver.PhantomJS(executable_path="D:\Python27\Scripts\phantomjs.exe")
obj.set_page_load_timeout(5)
obj.set_window_size('480','800') #设置浏览器宽480，高800
try:
    obj.get('http://www.baidu.com')
    obj.save_screenshot('12.png')  # 截取全屏，并保存
except Exception as e:
    print e
操作浏览器前进、后退
from selenium import webdriver
obj = webdriver.PhantomJS(executable_path="D:\Python27\Scripts\phantomjs.exe")
try:
    obj.get('http://www.baidu.com')   #访问百度首页
    obj.save_screenshot('1.png')
    obj.get('http://www.sina.com.cn') #访问新浪首页
    obj.save_screenshot('2.png')
    obj.back()                           #回退到百度首页
    obj.save_screenshot('3.png')
    obj.forward()                        #前进到新浪首页
    obj.save_screenshot('4.png')
except Exception as e:
    print e
键盘按键用法
from selenium.webdriver.common.keys import Keys
obj = webdriver.PhantomJS(executable_path="D:\Python27\Scripts\phantomjs.exe")
obj.set_page_load_timeout(5)
try:
    obj.get('http://www.baidu.com')
    obj.find_element_by_id('kw').send_keys(Keys.TAB)   #用于清除输入框的内容,相当于clear()
    obj.find_element_by_id('kw').send_keys('Hello')   #在输入框内输入Hello
    obj.find_element_by_id('su').send_keys(Keys.ENTER) #通过定位按钮，通过enter（回车）代替click()
 
except Exception as e:
    print e	
键盘组合键使用
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
obj = webdriver.PhantomJS(executable_path="D:\Python27\Scripts\phantomjs.exe")
obj.set_page_load_timeout(5)
try:
    obj.get('http://www.baidu.com')
    obj.find_element_by_id('kw').send_keys(Keys.TAB)   #用于清除输入框的内容,相当于clear()
    obj.find_element_by_id('kw').send_keys('Hello')   #在输入框内输入Hello
    obj.find_element_by_id('kw').send_keys(Keys.CONTROL,'a')   #ctrl + a 全选输入框内容
    obj.find_element_by_id('kw').send_keys(Keys.CONTROL,'x')   #ctrl + x 剪切输入框内容
except Exception as e:
    print e
鼠标右击
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
obj = webdriver.PhantomJS(executable_path="D:\Python27\Scripts\phantomjs.exe")
try:
    obj.get("http://pan.baidu.com")
    obj.find_element_by_id('TANGRAM__PSP_4__userName').send_keys('13201392325')   #定位并输入用户名
    obj.find_element_by_id('TANGRAM__PSP_4__password').send_keys('18399565576lu') #定位并输入密码
    obj.find_element_by_id('TANGRAM__PSP_4__submit').submit()                     #提交表单内容
    f = obj.find_element_by_xpath('/html/body/div/div[2]/div[2]/....')            #定位到要点击的标签
    ActionChains(obj).context_click(f).perform()                                  #对定位到的元素进行右键点击操作
except Exception as e:
    print e
鼠标双击
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
obj = webdriver.PhantomJS(executable_path="D:\Python27\Scripts\phantomjs.exe")
try:
    obj.get("http://pan.baidu.com")
    obj.find_element_by_id('TANGRAM__PSP_4__userName').send_keys('13201392325')   #定位并输入用户名
    obj.find_element_by_id('TANGRAM__PSP_4__password').send_keys('18399565576lu') #定位并输入密码
    obj.find_element_by_id('TANGRAM__PSP_4__submit').submit()                     #提交表单内容
    f = obj.find_element_by_xpath('/html/body/div/div[2]/div[2]/....')            #定位到要点击的标签
    ActionChains(obj).double_click(f).perform()                                   #对定位到的元素进行双击操作
except Exception as e:
    print e
