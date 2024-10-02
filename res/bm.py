def convert_utf8_to_gbk(input_file, output_file):
    try:
        # 读取文件内容（假设原文件是UTF-8编码）
        with open(input_file, 'r', encoding='utf-8-sig') as file:
            content = file.read()
        
        # 将内容写入到新文件，使用GBK编码
        with open(output_file, 'w', encoding='gbk') as file:
            file.write(content)
        
        print(f"文件已成功从UTF-8转换为GBK编码并保存为 {output_file}")
    
    except Exception as e:
        print(f"发生错误: {e}")

# 设置输入文件和输出文件的路径
input_file = 'DL.bat'
output_file = 'DL_GBK.bat'

# 调用函数进行编码转换
convert_utf8_to_gbk(input_file, output_file)
