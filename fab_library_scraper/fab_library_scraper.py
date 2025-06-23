import cloudscraper
import time
import csv
from datetime import datetime
import os  # 1. 引入 os 模块，用于处理文件和目录

# ================== 配置区 (如果脚本失效，优先检查这里) ==================

# 目标API的URL地址
base_url = "https://www.fab.com/i/library/entitlements/search"

# API请求参数，'createdAt'表示按入库时间从旧到新排序
params = {
    'sort_by': 'createdAt'
}

# 请求头，包含了身份验证信息，是成功爬取的关键
# 注意：cookie和cf_clearance等值具有时效性，如果脚本运行失败提示认证错误，请更新此处的cookie值
headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en',
    'cache-control': 'no-cache',
    'cookie': 'sb_csrftoken=x2ZdOSLN0zSkJor76eCxzFc2s8SxBkG6; OptanonConsent=isGpcEnabled=0&datestamp=Sun+Dec+29+2024+10%3A13%3A14+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202302.1.0&isIABGlobal=false&hosts=&consentId=b14cdfe7-b35b-43f7-82c1-0be7af88a1c3&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1&AwaitingReconsent=false; cf_clearance=mytzExgSmCP66NT4EclhC6THIlspJXGJCSyvX9SRJD0-1750474450-1.2.1.1-4MPj12ADVnAZIC18Jg.RIZgeKR7t6z6aDs5rwqC1ge5PxY9p69CoHtKZX2zo4q2bByF.bfCEoNsoGzOzyE3uDutv9LVk7De3wiYa7Cjc5ba.DN8unGErp02gHvJD4bdw09wRMrA3OEsU.xbiy82bzUhwooM5OLCQL_0oH1VVihx1hZVvdCu0omQLwaRIKdQR09i9ooLYD.nveFfaB0MD3UAblm3H892wwLYTdeMgx2Y2TqxXIQGUSuCuWOJxsS5n4xW6nigwIA4bPC8i75cWQ4Z_e3AegJfgg4ckql85Mqwo0oObbQLquMdrl7HltTNv9bi6k9ZO0EXzAJmGRvxemb2drdH6uYcqvdN25tSnnvE; fab_csrftoken=M5G9xF21jDIstC08zvuVtHvDnShyHK22; fab_sessionid=dlxiz3evisdfq2bw1emaw2deh90bmesc; __cf_bm=oyiMjLSPcFEi1.3ea._dU9d0JW9IUWFOEjzZv8UMmnk-1750474787-1.0.1.1-4dVxZzfype.YeGSzH0JKVX0kx1juQti3ajD5Kjq4JTnlIFa6yeP_nIQeKHa9fmnbtxpW.oQDqBYrHyq4qiRjpHIF3exgsgkfXt9tfFEQziY',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.fab.com/library?sort_by=createdAt',
    'sec-ch-ua': '"Microsoft Edge";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36 Edg/137.0.0.0',
    'x-csrftoken': 'xD71tekCz6lDOqBFctS5ntv9bHKm94jk',
    'x-requested-with': 'XMLHttpRequest'
}


# ================== 数据处理与抓取 ==================

def fetch_all_assets():
    """抓取所有资产数据并返回一个列表。"""
    scraper = cloudscraper.create_scraper()
    all_assets = []
    page_count = 1
    current_params = params.copy()

    print("爬虫启动...(获取已拥有资产，排序模式)")
    while True:
        response = None
        print(f"--- 正在获取第 {page_count} 页数据 ---")
        try:
            response = scraper.get(base_url, headers=headers, params=current_params, timeout=20)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print(f"请求或处理失败，错误信息: {e}")
            if 'response' in locals() and response is not None:
                print("URL:", response.url)
                print("Status Code:", response.status_code)
                print("Response Text:", response.text[:500])
            break

        results = data.get('results', [])
        if not results:
            print("当前页没有数据，抓取结束。")
            break

        print(f"成功获取 {len(results)} 个资产信息。")
        for item in results:
            listing_data = item.get('listing', {})
            note = ''
            raw_price_data = listing_data.get('startingPrice')
            if raw_price_data is None:
                note = 'Price data was null/missing in API response'
            price_data = raw_price_data or {}

            created_at_raw = item.get('createdAt', 'N/A')
            formatted_date = 'N/A'
            if created_at_raw != 'N/A':
                try:
                    dt_object = datetime.fromisoformat(created_at_raw.replace('Z', '+00:00'))
                    formatted_date = dt_object.strftime('%Y-%m-%d')
                except (ValueError, TypeError):
                    formatted_date = str(created_at_raw)[:10]

            uid = listing_data.get('uid', '')
            url = f"https://www.fab.com/listings/{uid}" if uid else 'N/A'

            asset_info = {
                'Title': listing_data.get('title', 'N/A'),
                'ListingType': listing_data.get('listingType', 'N/A'),
                'URL': url,
                'CurrencyCode': price_data.get('currencyCode', 'N/A'),
                'ListPrice': price_data.get('price', 'N/A'),
                'CreatedAt': formatted_date,
                'UID': uid if uid else 'N/A',
                'Notes': note
            }
            all_assets.append(asset_info)

        next_cursor = data.get('cursors', {}).get('next')
        if not next_cursor:
            print("--- 所有页面已抓取完毕 ---")
            break

        current_params['cursor'] = next_cursor
        page_count += 1
        time.sleep(2)

    return all_assets


