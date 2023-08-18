#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by zj on 2022/04/22 
# Task:

import logging
import os
import socket
import time
from datetime import datetime


def is_chinese(uchar):
    """判断一个unicode是否是汉字"""
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False


def is_number(uchar):
    """判断一个unicode是否是半角数字"""
    if uchar >= u'\u0030' and uchar <= u'\u0039':
        return True
    else:
        return False


def is_Qnumber(uchar):
    """判断一个unicode是否是全角数字"""
    if uchar >= u'\uff10' and uchar <= u'\uff19':
        return True
    else:
        return False


def is_alphabet(uchar):
    """判断一个unicode是否是半角英文字母"""
    if (uchar >= u'\u0041' and uchar <= u'\u005a') or (uchar >= u'\u0061' and uchar <= u'\u007a'):
        return True
    else:
        return False


def is_Qalphabet(uchar):
    """判断一个unicode是否是全角英文字母"""
    if (uchar >= u'\uff21' and uchar <= u'\uff3a') or (uchar >= u'\uff41' and uchar <= u'\uff5a'):
        return True
    else:
        return False


def is_other(uchar):
    """判断是否非汉字，数字和英文字符"""
    if not (is_chinese(uchar) or is_number(uchar) or is_alphabet(uchar)):
        return True
    else:
        return False


def Q2B(uchar):
    """单个字符 全角转半角"""
    inside_code = ord(uchar)
    if inside_code == 0x3000:
        inside_code = 0x0020
    else:
        inside_code -= 0xfee0
    if inside_code < 0x0020 or inside_code > 0x7e:  # 转完之后不是半角字符返回原来的字符
        return uchar
    return chr(inside_code)


def B2Q(uchar):
    """单个字符 半角转全角"""
    inside_code = ord(uchar)
    if inside_code < 0x0020 or inside_code > 0x7e:  # 不是半角字符就返回原来的字符
        return uchar
    if inside_code == 0x0020:  # 除了空格其他的全角半角的公式为: 半角 = 全角 - 0xfee0
        inside_code = 0x3000
    else:
        inside_code += 0xfee0
    return chr(inside_code)


def stringQ2B(ustring):
    """把字符串全角转半角"""
    return "".join([Q2B(uchar) for uchar in ustring])


def stringpartQ2B(ustring):
    """把字符串中数字和字母全角转半角"""
    return "".join([Q2B(uchar) if is_Qnumber(uchar) or is_Qalphabet(uchar) else uchar for uchar in ustring])


class AverageMeter(object):

    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count


def setup_logger(logger_name, log_root=None, log_file_save_basename=None, level=logging.INFO, screen=True,
                 tofile=False, msecs=False):
    '''set up logger'''
    lg = logging.getLogger(logger_name)
    if msecs:
        formatter = logging.Formatter('[%(levelname)s] [%(asctime)s.%(msecs)03d] %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')
    else:
        formatter = logging.Formatter('[%(levelname)s] [%(asctime)s] %(message)s',
                                      datefmt='%Y-%m-%d %I:%M:%S %p')
    lg.setLevel(level)
    if tofile and log_root:
        if not os.path.exists(log_root):
            os.makedirs(log_root)
        if log_file_save_basename:
            log_file = os.path.join(log_root, log_file_save_basename)
        else:
            log_file = os.path.join(log_root, f'{get_time_str()}.log')

        fh = logging.FileHandler(log_file, mode='a')
        fh.setFormatter(formatter)
        lg.addHandler(fh)
    if screen:
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        lg.addHandler(sh)
    return lg


def get_time_int():
    return int(time.strftime("%Y%m%d%H%M%S", time.localtime(time.time())))


# def get_time_str():
#     return time.strftime("%m%d%H%M%S%Y", time.localtime(time.time()))

def get_time_str():
    return time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))


def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def main():
    mylogger = setup_logger('test', msecs=True)
    mylogger.info('tttt')


if __name__ == '__main__':
    start = datetime.now()
    print("Start time is {}".format(start))
    main()
    end = datetime.now()
    print("End time is {}".format(end))
    print("\nTotal running time is {}s".format((end - start).seconds))
    print("\nCongratulations!!!")
