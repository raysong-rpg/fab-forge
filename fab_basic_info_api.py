import cloudscraper
import json
from bs4 import BeautifulSoup


def get_fab_asset_description_from_api(asset_uid: str):
    """
    通过直接请求资产的专属API接口来获取其详细信息，包括描述。
    这是解决此问题的正确途径。

    Args:
        asset_uid (str): 资产的唯一标识符 (UID)。
    """
    # 1. 构造正确的API URL，而不是页面URL
    api_url = f"https://www.fab.com/i/listings/{asset_uid}"

    print(f"策略已更正：直接请求数据API: {api_url}")

    # 2. 使用您提供的、已被证明对API请求有效的【完整请求头】
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en',
        'cookie': 'sb_csrftoken=x2ZdOSLN0zSkJor76eCxzFc2s8SxBkG6; OptanonConsent=isGpcEnabled=0&datestamp=Sun+Dec+29+2024+10%3A13%3A14+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202302.1.0&isIABGlobal=false&hosts=&consentId=b14cdfe7-b35b-43f7-82c1-0be7af88a1c3&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1&AwaitingReconsent=false; fab_csrftoken=M5G9xF21jDIstC08zvuVtHvDnShyHK22; fab_sessionid=dlxiz3evisdfq2bw1emaw2deh90bmesc; cf_clearance=GH64MkSxOalYnA67asEKOyd2qKwjd4c3mHftQo8otS0-1750642514-1.2.1.1-zIAoH7w28FDRoCgrZBFe096fgMS2GzAA6gmRsk6_sVUTqWOd5ir.YgHTRE_5oZcD8iSy_d4ZKB801NlzITIfK6yXblwH07OLqef3_gLAD0D8p6pyTT63AmS3AY3znVgWdPZ6.y5aqXW77dV600bylRx2_VXjXa_n4PzXK4uea09PUsmHN_Dd0V5e3HR3oSgSqBgLTSUnHGKXqXm4KwYX_FgGZ_IA63JEkNPxrfVxqMJ7_sWgnPKW6ZSVmeJg.eOZGp.Z50H4Nnxz5Wsa6qKks9dcryob0LystSvi3Pteo8xqVGqQjZiIhW.pltHLCssoAC54pBzdW4k77yh_qVLUgABsvqyQ4RDD5kYjSIAkdOM; __cf_bm=MD.Gs8y71xQfBhgIsz6oPXn7l.XlY9CMN.PVuaIIfL0-1750642758-1.0.1.1-VE7KB6rUu1uJo4nfyqLTWdvLCxYa5XrH937yYGK7D8rwL8os0BobVUyPp6rN3B3tQzKsIuz0UiABJ2fnalE.P5wXuz7HAZyU4JG4wmPF1z4',
        'priority': 'u=1, i',
        'referer': 'https://www.fab.com/listings/906d1e98-423a-4516-9715-c950adc88d6f',  # Referer是页面URL，这很合理
        'sec-ch-ua': '"Microsoft Edge";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36 Edg/137.0.0.0',
        'x-csrftoken': 'M5G9xF21jDIstC08zvuVtHvDnShyHK22',
        'x-requested-with': 'XMLHttpRequest',
    }

    scraper = cloudscraper.create_scraper()

    try:
        # 3. 对正确的API URL发起请求
        response = scraper.get(api_url, headers=headers, timeout=20)
        response.raise_for_status()

        # 4. 直接将返回内容解析为JSON，不再需要BeautifulSoup解析HTML
        data = response.json()

        # 5. 从JSON数据中直接提取描述信息
        # 根据经验，数据可能在'listing'键下，也可能直接在顶层
        listing_data = data.get('listing', data)  # 如果没有'listing'键，就尝试在根对象找
        description_html = listing_data.get('description')

        if description_html:
            print("\n" + "=" * 20 + " 成功获取到资产描述 " + "=" * 20)
            # 描述本身是HTML，我们用BS来清理一下，只输出纯文本
            description_soup = BeautifulSoup(description_html, 'html.parser')
            clean_text = description_soup.get_text(separator='\n').strip()
            print(clean_text)
            print("=" * 62 + "\n")
        else:
            print("错误：API返回的JSON中未找到'description'字段。请检查JSON结构。")
            # print(json.dumps(data, indent=2)) # 如果失败，取消注释以查看完整的JSON响应

    except Exception as e:
        print(f"\n抓取过程中发生错误: {e}")
        if 'response' in locals():
            print(f"状态码: {response.status_code}")
            print(f"响应内容: {response.text[:500]}")


# ================== 主程序执行 ==================
if __name__ == "__main__":
    # 从页面URL中提取资产UID
    target_page_url = "https://www.fab.com/listings/906d1e98-423a-4516-9715-c950adc88d6f"
    asset_uid = target_page_url.split('/')[-1]

    get_fab_asset_description_from_api(asset_uid)