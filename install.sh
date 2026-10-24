#!/usr/bin/env bash
# 一键把 myCFO 安装为 DSH profile 插件。
#   ./install.sh            # 装到 desktop profile
#   ./install.sh web        # 装到 web profile
#   ./install.sh desktop --remove
set -euo pipefail

PROFILE="${1:-desktop}"
ACTION="${2:-install}"
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if ! command -v dsh >/dev/null 2>&1; then
  echo "未找到 dsh 命令。请先安装 DeepSeek Harness（npm i -g @deepseek-ai/dsh）。" >&2
  exit 1
fi

if [ "$ACTION" = "--remove" ]; then
  echo "从 profile '$PROFILE' 移除 myCFO 插件..."
  dsh plugin --profile "$PROFILE" remove dsh-mycfo
  echo "已移除。重启 DSH 生效。"
  exit 0
fi

echo "安装 myCFO 插件到 profile '$PROFILE'"
echo "  来源: $SRC"
dsh plugin --profile "$PROFILE" add "$SRC"

echo
echo "完成。请重启 DSH，然后在会话里说："
echo "  「帮我做一次公司体检」「这个月要交多少税」「要不要转一般纳税人」"
