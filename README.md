# Competitor Insight Agent

AI 驱动的竞品信息自动采集与分析助手，面向营销业务场景。

## 项目背景

在日常营销工作中，需要持续跟踪竞品动态（官网更新、产品发布、价格变化等），但人工监控效率低、容易遗漏。本项目通过自动化工具 + AI 分析，实现竞品信息的自动采集、结构化存储、智能问答和报告生成。

## 核心功能

1. **竞品数据采集**：自动抓取竞品官网的关键信息（产品介绍、定价、更新日志），并初步提取价格、产品名等结构化字段
2. **知识库构建**：将采集到的文档切片后存入向量数据库，支持语义检索
3. **智能问答**：基于 RAG 技术，检索相关片段后调用 LLM 生成回答，支持自然语言查询
4. **报告自动生成**：采集完成后自动生成结构化的 Markdown 竞品分析报告
5. **业务对象建模**：定义了"竞品公司"、"产品"、"定价方案"等业务对象及其关系

## 技术栈

- Python 3.10+
- Requests + BeautifulSoup（网页采集）
- ChromaDB（向量数据库）
- OpenAI GPT-3.5-turbo（LLM 回答生成）
- FastAPI（API 接口）

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 填入你的 OPENAI_API_KEY

# 采集竞品数据并生成报告
python main.py collect --url https://example-competitor.com

# 向知识库提问
python main.py ask --question "这个产品的定价方案有哪些？"

# 启动 API 服务
python main.py serve
# 访问 http://localhost:8000/docs 查看接口文档
```

## 效果展示

### 示例：采集后生成的竞品报告

```markdown
# example.com 竞品分析报告

> 生成时间：2026-11-01

## 一、采集概况
- 采集页面总数：5
- 成功页面数：4
- 采集成功率：80.0%

## 二、产品与定价信息
### 识别到的产品/套餐：
- 基础版
- 专业版
- 企业版

### 识别到的价格点：
- ¥99
- ¥299
- ¥999

## 三、各页面内容摘要
### 1. 首页
- 地址：https://example.com/
- 摘要：我们是一家专注于企业级 SaaS 服务的公司...
```

### 示例：RAG 问答效果

```
问题：这个产品的定价方案有哪些？

回答：根据收集到的信息，该产品主要提供三个定价方案：
1. 基础版：¥99/月，适合小型团队
2. 专业版：¥299/月，适合成长型企业
3. 企业版：定制价格，适合大型组织

信息来源：
  - https://example.com/pricing
```

## 项目结构

```
competitor-insight-agent/
├── main.py              # 入口文件
├── requirements.txt     # 依赖列表
├── .env.example         # 环境变量示例
├── data/
│   └── business_ontology.md  # 业务对象数据字典
├── src/
│   ├── collector.py         # 网页采集模块（含结构化提取）
│   ├── knowledge_base.py   # RAG 知识库（含 LLM 回答生成）
│   ├── report_generator.py  # 竞品报告生成
│   └── api.py              # FastAPI 接口
└── output/              # 采集结果输出目录
```

## 业务对象说明

详见 [data/business_ontology.md](data/business_ontology.md)

## 作者

Nh060704
