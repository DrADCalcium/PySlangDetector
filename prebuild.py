import os
import glob
import pygtrie
import pickle


def load_sensitive_words(dic_dir):
    """加载敏感词目录下的所有txt文件"""
    trie = pygtrie.CharTrie()
    txt_files = glob.glob(os.path.join(dic_dir, "*.txt"))

    for file_path in txt_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                word = line.strip()
                if word:
                    trie[word] = True  # 使用True作为占位值
    return trie


def build_trie(output_file):
    """构建并保存Trie树"""
    dic_dir = os.path.join(os.path.dirname(__file__), "dic/raw")
    trie = load_sensitive_words(dic_dir)

    with open(output_file, 'wb') as f:
        pickle.dump(trie, f, protocol=pickle.HIGHEST_PROTOCOL)
    return True


def main():
    output_path = os.path.join(os.path.dirname(__file__), "./dic/sensitive_words.trie")
    build_trie(output_path)
    print(f"Trie树构建完成，已保存至：{output_path}")

if __name__ == "__main__":

    print("\n=== 开始Trie树测试 ===")
    test_words = [
        "bad",
        "ban",
        "badminton",
        "你好",
        "您好",
        "你好吗"
    ]
    test_trie = pygtrie.CharTrie()
    for word in test_words:
        test_trie[word] = True

    test_output_path = os.path.join(os.path.dirname(__file__), "./dic/test_words.trie")
    with open(test_output_path, 'wb') as f:
        pickle.dump(test_trie, f, protocol=pickle.HIGHEST_PROTOCOL)
    print(f"测试Trie树已保存至：{test_output_path}")

    with open(test_output_path, 'rb') as f:
        loaded_trie = pickle.load(f)

    print("\nTrie树内容:")
    for word in test_words:
        print(f"单词 '{word}' 存在于Trie树中: {'是' if word in loaded_trie else '否'}")