import os
from groq import Groq
from dotenv import load_dotenv
import time

# 1. 加载配置
load_dotenv()

# 2. 创建Groq对象
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def test_speed_chat():
    print("\n--- 测试 1: 体验 LPU 的速度 (Llama 3 8B) ---")
    start_time = time.time()

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": "请用中文写一段50字绕口令."}
        ],
        temperature=0.7,
    )

    end_time = time.time()
    content = completion.choices[0].message.content

    print(f"AI 回复:{content}")
    print(f"耗时: {end_time - start_time:.4f} 秒")

def test_json_mode():
    print("\n--- 测试 2: 强制 JSON 输出 (用于数据提取) ---")

    user_input = "张三 (男) 13800138000; 李四 (女) 13900139000"

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "提取用户信息，返回 JSON 对象，格式为：{'users': [{'name': '...', 'phone': '...'}]}"},
            {"role": "user", "content": user_input}
        ],
        response_format={"type": "json_object"},
    )
    print(f"原始 JSON: {completion.choices[0].message.content}")

if __name__ == "__main__":
    test_speed_chat()
    test_json_mode()