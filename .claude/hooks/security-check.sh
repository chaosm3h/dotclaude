#!/bin/bash
# git commit 実行時にステージング済みファイルの秘密情報をスキャン
INPUT=$(cat)
CMD=$(echo "$INPUT" | jq -r '.tool_input.command // ""')

if echo "$CMD" | grep -q 'git commit'; then
  SECRETS=$(git diff --cached 2>/dev/null | grep -Ei '(api[_-]?key|secret|password|token|private[_-]?key)\s*[:=]\s*["'"'"'][^"'"'"']{8,}' 2>/dev/null)
  if [ -n "$SECRETS" ]; then
    printf '{"continue":false,"stopReason":"セキュリティ警告: ステージされたファイルにハードコードされた秘密情報が検出されました。コミットをブロックしました。"}'
  fi
fi