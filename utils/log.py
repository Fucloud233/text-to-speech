# -*- coding = utf-8 -*-
# @Time : 2023/08/08 18:44
# @Autor : Fucloud
# @FIle : log.py
# @Software : PyCharm

from enum import Enum
from pathlib import Path
from utils import time


class LogType(Enum):
    info = 'info'
    warn = 'warn'
    error = 'error'

    def __str__(self):
        return self.name


class Log:
    __output_path = Path("log")

    def __init__(self, show_on_cli: bool = True):
        # 创建文件名
        self.__log_save_path: Path
        self.__log_file = None
        self.__create()

        self.show_on_cli = show_on_cli

    # 创建log文件
    def __create(self):
        if not Log.__output_path.exists():
            Log.__output_path.mkdir()

        # 创建文件
        log_file_name = Path(time.get_log_file_time() + ".log")
        log_file_name = Path.joinpath(Log.__output_path, log_file_name)
        self.__log_file = open(log_file_name, "w", encoding="utf-8")

    def __check_valid(self) -> bool:
        return self.__log_file is not None

    def __log(self, msg_type: LogType, args: tuple):
        if not self.__check_valid():
            return

        # 生成文本
        output_text = "[%s]%-7s" % (time.get_log_time(), f"[{msg_type}]")
        for arg in args:
            output_text += " " + str(arg)

        if self.show_on_cli:
            print(output_text)
        self.__log_file.write(output_text + '\n')

    # 清除所有日志文件
    @staticmethod
    def clear():
        if not Log.__output_path.exists():
            return
        # 删除文件
        for file in Log.__output_path.iterdir():
            file.unlink()

    def info(self, *args):
        self.__log(LogType.info, args)

    def warn(self, *args):
        self.__log(LogType.warn, args)

    def error(self, *args):
        self.__log(LogType.error, args)


if __name__ == "__main__":
    Log.clear()
    log = Log()
    log.info("hello", 1, 2, 3)
    log.error("file not found")
    log.warn("you are wrong")
