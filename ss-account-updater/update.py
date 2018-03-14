#!python3
#encoding: utf-8

import requests
from bs4 import BeautifulSoup
import json
import re
import base64
import os
import uuid
import time

# 网站一：HTML数据
URL_1 = 'https://global.ishadowx.net'
# 网站二：二维码数据
URL_2 = 'https://en.ss8.fun/images/server0{0}.png'
HEADERS_1 = {
    'Host': 'global.ishadowx.net',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'
}

# 解析二维码的API
QR_URL = 'http://jiema.wwei.cn/url-jiema.html'
HEADERS_QR = {
    'Host': 'jiema.wwei.cn',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'
}

# 本地SS配置文件路径
ss_cnf = ''

# 获取页面内容
def get_html():
    try:
        r = requests.get(URL_1, headers=HEADERS_1)
        r.raise_for_status()
    except Exception as e:
        print(URL_1+' 更新失败 - '+str(e))
        raise e
    else:
        r.encoding = 'utf8'
        return r.text

def get_ss_url():
    ss_urls = []
    for i in range(3):
        post_data = {
            # token其实无所谓，这里是40位随机
            'token': str(uuid.uuid1()).replace('-','')[:30]+str(int(time.time())),
            'jiema_url': URL_2.format(i+1)
        }
        try:
            r = requests.post(
                url=QR_URL, 
                data=post_data,
                headers=HEADERS_QR
            )
            r.raise_for_status()
        except Exception as e:
            print(URL_2+' 更新失败 - '+str(e))
            raise e
        else:
            ss_urls.append(r.json()['data'])
    return ss_urls

# 提取更新目标的最新SS配置
def extract_ss(html, ss_urls=[]):
    html = BeautifulSoup(html, 'html.parser')
    servers = []
    # 提取美国节点
    for node in html.select('.us'):
        s = ext_f(node.get_text())
        servers.append(s)
    # 提取日本节点
    for node in html.select('.jp'):
        s = ext_f(node.get_text())
        servers.append(s)
    # 提取新加坡节点
    for node in html.select('.sg'):
        s = ext_f(node.get_text())
        servers.append(s)
    # 更新网站二的节点
    for ss_url in ss_urls:
        s = ext_ss_url(ss_url)
        servers.append(s)
    return servers

# SS地址解析提取账号信息
def ext_ss_url(ss_url):
    try:
        ss_url = ss_url.split('//')[1]
        # example: 'aes-256-cfb:21234016@sga.ss8.site:16909'
        info_str = base64.b64decode(ss_url).decode().strip()
        server_info = info_str.split('@')[1].split(':')
        passwd_info = info_str.split('@')[0].split(':')
        server = server_info[0]
        server_port = server_info[1]
        password = passwd_info[1]
        method = passwd_info[0]
    except Exception as e:
        server = ""
        server_port = ""
        password = ""
        method = ""
    return {
        'server'     :server,
        'server_port':server_port,
        'password'   :password,
        'method'     :method
    }

# 提取节点账号信息
def ext_f(text):
    info = text.strip().replace(' ','')[:-17]
    try:
        server = re_f('IPAddress', info)  # IP地址
    except Exception as e:
        server = ""
    try:
        server_port = re_f('Port', info)  # 端口
    except Exception as e:
        server_port = "1234" # 默认端口(无效)
    try:
        password = re_f('Password', info) # 密码
    except Exception as e:
        password = ""
    try:
        method = re_f('Method', info)     # 加密方式
    except Exception as e:
        method = "aes-256-cfb" # 默认加密方式
    return {
        'server'     :server,
        'server_port':server_port,
        'password'   :password,
        'method'     :method
    }

# 根据关键字提取字符串内容
def re_f(keyword, str):
    pattern = keyword+':(.+?)\\n'
    value = re.findall(pattern, str)
    return value[0].strip()

# 更新本地SSR配置文件
def update_ss(latest):
    with open(ss_cnf,'r',encoding='utf8') as fr:
        cnf = json.load(fr)
    accounts = cnf['configs']
    n,old = 0,''
    for node in latest:
        # 抓的数据为空就跳过
        if node['server'] == '':
            continue
        # 比对：新节点添加|老节点更新
        for i in range(len(accounts)):
            if accounts[i]['server'] == node['server']:
                old = accounts[i]
                n = i
                break
        if old == '': # 添加新节点
            node = {
                "server"     : node['server'],
                "server_port": node['server_port'],
                "password"   : node['password'],
                "method"     : node['method'],
                "protocol"   : "origin",
                "obfs"       : "plain"
            }
            cnf['configs'].append(node)
            n = len(cnf['configs']) - 1
        else: # 更新老节点
            old['server'] = node['server']
            old['server_port'] = node['server_port']
            old['password'] = node['password']
            old['method'] = node['method']
            cnf['configs'][n] = old
        print(str(cnf['configs'][n])+'\n')
        n,old = 0,''

    with open(ss_cnf,'w',encoding='utf8') as fw:
        fw.write(json.dumps(cnf))
    print('\n更新完成~')


if __name__ == '__main__':
    cnf_path = input('选择SS版本(1.SS, 2.SSR): ').strip()
    print()
    if cnf_path is '1':
        ss_version = 'SS'
    else:
        ss_version = 'SSR'
    # 自己配置SS_HOME系统变量
    # 我的本地路径如下：
    # E:\Arsenal\Shadowsocks\SS
    # E:\Arsenal\Shadowsocks\SSR
    # 所以可以选择性更新
    ss_cnf = os.getenv('SS_HOME') + os.sep + ss_version + os.sep + 'gui-config.json'

    try:
       html = get_html()
       urls = get_ss_url()
    except Exception as e:
        pass
    else:
        latest = extract_ss(html, urls) # 一次全部更新
        update_ss(latest)
