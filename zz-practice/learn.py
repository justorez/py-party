#!python3
# coding: utf-8

import utils
import zz_info
import time
import zz_data
import re


# 燥起来
def fk_zz(session, section):
	batchId = 1
	section_status = zz_info.getSectionStatus(session, section['jid'])

	last_time = int(section_status['learned_time'])
	while True:
		learned_time = int(section_status['learned_time'])
		total_time = int(section_status['total_time'])
		if section_status['status']:
			print('该章节已修行完毕：'+section['title'], end='\n\n')
			return
		else:
			if not last_time is learned_time:
				print('\r修行进度：'+section['title']+' {:.2f}%'.format(learned_time*100/total_time))
				last_time = learned_time
				batchId = batchId + 1

		# 延迟15秒（模拟学习，时间不够会出错）
		time.sleep(15)

		learn_header = zz_data.learn_header
		learn_payload = zz_data.learn_payload
		p = re.compile('jid=\d*')
		learn_header['Referer'] = re.sub(p, 'jid='+section['jid'], learn_header['Referer'])
		learn_payload['c0-e2'] = re.sub('number:\d*', 'number:'+section['jid'], learn_payload['c0-e2'])
		learn_payload['page'] = re.sub(p, 'jid=' + section['jid'], learn_payload['page'])
		learn_payload['batchId'] = batchId
		learn_payload['scriptSessionId'] = utils.genSSIdBySession(session)

		# TODO 测试点：学习请求参数
		# print( str(learn_payload) )

		r = session.post(
			url = zz_data.learn_url,
			data = learn_payload,
			headers = learn_header
		)
		r.encoding = 'UTF-8'

		# TODO 测试点：学习请求响应信息
		# print(r.text)

		if r.text.find('flag:1') is -1:
			print(section['title']+' 走火入魔啦~~~')
		else:
			print(section['title']+': 又修行了15秒！')
			section_status = zz_info.getSectionStatus(session, section['jid'])

		batchId += 1


# 修行开始
def toBeImmortal(session):
	print("您已进入修行模式~：")
	all_chapter = zz_info.getAllChapter(session)
	for chapter in all_chapter:
		print(chapter['title']+' '+'*'*100)
		sections  = chapter['sections']
		for section in sections:
			fk_zz(session, section)
	print('您已完成全部修行~！')