# ================== 文件保存函数 ==================

def save_to_csv(asset_data_list, filename):
    """将数据保存为CSV文件，URL列使用HYPERLINK公式以兼容Excel。"""
    if not asset_data_list:
        return

    fieldnames = ['Title', 'ListingType', 'URL', 'CurrencyCode', 'ListPrice', 'CreatedAt', 'UID', 'Notes']

    # 为CSV创建专门的数据副本，将URL转换为Excel公式
    csv_rows = []
    for asset in asset_data_list:
        row = asset.copy()
        url = row.get('URL', 'N/A')
        if url and url != 'N/A':
            # 这个公式能让Excel将文本识别为可点击的链接
            row['URL'] = f'=HYPERLINK("{url}")'
        csv_rows.append(row)

    with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_rows)
    print(f"数据已成功保存到CSV文件: {filename}")


def save_to_xlsx(asset_data_list, filename):
    """将数据保存为XLSX文件，URL列是真正的可点击超链接。"""
    if not asset_data_list:
        return

    try:
        import xlsxwriter
    except ImportError:
        print("\n[提示] 未找到 'xlsxwriter' 库，跳过生成Excel文件。")
        print("若要生成.xlsx文件，请运行: pip install XlsxWriter")
        return

    fieldnames = ['Title', 'ListingType', 'URL', 'CurrencyCode', 'ListPrice', 'CreatedAt', 'UID', 'Notes']
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet("My Fab Assets")
    header_format = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1})

    for col_num, header_name in enumerate(fieldnames):
        worksheet.write(0, col_num, header_name, header_format)

    for row_num, asset_info in enumerate(asset_data_list, 1):
        for col_num, field in enumerate(fieldnames):
            cell_value = asset_info.get(field, '')
            if field == 'URL' and cell_value and cell_value != 'N/A':
                worksheet.write_url(row_num, col_num, cell_value, string=cell_value)
            else:
                worksheet.write(row_num, col_num, cell_value)

    worksheet.set_column('A:A', 50)
    worksheet.set_column('B:B', 15)
    worksheet.set_column('C:C', 50)
    worksheet.set_column('D:E', 12)
    worksheet.set_column('F:F', 15)
    worksheet.set_column('G:G', 40)
    worksheet.set_column('H:H', 40)

    workbook.close()
    print(f"数据已成功保存到Excel文件: {filename}")


# ================== 主程序执行 ==================

if __name__ == "__main__":
    # 1. 抓取所有数据
    my_assets = fetch_all_assets()

    # 2. 如果抓取到了数据，则保存文件
    if my_assets:
        print(f"\n抓取完成！总共抓取了 {len(my_assets)} 个你已拥有的资产。")

        # 3. 定义并创建输出文件夹
        output_dir = "../my_fab_assets_library"
        os.makedirs(output_dir, exist_ok=True)
        print(f"现在开始保存文件到 ./{output_dir}/ 文件夹...")

        # 4. 构建完整的文件路径
        csv_filepath = os.path.join(output_dir, 'my_fab_assets_library.csv')
        xlsx_filepath = os.path.join(output_dir, 'my_fab_assets_library.xlsx')

        # 5. 保存为CSV文件 (适合数据存储和交换)
        # 如果不需要CSV文件，可以注释掉下面这行
        save_to_csv(my_assets, filename=csv_filepath)

        # 6. 保存为XLSX文件 (适合查看和编辑)
        save_to_xlsx(my_assets, filename=xlsx_filepath)

        print("\n所有操作完成！")
    else:
        print("\n未能抓取到任何资产数据，程序结束。")