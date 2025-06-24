# 02_enrich_data/services/deepseek_client.py

# 首先，确保你已经安装了openai库: pip install openai
from openai import OpenAI, OpenAIError

# 从我们的配置文件中导入所需信息
# 原来的错误代码:
# from ..config import ...

# 修改为:
from ..config import DEEPSEEK_API_KEY, DEEPSEEK_MODEL, DEEPSEEK_PROMPT_TEMPLATE

# --- 初始化客户端 ---
# 检查API Key是否已配置
if not DEEPSEEK_API_KEY or "sk-xxx" in DEEPSEEK_API_KEY:
    print("[DeepSeek Client] 警告: API Key未在config.py中配置，AI功能将不可用。")
    client = None
else:
    # 按照官方示例，初始化一个全局的client实例
    # 这样可以复用连接，提高效率
    client = OpenAI(
        base_url="https://api.deepseek.com/v1",  # 官方推荐使用/v1路径
        api_key=DEEPSEEK_API_KEY
    )


def get_summary_from_deepseek(title: str, description: str, technical_details: str) -> str:
    """
    使用与OpenAI兼容的SDK，调用DeepSeek API生成资产简介。

    Args:
        title (str): 资产标题。
        description (str): 资产的原始英文描述。
        technical_details (str): 资产的技术细节。

    Returns:
        str: AI生成的中文简介，或一条错误/提示信息。
    """
    # 如果客户端没有被成功初始化，直接返回提示信息
    if client is None:
        return "DeepSeek客户端未初始化 (请检查config.py中的API Key)"

    # 使用 f-string 和模板来动态生成最终的prompt
    user_prompt = DEEPSEEK_PROMPT_TEMPLATE.format(
        title=title,
        description=description,
        technical_details=technical_details
    )

    try:
        # 按照官方示例调用 client.chat.completions.create
        completion = client.chat.completions.create(
            model=DEEPSEEK_MODEL,
            messages=[
                # 这里的system message可以留空，因为我们的主要指令在user_prompt里
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=400  # 稍微增加一些token，以防简介被截断
        )

        # 从返回结果中提取内容
        summary = completion.choices[0].message.content
        return summary.strip()

    except OpenAIError as e:
        # openai库会抛出它自己的特定错误类型，捕获它们
        print(f"  [DeepSeek] API调用时发生错误: {e}")
        return f"DeepSeek API调用失败: {e.type}"
    except Exception as e:
        print(f"  [DeepSeek] 发生未知错误: {e}")
        return "调用DeepSeek时发生未知错误"