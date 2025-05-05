from urllib.parse import urlparse, parse_qs
import requests

def extract_xhs_from_url(url):
    """
    从小红书URL中提取推文ID和xsec_token
    参数:
            url (str): 小红书URL（可以是长链或xhslink短链）
    返回:
            str: 提取到的推文ID和xsec_token，如果提取失败则返回None
    """
    # 如果是xhslink短链，先解析成长链
    if 'xhslink.com' in url:
        try:
            # 添加协议头如果缺失
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url

            # 发起HEAD请求获取真实URL（比GET更高效）
            response = requests.head(url, allow_redirects=True, timeout=5)
            url = response.url
            print(f"解析短链成功，真实URL为: {url}")

        except Exception as e:
            print(f"解析短链失败: {e}")
            return None

    # 使用正则表达式匹配推文ID和xsec_token
    # 推文ID格式为item/后的一串数字
    # xsec_token可以直接在长链中解析到

    # 拆解 URL
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)  # 解析查询参数

    # 提取推文ID（直接从路径中提取）
    tweet_id = parsed_url.path.split("/item/")[-1].split("?")[0]
    #print("推文ID:", tweet_id)  # 输出: 1234567890

    # 提取 xsec_token（从查询参数中获取）
    xsec_token = query_params.get("xsec_token", [None])[0]
    #print("xsec_token:", xsec_token)  # 输出: abc123-def_456

    if tweet_id and xsec_token:
        return tweet_id, xsec_token
    else:
        return None, None


#测试实例
if __name__ == '__main__':
    test_urls = ['http://xhslink.com/a/XIbCDRUzFiObb',
                 'https://www.xiaohongshu.com/discovery/item/6807a827000000001202c7c0?app_platform=ios&app_version=8.81.2&share_from_user_hidden=true&xsec_source=app_share&type=normal&xsec_token=CB8CE-Xn4JgewHBHkqI6z_cWQ-iOIJl1bXZtAWx19DAR4=&author_share=1&xhsshare=CopyLink&shareRedId=OD4yNztGOko2NzUyOTgwNjZEOTpJO0dK&apptime=1746436889&share_id=384f4fe9981347a9891e3dc7d48722f9']

    for url in test_urls:
        xhs_id, xsec_token = extract_xhs_from_url(url)
        if xhs_id and xsec_token:
            print(f"推文ID: {xhs_id}")
            print(f"xsec_token: {xsec_token}")
        else:
            print("推文ID或xsec_token提取失败")