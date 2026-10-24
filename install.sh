#!/usr/bin/env bash
# 一键把 myCFO 安装为 DSH profile 插件。
#   ./install.sh              # 用当前目录安装到 desktop profile
#   ./install.sh web          # 装到 web profile
#   ./install.sh desktop --github   # 自动从 GitHub 拉取后安装
#   ./install.sh desktop --remove   # 卸载
set -euo pipefail

PROFILE="${1:-desktop}"
ACTION="${2:-install}"
REPO_URL="https://github.com/whoisjackchao-dot/myCFO.git"
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

if [ "$ACTION" = "--github" ]; then
  TMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/mycfo-XXXXXX")"
  echo "从 GitHub 拉取到 $TMP_DIR ..."
  git clone --depth 1 "$REPO_URL" "$TMP_DIR"
  SRC="$TMP_DIR"
fi

echo "安装 myCFO 插件到 profile '$PROFILE'"
echo "  来源: $SRC"
dsh plugin --profile "$PROFILE" add "$SRC"

echo
echo "完成。请重启 DSH，然后在会话里说："
echo "  「帮我做一次公司体检」「这个月要交多少税」「要不要转一般纳税人」"
echo
echo "更新：重新运行本脚本；或 dsh plugin --profile $PROFILE update dsh-mycfo"
