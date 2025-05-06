![title.png](.\static\title.png "title")

 

# PySlangDetector

---

*小孩子不可以在网上说藏话，不懂事说着玩也不可以哦。*

一个用于检测社交媒体推文以及评论区内容中是否包含指定词汇（如敏感词）的工具，基于 Python 3.12开发，支持的社交媒体平台有 Bilibili 、小红书和微博。使用时可以直接在终端运行，也可以使用基于 tkinter 开发的 GUI ，或是自行打包成可执行文件运行。

---

## Announcement

本项目（以下简称“本项目”）是作为一个技术研究与学习工具而创建的，旨在探索和学习网络数据采集技术。本项目专注于自媒体平台的文本内容检测研究，旨在提供给学习者和研究者作为技术交流之用。

本项目开发者（以下简称“开发者”）郑重提醒用户在下载、安装和使用本项目时，严格遵守中华人民共和国相关法律法规，包括但不限于《中华人民共和国网络安全法》、《中华人民共和国反间谍法》等所有适用的国家法律和政策。用户应自行承担一切因使用本项目而可能引起的法律责任。

本项目严禁用于任何非法目的或非学习、非研究的商业行为。本项目不得用于任何形式的非法侵入他人计算机系统，不得用于任何侵犯他人知识产权或其他合法权益的行为。用户应保证其使用本项目的目的纯属个人学习和技术研究，不得用于任何形式的非法活动。

开发者已尽最大努力确保本项目的正当性及安全性，但不对用户使用本项目可能引起的任何形式的直接或间接损失承担责任。包括但不限于由于使用本项目而导致的任何数据丢失、设备损坏、法律诉讼等。

关于本项目的最终解释权归开发者所有。开发者保留随时更改或更新本免责声明的权利，恕不另行通知。

---

## Installation

### 下载源码

可以直接在项目页面右上角处下载，下载后解压即可。

```
Code > Download ZIP
```

或是直接在终端使用 `git` 命令克隆仓库（需要提前安装好 git ）。

```bash
git clone --depth=1 https://github.com/DrADCalcium/PySlangDetector.git
```

### 准备环境

#### 使用全局环境

安装好Python 3.12及以上版本后，打开系统的终端或命令行，使用 `cd` 命令进入项目目录（Windows系统下使用cmd为 `dir` ），执行 `pip` 安装所需的外部库。如果网络环境无法正常安装，可以指定国内镜像源。

```bash
cd /path/to/project
# cmd进入项目目录
dir /path/to/project

# pip安装外部依赖库
pip install -r requirements.txt
# 下载较慢或超时，可以使用下方镜像源
# 阿里源
pip install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt
# 清华tuna源
pip install -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple -r requirements.txt
```

外部库安装完毕后，还需要手动安装 playwright 。如果网络环境无法正常安装，可以指定国内镜像源。

```bash
playwright install
# 下载较慢或超时，可以使用下方镜像源
# 阿里源
playwright install -i https://mirrors.aliyun.com/pypi/simple/
# 清华tuna源
playwright install -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
```

Windows下 playwright 默认安装地址如下：

```bash
%USERPROFILE%\AppData\Local\ms-playwright
```

#### 使用虚拟环境（推荐）

安装好 Python 3.12 及以上版本后，打开系统的终端或命令行，使用 `cd` 命令进入项目目录（Windows 系统下使用 cmd 为 `dir` ），使用 Python 命令创建 venv 虚拟环境，激活虚拟环境，然后执行 `pip` 安装所需的外部库。外部库安装完毕后，还需要手动安装 playwright 。如果网络环境无法正常安装，可以指定国内镜像源。

```bash
cd /path/to/project
# cmd进入项目目录
dir /path/to/project

# 创建虚拟环境
python -m venv venv

# Linux / macOS / 类Unix系统激活虚拟环境
source venv/bin/activate

# Windows系统激活虚拟环境
venv\Scripts\activate

# pip安装外部依赖库
pip install -r requirements.txt
# 下载较慢或超时，可以使用下方镜像源
# 阿里源
pip install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt
# 清华tuna源
pip install -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple -r requirements.txt

# 安装playwright
playwright install
# 下载较慢或超时，可以使用下方镜像源
# 阿里源
playwright install -i https://mirrors.aliyun.com/pypi/simple/
# 清华tuna源
playwright install -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
```

---

## Usage

### 词库准备

*由于某些原因，项目不提供现成的敏感词库，请自行准备。*

