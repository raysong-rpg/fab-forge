import cloudscraper
import time
import os
import sys

# --- 核心修改：动态添加项目根目录到Python搜索路径 ---
# 这使得此脚本可以导入项目中其他模块（如utils）的功能
# __file__ 指的是当前脚本文件 'fab_library_scraper.py'
# os.path.abspath(__file__) 获取它的绝对路径
# os.path.dirname(...) 获取它所在的目录 ('.../step1_fetch_library/')
# 再一次 os.path.dirname(...) 就得到了项目根目录 ('.../fab-forge/')
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

# 现在可以安全地从项目的其他模块导入了
# 假设 file_handler.py 在 'step2_enrich_data/utils/' 目录下
try:
    from step2_enrich_data.utils.file_handler import save_to_csv_with_hyperlink, save_to_xlsx_with_hyperlink
except ImportError as e:
    print(f"错误：无法导入文件处理模块。请确保项目结构正确。 {e}")


    # 定义一个备用的空函数，以防导入失败，保证脚本能继续运行（但无法保存）
    def save_to_csv_with_hyperlink(*args, **kwargs):
        print("警告：CSV保存功能不可用。")


    def save_to_xlsx_with_hyperlink(*args, **kwargs):
        print("警告：XLSX保存功能不可用。")

# ================== 配置区 (如果脚本失效，优先检查这里) ==================

# 目标API的URL地址
base_url = "https://www.fab.com/i/library/entitlements/search"

# API请求参数，'createdAt'表示按入库时间从旧到新排序
params = {
    'sort_by': 'createdAt'
}

# 请求头，包含了身份验证信息
# !!! 注意：如果脚本失效，优先更新这里的 'cookie' 值 !!!
headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en',
    'cache-control': 'no-cache',
    'cookie': 'sb_csrftoken=x2ZdOSLN0zSkJor76eCxzFc2s8SxBkG6; OptanonConsent=isGpcEnabled=0&datestamp=Sun+Dec+29+2024+10%3A13%3A14+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202302.1.0&isIABGlobal=false&hosts=&consentId=b14cdfe7-b35b-43f7-82c1-0be7af88a1c3&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1&AwaitingReconsent=false; cf_clearance=mytzExgSmCP66NT4EclhC6THIlspJXGJCSyvX9SRJD0-1750474450-1.2.1.1-4MPj12ADVnAZIC18Jg.RIZgeKR7t6z6aDs5rwqC1ge5PxY9p69CoHtKZX2zo4q2bByF.bfCEoNsoGzOzyE3uDutv9LVk7De3wiYa7Cjc5ba.DN8unGErp02gHvJD4bdw09wRMrA3OEsU.xbiy82bzUhwooM5OLCQL_0oH1VVihx1hZVvdCu0omQLwaRIKdQR09i9ooLYD.nveFfaB0MD3UAblm3H892wwLYTdeMgx2Y2TqxXIQGUSuCuWOJxsS5n4xW6nigwIA4bPC8i75cWQ4Z_e3AegJfgg4ckql85Mqwo0oObbQLquMdrl7HltTNv9bi6k9ZO0EXzAJmGRvxemb2drdH6uYcqvdN25tSnnvE; fab_csrftoken=M5G9xF21jDIstC08zvuVtHvDnShyHK22; fab_sessionid=dlxiz3evisdfq2bw1emaw2deh90bmesc; __cf_bm=oyiMjLSPcFEi1.3ea._dU9d0JW9IUWFOEjzZv8UMmnk-1750474787-1.0.1.1-4dVxZzfype.YeGSzH0JKVX0kx1juQti3ajD5Kjq4JTnlIFa6yeP_nIQeKHa9fmnbtxpW.oQDqBYrHyq4qiRjpHIF3exgsgkfXt9tfFEQziY',  # <--- 请务必替换为您自己的、最新的Cookie字符串
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
    'x-csrftoken': 'xD71tekCz6lDOqBFctS5ntv9bHKm94jk',  # <--- 如果需要，也请替换
    'x-requested-with': 'XMLHttpRequest'
}


# ================== 数据处理与抓取 ==================

def fetch_all_assets():
    """抓取所有已拥有的资产数据并返回一个字典列表。"""
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
                print(f"URL: {response.url}")
                print(f"Status Code: {response.status_code}")
                print(f"Response Text: {response.text[:500]}")
            break

        results = data.get('results', [])
        if not results:
            print("当前页没有数据，抓取结束。")
            break

        print(f"成功获取 {len(results)} 个资产信息。")
        for item in results:
            listing_data = item.get('listing', {})
            price_data = listing_data.get('startingPrice') or {}
            uid = listing_data.get('uid', '')

            created_at_raw = item.get('createdAt', 'N/A')
            formatted_date = str(created_at_raw)[:10]  # 简化日期处理

            asset_info = {
                'Title': listing_data.get('title', 'N/A'),
                'ListingType': listing_data.get('listingType', 'N/A'),
                'URL': f"https://www.fab.com/listings/{uid}" if uid else 'N/A',
                'CurrencyCode': price_data.get('currencyCode', 'N/A'),
                'ListPrice': price_data.get('price', 'N/A'),
                'CreatedAt': formatted_date,
                'UID': uid or 'N/A',
                'Notes': 'Price data missing' if listing_data.get('startingPrice') is None else ''
            }
            all_assets.append(asset_info)

        next_cursor = data.get('cursors', {}).get('next')
        if not next_cursor:
            print("--- 所有页面已抓取完毕 ---")
            break

        current_params['cursor'] = next_cursor
        page_count += 1
        time.sleep(2)  # 友好的抓取延时

    return all_assets


# ================== 主程序执行 ==================

def main():
    """主执行函数"""
    # 1. 动态确定输出目录
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(current_script_dir, "output")
    os.makedirs(output_dir, exist_ok=True)  # 确保目录存在

    # 2. 抓取所有数据
    my_assets = fetch_all_assets()

    # 3. 如果抓取到了数据，则调用外部模块进行保存
    if my_assets:
        print(f"\n抓取完成！总共抓取了 {len(my_assets)} 个你已拥有的资产。")
        print(f"现在开始保存文件到 '{output_dir}' 文件夹...")

        # 构建完整的文件路径
        csv_filepath = os.path.join(output_dir, 'my_fab_assets_library.csv')
        xlsx_filepath = os.path.join(output_dir, 'my_fab_assets_library.xlsx')

        # 调用从 file_handler.py 导入的函数
        save_to_csv_with_hyperlink(my_assets, file_path=csv_filepath, url_column='URL')
        save_to_xlsx_with_hyperlink(my_assets, file_path=xlsx_filepath, url_column='URL')

        print("\n所有操作完成！")
    else:
        print("\n未能抓取到任何资产数据，程序结束。")


if __name__ == "__main__":
    main()