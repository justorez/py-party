#!python3
# coding: utf-8


# 首页地址
index_url = 'http://www.attop.com/index.htm'

# 用户中心地址
userhome_url = 'http://www.attop.com/user/index.htm'

# 成绩信息列表地址
score_url = 'http://www.attop.com/wk/score.htm?id=42'

# 章节信息地址
chapter_url = 'http://www.attop.com/wk/learn.htm?id=42'



# 登录界面地址
loginUI_url = 'http://www.attop.com/login_pop.htm'
# 登录请求地址
login_url = 'http://www.attop.com/js/ajax/call/plaincall/zsClass.coreAjax.dwr'
# 登录请求参数
login_payload = {
	'callCount': 1,
	'windowName': '',
	'c0-scriptName': 'zsClass',
	'c0-methodName': 'coreAjax',
	'c0-id': 0,
	'c0-e1': 'string:',  # 用户名
	'c0-e2': 'string:',  # 密码
	'c0-e3': 'string:',  # 验证码
	'c0-param0': 'string:loginWeb',
	'c0-e4': 'number:2',
	'c0-param1': 'Object_Object:{username:reference:c0-e1, password:reference:c0-e2, rand:reference:c0-e3, autoflag:reference:c0-e4}',
	'c0-param2': 'string:doLogin',
	'batchId': 1,
	'instanceId': 0,
	'page': '/login_pop.htm',
	'scriptSessionId': ''
}
# 登录请求消息头
login_header = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
	'Referer': 'http://www.attop.com/login_pop.htm'
}

# 验证码地址
checkcode_url = 'http://www.attop.com/image.jpg'
# 验证码本地保存路径
checkcode_path = 'D:/code.jpg'

# DWRSESSIONID 字符串
dwr_session_id = 'DWRSESSIONID'
# 生成 DWRSESSIONID 请求地址
genDwrsid_url = 'http://www.attop.com/js/ajax/call/plaincall/__System.generateId.dwr'
# 生成 DWRSESSIONID 请求参数
genDwrsid_payload = {
	'callCount': 1,
	'windowName': '',
	'c0-scriptName': '__System',
	'c0-methodName': 'generateId',
	'c0-id': 0,
	'batchId': 0,
	'instanceId': 0,
	'page': '/index.htm',
	'scriptSessionId': ''
}



# 作用未知
topnum_url = 'http://www.attop.com/js/ajax/call/plaincall/zsClass.commonAjax.dwr'
topnum_payload = {
	'callCount':'1',
	'windowName': '',
	'c0-scriptName': 'zsClass',
	'c0-methodName': 'commonAjax',
	'c0-id': '0',
	'c0-param0': 'string:getTopDhNum',
	'c0-param1': 'Object_Object:{}',
	'c0-param2': 'string:doGetTopDhNum',
	'batchId': '1',
	'instanceId': '0',
	'page': '/wk/learn.htm?id=42&jid=',
	'scriptSessionId': ''
}
topnum_header = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
	'Referer': 'http://www.attop.com/wk/learn.htm?id=42&jid='
}


# 章节学习状态地址（需要设置章节序号）
status_url = 'http://www.attop.com/js/ajax/call/plaincall/zsClass.commonAjax.dwr'
# 章节状态信息请求参数
status_payload = {
	'callCount': 1,
	'windowName': '',
	'c0-scriptName': 'zsClass',
	'c0-methodName': 'commonAjax',
	'c0-id': 0,
	'c0-param0': 'string:getAjaxList2',
	'c0-e1': 'string:id=42&jid=',
	'c0-e2': 'string:learn_1.htm',
	'c0-e3': 'number:1',
	'c0-e4': 'string:showajaxinfo2',
	'c0-param1': 'Object_Object:{param:reference:c0-e1, pagename:reference:c0-e2, currentpage:reference:c0-e3, id:reference:c0-e4}',
	'c0-param2': 'string:doShowAjaxList2',
	'batchId': 4,
	'instanceId': 0,
	'page': '/wk/learn.htm?id=42&jid=',
	'scriptSessionId': ''
}
# 章节状态信息请求头信息
status_header = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
	'Referer': 'http://www.attop.com/wk/learn.htm?id=42&jid='
}



# 关于学习请求地址
learn_url = 'http://www.attop.com/js/ajax/call/plaincall/zsClass.commonAjax.dwr'
# 学习ing 请求参数
learn_payload = {
	'callCount': 1,
	'windowName': '',
	'c0-scriptName': 'zsClass',
	'c0-methodName': 'commonAjax',
	'c0-id': 0,
	'c0-param0':'string:getWkOnlineNum',
	'c0-e1': 'number:42',                 # CourseID
	'c0-e2': 'number:',               # 需要设置 jid
	'c0-param1': 'Object_Object:{bid:reference:c0-e1, jid:reference:c0-e2}',
	'c0-param2': 'string:doGetWkOnlineNum',
	'batchId': 1,
	'instanceId': 0,
	'page': '/wk/learn.htm?id=42&jid=',
	'scriptSessionId':''
}
# 关于学习请求消息头
learn_header = {
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
	'Referer': 'http://www.attop.com/wk/learn.htm?id=42&jid='
}


# 通用请求消息头（模拟浏览器）
common_header = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
}


