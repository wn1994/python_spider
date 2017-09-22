# -*- coding: utf-8 -*-

import re
import urlparse
import requests
import json
from bs4 import BeautifulSoup
import MySQLdb
import time

class Spider(object):
    url = 'https://www.zhihu.com/topic/19642818/followers'

    headers_get = {
        'Host': 'www.zhihu.com',
        'Referer': 'https://www.zhihu.com',
        'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Cookie': 'q_c1=ed3fc6082a354c47be768401258d3a7b|1505624607000|1505624607000; r_cap_id="ZTA2YzU0ODAwNmVmNDgwZWFhNjRhZGY5NjAzMGEyZjQ=|1505637163|84ce76c9a25db99e63fb524d6863d746e6f45c83"; cap_id="MmNiZmVjNTA3ZGU2NGE4MTlmOGU2MzJmYWY1M2IzZDc=|1505637163|184b324450e0b4a520adb7222703e49b22950acd"; _zap=9d069655-73cb-4325-96aa-427793266dfc; aliyungf_tc=AQAAAFKP/VinXgcAzM54apzxqbqIk0DB; _xsrf=d45e1e92-4a3d-4908-a1f7-c82c2aac5dee; d_c0="ADDC7Bi4YwyPTufdhT1rK0gm79igj-VcsY4=|1505630467"; __utma=51854390.1596427626.1505630468.1505630468.1505634366.2; __utmc=51854390; __utmz=51854390.1505634366.2.2.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=51854390.100-1|2=registration_date=20140128=1^3=entry_date=20140128=1; s-q=Wind; s-i=10; sid=crepe7os; __utmb=51854390.0.10.1505634366; z_c0=Mi4xcklBeUFBQUFBQUFBTU1Mc0dMaGpEQmNBQUFCaEFsVk5PTURsV1FBUjZWT0k1RWhRZ0ZFblJWQWFsbEtkN08yc1Bn|1505637176|28454d96955c7c85bd1e8591770e9d3c5a606194'
    }

    headers_post = {
        'Host':'www.zhihu.com',
        'Referer':'https://www.zhihu.com/topic/19642818/followers',
        'Connection':'keep-alive',
        'X-Requested-With':'XMLHttpRequest',
        'Content-Type':'application/x-www-form-urlencoded',
        'Accept-Language':'en-US,en;q=0.5',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept':'*/*',
        'User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0',
        'X-Xsrftoken': 'd45e1e92-4a3d-4908-a1f7-c82c2aac5dee',
        'Cookie':'q_c1=ed3fc6082a354c47be768401258d3a7b|1505624607000|1505624607000; r_cap_id="ZTA2YzU0ODAwNmVmNDgwZWFhNjRhZGY5NjAzMGEyZjQ=|1505637163|84ce76c9a25db99e63fb524d6863d746e6f45c83"; cap_id="MmNiZmVjNTA3ZGU2NGE4MTlmOGU2MzJmYWY1M2IzZDc=|1505637163|184b324450e0b4a520adb7222703e49b22950acd"; _zap=9d069655-73cb-4325-96aa-427793266dfc; aliyungf_tc=AQAAAFKP/VinXgcAzM54apzxqbqIk0DB; _xsrf=d45e1e92-4a3d-4908-a1f7-c82c2aac5dee; d_c0="ADDC7Bi4YwyPTufdhT1rK0gm79igj-VcsY4=|1505630467"; __utma=51854390.1596427626.1505630468.1505630468.1505634366.2; __utmc=51854390; __utmz=51854390.1505634366.2.2.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=51854390.100-1|2=registration_date=20140128=1^3=entry_date=20140128=1; s-q=Wind; s-i=10; sid=crepe7os; __utmb=51854390.0.10.1505634366; z_c0=Mi4xcklBeUFBQUFBQUFBTU1Mc0dMaGpEQmNBQUFCaEFsVk5PTURsV1FBUjZWT0k1RWhRZ0ZFblJWQWFsbEtkN08yc1Bn|1505637176|28454d96955c7c85bd1e8591770e9d3c5a606194'
    }

    def get_cookies(cookies):
        cookies_dict = {}
        items = cookies.split(';')
        for item in items:
            key = item.split('=')[0].replace(' ','').replace('\n','')
            value = item.split('=')[1].replace('\n','').replace(' ','')
            cookies_dict[key] = value
        return cookies_dict

    def start_requests(self):
        # login_url = 'https://www.zhihu.com/#signin'
        self.offset = 40
        req = requests.get(self.url,headers=self.headers_get)
        self.parse(req.text)

    def parse(self, response_text):

        print '1 ok'
        soup = BeautifulSoup(response_text,'lxml')
        pages=[]
        for link in soup.find_all('a',class_='author-link'):
            pages.append(link['href'])
            #id="mi-1320560825
        next_id = re.findall(r'.*?mi-(\d+).*?',response_text,re.DOTALL)[-1]
        temp = soup.find_all('div',class_='zm-person-item')
        next_id = temp[-1]['id']
        # pages = response.css("a.zg-link.author-link::attr(href)").extract()
        # next_id = response.xpath("//div[@id='zh-topic-users-list-wrap']/div[@class='zm-person-item'][last()]/@id").extract_first('')
        if next_id:
            next_id = re.match(r'.*?(\d+)',next_id).group(1)
        for page in pages:
            user_url = urlparse.urljoin('https://www.zhihu.com', page)
            time.sleep(3)
            times = 2
            while(times != 0):
                try:
                    user_response = requests.get(user_url,headers=self.headers_get,timeout = 3)
                    self.parse_detail(user_response)
                    times = 0
                    print '2'
                except Exception:
                    times -= 1


        formdata = {
            'offset':self.offset,
            'start':str(next_id)
        }
        if len(pages) >= 20:
            while(True):
                try:
                    req = requests.post(self.url,headers=self.headers_post,data=formdata,timeout=10)
                    if req.status_code != 200:
                        print '1 error',req.status_code
                        raise Exception

                    with open('last_log','wb') as f:
                        f.write(req.text.encode('utf-8'))
                        f.write(str(self.offset))
                        f.flush()

                    self.offset += 20
                    # 正确获得json直接调用函数，然后又会回到这个函数，所以不需要while的出口
                    self.parse_json(req)
                    pass
                    pass
                except Exception,e:
                    print '1 false'
                    print e.message

    def parse_detail(self,response):
        user_url = response.url
        user_id = re.match(r'https://www.zhihu.com/people/(.*)',response.url).group(1)
        soup = BeautifulSoup(response.text,'lxml')
        user_name = soup.find(class_='ProfileHeader-name').get_text()
        user_gender = soup.find('meta',itemprop='gender')['content']
        # user_name = response.css(".ProfileHeader-name::text").extract_first('')
        # user_gender = response.xpath("//meta[@itemprop='gender']/@content").extract_first("none")
        user_answers = int(soup.find('a',href='/people/'+user_id+'/answers').span.string)
        user_asks = int(soup.find('a',href='/people/'+user_id+'/asks').span.string)
        user_articles = int(soup.find('a',href='/people/'+user_id+'/posts').span.string)
        user_columns = int(soup.find('a',href='/people/'+user_id+'/columns').span.string)
        user_thinks = int(soup.find('a',href='/people/'+user_id+'/pins').span.string)
        #js隐藏div处理办法？
        # user_collections = int(soup.find('a',href='/people/'+user_id+'/collections').span.string)
        try:
            ma = re.match(ur'.*(获得.*?(\d+).*?次赞同).*',response.text,re.DOTALL)
            user_praise = int(ma.group(2))
        except Exception:
            user_praise = 0

        tmp_list = soup.find_all('div', class_='Profile-sideColumnItemValue')
        if len(tmp_list) == 2:
            tmp_str = tmp_list[1].get_text()
            pass
        elif len(tmp_list) == 1:
            tmp_str = tmp_list[0].get_text()
            pass
        else:
            user_thanks = 0
            user_collected = 0
        if u'感谢' and u'收藏' in tmp_str:
            ma = re.match(r'.*?(\d+).*?(\d+).*?', tmp_str)
            user_thanks = int(ma.group(1))
            user_collected = int(ma.group(2))
        elif u'感谢' in tmp_str:
            ma = re.match(r'.*?(\d+).*?', tmp_str)
            user_thanks = int(ma.group(1))
            user_collected = 0
        elif u'收藏' in tmp_str:
            ma = re.match(r'(\d+).*?', tmp_str)
            user_collected = int(ma.group(1))
            user_thanks = 0

        tmp_list = soup.find_all('div',class_='NumberBoard-value')
        user_fans = int(tmp_list[1].string)
        user_concerns = int(tmp_list[0].string)
        mysql_data =(user_id,user_name,user_gender,user_answers,user_asks,user_articles,user_columns,user_thinks,user_praise,user_thanks,user_collected,user_fans,user_concerns,user_url)
        self.connect_mysql(mysql_data)
        # return mysql_data

    def parse_json(self,response):
        js = json.loads(response.text)
        html = js['msg'][1]
        self.parse(html)

    def connect_mysql(self,mysql_data):
        conn = MySQLdb.Connect('127.0.0.1','root','wn3527825','zhihuspider',charset='utf8')
        cursor = conn.cursor()
        cursor.execute('''
        replace into zhihuspider(id,name,gender,answers,asks,articles,columns,thinks,praise,thanks,collected,fans,concerns,url)
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ''',mysql_data)
        conn.commit()


if __name__=='__main__':
    Spider().start_requests()

