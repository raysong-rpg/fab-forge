import cloudscraper
import time
import csv
from datetime import datetime

# ================== 配置区 (如果脚本失效，优先检查这里) ==================

# 目标API的URL地址
base_url = "https://www.fab.com/i/library/entitlements/search"

# API请求参数，'createdAt'表示按入库时间从旧到新排序
params = {
    'sort_by': 'createdAt'
}

# 请求头，包含了身份验证信息，是成功爬取的关键
# 注意: 如果脚本未来失效 (例如返回401或403错误)，最可能的原因是cookie过期。
# 你需要重新登录Fab网站，从浏览器开发者工具中复制新的cookie值来替换它。
headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en',
    'cache-control': 'no-cache',
    'cookie': 'sb_csrftoken=x2ZdOSLN0zSkJor76eCxzFc2s8SxBkG6; OptanonConsent=isGpcEnabled=0&datestamp=Sun+Dec+29+2024+10%3A13%3A14+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202302.1.0&isIABGlobal=false&hosts=&consentId=b14cdfe7-b35b-43f7-82c1-0be7af88a1c3&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1&AwaitingReconsent=false; fab_csrftoken=xD71tekCz6lDOqBFctS5ntv9bHKm94jk; fab_sessionid=xkycivcj55ebc91g0rrjtwngld1uibqz; cf_clearance=zmNVZNFpnTa2YPAZf0N3R7SJbUi90IsIc2.92j4owkw-1750423042-1.2.1.1-JUAC4XccMMwumBwblXbWyLqyC3.AA22.vDU.LIWQs0eLVEaWshoCwiOjkhkH1ZaYiVaqOacKei.GYcaRsLwaIodr0EoaEP_krHKss8aR9hDlfrQM8J6uQs2q0tgETDY3QEXGiBEVST6t8v3DW89UNHSsPBgaQvua3N1LLhTY9bPhlBxq9.zmsM9nLQRtunbNPkw89yuQmKMLZjip6qEZuKNA6YEBou5SpgdDdQvsLU.c_bv6KRSopdnHe04NHwq9C21vmfWDvXyMbCY1UPcDVp0okidrBBxfeckP5FD5DIbSbMik5WbYRQifsKRtp5_m4ThhQxRcTcVtlRaAIGlOoMUNEwAjNs1jMC1i9L2kQCs; __cf_bm=lao2jgJWY3abfE0onUxoxcaA2yBfb_I9FO0qZvRhFeQ-1750423448-1.0.1.1-HH5Tc_j3_a_UvDIHWQtg5xHii7ccNcMQGZUTmnuo4ldM2XS59JFxU86waZslMpAxraK5oxCkmv3HVWetzVLGwqLfF3nIvLo7UEowzv5c_YM',
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

# ================== 主程序区 ==================

# 初始化cloudscraper，用于绕过Cloudflare的JS验证
scraper = cloudscraper.create_scraper()
# 创建一个空列表，用于存储所有处理好的资产信息
all_my_assets = []
page_count = 1

print("爬虫启动...(获取已拥有资产，排序模式)")

# 通过循环和游标(cursor)实现自动翻页
while True:
    print(f"--- 正在获取第 {page_count} 页数据 ---")

    try:
        # 发送网络请求
        response = scraper.get(base_url, headers=headers, params=params, timeout=20)
        # 如果请求失败 (例如状态码为4xx或5xx)，则抛出异常
        response.raise_for_status()
        # 解析返回的JSON数据
        data = response.json()
    except Exception as e:
        print(f"请求或处理失败，错误信息: {e}")
        if 'response' in locals():
            print("URL:", response.url)
            print("Status Code:", response.status_code)
            print("Response Text:", response.text[:500])
        break

    # 从JSON数据中安全地获取资产列表
    results = data.get('results', [])
    if not results:
        print("当前页没有数据，抓取结束。")
        break

    print(f"成功获取 {len(results)} 个资产信息。")

    # 遍历当前页的每一个资产，进行数据清洗和格式化
    for item in results:
        # 安全地获取嵌套层级的数据
        listing_data = item.get('listing', {})
        price_data = listing_data.get('startingPrice', {})

        # 将ISO 8601标准日期格式化为'YYYY-MM-DD'
        created_at_raw = item.get('createdAt', 'N/A')
        formatted_date = 'N/A'
        if created_at_raw != 'N/A':
            try:
                dt_object = datetime.fromisoformat(created_at_raw.replace('+00:00', ''))
                formatted_date = dt_object.strftime('%Y-%m-%d')
            except ValueError:
                formatted_date = created_at_raw[:10]

        # 拼接资产详情页的URL
        uid = listing_data.get('uid', '')
        url = f"https://www.fab.com/listings/{uid}" if uid else 'N/A'

        # 将所有处理好的信息存入一个字典
        asset_info = {
            'Title': listing_data.get('title', 'N/A'),
            'ListingType': listing_data.get('listingType', 'N/A'),
            'URL': url,
            'CurrencyCode': price_data.get('currencyCode', 'N/A'),
            'ListPrice': price_data.get('price', 'N/A'),
            'CreatedAt': formatted_date,
            'UID': uid if uid else 'N/A'
        }
        all_my_assets.append(asset_info)

    # 获取下一页的游标(cursor)
    next_cursor = data.get('cursors', {}).get('next')
    if not next_cursor:
        print("--- 所有页面已抓取完毕 ---")
        break

    # 更新请求参数，用于下一次循环
    params['cursor'] = next_cursor
    page_count += 1
    # 礼貌性延时，避免给服务器造成过大压力
    time.sleep(2)

# ================== 保存文件区 ==================

print(f"\n抓取完成！总共抓取了 {len(all_my_assets)} 个你已拥有的资产。")
if all_my_assets:
    # 定义输出文件名和CSV文件的列名（表头）
    filename = 'my_fab_assets_library_final.csv'
    fieldnames = ['Title', 'ListingType', 'URL', 'CurrencyCode', 'ListPrice', 'CreatedAt', 'UID']

    # 使用'w'模式写入文件，'newline='' '避免空行，'encoding='utf-8-sig''确保Excel能正确显示中文
    with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # 写入表头
        writer.writeheader()
        # 一次性写入所有数据行
        writer.writerows(all_my_assets)

    print(f"数据已成功保存到文件: {filename}")