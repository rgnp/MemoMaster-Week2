import os
from dotenv import load_dotenv
from groq import Groq
from openai import OpenAI

# 加载环境变量
load_dotenv()

def transcribe_audio(file_path):
    """
    【API 调用 1】使用 Groq (Whisper-v3) 进行极速语音转文字
    输入：音频文件路径
    输出：转写后的全文 (String)
    """
    print(f"[Log] 正在调用 Groq 听写: {file_path}...")

    # 初始化 Groq 客户端
    client = Groq(
        api_key = os.getenv("GROQ_API_KEY"),
    )

    with open(file_path, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(file_path, file.read()),
            model="whisper-large-v3",
            response_format = "json",
            language="zh",
            temperature=0.0
        )

    return transcription.text

def format_transcript(raw_text):
    """
    【新函数】专门用 DeepSeek 给文字加标点和分段
    """
    print("[Log] 正在调用 DeepSeek 修复标点...")
    
    # 简单的逻辑：如果文本太短，就不修了，省钱
    if len(raw_text) < 5: return raw_text

    client = OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"), 
        base_url=os.getenv("DEEPSEEK_BASE_URL")
    )

    system_prompt = """
    你是一个文字排版助手。
    用户会输入一段语音转写的文本，可能完全没有标点，或者有错别字。
    请重新排版这段文字：
    1. 添加正确的标点符号。
    2. 适当分段。
    3. 修正明显的同音错别字。
    4. **绝对不要**删减或改写原文含义，只做格式修复。
    5. 直接输出修复后的文本，不要包含任何“好的”、“修复如下”等废话。
    """

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": raw_text[:10000]} # 限制长度防止报错
        ],
        temperature=0.1
    )
    return response.choices[0].message.content

def summarize_text(text):
    """
    【API 调用 2】使用 DeepSeek 进行会议纪要总结
    """
    print(f"[Log] 正在调用 DeepSeek 总结，字数: {len(text)}...")

    client = OpenAI(
        api_key = os.getenv("DEEPSEEK_API_KEY"),
        base_url = os.getenv("DEEPSEEK_BASE_URL")
    )

    system_prompt = """
    你是一个专业的会议/视频内容整理助手。
    请阅读以下语音转写的文本，生成一份结构化的笔记。
    
    要求输出格式：
    1. 【一句话摘要】：30字以内概括核心内容。
    2. 【关键要点】：使用 Bullet points 列出 3-5 个核心观点。
    3. 【行动项/结论】：如果有下一步计划或明确结论，请列出。
    4. 【思维导图代码】：请生成 Mermaid 格式的思维导图代码，放在 ```mermaid ... ``` 代码块中。
    """
    # system_prompt = """
    # 你是一个专业的文本处理助手。
    
    # 【任务 1：清洗文本】
    # 用户提供的语音转写文本可能**完全没有标点符号**，或者有错别字。
    # 请首先在脑海中修复这些标点和错误。
    
    # 【任务 2：生成笔记】
    # 基于修复后的文本，生成一份结构化的微博风格文案。
    # 要求：
    # 1. 语气激动，带 Emoji
    # 2. 100字左右
    # """


    # 防止文本太长爆 Token，这里做个简单截断（Groq 支持很长，但 LLM 有上限）
    # 实际生产中应用 RAG，这里简化处理
    text = text[:10000]

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ],
        temperature=0.1
    )

    return response.choices[0].message.content