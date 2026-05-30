<div align="center">

# 高校报销整理助手

**把乱糟糟的发票、截图、行程单扔给 AI，自动归类出表。**

讲座 · 论坛 · 会议 · 差旅 · 文印 · 图书

<br>

![License](https://img.shields.io/badge/license-MIT-blue)
![场景](https://img.shields.io/badge/场景-高校-green)

</div>

---

这是一个 **Hermes Agent skill**：把你的报销材料目录交给 AI，它自动扫描所有 PDF 和图片，按费用归类，重命名文件，生成汇总 Excel。

---

## 整理前 vs 整理后

```
原始文件/                         已整理/
├── IMG_001.png               ├── 2026-07-01_机票_北京至上海_1260 元/
├── wxpay_screenshot.jpg       │   ├── 01_发票.pdf
├── fapiao(2).pdf              │   ├── 02_付款记录_微信支付.png
├── 行程单.pdf                 │   └── 03_订单.png
├── 酒店水单.pdf               ├── 2026-07-01_打车_机场至酒店_168 元/
├── 微信图片_20260701.jpg      │   ├── 01_发票.pdf
├── didi_fapiao.pdf            │   ├── 02_付款记录.png
└── ... (16 more files)        │   ├── 03_订单.png
                               │   └── 04_行程单.pdf
                               ├── 2026-07-01_住宿_锦江之星_298 元/
                               ├── 2026-07-02_机票_上海至北京_1360 元/
                               └── 报销整理表.xlsx
```

左边一锅粥，右边清清爽爽。**耗时：从半小时变成两分钟。**

---

## 安装

```bash
git clone https://github.com/cy773312/university-reimbursement.git
cd university-reimbursement
bash install.sh
```

## 使用

```bash
# 在你的报销目录里放好所有原始材料
cp template/AGENTS.md ~/报销/
cd ~/报销 && hermes -s university-reimbursement
```

---

## 覆盖的费用类型

机票、打车（含高速费）、住宿、文印、图书、快递、茶歇、劳务费、场地租赁、用餐……

AI 会自动识别文件类型，提取关键信息（金额、日期、收款方），按一笔费用一个文件夹归并。

---

## 核心理念

- **AI 做归类，人做决策**——AI 扫描分析，标记疑问，你来确认
- **命名让人一眼看懂**——"机票"比"专家差旅费"直观
- **金额必须对上**——对不上的标出来
- **通用覆盖大多数场景**——特殊需求按需补充，不塞进核心逻辑

---

## License

MIT
