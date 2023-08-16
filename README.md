# TTS程序

## 打包方式
* 打包教程：https://www.zhihu.com/tardis/zm/art/162237978?source_id=1003
* 缺少dll文件解决方案：https://blog.csdn.net/Neil_001/article/details/121132604

1. 使用pip/conda安装`Pyinstaller`打包程序
2. 使用`pyinstaller -F xx.py`/`pyinstaller xx.spec` 命令安装
> 注意事项： 使用ms的tts服务需要使用dll文件
> ```python
> datas=[ ('xx.dll', '.') ],
> ```
> `xx.dll`为对应文件路径，将文件赋值过来似乎不可以