from django.shortcuts import render
from tieba import models
import requests
from lxml import etree
import urllib
import random
import os
import pymysql
from .send_email import *
import time,datetime

def search(request):
	clean_database()
	if request.method == "POST":
		people = request.POST.get("pn", None)
		print(people)
		contentlist = request.POST.get("search", None)#获取关键字
		content = contentlist.split()
		for each in content:
			content = each.encode('utf8')
			content = urllib.parse.quote(content)
			try:
				url = 'http://tieba.baidu.com/f?fr=wwwt&kw=' + str(content)
				res = requests.get(url=url)
				root = etree.HTML(res.text)
				baming = root.xpath('//div[@class="card_title"]/a/text()')
				baming = baming[0]
				baming = baming.strip()
				guanzhuliang = root.xpath('//span[@class="card_menNum"]/text()')
				guanzhuliang = guanzhuliang[0]
				guanzhuliang= str(guanzhuliang).replace(',', '')
				guanzhuliang = int(guanzhuliang)
				fatieshu = root.xpath('//span[@class="card_infoNum"]/text()')
				fatieshu = fatieshu[0]
				fatieshu = str(fatieshu).replace(',', '')
				fatieshu = int(fatieshu)
				twz = models.subscription.objects.create(baming=forum,guanzhuliang=title,fatieshu=content)  # 需要修改--已修改
				twz.save()
			except IndexError:
				pass

		curdate = time.strftime('%Y%m%d', time.localtime(time.time()))
		filepath = 'C:/bychannel{}.xlsx'.format(curdate)
		get_execl(filepath)
		if len(people) > 0:
			sendmail(people,filepath)

	return render(request,'tieba/search.html')

#定义展示函数
def list(request):
	list = models.subscription.objects.all()
	return render(request, 'tieba/show.html', {"list":list})