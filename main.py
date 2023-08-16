# -*- coding = utf-8 -*-
# @Time : 2023/08/09 19:07
# @Autor : Fucloud
# @FIle : tts.py
# @Software : PyCharm

from core.ms.tts import TTS
from utils import arg_parser

if __name__ == '__main__':
    args = arg_parser.get_args()

    # 输出结果
    tts = TTS(args.name)
    tts.read_speak_text(args.input)
    tts.speak()
