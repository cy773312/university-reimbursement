# OCR 工具检测与安装

## 检测命令

```bash
# 检查 tesseract 二进制
which tesseract

# 检查可用语言包
tesseract --list-langs

# 检查内置 OCR 脚本
python3 /Users/chenyang/.hermes/skills/productivity/university-reimbursement/scripts/ocr_images.py --help
```

## 安装命令（macOS）

```bash
# 安装 tesseract 引擎（含 eng 基础语言包）
brew install tesseract

# 安装中文语言包（简体 + 繁体，约 685MB）
brew install tesseract-lang
```

## 使用脚本

Hermes 报销 skill 内置了 OCR 脚本 `ocr_images.py`，支持批量处理：

```bash
# 批量 OCR 一个目录下的所有图片
python3 /Users/chenyang/.hermes/skills/productivity/university-reimbursement/scripts/ocr_images.py /Users/chenyang/报销/原始文件/

# 提取关键信息（金额/日期/收款方）
python3 /Users/chenyang/.hermes/skills/productivity/university-reimbursement/scripts/ocr_images.py /path/to/images/ --extract

# OCR 指定文件
python3 /Users/chenyang/.hermes/skills/productivity/university-reimbursement/scripts/ocr_images.py IMG_0014.png IMG_0015.png --extract

# 输出到 JSON 文件
python3 /Users/chenyang/.hermes/skills/productivity/university-reimbursement/scripts/ocr_images.py /path/to/ --extract -o ocr_result.json
```

### 脚本输出示例

```json
{
  "file": "IMG_0014.png",
  "success": true,
  "text": "账单\\n\\n-175.30\\n\\n支付成功\\n支付时间 2026年7月12日 14:25:18\\n商户全称 某某打车科技有限公司\\n支付方式 零钱通\\n交易单号 123456789012345678901234",
  "key_info": {
    "金额": "-175.30",
    "日期": "2026年7月12日 14:25:18",
    "收款方": "某某打车科技有限公司",
    "付款方式": "零钱通",
    "交易单号": "123456789012345678901234"
  }
}
```

## 在 Hermes 报销工作流中的使用

当 Hermes 使用无多模态能力的模型时，OCR 脚本作为视觉能力的替代方案：

1. **遇到图片文件时**，调用 `ocr_images.py --extract` 提取关键信息
2. **读取 JSON 输出**的 `key_info` 字段，提取金额、日期、收款方
3. **如果 OCR 失败或关键信息缺失**，在 Excel 中标记"缺付款记录"，放入 `待确认/信息不完整/`，并告知用户具体哪些文件无法识别

## 使用示例（Python 中调用）

```python
import subprocess
import json

def ocr_images(image_dir):
    """对目录下的所有图片执行 OCR，返回提取结果"""
    script = "/Users/chenyang/.hermes/skills/productivity/university-reimbursement/scripts/ocr_images.py"
    result = subprocess.run(
        ['python3', script, image_dir, '--extract'],
        capture_output=True, text=True, timeout=120
    )
    return json.loads(result.stdout)
```

## 备选方案

如果无法安装 tesseract：

1. **PDF 优先**：先用 `pdftotext` 处理所有 PDF（发票、行程单通常有 PDF 版）
2. **图片标记为待确认**：将截图放入 `待确认/信息不完整/`
3. **用户手动补充**：让用户告知图片中的金额/时间/收款方
4. **使用在线 OCR**：如用户有偏好工具，可导出后手动处理

## 常见图片类型

| 图片特征 | 可能内容 | 关键字段 |
|----------|----------|----------|
| 竖屏 1290×2796 | iPhone 截图 | 微信支付/支付宝账单 |
| 横屏截图 | 网页/APP 界面 | 订单确认页 |
| 照片 | 纸质发票/小票 | 需要正射校正 |
| ~700KB | 标准截图 | 单笔交易 |
| ~2-3MB | 长截图/高清 | 多笔交易或详情 |
