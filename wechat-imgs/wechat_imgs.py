#!python3
# coding: utf-8

import itchat
import os

from PIL import Image
import math


# 首先登陆python版本微信itchat，生成二维码
# itchat.auto_login(enableCmdQR=True)
itchat.auto_login()

# 获取好友列表
friends = itchat.get_friends(update=True)[0:]

# 以自己的用户名加密码创建文件夹来存储图片
user = friends[0]["UserName"]
print("User Code: "+user)
os.mkdir(user)

# 使用itchat的get_head_img(userName=none)函数
# 爬取好友列表的头像,并下载到本地
num = 0
for i in friends:
	img = itchat.get_head_img(userName=i["UserName"])
	with open(user + "/" + str(num) + ".jpg", 'wb') as fileImage:
		fileImage.write(img)
	num += 1

# 计算好友数量
pics = os.listdir(user)
numPic = len(pics)
print("好友总数："+str(numPic))

# 计算每张头像缩小后的边长(默认为正方形)
eachsize = int(math.sqrt(float(640 * 640) / numPic))
# print(eachsize)

# 计算合成图片每一边分为多少小边
numline = int(640 / eachsize)
toImage = Image.new('RGBA', (640, 640))
# print(numline)

# 缩小并拼接图片
x, y = 0, 0
for i in pics:
	try:
		# 打开图片
		img = Image.open(user + "/" + i)
	except IOError:
		print("Error: 没有找到文件或读取文件失败")
	else:
		# 缩小图片
		img = img.resize((eachsize, eachsize), Image.ANTIALIAS)
		# 拼接图片
		toImage.paste(img, (x * eachsize, y * eachsize))
		x += 1
		if x == numline:
			x = 0
			y += 1

# 保存拼接好的图片
# 通过文件助手发送给自己
toImage.save("funny.jpg")
itchat.send_image("funny.jpg", 'filehelper')
print("好友头像拼接完毕，快去查看吧~")


