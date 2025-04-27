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
    dic_dir = os.path.join(os.path.dirname(__file__), "dic")
    trie = load_sensitive_words(dic_dir)

    with open(output_file, 'wb') as f:
        pickle.dump(trie, f, protocol=pickle.HIGHEST_PROTOCOL)
    return True


if __name__ == "__main__":
    output_path = os.path.join(os.path.dirname(__file__), "./data/sensitive_words.trie")
    build_trie(output_path)
    print(f"Trie树构建完成，已保存至：{output_path}")