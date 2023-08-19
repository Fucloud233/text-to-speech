# -*- coding = utf-8 -*-
# @Time : 2023/08/05 20:24
# @Autor : Fucloud
# @FIle : tts.py
# @Software : PyCharm

from datetime import datetime
from pathlib import Path
import shutil

from core.ms.tts_sdk import Speech
from utils.log import Log
from utils import time
from utils.system import exit_program

# 默认输入文件
default_input_file_name = "input.txt"
# 注释文本
example_note = "// 以下第一行为输出文件，接下来的所有行会被转换为语音\n" \
    "// 注意程序会忽略“//”开头的文本和空行"


class TTS:
    __speak_texts = []

    def __init__(self, output_path: str = 'output', name_len: int = 5):
        # 初始化 加载配置信息+连接api
        self.speech = Speech()
        self.speech.connect()

        self.name = None
        self.input_path: Path = Path()
        self.output_path: Path = Path(output_path)

        # name_len 用于个输入message命名(输入文本的前n个)
        self.name_len = max(3, name_len)

    # 文本列表输入
    def set_speak_text(self, speak_texts: list):
        self.__speak_texts = speak_texts

    # 文件输入
    def read_speak_text(self, read_file_path: str = default_input_file_name):
        try:
            with open(read_file_path, "r", encoding="utf-8") as f:
                read_texts = f.readlines()
        except FileNotFoundError:
            if read_file_path == default_input_file_name:
                gen_default_input_file()
                Log.error("默认输入文件不存在，已创建", default_input_file_name)
            else:
                Log.error("{} 文件不存在".format(read_file_path))

            exit_program(-1)

        #  取第一个元素为项目名字
        counter = 0
        for i in range(0, len(read_texts)):
            text = read_texts[i].strip()
            # 如果文本非空 而且并非//开头 则加入
            if text.startswith("//") or text is None:
                continue
            elif counter == 0:
                self.name = read_texts[i].strip()
            else:
                self.__speak_texts.append(text)
            counter += 1

        if counter < 2:
            Log.error("没有输入“输出路径”或“转换文本”")
            exit_program(-1)

        self.input_path = Path(read_file_path)

    # 文本转语音 (返回输出路径)
    def speak(self) -> Path:
        begin_time = time.get_cur_time()
        output_path = self.__gen_output_path(begin_time)

        # 转换音频
        for i in range(len(self.__speak_texts)):
            speak_text = self.__speak_texts[i]
            self.__to_sound(output_path, speak_text, i)

        # 备份输入信息
        shutil.copy(self.input_path, Path.joinpath(output_path, self.input_path.name))

        # 显示结果
        Log.info("合成音频完成! 共{}个文本, 耗时: {}s".format(
            len(self.__speak_texts),
            time.get_need_time(begin_time)
        ))
        Log.info("输出路径: ", output_path.absolute())

        return output_path

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
            return f"[%02d] %s" % (index + 1, file_name)

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


def gen_default_input_file():
    with open(default_input_file_name, "w", encoding="utf-8") as f:
        f.write(example_note)