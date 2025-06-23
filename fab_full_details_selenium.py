import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


def get_final_asset_details(page_url: str):
    """
    最终修正版：使用Selenium加载页面，并根据已验证的HTML结构，
    通过文本标签和DOM关系，精确提取所有指定的信息。
    """
    print(f"最终方案：使用Selenium浏览器自动化访问 -> {page_url}")

    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    service = ChromeService()
    driver = None

    try:
        print("正在启动浏览器...")
        driver = webdriver.Chrome(service=service, options=options)

        driver.get(page_url)
        print("页面已打开，等待动态内容加载...")

        # 等待页面上出现 "Technical details" 这个标题，确保核心内容区已加载
        wait = WebDriverWait(driver, 30)
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Technical details')]")))
        print("目标内容已加载！开始精确解析...")

        time.sleep(2)  # 增加一个短暂的稳定等待时间

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        print("\n" + "=" * 20 + " 您需要的最终信息 " + "=" * 20)

        # --- 1. 提取 Technical details ---
        print("\n[Technical details]")
        tech_header = soup.find('h3', string='Technical details')
        if tech_header:
            tech_container = tech_header.find_next_sibling('div')
            if tech_container:
                details_paragraphs = tech_container.find_all('p')
                for p in details_paragraphs:
                    text = p.get_text(strip=True)
                    if text:
                        print(text)
        else:
            print("未能找到 'Technical details' 部分。")

        # --- 2. 提取 Supported Unreal Engine Versions ---
        print("\n[Compatibility]")
        ue_versions_label = soup.find(string='Supported Unreal Engine Versions')
        if ue_versions_label:
            # 它的值在父级的下一个兄弟div的子div里
            value_div = ue_versions_label.find_parent('div').find_next_sibling('div')
            if value_div:
                print(f"Supported Unreal Engine Versions: {value_div.text.strip()}")
            else:
                print("Supported Unreal Engine Versions: 未找到值。")
        else:
            print("Supported Unreal Engine Versions: 未找到标签。")

        # --- 3. 提取 Other information ---
        print("\n[Other information]")
        # Last update 和 Distribution Method 在不同的HTML结构中

        # 提取 Last update (它在右侧边栏的"Details"部分)
        last_update_label = soup.find(string='Last update')
        if last_update_label:
            # 它的值在父级的下一个兄弟div的第一个子div里
            value_div = last_update_label.find_parent('div').find_next_sibling('div').find('div')
            if value_div:
                print(f"Last update: {value_div.text.strip()}")
            else:
                print("Last update: 未找到值。")
        else:
            print("Last update: 未找到标签。")

        # 提取 Distribution Method (它在中间的"Other information"部分)
        dist_method_label = soup.find(string='Distribution Method')
        if dist_method_label:
            # 它的值就在父级的下一个兄弟div里
            value_div = dist_method_label.find_parent('div').find_next_sibling('div')
            if value_div:
                print(f"Distribution Method: {value_div.text.strip()}")
            else:
                print("Distribution Method: 未找到值。")
        else:
            print("Distribution Method: 未找到标签。")


    except Exception as e:
        print(f"\n抓取过程中发生错误: {e}")
    finally:
        if driver:
            driver.quit()
        print("\n脚本执行完毕，浏览器已关闭。")


# ================== 主程序执行 ==================
if __name__ == "__main__":
    target_page_url = "https://www.fab.com/listings/906d1e98-423a-4516-9715-c950adc88d6f"
    get_final_asset_details(target_page_url)