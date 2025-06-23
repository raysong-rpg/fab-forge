import time
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


def get_full_details(page_url: str, driver: WebDriver) -> dict:
    """
    使用一个已有的Selenium WebDriver实例访问页面，并根据经过验证的HTML结构，
    通过文本标签和DOM关系，精确提取所有指定的技术信息。

    Args:
        page_url (str): 目标资产的完整页面URL。
        driver (WebDriver): 一个已经启动和配置好的Selenium WebDriver实例。

    Returns:
        dict: 一个包含所有技术细节的字典。如果抓取失败，会返回包含错误信息的字典。
    """
    # 初始化一个默认的失败结果字典，保证任何情况下返回的结构都一致
    details = {
        "Technical details": "抓取失败",
        "Supported Unreal Engine Versions": "抓取失败",
        "Last update": "抓取失败",
        "Distribution Method": "抓取失败"
    }

    try:
        # 使用传入的driver实例加载页面
        driver.get(page_url)

        # 等待一个明确的、通常靠后加载的元素出现，以确保页面JS已执行完毕
        # 这里我们等待 "Distribution Method" 文本出现，因为它在目标信息中
        wait = WebDriverWait(driver, 20)  # 设置20秒超时
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[text()='Distribution Method']")))

        # 增加一个短暂的固定等待，确保DOM完全稳定
        time.sleep(1)

        # 获取由JS完全渲染后的最终页面HTML
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # --- 开始基于HTML结构的精确提取 ---

        # 1. 提取 Technical details
        tech_list = []
        tech_header = soup.find('h3', string='Technical details')
        if tech_header and tech_header.find_next_sibling('div'):
            tech_container = tech_header.find_next_sibling('div')
            for p in tech_container.find_all('p'):
                text = p.get_text(strip=True)
                if text:
                    tech_list.append(text)
            details["Technical details"] = "\n".join(tech_list) if tech_list else "无详细信息"
        else:
            details["Technical details"] = "未找到该部分"

        # 2. 提取 Supported Unreal Engine Versions
        ue_versions_label = soup.find(string='Supported Unreal Engine Versions')
        if ue_versions_label and ue_versions_label.find_parent('div'):
            value_div = ue_versions_label.find_parent('div').find_next_sibling('div')
            details["Supported Unreal Engine Versions"] = value_div.text.strip() if value_div else "值未找到"
        else:
            details["Supported Unreal Engine Versions"] = "标签未找到"

        # 3. 提取 Last update
        last_update_label = soup.find(string='Last update')
        if last_update_label and last_update_label.find_parent('div'):
            # 其DOM结构比较特殊，需要多层查找
            value_div = last_update_label.find_parent('div').find_next_sibling('div').find('div')
            details["Last update"] = value_div.text.strip() if value_div else "值未找到"
        else:
            details["Last update"] = "标签未找到"

        # 4. 提取 Distribution Method
        dist_method_label = soup.find(string='Distribution Method')
        if dist_method_label and dist_method_label.find_parent('div'):
            value_div = dist_method_label.find_parent('div').find_next_sibling('div')
            details["Distribution Method"] = value_div.text.strip() if value_div else "值未找到"
        else:
            details["Distribution Method"] = "标签未找到"

        return details

    except Exception as e:
        # 在批量处理中，打印简洁的错误信息，但不会让整个程序崩溃
        print(f"  [Selenium] URL {page_url} 抓取失败: {type(e).__name__}")
        # 即使发生异常，也返回包含错误信息的字典，保持数据结构一致
        return details