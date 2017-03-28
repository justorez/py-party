#!python3
# coding: utf-8

import json
import time
import math
import requests
from urllib.parse import urlencode

import zz_data
import utils
from zz_test import testLogin



# 根据配置文件读取用户信息
def loginInfo():
	with open('conf/user_info.json', 'r', encoding='utf-8') as fr:
		info = json.load(fr)
	return info


# 登录 ZZ
def loginZZ():
	# 开启会话
	session = requests.Session()

	login_info = loginInfo()
	if len(login_info) < 2:
		username = input('你的 ZZ 用户名：')
		password = input('你的 ZZ 密码：')
	else:
		username = login_info['username']
		password = login_info['password']

	# 先打开一次登录界面
	session.get(
		zz_data.loginUI_url,
		timeout = 23,
		headers = zz_data.common_header
	)

	# 获取并设置 DWRSESSIONID
	dwrsid = getDwrsid(session)
	if not len(dwrsid)>0:
		print('无法获取 DWRSESSIONID~一脸懵逼')
		return False,None
	utils.addCooike(session, {zz_data.dwr_session_id: dwrsid})

	# 设置验证码-请求参数（两套方案）
	try:
		autoHandleCheckCode(session)
	except:
		handleCheckcode(session)

	login_payload = zz_data.login_payload
	# 设置用户密码-请求参数
	login_payload['c0-e1'] = login_payload['c0-e1'].format(username)
	login_payload['c0-e2'] = login_payload['c0-e2'].format(password)

	# 对请求参数进行编码
	post_data = urlencode(login_payload)
	# TODO 测试点：URL 编码后登录请求参数
	# print('Request payload: \n'+post_data)

	# 开始登录
	try:
		r = session.post(
			zz_data.login_url,
			data = post_data,
			headers = zz_data.login_header
		)
		r.raise_for_status()
	except:
		print("failed to login, status: %d" % r.status_code)
		return False,None
	else:
		r.encoding = r.apparent_encoding

		# TODO 测试点：验证登录是否成功
		# print(r.text)
		# print( str(session.cookies) )

		# 登录测试失败，则直接结束修行
		if not testLogin(session):
			exit(-1)
		return True,session


# 设置验证码（人工）
def handleCheckcode(session):
	login_payload = zz_data.login_payload
	checkcode_url = zz_data.checkcode_url

	# 生成一个时间戳
	timestamp = str(math.floor(time.time() * 1000))
	try:
		r = session.get(
			checkcode_url+'?r='+timestamp,
			timeout = 30
		)
		print(utils.getCookieInSession(session))
		r.raise_for_status()
	except:
		print("failed to get Check Code, status: %d"%r.status_code)
	else:
		with open(zz_data.checkcode_path, 'wb') as fw:
			fw.write(r.content)
		checkcode = input('请到D盘根目录查看验证码并输入：')
		login_payload['c0-e3'] = login_payload['c0-e3'].format(checkcode)


# 设置验证码（自动，根据 Cookie）
def autoHandleCheckCode(session):
	login_payload = zz_data.login_payload
	checkcode_url = zz_data.checkcode_url

	# 生成一个时间戳
	timestamp = str(math.floor(time.time() * 1000))
	try:
		r = session.get(
			checkcode_url + '?r=' + timestamp,
			timeout=30
		)
		cookies = utils.getCookieInSession(session)
		r.raise_for_status()
	except:
		raise Exception
	else:
		checkCode = cookies['rand']
		login_payload['c0-e3'] = login_payload['c0-e3'].format(checkCode)


# 获取 DWRSESSIONID
def getDwrsid(session):
	try:
		r = session.post(
			zz_data.genDwrsid_url,
			data = zz_data.genDwrsid_payload,
			headers = zz_data.common_header
		)
		r.raise_for_status()
	except:
		print("failed to get DWRSESSIONID, status: %d" % r.status_code)
		return ''
	else:
		callback_msg = r.text
		head = "r.handleCallback(\"0\",\"0\",\""
		tail = "\")"
		dwrsid = utils.subStr(callback_msg, head, tail)
		if len(dwrsid)>0:
			return dwrsid
		else:
			return ''


if __name__ == '__main__':
	print( loginInfo() )
	loginZZ()

