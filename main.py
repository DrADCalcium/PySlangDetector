from pathlib import Path
from tokenizer import Tokenizer
from filter import FilterAPI
from prebuild import main as prebuild
from csv2txt import main as csv2txt
import argparse
import sys
import subprocess
from bv_convertor import extract_bv_from_url as url2bv
import shutil
import os
import platform
import glob

def trie_prebuild():
    prebuild()

def txt_prebuild():
    csv2txt()

def load_file_lines(file_path):
    if Path(file_path).is_file():
        with open(file_path, 'r', encoding='utf-8') as f:
            return [line.rstrip('\n') for line in f]
    else:
        print(f"文件 {file_path} 不存在")
        sys.exit(1)

def save_file_lines(file_path, lines):
    with open(file_path, 'a+', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')

def data_init():
    crawler_data_dir = './MediaCrawler-Modified/data'
    if os.path.exists(crawler_data_dir):
        shutil.rmtree(crawler_data_dir)
    data_dir = 'data'
    if os.path.exists(data_dir):
        shutil.rmtree(data_dir)
    os.makedirs(data_dir)

def args_decode(args):
    current_dir = Path(__file__).parent.absolute()
    crawler_dir = current_dir / "MediaCrawler-Modified"

    if args.prebuild:
        trie_prebuild()
        sys.exit(0)

    if args.platform == 'bili' and args.url:
        cmd = [
            'python',
            'main.py',
            '--platform', 'bili',
            '--type', 'detail',
            '--get_comment', 't',
            '--get_sub_comment', 't',
            '--save_data_option', 'csv',
            '--bv', url2bv(args.url),  # 从URL提取bv号
            '--headless', 't'
        ]

        # 执行爬虫脚本
        try:
            subprocess.run(cmd, check=True, cwd=str(crawler_dir))
            print("B站数据抓取完成")
        except subprocess.CalledProcessError as e:
            print(f"执行出错: {e}")
            sys.exit(1)

    elif args.platform == 'xhs' and args.url:
        cmd = [
            'python',
            'main.py',
            '--platform', 'xhs',
            '--type', 'detail',
            '--get_comment', 't',
            '--get_sub_comment', 't',
            '--save_data_option', 'csv',
            '--xhs_url', args.url,
            '--headless', 't'
        ]

        try:
            subprocess.run(cmd, check=True, cwd=str(crawler_dir))
            print("小红书数据抓取完成")
        except subprocess.CalledProcessError as e:
            print(f"执行出错: {e}")
            sys.exit(1)

    elif args.platform == 'wb' and args.url:
        cmd = [
            'python',
            'main.py',
            '--platform', 'wb',
            '--type', 'detail',
            '--get_comment', 't',
            '--get_sub_comment', 't',
            '--save_data_option', 'csv',
            '--wb_url', args.url,
            '--headless', 't'
        ]

        try:
            subprocess.run(cmd, check=True, cwd=str(crawler_dir))
            print("微博数据抓取完成")
        except subprocess.CalledProcessError as e:
            print(f"执行出错: {e}")
            sys.exit(1)

    elif args.platform is None:
        cmd = [
            'python',
            './main.py',
            '--help'
        ]
        subprocess.run(cmd, check=True)
        sys.exit(0)

    elif args.platform and args.login:
        cmd = [
            'python',
            'main.py',
            '--platform', args.platform,
            '--lt', 'qrcode'
        ]
        subprocess.run(cmd, cwd=str(crawler_dir))
        sys.exit(0)

    else:
        print('请指定有效的平台')
        sys.exit(1)


if __name__ == '__main__':
    data_init()

    parser = argparse.ArgumentParser(description='基于文本内容安全的社交媒体敏感词检测系统 by Edgar')
    parser.add_argument('--prebuild', action='store_true', help='预处理敏感词库，构建Trie树，处理后退出')
    parser.add_argument('--platform', type=str, help='指定目标平台 { bili | xhs | wb }')
    parser.add_argument('--url', type=str, help='视频或推文链接')
    parser.add_argument('--login', action='store_true', help='弹出浏览器登录对应平台')

    args = parser.parse_args()
    args_decode(args)
    txt_prebuild()

    tokenizer = Tokenizer()
    filter_instance = FilterAPI.create_filter("./dic/sensitive_words.trie")
    count = 0
    for line in load_file_lines('data/contents.txt'):
        words =  tokenizer.tokenize(line)
        is_sensitive =  FilterAPI.check_sensitive(filter_instance, words)
        if is_sensitive:
            save_file_lines('data/sensitive_contents.txt', line)
            count = count + 1

    if count:
        print(f"检测到敏感词，共发现 {count} 条敏感内容")
        print("敏感内容已保存至 data/sensitive_contents.txt")
        system = platform.system()
        if system == "Windows":
            os.startfile('data/sensitive_contents.txt')
        elif system == "Darwin":  # macOS
            subprocess.run(["open", 'data/sensitive_contents.txt'])
        else:  # Linux 和其他类Unix系统
            subprocess.run(["xdg-open", 'data/sensitive_contents.txt'])

    else:
        print("没有检测到敏感内容，程序退出")
        sys.exit(0)



