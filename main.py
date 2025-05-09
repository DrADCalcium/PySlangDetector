import logging
from pathlib import Path
from tokenizer import Tokenizer
from filter import FilterAPI
from prebuild import main as prebuild
from csv2txt import main as csv2txt
import argparse
import sys
import subprocess
from bv_convertor import extract_bv_from_url as url2bv
from xhs_convertor import extract_xhs_from_url as url2xhs
import shutil
import os
import platform

logger = logging.getLogger()
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('app.log', encoding='utf-8')
file_handler.setLevel(logging.INFO)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - [main] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
def trie_prebuild():
    prebuild()
    logger.info("Trie树构建完成，已保存至：/dic/sensitive_words.trie")

def txt_prebuild():
    csv2txt()

def load_file_lines(file_path):
    if Path(file_path).is_file():
        with open(file_path, 'r', encoding='utf-8') as f:
            return [line.rstrip('\n') for line in f]
    else:
        logger.info(f"文件 {file_path} 不存在")
        sys.exit(1)

def save_file_lines(file_path, lines):
    with open(file_path, 'a+', encoding='utf-8') as f:
        for line in lines:
            f.write(line)

def data_init():
    crawler_data_dir = './MediaCrawler-Modified/data'
    if os.path.exists(crawler_data_dir):
        shutil.rmtree(crawler_data_dir)
    data_dir = 'data'
    if os.path.exists(data_dir):
        shutil.rmtree(data_dir)
    os.makedirs(data_dir)
    logger.info('程序初始化...')


def args_decode(args):
    current_dir = Path(__file__).parent.absolute()
    crawler_dir = current_dir / "MediaCrawler-Modified"

    if args.prebuild:
        trie_prebuild()
        sys.exit(0)

    if args.platform == 'bili' and args.url:
        logger.info("正在抓取B站数据...")
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
            logger.info("B站数据抓取完成")
        except subprocess.CalledProcessError as e:
            logger.error(f"执行出错: {e}")
            sys.exit(1)

    elif args.platform == 'xhs' and args.url:
        logger.info("正在抓取小红书数据...")
        xhs_id, xsec_token = url2xhs(args.url)
        cmd = [
            'python',
            'main.py',
            '--platform', 'xhs',
            '--type', 'detail',
            '--get_comment', 't',
            '--get_sub_comment', 't',
            '--save_data_option', 'csv',
            '--xhs_url', f'https://www.xiaohongshu.com/discovery/item/{xhs_id}?xsec_token={xsec_token}',
            '--headless', 't'
        ]

        try:
            subprocess.run(cmd, check=True, cwd=str(crawler_dir))
            logger.info("小红书数据抓取完成")
        except subprocess.CalledProcessError as e:
            logger.error(f"执行出错: {e}")
            sys.exit(1)

    elif args.platform == 'wb' and args.url:
        logger.info("正在抓取微博数据...")
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
            logger.info("微博数据抓取完成")
        except subprocess.CalledProcessError as e:
            logger.error(f"执行出错: {e}")
            sys.exit(1)

    elif args.platform is None:
        cmd = [
            'python',
            './main.py',
            '--help'
        ]
        subprocess.run(cmd, check=True)
        logger.info("无参数输入，程序退出")
        sys.exit(0)

    elif args.platform and args.login:
        logger.info(f'正在登录{args.platform}平台...')
        cmd = [
            'python',
            'main.py',
            '--platform', args.platform,
            '--lt', 'qrcode'
        ]
        result = subprocess.run(cmd, check=True, cwd=str(crawler_dir), capture_output=True, text=True)
        logger.info(result.stdout)
        print(result.stdout)
        if result.stderr:
            logger.error(result.stderr)
            print(result.stderr)
        sys.exit(0)

    else:
        logger.info('请指定有效的参数')
        sys.exit(1)


if __name__ == '__main__':

    data_init()

    parser = argparse.ArgumentParser(
        description='基于文本内容安全的社交媒体敏感词检测系统 by Edgar \nPS：首次运行前请先预处理词库，并登录想要检测的社交媒体平台\nPPS：在传入小红书URL时，由于命令行特性，请只保留推文ID和xsec_token，移动端URL短链可自动处理。',
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--prebuild', action='store_true', help='预处理敏感词库，构建Trie树，处理后退出')
    parser.add_argument('--platform', type=str, help='指定目标平台为B站、小红书或微博 { bili | xhs | wb }')
    parser.add_argument('--url', type=str, help='视频或推文链接')
    parser.add_argument('--login', action='store_true', help='弹出浏览器窗口以登录对应平台')
    parser.add_argument('--show', action='store_true', help='检测结束后通过默认文本编辑器打开结果')

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
            save_file_lines('data/sensitive_contents.txt', [line + '\n'])
            count = count + 1

    if count:
        logger.info(f"检测到敏感词，共发现 {count} 条敏感内容")
        logger.info("敏感内容已保存至 data/sensitive_contents.txt")

        if args.show:
            system = platform.system()
            file_path = 'data/sensitive_contents.txt'
            full_path = Path(file_path).resolve()
            if system == "Windows":
                os.startfile(str(full_path))
                logger.info("已通过默认文本编辑器打开敏感文本文件")
            elif system == "Darwin":  # macOS
                subprocess.run(["open", str(full_path)])
                logger.info("已通过默认文本编辑器打开敏感文本文件")
            else:  # Linux 和其他类Unix系统
                subprocess.run(["xdg-open", str(full_path)])
                logger.info("已通过默认文本编辑器打开敏感文本文件")

    else:
        logger.info("没有检测到敏感内容，程序退出")
        sys.exit(0)



