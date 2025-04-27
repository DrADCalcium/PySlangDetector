# filter.py

import pickle
from typing import List

import pygtrie


class SensitiveFilter:
    def __init__(self, trie: pygtrie.CharTrie):
        """
        初始化过滤器
        :param trie: 预加载的Trie树（要求线程安全）
        """
        self.trie = trie  # pygtrie的CharTrie本身是线程安全的只读结构

    @staticmethod
    def load_trie(trie_path: str) -> pygtrie.CharTrie:
        """加载预生成的Trie树（独立方法方便GUI调用）"""
        with open(trie_path, 'rb') as f:
            return pickle.load(f)

    def contains_sensitive(self, tokens: List[str]) -> bool:
        """
        线程安全的敏感词检测方法
        :param tokens: 分词后的token列表
        :return: 存在敏感词返回True，否则False
        """
        return any(token in self.trie for token in tokens)

    # 以下是支持多线程操作的扩展方法
    def batch_check(self, tokens_list: List[List[str]]) -> List[bool]:
        """批量检测接口（适用于多线程处理）"""
        return [self.contains_sensitive(tokens) for tokens in tokens_list]

# GUI接口层
class FilterAPI:
    @staticmethod
    def create_filter(trie_path: str):
        """创建过滤器实例（主线程调用）"""
        trie = SensitiveFilter.load_trie(trie_path)
        return SensitiveFilter(trie)

    @staticmethod
    def check_sensitive(filter_obj: SensitiveFilter, tokens: List[str]) -> bool:
        """执行检测（多线程安全）"""
        return filter_obj.contains_sensitive(tokens)

    @staticmethod
    def batch_check(filter_obj: SensitiveFilter, tokens_list: List[List[str]]) -> List[bool]:
        """批量检测（多线程安全）"""
        return filter_obj.batch_check(tokens_list)

if __name__ == "__main__":
    # 初始化
    trie = pygtrie.CharTrie()
    trie["敏感词"] = True
    filter = SensitiveFilter(trie)

    # Sample
    print(filter.contains_sensitive(["正常", "文本"]))  # False
    print(filter.contains_sensitive(["包含", "敏感词"]))  # True