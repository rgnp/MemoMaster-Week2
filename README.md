# **🎙️ MemoMaster: 基于 Groq LPU 的极速智能会议纪要系统**

**"天下武功，唯快不破。"** —— MemoMaster 利用 Groq 的 LPU 芯片技术，实现了毫秒级的语音转写，并结合 DeepSeek 大模型进行智能总结。

## **📸 Demo 演示**

## **💡 项目背景**

在传统的会议记录或视频学习场景中，我们面临两大痛点：

1. **听写慢**：OpenAI Whisper 虽然准确，但推理速度较慢，处理 1 小时音频通常需要数分钟。  
2. **整理难**：转写出的文字往往缺乏标点、逻辑混乱，人工整理耗时耗力。

本项目 **MemoMaster** 旨在打造一个“录音即笔记”的生产力工具，通过 **Pipeline Cleaning (流水线清洗)** 策略，完美解决了上述问题。

## **🛠️ 核心技术栈 (My AI Arsenal \- Week 2\)**

| 组件 | 技术选型 | 核心作用 | 为什么选它？ |
| :---- | :---- | :---- | :---- |
| **耳朵 (Hearing)** | **Groq API** (Whisper-large-v3) | 语音转文字 | **速度极快** (LPU 架构)，比传统 GPU 推理快 10 倍以上。 |
| **大脑 (Brain)** | **DeepSeek API** (V3) | 文本清洗 & 总结 | **中文能力强**，擅长处理长文本和逻辑归纳。 |
| **清洗 (Cleaning)** | **Prompt Engineering** | 修复标点/幻觉 | 解决了 Whisper 在静音片段产生幻觉的问题。 |
| **前端 (UI)** | **Streamlit** | 交互界面 | 快速构建可视化 Web 应用，支持文件上传与实时反馈。 |

## **⚙️ 工程架构与挑战解决**

### **1\. 解决 "Whisper 幻觉" 问题**

挑战：在音频开头或静音处，Groq (Whisper) 经常会产生幻觉，输出 "请使用简体中文" 等无关文字，且经常丢失标点。  
方案：采用 Pipeline 解耦 策略。

* **Step 1 (听)**：Groq 只负责快速转写，不加 Prompt，防止幻觉。  
* **Step 2 (修)**：引入 DeepSeek 作为“洗稿工”，专门负责修复标点符号和分段。  
* **Step 3 (写)**：修复后的文本再送入 DeepSeek 进行结构化总结。

### **2\. 动态 API Key 管理**

挑战：为了让项目具备通用性，不能将 API Key 写死在代码中。  
方案：实现了 混合鉴权机制。优先读取本地 .env 环境配置，若不存在，则动态在 UI 侧边栏请求用户输入。

## **🚀 快速开始 (Quick Start)**

### **1\. 克隆仓库**

```bash
git clone https://github.com/rgnp/MemoMaster-Week2.git
cd MemoMaster-Week2
```

### **2\. 安装依赖**

```bash
# 建议使用虚拟环境  
python -m venv .venv  
source .venv/bin/activate 

pip install -r requirements.txt
```

### **3\. 配置密钥 (可选)**

创建 .env 文件：

```
GROQ_API_KEY=gsk_xxxxxxxxxxxx  
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxx  
DEEPSEEK_BASE_URL=https://api.deepseek.com
```

### **4\. 运行应用**

```
streamlit run src/app.py
```

## **📝 学习心得 (My Learning Path)**

* **API 组合拳**：学会了如何串联不同的模型（Whisper \+ DeepSeek）来弥补单一模型的短板。  
* **工程化思维**：从随手写代码进化到标准的目录结构 (src/utils.py) 和版本控制。  
* **产品体验**：通过 Streamlit 的 st.download\_button 和 st.expander 提升了用户体验。

## **🔮 Future Work**

* \[ \] 支持 YouTube 链接直接解析  
* \[ \] 增加“思维导图”的一键渲染功能  
* \[ \] 引入向量数据库 (RAG) 以支持对超长会议记录的问答

*Built with ❤️ by \[RGNP\] \- A Computer Science Graduate Student*