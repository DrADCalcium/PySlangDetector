import csv


def extract_column_to_txt(csv_file, column_name, output_file):
    """
    从CSV文件中提取指定列数据并写入TXT文件，每个单元格内容单独一行

    参数:
        csv_file (str): 输入CSV文件路径
        column_name (str): 要提取的列名
        output_file (str): 输出TXT文件路径

    返回:
        int: 写入的行数
    """
    try:
        with open(csv_file, mode='r', encoding='utf-8') as csv_input, \
                open(output_file, mode='w', encoding='utf-8') as txt_output:

            # 读取CSV文件
            csv_reader = csv.DictReader(csv_input)

            # 检查列名是否存在
            if column_name not in csv_reader.fieldnames:
                raise ValueError(f"列名 '{column_name}' 不存在于CSV文件中")

            line_count = 0
            for row in csv_reader:
                # 获取指定列的值并写入TXT文件
                cell_value = row[column_name]
                txt_output.write(f"{cell_value}\n")
                line_count += 1

            return line_count

    except FileNotFoundError:
        raise FileNotFoundError(f"文件 {csv_file} 不存在")
    except Exception as e:
        raise Exception(f"处理文件时出错: {str(e)}")


# 使用示例
if __name__ == "__main__":
    # 示例用法
    input_csv = "./data/comments.csv"  # 替换为你的CSV文件路径
    output_txt = "./data/comments.txt"  # 替换为你想保存的TXT文件路径
    column_to_extract = "email"  # 替换为你想提取的列名

    try:
        count = extract_column_to_txt(input_csv, column_to_extract, output_txt)
        print(f"成功提取 {count} 行数据到 {output_txt}")
    except Exception as e:
        print(f"错误: {str(e)}")