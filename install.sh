#!/usr/bin/env bash
set -e

# university-reimbursement 安装脚本
# 安装 Hermes skill 及依赖

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DEST="$HOME/.hermes/skills/productivity/university-reimbursement"

echo "📦 安装高校报销整理助手..."
echo ""

# 1. 安装 Hermes skill
echo "▸ 安装 Hermes skill..."
mkdir -p "$SKILL_DEST"/{references,scripts}
cp -r "$REPO_DIR"/skill/SKILL.md "$SKILL_DEST/"
cp -r "$REPO_DIR"/skill/references/* "$SKILL_DEST/references/" 2>/dev/null || true
cp -r "$REPO_DIR"/skill/scripts/* "$SKILL_DEST/scripts/" 2>/dev/null || true
echo "  ✓ skill 已安装到 $SKILL_DEST"

# 2. 检测 tesseract（OCR 依赖）
echo "▸ 检测 OCR 依赖..."
if command -v tesseract &>/dev/null; then
    echo "  ✓ tesseract 已安装"
else
    echo "  ⚠ tesseract 未安装"
    echo "    安装命令: brew install tesseract tesseract-lang"
    echo "    或跳过此步（仅视觉模型可用时无需 OCR）"
fi

# 3. 使用说明
echo ""
echo "✅ 安装完成"
echo ""
echo "使用方法："
echo "  1. 在你的报销目录中放入 template/AGENTS.md"
echo "     cp template/AGENTS.md ~/报销/"
echo ""
echo "  2. 将原始材料放入 原始文件/ 目录"
echo ""
echo "  3. 运行整理"
echo "     cd ~/报销 && hermes -s university-reimbursement"
echo "     或: hermes chat -q \"帮我整理报销材料\""
echo ""
echo "更多说明见 README.md"
