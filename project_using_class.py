from flask import Flask
from flask.ext.classy import FlaskView
import MySQLdb
from bs4 import BeautifulSoup
import requests


app = Flask(__name__)


news_sites=[
	{
		'id':'timesofindia.indiatimes.com',
		'url':'/rssfeeds/1221656.cms'
	},
	{
		'id':'zeenews.india.com',
		'url':'/rss/world-news.xml'
	},
	{
		'id':'www.ndtv.com',
		'url':'http://feeds.feedburner.com/ndtvnews-latest'
	}
	
	
]


class ApiView(FlaskView):
	def index(self):
		return 'this is blank'


	def get(self,news):
                if(news==news_sites[2]['id']):               
                        url1 = news_sites[2]['url']

# i wrote this extra line above ,bcoz www.ndtv.com is redirecting to feedburner.com/ndtvnews-latest so i need to match that url with my mine in dictionry above.

                        html=requests.get(url1)
                        if(html):
                                soup = BeautifulSoup(html.content, 'html.parser')
                        	items = soup.find_all('item')
                        	conn = MySQLdb.connect(host="localhost",user="root", passwd="", db="news")
                                cursor=conn.cursor()
                                cursor.execute ('delete from news')  # to delete all entries (to enter fresh entries)
                                cursor.close()
                                conn.commit()
                                conn.close()
                        	for count in range(3):
                                	item=items[count]
                                        title=str(item.title.text).encode('utf8')
                                	date=str(item.pubdate.text).encode('utf8')
                                	description=str((item.description.text).encode("utf8"))
                                	print title
                                        print date
                			print str(description)
                        		conn = MySQLdb.connect(host="localhost",user="root", passwd="", db="news")
                                        cursor=conn.cursor()
                                        cursor.execute ('INSERT INTO news(title,date,story) VALUES(\"'+title+'\",\"'+date+'\",\"'+description+'\")')
                        		cursor.close()
                                	conn.commit()
                                conn.close()







        		
                	if(html):
                        	return "done.."
                        else:
                                return "not done.."
                #for other two sites defined above
        	for count in range(3):
                	if(news==news_sites[count]['id']):
                        	bb=count
                                url1="http://"+news+news_sites[bb]['url']
                                html=requests.get(url1)
                                if(html):
                                        soup = BeautifulSoup(html.content, 'html.parser')
                                	items = soup.find_all('item')
                                	conn = MySQLdb.connect(host="localhost",user="root", passwd="", db="news")
                                        cursor=conn.cursor()
                                	cursor.execute ('delete from news')  # to delete all entries (to enter fresh entries)
                                	cursor.close()
                                        conn.commit()
                                        conn.close()
                                	for count in range(3):
                                        	item=items[count]
                                                title=str(item.title.text).encode('utf8')
                                        	date=str(item.pubdate.text).encode('utf8')
                                        	description=str((item.description.text).encode("utf8"))
                                        	print title
                                                print date
                                		print str(description)
                                                conn = MySQLdb.connect(host="localhost",user="root", passwd="", db="news")
                                                cursor=conn.cursor()
                                                cursor.execute ('INSERT INTO news(title,date,story) VALUES(\"'+title+'\",\"'+date+'\",\"'+description+'\")')
                                		cursor.close()
                                        	conn.commit()
                                        conn.close()


        			
                		if(html):
                        		return "done.."
                                else:
                                        return "not done"
		

		
ApiView.register(app)


if __name__=='__main__':
	app.run()
