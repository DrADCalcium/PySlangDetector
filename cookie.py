import json
from selenium import webdriver
#from selenium.webdriver.firefox.service import Service
from typing import Optional, List, Dict
import time

#等待登录时间（默认15秒）
sleep_time = 15

class CookieManager :
    def __init__(self,
                 #driver_path: str
                 ):
        """
        初始化 Firefox Cookie 管理器
        param driver_path: GeckoDriver 路径（如 "geckodriver.exe"）
        """
        self.driver = webdriver.Firefox(
            #service=Service(driver_path)
        )

    def save_cookies(self, url: str, cookie_file: str) -> bool:
        """
        访问网站并保存 Cookies 到 JSON 文件
        :param url: 目标网站 URL（如 "https://example.com"）
        :param cookie_file: Cookie 存储路径（如 "cookies.json"）
        :return: 是否保存成功
        """
        try:
            self.driver.get(url)
            self.driver.maximize_window()
            time.sleep(sleep_time)
            self.driver.refresh()
            cookies = self.driver.get_cookies()
            with open(cookie_file, 'w') as f:
                json.dump(cookies, f)
            return True
        except Exception as e:
            print(f"[ERROR] 保存 Cookie 失败: {e}")
            return False

    def load_cookies(self, url: str, cookie_file: str):
        """
        加载 Cookies 并访问网站（需先访问目标域名）
        :param url: 必须与 Cookie 的域名一致（如 "https://example.com"）
        :param cookie_file: Cookie 文件路径
        :return: 是否加载成功
        """
        try:
            self.driver.get(url)  # 先访问域名才能加载 Cookie
            with open(cookie_file, 'r') as f:
                cookies: List[Dict] = json.load(f)
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.refresh()  # 刷新使 Cookie 生效
        except Exception as e:
            print(f"[ERROR] 加载 Cookie 失败: {e}")

        return self.driver

    def close(self):
        """关闭浏览器"""
        self.driver.quit()

if __name__ == "__main__":
    cookie = CookieManager()
    cookie.load_cookies("https://www.xiaohongshu.com/explore", "./cookies/xhs_cookie.json")
    time.sleep(5)
    cookie.close()
