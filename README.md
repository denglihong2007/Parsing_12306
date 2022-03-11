# `Parsing_12306`
## **项目简介：**

将`12306`车次信息转换为`pyETRC/qETRC`的车次文件。

本项目使用`GPLv3`许可证，具体请查看`LICENSE`。

Github链接： https://www.github.com/denglihong2007/Parsing_12306

Gitee链接： https://www.gitee.com/zhupaigu/Parsing_12306

## **直接运行（`Only For Windows`）：**

●前往 https://github.com/denglihong2007/Parsing_12306/releases 或 https://gitee.com/zhupaigu/Parsing_12306/releases 下载exe文件，直接解压运行即可。

## **如何使用源码来运行：**

### **运行依赖库安装：**

●点击[链接](https://github.com/denglihong2007/Parsing_12306/archive/refs/heads/main.zip)下载最新的`releases`。

●解压缩程序文件。

●对于网络不好的用户，请在`Terminal`中运行以下代码来将`pip`软件源更换为清华源。

```shell
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

#### **对于`Windows`用户：**

●双击`setup.bat`安装运行依赖库，静候安装完成。

#### **对于其它`OS`用户（未测试，示例`Python 3.9.10`）：**

●打开终端，参考以下`bat`代码安装运行依赖库。

```shell
pip install requests
cd libs
python-3.9.10.exe
cd Timetable_new-master
python setup.py build
python setup.py sdist
python setup.py install
cd..
cd train_graph-master
python setup.py install
pause
```

### **运行程序：**

●直接打开`Parsing_12306.py`或在终端运行`python Parsing_12306.py`。

## **注意事项**

●感谢`CDK6182CHR`的`train_graph`库和`Timetable_new`库以及本程序的最初版本，没有您就没有本项目！感谢群友“扫同打充办“的宝贵意见，因为您我们才有2.0版本！”

●将车次描述文件导入到`pyETRC/qETRC`时，请务必先调整“最大跨越站数”。

●如有建议或反馈，可以直接新建`issues`或添加`QQ:2638367181`说明。

●如果您觉得此项目帮助到您，请按下`star`，谢谢！

●本程序仅在`Windows 11 and macOS and Linux`平台上测试通过，其它平台请自行测试。

●多规则请使用回车间隔。
