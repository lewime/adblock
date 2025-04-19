# -*- encoding: utf-8 -*-

# Homepage: https://github.com/lewime/adblock

import base64
import hashlib
import os
import re
import time
import urllib.parse
import urllib.request

URL = [
    'https://easylist-downloads.adblockplus.org/easylist.txt',
    'https://easylist-downloads.adblockplus.org/easylistchina.txt',
    'https://easylist-downloads.adblockplus.org/easyprivacy.txt',
    'https://raw.githubusercontent.com/cjx82630/cjxlist/master/cjxlist.txt',
    'https://raw.githubusercontent.com/cjx82630/cjxlist/master/cjx-annoyance.txt',
    'https://raw.githubusercontent.com/xinggsf/Adblock-Plus-Rule/master/mv.txt',
]


def read_file(file_path: str):
    with open(file_path, mode='r', encoding='utf8') as f:
        return f.read()


def write_file(file_path: str, text: str):
    with open(file_path, mode='w', encoding='utf8') as f:
        return f.write(text)


def remove_line(text: str):
    tmp = []
    for line in text.split('\n'):
        if line.startswith('[') or line.startswith('!') or line.strip() == '':
            continue
        tmp.append(line)
    lines = list(set(tmp))
    lines.sort()
    return '\n'.join(lines)


def calc_checksum(text: str):
    text = re.sub(r'\r', '', text)
    text = re.sub(r'\n+', '\n', text)
    md5 = hashlib.md5(str(text).encode()).digest()
    result = base64.b64encode(md5).decode().rstrip('=')
    return result


def generate_header(title: str, version: str, date: str, checksum: str):
    tmp = []
    tmp.append('[Adblock Plus 2.0]')
    tmp.append(f'! Checksum: {checksum}')
    tmp.append(f'! Version: {version}')
    tmp.append(f'! Title: {title}')
    tmp.append('! Expires: 12 hours')
    tmp.append(f'! Last Modified: {date}')
    tmp.append('! Homepage: https://github.com/lewime/adblock')
    tmp.append('! \n')
    return '\n'.join(tmp)


def download_rule():
    if not os.path.exists('./download'):
        os.mkdir('./download')
    for url in URL:
        print(f'Download: {url}')
        filename = url.split('/')[-1:][0]
        urllib.request.urlretrieve(url, f'./download/{filename}')


def generate_rule():
    easylist = read_file('./download/easylist.txt')
    easylistchina = read_file('./download/easylistchina.txt')
    easyprivacy = read_file('./download/easyprivacy.txt')
    cjxlist = read_file('./download/cjxlist.txt')
    cjxannoyance = read_file('./download/cjx-annoyance.txt')
    xinggsf_mv = read_file('./download/mv.txt')
    rule = read_file('./rule.txt')
    rule_pc = rule + cjxannoyance + xinggsf_mv + easylist + easylistchina + easyprivacy
    rule_mobile = rule + cjxlist + cjxannoyance + xinggsf_mv + easylistchina
    rule_pc = remove_line(rule_pc)
    rule_mobile = remove_line(rule_mobile)
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    ver = str(int(time.time() * 1000))
    pc = generate_header('Adblock (for PC)', ver, date, calc_checksum(rule_pc)) + rule_pc
    mobile = generate_header('Adblock (for Mobile)', ver, date, calc_checksum(rule_mobile)) + rule_mobile
    write_file('./ad-pc.txt', pc)
    write_file('./ad.txt', mobile)


def main():
    download_rule()
    generate_rule()


if __name__ == '__main__':
    main()
