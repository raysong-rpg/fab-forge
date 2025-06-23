# 文件路径: step2_enrich_data/utils/file_handler.py

import pandas as pd
import csv

# 将xlsxwriter作为可选依赖，这样即使没安装，CSV功能也能用
try:
    import xlsxwriter
except ImportError:
    xlsxwriter = None


def save_to_csv_with_hyperlink(data_list: list, file_path: str, url_column: str = 'URL'):
    """
    将字典列表保存为CSV文件，并自动将指定列转换为Excel的HYPERLINK公式。

    Args:
        data_list (list): 包含字典的列表。
        file_path (str): 完整的文件保存路径。
        url_column (str): 需要转换为超链接的列名。
    """
    if not data_list:
        return

    # 获取表头
    fieldnames = list(data_list[0].keys())

    # 创建专门用于写入CSV的数据副本
    csv_rows = []
    for item in data_list:
        row = item.copy()
        url = row.get(url_column)
        if url and isinstance(url, str) and url != 'N/A':
            row[url_column] = f'=HYPERLINK("{url}")'
        csv_rows.append(row)

    with open(file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_rows)
    print(f"数据已成功保存到CSV文件: {file_path}")


def save_to_xlsx_with_hyperlink(data_list: list, file_path: str, url_column: str = 'URL'):
    """
    将字典列表保存为XLSX文件，并自动将指定列转换为可点击的超链接。

    Args:
        data_list (list): 包含字典的列表。
        file_path (str): 完整的文件保存路径。
        url_column (str): 需要转换为超链接的列名。
    """
    if not data_list:
        return

    if xlsxwriter is None:
        print(f"\n[提示] 未找到 'xlsxwriter' 库，跳过生成 {file_path}。")
        print("若要生成.xlsx文件，请运行: pip install XlsxWriter")
        return

    # 使用Pandas可以更轻松地处理数据到Excel的转换
    df = pd.DataFrame(data_list)

    # 创建一个Excel writer对象
    writer = pd.ExcelWriter(file_path, engine='xlsxwriter')

    # 将DataFrame写入Excel，但不包含索引
    df.to_excel(writer, sheet_name='My Fab Assets', index=False)

    # 获取workbook和worksheet对象以便进行格式化
    workbook = writer.book
    worksheet = writer.sheets['My Fab Assets']

    # 设置URL列为超链接
    if url_column in df.columns:
        url_col_idx = df.columns.get_loc(url_column)
        for row_num, url in enumerate(df[url_column], 1):  # 从1开始，因为0是表头
            if pd.notna(url) and isinstance(url, str) and url != 'N/A':
                worksheet.write_url(row_num, url_col_idx, url)

    # 自动调整列宽 (一个简单的实现)
    for i, col in enumerate(df.columns):
        width = max(df[col].astype(str).map(len).max(), len(col)) + 2
        worksheet.set_column(i, i, width)

    writer.close()
    print(f"数据已成功保存到Excel文件: {file_path}")