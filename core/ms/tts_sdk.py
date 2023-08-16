import time
# 通信地址
import azure.cognitiveservices.speech as speechsdk

# import asyncio
# import edge_tts

from pathlib import Path
from core.ms import tts_voice
from core.ms.tts_voice import EnumVoice
from utils.tts_config import TTSConfig as Config
from utils.log import Log


class Speech:
    config = Config()

    def __init__(self):
        self.ms_tts = False

        if self.config.is_valid:
            speech_config = speechsdk.SpeechConfig(
                subscription=self.config.key,
                region=self.config.region)
            speech_config.speech_recognition_language = "zh-CN"
            speech_config.speech_synthesis_voice_name = "zh-CN-XiaoxiaoNeural"
            speech_config.set_speech_synthesis_output_format(
                speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)
            self.__speech_config = speech_config
            self.__synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
            self.ms_tts = True

        self.__connection = None
        self.__history_data = []

    def __get_history(self, voice_name, style, text):
        for data in self.__history_data:
            if data[0] == voice_name and data[1] == style and data[2] == text:
                return data[3]
        return None

    def connect(self):
        if self.ms_tts:
            self.__connection = speechsdk.Connection.from_speech_synthesizer(self.__synthesizer)
            self.__connection.open(True)
        Log.info("TTS 服务已经连接！")

    def close(self):
        if self.__connection is not None:
            self.__connection.close()

    # 生成mp3音频
    # async def get_edge_tts(self,text,voice,file_url) -> None:
    #     communicate = edge_tts.Communicate(text, voice)
    #     await communicate.save(file_url)

    """
    文字转语音
    :param text: 文本信息
    :param style: 说话风格、语气
    :returns: 音频文件路径
    """

    def to_sample(self, text, style="",
                  output_path: Path = Path('samples'), file_name: str = None):

        def get_file_url() -> str:
            file_output_name = file_name
            if file_output_name is None:
                file_output_name = 'sample-' + str(int(time.time() * 1000))
            # 添加后缀
            file_output_name += ".mp3"
            # 合并路径
            result_file_name = Path.joinpath(Path(output_path), file_output_name)
            return result_file_name.as_posix()

        # 选择声源
        voice_type = tts_voice.get_voice_of(self.config.voice)
        voice_name = EnumVoice.XIAO_XIAO.value["voiceName"]
        if voice_type is not None:
            voice_name = voice_type.value["voiceName"]
        history = self.__get_history(voice_name, style, text)
        if history is not None:
            return history
        # 加快了声音
        ssml = '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="zh-CN">' \
               '<voice name="{}">' \
               '<mstts:express-as style="{}" styledegree="{}">' \
               '<prosody rate="0.00%">' \
               '{}' \
               '</prosody>' \
               '</mstts:express-as>' \
               '</voice>' \
               '</speak>'.format(voice_name, style, 1.8, text)

        if self.ms_tts:
            result = self.__synthesizer.speak_ssml(ssml)
            audio_data_stream = speechsdk.AudioDataStream(result)

            file_url = get_file_url()
            audio_data_stream.save_to_wav_file(file_url)
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                self.__history_data.append((voice_name, style, text, file_url))
                return file_url
            else:
                Log.error("语音转换失败！\n", str(result.reason))
                return None
        # else:
        #     try:
        #         file_url = get_file_url()
        #         asyncio.new_event_loop().run_until_complete(self.get_edge_tts(text, voice_name, file_url))
        #         self.__history_data.append((voice_name, style, text, file_url))
        #     except Exception as e:
        #         Log.error("语音转换失败！\n", repr(e))
        #         file_url = None
        #     return file_url


if __name__ == '__main__':
    sp = Speech()
    sp.connect()
    text = """这是一段音频，测试一下3"""
    s = sp.to_sample(text, "cheerful")

    print(s)
    sp.close()

