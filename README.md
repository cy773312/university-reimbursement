# 高校报销整理助手

讲座/论坛/会议/差旅/文印/图书……学术活动报销材料，扔给 AI 自动整理。

<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="MIT">
  <img src="https://img.shields.io/badge/AI-Hermes%20%7C%20Claude%20%7C%20Codex-blue" alt="AI">
  <img src="https://img.shields.io/badge/场景-高校通用-green" alt="高校">
</p>

---

## 概述

学术报销材料（发票、截图、行程单、高速费）文件杂乱，人工整理费时且易出错。本项目将整理规则写成 AI 能执行的文档，自动完成文件归并、命名规范化和 Excel 生成。

**典型场景：** 一次跨市出差打车产生 11 个文件（发票 + 支付截图 + 行程单 + 去程高速费多段 + 返程高速费 + 汇总单），AI 自动归入一个文件夹，金额核对无误。

---

## 安装

```bash
# 克隆仓库
git clone https://github.com/cy773312/university-reimbursement.git
cd university-reimbursement

# 一键安装（安装 Hermes skill + 依赖）
bash install.sh

# 验证
hermes skills list | grep university-reimbursement
```

---

## 使用

```bash
# 在你的报销目录里放好原始文件
mkdir -p ~/报销/原始文件
cp template/AGENTS.md ~/报销/

# 运行整理
cd ~/报销
hermes -s university-reimbursement

# 或直接在对话中触发
hermes chat -q "帮我整理报销材料"
```

---

## 目录结构

```
university-reimbursement/
├── skill/                          # Hermes skill（核心）
│   ├── SKILL.md                    # AI 工作规则
│   ├── references/
│   │   ├── ocr-setup.md            # OCR 配置
│   │   └── toll-fee-analysis.md    # 高速费分析案例
│   └── scripts/
│       └── read_image.py           # 图片 OCR 识别
├── template/
│   ├── AGENTS.md                   # 项目工作规则（复制到报销目录）
│   └── example/                    # 示例结构
├── docs/                           # 文档
├── install.sh                      # 一键安装
├── LICENSE
└── README.md
```

---

## 整理流程

1. **扫描**：列出所有文件，PDF 提取文字，图片 OCR 识别
2. **归类**：按金额、日期、收款方、上下文判断归属
3. **重命名**：统一编号 + 类型 + 说明
4. **核验**：发票金额 + 高速费 ≈ 实付金额
5. **输出**：生成 `报销整理表.xlsx`

### 跨市高速费处理

跨市网约车行程，高速费分两段：

- **去程（载客）**：乘客乘坐路段的高速费
- **返程（空车）**：司机送完乘客后空车返回的高速费

两部分均归入打车费文件夹，方向依据行程单的入口/出口站名判断。

---

## 支持的费用类型

| 日常用语 | 财务归类 | 所需材料 |
|---------|---------|---------|
| 机票 | 差旅交通费 | 行程单 + 支付记录 |
| 打车 | 市内交通费 | 发票 + 支付记录 + 行程单 + 高速费 |
| 住宿 | 住宿费 | 发票 + 支付记录 + 水单 |
| 高速费 | 通行费 | 归入打车文件夹 |
| 文印 | 打印/印刷费 | 发票 + 支付记录 |
| 书籍 | 图书资料费 | 发票 + 支付记录 |
| 快递 | 邮寄费 | 发票 + 支付记录 |
| 茶歇 | 会议茶歇费 | 发票 + 支付记录 |
| 劳务费 | 专家讲座费 | 发票 + 身份证 + 邀请函 |
| 场地 | 场地租赁费 | 发票 + 支付记录 |
| 用餐 | 工作餐 | 发票 + 支付记录 |

---

## 图片识别

| 路径 | 条件 | 方式 |
|------|------|------|
| 视觉识别 | 大模型支持多模态 | 直接调用 vision_analyze |
| OCR 兜底 | 纯文本模型或离线 | `scripts/read_image.py` |

---

## 许可证

MIT
