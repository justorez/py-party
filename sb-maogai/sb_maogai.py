#!python3
# coding:utf-8

content = ''

def loadContent():
	global content
	with open('questions.txt','r',encoding='utf-8') as fr:
		for line in fr.readlines():
			content = content + line

def search(key):
	start = content.find(key)
	end = content[start:].find('习题') - 1
	print('\n'+content[start:start+end], end='\n')


if __name__ == '__main__':
	loadContent()
	while True:
		key = input('请输入SB-毛概的题目：')
		if key=='fuck off':
			exit()
		search(key)

	