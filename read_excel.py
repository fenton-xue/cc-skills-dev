import pandas as pd
import sys

# 读取测试用例
file_path = sys.argv[1]
output_file = sys.argv[2]

df = pd.read_excel(file_path)

with open(output_file, 'w', encoding='utf-8') as f:
    f.write('=== 列名 ===\n')
    f.write(str(df.columns.tolist()))
    f.write('\n\n')

    f.write('=== 数据形状 ===\n')
    f.write(f'行数: {df.shape[0]}, 列数: {df.shape[1]}\n\n')

    f.write('=== 前20行数据 ===\n')
    f.write(df.head(20).to_string())
    f.write('\n\n')

    f.write('=== 数据类型 ===\n')
    f.write(str(df.dtypes))
    f.write('\n\n')

    f.write('=== 所有数据 ===\n')
    f.write(df.to_string())
