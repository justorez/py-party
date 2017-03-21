#!python3
# coding: utf-8

from login import loginZZ
from learn import toBeImmortal


# 跑起来
def run():
	flag,session = loginZZ()
	if not flag or session is None:
		print('\n服务器君抽风啦~(＞﹏＜)')
		return
	else:
		print('='*100)
		input('Please press Enter to f**k ZZ!')
		try:
			toBeImmortal(session)
		except:
			print('\n服务器君抽风啦~(＞﹏＜)')
			print('请稍后重试')


if __name__ == '__main__':
	run()
