# -*- coding = utf-8 -*-
# @Time : 2023/08/09 19:07
# @Autor : Fucloud
# @FIle : tts.py
# @Software : PyCharm
import os

from core.ms.tts import TTS
from utils import arg_parser

if __name__ == '__main__':
    args = arg_parser.get_args()

    # 输出结果
    tts = TTS()
    tts.read_speak_text(args.input)
    output_path = tts.speak()

    # 自动打开资源管理器
    os.system(f"explorer {output_path}")
    os.system("pause")