将想要过滤的词按照每个单独一行的格式存储在 txt 文件内，可保存多个 txt 文件，并移动到项目目录中的 `dic/raw` 文件夹内，程序在词库预处理时会收集文件夹内的所有 txt 文件。文件夹内有 `example.txt` 作为示例文档，可以随意修改使用。

预处理好的词库使用 Trie 树数据结构存储在项目目录内的 `dic` 文件夹中，如需修改可直接对 `dic/raw` 内的 txt 进行修改，然后重新生成词库即可。文档下方将介绍如何预处理词库。

### 使用命令

打开系统的终端或命令行，使用 `cd` 命令进入项目目录（Windows 系统下使用 cmd 为 `dir` ），使用 Python 命令运行 `main.py` ，可得到运行参数帮助。

```bash
python main.py
#也可添加参数 -h 或 --help
python main.py -h
python main.py --help
```

终端会输出如下提示信息：

```echo
usage: main.py [-h] [--prebuild] [--platform PLATFORM] [--url URL] [--login] [--show]

基于文本内容安全的社交媒体敏感词检测系统 by Edgar
PS：首次运行前请先预处理词库，并登录想要检测的社交媒体平台。
PPS：在传入小红书URL时，由于命令行特性，请只保留推文ID和xsec_token，移动端URL短链可自动处理。

options:
  -h, --help           show this help message and exit
  --prebuild           预处理敏感词库，构建Trie树，处理后退出
  --platform PLATFORM  指定目标平台为B站、小红书或微博 { bili | xhs | wb }
  --url URL            视频或推文链接
  --login              弹出浏览器窗口以登录对应平台
  --show               检测结束后通过默认文本编辑器打开结果
```

按照提示信息传入参数即可。

由于诸多平台默认的长链接 URL 带有较多参数，而未经编码的 URL 参数间使用的 `&` 连接符会被终端处理成并行指令，所以在传入长链接时请手动删除多余参数，如 `https://www.platform.com/item/ABC123def`  （小红书平台请保留 `xsec_token` 参数，修改为 `https://www.xiaohongshu.com/explore/123456?xsec_token=ABC-def-789=` 的形式）。移动端所使用的短链接无需处理。

**如果是首次使用请先预处理词库，并登录想要检测的社交媒体平台。**

```bash
# 预处理词库
python main.py --prebuild

# 登录社交媒体平台账户（如B站）
python main.py --platform bili --login

# 检测指定URL页面的社交媒体文本内容（如B站视频 BV123abcDEF 的视频简介和评论区
python main.py --platform bili --url https://www.bilibili.com/BV123abcDEF
```

### 使用GUI

#### 直接运行

打开系统的终端或命令行，使用 `cd` 命令进入项目目录（Windows 系统下使用 cmd 为 `dir` ），使用 Python 命令运行 `GUI.py` ，即可打开图形用户界面。

![gui_example.png](.\static\gui_example.png "gui_example")

#### 打包后运行（未测试）

打开系统的终端或命令行，使用 `cd` 命令进入项目目录（Windows 系统下使用 cmd 为 `dir` ）。可以使用 pyinstaller 对 `GUI.py` 打包成可执行文件后运行。由于未测试具体运行环境，所以不推荐打包后脱离项目源码。

---

## Results

输出结果可在项目 `data` 目录下找到，其中 `contents.txt` 为未过滤文本内容，`sensitive_contents.txt` 为过滤后包含敏感信息的文本内容，两个文件中每条文本独立成行。在命令运行或GUI运行时选择展示结果，会在主程序检测完毕后使用操作系统默认的文本编辑器打开 `sensitive_contents.txt` 。

---

## Acknowledgement

本项目使用的爬虫部分为开源项目 [NanmiCoder](https://github.com/NanmiCoder) / [MediaCrawler](https://github.com/NanmiCoder/MediaCrawler) 修改而成。

> ~~谢谢他的项目减少了我很多的毕设工作量。~~~~简中互联网使用环境懂得都懂，平台不开放而且反爬机制肥肠滴先进。QwQ本科毕设只做爬虫的工作量其实就够了。~~

本项目开发基于 Python 3.12 及有关的外部库。

本项目使用 JetBrains 开发的 PyCharm IDE 编写。

~~本项目莫名其妙由 systemd 驱动~~ 假的，我拿Windows开发的（笑 

~~（（那我是不是还得感谢微软最近几个Windows累计更新没有让我电脑蓝屏~~


