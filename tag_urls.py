import requests
from pyquery import PyQuery as pq
import redis

url = "https://book.douban.com/tag/?view=type&icn=index-sorttags-all"
# 抓取信息
res = requests.get(url)
# 获取响应内容
data = res.content.decode('utf-8')
# 用pyquery进行解析
doc = pq(data)
# 连接Redis数据库
r = redis.Redis(host="localhost",port="6379",decode_responses=True)

# 获取所有含tags的a标签
alist = doc("table.tagCol td a")

for i in alist.items():
	'''
	遍历将tags放入redis数据库中
	'''
	tag = i.attr.href
	r.lpush("books:tag_urls",tag)

print("共有%d个tags"%len(alist))

