# 02_enrich_data/main.py

import pandas as pd
from tqdm import tqdm
import time
from datetime import datetime
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
# 导入我们自己的模块和配置
from config import (
    SOURCE_CSV_FILE_PATH, OUTPUT_FILENAME_BASE, FAB_API_HEADERS,
    SELENIUM_HEADLESS, SELENIUM_TIMEOUT
)
from scrapers.basic_info_api import get_basic_info
from scrapers.full_details_selenium import get_full_details
from services.deepseek_client import get_summary_from_deepseek


def setup_selenium_driver():
    """初始化并返回一个Selenium WebDriver实例。"""
    print("正在初始化Selenium浏览器...")
    options = webdriver.ChromeOptions()
    if SELENIUM_HEADLESS:
        options.add_argument('--headless')
        print("模式：无头模式 (后台运行)")
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1920,1080')
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    # 自动查找位于项目根目录的 chromedriver.exe
    # 注意路径是相对于main.py的
    service = ChromeService(executable_path="../chromedriver.exe")

    try:
        driver = webdriver.Chrome(service=service, options=options)
        print("Selenium浏览器已准备就绪。")
        return driver
    except Exception as e:
        print(f"启动Selenium失败！请确保 'chromedriver.exe' 在项目根目录下，并且与您的Chrome浏览器版本匹配。")
        print(f"错误详情: {e}")
        return None


def main():
    """主执行函数，负责整个数据增强流程。"""
    print("--- Fab资产信息增强工具启动 ---")

    # 1. 读取源CSV文件
    try:
        # 确保使用相对路径正确读取文件
        df = pd.read_csv(SOURCE_CSV_FILE_PATH)
        # 从Excel公式中提取纯URL
        df['URL'] = df['URL'].str.extract(r'HYPERLINK\("([^"]+)"\)')
        print(f"成功读取源文件: {SOURCE_CSV_FILE_PATH}，共 {len(df)} 条记录。")
    except FileNotFoundError:
        print(f"错误：未找到源文件 '{SOURCE_CSV_FILE_PATH}'。")
        print("请先运行 01_fetch_library/fab_library_scraper.py 生成原始数据。")
        return
    except Exception as e:
        print(f"读取CSV文件时出错: {e}")
        return

    # 2. 启动Selenium Driver
    driver = setup_selenium_driver()
    if not driver:
        return  # 如果启动失败则退出

    # 3. 准备新列
    new_columns = [
        'Supported_UE_Versions', 'Last_update', 'Distribution_Method',
        'AI_Summary', 'Full_Description', 'Technical_details_Text'
    ]
    for col in new_columns:
        if col not in df.columns:
            df[col] = ''

    # 4. 循环处理每一行数据
    try:
        for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="增强资产信息中"):
            title = row['Title']
            url = row['URL']
            uid = row['UID']

            print(f"\n[{index + 1}/{len(df)}] 正在处理: {title}")

            # a. 通过API获取基础信息 (Description)
            print("  > 步骤1: API获取描述...")
            basic_info = get_basic_info(uid, FAB_API_HEADERS)
            df.loc[index, 'Full_Description'] = basic_info.get('description', 'N/A')

            # b. 通过Selenium获取完整细节
            print("  > 步骤2: Selenium获取技术细节...")
            full_details = get_full_details(url, driver)
            df.loc[index, 'Supported_UE_Versions'] = full_details.get('Supported Unreal Engine Versions', 'N/A')
            df.loc[index, 'Last_update'] = full_details.get('Last update', 'N/A')
            df.loc[index, 'Distribution_Method'] = full_details.get('Distribution Method', 'N/A')
            df.loc[index, 'Technical_details_Text'] = full_details.get('Technical details', 'N/A')

            # c. 调用AI生成简介
            print("  > 步骤3: DeepSeek生成简介...")
            ai_summary = get_summary_from_deepseek(
                title=title,
                description=df.loc[index, 'Full_Description'],
                technical_details=df.loc[index, 'Technical_details_Text']
            )
            df.loc[index, 'AI_Summary'] = ai_summary

            time.sleep(1)  # 礼貌性延时

    finally:
        # 5. 确保无论如何都关闭浏览器
        if driver:
            driver.quit()
            print("\nSelenium浏览器已关闭。")

    # 6. 保存最终结果
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, f"{OUTPUT_FILENAME_BASE}.csv")
    xlsx_path = os.path.join(output_dir, f"{OUTPUT_FILENAME_BASE}.xlsx")

    print(f"\n正在保存增强后的数据...")
    try:
        # 保存为CSV
        df.to_csv(csv_path, index=False, encoding='utf-8-sig')
        print(f"CSV文件已保存到: {csv_path}")

        # 保存为XLSX
        df.to_excel(xlsx_path, index=False, engine='openpyxl')
        print(f"Excel文件已保存到: {xlsx_path}")

        print("\n--- 所有任务处理完成！ ---")
    except Exception as e:
        print(f"保存文件时出错: {e}")


if __name__ == "__main__":
    main()