from bs4 import BeautifulSoup
from flask import Flask
import requests
import MySQLdb



app=Flask(__name__)


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

@app.route('/api/<string:news>', methods=['GET'])
def main(news):
	if(news==news_sites[2]['id']):
		url1 = news_sites[2]['url']
		res = retrieve(url1)
		if(res):
			return "done.."
		else:
			return "not done.."
	#for other two sites defined above
	for count in range(3):
		if(news==news_sites[count]['id']):
			bb=count
			url1="http://"+news+news_sites[bb]['url']
			res = retrieve(url1)
			if(res):
				return "done.."
			else:
				return "not done"
		
		
	


def retrieve(url):
	html=requests.get(url)
	if(html):
		soup = BeautifulSoup(html.content, 'html.parser')
		items = soup.find_all('item')
		conn = MySQLdb.connect(host="localhost",user="root", passwd="", db="news")
		cursor=conn.cursor()
		cursor.execute ('delete from news')
		cursor.close()
		conn.commit()  # to delete all entries (to enter fresh entries)
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
			#cursor.execute(ins)
			cursor.close()
			conn.commit()
		conn.close()
		return True



	
	

if __name__=='__main__':
	app.run()

