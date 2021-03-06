# -*- encoding:utf-8 -*-
# 这个程序用于 

import urllib2
import urllib
import re
import thread
import time

class Spider_Model:

    def __init__(self):

        self.page = 1
        self.pages = []
        self.enable = False

    # 将所有的段子都添加到列表中并且返回列表
    def GetPage(self, page):

        myUrl = "http://m.qiushibaike.com/hot/page/" + page
        user_agent = "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"
        headers = {'User-Agent' : user_agent}
        req = urllib2.Request(myUrl, headers = headers)
        myResponse = urllib2.urlopen(req)
        myPage = myResponse.read()

        unicodePage = myPage.decode('utf-8')

        # 找出所有class="content"的div标记
        # re.s是任意匹配模式，也就是.可以匹配换行符
        pattern ='<div.*?class="content".*?title="(.*?)">(.*?)</div>(.*?)<div class="stats.*?class="number">.*?<i>'
        myItems = re.findall(pattern, unicodePage, re.S)

        items = []

        for item in myItems:
            # item中的第一个是div的标题，也就是时间
            # item中的第二个是div的内容，也就是内容
            # 利用第三个元素判断内部是否有图片
            if not re.search("img",item[2]):
                items.append([item[0].replace("\n", ""), item[1].replace("\n", "")])
        return items

    # 用于加载新的段子
    def LoadPage(self):
        # 如果用户未输入quit则一直运行
        while self.enable:
            # 如果pages数组中德内容小于2个
            if len(self.pages) < 2:
                try:
                    # 获取新的页面中德段子
                    myPage = self.GetPage(str(self.page))
                    self.page += 1
                    self.pages.append(myPage)
                except:
                    print u"无法连接糗事百科".encode('gbk')
            else:
                time.sleep(1)

    def ShowPage(self, nowPage, page):
        for items in nowPage:
            print u"第%d页" % page, items[0], items[1]
            myInput = raw_input()
            if myInput == "quit":
                self.enable = False
                break

    def Start(self):
        self.enable = True
        page = self.page

        print u"正在加载中请稍候……".encode('gbk')

        # 新建一个线程在后台加载段子并存储
        thread.start_new_thread(self.LoadPage, ())

        while self.enable:
            #如果self的page数组中存有元素
            if self.pages:
                nowPage = self.pages[0]
                del self.pages[0]
                self.ShowPage(nowPage, page)
                page += 1

print u"请按下回车浏览今日的糗百内容：".encode('gbk')
raw_input(" ")
myModel = Spider_Model()
myModel.Start()

