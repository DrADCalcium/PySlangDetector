import subprocess
from pathlib import Path
import threading

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
    def start_main(self,evt):
        input_url = self.ui.get_input_url()
        selected_platform = self.ui.get_selected_platform()
        show_result = self.ui.get_show_result_checkbox_state()

        if input_url and selected_platform == "bili":

            cmd = [
                'python',
                'main.py',
                '--platform', 'bili',
                '--url', str(input_url),
                *(['--show'] if show_result else [])
            ]
            threading.Thread(target=subprocess.run, args=(cmd,)).start()

        elif input_url and selected_platform == "xhs":

            cmd = [
                'python',
                'main.py',
                '--platform', 'xhs',
                '--url', str(input_url),
                *(['--show'] if show_result else [])
            ]
            threading.Thread(target=subprocess.run, args=(cmd,)).start()

        elif input_url and selected_platform == "wb":

            cmd = [
                'python',
                'main.py',
                '--platform', 'wb',
                '--url', str(input_url),
                *(['--show'] if show_result else [])
            ]
            threading.Thread(target=subprocess.run, args=(cmd,)).start()

        elif not input_url :
            print('请输入URL')
        elif not selected_platform:
            print('请选择平台')

        #elif 'http' not in input_url:
        #    print('请输入有效的URL')

    def init_trie(self,evt):
        from main import trie_prebuild
        trie_prebuild()
    def browser_login_bilibili(self,evt):
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
        current_dir = Path(__file__).parent.absolute()
        crawler_dir = current_dir / "MediaCrawler-Modified"
        cmd = [
            'python',
            'main.py',
            '--platform', 'wb',
            '--lt', 'qrcode'
        ]
        threading.Thread(target=subprocess.run, args=(cmd,), kwargs={'cwd': str(crawler_dir)}).start()
