import sys

def read_and_print(file_path):
    try:
        # 以 UTF-8 格式打开文件
        with open(file_path, 'r', encoding='utf-16') as f:
            content = f.read()
            print("📄 文件内容如下：")
            print("-" * 20)
            for line_num, line in enumerate(content.splitlines(), 1):
                print(f"{line_num}: {line}")
            print("-" * 20)
    except FileNotFoundError:
        print(f"❌ 报错啦！找不到文件：{file_path}")
    except Exception as e:
        print(f"❌ 未知错误：{e}")

if __name__ == "__main__":
    # 从命令行获取参数
    if len(sys.argv) < 2:
        print("用法: python read_file.py <文件路径>")
        print("示例: python read_file.py sample.txt")
    else:
        read_and_print(sys.argv[1])