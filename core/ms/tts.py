# -*- coding = utf-8 -*-
# @Time : 2023/08/05 20:24
# @Autor : Fucloud
# @FIle : tts.py
# @Software : PyCharm

from datetime import datetime
from pathlib import Path

from core.ms.tts_sdk import Speech
from utils.log import Log
from utils import time
from utils.system import exit_program


class TTS:
    __speak_texts = []

    def __init__(self, name: str = "tts",
                 output_file_path: str = "output",
                 name_len: int = 5):
        # 初始化 加载配置信息+连接api
        self.speech = Speech()
        self.speech.connect()

        self.name = name
        self.output_path = Path(output_file_path)
        if not self.output_path.exists():
            self.output_path.mkdir()

        # name_len 用于个输入message命名(输入文本的前n个)
        self.name_len = max(3, name_len)

    # 文本列表输入
    def set_speak_text(self, speak_texts: list):
        self.__speak_texts = speak_texts

    # 文件输入
    def read_speak_text(self, read_file_path: str):
        try:
            with open(read_file_path, "r", encoding="utf-8") as f:
                read_texts = f.readlines()
        except FileNotFoundError:
            Log.error("{} not exists!".format(read_file_path))
            exit_program(-1)

        for text in read_texts:
            # 去除空值
            if text != "":
                self.__speak_texts.append(text)

    # 文本转语音
    def speak(self):
        begin_time = time.get_cur_time()
        output_path = self.__gen_output_path(begin_time)

        # 转换音频
        for i in range(len(self.__speak_texts)):
            speak_text = self.__speak_texts[i]
            self.__to_sound(output_path, speak_text, i)

        # 显示结果
        Log.info("合成音频完成! 共{}个文本, 耗时: {}s".format(
            len(self.__speak_texts),
            time.get_need_time(begin_time)
        ))
        Log.info("输出路径: ", output_path.absolute())

    # 文本转语言 单元
    def __to_sound(self, output_path: Path, speak_text: str, index: int = -1):
        file_name = self.__get_file_name(speak_text, index)
        _ = self.speech.to_sample(speak_text,
                                  output_path=output_path,
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
            return f"[{index + 1}] {file_name}"

    # 设置输出路径
    def __gen_output_path(self, begin_time: datetime) -> Path:
        sub_output_path = str(int(begin_time.timestamp()))
        output_path = Path.joinpath(self.output_path, self.name, sub_output_path)

        # 如果添加时间戳后缀仍重复 则删除重新创建
        if output_path.exists():
            for f in output_path.iterdir():
                f.unlink()
        else:
            # 设置参parents为True 同时创建多个文件夹
            output_path.mkdir(parents=True)

        return output_path

