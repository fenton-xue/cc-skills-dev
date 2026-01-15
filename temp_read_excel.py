#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import sys

try:
    # 读取Excel文件，前26行，不设置header以便看到原始数据
    df = pd.read_excel('测试用例me#71489 新增并单、合并清关、拆分清关功能.xlsx', nrows=26, header=None)

    print(f'总行数: {len(df)}, 总列数: {len(df.columns)}')
    print('\n列名:', df.iloc[0].tolist())

    print('\n=== 第1-26行数据（所有列）===')
    for idx in range(len(df)):
        print(f'\n行{idx}:')
        for col_idx in range(len(df.columns)):
            val = df.iloc[idx, col_idx]
            if pd.notna(val):
                val_str = str(val)[:80]  # 限制长度
                print(f'  列{col_idx}: {val_str}')

except Exception as e:
    print(f'错误: {e}', file=sys.stderr)
    import traceback
    traceback.print_exc()
    sys.exit(1)
