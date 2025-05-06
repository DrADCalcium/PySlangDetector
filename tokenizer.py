# tokenizer.py
import logging

import jieba
import re
from typing import List


class Tokenizer:
    def __init__(self, custom_dict_path: str = None):
        """
        初始化分词器
        :param custom_dict_path: 自定义词典路径（可选）
        """
        self._init_jieba(custom_dict_path)

    def _init_jieba(self, custom_dict_path):
        """初始化jieba分词配置"""
        jieba.setLogLevel(logging.CRITICAL)
        jieba.initialize()
        if custom_dict_path:
            jieba.load_userdict(custom_dict_path)

        # 添加默认英文处理规则
        self.eng_pattern = re.compile(r'[a-zA-Z0-9_]+')

    def tokenize(self, text: str,
                 mode: str = 'accurate') -> List[str]:
        """
        执行分词操作
        :param text: 输入文本
        :param mode: 分词模式（accurate/全模式）
        :return: 分词结果列表
        """
        # 预处理：分离中英文
        segments = []
        last_end = 0

        for match in self.eng_pattern.finditer(text):
            start, end = match.span()
            if start > last_end:
                chinese_part = text[last_end:start]
                segments.extend(self._cut_chinese(chinese_part, mode))
            segments.append(match.group())
            last_end = end

        if last_end < len(text):
            chinese_part = text[last_end:]
            segments.extend(self._cut_chinese(chinese_part, mode))

        return [token for token in segments if token.strip()]

    def _cut_chinese(self, text: str, mode: str) -> List[str]:
        """中文部分分词"""
        if mode == 'accurate':
            return jieba.lcut(text, cut_all=False)
        elif mode == 'full':
            return jieba.lcut(text, cut_all=True)
        raise ValueError("Invalid mode. Use 'accurate' or 'full'")


# GUI接口预留
class TokenizerAPI:
    @staticmethod
    def create_tokenizer(custom_dict=None):
        """创建分词器实例（GUI调用入口）"""
        return Tokenizer(custom_dict)

    @staticmethod
    def tokenize_text(text, tokenizer, mode='accurate'):
        """执行分词操作（GUI调用入口）"""
        return tokenizer.tokenize(text, mode)


if __name__ == '__main__':
    # Sample
    tokenizer = Tokenizer()
    sample_text = "我爱Python编程和信息安全"
    print(tokenizer.tokenize(sample_text))
    # 输出: ['我', '爱', 'Python', '编程', '和', '深度学习', 'deeplearning']