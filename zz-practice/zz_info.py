#!python3
# coding: utf-8

import zz_data
from bs4 import BeautifulSoup
from login import loginZZ
import utils
import re


# 取出所有的章节信息
def getAllChapter(session):
	# 全部章节信息
	all_chapter = []

	r = session.get(
		zz_data.chapter_url,
		timeout = 23,
		headers = zz_data.common_header
	)
	r.encoding = 'UTF-8'
	soup = BeautifulSoup(r.text, 'html.parser')
	chapter_titles = soup.select('dt[name="zj"]')
	chapters = soup.select('dd[id^="zj_"]')

	for i in range(0, len(chapters)):
		# 设置章信息
		c = dict()
		c['cid'] = chapters[i].attrs['id'].replace('zj_', '')
		c_title = chapter_titles[i].find_all('span')
		c['cnum'] = c_title[0].string
		c['title'] = c_title[1].attrs['title']

		# 设置章节信息
		sections = []
		sinfos = chapters[i].select('li')
		for sinfo in sinfos:
			section = dict()
			sinfo1 = sinfo.attrs
			sinfo2 = sinfo.a.attrs
			section['jid'] = sinfo1['id'].replace('j_', '')
			section['title'] = sinfo2['title']
			section['url'] = sinfo2['href'].replace('&amp;', '&')
			sections.append(section)

		c['sections'] = sections
		all_chapter.append(c)

	# TODO 测试点：课程全部章节数和封装的全部的课程章节信息
	# print(len(all_chapter))
	# print(all_chapter)

	return all_chapter

# 未知作用
# def getTopNum(session, sectionId):
# 	topnum_header = zz_data.topnum_header
# 	topnum_payload = zz_data.topnum_payload
# 	topnum_header['Referer'] += sectionId
# 	topnum_payload['page'] += sectionId
# 	scriptSessionId = utils.genSSIdBySession(session)
# 	topnum_payload['scriptSessionId'] = scriptSessionId
#
# 	r = session.post(
# 		zz_data.topnum_url,
# 		data = topnum_payload,
# 		headers = topnum_header
# 	)
# 	r.encoding = 'UTF-8'
# 	print(r.text)


# 根据 sectionId 获取章节的状态：时间完成情况等
def getSectionStatus(session, sectionId):
	status_header = zz_data.status_header
	status_payload = zz_data.status_payload

	p = re.compile(r'jid=\d*')
	status_header['Referer'] = re.sub(p, 'jid='+sectionId, status_header['Referer'])
	status_payload['c0-e1'] = re.sub(p, 'jid='+sectionId, status_payload['c0-e1'])
	status_payload['page'] = re.sub(p, 'jid='+sectionId, status_payload['page'])
	status_payload['scriptSessionId'] = utils.genSSIdBySession(session)

	# TODO 测试点：章节状态请求参数
	# print( str(status_payload) )

	r = session.post(
		zz_data.status_url,
		data = status_payload,
		headers = status_header
	)
	r.encoding = 'unicode-escape' # 指定编码方式为 Unicode

	# TODO 测试点：章节状态响应信息
	# print(r.text)

	section_status = dict()
	if not r.text.find('已学时间') is -1:
		section_status['status'] = False
		soup = BeautifulSoup(r.text, 'html.parser')
		# 此处仅提取学习时间信息
		section_status['learned_time'] = soup.select('span[title="已学时间"]')[0].string
		section_status['total_time'] = soup.select('span[title="总学习时间"]')[0].string.replace(' 分钟','')
	else:
		section_status['status'] = True
		section_status['learned_time'] = '233'
		section_status['total_time'] =  '233'

	# TODO 测试点：封装的章节信息
	# print(section_status)

	return section_status


if __name__ == '__main__':
	flag,session = loginZZ()

	getSectionStatus(session, '1080')
	getSectionStatus(session, '1069')


