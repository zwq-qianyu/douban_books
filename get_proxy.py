import requests,redis,time

r = redis.Redis(host="localhost", port="6379", decode_responses=True)
get_url = 'http://tvp.daxiangdaili.com/ip/?tid=558112377486448&num=20&filter=on'

while 1:
    while 1:
        lists = None
        print('get_proxy循环中...')
        try:
            res = requests.get(get_url)
            content = res.content.decode('utf-8')
            lists = content.strip().split('\r\n')
            break
        except Exception as err:
            print(err)

    if lists:
        for i in lists:
            print(i)
    #       r.lpush('proxy', i)
            
            proxies = {
                'http': 'http://' + i,
                'https': 'https://' + i,
            }
            try:
                url = 'http://book.douban.com'
                response = requests.get(url, proxies=proxies)
                r.lpush('proxy', i)
                print('ip可用！')
            except Exception as err:
                print('ip不可用！')
                print(err)
            
    time.sleep(30)
