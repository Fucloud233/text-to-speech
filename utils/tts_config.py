# -*- coding = utf-8 -*-
# @Time : 2023/08/09 17:57
# @Autor : Fucloud
# @FIle : tts_config.py
# @Software : PyCharm

from utils.config import Config
from utils.log import Log


class TTSConfig(Config):
    def _check_config_info(self):
        try:
            return self._config_info["key"] \
                   and self._config_info["region"] \
                   and self._config_info["voice"] is not None
        except KeyError:
            return False

    def _init_config_info(self) -> dict:
        return {
            "key": "",
            "region": "",
            "voice": "YUN_FENG"
        }

    @property
    def key(self):
        return self._config_info["key"]

    @property
    def region(self):
        return self._config_info["region"]

    @property
    def voice(self):
        return self._config_info["voice"]


if __name__ == "__main__":
    Log.init()
    config = TTSConfig()
    Log.debug("key: {}, region: {}".format(config.key, config.region))
    Log.debug("is_valid: ", config.is_valid)

