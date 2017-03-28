#!python3
# coding: utf-8

from bs4 import BeautifulSoup

import zz_data


def testLogin(session):
	"""
	模拟登录测试
	:param session: 
	"""
	# 测试链接（用户中心）
	test_url = zz_data.userhome_url
	try:
		r = session.get(test_url, timeout=23)
		r.raise_for_status()
	except:
		print("failed to login test, status: %d" % r.status_code)
		return False
	else:
		soup = BeautifulSoup(r.text, 'html.parser')
		print('='*100)
		# 登录成功后，访问用户中心，响应页面不会有登录字样
		if not soup.title.get_text().find('登录') is -1:
			print('登录失败！\n')
			return False
		else:
			print('登录成功！\n')
			print('修行者: '+soup.title.get_text().split('_')[0])
		print('='*100)
		return True

