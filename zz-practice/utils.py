#!python3
# coding: utf-8

import random
import math
import time
import requests


def __tokenify(number):
	"""
	生成随机验证字符串
	:param number: 
	:return: 随机验证字符串
	"""
	token_buf = []
	# char map 共64个字符
	char_map = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ*$'
	remainder = number
	while remainder>0:
		token_buf.append(char_map[remainder&0x3F])
		remainder = remainder // 64
	return ''.join(token_buf)


def __genSSId(DWRSESSIONID):
	"""
	生成 scriptSessionId
	:param DWRSESSIONID:
	:return: scriptSessionId
	"""
	token1 = __tokenify(math.floor(time.time()*1000))
	token2 = __tokenify(math.floor(random.random()*1E16))
	page_id = token1 + '-' + token2
	# page_id = genRandStr(7) + '-' + genRandStr(9)
	return DWRSESSIONID + '/' + page_id


# 生成指定长度的随机字符串
def genRandStr(num):
	rand_str = ''
	char_map = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ*$'
	for i in range(0, num):
		rand_str = rand_str + char_map[ random.randint(0, 63) ]
	return rand_str


# 根据 session cookie 中的 DWRSESSIONID 生成 scriptSessionId
def genSSIdBySession(session):
	cookies = requests.utils.dict_from_cookiejar(session.cookies)
	dsid = cookies['DWRSESSIONID']
	if not dsid is None:
		return __genSSId(dsid)
	else:
		return ''


# 根据源字符串的头尾，提取中间部分（或直接写正则实现该功能）
def subStr(s, head, tail):
	i = s.find(head)
	j = s.find(tail)
	if i==-1 or j==-1:
		return ''
	else:
		return s[i+len(head):j]

# 取出 session 中的 cookie，返回字典格式数据
def getCookieInSession(session):
	cookies = requests.utils.dict_from_cookiejar(session.cookies)
	return cookies

# 向 session 中添加新的 cookie（字典格式）
def addCooike(session, new_cookie):
	cookies = getCookieInSession(session)
	for k,v in new_cookie.items():
		cookies[k] = v
	cookiejar = requests.utils.cookiejar_from_dict(cookies)
	session.cookies = cookiejar


if __name__ == '__main__':
	print(genRandStr(7))
	print(genRandStr(9))

	print(__genSSId('3LHsU0$82nWNQH$ettx6nadYRGl'))

	print( subStr('abcd(123)dc', 'cd(', ')dc') )
