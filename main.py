# -*- coding = utf-8 -*-
# @Time : 2023/08/09 19:07
# @Autor : Fucloud
# @FIle : tts.py
# @Software : PyCharm

from core.ms.tts import TTS

if __name__ == '__main__':
    input_file_url = "input.txt"

    # 输出结果
    tts = TTS("light")
    tts.read_speak_text(input_file_url)
    tts.speak()
