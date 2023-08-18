#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   config.py
@Time    :   2023/08/11 15:44:57
@Author  :   mf.liang
@Version :   1.0
@Contact :   mf.liang@outlook.com
@Desc    :   
'''

# here put the import lib
import json
import yaml

def read_yaml_config():
    # 读取YAML文件
    with open('C:\\Users\\mflia\\vscodework\\dhcptool\\dhcptool\\config.yaml', 'r') as file:
        data = yaml.safe_load(file)

    # 打印读取的数据
    print(json.dumps(data, indent=4,ensure_ascii=False))

if __name__ == '__main__':
    # read_ini_conf()
    read_yaml_config()