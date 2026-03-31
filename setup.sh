#!/bin/bash
DOTFILES="$PWD/.claude"
TARGET="$HOME/.claude"

mkdir -p "$TARGET"

# symlinkを張る（既存ファイルは上書き）
ln -sf "$DOTFILES/settings.json"  "$TARGET/settings.json"
ln -sf "$DOTFILES/CLAUDE.md"      "$TARGET/CLAUDE.md"
ln -sf "$DOTFILES/agents"         "$TARGET/agents"
ln -sf "$DOTFILES/skills"         "$TARGET/skills"
ln -sf "$DOTFILES/rules"          "$TARGET/rules"