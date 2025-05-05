import re
import requests



def extract_bv_from_url(url):
    """
    从B站视频URL中提取BV号

    参数:
        url (str): B站视频URL（可以是长链或b23.tv短链）

    返回:
        str: 提取到的BV号，如果提取失败则返回None
    """
    # 如果是b23.tv短链，先解析成长链
    if 'b23.tv' in url:
        try:
            # 添加协议头如果缺失
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url

            # 发起HEAD请求获取真实URL（比GET更高效）
            response = requests.head(url, allow_redirects=True, timeout=5)
            url = response.url
        except Exception as e:
            print(f"解析短链失败: {e}")
            return None

    # 使用正则表达式匹配BV号
    # B站BV号格式为 BV + 10位字母数字组合
    bv_pattern = re.compile(r'(BV[0-9A-Za-z]{10})')
    match = bv_pattern.search(url)

    if match:
        return match.group(1)
    else:
        return None


# 测试示例
if __name__ == "__main__":
    test_urls = [
        "https://www.bilibili.com/video/BV1ztSeYxEgp/?share_source=copy_web&vd_source=cdb078b803a73459090c408d9ecbf954",
        "https://b23.tv/O5EBqUR",
        "无效的URL"
    ]

    for url in test_urls:
        bv = extract_bv_from_url(url)
        print(f"URL: {url} -> BV号: {bv}")