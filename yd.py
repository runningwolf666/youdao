#!/usr/bin/env python3
#-*- coding:utf-8 -*-
请在Python3下运行此程序='Please run this program with Python3'


# from pyquery import PyQuery as pq
import sys
import requests  # Request快速上手： http://cn.python-requests.org/zh_CN/latest/user/quickstart.html 本页内容为如何入门Requests提供了很好的指引。

'''
版本：1.1，请求方式：get，编码方式：utf-8
主要功能：中英互译，同时获得有道翻译结果和有道词典结果（可能没有）
参数说明：
　type - 返回结果的类型，固定为data
　doctype - 返回结果的数据格式，xml或json或jsonp
　version - 版本，当前最新版本为1.1
　q - 要翻译的文本，必须是UTF-8编码，字符长度不能超过200个字符，需要进行urlencode编码
　only - 可选参数，dict表示只获取词典数据，translate表示只获取翻译数据，默认为都获取
　注： 词典结果只支持中英互译，翻译结果支持英日韩法俄西到中文的翻译以及中文到英语的翻译
errorCode：
　0 - 正常
　20 - 要翻译的文本过长
　30 - 无法进行有效的翻译
　40 - 不支持的语言类型
　50 - 无效的key
　60 - 无词典结果，仅在获取词典结果生效
'''


def parseYoudao(url):
	'''
	IN: <class 'str'>url
	OUT: None
	'''

	headers = {
		'Host': 'fanyi.youdao.com',
		'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:33.0) Gecko/20100101 Firefox/33.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Language': 'en-US,en;q=0.5',
		'Accept-Encoding': 'gzip, deflate'
	}
	errorCodedict = {
		0: '正常',
		20 :'要翻译的文本过长',
		30 :'无法进行有效的翻译',
		40: '不支持的语言类型',
		50 :'无效的key',
		60 :'无词典结果，仅在获取词典结果生效'
	}

	try:
		page = requests.get(url, headers=headers)
		content = page.content.decode('utf8')
		# print(content)
		content = eval(content)

		# processing data
		# errorCode
		errorCode = content['errorCode']
		if errorCode != 0:
			print(errorCodedict[errorCode])
			sys.exit()

		if 'translation' in content:
			for item in content['translation']:
				print(item, end='  ')
		print()

		# "basic":{
		# "us-phonetic":"host",
		# "phonetic":"həʊst",
		# "uk-phonetic":"həʊst",
		# "explains":[
		# 	"n. [计] 主机；主人；主持人；许多",
		# 	"vt. 主持；当主人招待",
		# 	"vi. 群集；做主人"
		# 	]
		# }
		if 'basic' in content:
			if 'us-phonetic' in content['basic']:
				print('美式发音: ', content['basic']['us-phonetic'])
			if 'explains' in content['basic']:
				print('基本词典: ', end='')
				for item in content['basic']['explains']:
					print(item, end='\n\t  ')
		print()

		# "web":[
		# 	{"value":["宿主","主机","主持人"],"key":"host"},
		# 	{"value":["主机","主计算机","上位机"],"key":"host computer"},
		# 	{"value":["寄宿家庭","接待家庭","房东"],"key":"host family"}
		# ]
		if 'web' in content:
			print('网络释义: ', end='')
			for item in content['web']:
				print(item['key']+': ', end=' ')
				for item2 in item['value']:
					print(item2, end=' ')
				print(end='\n\t  ')
		print()


	# requests.exceptions.ConnectionError: HTTPSConnectionPool(host='pypi.python.org', port=443): Max retries exceeded with url: /pypi/pybencoder/1.0 (Caused by <class 'ConnectionResetError'>: [Errno 104] Connection reset by peer)
	# 经常出现的Connection reset by peer: 原因可能是多方面的，不过更常见的原因是：①：服务器的并发连接数超过了其承载量，服务器会将其中一些连接Down掉；②：客户关掉了浏览器，而服务器还在给客户端发送数据；③：浏览器端按了Stop
	except requests.exceptions.ConnectionError as e:
		print('ERROR ---> {}'.format(e))
	except Exception as e:
		print('ERROR ---> {}'.format(e))



url = 'http://fanyi.youdao.com/openapi.do?keyfrom=bbbb666bbbb&key=1846765962&type=data&doctype=json&version=1.1&q='

if __name__ == '__main__':
	if sys.argv[1] == '-':
		parseYoudao(url + ' '.join(sys.argv[2:]))
	else:
		for item in sys.argv[1:]:
			parseYoudao(url+item)




