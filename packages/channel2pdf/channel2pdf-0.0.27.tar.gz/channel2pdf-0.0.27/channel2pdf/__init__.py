#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'channel2pdf'

import os
from .find_resource import findResource
from .article import getArticleHtml, getCustomHtml
from .index import getIndexHtml
from datetime import date
from telegram_util import cleanFileName
from .gen_index import genIndex

if os.name == 'posix':
	ebook_convert_app = '/Applications/calibre.app/Contents/MacOS/ebook-convert'
else:
	ebook_convert_app = 'ebook-convert'

def gen(source, ebook_convert_app=ebook_convert_app, additional_setting='', filename_suffix = ''):
	name, links, pics, texts = findResource(source)
	filename = '%s_%s' % (date.today().strftime("%m%d"), name) + filename_suffix
	filename = filename.replace(' ', '_')

	os.system('rm -rf html_result')	
	os.system('mkdir html_result > /dev/null 2>&1')

	links['图集精选'] = '图集精选'
	links['消息精选'] = '消息精选'
	for link, title in links.copy().items():
		if title == '图集精选':
			html = getCustomHtml(title, pics, filename + '.html')
		elif title == '消息精选':
			html = getCustomHtml(title, texts, filename + '.html')
		else:
			html = getArticleHtml(title, link, filename + '.html')
		if title and html:
			with open('html_result/%s.html' % cleanFileName(title), 'w') as f:
				f.write(html)
		else:
			del links[link]

	index_html_name = 'html_result/%s.html' % filename
	with open(index_html_name, 'w') as f:
		f.write(getIndexHtml(name, source, links))

	os.system('mkdir pdf_result > /dev/null 2>&1')
	pdf_name = 'pdf_result/%s.pdf' % filename
	os.system('%s %s %s %s > /dev/null 2>&1' % \
		(ebook_convert_app, index_html_name, pdf_name, additional_setting))
	return pdf_name
		

