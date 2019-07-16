#-*- coding=utf-8 -*-#

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

#生成一个浏览器的实例对象
driver = webdriver.Chrome()
#跳转到要打开的url
driver.get('http://kingcms.beta.wsd.com/htdoc/main#?pageId=102435')

#登录
def loginweb():
	path0 = "//iframe[contains(@frameborder,'0')]"
	#等待页面找到元素
	WebDriverWait(driver,10,0.5).until(EC.presence_of_element_located((By.XPATH,path0)))
    #切换到ifame
	driver.switch_to.frame(driver.find_element_by_xpath(path0))
	#等待页面找到元素
	WebDriverWait(driver,10,0.5).until(EC.presence_of_element_located((By.NAME,"txtLoginName")))
	#输入用户名
	driver.find_element_by_name("txtLoginName").send_keys("v_rhcchen")
	#点击outlook
	driver.find_element_by_css_selector("p[class = 'login_outlook']").click()
	#输入密码
	driver.find_element_by_id("txtPassword").send_keys("*****")
	#点击确定
	driver.find_element_by_name("ibnLogin").click()
	print "登录成功\n"


#查询补丁
def checkpatch(i):
	path1 = "/html/body/div[2]/div/div/div/div/form/div/div/div[1]/div/div/input"
	path2 ="/html/body/div[2]/div/div/div/div/form/div/div/div[6]/a[1]"
	#等待页面找到元素
	WebDriverWait(driver,10,0.5).until(EC.presence_of_element_located((By.XPATH,path1)))
	#输入需要查询的补丁ID
	driver.find_element_by_xpath(path1).send_keys(i)
	time.sleep(1)
	#点击查询
	driver.find_element_by_xpath(path2).click()
	time.sleep(2)
	
	


#下载补丁的url
def geturl():
	path3 = "/html/body/div[2]/div/div/div/div/div[3]/table/tbody/tr[1]/td[9]/span[5]/a"
	path4 = "//*[@id='field-url']/div/input"
	#点击编辑
	driver.find_element_by_xpath(path3).click()
	time.sleep(4)
    #切换到ifame
	driver.switch_to.frame(driver.find_element_by_xpath("//iframe[contains(@frameborder,'0')]"))
	# driver.switch_to.default_content()
	time.sleep(2)

	#获得url的值，将其赋值到url 
	url = driver.find_element_by_xpath(path4).get_attribute('value')
	print url
	#把补丁的URL写入文档
	writeurls(url)
	time.sleep(2)
	reflash_page()

#把补丁的URL写入文档
def writeurls(url):
	with open("path_urls.txt", "a") as f:
		f.write(url + '\n')

#更新页面
def reflash_page():
	path5 = "/html/body/section/nav/div[3]/ul[3]/li[8]/i"
	driver.switch_to.default_content()
	time.sleep(2)
	driver.find_element_by_xpath(path5).click()
	time.sleep(1)
	driver.switch_to.frame(driver.find_element_by_xpath("//iframe[contains(@frameborder,'0')]"))
	time.sleep(2)

#该方法主要用于下架补丁
def patch_down():
	path3 = "/html/body/div[2]/div/div/div/div/div[3]/table/tbody/tr[1]/td[9]/span[5]/a"
	path6 = "//*[@id='field-status']/label[1]/input"
	path7 = "/html/body/div[2]/div/div/form/div[2]/button[2]"	
	#点击编辑
	driver.find_element_by_xpath(path3).click()
	time.sleep(4)

	driver.switch_to.frame(driver.find_element_by_xpath("//iframe[contains(@frameborder,'0')]"))
	# driver.switch_to.default_content()
	WebDriverWait(driver,5,0.5).until(EC.presence_of_element_located((By.XPATH,path6)))

	driver.find_element_by_xpath(path6).click()
	driver.find_element_by_xpath(path7).click()
	time.sleep(2)
	reflash_page()

#判断补丁的状态，如已经为无效，则跳过。如为有效，则调用patch_down方法，将其设置为无效
def patch_status():
	
	path8 = "/html/body/div[2]/div/div/div/div/div[3]/table/tbody/tr[1]/td[4]/div"
	path1 = "/html/body/div[2]/div/div/div/div/form/div/div/div[1]/div/div/input"
	WebDriverWait(driver,5,0.5).until(EC.presence_of_element_located((By.XPATH,path8)))
	staus = driver.find_element_by_xpath(path8).text
	# print staus

	if(staus == u'无效'):
		print "补丁已经为无效，不用处理!"
		driver.find_element_by_xpath(path1).clear()
		# checkpatch(i+1)
	else:
		print "补丁为有效，正在处理!"
		time.sleep(2)
		patch_down()
		print "补丁成功设置为无效！"

#获取补丁的策略信息
def getrules():
	path9 = "/html/body/div[2]/div/div/div/div/div[3]/table/tbody/tr[1]/td[9]/span[6]/a"
	path10 = "/html/body/div[2]/div/div/div/div/div[4]/div/div[1]/span"
	driver.find_element_by_xpath(path9).click()
	driver.switch_to.frame(driver.find_element_by_xpath("//iframe[contains(@frameborder,'0')]"))

	WebDriverWait(driver,5,0.5).until(EC.presence_of_element_located((By.XPATH,path10)))
	rules_num = driver.find_element_by_xpath(path10).text
	print rules_num + "\n"
	# print type(rules_num)
	writedata(rules_num)

	reflash_page()

#把每一个补丁的策略数据写入一个文件
def writedata(data):
	with open("rules_data.txt",'a') as f:
		f.write(data.encode('utf-8')+ "\n")



#主方法
if __name__ == "__main__":
	#登录
	loginweb()
	time.sleep(3)
	#设置要下载url的补丁ID的范围
	for i in xrange(7300,7341):
		print "正在处理的补丁ID为：" + str(i) + '\n'
		checkpatch(i)
		#判断补丁的状态，如已经为无效，则跳过。如为有效，则调用patch_down方法，将其设置为无效
		

		#geturl方法，去获取补丁的URL
		# geturl()
	
		#获取补丁的策略信息
		getrules()

	driver.quit()
