# -*- coding: utf-8 -*-
# @Time    : 2022/10/23 18:56
# @Author  : mf.liang
# @File    : tools.py
# @Software: PyCharm
# @desc    :

import hashlib
import re
import socket
from argparse import Namespace
from inspect import getmodule, stack
from scapy.interfaces import get_working_if
from scapy.arch import get_if_hwaddr
from scapy.layers.dhcp import DHCPTypes, DHCP, BOOTP
from scapy.layers.dhcp6 import dhcp6types, DHCP6OptIAAddress, DHCP6OptRelayMsg, DHCP6OptIAPrefix
from scapy.layers.inet import IP, UDP
from scapy.layers.inet6 import IPv6
from scapy.layers.l2 import Ether
from scapy.utils import mac2str, str2mac
from scapy.volatile import RandMAC
from dhcptool.env_args import pkt_result, logs, summary_result, global_var
import time


class Tools:

    @staticmethod
    def mac_self_incrementing(mac, num, offset=1):
        """
        mac自增
        :param mac:
        :param num:
        :param offset:
        :return:
        """
        mac = ''.join(mac.split(':'))

        #  使用format格式化字符串，int函数，按照16进制算法，将输入的mac地址转换成十进制，然后加上偏移量
        # {:012X}将十进制数字，按照16进制输出。其中12表示只取12位，0表示不足的位数在左侧补0
        mac_address = "{:012X}".format(int(mac, 16) + offset * num)
        mac_address = ':'.join(re.findall('.{2}', mac_address)).lower()
        return mac_address

    @staticmethod
    def mac_self_subtracting(mac, num, offset=1):
        """
        mac自增
        :param mac:
        :param num:
        :param offset:
        :return:
        """
        mac = ''.join(mac.split(':'))

        #  使用format格式化字符串，int函数，按照16进制算法，将输入的mac地址转换成十进制，然后加上偏移量
        # {:012X}将十进制数字，按照16进制输出。其中12表示只取12位，0表示不足的位数在左侧补0
        mac_address = "{:012X}".format(int(mac, 16) - offset * num)
        mac_address = ':'.join(re.findall('.{2}', mac_address)).lower()
        return mac_address

    @staticmethod
    def get_mac(args: Namespace = None):
        """
        获取mac信息
        :return:
        """
        if args.mac is not None:
            if args.fixe:
                mac = mac2str(args.mac)
            else:
                mac = Tools.mac_self_incrementing(args.mac, global_var.get('tag'))
                mac = mac2str(mac)
        else:
            if args.filter and len(args.filter.split('.')) == 4:
                mac = get_if_hwaddr(get_working_if().name)
                mac = Tools.mac_self_incrementing(mac, global_var.get('tag'))
                mac = mac2str(mac)
            else:
                mac = mac2str(RandMAC())
        global_var.update({"generate_mac": mac})
        return mac

    @staticmethod
    def get_xid_by_mac(mac):
        """
        根据mac生成hash
        :return:
        """
        mac = str2mac(mac).encode('utf-8')
        m = hashlib.md5()
        m.update(mac)
        mac_xid = int(str(int(m.hexdigest(), 16))[0:9])
        return mac_xid

    @staticmethod
    def convert_code(data):
        """
        字节/16进制相互转换
        :param data:
        :return:
        """
        if isinstance(data, bytes):  # 转 16进制
            data = data.hex()
        else:  # 字符串转化成字节码
            data = bytes.fromhex(data)
        return data

    @staticmethod
    def get_local_ipv4():
        # 获取本机IP
        local_ipv4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        local_ipv4.connect(('8.8.8.8', 80))
        local_ipv4 = local_ipv4.getsockname()[0]

        return local_ipv4

    @staticmethod
    def get_local_ipv6():
        # 获取本机ipv6
        local_ipv6 = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        try:
            local_ipv6.connect(('2001:da8:ff:305:20c:29ff:fe1f:a92a', 80))
            local_ipv6 = local_ipv6.getsockname()[0]
        except:
            local_ipv6 = "1000:0:0:31::135"
        return local_ipv6

    @staticmethod
    def analysis_results(pkts_list, args: Namespace = None, call_name=None):
        """
        解析结果并存入队列
        :param args:
        :param pkts_list:
        :param DHCPv6:
        :param filter:
        :return:
        """
        if args.filter:
            filter_ip = args.filter
        else:
            filter_ip = args.dhcp_server
        call_func_name = getmodule(stack()[1][0])
        call_mod = call_func_name.__name__
        for pkt in pkts_list:
            if 'dhcp4' in call_mod:
                Tools.analysis_results_v4(pkt, args, filter_ip)
            else:
                Tools.analysis_results_v6(pkt, args, filter_ip, call_name)

    @staticmethod
    def analysis_results_v4(pkt, args, filter_ip):
        if pkt[IP].src == filter_ip:
            if pkt[DHCP].options[0][1] == 2:
                pkt_result.get('dhcp4_offer').put(pkt)
                Tools.print_formart(pkt, args.debug)
            elif pkt[DHCP].options[0][1] == 5:
                pkt_result.get('dhcp4_ack').put(pkt)
                Tools.print_formart(pkt, args.debug)
            elif pkt[DHCP].options[0][1] == 6:
                pkt_result.get('dhcp4_nak').put(pkt)
                Tools.print_formart(pkt, args.debug)
        else:
            logs.info('没有监听到 server 返回 结果！,请检查是否有多个DHCP server影响监听结果')

    @staticmethod
    def analysis_results_v6(pkt, args, filter_ip, call_name=None, DHCPv6=None, ):
        if pkt[IPv6].src == filter_ip:
            if pkt[DHCPv6].msgtype == 2:
                try:
                    assert pkt[DHCP6OptIAAddress].addr
                    pkt_result.get('dhcp6_advertise').put(pkt)
                    if call_name is None:
                        Tools.print_formart(pkt, args.debug)
                except Exception as ex:
                    try:
                        assert pkt[DHCP6OptIAPrefix].prefix
                        pkt_result.get('dhcp6_advertise').put(pkt)
                        if call_name is None:
                            Tools.print_formart(pkt, args.debug)
                    except Exception as ex:
                        logs.error('返回包中没有携带分配ip！')
                        assert False
            elif pkt[DHCPv6].msgtype == 7:
                pkt_result.get('dhcp6_reply').put(pkt)
                if call_name is None:
                    Tools.print_formart(pkt, args.debug)

            elif pkt[DHCPv6].msgtype == 13:
                ether_ipv6_udp = Ether() / IPv6(src=pkt[IPv6].src) / UDP()
                relay_pkt = ether_ipv6_udp / pkt[DHCP6OptRelayMsg].message
                Tools.analysis_results(pkts_list=relay_pkt, args=args, call_name=1)
                Tools.print_formart(pkt, args.debug)
        else:
            logs.info('没有监听到 server 返回 结果！,请检查是否有多个DHCP server影响监听结果')

    @staticmethod
    def print_formart(pkt, debug):
        """
        格式化打印
        :param pkt:
        :param level:
        :return:
        """
        response_dict = {}
        if debug:
            pkt.show2()
        else:
            detail_info = pkt[UDP][1:].summary()
            mac = str2mac(global_var.get('generate_mac')) or ''
            if pkt.payload.name == 'IPv6':
                src_dst = pkt[IPv6].mysummary().split('(')[0]
                response_dict.update({"info": "{:<36} | {}".format(src_dst, detail_info.split('/')[0])})
                content_format = Tools.print_formart_v6(pkt, response_dict, mac)
            else:
                src_dst = pkt[IP].mysummary().split('udp')[0]
                response_dict.update({"info": "{:<36} | {}".format(src_dst, detail_info)})
                content_format = Tools.print_formart_v4(pkt, response_dict, mac)
            logs.info(content_format)
        Tools.record_pkt_num(pkt)

    @staticmethod
    def print_formart_v4(pkt, response_dict, mac):
        """
        DHCPv6格式化打印
        :param pkt:
        :param response_dict:
        :param mac:
        :return:
        """
        yiaddr = pkt[BOOTP].yiaddr
        response_dict.update({"yiaddr": yiaddr})
        yiaddr = response_dict.get('yiaddr') or ''
        info = response_dict.get('info') or ''
        content_format = "v4 | {:<} | {:<15} | {:<}".format(mac, yiaddr, info)
        return content_format

    @staticmethod
    def print_formart_v6(pkt, response_dict, mac):
        """
        DHCPv4格式化打印
        :param pkt:
        :param response_dict:
        :param mac:
        :return:
        """
        try:
            addr = pkt[DHCP6OptIAAddress].addr
            response_dict.update({"addr": addr})
            prefix = pkt[DHCP6OptIAPrefix].prefix
            response_dict.update({"prefix": prefix})
        except Exception as ex:
            if 'DHCP6OptIAAddress' in str(ex):
                try:
                    prefix = pkt[DHCP6OptIAPrefix].prefix
                    response_dict.update({"prefix": prefix})
                except:
                    pass
        addr = response_dict.get('addr') or ''
        prefix = response_dict.get('prefix') or ''
        info = response_dict.get('info') or ''
        content_format = "v6 | {:<} | NA: {:<15} | PD: {:<} | {:<}".format(mac, addr, prefix, info)
        return content_format

    @staticmethod
    def record_pkt_num(pkt, DHCPv6=None):
        try:
            for i in dhcp6types:
                if pkt[DHCPv6].msgtype == i:
                    summary_result[dhcp6types.get(i)] += 1
                    if pkt[DHCPv6].msgtype in (12, 13):
                        Tools.record_pkt_num(pkt[DHCP6OptRelayMsg].message)
        except:
            for v in DHCPTypes.values():
                pkt_type = pkt[DHCP].options[0][1]
                if isinstance(pkt_type, int):
                    pkt_type = DHCPTypes.get(pkt_type)
                if pkt_type == v:
                    summary_result[v.upper()] += 1

    @staticmethod
    def rate_print(text_tips, sleep_time):
        """
        倒计时打印
        :param text_tips:
        :param sleep_time:
        :return:
        """
        if sleep_time != 0:
            for i in range(sleep_time, 0, -1):
                print("\r", text_tips, '倒计时', "{}".format(i), '', end="", flush=True)
                time.sleep(1)

    @staticmethod
    def get_version_desc():
        version_desc = """
        dhcptool@1.1:
        1. 重新将iface支持增加回来
        2. 支持广播模式下配置指定的中继
        """
        return version_desc
