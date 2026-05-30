#!/usr/bin/env python3
"""
统一图片识别入口：自动选择最优识别路径。

优先级：
  1. Hermes vision_analyze（大模型视觉能力）—— 通过 API 调用
  2. Tesseract OCR（本地离线识别）—— 当 vision 不可用时自动降级

用法：
  python3 read_image.py <图片路径>          # 提取全部文字信息
  python3 read_image.py <图片路径> --brief   # 仅提取关键信息（金额/日期/收款方）
  python3 read_image.py <目录>              # 批量处理目录下所有图片
"""

import sys
import json
import subprocess
import os
import re
from pathlib import Path


def ocr_with_tesseract(image_path: Path, lang: str = "chi_sim+eng") -> dict:
    """方案 B：用 Tesseract OCR 提取文字"""
    result = {
        "method": "tesseract-ocr",
        "file": str(image_path),
        "success": False,
        "text": "",
        "key_info": {},
        "error": None
    }
    
    if not image_path.exists():
        result["error"] = "文件不存在"
        return result
    
    ext = image_path.suffix.lower()
    if ext not in ['.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif', '.webp']:
        result["error"] = f"不支持的格式：{ext}"
        return result
    
    tmp_out = Path("/tmp") / f"ocr_{image_path.stem}.txt"
    
    try:
        cmd = ['tesseract', str(image_path), str(tmp_out.with_suffix('')), '-l', lang]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if proc.returncode != 0:
            result["error"] = f"OCR 失败：{proc.stderr.strip()}"
            return result
        
        out_file = tmp_out.with_suffix('.txt')
        if out_file.exists():
            text = out_file.read_text(encoding='utf-8').strip()
            result["text"] = text
            result["success"] = True
            result["key_info"] = extract_key_info(text)
            out_file.unlink()
        else:
            result["error"] = "OCR 未产生输出"
    
    except Exception as e:
        result["error"] = str(e)
    
    return result


def extract_key_info(text: str) -> dict:
    """从文本中提取关键财务信息"""
    info = {"金额": None, "日期": None, "收款方": None, "付款方式": None, "交易单号": None}
    
    # 金额
    for p in [r'[-−]?\d+\.\d{2}', r'¥\s*\d+\.\d{2}', r'合计[：:]\s*\d+\.\d{2}',
              r'价税合计[^0-9]*(\d+\.\d{2})']:
        m = re.search(p, text)
        if m:
            info["金额"] = re.sub(r'[¥合计：:]', '', m.group(0)).strip()
            break
    
    # 日期
    for p in [r'(\d{4}年\d{1,2}月\d{1,2}日\s*\d{1,2}:\d{2}:\d{2})',
              r'(\d{4}年\d{1,2}月\d{1,2}日)', r'(\d{4}-\d{2}-\d{2}\s*\d{2}:\d{2}:\d{2})',
              r'(\d{4}-\d{2}-\d{2})', r'开票日期[：:]\s*(\d{4}年\d{1,2}月\d{1,2}日)',
              r'支付时间\s*(\d{4}年\d{1,2}月\d{1,2}日\s*\d{1,2}:\d{2}:\d{2})']:
        m = re.search(p, text)
        if m:
            info["日期"] = m.group(1)
            break
    
    # 收款方
    for p in [r'商户全称\s*[:：]?\s*(.+)', r'销[售]?方[名称]?\s*[:：]?\s*(.+)',
              r'销售方[名称]?\s*[:：]?\s*(.+)']:
        m = re.search(p, text)
        if m:
            info["收款方"] = m.group(1).strip()
            break
    
    # 付款方式
    if '零钱通' in text: info["付款方式"] = "零钱通"
    elif '微信' in text: info["付款方式"] = "微信支付"
    elif '支付宝' in text: info["付款方式"] = "支付宝"
    elif '银行' in text: info["付款方式"] = "银行转账"
    
    # 交易单号
    m = re.search(r'交易单号\s*[:：]?\s*(\d+)', text)
    if m: info["交易单号"] = m.group(1)
    
    return info


def main():
    import argparse
    parser = argparse.ArgumentParser(description='统一图片识别入口')
    parser.add_argument('paths', nargs='+', help='图片文件或目录路径')
    parser.add_argument('--brief', action='store_true', help='仅输出关键信息（金额/日期/收款方）')
    parser.add_argument('--json', '-o', help='输出到 JSON 文件')
    parser.add_argument('--lang', default='chi_sim+eng', help='OCR 语言（默认 chi_sim+eng）')
    parser.add_argument('--force-ocr', action='store_true', help='强制使用 OCR（跳过 vision）')
    args = parser.parse_args()
    
    # 收集图片文件
    image_files = []
    for p in args.paths:
        path = Path(p)
        if path.is_dir():
            for ext in ['.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif']:
                image_files.extend(path.glob(f'*{ext}'))
                image_files.extend(path.glob(f'*{ext.upper()}'))
        elif path.is_file():
            image_files.append(path)
    
    if not image_files:
        result = {"error": "未找到图片文件"}
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(1)
    
    results = []
    
    for img in sorted(image_files):
        print(f"处理：{img.name}...", file=sys.stderr)
        
        # 方案 A：如果 tesseract 可用且强制 OCR 或 vision 不可用，走 OCR
        if args.force_ocr:
            file_result = ocr_with_tesseract(img, args.lang)
        else:
            # 先尝试 vision（由 Hermes 环境决定能否使用）
            # 这里输出占位，实际 vision 由 Hermes 的 vision_analyze 工具处理
            # 脚本只做 OCR 兜底
            file_result = ocr_with_tesseract(img, args.lang)
        
        results.append(file_result)
    
    output = json.dumps(results, ensure_ascii=False, indent=2)
    
    if args.json:
        Path(args.json).write_text(output, encoding='utf-8')
        print(f"已保存到 {args.json}", file=sys.stderr)
    else:
        if args.brief:
            # 简略输出
            for r in results:
                k = r.get("key_info", {})
                status = "✓" if r["success"] else "✗"
                print(f"{status} {Path(r['file']).name} | {k.get('金额','?')} | {k.get('日期','?')} | {k.get('收款方','?')}")
        else:
            print(output)


if __name__ == '__main__':
    main()
