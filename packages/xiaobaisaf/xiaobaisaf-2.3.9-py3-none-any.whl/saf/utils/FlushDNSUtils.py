#! /usr/bin/env python
'''
@Author: xiaobaiTser
@Time  : 2023/8/15 0:51
@File  : GithubUtils.py
'''
import os
import sys
import time
from random import randint

try:
    from tkinter.messagebox import *
except ModuleNotFoundError:
    showinfo = showerror = print
try:
    from requests import get, exceptions
    import dns.resolver
except ModuleNotFoundError:
    if sys.version_info.major == 3 and os.name != 'nt':
        os.system('pip3 install requests')
        os.system('pip3 install dnspython')
    else:
        os.system('pip install requests')
        os.system('pip install dnspython')

def get_dns_ips(domain: str = 'github.com'):
    # 获取域名的 A 记录
    ips = []
    try:
        answers = dns.resolver.resolve(domain, 'A')
        for answer in answers:
            if '0.0.0.0' == answer.to_text():
                ips = get_ip138_ip(domain)
            else:
                ips.append(answer.to_text())
    except dns.resolver.NXDOMAIN:
        raise (f"域名【{domain}】不存在")
    except dns.resolver.NoAnswer:
        raise (f"无法获取【{domain}】的 DNS 解析记录")

    return ips

def get_myssl_ip(domain: str = 'github.com'):
    headers = {
        'authority': 'myssl.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cookie': '_ga=GA1.1.473578308.1692038436; Hm_lvt_3eb1b7728282a6055c77885a3ebb8917=1692038436; '
                  '_hjSessionUser_427812=eyJpZCI6ImYyMGEyYzhkLTg4YWItNTBkOC05NDJjLTcyYTgxYzA5MmRkMSIsImNyZWF0ZWQiOjE2OTIwMzg0MzU5ODYsImV4aXN0aW5nIjpmYWxzZX0=; '
                  '_hjShownFeedbackMessage=true; '
                  f'Hm_lpvt_3eb1b7728282a6055c77885a3ebb8917={int(time.time())}; '
                  '_ga_BTRWVRDVDJ=GS1.1.1692114929.2.1.1692114973.0.0.0',
        'referer': 'https://myssl.com/dns_check.html',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Microsoft Edge";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'qtype': '1',
        'host': domain,
        'qmode': '-1',
    }
    try:
        res_cur = get('https://myssl.com/api/v1/tools/dns_query', params=params, headers=headers, timeout=5).json()
        if 'data' in dict(res_cur).keys():
            ips = [ip['value'] for ip in res_cur['data']['01']['answer']['records'] if ip['value'] != '0.0.0.0']
            return ips
    except Exception:
        return ['\n']


def get_ip138_ip(domain: str = 'github.com'):
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Cookie': f'Hm_lvt_9528a85ee34f0781ac55bb6e2c29e7ae=1692031412; '
                  f'Hm_lpvt_9528a85ee34f0781ac55bb6e2c29e7ae={int(time.time())}',
        'Referer': f'https://site.ip138.com/{domain}/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Microsoft Edge";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    params = {
        'domain': domain,
        'time': int(time.time()*1000),
    }
    try:
        cur_res = get('https://site.ip138.com/domain/read.do', params=params, headers=headers, timeout=5).json()
        if cur_res['status']:
            ips = [ip['ip'] for ip in cur_res['data'] if '0.0.0.0' != ip['ip']]
            return ips
        else:
            return get_myssl_ip(domain)
    except Exception:
        return get_myssl_ip(domain)

def rewrite_hosts(domain: str = 'github.com'):
    if sys.platform in ['win32']:
        HOSTS_PATH = r'C:\Windows\System32\drivers\etc\hosts'
    elif sys.platform in ['linux']:
        HOSTS_PATH = '/etc/hosts'
    elif sys.platform in ['darwin']:
        HOSTS_PATH = '/private/etc/hosts'
    else:
        HOSTS_PATH = 'C:/Windows/System32/drivers/etc/hosts'
    if domain:
        ips = get_dns_ips(domain)   # list
        if os.name == 'nt':
            LINES = '\r\n'.join([f'{ip}\t{domain}' for ip in ips if [] != ips])
        else:
            LINES = '\n'.join([f'{ip}\t{domain}' for ip in ips if [] != ips])
        if os.access(HOSTS_PATH, os.R_OK) and os.access(HOSTS_PATH, os.W_OK):
            with open(HOSTS_PATH, 'r+', encoding='UTF-8') as fr:
                HOSTS_LINES = fr.readlines()
                fr.close()
            NEW_LINES = [line for line in LINES if line not in HOSTS_LINES and '\n' != line]
            NEW_LINES.insert(0, '\n')
            HOSTS_LINES.extend(NEW_LINES)
            with open(HOSTS_PATH, 'w+', encoding='UTF-8') as fw:
                fw.writelines(HOSTS_LINES)
                fw.close()
        else:
            showerror('小白警告⚠', '[-] ' + HOSTS_PATH + "，文件无【读&写】权限！请赋权后再次尝试本脚本！")
    else:
        showerror('小白警告⚠', "[-] 不能写入空数据！")



def flushDNS(domains: str = '', limiter: str = ','):
    domains = domains.replace('，', ',')
    for domain in domains.split(limiter):
        time.sleep(randint(2, 5))
        rewrite_hosts(domain=domain)
    os.popen('ipconfig /flushdns')
    showinfo('小白提示😀：', f'所有数据均已经写入HOSTS文件且已经刷新DNS缓存\n如果发现有缺失请重新执行脚本即可！')

# if __name__ == '__main__':
#     flushDNS(
#         ','.join(
#             [
#                 'github.com',
#                 'github.global.ssl.fastly.net',
#                 'assets-cdn.github.com',
#                 'raw.githubusercontent.com',
#                 'carla.org'
#             ]
#         ),
#         ','
#     )