from bs4 import BeautifulSoup
import readee

def getHtml(name, soup, index_loc):
	return '''
<html>
	<body>
		<title>%s</title>
		<h1>%s</h1>
		<div><a href="%s">返回目录</a></div>
		%s
		<div><br/><a href="%s">返回目录</a></div>
	</body>
</html>
	''' % (name, name, index_loc, str(soup), index_loc)

def getCustomHtml(name, content, index_loc):
	if not content:
		return
	raw = []
	for x, y in content:
		raw.append('<div>%s%s</div>' % (x, y))
	return getHtml(name, '<br/><br/>' + '<br/><hr/><br/>'.join(raw), index_loc)

def getArticleHtml(name, link_list, index_loc):
	result = ''
	for link in link_list: 
		soup = readee.export(link)
		if len(soup.text) < 100:
			continue
		result += str(soup)
	if not result:
		return
	return getHtml(name, '''
		%s
		<div><br/><a href="%s">原文</a></div>
	''' % (result, link), index_loc)