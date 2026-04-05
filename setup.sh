#!/bin/bash
DOTFILES="$PWD/.claude"
TARGET="$HOME/.claude"

# ターゲットディレクトリを作成（存在しない場合）
mkdir -p "$TARGET"

# 既存のターゲット（シンボリックリンク予定のパス）があれば削除し、シンボリックリンクを張る
ITEMS=("settings.json" "CLAUDE.md" "agents" "hooks" "rules" "skills")
for item in "${ITEMS[@]}"; do
    if [ -e "$TARGET/$item" ] || [ -L "$TARGET/$item" ]; then
      rm -rf "${TARGET:?}/$item"
    fi
    ln -sf "$DOTFILES/$item" "$TARGET/$item"
done

# シンボリックリンクのみを確認
for item in "${ITEMS[@]}"; do
    if [ -L "$TARGET/$item" ]; then
        echo "$TARGET/$item -> $(readlink "$TARGET/$item")"
    fi
done