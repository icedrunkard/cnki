# -*- coding: utf-8 -*-
import pymongo
import random
from scrapy import Request,Spider
from scrapy.http.cookies import CookieJar
from cnki.cnki_params import paramize
from bs4 import BeautifulSoup as bs
from cnki.items import CnkiItem
#from cnki.settings import COLLECTION_NAME,MONGO_DATABASE,MONGO_HOST
from cnki.settings import MONGO_HOST,SCHOOL_LIST

client=pymongo.MongoClient(MONGO_HOST)
#db=client[MONGO_DATABASE]
#col=db[COLLECTION_NAME+'_teachers']

db2=client['schools']
col2=db2['dpts_985']




#得出某学院的老师搜索链接
def tutor_url(short):
    urls=[]
    c={}
    db=client[short]
    dpts=col2.find_one({'short':short})['dpts']
    for dpt in dpts:
        col=db[dpt+'_teachers']
    
        for i in col.find({}):
            teacher=i['name']
    
            school=col2.find_one({'short':short})['university']
            #paramize返回[网址，老师名，学校名]，时间是2010-01-01之后
            url=paramize(teacher,school)
            urls.append(url)
        #{'dpt1':urls1,'dpt2':urls2}    
        c[dpt]=urls
    return c


#第二次所需访问的网址
url_brief='http://kns.cnki.net/kns/brief/brief.aspx?pagename=ASP.brief_result_aspx&dbPrefix=SCDB&dbCatalog=%e4%b8%ad%e5%9b%bd%e5%ad%a6%e6%9c%af%e6%96%87%e7%8c%ae%e7%bd%91%e7%bb%9c%e5%87%ba%e7%89%88%e6%80%bb%e5%ba%93&ConfigFile=SCDB.xml&research=off&keyValue=&S=1&recordsperpage=50'

#link_root指item各项的根地址
link_root='http://kns.cnki.net'





class MseSpider(Spider):
	name = 'sss'
	allowed_domains = ['cnki.net']

    #1st step:SearchHandler
	def start_requests(self):
            for short in SCHOOL_LIST:
                container=tutor_url(short)
                for dpt in container.keys():
                    urls=container[dpt]
                    for list_ in urls:
                        ra=random.random()
                        yield Request(list_[0],
                                      meta={'cookiejar':ra,'tutor':list_[1],'school':list_[2],'short':short,'dpt':dpt},
                                      callback=self.call,
                                      dont_filter=True)

    #request content page
	def call(self, response):
		key=response.meta['cookiejar']
		tutor=response.meta['tutor']
		school=response.meta['school']
		short=response.meta['short']
		dpt=response.meta['dpt']
		yield Request(url_brief,
                              meta={'cookiejar':key,'tutor':tutor,'school':school,'short':short,'dpt':dpt},
                              callback=self.parse,
                              dont_filter=True
                              )

	def parse(self,response):
		key=response.meta['cookiejar']
		item=CnkiItem()
		item['tutor']=tutor=response.meta['tutor']
		item['school']=school=response.meta['school']
		item['short']=short=response.meta['short']
		item['dpt']=dpt=response.meta['dpt']
		soup=bs(response.text,'lxml')
		if soup.find_all('tr',bgcolor=True):
            
			for piece in soup.find_all('tr',bgcolor=True):
				item['paper_name']=piece.find('a',class_='fz14').get_text(strip=True)
				item['paper_link']=link_root+piece.find('a',class_='fz14').attrs['href']
				item['author']=[]
				for i in piece.find('td',class_='author_flag').find_all('a'):
					k=0
					item['author'].append({'name':i.get_text(strip=True),'link':link_root+i.attrs['href']})
					#yield Request(item['author'][k]['link'],callback=self.parse_author)
                #4th 'td'
				item['publication']=piece.find_all('td')[3].get_text(strip=True)
                #<td>里面有一个<a>
				if piece.find_all('td')[3].findAll('a'):
					item['publication_link']=link_root+piece.find_all('td')[3].findAll('a')[0].attrs['href']#所以有‘.a’
				item['pub_date']=piece.find_all('td')[4].get_text(strip=True)[:10]
				item['pub_type']=piece.find_all('td')[5].get_text(strip=True)
				yield item

			if soup.find('a',text='下一页'):
				url_next='http://kns.cnki.net/kns/brief/brief.aspx'+soup.find('a',text='下一页').attrs['href']
				yield Request(url_next,
                                              meta={'cookiejar':key,'tutor':tutor,'school':school,'short':short,'dpt':dpt},
                                              callback=self.parse,
                                              dont_filter=True
                                              )
	def parse_author(self,response):
            	pass        


