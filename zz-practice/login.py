#!python3
# coding: utf-8

import requests
import time
import math
from urllib.parse import urlencode
import zz_data
from zz_test import testLogin
import utils


def loginZZ():
	loginUI_url = zz_data.loginUI_url
	login_url = zz_data.login_url
	login_payload = zz_data.login_payload
	login_header = zz_data.login_header

	# 开启会话
	session = requests.Session()

	username = input('你的 ZZ 用户名：')
	password = input('你的 ZZ 密码：')

	# 先打开一次登录界面
	session.get(
		loginUI_url,
		timeout=23,
		headers=zz_data.common_header
	)

	# 获取并设置 DWRSESSIONID
	dwrsid = getDwrsid(session)
	if not len(dwrsid)>0:
		print('无法获取 DWRSESSIONID~一脸懵逼')
		return False,None
	utils.addCooike(session, {zz_data.dwr_session_id: dwrsid})

	# 设置验证码-请求参数
	handleCheckcode(session)
	# 设置用户密码-请求参数
	login_payload['c0-e1'] = login_payload['c0-e1'] + str(username)
	login_payload['c0-e2'] = login_payload['c0-e2'] + str(password)

	# 对请求参数进行编码
	post_data = urlencode(login_payload)
	# TODO 测试点：URL 编码后登录请求参数
	# print('Request payload: \n'+post_data)

	# 开始登录
	try:
		r = session.post(
			login_url,
			data=post_data,
			headers=login_header
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

		testLogin(session)
		return True,session


# 设置验证码
def handleCheckcode(session):
	login_payload = zz_data.login_payload
	checkcode_url = zz_data.checkcode_url
	checkcode_path = zz_data.checkcode_path

	timestamp = str(math.floor(time.time() * 1000))
	try:
		r = session.get(
			checkcode_url+'?r='+timestamp,
			timeout=30
		)
		r.raise_for_status()
	except:
		print("failed to get Check Code, status: %d"%r.status_code)
	else:
		with open(checkcode_path, 'wb') as fw:
			fw.write(r.content)
		checkcode = input('请到D盘根目录查看验证码并输入：')
		login_payload['c0-e3'] = login_payload['c0-e3'] + str(checkcode)


# 获取 DWRSESSIONID
def getDwrsid(session):
	genDwrsid_url = zz_data.genDwrsid_url
	genDwrsid_payload = zz_data.genDwrsid_payload
	common_header = zz_data.common_header

	try:
		r = session.post(
			genDwrsid_url,
			data=genDwrsid_payload,
			headers=common_header
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
	loginZZ()

