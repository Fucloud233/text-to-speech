# -*- coding = utf-8 -*-
# @Time : 2023/08/15 15:44
# @Autor : Fucloud
# @FIle : arg_parser.py
# @Software : PyCharm

import argparse
from argparse import Namespace
from utils.log import Log


def get_args() -> Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="输入文件路径")
    parser.add_argument('--name', default="tts", help="输出名")
    args = parser.parse_args()

    if args.input is None:
        parser.error("缺少输入文件位置")
    elif args.name is None:
        parser.error("缺少输出文件名称")

    Log.info("读取文件: {} 输出名: {}".format(args.input, args.name))

    return args


