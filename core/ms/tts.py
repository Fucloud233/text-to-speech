# -*- coding = utf-8 -*-
# @Time : 2023/08/05 20:24
# @Autor : Fucloud
# @FIle : tts.py
# @Software : PyCharm

import math
import time
from pathlib import Path

from core.ms.tts_sdk import Speech
from utils.log import Log


def get_need_time(begin_time: time):
    return math.floor((time.time() - begin_time) * 1000)


class TTS:
    __speak_texts = []

    def __init__(self, name: str = "tts",
                 output_file_path: str = "output",
                 name_len: int = 5):
        # 初始化 加载配置信息+连接api
        self.speech = Speech()
        self.speech.connect()

        self.output_path = Path.joinpath(Path(output_file_path), name)
        if not self.output_path.exists():
            # 设置参parents为True 同时创建多个文件夹
            self.output_path.mkdir(parents=True)
        # else:
        #     for item in self.output_path.iterdir():
        #         if item.suffix == ".mp3":
        #             item.unlink()

        # name_len 用于个输入message命名(输入文本的前n个)
        self.name_len = max(3, name_len)

    # 文本列表输入
    def set_speak_text(self, speak_texts: list):
        self.__speak_texts = speak_texts

    # 文件输入
    def read_speak_text(self, read_file_path: str):
        try:
            with open(read_file_path, "r", encoding="utf-8") as f:
                self.__speak_texts = f.readlines()
        except FileNotFoundError:
            Log.error("{} not exists!".format(read_file_path))
            return

        for i in range(len(self.__speak_texts)):
            self.__speak_texts[i] = self.__speak_texts[i].strip()

    # 文本转语音
    def speak(self):
        begin_time = time.time()
        # 转换音频
        for i in range(len(self.__speak_texts)):
            speak_text = self.__speak_texts[i]
            self.__to_sound(speak_text, i)

        # 显示结果
        Log.info("合成音频完成! 共{}个文本, 耗时: {}s".format(
            len(self.__speak_texts),
            get_need_time(begin_time)
        ))

    # 文本转语言 单元
    def __to_sound(self, speak_text: str, index: int = -1):
        file_name = self.__get_file_name(speak_text, index)
        file_url = self.speech.to_sample(speak_text,
                                         output_path=self.output_path,
                                         file_name=file_name)
        # print("[info] 合成完毕: ", file_url)

    # 设置文件名
    def __get_file_name(self, input_message: str, index: int) -> str:
        file_name: str
        if len(input_message) <= self.name_len:
            file_name = input_message
        else:
            # 如果长度小于3
            file_name = input_message[:self.name_len]

        # 添加序号
        if index == -1:
            return file_name
        else:
            return f"{index} {file_name}"