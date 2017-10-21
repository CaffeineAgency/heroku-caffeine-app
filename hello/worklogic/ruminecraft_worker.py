import bs4 as bs
from bs4 import Comment
import base64
from hello.worklogic.models.rumine_models import Post, Response
import jsonpickle
import requests

def check_for_input(request):
	if not "threadId" in request:
		raise Exception("No threadId passed")
	thread = request["threadId"]
	if not "pagenum" in request:
		pagenum = 9999999999999
	else:
		pagenum = request["pagenum"]
	return "https://ru-minecraft.ru/forum/showtopic-{}/page-{}/".format(thread, pagenum)


def sanitize_html(soup):
	[itm.nextSibling.extract() for itm in soup.findAll("div", class_="clr")]
	[likr.extract() for likr in soup.findAll("div", class_="EditMsgView")]
	[comment.extract() for comment in soup.findAll(text=lambda text: isinstance(text, Comment))]
	return soup


def parse_data(soup, tb64):
	[spmark.extract() for spmark in soup.findAll("div", class_="title_spoiler")]
	for spler in soup.findAll("div", class_="text_spoiler"):
		del(spler['style'])
	posts = []
	for item in soup.find_all('li', class_="msg"):
		pid = item.select_one(".msgInfo a").text.replace("#", "")
		sender = item.select_one(".msgAutorInfo .autorInfo p > a").text
		stri = item.select_one(".msgText td > div").encode('utf-8')
		posts.append(Post(pid, sender, (stri, base64.b64encode(stri))[tb64]))
	return Response(posts)


def getComments(request):
	try:
		url = check_for_input(request)
		source = requests.get(url).raw
		soup = bs.BeautifulSoup(source, "html5lib")
		soup = sanitize_html(soup)
		return jsonpickle.encode(parse_data(soup, request["b64"]), unpicklable=False)
	except Exception as ex:
		return jsonpickle.encode(ex, unpicklable=False)

