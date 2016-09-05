# coding:utf-8

import re
import os
import time
import shutil
#import MySQLdb
import urllib
import urllib2
from random import randint

# import sys            要向数据库中存储中文的话，就要改变编码
# reload(sys)
# sys.set default encoding('utf8')


class Spider:

	def __init__(self):     # init and connect ONE
		page = randint(1, 1024)

		headers = {
			'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
		req = urllib2.Request('http://wufazhuce.com/one/' + str(page), headers=headers)
		try:				#resp is the web-source-code
			self.resp = urllib2.urlopen(req).read()
		except urllib2.URLError:
			self.resp = '0'

	def word(self):			# the sentences
		result = re.findall('<div class="one-cita">(.*?)</div>', self.resp, re.S)
		return ''.join(result).replace(' ', '').replace('\t', '').replace('\n', '')

	def pic(self):			# the pictures
		result = re.findall('<div class="one-imagen">.*?<img src="(.*?)" alt="" />.*?</div>', self.resp, re.S)
		return result

	def date(self):
		day = re.findall('<p class="dom">(.*?)</p>', self.resp, re.S)
		y_m = re.findall('<p class="may">(.*?)</p>', self.resp, re.S)
		return day[0]+' '+y_m[0]    # return 'dd mm yy'

# 俩个下划线是私有属性或方法


# class Sql:

# 	# connect mysql
# 	con = MySQLdb.connect(user='root', passwd='ycj19950510', host='127.0.0.1', db='ycj')
# 	cur = con.cursor()  # get the cursor

# 	def __init__(self):
# 		pass

# 	def select(self, date):
# 		sql = "select * from one where date ='"+date+"';"
# 		try:
# 			self.cur.execute(sql)
# 			data = self.cur.fetchall()
# 			return data
# 		except MySQLdb.Error:
# 			self.con.rollback()

# 	def insert(self, date, path):
# 		try:
# 			sql = "insert into one values('"+date+"','"+path+"');"
# 			self.cur.execute(sql)
# 			self.con.commit()
# 			return 1
# 		except MySQLdb.Error:
# 			self.con.rollback()
# 			return 0

# 	def delete(self, date):
# 		sql = "delete from one where date ='"+date+"';"
# 		try:
# 			self.cur.execute(sql)
# 			self.con.commit()
# 		except MySQLdb.Error:
# 			self.con.rollback()

# 	def close(self):
# 		self.cur.close()
# 		self.con.close()


class Files:

	def __init__(self, date, word, pic):
		self.word = word
		self.pic = pic
		self.date = date

	def newdir(self):

		if os.path.exists(self.date):
			return os.getcwd()+'/'+self.date
		else:
			files = open(self.date+'.txt', 'w')   # word
			files.write(self.word)
			files.close()

			for p in self.pic:		# pic
				urllib.urlretrieve(p, self.date+'.jpg')

			os.mkdir(self.date)					# 储存到对应文件夹
			shutil.move(self.date+'.jpg', self.date+'/'+self.date+'.jpg')
			shutil.move(self.date+'.txt', self.date+'/'+self.date+'.txt')
			return os.getcwd()+'/'+self.date


def search(n):
	print '正在运行...'
	time_s = time.time()
	num = 0
#	sq = Sql()
	for i in range(n):
		one = Spider()
		if one.resp != '0':
			word = one.word()
			pic = one.pic()
			date = one.date()
			fi = Files(date, word, pic)
			path = fi.newdir()
			num += 1;'''sq.insert(date, path)'''

		else:
			print 404, '网站未找到'
#	sq.close()
	time_e = time.time()
	print '共用时：', time_e-time_s, 'sec'
	print '已下载：', num, '个，', n-num, '个已下载或网站未响应'

print "下载个数："
num = input()
search(num)