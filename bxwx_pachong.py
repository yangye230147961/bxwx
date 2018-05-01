#coding=utf-8
import requests
from bs4 import BeautifulSoup


#==========核心函数========
def rqe(url):
	#请求页面函数，返回html
	headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36'}
	a=requests.get(url,headers=headers)
	#设置UA伪装成浏览器
	a.encoding=a.apparent_encoding
	#重点！
	#从网页获取文本编码 
	return a.text
	
	
def fxurl(html):
	#分析源码
	#返回:下页URL,标题,文章内容
	soup=BeautifulSoup(html,'html.parser')
	#重点！！！
	#转换为bs型数据，添加解析器！！！！
	j=soup.find_all(class_="p3")
	ll=j[0]
	#重点,查找id=pt_next的元素(下一页url)
	#.find(属性=参数)搜索单一元素
	lj=ll.find("a")
	l=lj.get("href")
	#获得下一页的部分链接
	#元素.get(属性)返回参数
	url='http://m.bxwz9.org'+l
	#组成完整url
	return url
	#返回url
	
	
def fxtext(html):
	#分析源码，获得文章内容，标题
	#返回值:注意!返回两个参数.英文逗号间隔
	soup=BeautifulSoup(html,'html.parser')
	#重点！！！
	#转换为bs型数据，添加解析器！！！
	bt=soup.find(id='chaptertitle')
	#查找id=nr_title的元素(标题)
	nr=soup.find(id='novelcontent')
	#查找id=nr1的元素(内容)
	a=bt.text
	#标题传入a
	b=nr.text
	#内容传入b
	return a,b
	#返回两个参数
	
def write(bt,nr,src="D:/小说.txt"):
	a=open(src,'a')
	#读写方式'a'文件不存在可自动创建，只写模式
	#只能创建文件！！不能创建文件夹！！
	#从文件末尾开始写入，不覆盖源文件。
	a.write(bt)
	#写入标题
	a.write('\n')
	#写入换行
	a.write(nr)
	#写入内容
	a.close()
	#关闭文件
	
#==========核心函数========
	
	
	
if __name__=='__main__':#main函数
	url1=input("请输入开始章节链接：\n")
	#起始url
	src=input("请输入储存位置:\n默认位置:D:/小说.txt\n")
	for i in range(1000000):
		try:
			html=rqe(url1)
			print(html)
			#获取html
			bt,nr=fxtext(html)
			print(2)
			#获取内容，标题
			write(bt,nr,src)
			#写入文件
			print('正在写入\n'+bt)
			url2=fxurl(html)
			print(3)
			print(url2)
			#获取下页的url
			url1=url2
			#将下页url传入起始url
		except AttributeError:
			break
	print('\n\n全部写入完成')
