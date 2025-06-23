# 文件路径: step2_enrich_data/scrapers/basic_info_api.py

import cloudscraper
from bs4 import BeautifulSoup


def get_basic_info(asset_uid: str, headers: dict) -> dict:
    """
    通过直接请求资产的专属API接口，获取其基础信息。

    Args:
        asset_uid (str): 资产的唯一标识符 (UID)。
        headers (dict): 用于API请求的完整请求头。

    Returns:
        dict: 一个包含基础信息的字典，例如 {'description': '...'}
    """
    api_url = f"https://www.fab.com/i/listings/{asset_uid}"
    scraper = cloudscraper.create_scraper()

    # 初始化一个空的返回结果
    result = {"description": ""}

    try:
        response = scraper.get(api_url, headers=headers, timeout=20)
        response.raise_for_status()
        data = response.json()

        # 描述内容本身是HTML，先提取，清理工作留给AI部分或之后处理
        description_html = data.get('description', '')
        if description_html:
            # 清理HTML标签，得到纯文本
            soup = BeautifulSoup(description_html, 'html.parser')
            result['description'] = soup.get_text(separator='\n', strip=True)

        # 未来可以从这里提取更多API返回的基础信息
        # result['title'] = data.get('title', '')

        return result

    except Exception as e:
        # 在批量处理中，打印简洁的错误信息
        print(f"  [API] UID {asset_uid} 抓取失败: {type(e).__name__}")
        return result  # 即使失败，也返回一个包含空字符串的字典，保证结构一致