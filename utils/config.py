# -*- coding = utf-8 -*-
# @Time : 2023/08/08 18:11
# @Autor : Fucloud
# @FIle : config.py
# @Software : PyCharm

import json
from json.decoder import JSONDecodeError
from utils.log import Log


def gen_config_file():
    config_info = {
        "key": "",
        "region": ""
    }
    with open(Config.config_file_path, 'w', encoding="utf-8") as f:
        config_info_json = json.dumps(config_info, indent=4, separators=(',', ':'))
        f.write(config_info_json)


class Config:
    config_file_path = "config.json"

    def __init__(self):
        self.__config_key = None
        self.__config_region = None
        # 用于记录配置信息是否有效
        self.__is_valid = False
        self.load_key()

    def load_key(self):
        self.__is_valid = False

        config_info_str = "{}"

        # 读取配置文件
        try:
            with open(Config.config_file_path, 'r', encoding="utf-8") as f:
                for line in f.readlines():
                    config_info_str += line.strip()
        except FileNotFoundError:
            # 文件不存在则生成文件
            gen_config_file()
            # print('[error] "config.json"文件不存在')

        # 读取配置文件中的信息
        try:
            config_info = json.loads(config_info_str)
            self.__config_key = config_info["key"]
            self.__config_region = config_info["region"]
        except (JSONDecodeError, KeyError):
            Log.error('缺少"key"或者"region"配置信息')
            # print('[error] 缺少"key"或者"region"配置信息')
        # 验证读取非空
        if self.__config_key and self.__config_region is not None:
            self.__is_valid = True

    def get_key(self):
        return self.__config_key

    def get_region(self):
        return self.__config_region

    def is_valid(self):
        return self.__is_valid


if __name__ == "__main__":
    Log.init()
    config = Config()
    Log.debug("key: {}, region: {}".format(config.get_key(), config.get_region()))
    Log.debug("is_valid: ", config.is_valid())
