import subprocess
from pathlib import Path
import threading
import logging


class Controller:
    # 导入UI类后，替换以下的 object 类型，将获得 IDE 属性提示功能
    ui: object
    def __init__(self):
        self.win = None
    def init(self, ui):
        """
        得到UI实例，对组件进行初始化配置
        """
        self.ui = ui
        # TODO 组件初始化 赋值操作
        logging.basicConfig(
            filename='app.log',  # 日志文件名
            level=logging.INFO,  # 日志级别
            format='%(asctime)s - %(levelname)s - [GUI] %(message)s',  # 日志格式
            datefmt='%Y-%m-%d %H:%M:%S',
            encoding='utf-8'
        )

        #控制台日志输出
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - [control] %(message)s')
        console_handler.setFormatter(formatter)
        logging.getLogger().addHandler(console_handler)

    def start_main(self,evt):
        input_url = self.ui.get_input_url()
        selected_platform = self.ui.get_selected_platform()
        show_result = self.ui.get_show_result_checkbox_state()

        if input_url and selected_platform == "bili":
            logging.info(f"开始处理B站URL: {input_url}")
            cmd = [
                'python',
                'main.py',
                '--platform', 'bili',
                '--url', str(input_url),
                *(['--show'] if show_result else [])
            ]
            threading.Thread(target=subprocess.run, args=(cmd,)).start()

        elif input_url and selected_platform == "xhs":
            logging.info(f"开始处理小红书URL: {input_url}")
            cmd = [
                'python',
                'main.py',
                '--platform', 'xhs',
                '--url', str(input_url),
                *(['--show'] if show_result else [])
            ]
            threading.Thread(target=subprocess.run, args=(cmd,)).start()

        elif input_url and selected_platform == "wb":
            logging.info(f"开始处理微博URL: {input_url}")
            cmd = [
                'python',
                'main.py',
                '--platform', 'wb',
                '--url', str(input_url),
                *(['--show'] if show_result else [])
            ]
            threading.Thread(target=subprocess.run, args=(cmd,)).start()

        elif not input_url :
            logging.warning("未输入URL")

        elif not selected_platform:
            logging.warning("未选择平台")


        #elif 'http' not in input_url:
        #    print('请输入有效的URL')

    def init_trie(self,evt):
        logging.info("开始构建Trie树")
        from main import trie_prebuild
        trie_prebuild()
        logging.info("Trie树构建完成")
    def browser_login_bilibili(self,evt):
        logging.info("开始B站登录")
        current_dir = Path(__file__).parent.absolute()
        crawler_dir = current_dir / "MediaCrawler-Modified"
        cmd = [
            'python',
            'main.py',
            '--platform', 'bili',
            '--lt', 'qrcode'
        ]
        threading.Thread(target=subprocess.run, args=(cmd,), kwargs={'cwd': str(crawler_dir)}).start()
    def browser_login_xhs(self,evt):
        logging.info("开始小红书登录")
        current_dir = Path(__file__).parent.absolute()
        crawler_dir = current_dir / "MediaCrawler-Modified"
        cmd = [
            'python',
            'main.py',
            '--platform', 'xhs',
            '--lt', 'qrcode'
        ]
        threading.Thread(target=subprocess.run, args=(cmd,), kwargs={'cwd': str(crawler_dir)}).start()

    def browser_login_wb(self,evt):
        logging.info("开始微博登录")
        current_dir = Path(__file__).parent.absolute()
        crawler_dir = current_dir / "MediaCrawler-Modified"
        cmd = [
            'python',
            'main.py',
            '--platform', 'wb',
            '--lt', 'qrcode'
        ]
        threading.Thread(target=subprocess.run, args=(cmd,), kwargs={'cwd': str(crawler_dir)}).start()
