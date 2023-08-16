# -*- coding = utf-8 -*-
# @Time : 2023/08/08 18:11
# @Autor : Fucloud
# @FIle : config.py
# @Software : PyCharm

from abc import abstractmethod
import json
from json.decoder import JSONDecodeError
from utils.log import Log
from utils.system import exit_program


class Config:
    __config_file_path = "config.json"

    def __init__(self, auto_load: bool = True):
        self._config_info = None
        self.__is_valid = False
        # 设置是否自动加载
        if auto_load:
            self.load_key()

    # 用于记录配置信息是否有效
    def load_key(self):
        self.__is_valid = False

        # 读取配置文件
        config_info_str = ""
        try:
            with open(Config.__config_file_path, 'r', encoding="utf-8") as f:
                for line in f.readlines():
                    config_info_str += line.strip()

            # 读取配置文件中的信息
            self._config_info = json.loads(config_info_str)
        except FileNotFoundError:
            # 文件不存在 则直接生成基础的配置信息
            self.gen_config_file()
        except JSONDecodeError:
            Log.error('json解析失败')
            exit_program(-1)

        # 验证读取非空
        if not self._check_config_info():
            Log.error('缺少关键配置信息')
            exit_program(-1)

        self.__is_valid = True

    def gen_config_file(self):
        self._config_info = self._init_config_info()
        with open(Config.__config_file_path, 'w', encoding="utf-8") as f:
            config_info_json = json.dumps(self._config_info, indent=4, separators=(',', ':'))
            f.write(config_info_json)

    @abstractmethod
    def _check_config_info(self):
        pass

    # 用于初始化配置信息 (抽象函数)
    @abstractmethod
    def _init_config_info(self) -> dict:
        pass

    @property
    def config_info(self):
        return self._config_info

    @property
    def is_valid(self):
        return self.__is_valid
