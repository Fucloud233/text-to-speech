# 文本转语音程序
本程序使用微软Azure云服务中的tts（文本转语音）API实现

## 使用方法 
本程序提供两种运行的方式，但在使用程序之前都需要前配置好配置文件`config.json`中对应的区域和密钥。
不过，如果缺少配置文件，运行程序后会自动生成配置文件模板。

程序在生成成功后，会自动打开文件所在路径。

### BAT运行方法
1. 创建`input.txt`输入文件（直接运行程序也会生成对应模板）
2. 在一行输入“输出路径”，并在后面依次输入需要转换的文本
3. 双击`tts.bat`文件运行程序
> **注意事项：** 程序会忽略以"//"开头的文本和空行，“输出路径”所在行是从不被忽略文本开始的第一行
### EXE运行方法
EXE运行方法与BAT运行方式类似，使用EXE运行方法能够自定义输入的文件的文件名
1. 创建输入文件名（此处假设为`xxx.txt`)
2. 在Powershell/cmd中打开程序所在文件夹
3. 输入`./tts xxx.txt`程序