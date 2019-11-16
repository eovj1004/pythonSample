import logging
import requests
from bs4 import BeautifulSoup
from django.shortcuts import render


logger = logging.getLogger(__name__)

def getYahooNews(request):
	"""
	yahooからnews listをscraping

	@param request: Request Object
	@return: yahoo news list 画面
	"""
	logger.debug('Call scraping:getYahooNews')

	# scraping data
	newsList = []

	try:
		# yahoo japan siteにアクセスする
		resp = requests.get('https://www.yahoo.co.jp/')
		soup = BeautifulSoup(resp.text, 'html.parser')
		linkList = soup.find_all('a')
		for link in linkList:
			newsData = {}
			if link.get('href').find('news.yahoo.co.jp/pickup/') > 0:
				href = link.get('href')

				newsData['text'] = link.text
				newsData['newsIdx'] = href[href.rindex('/')+1:]
				newsList.append(newsData)
		
		context = {}
		context['newsList'] = newsList
		context['idx_top'] = len(newsList)

		return render(request, "scraping/list.html", context)
	except Exception as e:
		strErr = "scraping:getNewsContent::::: scrapingerror"
		logger.error(strErr + e)
		raise  Exception(strErr)


def getNewsContent(request):
	"""
	yahooから記事の内容をscraping

	@param request: Request Object
	@return: yahoo news content 画面
	"""
	logger.debug('Call scraping:getNewsContent')

	if request.method == 'POST':
		strErr = 'scraping:getNewsContent::::: request type error'
		logger.error(strErr)
		raise Exception(strErr)
	elif request.method == 'GET':
		newsIdx = request.GET['newsIdx']
		title = request.GET['title']
		if not newsIdx:
			strErr = 'scraping:getNewsContent::::: index not found error'
			logger.error(strErr)
			raise Exception(strErr)

		try:
			# yahoo japan 記事を読み込む
			resp = requests.get('https://news.yahoo.co.jp/pickup/{}'.format(newsIdx))
			soup = BeautifulSoup(resp.text, 'html.parser')

			content = soup.select('.tpcDetail')
			context = {}
			context['content'] = content[0].decode_contents(formatter="html")
			context['title'] = title
			return render(request, "scraping/view.html", context)
		except Exception as e:
			strErr = "scraping:getNewsContent::::: scrapingerror"
			logger.error(strErr + e)
			raise  Exception(strErr)


def getDetailContent(request):
	"""
	yahooから記事の内容をscraping

	@param request: Request Object
	@return: yahoo news 詳細画面
	"""
	logger.debug('Call scraping:getDetailContent')
	if request.method == 'POST':
		strErr = 'scraping:getNewsContent::::: request type error'
		logger.error(strErr)
		raise Exception(strErr)
	elif request.method == 'GET':
		url = request.GET['url']
		
		try:
			# yahoo japan 記事を読み込む
			resp = requests.get(url)
			soup = BeautifulSoup(resp.text, 'html.parser')

			content = soup.select('#ym_newsarticle')
			context = {}
			print(content[0].decode_contents(formatter="html"))
			context['content'] = content[0].decode_contents(formatter="html")
			context['title'] = ''
			return render(request, "scraping/view.html", context)
		except Exception as e:
			strErr = "scraping:getNewsContent::::: scrapingerror"
			logger.error(strErr + e)
			raise  Exception(strErr)