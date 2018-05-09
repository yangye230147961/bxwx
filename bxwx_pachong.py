# coding=utf-8
import time
import requests
from bs4 import BeautifulSoup


# ==========核心函数========
def rqe(url):
    # 请求页面函数，返回html
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36'}
    a = requests.get(url, headers=headers)
    # 设置UA伪装成浏览器
    a.encoding = a.apparent_encoding
    # 重点！
    # 从网页获取文本编码
    return a.text


def fxurl(html):
    # 分析源码
    # 返回:下页URL,标题,文章内容
    soup = BeautifulSoup(html, 'html.parser')
    # 重点！！！
    # 转换为bs型数据，添加解析器！！！！
    j = soup.find_all(class_="p3")
    ll = j[0]
    # 重点,查找id=pt_next的元素(下一页url)
    # .find(属性=参数)搜索单一元素
    lj = ll.find("a")
    l = lj.get("href")
    # 获得下一页的部分链接
    # 元素.get(属性)返回参数
    url = 'http://m.bxwz9.org' + l
    # 组成完整url
    return url


# 返回url


def fxtext(html):
    # 分析源码，获得文章内容，标题
    # 返回值:注意!返回两个参数.英文逗号间隔
    soup = BeautifulSoup(html, 'html.parser')
    # 重点！！！
    # 转换为bs型数据，添加解析器！！！
    bt = soup.find(id='chaptertitle')
    # 查找id=nr_title的元素(标题)
    nr = soup.find(id='novelcontent')
    # 查找id=nr1的元素(内容)
    a = bt.text
    # 标题传入a
    b = nr.text
    # 内容传入b
    return a, b


# 返回两个参数

def write(text, src='./小说.txt', m='a'):
    with open(src, m) as f:
        f.write(text)


def main(url1, src):
    while True:
        try:
            html = rqe(url1)
            # 获取html
            bt, nr = fxtext(html)
            # 获取内容，标题
            text = "%s\n%s" % (bt, nr)
            # 内容拼接
            text = text.strip()
            # 清除首位空格与换行
            text = text[:-17]
            # 截取正文，清除'下一页。。。。'
            write(text, src)
            # 写入正文
            logtext = "{'bt':'%s','src':'%s','url':'%s'}" % (bt, src, url1)
            # 生成Log,记录错误和方便下次使用
            logsrc = "./bxwx.log"
            # Log路径
            print('正在写入：\t' + bt + '\t请稍候......')
            # 生成信息
            write(logtext, logsrc, 'w+')
            # 写入Log
            time.sleep(0.5)
            print('写入完成\n\n')
            # 提示信息
            url2 = fxurl(html)
            # 获取下页的url
            url1 = url2
        # 将下页url传入起始url
        except AttributeError:
            break
    print('\n\n全部写入完成')


# ==========核心函数========

if __name__ == '__main__':
    # main函数
    while True:
        print('请输入启动模式(序号):\n1 新建模式(新建爬取内容)\n2 记忆模式(继续上次爬取)\n3 退出')
        ms = input("请输入启动模式:")
        if ms == "1":
            url = input("请输入开始章节链接：")
            # 起始url
            src = input("请输入储存位置:\n默认位置:当期目录/小说.txt\n")
            main(url, src)
        elif ms == "2":
        	try:
        		with open('./bxwx.log', 'r') as f:
                    for i in f:
                        a = eval(i)
                        print("记录:%s" % (a['bt']))
                        print('是否继续爬取？(y/n)')
                        s = input('继续输入y,返回输入n：')
                        if s == 'y':
                            main(a['url'], a['src'])
        	except FileNotFoundError:
        		print("没有记录,无法调用记忆模式,请选择新建模式")
            
        elif ms == "3":
            break
        else:
            print('输入错误')