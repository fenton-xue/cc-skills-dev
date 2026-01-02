#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
生成测试用例Excel文件脚本
用于gen-test-case skill
"""

import json
import xlsxwriter
import sys

def generate_testcase_excel(json_file_path, output_file_path):
    """
    根据清洗后的JSON文件生成测试用例Excel

    Args:
        json_file_path: 清洗后的JSON文件路径
        output_file_path: 输出Excel文件路径
    """

    # 读取清洗后的JSON文件
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 提取需求信息
    req_id = data['requirement']['req_id']
    req_title = data['requirement']['title']
    module_name = data['requirement']['module_name']

    # 生成测试用例数据
    testcases = []

    for function in data['business_functions']:
        function_name = function['function_name']

        for scenario in function['scenarios']:
            scenario_id = scenario['scenario_id']
            scenario_name = scenario['scenario_name']
            priority = scenario['priority']

            # 生成用例名称
            case_name = f"{req_id}-{scenario_id}-{function_name}"

            # 拼接测试步骤和预期结果
            step_descriptions = []
            expected_results = []

            for step in scenario['test_steps']:
                step_descriptions.append(step['step_description'])
                expected_results.append(step['expected_result'])

            # 用#拼接，确保第一个步骤前也有#
            steps_str = '#' + '#'.join(step_descriptions)
            results_str = '#' + '#'.join(expected_results)

            # 组装一行测试用例
            testcase_row = {
                '一级模块': module_name,
                '二级模块': function_name,
                '三级模块': '',
                '四级模块': '',
                '用例名称': case_name,
                '优先级': priority,
                '用例类型': '功能测试',
                '前置条件': '',
                '步骤描述': steps_str,
                '预期结果': results_str,
                '备注': '',
                '维护人': ''
            }

            testcases.append(testcase_row)

    # 创建Excel文件
    workbook = xlsxwriter.Workbook(output_file_path)
    worksheet = workbook.add_worksheet()

    # 设置列宽
    worksheet.set_column('A:A', 20)  # 一级模块
    worksheet.set_column('B:B', 15)  # 二级模块
    worksheet.set_column('C:C', 15)  # 三级模块
    worksheet.set_column('D:D', 15)  # 四级模块
    worksheet.set_column('E:E', 40)  # 用例名称
    worksheet.set_column('F:F', 10)  # 优先级
    worksheet.set_column('G:G', 15)  # 用例类型
    worksheet.set_column('H:H', 20)  # 前置条件
    worksheet.set_column('I:I', 60)  # 步骤描述
    worksheet.set_column('J:J', 60)  # 预期结果
    worksheet.set_column('K:K', 20)  # 备注
    worksheet.set_column('L:L', 15)  # 维护人

    # 定义12列表头（符合项目管理系统导入格式）
    headers = [
        '一级模块',
        '二级模块',
        '三级模块',
        '四级模块',
        '用例名称',
        '优先级',
        '用例类型',
        '前置条件',
        '步骤描述',
        '预期结果',
        '备注',
        '维护人'
    ]

    # 写入第一行：列名
    for col_idx, col_name in enumerate(headers):
        worksheet.write(0, col_idx, col_name)

    # 写入测试用例数据（从第二行开始，不保留示例数据）
    row_num = 1
    for tc in testcases:
        worksheet.write(row_num, 0, tc['一级模块'])
        worksheet.write(row_num, 1, tc['二级模块'])
        worksheet.write(row_num, 2, tc['三级模块'])
        worksheet.write(row_num, 3, tc['四级模块'])
        worksheet.write(row_num, 4, tc['用例名称'])
        worksheet.write(row_num, 5, tc['优先级'])
        worksheet.write(row_num, 6, tc['用例类型'])
        worksheet.write(row_num, 7, tc['前置条件'])
        worksheet.write(row_num, 8, tc['步骤描述'])
        worksheet.write(row_num, 9, tc['预期结果'])
        worksheet.write(row_num, 10, tc['备注'])
        worksheet.write(row_num, 11, tc['维护人'])
        row_num += 1

    workbook.close()

    return {
        'req_id': req_id,
        'req_title': req_title,
        'testcase_count': len(testcases),
        'modules': list(set([tc['二级模块'] for tc in testcases])),
        'total_scenarios': sum([len(function['scenarios']) for function in data['business_functions']])
    }

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python generate_excel.py <json_file> <output_file>")
        sys.exit(1)

    json_file = sys.argv[1]
    output_file = sys.argv[2]

    result = generate_testcase_excel(json_file, output_file)

    print(f"✅ 测试用例生成成功！")
    print(f"需求编号：{result['req_id']}")
    print(f"需求标题：{result['req_title']}")
    print(f"生成的测试用例数量：{result['testcase_count']}")
    print(f"涉及的功能模块：{', '.join(result['modules'])}")
    print(f"总测试场景数量：{result['total_scenarios']}")
    print(f"输出文件：{output_file}")
