import streamlit as st
import tempfile
import os
from utils import transcribe_audio, summarize_text, format_transcript # 记得导入新函数

st.set_page_config(page_title="MemoMaster AI", layout="wide")
st.title("🎙️ MemoMaster: 智能会议纪要")
st.caption("Week 2 Project: Powered by Groq (Whisper-v3) & DeepSeek")

# 初始化状态
if "transcript" not in st.session_state:
    st.session_state.transcript = ""
if "summary" not in st.session_state:
    st.session_state.summary = ""

# 侧边栏：上传
with st.sidebar:
    st.header("📂 上传文件")
    uploaded_file = st.file_uploader("选择录音/视频文件", type=["mp3","m4a","wav","mp4"])

    if uploaded_file:
        if st.button("开始分析"):
            with st.spinner("🎧 AI 正在听写 (Groq 加速中)..."):
                # 1. 保存临时文件
                # 注意：Groq 限制文件大小约 25MB。如果太大需要切片（进阶课再讲）。
                suffix = os.path.splitext(uploaded_file.name)[1]
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    tmp.write(uploaded_file.getvalue())
                    tmp_path = tmp.name

                try:
                    # 2. 转写 (拿到的是无标点的生肉)
                    raw_text = transcribe_audio(tmp_path)

                    # 🔥 新增步骤：清洗数据 (把生肉煮熟)
                    with st.spinner("✨ 正在修复标点符号..."):
                        # 如果你有 user_api_key 就传，没有就用默认的
                        polished_text = format_transcript(raw_text)

                    # 把修好的文字存进状态
                    st.session_state.transcript = polished_text
                    st.success("听写 & 修复完成！")

                    # 3. 总结
                    with st.spinner("🧠 AI 正在总结..."):
                        summary = summarize_text(polished_text)
                        st.session_state.summary = summary
                except Exception as e:
                    st.error(f"发生错误: {e}")

                finally:
                    os.remove(tmp_path)  

# 主面板：听写结果
# col1, col2 = st.columns([1, 1])

# with col1:
#     st.subheader("📝 语音转写原文")
#     st.text_area("Transcript", st.session_state.transcript, height=600)

# with col2:
#     st.subheader("💡 智能总结笔记")
#     if st.session_state.summary:
#         st.markdown(st.session_state.summary)

#         # 尝试渲染 Mermaid 思维导图
#         # Streamlit 原生不支持 Mermaid，但我们可以用 markdown 扩展
#         # 这是一个小彩蛋功能
#         if "```mermaid" in st.session_state.summary:
#             st.info("检测到思维导图结构，请复制到 Mermaid Live Editor 查看。")

# 1. 显示原文 (使用折叠面板，节省空间)
with st.expander("📝 查看语音转写原文", expanded=False):
    st.text_area("Transcript", st.session_state.transcript, height=300)

# 2. 显示总结 (作为主内容展示)
if st.session_state.summary:
    st.divider() # 画一条分割线
    st.subheader("💡 智能总结笔记")
    st.markdown(st.session_state.summary)
    
    # --- 新增功能：下载按钮 ---
    # data: 要下载的内容
    # file_name: 下载后的文件名
    # mime: 文件类型 (纯文本用 text/plain)
    st.download_button(
        label="📥 下载笔记 (.txt)",
        data=st.session_state.summary,
        file_name="meeting_notes.txt",
        mime="text/plain"
    )