def create_readme_file():
    """
    生成 fab-forge 项目的 README.md 文件。
    将 README 内容逐行存入列表，最后统一写入文件，以避免任何渲染错误。
    【已根据新版 fab_library_scraper.py 进行更新】
    """
    readme_content = []

    # 1. 项目标题和简介
    readme_content.append("# Fab-Forge 锻造厂 🛠️")
    readme_content.append("")
    readme_content.append("> 一系列旨在增强您在 Fab.com 平台体验的实用工具集合。")
    readme_content.append("")
    readme_content.append(
        "[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)")
    readme_content.append("")
    readme_content.append("## 📖 项目简介")
    readme_content.append("")
    readme_content.append(
        "`fab-forge` 是一个开源项目，致力于为 Fab.com 用户提供一系列自动化、高效的工具。无论您是想备份自己的资产库、监控商品折扣，还是进行其他批量操作，这里都希望能为您提供解决方案。")
    readme_content.append("")
    readme_content.append("本项目的所有工具都基于 Python 编写，并尽可能提供清晰的说明和简单的使用方法。")
    readme_content.append("")
    readme_content.append("---")
    readme_content.append("")

    # 2. 安装说明
    readme_content.append("## ⚙️ 安装与准备")
    readme_content.append("")
    readme_content.append("1. **克隆仓库**")
    readme_content.append("   ```bash")
    readme_content.append("   git clone https://github.com/raysong-rpg/fab-forge.git")
    readme_content.append("   cd fab-forge")
    readme_content.append("   ```")
    readme_content.append("")
    readme_content.append("2. **安装依赖**")
    readme_content.append("   项目的所有依赖项都已在 `requirements.txt` 文件中列出。")
    readme_content.append("   建议在虚拟环境中安装：")
    readme_content.append("   ```bash")
    readme_content.append("   pip install -r requirements.txt")
    readme_content.append("   ```")
    readme_content.append("   > **提示:** `fab_library_scraper.py` 的 Excel(.xlsx)导出功能依赖 `XlsxWriter` 库。如果`requirements.txt`中未包含，请手动安装: `pip install XlsxWriter`")
    readme_content.append("")
    readme_content.append("---")
    readme_content.append("")

    # 3. 工具列表
    readme_content.append("## 🧰 工具列表")
    readme_content.append("")

    # --- 工具 1: Fab 库资产导出器 (更新) ---
    readme_content.append("### 1. Fab 库资产导出器 (`fab_library_scraper`)")
    readme_content.append("")
    readme_content.append(
        "**功能描述：** 登录您的 Fab 账户，自动抓取您已拥有的 **全部** 资产，并将其详细信息导出为结构清晰的 `.xlsx` (Excel) 和 `.csv` 文件。")
    readme_content.append("")
    readme_content.append("**核心特性：**")
    readme_content.append("- **完整数据抓取：** 通过模拟API排序参数，确保获取到您资产库中的每一项内容。")
    readme_content.append("- **双格式智能输出：**")
    readme_content.append("  - **`.xlsx` (推荐):** 生成格式化的Excel文件，URL可直接点击，列宽已自动调整，提供最佳阅读体验。")
    readme_content.append("  - **`.csv`:** 生成标准的CSV文件，具有最佳的数据兼容性，方便导入其他程序或数据库。")
    readme_content.append("- **详细字段导出：** 导出内容包括资产名、类型、详情页URL、价格、货币、入库日期、UID以及新增的 `Notes` 字段。")
    readme_content.append("- **智能容错与标记：** 能够自动处理API返回的不规范数据（如缺失的价格信息），确保脚本不会中途崩溃，并会在 `Notes` 列中对这些特殊条目进行标注。")
    readme_content.append("- **自动防护绕过：** 集成了 `cloudscraper` 库，能够自动应对 Cloudflare 的 JavaScript 验证。")
    readme_content.append("- **整洁的文件管理：** 所有导出的文件都会自动保存在一个名为 `my_fab_assets_library` 的文件夹中，保持项目根目录的整洁。")
    readme_content.append("")
    readme_content.append("#### 使用说明")
    readme_content.append("")
    readme_content.append("1. **【关键步骤】更新认证信息 (Cookie)**")
    readme_content.append("   - 由于需要访问您的私人资产库，脚本必须使用您的登录凭证（即 `Cookie`）。")
    readme_content.append("   - **第一步：** 在浏览器中登录您的 Fab 账户。")
    readme_content.append("   - **第二步：** 访问您的资产库页面，例如: [https://www.fab.com/library](https://www.fab.com/library)")
    readme_content.append("   - **第三步：** 在该页面上，按下 `F12` 打开开发者工具，切换到 **“网络(Network)”** 标签页。")
    readme_content.append("   - **第四步：** 刷新页面。在请求列表中，找到任意一个向 `www.fab.com/i/...` 发出的请求（例如 `search?sort_by=...`）。点击它。")
    readme_content.append("   - **第五步：** 在右侧的 **“标头(Headers)”** 部分，向下滚动到 **“请求标头(Request Headers)”**，然后右键点击 `cookie:` 字段，选择 **“复制值(Copy value)”**。")
    readme_content.append("   - **第六步：** 打开 `fab_library_scraper.py` 文件，将您复制的 `Cookie` 值完整地粘贴到 `headers` 字典的 `cookie` 键对应的值的位置。")
    readme_content.append("     ```python")
    readme_content.append("     # fab_library_scraper.py")
    readme_content.append("     headers = {")
    readme_content.append("         'cookie': '在此处粘贴您复制的完整Cookie字符串',")
    readme_content.append("         # ... 其他请求头保持不变 ...")
    readme_content.append("     }")
    readme_content.append("     ```")
    readme_content.append("   - **注意：** Cookie 有时效性。如果脚本在未来失效并提示认证错误（如401或403），请重复此步骤更新 Cookie。")
    readme_content.append("")
    readme_content.append("2. **运行脚本**")
    readme_content.append("   在终端中运行：")
    readme_content.append("   ```bash")
    readme_content.append("   python fab_library_scraper.py")
    readme_content.append("   ```")
    readme_content.append("")
    readme_content.append("3. **查看结果**")
    readme_content.append("   运行成功后，将在项目根目录下创建一个名为 **`my_fab_assets_library`** 的文件夹。其中包含两个文件：")
    readme_content.append("   - 📄 **`my_fab_assets_library.xlsx`**")
    readme_content.append("     - **（推荐查看）** 这是一个格式精美的Excel文件，为最佳查看体验而设计。")
    readme_content.append("   - 💾 **`my_fab_assets_library.csv`**")
    readme_content.append("     - 一个标准的CSV文件，适合程序读取、数据迁移或导入其他数据库。")
    readme_content.append("")
    readme_content.append("---")
    readme_content.append("")

    # --- 工具 2: 预留位置 ---
    readme_content.append("### 2. [待开发] Fab 资产批量下载器 (`fab_asset_downloader.py`)")
    readme_content.append("")
    readme_content.append(
        "**功能设想：** 读取由 `fab_library_scraper.py` 生成的CSV或Excel文件，根据用户的选择，批量下载指定资产的源文件。")
    readme_content.append("")
    readme_content.append("> **状态：** 计划中... 欢迎贡献！")
    readme_content.append("")
    readme_content.append("---")
    readme_content.append("")

    # --- 工具 3: 预留位置 ---
    readme_content.append("### 3. [待开发] Fab 愿望单折扣监控器 (`fab_wishlist_monitor.py`)")
    readme_content.append("")
    readme_content.append("**功能设想：** 定期检查您 Fab 愿望单中的商品，当有商品开始打折时，通过邮件或其他方式发送通知。")
    readme_content.append("")
    readme_content.append("> **状态：** 计划中... 欢迎贡献！")
    readme_content.append("")
    readme_content.append("---")
    readme_content.append("")

    # 4. 贡献和许可证
    readme_content.append("## 🤝 如何贡献")
    readme_content.append("")
    readme_content.append("欢迎任何形式的贡献！无论是提交 Issue、修复 Bug，还是开发新工具，我们都非常欢迎。请遵循以下步骤：")
    readme_content.append("")
    readme_content.append("1. Fork 本仓库。")
    readme_content.append("2. 创建您的分支 (`git checkout -b feature/AmazingFeature`)。")
    readme_content.append("3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)。")
    readme_content.append("4. 推送到分支 (`git push origin feature/AmazingFeature`)。")
    readme_content.append("5. 开启一个 Pull Request。")
    readme_content.append("")
    readme_content.append("## 📄 许可证")
    readme_content.append("")
    readme_content.append("本项目采用 MIT 许可证。详情请见 `LICENSE` 文件。")

    # 拼接并写入文件
    try:
        filename = "README.md"
        content = "\n".join(readme_content)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"成功！ '{filename}' 文件已生成。")
    except Exception as e:
        print(f"错误：无法写入文件。 {e}")


if __name__ == '__main__':
    create_readme_file()