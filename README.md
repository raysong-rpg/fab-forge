# Fab-Forge 锻造厂 🛠️

> 一系列旨在增强您在 Fab.com 平台体验的实用工具集合。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📖 项目简介

`fab-forge` 是一个开源项目，致力于为 Fab.com 用户提供一系列自动化、高效的工具。无论您是想备份自己的资产库、监控商品折扣，还是进行其他批量操作，这里都希望能为您提供解决方案。

本项目的所有工具都基于 Python 编写，并尽可能提供清晰的说明和简单的使用方法。

---

## ⚙️ 安装与准备

1. **克隆仓库**
   ```bash
   git clone https://github.com/raysong-rpg/fab-forge.git
   cd fab-forge
   ```

2. **安装依赖**
   项目的所有依赖项都已在 `requirements.txt` 文件中列出。
   建议在虚拟环境中安装：
   ```bash
   pip install -r requirements.txt
   ```

---

## 🧰 工具列表

### 1. Fab 库资产导出器 (`fab_library_scraper.py`)

**功能描述：** 登录您的 Fab 账户，自动抓取您已拥有的 **全部** 资产，并将其详细信息导出为 `.csv` 和 `.xlsx` 两种格式的文件。

**核心特性：**
- **完整导出：** 通过模拟排序操作，成功绕过“数据注水”技术，确保获取到您资产库中的每一项内容。
- **双格式输出：** 同时生成 `.xlsx` (Excel) 和 `.csv` 文件，兼顾了人类阅读的便利性与数据的可移植性。
- **详细字段：** 导出内容包括资产名、类型、详情页URL、价格、货币、入库日期、UID以及新增的 `Notes` (备注) 字段。
- **智能容错与标记：** 能够自动处理API返回的不规范数据（如缺失的价格信息），确保脚本不会中途崩溃，并会在 `Notes` 列中对这些特殊条目进行标注。
- **智能防护：** 集成了 `cloudscraper` 库，能够自动应对 Cloudflare 的 JavaScript 验证。

#### 使用说明

1. **【关键步骤】更新认证信息 (Cookie)**
   - 由于需要访问您的私人资产库，脚本必须使用您的登录凭证。最简单的方式就是提供 `Cookie`。
   - **第一步：** 在浏览器中登录您的 Fab 账户。
   - **第二步：** **点击以下链接**，直接访问一个能触发API请求的页面：
     > [https://www.fab.com/library?sort_by=createdAt](https://www.fab.com/library?sort_by=createdAt)
   - **第三步：** 在该页面上，按下 `F12` 打开开发者工具，并进行以下关键设置：
     - (a) 切换到 **“网络(Network)”** 标签页。
     - (b) **勾选** 筛选栏中的 **“保留日志 (Preserve log)”** 复选框。
     - (c) **选中** 筛选器中的 **“Fetch/XHR”** 类别。

   - **第四步：** **强制刷新** 页面 (`Ctrl + Shift + R`)。然后，您会在请求列表中看到一个以 `search?sort_by=createdAt` 开头的请求。点击它。

   - **第五步：** 在右侧的 **“标头(Headers)”** 部分，找到 **“请求标头(Request Headers)”**，然后复制其中 `cookie:` 字段的 **全部值**。
   - **第六步：** 打开 `fab_library_scraper.py` 文件，将您复制的 `Cookie` 值粘贴到 `headers` 字典的相应位置。
     ```python
     headers = {
         # ... 其他标头
         'cookie': '在此处粘贴您复制的完整Cookie字符串',
         # ... 其他标头
     }
     ```
   - **注意：** Cookie 有时效性，如果脚本在未来失效并提示认证错误，请重复此步骤更新 Cookie。

2. **运行脚本**
   在终端中运行：
   ```bash
   python fab_library_scraper.py
   ```

3. **查看结果**
   运行成功后，将在项目根目录下生成 **两个文件**：
   - 📄 **`my_fab_assets_library.xlsx`**
     - **（推荐查看）** 这是一个格式化的Excel文件，为最佳查看体验设计。URL可直接点击，列宽已自动调整。
   - 💾 **`my_fab_assets_library.csv`**
     - 一个标准的CSV文件，URL被处理为Excel兼容的`HYPERLINK`公式。适合程序读取、数据迁移或导入其他数据库。

---

### 2. [待开发] Fab 资产批量下载器 (`fab_asset_downloader.py`)

**功能设想：** 读取由 `fab_library_scraper.py` 生成的CSV或Excel文件，根据用户的选择，批量下载指定资产的源文件。

> **状态：** 计划中... 欢迎贡献！

---

### 3. [待开发] Fab 愿望单折扣监控器 (`fab_wishlist_monitor.py`)

**功能设想：** 定期检查您 Fab 愿望单中的商品，当有商品开始打折时，通过邮件或其他方式发送通知。

> **状态：** 计划中... 欢迎贡献！

---

## 🤝 如何贡献

欢迎任何形式的贡献！无论是提交 Issue、修复 Bug，还是开发新工具，我们都非常欢迎。请遵循以下步骤：

1. Fork 本仓库。
2. 创建您的分支 (`git checkout -b feature/AmazingFeature`)。
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)。
4. 推送到分支 (`git push origin feature/AmazingFeature`)。
5. 开启一个 Pull Request。

## 📄 许可证

本项目采用 MIT 许可证。详情请见 `LICENSE` 文件。